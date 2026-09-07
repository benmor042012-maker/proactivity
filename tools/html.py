# -*- coding: utf-8 -*-
"""HTML body. LOGO is substituted at build time.
data-i18n sets textContent, data-i18n-html sets innerHTML, data-i18n-ph sets placeholder."""

def i(name, cls=''):
    c = ('ic ' + cls).strip()
    return f'<svg class="{c}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def benefit(n, key):
    return f'<div class="ben">{i(n)}<span data-i18n="{key}"></span></div>'


def step_block(num):
    return (f'<li class="stp"><div class="num" aria-hidden="true">{num}</div><div>'
            f'<h3 data-i18n="n.how.{num}.t"></h3><p data-i18n="n.how.{num}.d"></p></div></li>')


def scenario(n):
    """One everyday situation shown twice: waiting for it, and acting on it."""
    return (f'<li class="sc">'
            f'<div class="sc-h">{i("compass")}<span data-i18n="n.sc.{n}.t"></span></div>'
            f'<div class="sc-r"><span class="sc-tag">{i("x")}<span data-i18n="n.def.re"></span></span>'
            f'<p data-i18n="n.sc.{n}.r"></p></div>'
            f'<div class="sc-p"><span class="sc-tag">{i("check")}<span data-i18n="n.def.pro"></span></span>'
            f'<p data-i18n="n.sc.{n}.p"></p></div></li>')


def faq_item(n):
    return (f'<details><summary><span data-i18n="l.faq.q{n}"></span>{i("chevron")}</summary>'
            f'<p data-i18n="l.faq.a{n}"></p></details>')


def plan_card(pid, feature=False):
    tag = (f'<div class="tag"><span data-i18n="l.pr.popular"></span>'
           f'<span class="dot"></span><span data-i18n="l.pr.save"></span></div>') if feature else ''
    feats = ''.join(f'<li>{i("check")}<span data-i18n="l.pr.f{n}"></span></li>' for n in range(1, 7))
    btn = 'btn-primary' if feature else 'btn-ghost'
    return (f'<div class="plan{" feature" if feature else ""}">{tag}'
            f'<h3 data-i18n="l.pr.{pid}"></h3>'
            f'<div class="price"><span class="amt" data-price="{pid}"></span>'
            f'<span class="per" data-i18n="l.pr.permonth"></span></div>'
            f'<div class="bill" data-bill="{pid}"></div>'
            f'<ul>{feats}</ul>'
            f'<button class="btn {btn} btn-block" data-buy="{pid}" data-i18n="l.pr.cta"></button></div>')


def opt(attr, val, icon, key):
    return (f'<button type="button" class="opt" data-{attr}="{val}" aria-pressed="false">{i(icon)}'
            f'<span data-i18n="{key}"></span></button>')


def nav(back=True, next_id=None, next_key='c.next', skip=None):
    out = ''
    if back:
        out += (f'<button class="btn btn-ghost" data-back>{i("chevron","flip")}'
                f'<span data-i18n="c.back"></span></button>')
    if skip:
        out += f'<button class="btn btn-quiet" id="{skip[0]}" data-i18n="{skip[1]}"></button>'
    nid = f' id="{next_id}"' if next_id else ' data-next'
    out += (f'<button class="btn btn-primary"{nid}><span data-i18n="{next_key}"></span>'
            f'{i("arrow")}</button>')
    return f'<div class="nav">{out}</div>'


TABS = [('home', 'home', 'n.tab.home'),
        ('tasks', 'check', 'n.tab.tasks'),
        ('goals', 'target', 'a.tab.goals'),
        ('progress', 'trending', 'n.tab.prog'),
        ('learn', 'brain', 'n.tab.learn'),
        ('body', 'activity', 'a.tab.body')]

LANGS = [('he', 'עברית', 'עב'), ('en', 'English', 'EN'), ('fr', 'Français', 'FR'),
         ('ru', 'Русский', 'RU'), ('ar', 'العربية', 'ع')]


