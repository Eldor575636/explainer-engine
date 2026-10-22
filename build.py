#!/usr/bin/env python3
"""Build a vertical explainer from numbered images + voiceover + exact script.
Usage: python3 build.py <project_dir>
project_dir must contain: raw.wav, words.json (whisper), script.json, NN.jpg images.
script.json: {"sentences": [...], "scenes": [[first_sentence_index, image, label], ...]}
"""
import json, re, subprocess, sys, difflib
from pathlib import Path

W, H, FPS = 1080, 1920, 30
NAVY, MUSTARD = "0x1B2A4A", "0xD4A23A"
ZOOM = 0.10
FONTS = Path(__file__).parent / "fonts"
KEEP_PAUSE = 0.32      # longest pause kept between sentences (seconds)
PAD = 0.12             # breathing room kept around speech


def sh(cmd, cwd=None, capture=False):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, check=True,
                       capture_output=capture, text=True)
    return r.stderr if capture else None


def norm(s):
    s = s.lower()
    for a in "‘’ʻʼ`´":
        s = s.replace(a, "'")
    return re.sub(r"[^\w']", "", s)


# ---------- 1. align script words to whisper words ----------
def align(script_words, asr):
    a = [norm(w) for w in script_words]
    b = [norm(w[0]) for w in asr]
    n, m = len(a), len(b)
    GAP = -0.6
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * GAP; back[i][0] = 1
    for j in range(1, m + 1):
        score[0][j] = j * GAP; back[0][j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sim = difflib.SequenceMatcher(None, a[i-1], b[j-1]).ratio()
            opts = (score[i-1][j-1] + (sim * 2 - 0.8), score[i-1][j] + GAP, score[i][j-1] + GAP)
            k = max(range(3), key=lambda x: opts[x])
            score[i][j], back[i][j] = opts[k], k
    match = [None] * n
    i, j = n, m
    while i > 0 or j > 0:
        k = back[i][j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if k == 0:
            if difflib.SequenceMatcher(None, a[i-1], b[j-1]).ratio() >= 0.45:
                match[i-1] = j-1
            i, j = i-1, j-1
        elif k == 1:
            i -= 1
        else:
            j -= 1
    # timings, interpolate unmatched
    times = [(asr[k][1], asr[k][2]) if k is not None else None for k in match]
    known = [i for i, t in enumerate(times) if t]
    for i in range(n):
        if times[i] is None:
            prev = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            t0 = times[prev][1] if prev is not None else 0.0
            t1 = times[nxt][0] if nxt is not None else t0 + 0.4
            span = (nxt if nxt is not None else n) - (prev if prev is not None else -1)
            pos = i - (prev if prev is not None else -1)
            s = t0 + (t1 - t0) * (pos - 0.5) / span
            times[i] = (s, s + 0.25)
    return times, sum(k is not None for k in match)


# ---------- 2. find speech regions and shorten pauses ----------
def speech_regions(wav, total):
    log = sh(["ffmpeg", "-i", wav, "-af", "silencedetect=noise=-40dB:d=0.3", "-f", "null", "-"],
             capture=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = list(zip(starts, ends + [total] * (len(starts) - len(ends))))
    keep, cur = [], 0.0
    for s, e in sil:
        if s - cur > 0.15:
            keep.append([max(0.0, cur - PAD), min(total, s + PAD)])
        cur = e
    if total - cur > 0.15:
        keep.append([max(0.0, cur - PAD), total])
    # merge overlaps, then make sure no kept pause is longer than KEEP_PAUSE
    merged = []
    for s, e in keep:
        if merged and s <= merged[-1][1] + 0.01:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


def make_timemap(regions):
    """old time -> new time after cutting the gaps between regions down."""
    pieces, t = [], 0.0
    for i, (s, e) in enumerate(regions):
        gap = 0.0 if i == 0 else min(KEEP_PAUSE - 2 * PAD, s - regions[i-1][1])
        gap = max(gap, 0.0)
        t += gap
        pieces.append((s, e, t))
        t += e - s
    def f(x):
        for s, e, ns in pieces:
            if x < s:
                return ns
            if x <= e:
                return ns + (x - s)
        return t
    return f, pieces, t


# ---------- 3. render ----------
def render_scene(d, img, frames, label, idx):
    zoom_in = idx % 2 == 0
    z = f"1+{ZOOM}*on/{frames}" if zoom_in else f"{1+ZOOM}-{ZOOM}*on/{frames}"
    vf = (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase:flags=lanczos,"
          f"crop={W*2}:{H*2},"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}")
    if label:
        lf = d / "tmp" / f"label{idx:02d}.txt"
        lf.write_text(label, encoding="utf-8")
        vf += (f",drawtext=fontfile={FONTS/'Anton-Regular.ttf'}:textfile={lf}:fontsize=96"
               f":fontcolor={NAVY}:box=1:boxcolor={MUSTARD}:boxborderw=30"
               f":x=(w-text_w)/2:y=h*0.10:enable='gte(t,0.2)'")
    out = d / "tmp" / f"clip{idx:02d}.mp4"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", d / img, "-vf", vf,
        "-frames:v", frames, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p", out])
    return out


def ass_t(t):
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"


def write_captions(path, chunks):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
            "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, "
            "MarginV, Encoding\n"
            "Style: Cap,Montserrat ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H004A2A1B,&H00000000,"
            "0,0,0,0,100,100,0,0,1,8,0,2,90,90,300,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
            "Effect, Text\n")
    lines = [f"Dialogue: 0,{ass_t(s)},{ass_t(e)},Cap,,0,0,0,,{{\\fad(60,0)}}{t}"
             for s, e, t in chunks]
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    d = Path(sys.argv[1]).resolve()
    (d / "tmp").mkdir(exist_ok=True)
    cfg = json.loads((d / "script.json").read_text(encoding="utf-8"))
    sentences, scenes = cfg["sentences"], cfg["scenes"]
    asr = json.loads((d / "words.json").read_text(encoding="utf-8"))
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", d / "raw.wav"], capture_output=True,
                                 text=True).stdout)

    # words with sentence index
    sw = [(w, si) for si, s in enumerate(sentences) for w in s.split()]
    times, matched = align([w for w, _ in sw], asr)
    print(f"Aligned {matched}/{len(sw)} script words to the recording")

    regions = speech_regions(d / "raw.wav", total)
    tmap, pieces, new_total = make_timemap(regions)
    print(f"Voice: {total:.1f}s -> {new_total:.1f}s after trimming pauses")

    # trimmed + cleaned audio
    parts = "".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[p{i}];"
                    for i, (s, e, _) in enumerate(pieces))
    gaps, chain = [], ""
    for i, (s, e, ns) in enumerate(pieces):
        if i:
            g = ns - (pieces[i-1][2] + pieces[i-1][1] - pieces[i-1][0])
            if g > 0.001:
                gaps.append(f"anullsrc=r=48000:cl=mono,atrim=0:{g:.3f}[g{i}];")
                chain += f"[g{i}]"
        chain += f"[p{i}]"
    n_in = chain.count("[")
    fc = parts + "".join(gaps) + chain + f"concat=n={n_in}:v=0:a=1,highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[a]"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", d / "raw.wav", "-filter_complex", fc,
        "-map", "[a]", "-ar", "48000", d / "tmp" / "voice_clean.wav"])

    # new word times
    nt = [(tmap(s), tmap(e)) for s, e in times]
    sent_start = {}
    for (w, si), (s, e) in zip(sw, nt):
        sent_start.setdefault(si, s)

    # scene boundaries: just before the first word of the scene's first sentence
    bounds = [0.0] + [max(0.0, sent_start[sc[0]] - 0.08) for sc in scenes[1:]] + [new_total]
    clips = []
    for i, sc in enumerate(scenes):
        frames = max(1, round(bounds[i+1] * FPS) - round(bounds[i] * FPS))
        print(f"  scene {i+1:2d} {bounds[i]:6.2f}s  {frames/FPS:4.1f}s  {sc[1]}  {sc[2]}")
        clips.append(render_scene(d, sc[1], frames, sc[2], i))
    (d / "tmp" / "list.txt").write_text("".join(f"file '{c.name}'\n" for c in clips))

    # captions: chunks of up to 3 words, never crossing a sentence
    chunks, cur = [], []
    for k, ((w, si), (s, e)) in enumerate(zip(sw, nt)):
        cur.append((w, s, e))
        last_in_sent = k == len(sw) - 1 or sw[k+1][1] != si
        if len(cur) == 3 or last_in_sent or w.endswith((",", ":")):
            chunks.append([cur[0][1], cur[-1][2], " ".join(x[0] for x in cur).upper()])
            cur = []
    for i in range(len(chunks) - 1):   # hold each caption until the next one
        chunks[i][1] = min(max(chunks[i][1], chunks[i][0] + 0.35), chunks[i+1][0])
    chunks[-1][1] = new_total
    write_captions(d / "tmp" / "captions.ass", chunks)

    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", d / "tmp" / "list.txt",
        "-i", d / "tmp" / "voice_clean.wav",
        "-vf", f"subtitles={d/'tmp'/'captions.ass'}:fontsdir={FONTS}",
        "-map", "0:v", "-map", "1:a", "-t", f"{new_total:.2f}", "-c:v", "libx264", "-preset", "medium",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-r", FPS,
        "-movflags", "+faststart", d / "final.mp4"])
    print("Done:", d / "final.mp4")


if __name__ == "__main__":
    main()
