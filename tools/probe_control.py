"""Control: does the action bar reach the player from a command, and from a function?"""

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
home = Path(tempfile.mkdtemp(prefix="dc-ctl-home-"))
env["HORIZON_HOME"] = str(home)
env["HORIZON_CONTROL"] = str(home / "control.sock")
for key in ("HORIZON_LAUNCHER_HOME", "XDG_DATA_HOME", "XDG_CONFIG_HOME"):
    env[key] = tempfile.mkdtemp(prefix="dc-ctl-")
env["HORIZON_NO_AUDIO"] = "1"
shutil.copytree(INSTALL / "horizon-mods", home / "horizon-mods")
shutil.copy2(INSTALL / "horizon-mods.txt", home / "horizon-mods.txt")


def ctl(*a, timeout=90):
    o, e = OUT / "dc2.out", OUT / "dc2.err"
    with o.open("wb") as fo, e.open("wb") as fe:
        done = subprocess.run([str(INSTALL / "horizon-ctl.exe"), *a], stdout=fo, stderr=fe,
                              env=env, timeout=timeout, cwd=str(home))
    text = o.read_text(encoding="utf-8", errors="replace").strip()
    if done.returncode != 0:
        return {"_error": text}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"_raw": text}


def cmd(text):
    value = ctl("command", text)
    print(f"--- {text}\n    {json.dumps(value)[:200]}")
    return value


def bar():
    return ctl("state").get("actionbar")


ctl("launch", "--game", str(INSTALL / "horizon-client.exe"), "--world", "DCControl",
    "--creative", "--wait", "--render-distance", "4",
    "--resources", str(INSTALL / ".local" / "horizon-client" / "26.3"), "--test-terrain", timeout=420)
ctl("wait-ready", "120", timeout=150)
for _ in range(6):
    if ctl("state").get("screen") == "playing":
        break
    ctl("close")
    ctl("resume")
    ctl("wait", "5")

print("\n### 1. a title from the PLAYER")
cmd('title @a actionbar [{"text":"FROM PLAYER"}]')
time.sleep(0.4)
print("   actionbar:", json.dumps(bar()))

print("\n### 2. a title from a FUNCTION (the console)")
cmd("function day_counter:tick")
time.sleep(0.4)
print("   actionbar:", json.dumps(bar()))

print("\n### 3. a title from the CONSOLE via a function with the score")
cmd('function day_counter:tick')
time.sleep(0.4)
print("   actionbar:", json.dumps(bar()))

print("\n### 4. a sidebar instead")
cmd("scoreboard objectives setdisplay sidebar daycounter")
time.sleep(0.4)
print("   state has sidebar:", "sidebar" in json.dumps(ctl("state")))

try:
    ctl("quit", timeout=90)
except Exception as exc:
    print(f"quit: {exc}")
