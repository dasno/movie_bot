import subprocess

async def CheckStreamRunning(address:str):
    res = subprocess.run(["timeout", "10s", "ffprobe", "-v", "quiet", address])
    if res.returncode == 0:
        return True
    return False