def build_body(logo):
    L = ''.join(f'<button class="langbtn" data-lang="{c}" data-short="{sh}" lang="{c}">{n}</button>'
                for c, n, sh in LANGS)
    L += ('<span class="bar-sep" aria-hidden="true"></span>'
          + ''.join(f'<button class="accdot" data-set-accent="{a}" '
                    f'data-i18n-title="th.acc.{a}" aria-label="{a}"></button>'
                    for a in ('flame', 'bloom', 'mint'))
          + f'<button class="modebtn" id="modeBtn" data-i18n-title="th.dark">'
            f'{i("sun","ic-sun")}{i("moon","ic-moon")}</button>')

    # ---------- landing ----------
    landing = f'''
<main class="landing" id="landing">
 <div class="wrap">

  <section class="hero">
   <p class="kicker">{i("sparkles")}<span data-i18n="n.hero.kicker"></span></p>
   <h1><span data-i18n="n.hero.a"></span><br><span class="dim" data-i18n="n.hero.b"></span></h1>
   <p class="lead" data-i18n="n.hero.sub"></p>
   <div class="cta-row">
    <button class="btn btn-primary btn-lg" id="ctaTop"><span data-i18n="n.hero.cta"></span>{i("arrow")}</button>
    <a class="btn btn-ghost" href="#what"><span data-i18n="n.hero.cta2"></span></a>
   </div>
   <p class="fineprint">{i("shield")}<span data-i18n="n.hero.note"></span></p>
  </section>

  <section class="blk" id="what">
   <h2 data-i18n="n.def.t"></h2>
   <p class="lede" data-i18n="n.def.b"></p>
   <p class="sc-hint" data-i18n="n.def.hint"></p>
   <ul class="scgrid">{''.join(scenario(n) for n in range(1, 9))}</ul>
   <p class="sc-close">{i("seedling")}<span data-i18n="n.def.close"></span></p>
  </section>

  <div class="proof">
   <div><div class="n">10</div><div class="l" data-i18n="n.pf1.t"></div></div>
   <div><div class="n">5</div><div class="l" data-i18n="n.pf2.t"></div></div>
   <div><div class="n">5</div><div class="l" data-i18n="n.pf3.t"></div></div>
  </div>

  <section class="blk" id="how">
   <h2 data-i18n="n.how.t"></h2>
   <ol class="steps">{step_block(1)}{step_block(2)}{step_block(3)}</ol>
  </section>

  <section class="blk">
   <h2 data-i18n="l.why.t"></h2>
   <div class="bengrid">
    {benefit("target","l.why.1")}{benefit("rocket","l.why.2")}{benefit("refresh","l.why.3")}
    {benefit("users","l.why.4")}{benefit("book","l.why.5")}{benefit("activity","l.why.6")}
    {benefit("clock","l.why.7")}{benefit("compass","l.why.8")}
   </div>
  </section>

  <section class="blk" id="pricing">
   <h2 data-i18n="l.pr.t"></h2>
   <p class="lede" style="margin-bottom:var(--s5)" data-i18n="l.pr.sub"></p>
   <div class="plans">{plan_card("monthly")}{plan_card("annual", True)}</div>
   <p class="trust" data-i18n="l.pr.trust"></p>
  </section>

  <section class="blk faq">
   <h2 data-i18n="l.faq.t"></h2>
   {''.join(faq_item(n) for n in range(1,7))}
  </section>

  <section class="finale">
   <h2 data-i18n="n.fin.t"></h2>
   <p data-i18n="n.fin.sub"></p>
   <button class="btn btn-primary btn-lg" id="ctaBottom"><span data-i18n="n.hero.cta"></span>{i("arrow")}</button>
  </section>

  <footer data-i18n="l.footer"></footer>
 </div>
</main>
<div class="sticky-cta" id="stickyCta">
 <button class="btn btn-primary btn-block" id="ctaSticky"><span data-i18n="n.hero.cta"></span>{i("arrow")}</button>
</div>'''

    # ---------- onboarding ----------
    colours = ''.join(
        f'<button type="button" class="opt swatch" data-acc="{a}" aria-pressed="false">'
        f'<span class="sw sw-{a}" aria-hidden="true"></span>'
        f'<span data-i18n="th.acc.{a}"></span></button>'
        for a in ('mint', 'flame', 'bloom'))

    onb = f'''
<div class="onb" id="onboarding" role="dialog" aria-modal="true" aria-labelledby="onbHead"><div class="onb-inner">
 <div class="onb-top">
  <div class="mark"><img src="{logo}" alt="" width="28" height="28"><span data-i18n="b.name"></span></div>
  <div class="count" id="stepCount"></div>
 </div>
 <div class="bar"><i id="onbBar" style="width:14%"></i></div>

 <section class="step on" data-step="1">
  <h2 id="onbHead" data-i18n="n.o.1.t"></h2><p class="sub" data-i18n="n.o.1.s"></p>
  <ul class="welc">
   <li>{i("compass")}<span data-i18n="n.o.1.p1"></span></li>
   <li>{i("gauge")}<span data-i18n="n.o.1.p2"></span></li>
   <li>{i("rocket")}<span data-i18n="n.o.1.p3"></span></li>
  </ul>
  <div class="note">{i("shield")}<span data-i18n="n.hero.note"></span></div>
  {nav(back=False, next_key="n.o.1.go")}
 </section>

 <section class="step" data-step="2">
  <h2 data-i18n="n.o.2.t"></h2><p class="sub" data-i18n="n.o.2.s"></p>
  <div class="field"><label for="oName" data-i18n="n.o.2.name"></label>
   <input type="text" id="oName" autocomplete="nickname" data-i18n-ph="n.o.2.nameph"></div>
  <div class="field"><label for="oAge" data-i18n="n.o.2.age"></label>
   <input type="number" id="oAge" min="13" max="120" step="1" inputmode="numeric"
          enterkeyhint="next" autocomplete="off" data-i18n-ph="o.age.ph">
   <p class="hint agehint" id="oAgeBand"></p></div>
  <div class="qlabel" data-i18n="n.o.2.gender"></div>
  <div class="opts" id="oGender">
   {opt("gnd","m","user","o.iam.boy")}{opt("gnd","f","user","o.iam.girl")}{opt("gnd","n","compass","o.iam.na")}
  </div>
  <p class="hint">{i("sparkles")}<span data-i18n="n.o.2.gendern"></span></p>
  <div class="qlabel" data-i18n="n.o.2.color"></div>
  <div class="opts" id="oAcc">{colours}</div>
  <p class="hint">{i("palette")}<span data-i18n="n.o.2.colorn"></span></p>
  <div class="note">{i("lock")}<span data-i18n="n.o.2.privacy"></span></div>
  {nav()}
 </section>

 <section class="step" data-step="3">
  <h2 data-i18n="n.o.3.t"></h2><p class="sub" data-i18n="n.o.3.s"></p>
  <div class="opts" id="oGoals"></div>
  <div class="field" style="margin-top:var(--s4)"><label for="oCustom" data-i18n="o.2.custom"></label>
   <div class="addrow"><input type="text" id="oCustom" data-i18n-ph="o.2.custom.ph">
   <button class="btn btn-ghost" id="addCustom" data-i18n-title="c.add">{i("plus")}</button></div></div>
  <div class="qlabel" data-i18n="n.o.3.time"></div>
  <div class="opts" id="oTime">
   {opt("time","15","zap","o.time.15")}{opt("time","30","flame","o.time.30")}{opt("time","45","gem","o.time.45")}
  </div>
  {nav()}
 </section>

 <section class="step" data-step="4">
  <div id="qzIntro">
   <h2 class="qz-h" data-i18n="qz.t"></h2>
   <p class="sub" data-i18n="qz.s"></p>
  </div>
  <div class="qz-meta"><span class="qz-count" id="qzCount"></span><span class="qz-dim" id="qzDim"></span></div>
  <div class="bar qz-bar"><i id="qzBar" style="width:10%"></i></div>
  <h3 class="qz-q" id="qzQ" aria-live="polite"></h3>
  <div class="qz-opts" id="qzOpts"></div>
  <div class="qz-foot">
   <button class="btn btn-quiet" id="qzPrev">{i("chevron","flip")}<span data-i18n="qz.prev"></span></button>
  </div>
  <p class="hint">{i("shield")}<span data-i18n="qz.notest"></span></p>
 </section>

 <section class="step" data-step="5">
  <h2 data-i18n="rs.t"></h2><p class="sub" data-i18n="rs.s"></p>
  <div class="profile" id="rsBody"></div>
  {nav(back=False, next_id="rsNext", next_key="rs.cta")}
 </section>

 <section class="step" data-step="6">
  <h2 data-i18n="n.o.5.t"></h2><p class="sub" data-i18n="n.o.5.s"></p>
  <div class="field"><input type="text" id="oG1" data-i18n-ph="n.o.5.ph"></div>
  {nav(skip=("skipGoal","n.o.5.skip"))}
 </section>

 <section class="step" data-step="7">
  <h2 data-i18n="n.o.6.t"></h2><p class="sub" data-i18n="n.o.6.s"></p>
  <div class="qlabel" data-i18n="o.5.goal"></div>
  <div class="opts" id="oWO">
   {opt("wo","strength","activity","wo.strength")}{opt("wo","cardio","trending","wo.cardio")}
   {opt("wo","flex","seedling","wo.flex")}{opt("wo","general","sparkles","wo.general")}
  </div>
  <div class="qlabel" data-i18n="o.5.exp"></div>
  <div class="opts" id="oFL">
   {opt("fl","beginner","seedling","fl.beginner")}{opt("fl","basic","flame","fl.basic")}{opt("fl","inter","gem","fl.inter")}
  </div>
  <div class="qlabel" data-i18n="o.6.skin"></div>
  <div class="opts" id="oSkin">
   {opt("skin","normal","user","sk.type.normal")}{opt("skin","oily","drop","sk.type.oily")}
   {opt("skin","dry","sun","sk.type.dry")}{opt("skin","combo","refresh","sk.type.combo")}
   {opt("skin","dunno","compass","sk.type.dunno")}
  </div>
  {nav(skip=("skipBody","n.o.6.skip"), next_id="oFinish", next_key="n.o.6.finish")}
 </section>

 <section class="step" data-step="8">
  <h2 data-i18n="o.9.t"></h2><p class="sub" data-i18n="o.9.s"></p>
  <div class="built" id="builtList"></div>
  <div class="plans">{plan_card("monthly")}{plan_card("annual", True)}</div>
  <p class="trust" data-i18n="l.pr.trust"></p>
  <div class="nav" style="flex-direction:column;gap:var(--s2)">
   <button class="btn btn-ghost btn-block" id="skipPay" data-i18n="o.9.later"></button>
   <p class="trust" style="margin:0" data-i18n="o.9.laternote"></p>
  </div>
 </section>
</div></div>'''

    tabs = ''.join(
        f'<button class="tab" data-page="{p}" role="tab" aria-selected="false" '
        f'aria-controls="page-{p}">{i(ic_)}<span data-i18n="{k}"></span></button>'
        for p, ic_, k in TABS)

    # ---------- app ----------
    app = f'''
<div id="app"><div class="wrap">
 <div class="trialbar" id="trialBar">
  {i("flame")}<span id="trialTxt"></span>
  <button id="trialCta" data-i18n="trial.cta"></button>
 </div>

 <header class="apphead">
  <div class="who"><img src="{logo}" alt="" width="40" height="40">
   <div><p class="greet" id="greetName"></p><p class="quote" id="proQuote"></p><p class="date" id="dateStr"></p></div>
  </div>
  <div class="lvl">
   <div class="row">
    <span class="lab"><span data-i18n="a.level"></span><span class="num" id="lvl">1</span></span>
    <span class="stage" id="stg"></span>
   </div>
   <div class="xp"><i id="xpF" style="width:0%"></i></div>
  </div>
 </header>

 <nav class="tabs" id="tabBar" role="tablist" data-i18n-title="n.nav.label">{tabs}</nav>

 <div class="page" id="page-home" role="tabpanel">
  <div class="dash-grid" id="dashStats"></div>
  <div class="nextcard" id="nextCard"></div>
  <div class="dash-two">
   <section class="dash-box">
    <h2 class="boxh">{i("gauge")}<span data-i18n="d.profile"></span></h2>
    <div id="dashProfile"></div>
   </section>
   <section class="dash-box">
    <h2 class="boxh">{i("compass")}<span data-i18n="d.focus"></span></h2>
    <div id="dashFocus"></div>
   </section>
  </div>
  <div id="dIns"></div>
 </div>

 <div class="page" id="page-tasks" role="tabpanel">
  <h2 class="ptitle" data-i18n="n.tk.t"></h2><p class="psub" data-i18n="n.tk.s"></p>
  <div class="ringbox">
   <div class="ringwrap"><svg viewBox="0 0 132 132" id="rSvg" role="img" data-i18n-title="h.ring.t"></svg>
    <div class="ringmid"><div class="pct" id="rPct">0%</div><div class="cap" data-i18n="h.done"></div></div></div>
   <div class="ringtxt">
    <h3 data-i18n="h.ring.t"></h3><p data-i18n="h.ring.s"></p>
    <div class="stats">
     <div class="stat"><div class="v">{i("flame")}<span id="skV">0</span></div><div class="k" data-i18n="h.streak"></div></div>
     <div class="stat"><div class="v">{i("star")}<span id="ptV">0</span></div><div class="k" data-i18n="h.points"></div></div>
     <div class="stat"><div class="v">{i("check")}<span class="numf"><span id="dnV">0</span>/<span id="tlV">0</span></span></div><div class="k" data-i18n="h.tasks"></div></div>
    </div>
   </div>
  </div>
  <div class="catgrid" id="catGrid"></div>
 </div>

 <div class="page" id="page-goals" role="tabpanel">
  <h2 class="ptitle" data-i18n="g.t"></h2><p class="psub" data-i18n="g.s"></p>
  <div class="newrow"><input type="text" id="nGoalIn" data-i18n-ph="g.new.ph" data-i18n-title="g.new.ph">
   <button class="btn btn-primary" id="aGoalBtn">{i("plus")}<span data-i18n="c.add"></span></button></div>
  <div id="goalsCont"></div>
 </div>

 <div class="page" id="page-progress" role="tabpanel">
  <h2 class="ptitle" data-i18n="n.pg.t"></h2><p class="psub" data-i18n="n.pg.s"></p>

  <section class="dash-box">
   <h3 class="boxh">{i("gauge")}<span data-i18n="rs.t"></span></h3>
   <div class="profile" id="profBody"></div>
  </section>

  <section class="dash-box">
   <div class="boxh-row"><h3 class="boxh">{i("star")}<span data-i18n="ac.t"></span></h3>
    <span class="boxh-n" id="acCount"></span></div>
   <p class="psub" data-i18n="ac.s"></p>
   <div class="achgrid" id="acGrid"></div>
  </section>

  <section class="dash-box">
   <h3 class="boxh">{i("calendar")}<span data-i18n="n.pg.week"></span></h3>
   <p class="psub" data-i18n="w.s"></p>
   <div class="wkbar">
    <div><span data-i18n="w.met"></span> <span class="numf"><b id="wMet">0</b>/<span id="wTot">0</span></span></div>
    <button class="btn btn-ghost btn-sm" id="rWkBtn">{i("refresh")}<span data-i18n="w.reset"></span></button>
   </div>
   <div class="scroller"><table class="grid"><caption class="sr" data-i18n="n.pg.week"></caption>
    <thead><tr id="wHead"></tr></thead><tbody id="wBody"></tbody></table></div>
   <div class="addrow" style="margin-top:var(--s3)">
    <input type="text" id="nMis" data-i18n-ph="w.new.ph" data-i18n-title="w.new.ph">
    <select id="nMisCat" style="max-width:150px" data-i18n-title="w.col.mission"></select>
    <input type="number" id="nMisT" min="1" max="7" value="3" data-i18n-title="w.target">
    <button class="btn btn-primary" id="aMisBtn" data-i18n-title="c.add">{i("plus")}</button>
   </div>
   <div class="review">
    <h4 data-i18n="w.rev.t"></h4><p data-i18n="w.rev.s"></p>
    <button class="btn btn-ghost btn-sm" id="rvBtn">{i("flag")}<span data-i18n="w.rev.btn"></span></button>
    <div class="rvout" id="rvRes"></div>
   </div>
  </section>
 </div>

 <div class="page" id="page-learn" role="tabpanel">
  <h2 class="ptitle" data-i18n="ls.t"></h2><p class="psub" data-i18n="ls.s"></p>
  <div class="lsgrid" id="lsGrid"></div>
  <h3 class="ptitle sechead" data-i18n="y.t"></h3><p class="psub" data-i18n="y.s"></p>
  <div class="thgrid" id="thGrid"></div>
 </div>

 <div class="page wide" id="page-body" role="tabpanel">

  <div class="mini-view on" data-mini="hub">
   <h2 class="ptitle" data-i18n="m.hub.t"></h2><p class="psub" data-i18n="m.hub.s"></p>
   <div class="mini-hub" id="hubGrid"></div>
   <h3 class="ptitle sechead" data-i18n="bd.hy.t"></h3><p class="psub" data-i18n="bd.hy.s"></p>
   <div class="plangrid" id="hyGrid"></div>
  </div>

  <div class="mini-view" data-mini="sport" id="miniSport">
   <div class="mini-top">
    <button class="btn btn-ghost btn-sm" data-mini-back>{i("chevron","flip")}<span data-i18n="m.back"></span></button>
    <h2 data-i18n="sp.t"></h2>
   </div>

   <div class="sp-screen on" data-sp="home">
    <div class="stat-row">
     <div class="stat-box"><div class="v" id="spTotal">0</div><div class="k" data-i18n="sp.total"></div></div>
     <div class="stat-box"><div class="v" id="spStreak">0</div><div class="k" data-i18n="sp.streak"></div></div>
     <div class="stat-box"><div class="v numf" id="spWeek">0/7</div><div class="k" data-i18n="sp.week"></div></div>
    </div>
    <div class="gbar"><i id="spWeekBar" style="width:0%"></i></div>
    <p class="hint" id="spFirst" data-i18n="sp.first"></p>
    <button class="big-btn" id="spStart">{i("play")}<span data-i18n="sp.start"></span></button>
    <div class="row-btns">
     <button class="btn btn-ghost" id="spProgress">{i("trending")}<span data-i18n="sp.progress"></span></button>
    </div>
    <h3 class="sub-h" data-i18n="sp.myplan"></h3>
    <p class="psub" id="woSub"></p>
    <div class="infoline" id="woInfo"></div>
    <div class="plangrid" id="woGrid"></div>
   </div>

   <div class="sp-screen" data-sp="pick">
    <h3 class="sub-h" data-i18n="sp.pick.t"></h3>
    <p class="psub" data-i18n="sp.pick.s"></p>
    <div class="pick-grid" id="spPickGrid"></div>
    <button class="btn btn-quiet" id="spPickBack">{i("chevron","flip")}<span data-i18n="m.back"></span></button>
   </div>

   <div class="sp-screen" data-sp="run">
    <div class="dots" id="spDots"></div>
    <div class="ex-card" id="spExBody">
     <div class="ex-of" id="spOf"></div>
     <div class="ex-n" id="spExName"></div>
     <div class="ex-r" id="spExReps"></div>
     <div class="ex-c" id="spExCue"></div>
     <button class="big-btn" id="spDid">{i("check")}<span data-i18n="sp.did"></span></button>
    </div>
    <div class="rest" id="spRest">
     <div class="rest-l" data-i18n="sp.rest"></div>
     <div class="rest-n" id="spRestN">0</div>
     <div class="rest-x" id="spRestNext"></div>
     <button class="btn btn-ghost btn-sm" id="spSkipRest">{i("arrow")}<span data-i18n="sp.skip"></span></button>
    </div>
    <p class="hint safe">{i("shield")}<span data-i18n="sp.safe"></span></p>
    <button class="btn btn-quiet" id="spQuit" data-i18n="sp.quit"></button>
   </div>

   <div class="sp-screen" data-sp="done">
    <div class="done-card">
     {i("check", "big-check")}
     <h3 data-i18n="sp.done.t"></h3>
     <div class="done-m"><span id="spDoneN"></span> · <span id="spDoneM"></span></div>
     <p class="done-msg" id="spDoneMsg"></p>
     <button class="big-btn" id="spDoneBack" data-i18n="sp.done.save"></button>
    </div>
   </div>

   <div class="sp-screen" data-sp="progress">
    <h3 class="sub-h" data-i18n="sp.pr.t"></h3>
    <div class="stat-row">
     <div class="stat-box"><div class="v" id="spPrWeek">0</div><div class="k" data-i18n="sp.week"></div></div>
     <div class="stat-box"><div class="v" id="spPrMonth">0</div><div class="k" data-i18n="sp.month"></div></div>
     <div class="stat-box"><div class="v" id="spPrStreak">0</div><div class="k" data-i18n="sp.streak"></div></div>
    </div>
    <h4 class="mini-h" data-i18n="sp.pr.board"></h4>
    <div class="wk-board" id="spBoard"></div>
    <h4 class="mini-h" data-i18n="sp.pr.hist"></h4>
    <div class="hist" id="spHist"></div>
    <button class="btn btn-quiet" id="spPrBack">{i("chevron","flip")}<span data-i18n="m.back"></span></button>
   </div>
  </div>

  <div class="mini-view" data-mini="skin" id="miniSkin">
   <div class="mini-top">
    <button class="btn btn-ghost btn-sm" data-mini-back>{i("chevron","flip")}<span data-i18n="m.back"></span></button>
    <h2 data-i18n="sn.t"></h2>
   </div>

   <div class="sn-screen on" data-sn="setup">
    <h3 class="sub-h" data-i18n="sn.setup.t"></h3>
    <p class="psub" data-i18n="sn.setup.s"></p>
    <div id="snSetup"></div>
    <button class="big-btn" id="snBuild">{i("sparkles")}<span data-i18n="sn.build"></span></button>
    <p class="hint">{i("shield")}<span data-i18n="sn.note"></span></p>
   </div>

   <div class="sn-screen" data-sn="routine">
    <div class="stat-row">
     <div class="stat-box"><div class="v" id="snStreak">0</div><div class="k" data-i18n="sp.streak"></div></div>
     <div class="stat-box"><div class="v numf" id="snWeek">0/7</div><div class="k" data-i18n="sn.week"></div></div>
    </div>
    <div class="do-row">
     <button class="do-btn" id="snDoAm"></button>
     <button class="do-btn" id="snDoPm"></button>
    </div>
    <h4 class="mini-h">{i("sun")}<span data-i18n="sn.am"></span></h4>
    <div class="sn-list" id="snAm"></div>
    <h4 class="mini-h">{i("moon")}<span data-i18n="sn.pm"></span></h4>
    <div class="sn-list" id="snPm"></div>
    <h4 class="mini-h" data-i18n="sp.pr.board"></h4>
    <div class="wk-board" id="snBoard"></div>
    <h4 class="mini-h" data-i18n="sn.hist"></h4>
    <div class="hist" id="snHist"></div>
    <p class="hint">{i("shield")}<span data-i18n="sn.gentle"></span></p>
    <button class="btn btn-quiet" id="snRedo">{i("refresh")}<span data-i18n="sn.redo"></span></button>
   </div>
  </div>

  <div class="mini-view" data-mini="fridge" id="miniFridge">
   <div class="mini-top">
    <button class="btn btn-ghost btn-sm" data-mini-back>{i("chevron","flip")}<span data-i18n="m.back"></span></button>
    <h2 data-i18n="fr.t"></h2>
   </div>

   <div class="fr-screen on" data-fr="entry">
    <p class="psub" data-i18n="fr.s"></p>
    <div class="entry-row">
     <button class="entry-btn" id="frPhotoBtn">{i("camera")}<span data-i18n="fr.photo"></span></button>
     <button class="entry-btn" id="frManual">{i("plus")}<span data-i18n="fr.manual"></span></button>
    </div>
    <p class="hint">{i("shield")}<span data-i18n="fr.photo.note"></span></p>
   </div>

   <div class="fr-screen" data-fr="pantry">
    <div id="frPhotoWrap" style="display:none">
     <img class="fr-photo" id="frPhoto" alt="">
     <button class="btn btn-quiet btn-sm" id="frPhotoRm">{i("x")}<span data-i18n="fr.photo.rm"></span></button>
    </div>
    <h4 class="mini-h" data-i18n="fr.pantry"></h4>
    <div id="frGroups"></div>
    <div class="chips" id="frCustom"></div>
    <div class="addrow">
     <input type="text" id="frAdd" data-i18n-ph="fr.custom.ph" data-i18n-title="fr.custom.ph">
     <button class="btn btn-ghost" id="frAddBtn" data-i18n-title="c.add">{i("plus")}</button>
    </div>
    <div class="fr-bar">
     <span id="frCount"></span>
     <button class="btn btn-quiet btn-sm" id="frClear" data-i18n="fr.clear"></button>
    </div>
    <button class="big-btn" id="frFind">{i("chef")}<span data-i18n="fr.find"></span></button>
    <p class="hint">{i("shield")}<span data-i18n="fr.note"></span></p>
   </div>

   <div class="fr-screen" data-fr="ideas">
    <div class="fr-tabs">
     <button class="fr-tab on" data-fr-tab="ideas" data-i18n="fr.tab.ideas"></button>
     <button class="fr-tab" data-fr-tab="favs" data-i18n="fr.tab.favs"></button>
     <button class="fr-tab" data-fr-tab="hist" data-i18n="fr.tab.hist"></button>
    </div>
    <div id="frOut"></div>
    <button class="btn btn-ghost btn-block" id="frAnother">{i("refresh")}<span data-i18n="fr.another"></span></button>
    <button class="btn btn-quiet" id="frIdeasBack">{i("chevron","flip")}<span data-i18n="m.back"></span></button>
   </div>

   <div class="sug">
    <h4 class="mini-h">{i("chef")}<span data-i18n="fs.t"></span></h4>
    <p class="psub" data-i18n="fs.s"></p>
    <div class="sug-filters" id="frSugFilters">
     <button class="sug-f on" data-sug-f="all" data-i18n="fs.all"></button>
     <button class="sug-f" data-sug-f="breakfast" data-i18n="fs.breakfast"></button>
     <button class="sug-f" data-sug-f="meal" data-i18n="fs.meal"></button>
     <button class="sug-f" data-sug-f="snack" data-i18n="fs.snack"></button>
     <button class="sug-f" data-sug-f="quick" data-i18n="fs.quick"></button>
    </div>
    <div id="frSugOut"></div>
    <button class="btn btn-ghost btn-block" id="frSugMore">{i("plus")}<span data-i18n="fs.more"></span></button>
   </div>

   <input type="file" accept="image/*" class="hidden-file" id="frFile">
  </div>
 </div>

 <footer data-i18n="l.footer"></footer>
</div></div>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="modal-bg" id="camModal"><div class="modal" role="dialog" aria-modal="true">
 <h3 data-i18n="cam.t"></h3><p id="camTN"></p>
 <video class="cam-v" id="camV" autoplay playsinline muted></video>
 <img class="cam-p" id="camP" alt="">
 <input type="file" accept="image/*" capture="environment" class="hidden-file" id="camF">
 <div class="modal-btns" id="camBtns"></div>
</div></div>

<div class="modal-bg" id="payModal"><div class="modal" role="dialog" aria-modal="true">
 <h3 data-i18n="pay.soon.t"></h3><p id="paySoonBody"></p>
 <div class="modal-btns"><button class="btn btn-primary" id="paySoonOk" data-i18n="pay.soon.ok"></button></div>
</div></div>'''

    return f'<div class="langbar">{L}</div>{landing}{onb}{app}'
