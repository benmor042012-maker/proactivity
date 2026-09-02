#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assembles index.html from the modules in this directory.

The app ships as one self-contained index.html; this script exists so the
five-language translation table stays editable and verifiable. Run:

    python3 tools/build.py

Edit the i18n_*.py tables (or the CSS/HTML/JS modules) and re-run.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from i18n_ui import UI
from i18n_app import APP
from i18n_content import CONTENT
from i18n_plan import PLAN
from i18n_mini import MINI
from i18n_food import FOOD
from assets import sprite
from css import CSS
from html import build_body
from js_core import JS_CORE
from js_app import JS_APP
from js_render import JS_RENDER
from js_mini import JS_MINI

LANGS = ['he', 'en', 'fr', 'ru', 'ar']
OUT = os.path.join(ROOT, 'index.html')
LOGO_FILE = os.path.join(HERE, 'logo.b64')


def merged_table():
    table = {}
    for src, name in ((UI, 'i18n_ui'), (APP, 'i18n_app'),
                      (CONTENT, 'i18n_content'), (PLAN, 'i18n_plan'),
                      (MINI, 'i18n_mini'), (FOOD, 'i18n_food')):
        for k, v in src.items():
            if k in table:
                raise SystemExit(f'duplicate translation key {k!r} (in {name})')
            if len(v) != len(LANGS):
                raise SystemExit(f'key {k!r} has {len(v)} values, expected {len(LANGS)}')
            for j, s in enumerate(v):
                if not str(s).strip():
                    raise SystemExit(f'key {k!r} is empty for language {LANGS[j]!r}')
            table[k] = v
    return table


def i18n_js(table):
    per_lang = {L: {k: v[j] for k, v in table.items()} for j, L in enumerate(LANGS)}
    return 'var I18N=' + json.dumps(per_lang, ensure_ascii=False, separators=(',', ':')) + ';'


def check_placeholders(table):
    """Every {var} in the Hebrew source must exist in the other four."""
    bad = []
    for k, v in table.items():
        want = set(re.findall(r'\{(\w+)\}', v[0]))
        for j in range(1, len(LANGS)):
            got = set(re.findall(r'\{(\w+)\}', v[j]))
            if got != want:
                bad.append(f'{k} [{LANGS[j]}]: expected {sorted(want)}, got {sorted(got)}')
    if bad:
        raise SystemExit('placeholder mismatch:\n  ' + '\n  '.join(bad))


def main():
    table = merged_table()
    check_placeholders(table)

    with open(LOGO_FILE, encoding='utf-8') as f:
        logo = f.read().strip()

    fonts = ('https://fonts.googleapis.com/css2'
             '?family=Heebo:wght@400;500;600;700;900'
             '&family=Secular+One'
             '&family=Inter:wght@400;600;700'
             '&family=Noto+Sans+Arabic:wght@400;600;700'
             '&display=swap')

    # Sets dir/lang before first paint so there is no RTL/LTR flash.
    early = ("(function(){try{var l=localStorage.getItem('proactive_lang');"
             "if(!l){var n=(navigator.language||'he').slice(0,2);"
             "l=['he','en','fr','ru','ar'].indexOf(n)>=0?n:'he';}"
             "var d=document.documentElement;d.lang=l;"
             "d.dir=(l==='he'||l==='ar')?'rtl':'ltr';}catch(e){}})();")

    js = '\n'.join([i18n_js(table), JS_CORE, JS_APP, JS_MINI, JS_RENDER])

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="he" dir="rtl">\n<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="theme-color" content="#09090A">\n'
        '<meta name="description" content="Proactive - turn big goals into small daily steps, with photo proof.">\n'
        '<title>Proactive</title>\n'
        f'<script>{early}</script>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link rel="stylesheet" href="{fonts}">\n'
        f'<link rel="icon" href="{logo}">\n'
        f'<style>{CSS}</style>\n'
        '</head>\n<body>\n'
        + sprite() + '\n'
        + build_body(logo) + '\n'
        + '<script>' + js + '</script>\n'
        '</body>\n</html>\n'
    )

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'wrote {OUT}')
    print(f'  {len(table)} translation keys x {len(LANGS)} languages')
    print(f'  {len(html):,} bytes ({len(html) - 3 * len(logo):,} excluding the embedded logo)')


if __name__ == '__main__':
    main()
