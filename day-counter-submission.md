# Day Counter 1.0.0 — registry submission sheet

Submit at: https://playhorizon.dev/mods/submit (sign in with GitHub as CGRLabs), choose **new
project** — `day_counter` is not in the registry yet.

**Status: ready to submit.** Everything the form asks for now exists: the package is built,
checked and signed, the icon is drawn, the source is public, and the current bytes were proven
in-game on 2026-11-21.

## Form fields

| Field | Value |
| --- | --- |
| Kind | Content mod (.hmod) |
| File | `D:\CGRLabs\Horizon-Ecosystem\development\mods\day-counter\target\horizon-mod\day_counter.hmod` |
| Id | `day_counter` |
| Version | `1.0.0` |
| For Minecraft | `26.3` |
| Name | Day Counter |
| Licence | MIT |
| Authors | CGRLabs |
| Source code | `https://github.com/CGRLabs/day-counter` (public, commit `3ad17ec`) |
| Categories | utility, information |
| Tags | hud, day, counter, quality-of-life, action-bar |
| Icon | `D:\CGRLabs\Horizon-Ecosystem\development\mods\day-counter\icon.png` (256×256 PNG, 4 KiB) |
| Public key | `RWRiGjU5z15nz08GagVi7PEavoOfCGsZEqUL5NdQkkilVp7lkOdJtGmk` |
| Signature | `D:\CGRLabs\Horizon-Ecosystem\development\mods\day-counter\target\horizon-mod\day_counter.hmod.minisig` |

## Release facts

- File size: **1 532 bytes**
- SHA-256: `fd07ec5e5e316756e95600523f3ad5d664e5fabcf1c1b42c6fc3b3af3835f5f5`
- Content mod API `0.2`, side `both`, capabilities `["registries"]`
- `cargo horizon-mod check` → `day_counter 1.0.0 (mod, API 0.2, both)`, `signature verified`
- Signature: minisign, trusted comment `day_counter 1.0.0`
- The installed copy at `horizon-windows-x64\horizon-mods\day_counter.hmod` is byte-identical
  (same SHA-256), so the file proven below is the file being submitted.

The source published at `CGRLabs/day-counter` is at commit `3ad17ec`, which contains exactly the
`data/` tree this package was built from — the `source` link and the uploaded file agree.

## What it does

The day of the world, on the action bar.

Two functions and two tag files: the load function makes a scoreboard, the tick function reads
the world's clock, divides it by the length of a day, and writes the number above your hotbar.

It adds no items, no blocks, no screens and no settings, and it changes no gameplay. It is
**data only** — nothing to compile, nothing that can break.

It also knows when to keep quiet: if the Day Tally native mod is installed it already draws the
day in the corner and sets `#day_tally daycounter 1`, and this line then stands down so the day
is never shown twice. With Day Tally absent — the only case that ships today — the guard passes
and the counter draws, which is what the proof below exercises.

## In-game proof — VERIFIED 2026-11-21

`python tools/proof_day_counter.py` against the real client on a scratch world, with the mod
installed and enabled. The scratch home carried `day_counter.hmod`, `flesh_to_leather.hmod` and
`salvage.hmod`; `mod.day_tally` was enabled but its file is gone, so this is the no-Day-Tally
path.

| Check | Result |
| --- | --- |
| The action bar | reads **`DAY 0`** on a fresh world |
| The day moves | after `/time set 25000` it reads **`DAY 1`** |
| The counter's source | the world's own clock (`/time query time`), the same day `/time query day` gives |

Report: `target/proof/day-counter-v01-report.json` (`"passed": true`). The screenshot
`target/proof/day-counter-v01.png` shows `DAY 1` above the hotbar.

The earlier run recorded on 2026-11-12 proved a 1 422-byte build; the package grew to 1 532 bytes
when the stand-down line was added, so it was proven again rather than assumed.

## Description (paste into the Markdown box)

**How long have you been out here?** Day Counter puts the day of the world above your hotbar,
so you always know.

> **DAY 12**

On the first day it reads `DAY 0`; the day after that, `DAY 1`. It is the same number
`/time query day` gives — the world's own clock — and it moves when you sleep.

**Nothing else.** No items, no blocks, no screens, no settings, nothing to configure. It is data
only: two small functions and two tag files. It cannot break anything, because there is nothing
to break.

**It works everywhere your world does.** The counter runs where the world is simulated — single
player, a LAN host, or a server that has the mod installed.

## Still to do (needs the user)

- **Fill in the form** at https://playhorizon.dev/mods/submit with the table above and the
  description, uploading `day_counter.hmod`, `day_counter.hmod.minisig` and `icon.png`.
- **Wait for the review** — a project's first listing is always reviewed by a person.

## Credits

Inspired by the [Day Counter](https://modrinth.com/datapack/daycounter) data pack by
justwilly (CC0-1.0). This is a Horizon version of the same idea.
