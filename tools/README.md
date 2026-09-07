# tools/

`index.html` is generated. Edit the modules here and run:

    python3 tools/build.py

| file | holds |
|---|---|
| `build.py` | assembles `index.html`; validates the translation tables |
| `i18n_ui.py` | landing, pricing, FAQ, shared UI strings |
| `i18n_home.py` | hero, the reactive/proactive explainer, onboarding, dashboard, goal ladder, SEO title/description |
| `i18n_quiz.py` | the profile the check-in produces, the micro-lessons, the achievements |
| `i18n_qbands.py` | the check-in questions, one set per age band |
| `i18n_chain.py` | the goal chain: areas, kinds, frequencies, obstacles, targets, and the micro-tips |
| `i18n_app.py` | onboarding, paywall, app shell, toasts |
| `i18n_content.py` | categories, stages, quotes, insights, theories |
| `i18n_plan.py` | exercises, skincare, hygiene, goal breakdowns, suggestions |
| `assets.py` | the inline SVG icon sprite |
| `css.py` | design tokens and all styles |
| `html.py` | page markup |
| `js_core.py` | i18n runtime, data tables, workout/skincare builders |
| `js_quiz.py` | check-in engine, scoring, profile, lessons, achievements, the daily next step |
| `js_chain.py` | the area → questions → goal → target chain, `startGoal()`, the tip engine |
| `js_app.py` | state, storage, migrations, pricing, onboarding |
| `js_render.py` | camera and every render function |
| `logo.b64` | the app logo as a data URI |

Translation entries are `'key': (he, en, fr, ru, ar)`. The build fails on a
duplicate key, a missing or empty language, a `{placeholder}` that does not
appear in all five languages, a malformed gender segment (see below), or an
age band of check-in questions with a key missing.

## Gender

A string addresses the user in their own grammatical gender with an inline
segment, `{masculine|feminine}`:

    '{אתה|את} {מתחיל|מתחילה} עכשיו'     he, whole words
    'בחר{|י} תחום'                        he, suffix
    'Tu es prêt{|e}'                      fr

`t()` resolves the segment *before* placeholder substitution, so a value the
user typed can never be re-read as a segment. `en` carries no segments. When
gender is unset the two forms are merged into the slash form (`מתחיל/ה`) by
`gmerge()`. The build rejects a segment whose two halves are identical, an
empty segment, or a stray brace, and prints how many keys inflect per language.

Gender is chosen in onboarding and stored under its own key, `proactive_gender`
(`m` | `f` | `n`), for the same reason as the theme keys below: it must survive a
refresh before the profile exists. It can be changed later in the profile card
on the progress page. Switching it re-renders exactly like switching language.

The app still ships as one self-contained `index.html`. `og.png`, `robots.txt`
and `sitemap.xml` sit next to it at the repository root and are the only other
files GitHub Pages serves.

## The check-in

Ten questions, two per dimension, defined in `js_quiz.py`. The *wording* comes
from `i18n_qbands.py` under `qz.<band>.<n>.<part>`, where the band follows the
user's age (`ageBand()`: `a13` 13–17, `a18` 18–29, `a30` 30–49, `a50` 50+) and
the part is `q` or one of the answers `a`–`d`. Scoring is positional and shared
across bands, so answer `a` of question 3 must mean the same thing in every
band — the header of `i18n_qbands.py` says so and the build checks that every
band has all fifty keys. Each answer carries a number in the a-b-c-d order; a
dimension score is the mean of its two questions, and the proactivity score is
the mean of the five dimensions. The band the user answered is stamped on the
result, and the profile offers a redo when the stored age no longer matches it. The result is not a
grade: it decides which of the five `rs.ac.<dim>.*` action sets the daily "next
step" is drawn from, and it sets `P.diff`, which is what sizes the seeded tasks.

The answers are written to their own `proactive_quiz` key rather than into the
profile, because the check-in runs *before* onboarding finishes and `save()` only
writes a profile once it does. `load()` folds them back in.

## The goal chain

A goal is no longer a free-text title with guessed steps. `js_chain.py` walks
the user through four screens — area, kind, times per week, main obstacle — and
composes a target from the answers: the ladder's top rung from area + kind +
frequency (`gt.title`), the weekly rung from frequency (`gw.line`), the daily
rung from the area (`gd.<area>`), and the "now" rung from the obstacle
(`gn.<obst>`). The nine areas share the frequency and obstacle sets; only the
kinds (`gk.<area>.1-6`, plus `gk.study.a.*` for adults) are per area.

The chain state `CH` is stored under `proactive_chain` so *back* and a refresh
lose nothing. It runs once inside onboarding and again from "new goal" on the
goals page; free-text goals are still there under a `<details>` on both.

A goal starts with `started:false`. Until the user presses *start the target*
its steps move no points, no weekly mission exists for it, and the streak is
untouched; `startGoal()` is the only place that flips it. Goals from before this
field existed are backfilled as started, since they were tracking already.

## Micro-tips

`tip(kind)` shows one short proactivity tip in `#tipCard`, keyed to what just
happened (`task.done`, `goal.new`, `goal.start`, `task.skip`, `streak`, `lesson`
…). Each kind fires at most once per day (`S.tips`), so the tips never nag.

## Pricing

`PRICES` in `js_app.py` holds the numbers; `CHECKOUT` holds the checkout URLs
for the two plans. While a URL is empty the plan renders without a buy button
and the "opening soon" line shows instead — there is no fake checkout. Nothing
is gated on a static site, and nothing pretends to be.

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

Additions inside version 4 (`S.tips`, `goal.started`, `S.quiz.band`) are
backfilled by `ensureV4Fields()` / `loadQuiz()` on every load, so no bump.

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

Onboarding asks for the colour directly, separately from gender — gender is
asked only so the app can address the user correctly, and never decides a
colour. The three dots and the sun/moon button in the top bar override it at
any time.
