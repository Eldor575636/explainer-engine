import json, subprocess, sys
P = list(json.load(open('../picture_prompts.json')))
B = "https://d8j0ntlcm91z4.cloudfront.net/user_3FbvzPQ97OscGh7itaIMGXFRzbY/"
for a in sys.argv[1:]:
    i, u = a.split("=", 1)
    r = subprocess.run(["curl", "-sSf", "-o", P[int(i)] + ".png", B + u + ".png"], capture_output=True, text=True)
    print(i, P[int(i)], "ok" if r.returncode == 0 else r.stderr[:80])
