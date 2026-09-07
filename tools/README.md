# tools/

`index.html` is generated. Edit the modules here and run:

    python3 tools/build.py

| file | holds |
|---|---|
| `build.py` | assembles `index.html`; validates the translation tables |
| `i18n_ui.py` | landing, pricing, FAQ, shared UI strings |
| `i18n_home.py` | hero, the reactive/proactive explainer, onboarding, dashboard, goal ladder, SEO title/description |
| `i18n_quiz.py` | the check-in questions, the profile it produces, the micro-lessons, the achievements |
| `i18n_app.py` | onboarding, paywall, app shell, toasts |
| `i18n_content.py` | categories, stages, quotes, insights, theories |
| `i18n_plan.py` | exercises, skincare, hygiene, goal breakdowns, suggestions |
| `assets.py` | the inline SVG icon sprite |
| `css.py` | design tokens and all styles |
| `html.py` | page markup |
| `js_core.py` | i18n runtime, data tables, workout/skincare builders |
| `js_quiz.py` | check-in engine, scoring, profile, lessons, achievements, the daily next step |
| `js_app.py` | state, storage, migrations, pricing, onboarding |
| `js_render.py` | camera and every render function |
| `logo.b64` | the app logo as a data URI |

Translation entries are `'key': (he, en, fr, ru, ar)`. The build fails on a
duplicate key, a missing or empty language, or a `{placeholder}` that does not
appear in all five languages.

The app still ships as one self-contained `index.html`. `og.png`, `robots.txt`
and `sitemap.xml` sit next to it at the repository root and are the only other
files GitHub Pages serves.

## The check-in

Ten questions, two per dimension, defined in `js_quiz.py`. Each answer carries a
number in the a-b-c-d order; a dimension score is the mean of its two questions,
and the proactivity score is the mean of the five dimensions. The result is not a
grade: it decides which of the five `rs.ac.<dim>.*` action sets the daily "next
step" is drawn from, and it sets `P.diff`, which is what sizes the seeded tasks.

The answers are written to their own `proactive_quiz` key rather than into the
profile, because the check-in runs *before* onboarding finishes and `save()` only
writes a profile once it does. `load()` folds them back in.

## Navigation

One `<nav class="tabs">` serves as top tabs on a wide screen and as the fixed
bottom bar under 760px, so there is a single set of buttons and one `goPage()`.
The chosen tab is remembered in `proactive_tab`.

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

Stored state lives under `S.mini` — see *Storage versions* below.

## Storage versions

`STORE_V` is 4 and `load()` chains `migrateV1` → `migrateV2` → `migrateV3`, so a
save from any earlier build upgrades in one pass. Every migration is additive:

| version | adds |
|---|---|
| 2 | translation keys instead of hardcoded Hebrew labels |
| 3 | the mini-apps (`S.mini`) |
| 4 | `S.quiz`, `S.lessons`, `S.ach`, `S.day`, `S.stats` |

`S.streak` and `S.chDone` are dead fields kept only so an old save round-trips
unchanged. The streak the user sees is `S.day`, a real run of calendar days
maintained by `markActiveToday()` — the single place any action reports in.

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

Onboarding asks for the colour directly (it used to ask whether you were a boy
or a girl and derive one, which was personal information the app never needed).
The three dots and the sun/moon button in the top bar override it at any time.
