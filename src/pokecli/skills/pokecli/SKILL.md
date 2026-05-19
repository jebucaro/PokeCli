---
name: pokecli
description: Queries Pokémon, Berries, Items, Moves, Abilities, Types, Natures, evolution chains, species, egg groups, growth rates, machines (TM/HM), Pokemon forms, versions, version groups, regions, locations, location areas, generations, and pokedexes via the pokecli CLI. Use when the user needs to look up Pokémon stats, type matchups, abilities, natures, evolution chains, berries, items, moves, TMs, breeding compatibility, alternative forms, encounter locations, regional pokedexes, generation rosters, game versions, download sprites, or manage the local cache. Also use when the user mentions "pokecli", "pokedex", or "PokeAPI"
allowed-tools: Bash(pokecli:*)
---

# Pokémon Data Lookup with pokecli

## Quick start

```bash
pokecli pokemon get pikachu
pokecli type get fire
pokecli ability get intimidate
pokecli nature get modest
pokecli berry get oran
pokecli item get master-ball
pokecli move get thunderbolt
```

## Core workflow

1. Query: Use `pokecli <resource> get <name_or_id>` to fetch details
2. Browse: Use `pokecli <resource> list` to paginate through all entries
3. Evolve: Use `pokecli pokemon evolution <name>` to see the full evolution chain
4. Species: Use `pokecli pokemon species <name>` for Pokédex entries, capture rate, egg groups
5. Download: Use `pokecli image download pokemon <name> -o <path>` for sprites
6. Cache: Use `pokecli cache stats` and `pokecli cache clear` to manage local data

Responses are cached locally after the first request. Use `--no-cache` to force a fresh fetch.

**Uniform contract:** every resource supports `get <name_or_id>` and `list [--limit --offset]` with `--format table|json` and `--no-cache`. The Pokemon resource adds `moves`, `species`, and `evolution` sub-commands because each maps to a different API endpoint.

## Decision tree

Pick the right command for a given user intent. When in doubt, every resource supports `pokecli <resource> get <name_or_id>`.

| User intent                                          | Command                                              |
|------------------------------------------------------|------------------------------------------------------|
| Pokemon stats, types, abilities                      | `pokecli pokemon get <name>`                         |
| Moves a Pokemon can learn                            | `pokecli pokemon moves <name>`                       |
| Pokedex entry, egg groups, capture rate              | `pokecli pokemon species <name>`                     |
| Full evolution chain for a Pokemon                   | `pokecli pokemon evolution <name>`                   |
| Where can I catch this Pokemon?                      | `pokecli pokemon encounters <name>`                  |
| All varieties/forms (Mega, Alolan, Gmax)             | `pokecli pokemon forms <name>`                       |
| What does an ability do?                             | `pokecli ability get <name>`                         |
| What stats does a nature affect?                     | `pokecli nature get <name>`                          |
| Type matchups (weak/resists/immune)                  | `pokecli type get <name>`                            |
| Berry profile / item description / move details      | `pokecli {berry,item,move} get <name>`               |
| What does an egg group mean? (breeding)              | `pokecli egg-group get <name>`                       |
| What growth rate does X use?                         | `pokecli growth-rate get <name>`                     |
| What does damage class X mean?                       | `pokecli move-damage-class get <name>`               |
| What does learn method X mean?                       | `pokecli move-learn-method get <name>`               |
| What does evolution trigger X mean?                  | `pokecli evolution-trigger get <name>`               |
| What game is X (e.g. Pokemon Red)?                   | `pokecli version get <name>`                         |
| What versions belong to group X (e.g. red-blue)?     | `pokecli version-group get <name>`                   |
| What TM/HM is machine #N?                            | `pokecli machine get <id>`                           |
| Inspect a specific form/variety                      | `pokecli pokemon-form get <form-name>`               |
| All locations in a region                            | `pokecli region get <region>` (renders inline)       |
| What Pokemon live at this location?                  | `pokecli location-area get <area>` (renders inline)  |
| Sub-areas of a location                              | `pokecli location get <name>` (renders inline)       |
| Pokemon/moves introduced in Gen N                    | `pokecli generation get <gen>` (renders inline)      |
| Regional Pokedex listing (entry numbers + species)   | `pokecli pokedex get <name>` (renders inline)        |
| Evolution chain by chain ID (not by Pokemon name)    | `pokecli evolution-chain get <id>`                   |
| Download a Pokemon sprite                            | `pokecli image download pokemon <name> -o <path>`    |
| Any resource not listed above                        | `pokecli <resource> get <name>` — uniform contract   |

## Multi-step workflows

