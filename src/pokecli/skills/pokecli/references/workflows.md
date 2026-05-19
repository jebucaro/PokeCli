# pokecli Multi-Step Workflows

Recipes that traverse multiple PokeAPI resources to answer questions a single
`get` cannot. Each workflow shows the command sequence and the field on each
response that feeds the next call.

## Where can I catch Pokemon X?

The most direct path. Uses the `/pokemon/{id}/encounters/` sub-endpoint.

```bash
pokecli pokemon encounters pikachu
```

Returns a table of `location_area`, `version`, `method`, `chance`, and level
range for every recorded encounter. For agent piping:

```bash
pokecli pokemon encounters pikachu --format json
# → [{"location_area": {...}, "version_details": [...]}, ...]
```

Drill into a single area to see all Pokemon that share it:

```bash
pokecli location-area get trophy-garden-area
```

## What lives at Route N in region R?

Top-down traversal: region → location → location-area → encounter table.

```bash
# 1. List locations in a region
pokecli region get kanto
# → "Locations" table includes "kanto-route-1", "pallet-town", etc.

# 2. Inspect a location to see its sub-areas
pokecli location get kanto-route-1
# → "Areas" table: "kanto-route-1-area"

# 3. Get the encounter table for the area
pokecli location-area get kanto-route-1-area
# → "Pokemon Encounters" table: pokemon, version, method, chance, levels
```

JSON variant for scripting:

```bash
pokecli region get kanto --format json | jq '.locations[].name'
pokecli location-area get kanto-route-1-area --format json \
  | jq '.pokemon_encounters[].pokemon.name'
```

## What's new in Generation N?

```bash
pokecli generation get generation-i
# → "Pokemon Species" count + list, "Moves" count + list
```

Filter to just the species:

```bash
pokecli generation get generation-iii --format json \
  | jq -r '.pokemon_species[].name' | sort
```

## Regional Pokedex listing

```bash
pokecli pokedex get kanto
# → "Entries" table with entry numbers + species names

# Just the species, sorted by dex number:
pokecli pokedex get kanto --format json \
  | jq -r '.pokemon_entries[] | "\(.entry_number) \(.pokemon_species.name)"'
```

## Which TM teaches a move?

The `move get` response includes a `machines[]` field listing every
TM/HM/version-group combination that teaches it.

```bash
pokecli move get thunderbolt --format json | jq '.machines'
# → [{"machine": {"url": ".../machine/79/"}, "version_group": {"name": "red-blue"}}, ...]

# Pull a machine ID from the URL and inspect:
pokecli machine get 79
# → Item: tm24, Teaches Move: thunderbolt, Version Group: red-blue
```

Cross-reference with what Pokemon can learn it via TM:

```bash
pokecli pokemon moves charizard --move thunderbolt --method machine
```

## Full Pokemon profile

Stack the existing pokemon sub-commands to build a complete agent context:

```bash
pokecli pokemon get pikachu          # stats, types, abilities
pokecli pokemon species pikachu      # pokedex entry, egg groups, capture rate
pokecli pokemon evolution pikachu    # branching evolution chain
pokecli pokemon forms pikachu        # varieties (mega, alola, gmax, etc.)
pokecli pokemon encounters pikachu   # wild encounter locations
pokecli pokemon moves pikachu        # learnable moves
```

## Alternative form inspection

The species `varieties[]` is the source of truth for non-default forms.
`pokemon forms` lists them, then `pokemon-form get` inspects one.

```bash
pokecli pokemon forms charizard
# → charizard (default), charizard-mega-x, charizard-mega-y, charizard-gmax

pokecli pokemon-form get charizard-mega-x
# → Form Name: mega-x, Types: fire/dragon, Battle Only: yes, Mega: yes
```

## Evolution chain by chain ID

`pokemon evolution` resolves a chain by Pokemon name. If you already have a
chain ID (from a previous query), skip the lookup:

```bash
pokecli evolution-chain get 67
# → Eevee's full branching chain (Vaporeon, Jolteon, Sylveon, etc.)
```

## Decoding cross-reference fields

When `pokemon species pikachu` returns `egg_groups: ["ground", "fairy"]`, look
up each group:

```bash
pokecli egg-group get ground
pokecli egg-group get fairy
```

Same pattern for growth rates, damage classes, evolution triggers, learn
methods:

```bash
pokecli growth-rate get medium-slow
pokecli move-damage-class get special
pokecli evolution-trigger get use-item
pokecli move-learn-method get machine
```
