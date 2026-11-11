"""In-game check for Day Counter: the action bar shows the day, and it moves."""

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = Path(r"D:\CGRLabs\Horizon-Ecosystem\horizon-windows-x64")
OUT = ROOT / "target" / "proof"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    env = dict(os.environ)
    home = Path(tempfile.mkdtemp(prefix="day-counter-home-"))
    env["HORIZON_HOME"] = str(home)
    env["HORIZON_CONTROL"] = str(home / "control.sock")
    for key in ("HORIZON_LAUNCHER_HOME", "XDG_DATA_HOME", "XDG_CONFIG_HOME"):
        env[key] = tempfile.mkdtemp(prefix="day-counter-")
    env["HORIZON_NO_AUDIO"] = "1"
    # The launch points --game-dir at HORIZON_HOME, so the mods must live there.
    shutil.copytree(INSTALL / "horizon-mods", home / "horizon-mods")
    shutil.copy2(INSTALL / "horizon-mods.txt", home / "horizon-mods.txt")
    log = (OUT / "day-counter-v01.log").open("w", encoding="utf-8")
    report = {"scratch_home": str(home),
              "mods": [p.name for p in (home / "horizon-mods").glob("*.hmod")],
              "enabled": (home / "horizon-mods.txt").read_text(encoding="utf-8").split()}

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    def ctl(*a, timeout=90):
        o, e = OUT / "ctl.out", OUT / "ctl.err"
        with o.open("wb") as fo, e.open("wb") as fe:
            done = subprocess.run([str(INSTALL / "horizon-ctl.exe"), *a], stdout=fo, stderr=fe,
                                  env=env, timeout=timeout, cwd=str(home))
        text = o.read_text(encoding="utf-8", errors="replace").strip()
        if done.returncode != 0:
            raise RuntimeError(f"ctl {' '.join(a)} -> {done.returncode}: {text}")
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            value = {"_raw": text}
        if isinstance(value, dict) and "error" in value:
            raise RuntimeError(f"ctl {' '.join(a)} -> {value['error']}")
        return value

    def command(text):
        value = ctl("command", text)
        say(f"command {text}: {json.dumps(value)}")
        return value

    def actionbar():
        # The action bar is reported by the messages command, not by state.
        return (ctl("messages", "3").get("actionbar") or "").strip()

    try:
        say(f"scratch home: {home}")
        say("launching VISIBLE window...")
        ctl("launch", "--game", str(INSTALL / "horizon-client.exe"), "--world", "DayCounterV01",
            "--creative", "--wait", "--render-distance", "6",
            "--resources", str(INSTALL / ".local" / "horizon-client" / "26.3"),
            "--test-terrain", timeout=420)
        ctl("wait-ready", "120", timeout=150)
        for _ in range(6):
            if ctl("state").get("screen") == "playing":
                break
            ctl("close")
            ctl("resume")
            time.sleep(2)
        assert ctl("state").get("screen") == "playing", "the game did not start"

        # Let the load function run and the tick function tick.
        deadline = time.monotonic() + 30
        shown = ""
        while time.monotonic() < deadline:
            time.sleep(1)
            shown = actionbar()
            if shown:
                break
        say(f"action bar: {shown!r}")
        report["actionbar_first"] = shown
        assert shown, "the action bar shows nothing: the mod is not running"
        assert shown.upper().startswith("DAY"), f"the action bar reads {shown!r}"

        # The day moves when the world's clock moves.
        command("time set 25000")
        deadline = time.monotonic() + 30
        after = ""
        while time.monotonic() < deadline:
            time.sleep(1)
            after = actionbar()
            if "1" in after:
                break
        say(f"action bar after the clock moved: {after!r}")
        report["actionbar_second"] = after
        assert after.strip() != shown, f"the day did not move: {after!r}"
        assert "1" in after, f"the day did not become 1: {after!r}"

        ctl("screenshot", str(OUT / "day-counter-v01.png"))
        report["passed"] = True
        say(f"the action bar reads {shown!r} and then {after!r}")
    except Exception as exc:
        report["error"] = str(exc)
        say(f"FAILED: {exc}")
        raise
    finally:
        (OUT / "day-counter-v01-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        try:
            ctl("quit", timeout=90)
        except Exception as exc:
            say(f"quit: {exc}")
        log.close()


if __name__ == "__main__":
    main()
