"""Probe: which stage of the Day Counter datapack is failing in Horizon?"""

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

INSTALL = Path(r"D:\CGRLabs\Horizon-Ecosystem\horizon-windows-x64")
OUT = Path(r"C:\Users\SKULL\AppData\Local\Temp\opencode")

env = dict(os.environ)
home = Path(tempfile.mkdtemp(prefix="dc-probe-home-"))
env["HORIZON_HOME"] = str(home)
env["HORIZON_CONTROL"] = str(home / "control.sock")
for key in ("HORIZON_LAUNCHER_HOME", "XDG_DATA_HOME", "XDG_CONFIG_HOME"):
    env[key] = tempfile.mkdtemp(prefix="dc-probe-")
env["HORIZON_NO_AUDIO"] = "1"
shutil.copytree(INSTALL / "horizon-mods", home / "horizon-mods")
shutil.copy2(INSTALL / "horizon-mods.txt", home / "horizon-mods.txt")


def ctl(*a, timeout=90):
    o, e = OUT / "dc.out", OUT / "dc.err"
    with o.open("wb") as fo, e.open("wb") as fe:
        done = subprocess.run([str(INSTALL / "horizon-ctl.exe"), *a], stdout=fo, stderr=fe,
                              env=env, timeout=timeout, cwd=str(home))
    text = o.read_text(encoding="utf-8", errors="replace").strip()
    if done.returncode != 0:
        return {"_error": text or e.read_text(encoding="utf-8", errors="replace").strip()}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"_raw": text}


def cmd(text):
    value = ctl("command", text)
    print(f"--- {text}\n    {json.dumps(value)[:300]}")
    return value


ctl("launch", "--game", str(INSTALL / "horizon-client.exe"), "--world", "DCProbe",
    "--creative", "--wait", "--render-distance", "4",
    "--resources", str(INSTALL / ".local" / "horizon-client" / "26.3"), "--test-terrain", timeout=420)
ctl("wait-ready", "120", timeout=150)
for _ in range(6):
    if ctl("state").get("screen") == "playing":
        break
    ctl("close")
    ctl("resume")
    ctl("wait", "5")

time.sleep(3)
print("=== is the load function's objective there? ===")
cmd("scoreboard objectives list")
print("=== is the tick function running? ===")
cmd("scoreboard players get $day daycounter")
cmd("scoreboard players get #ticks_per_day daycounter")
print("=== the action bar ===")
state = ctl("state")
print("actionbar:", json.dumps(state.get("actionbar")))
print("=== run the tick function by hand ===")
cmd("function day_counter:tick")
time.sleep(1)
print("actionbar after:", json.dumps(ctl("state").get("actionbar")))
print("=== the function tags the game knows ===")
cmd("scoreboard objectives list")
print("=== the world's functions ===")
cmd("function day_counter:load")

try:
    ctl("quit", timeout=90)
except Exception as exc:
    print(f"quit: {exc}")
