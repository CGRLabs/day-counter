# Day Counter 1.0.0 — registry submission sheet

Submit at: https://playhorizon.dev/mods/submit (sign in with GitHub as CGRLabs), choose **new
project** — `day_counter` is not in the registry yet.
**Verified in-game 2026-11-12**: the action bar reads `DAY 0`, and `DAY 1` once the world's
clock moves.

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
| Source code | *(not published yet — see "Still to do")* |
| Categories | utility, information |
| Tags | hud, day, counter, quality-of-life, action-bar |
| Icon | *(to be supplied — a PNG of at most 256 KiB)* |
| Public key | `RWRiGjU5z15nz08GagVi7PEavoOfCGsZEqUL5NdQkkilVp7lkOdJtGmk` |
| Signature | `D:\CGRLabs\Horizon-Ecosystem\development\mods\day-counter\target\horizon-mod\day_counter.hmod.minisig` |

## Release facts

- File size: **1 422 bytes**
- SHA-256: `3b70daaa451462d48065b4abf9782ac42fbad61cad0e2e92286bce879688f30b`
- Content mod API `0.2`, side `both`, capabilities `["registries"]`
- `cargo horizon-mod check` → `{"ok":true, …, "kind":"mod", "id":"day_counter", "size":1422, "version":"1.0.0"}`
- Signature: minisign, verified — *"Signature and comment signature verified"*, trusted comment
  `day_counter 1.0.0`
- The build is deterministic: the same sources give the same bytes.

## What it does

The day of the world, on the action bar.

That is all. Two functions and two tag files: the load function makes a scoreboard, the tick
function reads the world's clock, divides it by the length of a day, and writes the number above
your hotbar.

It adds no items, no blocks, no screens and no settings, and it changes no gameplay. It is
**data only** — nothing to compile, nothing that can break.

## In-game proof — VERIFIED 2026-11-12

`python tools/proof_day_counter.py` against the real client on a scratch world, with the mod
installed and enabled.

| Check | Result |
| --- | --- |
| The action bar | reads **`DAY 0`** on a fresh world |
| The day moves | after `/time set 25000` it reads **`DAY 1`** |
| The counter's source | the world's own clock (`/time query time`), the same day `/time query day` gives |

Report: `target/proof/day-counter-v01-report.json`. The proof's own picture shows `DAY 1` above
the hotbar.

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

- **The icon** — a PNG of at most 256 KiB, square is best. A picture of the action bar reading
  `DAY 12` would say what the mod is at a glance.
- **Publish the source** — the registry's pull-request template asks that the `source` link has
  the code the file was built from. The source should go to
  `https://github.com/CGRLabs/day-counter` (a public repo), like Flesh to Leather and Salvage.
- **Fill in the form** at https://playhorizon.dev/mods/submit with the table above and the
  description.
- **Wait for the review** — a project's first listing is always reviewed by a person.

## Credits

Inspired by the [Day Counter](https://modrinth.com/datapack/daycounter) data pack by
justwilly (CC0-1.0). This is a Horizon version of the same idea.
