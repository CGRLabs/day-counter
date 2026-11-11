import json, os, shutil, subprocess, tempfile, time
from pathlib import Path
INSTALL = Path(r"D:\CGRLabs\Horizon-Ecosystem\horizon-windows-x64")
OUT = Path(r"C:\Users\SKULL\AppData\Local\Temp\opencode")
env = dict(os.environ)
home = Path(tempfile.mkdtemp(prefix="dc-st2-home-"))
env["HORIZON_HOME"] = str(home); env["HORIZON_CONTROL"] = str(home / "control.sock")
for k in ("HORIZON_LAUNCHER_HOME", "XDG_DATA_HOME", "XDG_CONFIG_HOME"):
    env[k] = tempfile.mkdtemp(prefix="dc-st2-")
env["HORIZON_NO_AUDIO"] = "1"
shutil.copytree(INSTALL / "horizon-mods", home / "horizon-mods")
shutil.copy2(INSTALL / "horizon-mods.txt", home / "horizon-mods.txt")
def ctl(*a, timeout=90):
    o, e = OUT / "ds2.out", OUT / "ds2.err"
    with o.open("wb") as fo, e.open("wb") as fe:
        d = subprocess.run([str(INSTALL / "horizon-ctl.exe"), *a], stdout=fo, stderr=fe, env=env, timeout=timeout, cwd=str(home))
    t = o.read_text(encoding="utf-8", errors="replace").strip()
    if d.returncode != 0: return {"_error": t}
    try: return json.loads(t)
    except Exception: return {"_raw": t}
ctl("launch", "--game", str(INSTALL / "horizon-client.exe"), "--world", "DCState2", "--creative", "--wait",
    "--render-distance", "4", "--resources", str(INSTALL / ".local" / "horizon-client" / "26.3"), "--test-terrain", timeout=420)
ctl("wait-ready", "120", timeout=150)
for _ in range(6):
    if ctl("state").get("screen") == "playing": break
    ctl("close"); ctl("resume"); ctl("wait", "5")
ctl("command", 'title @a actionbar [{"text":"READ ME"}]')
time.sleep(0.2)
s = ctl("state")
print("TOP KEYS:", sorted(s.keys()))
for k, v in s.items():
    if isinstance(v, dict) and any(x in v for x in ("actionbar", "title", "chat")):
        print(f"  {k} -> actionbar={json.dumps(v.get('actionbar'))} title={json.dumps(v.get('title'))}")
try: ctl("quit", timeout=90)
except Exception as e: print("quit:", e)
