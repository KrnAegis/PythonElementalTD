# Fidelity to Element TD Survivor 4.3b

This is a playable, data-driven single-player recreation. It is **not an exact or fully verified Warcraft III engine port**. The extracted map is the source of the database; the browser simulation is a new implementation.

## Data and rules matched from the map

- All 134 named defense records, including all 15 dual recipes, all 20 triple recipes, upgraded families, pure towers, elemental Arrow/Cannon variants, mobile defenses, and Periodic.
- Actual upgrade graph, elemental research tier requirements, build/upgrade gold costs, attack ranges/intervals, displayed base damage, and native splash radii/factors.
- All 60 initialized enemy waves and their names, elements, classifications, health scaling, movement speeds, and difficulty armor bonus.
- 30 normal creeps per wave, a 0.45-second spawn interval, the 30/45/60-second normal/short/extra-short preparation timers, and the difficulty/wave-band clear-to-next-wave delays.
- Elemental matrix: 2× vulnerable, 0.5× resistant, 0.8× Composite, 1× otherwise. Armor coefficient 0.06.
- Initial normal/short/extra-short resources (normal begins with zero lumber; first pick after wave 5); 15-second interest starting at 2%, three +1% interest upgrades; difficulty-specific scripted bounty growth and Arbitrage rewards.
- Actual sell-ability classification: `A00T` towers refund fully; `A001` towers refund 75% in Pick/Draft and fully in Random. Clones do not refund. Investment accumulates across upgrades.
- Elemental guardians at three tiers, their HP tables, research-on-defeat, preparation shortcuts in Short/Extra Short, Pure Essence, and free late-game essence slots.
- Remaining health on leaks, normal one-life loss, guardian/Ancient three-life loss, and undead revival/removal behavior.
- Afterlife shares a player-level token pool. Below 50 lives outside Extreme, tiers add 6/9/18 tokens per kill; otherwise they add 2/3/6. Every 18 tokens adds a life.
- Ronald HP/speed arrays, replacement-on-kill behavior, stage thresholds, and trait changes.
- Original first player's static lane grid, spawn/exit coordinates, and terrain-region boundaries. Other original grids are retained in the data but there are no other playable seats.
- All Pick, All Random, Same Random, solo Draft, Short, Extra Short, Chaos, and Extreme. Chaos preserves the first five and final wave and uses the original swap range. Solo Draft lets the player eliminate five dual and seven triple families, with seeded initial choices.

## Implemented tower families

Every defense is reachable through its graph/requirements and has a working attack handler. This table describes the implementation, not a claim of byte-for-byte spell parity.

| Family | Browser behavior |
|---|---|
| Basic / Arrow / Cannon / single / pure / Periodic | Elemental attacks and splash, upgraded stats and requirements |
| Trickery / Mirage / Eidolon | Real temporary clones, tier lifetimes, eligibility restrictions, transferred support buffs, cleanup on sale/upgrade |
| Ice / Freezing / Sub-Zero | Line/helix damage with double damage near the center and endpoint explosion |
| Electricity / Lightning / Energy | Five possible hits, source-derived bounce damage index, closest-target bounce search and target revisits |
| Quark / Electron / Atom | Per-target accumulating additional damage; resets on target switch |
| Life / Eternal / Soul Catcher | Shared Afterlife token pool and reduced gain above the normal-life threshold |
| Magic / Sorcery / Wizardry | Activated three-second damage boost |
| Gunpowder / Mortar / Vulcan | Primary explosion plus two secondary area explosions |
| Blacksmith / Forge / Foundry | Nearby attack-damage support, tier strength and strongest-aura precedence |
| Poison / Pollution / Pestilence | Growing same-target splash, with damage tier scaling |
| Vapor / Mist / Steam | Radius-700 attack plus overlapping per-victim aftershocks |
| Hydro / Spout / Geyser | Chance-based area damage and temporary stun |
| Disease / Decay / Death | Max-HP/current-HP damage formula and support scaling |
| Flame / Solar / Sun | Stacking timed area burns |
| Mushroom / Toadstool / Fungus | Out-and-back line damage approximation |
| Well / Spring / Waterfall | Nearby attack-speed support |
| Zealot / Fanatic | Growing attack-speed stack, removed after four seconds without attacking |
| Quaker / Earthshaker | Chance-based area burst |
| Laser / Phasor | Inverse-distance damage |
| Oblivion / Necromancy | Seven-shot magazine, automatic reload, faster manual reload |
| Polar / Ice Age | Temporary HP removal/restoration and damage amplification |
| Drowning / Kraken | Health-dependent instant-kill probability |
| Radius / Orbit | Paired-orb area attack approximation |
| Flamethrower / Flamespewer | Stackable napalm explosions on target death |
| Voodoo / Witchcraft | Area damage amplification |
| Muck / Mire | Area slow |
| Corrosion / Hydrochloric | Area armor reduction and timed damage |
| Roots / Thorns | Area slow plus timed damage |
| Nova / Supernova | Area burst and slow |
| Gold / Wealth | Increased kill bounty |
| Windstorm / Monsoon | Target-centered recurring storm damage and slow |
| Hail / Comet | Up to three simultaneous targets |
| Tidal / Tsunami | Attack charges and activated Douse damage |
| Enchantment / Incantation | Armor reduction |
| Impulse / Velocity | Distance-proportional damage |
| Flesh Golem / Patchwork Abomination | Mobile defense using a walkable-grid route |

