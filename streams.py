import subprocess




def CheckStreamRunning(address:str):
    res = subprocess.run(["timeout", "10s", "ffprobe", "-v", "quiet", "rtmp://192.168.1.3/live/obs_stream"])
    if res.returncode == 0:
        return True
    return False

print(CheckStreamRunning("meme"))