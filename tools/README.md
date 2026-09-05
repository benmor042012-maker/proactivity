# tools/

`index.html` is generated. Edit the modules here and run:

    python3 tools/build.py

| file | holds |
|---|---|
| `build.py` | assembles `index.html`; validates the translation tables |
| `i18n_ui.py` | landing, pricing, FAQ, shared UI strings |
| `i18n_app.py` | onboarding, paywall, app shell, toasts |
| `i18n_content.py` | categories, stages, quotes, insights, theories |
| `i18n_plan.py` | exercises, skincare, hygiene, goal breakdowns, suggestions |
| `assets.py` | the inline SVG icon sprite |
| `css.py` | design tokens and all styles |
| `html.py` | page markup |
| `js_core.py` | i18n runtime, data tables, workout/skincare builders |
| `js_app.py` | state, storage, pricing, onboarding |
| `js_render.py` | camera and every render function |
| `logo.b64` | the app logo as a data URI |

Translation entries are `'key': (he, en, fr, ru, ar)`. The build fails on a
duplicate key, a missing or empty language, or a `{placeholder}` that does not
appear in all five languages.

The app still ships as one self-contained `index.html` — nothing here is served.

## Mini-apps

The Body tab is a small router (`showMini`) over four views: a hub plus the
sport, skincare and fridge mini-apps. All three are local-only — no API, no
key, no backend. The fridge photo is read with `FileReader`, downscaled to
900px and kept in `localStorage`; nothing is ever uploaded.

| file | holds |
|---|---|
| `i18n_mini.py` | mini-app interface strings |
| `i18n_food.py` | 31 ingredients and 17 recipes (name + steps) |
| `js_mini.py` | the router and all three mini-apps |

The sport app builds its five workouts from the `ex.*` and `cue.*` keys that
already ship translated, so adding a workout usually needs no new translation.

Stored state lives under `S.mini` and is versioned: `STORE_V` is 3, and
`load()` chains `migrateV1` then `migrateV2` so an old save upgrades in one
pass without losing anything.

## Themes

Colour is layered: base tokens, then surfaces (`data-theme` = dark|light),
then accent (`data-accent` = flame|bloom|mint). Both attributes are written to
`<html>` by the head script before first paint, so there is no flash.

`tools/themegen.py` (in the scratchpad during development, inlined into
`css.py`) generated the six surface x accent blocks. Each accent carries a
different tone per mode — a colour bright enough on a dark background fails
contrast on a light one.

Appearance is stored under its own keys, `proactive_accent` and
`proactive_theme`, not inside the profile: the profile is only written once
onboarding finishes, and a colour picked earlier must still survive a refresh.

The onboarding question only picks a *default* accent. The three dots and the
sun/moon button in the top bar override it at any time.