For multi-resource recipes (regional encounter lookup, TM tracing, full Pokemon
profile assembly, decoding cross-reference fields), see `references/workflows.md`.

## Commands

### Pokemon

```bash
pokecli pokemon get pikachu
pokecli pokemon get 25
pokecli pokemon get charizard --format json
pokecli pokemon get bulbasaur --no-cache
pokecli pokemon list
pokecli pokemon list --limit 50
pokecli pokemon list --limit 20 --offset 40
pokecli pokemon moves charmander
pokecli pokemon moves 4 --format json
pokecli pokemon moves pikachu --move thunderbolt
pokecli pokemon moves pikachu --move thunderbolt --format json
pokecli pokemon moves eevee --method egg
pokecli pokemon moves charizard --method level-up
pokecli pokemon species pikachu
pokecli pokemon species mewtwo --format json
pokecli pokemon evolution eevee
pokecli pokemon evolution bulbasaur --format json
pokecli pokemon encounters pikachu
pokecli pokemon encounters 25 --format json
pokecli pokemon forms charizard
pokecli pokemon forms vulpix --format json
```

### Ability

```bash
pokecli ability get intimidate
pokecli ability get 22
pokecli ability get levitate --format json
pokecli ability list
pokecli ability list --limit 20 --offset 40
```

### Nature

```bash
pokecli nature get modest
pokecli nature get 3
pokecli nature get jolly --format json
pokecli nature list
pokecli nature list --limit 25
```

### Type

```bash
pokecli type get fire
pokecli type get 10
pokecli type get dragon --format json
pokecli type get ghost --no-cache
pokecli type list
```

### Berry

```bash
pokecli berry get cheri
pokecli berry get 1
pokecli berry get oran --format json
pokecli berry list
pokecli berry list --limit 10
pokecli berry list --limit 10 --offset 20
```

### Item

```bash
pokecli item get potion
pokecli item get 1
pokecli item get master-ball --format json
pokecli item list
pokecli item list --limit 30
pokecli item list --limit 30 --offset 60
```

### Move

```bash
pokecli move get thunderbolt
pokecli move get 24
pokecli move get surf --format json
pokecli move get flamethrower --no-cache
pokecli move list
pokecli move list --limit 40
pokecli move list --limit 20 --offset 100
```

### Egg Group

```bash
pokecli egg-group get monster
pokecli egg-group get human-like
pokecli egg-group get 1 --format json
pokecli egg-group list
```

### Growth Rate

```bash
pokecli growth-rate get medium-slow
pokecli growth-rate get slow
pokecli growth-rate get 1 --format json
pokecli growth-rate list
```

### Evolution Trigger

```bash
pokecli evolution-trigger get level-up
pokecli evolution-trigger get use-item
pokecli evolution-trigger get 1 --format json
pokecli evolution-trigger list
```

### Move Damage Class

```bash
pokecli move-damage-class get physical
pokecli move-damage-class get special
pokecli move-damage-class get status --format json
pokecli move-damage-class list
```

### Move Learn Method

```bash
pokecli move-learn-method get level-up
pokecli move-learn-method get machine
pokecli move-learn-method get egg --format json
pokecli move-learn-method list
```

### Version

```bash
pokecli version get red
pokecli version get sword
pokecli version get 1 --format json
pokecli version list
```

### Version Group

```bash
pokecli version-group get red-blue
pokecli version-group get sword-shield
pokecli version-group get 1 --format json
pokecli version-group list
```

### Machine (TM/HM)

```bash
pokecli machine get 1
pokecli machine get 100 --format json
pokecli machine list --limit 50
```

### Pokemon Form

```bash
pokecli pokemon-form get charizard-mega-x
pokecli pokemon-form get vulpix-alola
pokecli pokemon-form get pikachu-gmax --format json
pokecli pokemon-form list --limit 50
```

### Region

```bash
pokecli region get kanto
pokecli region get hoenn --format json
pokecli region list
```

The `get` output includes the region's full list of child locations inline.

### Location

```bash
pokecli location get pallet-town
pokecli location get kanto-route-1
pokecli location get celadon-city --format json
pokecli location list --limit 50
```

The `get` output includes the location's sub-areas inline.

### Location Area

```bash
pokecli location-area get kanto-route-1-area
pokecli location-area get trophy-garden-area --format json
pokecli location-area list --limit 50
```

The `get` output includes the full Pokemon encounter table for the area
(pokemon × version × method × chance × levels).

### Generation

```bash
pokecli generation get generation-i
pokecli generation get generation-iii --format json
pokecli generation list
```

The `get` output includes counts and full lists of Pokemon species and moves
introduced in that generation.

