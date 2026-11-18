import numpy as np, subprocess, wave, sys
SR=48000
def load(p):
    b=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True,check=True).stdout
    return np.frombuffer(b,np.float32).copy()
def trim(x,th=0.01):
    a=np.abs(x); w=int(.01*SR)
    env=np.convolve(a,np.ones(w)/w,'same'); idx=np.where(env>th)[0]
    return x[max(idx[0]-int(.03*SR),0):idx[-1]+int(.05*SR)]
raw=load("raw_orig.wav")
fixes=[("final/s68.mp3",433.03,444.93),("final/s65.mp3",416.53,422.26),("final/s26.mp3",151.68,161.66)]
for f,a,b in fixes:  # reverse order already
    i,j=int(a*SR),int(b*SR); orig=raw[i:j]
    new=trim(load(f))
    rms=lambda v: np.sqrt(np.mean(v[np.abs(v)>0.01]**2))
    new*=rms(orig)/rms(new)
    print(f, "orig %.2fs new %.2fs"%((j-i)/SR,len(new)/SR))
    raw=np.concatenate([raw[:i],new,raw[j:]])
pcm=(np.clip(raw,-1,1)*32767).astype(np.int16)
with wave.open("raw_fixed.wav","wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("total %.2f s"%(len(raw)/SR))
