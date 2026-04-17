# pokecli API Field Reference

Detailed data fields returned by each resource type. Consult this when you need
to interpret or explain specific fields from `pokecli` output.

## Pokemon Fields

| Field | Description |
|-------|-------------|
| Name | Pokémon species name |
| ID | National Pokédex number |
| Types | Elemental types (e.g. Fire, Water, Grass) |
| Stats | HP, Attack, Defense, Sp. Atk, Sp. Def, Speed (base values) |
| Abilities | Normal and hidden abilities |
| Height | Height in decimetres |
| Weight | Weight in hectograms |
| Base Experience | Experience gained by defeating this Pokémon |

## Pokemon Moves Fields

Returned by `pokecli pokemon moves <name_or_id>`.

| Field | Description |
|-------|-------------|
| `name` | Move name (hyphen-separated, e.g. `flamethrower`) |
| `learn_method` | How the move is learned: `level-up`, `machine`, `tutor`, or `egg` |
| `level` | Level at which the move is learned (level-up only; `0` for all others) |

Results are deduplicated across all game versions. Each move appears once,
with the learn method taken from the most recent game version that includes it.
Sorted: level-up moves first (by level), then machine/tutor/egg alphabetically.

## Ability Fields

Returned by `pokecli ability get <name_or_id>`.

| Field | Description |
|-------|-------------|
| Name | Ability name (hyphen-separated, e.g. `speed-boost`) |
| ID | Ability identifier |
| Generation | Generation in which the ability was introduced |
| Pokemon with this ability | Count of Pokémon that can have this ability |
| Effect | Short mechanical effect summary |
| Full Effect | Detailed description including edge cases |

## Nature Fields

Returned by `pokecli nature get <name_or_id>`.

| Field | Description |
|-------|-------------|
| Name | Nature name |
| ID | Nature identifier |
| Stat Modifier | Which stat is boosted +10% and which is reduced -10% (or "Neutral" if no change) |
| Likes Flavor | Berry flavor this nature prefers |
| Hates Flavor | Berry flavor this nature dislikes |

There are 25 natures. 5 are neutral (no stat change). The remaining 20 each boost one stat and drop another.

## Type Fields

Returned by `pokecli type get <name_or_id>`.

| Field | Description |
|-------|-------------|
| Name | Type name (e.g. `fire`, `dragon`) |
| ID | Type identifier |
| Pokemon | Count of Pokémon with this type |
| Moves | Count of moves of this type |
| Super effective → | Types this deals 2× damage to (attacking) |
| Not very effective → | Types this deals 0.5× damage to (attacking) |
| No effect → | Types this deals 0× damage to (attacking) |
| Weak to ← | Types that deal 2× damage to this type (defending) |
| Resists ← | Types that deal 0.5× damage to this type (defending) |
| Immune to ← | Types that deal 0× damage to this type (defending) |

## Pokemon Species Fields

Returned by `pokecli pokemon species <name_or_id>`.

| Field | Description |
|-------|-------------|
| Name | Pokémon species name |
| ID | National Pokédex number |
| Legendary / Mythical | Flags shown in the header if applicable |
| Genus | Species descriptor (e.g. "Mouse Pokémon") |
| Generation | Generation in which the species was introduced |
| Color | Body color category |
| Growth Rate | Level-up experience curve (e.g. medium-slow) |
| Capture Rate | Catch rate out of 255 (higher = easier to catch) |
| Base Happiness | Starting friendship value |
| Gender | Male/female percentage ratio, or "Genderless" |
| Egg Groups | Breeding compatibility groups |
| Flavor Text | Latest English Pokédex entry with game version |

## Evolution Chain Fields

Returned by `pokecli pokemon evolution <name_or_id>`.

Displayed as a tree. Each node shows the species name and the condition required to evolve from the previous stage.

| Trigger | Example condition shown |
|---------|------------------------|
| `level-up` | `level 16`, `happiness 160`, `affection 2`, `knowing <move>`, `at <location>` |
| `use-item` | `use water-stone`, `use thunder-stone` |
| `trade` | `trade`, `trade holding metal-coat` |
| `shed` | `shed (level 20, empty slot, Pokeball)` |

Additional modifiers appended when present: `(day)`, `(night)`, `(rain)`, `(upside-down)`, `holding <item>`.

## Berry Fields

| Field | Description |
|-------|-------------|
| Name | Berry name |
| ID | Berry identifier |
| Growth Time | Hours per growth stage |
| Max Harvest | Maximum berries per harvest |
| Firmness | Texture category (very-soft to super-hard) |
| Flavors | Spicy, Dry, Sweet, Bitter, Sour (potency values) |
| Natural Gift Power | Power when used as Natural Gift move |
| Natural Gift Type | Type when used as Natural Gift move |

## Item Fields

| Field | Description |
|-------|-------------|
| Name | Item name |
| ID | Item identifier |
| Cost | Purchase price in Pokédollars |
| Category | Item category (e.g. medicine, pokeball) |
| Fling Power | Power when used with Fling move |
| Effect | Short mechanical effect text |
| Flavor Text | In-game description |

## Move Fields

| Field | Description |
|-------|-------------|
| Name | Move name |
| ID | Move identifier |
| Type | Elemental type |
| Damage Class | physical, special, or status |
| Power | Base power (null for status moves) |
| Accuracy | Hit chance percentage (null if always hits) |
| PP | Power Points (number of uses) |
| Effect Chance | Percentage chance of secondary effect |
| Effect | Mechanical effect description |

## Sprite Variants

| Variant Key | Description |
|-------------|-------------|
| `front_default` | Standard front-facing sprite |
| `front_shiny` | Shiny coloration, front-facing |
| `back_default` | Standard back-facing sprite |
| `back_shiny` | Shiny coloration, back-facing |
| `front_female` | Female variant, front-facing (if exists) |
| `front_shiny_female` | Shiny female variant, front-facing (if exists) |

## Cache Location

All cached responses are stored at `~/.pokecli/cache.json` using TinyDB.
Each entry is keyed by resource type and name/ID.

Tracked resource tables: `pokemon`, `berry`, `item`, `move`, `ability`, `nature`, `type`, `pokemon-species`, `evolution-chain`.

All tables are visible in `pokecli cache stats` and can be cleared individually with `pokecli cache clear --resource <table>`.

## Data Source

All data originates from [PokeAPI](https://pokeapi.co/api/v2).
No authentication required. Free and open.