### Pokedex

```bash
pokecli pokedex get kanto
pokecli pokedex get national --format json
pokecli pokedex list
```

The `get` output includes the full numbered entries list for the pokedex.

### Evolution Chain

```bash
pokecli evolution-chain get 67
pokecli evolution-chain get 1 --format json
pokecli evolution-chain list --limit 50
```

Reuses the same tree rendering as `pokecli pokemon evolution`, but accepts a
chain ID directly (useful when you already have one from another response).

### Image Download

```bash
pokecli image download pokemon pikachu -o pikachu.png
pokecli image download pokemon pikachu -o pikachu_shiny.png --variant front_shiny
pokecli image download pokemon 6 -o charizard_back.png --variant back_default
pokecli image download pokemon 133 -o /tmp/eevee.png
```

Sprite variants: `front_default`, `front_shiny`, `back_default`, `back_shiny`, `front_female`, `front_shiny_female`

### Cache Management

```bash
pokecli cache stats
pokecli cache clear
pokecli cache clear --resource pokemon
pokecli cache clear --resource ability
pokecli cache clear --resource nature
pokecli cache clear --resource type
pokecli cache clear --resource pokemon-species
pokecli cache clear --resource evolution-chain
pokecli cache clear --resource item
pokecli cache clear --resource machine
pokecli cache clear --resource egg-group
pokecli cache clear --resource version-group
```

Other cacheable resources: `move-damage-class`, `move-learn-method`, `growth-rate`, `evolution-trigger`, `version`, `pokemon-form`, `location`, `location-area`, `region`, `generation`, `pokedex`. Run `pokecli cache stats` for the full list.

## Global options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass local cache, fetch fresh from PokeAPI |
| `--format table` | Rich formatted table output (default) |
| `--format json` | Raw JSON with syntax highlighting |

> **For AI agents:** Prefer the default table output — it is plain text you can
> read directly. Use `--format json` only when you need to pipe the output to
> `jq` or a shell script. Raw JSON is not easier to process; it requires extra
> parsing steps that table output avoids entirely.

## `pokemon moves` options

| Option | Description |
|--------|-------------|
| `--move <name>` | Filter to a specific move; exits 1 if the Pokémon cannot learn it |
| `--method <method>` | Filter by learn method: `level-up`, `machine`, `tutor`, `egg` |

## Example: Compare two Pokémon

```bash
pokecli pokemon get charizard
pokecli pokemon get blastoise
```

## Example: Browse and then inspect

```bash
pokecli move list --limit 10
pokecli move get pound
```

## Example: Download all starters

```bash
pokecli image download pokemon bulbasaur -o bulbasaur.png
pokecli image download pokemon charmander -o charmander.png
pokecli image download pokemon squirtle -o squirtle.png
```

## Example: Look up moves a Pokémon can learn

```bash
# All moves with summary footer
pokecli pokemon moves pikachu

# Check if a Pokémon can learn a specific move (table)
pokecli pokemon moves pikachu --move thunderbolt

# Returns {"can_learn": true/false, "method": "...", "level": N} — useful for scripting
pokecli pokemon moves pikachu --move thunderbolt --format json

# Filter by learn method: level-up, machine, tutor, egg
pokecli pokemon moves eevee --method egg
pokecli pokemon moves charizard --method level-up --format json
```

**`--move` exit codes:** `0` if the Pokémon can learn the move, `1` if it cannot.

## Example: Look up type matchups

```bash
# What is fire weak to? What does it hit super effectively?
pokecli type get fire

# Full type chart as JSON
pokecli type get water --format json
```

## Example: Check a Pokémon's ability details

```bash
# Get the effect of an ability seen on a Pokémon
pokecli ability get intimidate
pokecli ability get levitate
```

## Example: Find the right nature for competitive play

```bash
# Which stat does modest boost/drop?
pokecli nature get modest

# Browse all 25 natures
pokecli nature list --limit 25
```

## Example: View a full evolution chain

```bash
# Branching evolution (Eevee has 8 evolutions)
pokecli pokemon evolution eevee

# Linear chain
pokecli pokemon evolution charmander

# Trade evolution
pokecli pokemon evolution haunter
```

## Example: Get a Pokémon's Pokédex entry and species data

```bash
# Capture rate, egg groups, flavor text, gender ratio
pokecli pokemon species bulbasaur

# Legendary check + habitat
pokecli pokemon species mewtwo
```

## Troubleshooting

For detailed command reference and data field descriptions, consult
`references/api-fields.md`. For multi-step recipes that chain commands across
resources, consult `references/workflows.md`.
