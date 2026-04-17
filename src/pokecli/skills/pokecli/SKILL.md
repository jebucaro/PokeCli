---
name: pokecli
description: Queries Pokémon, Berries, Items, Moves, Abilities, Types, Natures, evolution chains, and species data via the pokecli CLI. Use when the user needs to look up Pokémon stats, type matchups, abilities, natures, evolution chains, berries, items, or moves, download sprites, or manage the local cache. Also use when the user mentions "pokecli", "pokedex", or "PokeAPI"
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
```

## Global options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass local cache, fetch fresh from PokeAPI |
| `--format table` | Rich formatted table output (default) |
| `--format json` | Raw JSON with syntax highlighting |

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

# Agent-friendly: returns {"can_learn": true/false, "method": "...", "level": N}
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

For detailed command reference and data field descriptions, consult `references/api-fields.md`.