## Known differences

- **No Warcraft engine comparison was performed.** Exact native spell behavior, damage-event order, movement/collision, armor edge cases, buff stacking, autocast decisions, targeting ties, and timer rounding are not certified.
- Enemy routing uses a clearance-aware grid route calculated from the original pathing grid. Construction keeps that road clear. It does not reproduce dynamic Warcraft pathfinding, terrain height, destructible collisions, or the moving builder unit.
- Shots and many ability effects apply damage immediately. Their drawn projectiles animate independently. The original spell travel, helix/boomerang/orbit geometry, secondary bomb scatter, lightning callback timing, and precise impact collision are approximated.
- Poison uses a capped per-target radius progression instead of a complete translation of the original dynamic spreading/list implementation.
- Burn/corrosion/roots ticks, native stun duration, some debuff durations, tornado placement, reload durations, and native spell activation cooldowns are modeled rather than fully validated.
- The storm does not create and control a native tornado unit. Orbit and boomerang do not use the original motion/dummy systems. Oblivion ammo and Magic are simplified state machines.
- Enemy Mechanical shield, Healing, Fast, Undead, and Image behavior is implemented, but native mana regeneration, native illusion damage ratios, special spell immunity, and damage-trigger details can differ. Illusions expire after five seconds and do not consume lives or award normal bounty.
- Draft voting is replaced with solo elimination selection. Multiplayer, race scoring, opponent weapons, host voting, team mechanics, and Warcraft chat commands are omitted intentionally.
- Same Random and All Random have little meaningful difference with one player. Both are deterministic for a given seed, with their respective selection paths retained.
- Native RNG is replaced with a deterministic JavaScript PRNG. Seeded outcomes will not match Warcraft's original generator.
- Artwork, sound, music, UI, sprite silhouettes, and animations are original. The 48 atlas cells are reused across tower tiers/fusions and enemy classes; they do not recreate every original model as a unique sprite.
- Convenience features—pause, 1×/2×/4× speed, local autosave/resume, numbered building sites, tower database, manual shortening of a completed wave's countdown—are new.
- Coding combat runs at 250ms intervals and can alter targeting cadence. Built-in targeting is the closer mode for playing the original rules.
- Exact full balance and original-engine corner cases still need playtesting. Browser tests establish that the implementation runs, not that every original ability is numerically identical in all situations.

## Verification performed

- Simulation regression tests cover source values, requirements, upgrades/refunds, damage/armor, spawn counts, leaks/revival, Chaos/Draft, all 134 defense attack handlers, Afterlife, and Ronald progression.
- A stress defense completed all 60 waves with 1,800 credited normal kills and transitioned into the Ronald finale. That checks scheduling and state integrity, not normal-game balance or solvability.
- Chromium desktop/mobile checks cover startup, original data loading, grid-first building, confirmation, cancellation, and setup Library, wave spawning, responsive overflow, and uncaught runtime exceptions.

For stricter parity, the next engineering work is translating and testing the remaining native/dynamic spell behavior against the original 4.3b map in the matching Warcraft III runtime.

Placement uses a browser-friendly 96-unit grid with an 80-unit footprint and one tower per cell. This deliberately allows adjacent towers and differs from the original Warcraft placement spacing. Existing saved towers retain their positions.

Visual effects use original tower-family and element data to select distinct projectiles and fusion palettes. Terrain details, model ornaments, and emissive effects are new cosmetic rendering, with no changes to combat values or buildable ground. Source sprite atlases are retained.

Buff/debuff indicators are rendered from live status state, with source identity saved at application time. They are new browser visuals, not extracted Warcraft buff artwork. Expiring effects, damage-over-time, clones, native shields, speed bursts, healing, and revival are represented without changing their gameplay strength.

Monster walking artwork is new procedural pixel art with creature-category gaits and directional frames. It replaces the previous static enemy rendering, rather than reproducing native Warcraft model animations. Movement, speed modifiers, collision/path data, and combat values are unchanged.
