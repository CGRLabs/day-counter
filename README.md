# Day Counter

The day of the world, on the action bar, where you can see it without opening
anything.

> **DAY 12**

On the first day it reads `DAY 0`, the day after that `DAY 1` — the same number
`/time query day` gives. It is the world's clock divided by the length of a day,
so it counts the days the world has been through, and it moves when you sleep.

## What it does

- Puts the day of the world above your hotbar.
- Nothing else. It adds no items, no blocks, no screens and no settings.
- It is **data only** — two functions and two tag files, no code, nothing to
  compile, nothing that can break. It runs wherever your world is simulated.

## Install

1. Install the mod and enable it in Options → Mods, then restart the game.
2. Play. The day is on the action bar.

It works in single player, on a LAN host and on a server that has the mod — the
functions run where the world is simulated.

## Build from source

```sh
cargo install --git https://github.com/horizon-rust/horizon cargo-horizon-mod
cargo horizon-mod build
cargo horizon-mod check target/horizon-mod/day_counter.hmod
```

The build is deterministic: the same sources produce the same file bytes.

## What's inside

```
data/day_counter/function/load.mcfunction   the scoreboard the counter keeps
data/day_counter/function/tick.mcfunction   the count, and the action bar
data/minecraft/tags/function/load.json      runs load once, when the world loads
data/minecraft/tags/function/tick.json      runs tick, every tick
```

The day is read with `/time query time` and divided by the length of a day, so it
is the world's own day and not a number this mod keeps to itself.

## Credits

Inspired by the [Day Counter](https://modrinth.com/datapack/daycounter) data pack
by justwilly, which is released under CC0-1.0. This is a Horizon version of the
same idea, written for Horizon's function and scoreboard support.

## License

[MIT](LICENSE) — Copyright (c) 2026 CGRLabs.

Not an official Minecraft product. Not approved by or associated with Mojang or
Microsoft.
