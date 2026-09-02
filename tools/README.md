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
