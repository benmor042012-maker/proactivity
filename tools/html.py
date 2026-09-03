# -*- coding: utf-8 -*-
"""HTML body. LOGO is substituted at build time.
data-i18n sets textContent, data-i18n-html sets innerHTML, data-i18n-ph sets placeholder."""

def i(name, cls=''):
    c = ('ic ' + cls).strip()
    return f'<svg class="{c}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def benefit(n, key):
    return f'<div class="ben">{i(n)}<span data-i18n="{key}"></span></div>'


def step_block(num, tkey, dkey):
    return (f'<div class="stp"><div class="num">{num}</div><div>'
            f'<h3 data-i18n="l.how.{num}.t"></h3><p data-i18n="l.how.{num}.d"></p></div></div>')


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


def opt(group, attr, val, icon, key):
    return (f'<div class="opt" data-{attr}="{val}">{i(icon)}'
            f'<span data-i18n="{key}"></span></div>')


def nav(last=False, finish_id=None):
    back = f'<button class="btn btn-ghost" data-back>{i("chevron","flip")}<span data-i18n="c.back"></span></button>'
    if finish_id:
        fwd = f'<button class="btn btn-primary" id="{finish_id}"><span data-i18n="o.8.finish"></span>{i("arrow")}</button>'
    else:
        fwd = f'<button class="btn btn-primary" data-next><span data-i18n="c.next"></span>{i("arrow")}</button>'
    return f'<div class="nav">{"" if last else back}{fwd}</div>'


LANGS = [('he', 'עברית'), ('en', 'English'), ('fr', 'Français'), ('ru', 'Русский'), ('ar', 'العربية')]


def build_body(logo):
    L = ''.join(f'<button class="langbtn" data-lang="{c}">{n}</button>' for c, n in LANGS)

    # ---------- landing ----------
    landing = f'''
<div class="landing" id="landing">
 <div class="wrap">

  <section class="hero">
   <div class="kicker">{i("sparkles")}<span data-i18n="l.kicker"></span></div>
   <h1><span data-i18n="l.hero.a"></span><br><span class="dim" data-i18n="l.hero.b"></span></h1>
   <p class="lead" data-i18n="l.hero.sub"></p>
   <div class="cta-row">
    <button class="btn btn-primary" id="ctaTop"><span data-i18n="l.hero.cta"></span>{i("arrow")}</button>
    <a class="btn btn-ghost" href="#how"><span data-i18n="l.hero.cta2"></span></a>
   </div>
   <p class="fineprint" data-i18n="l.hero.note"></p>
  </section>

  <div class="proof">
   <div><div class="n" data-i18n="l.pf1.n"></div><div class="l" data-i18n="l.pf1.t"></div></div>
   <div><div class="n" data-i18n="l.pf2.n"></div><div class="l" data-i18n="l.pf2.t"></div></div>
   <div><div class="n" data-i18n="l.pf3.n"></div><div class="l" data-i18n="l.pf3.t"></div></div>
  </div>

  <section class="blk">
   <h2 data-i18n="l.what.t"></h2>
   <p class="lede" data-i18n="l.what.b"></p>
  </section>

  <section class="blk">
   <h2 data-i18n="l.why.t"></h2>
   <div class="bengrid">
    {benefit("target","l.why.1")}{benefit("rocket","l.why.2")}{benefit("refresh","l.why.3")}
    {benefit("users","l.why.4")}{benefit("book","l.why.5")}{benefit("activity","l.why.6")}
    {benefit("clock","l.why.7")}{benefit("compass","l.why.8")}
   </div>
  </section>

  <section class="blk" id="how">
   <h2 data-i18n="l.how.t"></h2>
   <div class="steps">{step_block(1,0,0)}{step_block(2,0,0)}{step_block(3,0,0)}</div>
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
   <h2 data-i18n="l.fin.t"></h2>
   <p data-i18n="l.fin.sub"></p>
   <button class="btn btn-primary" id="ctaBottom"><span data-i18n="l.hero.cta"></span>{i("arrow")}</button>
  </section>

  <footer data-i18n="l.footer"></footer>
 </div>
</div>
<div class="sticky-cta" id="stickyCta">
 <button class="btn btn-primary btn-block" id="ctaSticky"><span data-i18n="l.hero.cta"></span>{i("arrow")}</button>
</div>'''

    # ---------- onboarding ----------
    ages = ''.join(f'<option value="{a}">{a}</option>' for a in range(12, 19)) + '<option value="19">19+</option>'

    onb = f'''
<div class="onb" id="onboarding"><div class="onb-inner">
 <div class="onb-top">
  <div class="mark"><img src="{logo}" alt=""><span data-i18n="b.name"></span></div>
  <div class="count" id="stepCount"></div>
 </div>
 <div class="bar"><i id="onbBar" style="width:11%"></i></div>

 <div class="step on" data-step="1">
  <h2 data-i18n="o.1.t"></h2><p class="sub" data-i18n="o.1.s"></p>
  <div class="field"><label data-i18n="o.name"></label><input type="text" id="oName" data-i18n-ph="o.name.ph"></div>
  <div class="field"><label data-i18n="o.age"></label>
   <select id="oAge"><option value="" data-i18n="o.age.ph"></option>{ages}</select></div>
  <div class="field"><label data-i18n="o.email"></label><input type="email" id="oEmail" placeholder="you@email.com"></div>
  <div class="note">{i("flame")}<span data-i18n="o.trial"></span></div>
  {nav(last=True)}
 </div>

 <div class="step" data-step="2">
  <h2 data-i18n="o.2.t"></h2><p class="sub" data-i18n="o.2.s"></p>
  <div class="opts" id="oGoals"></div>
  <div class="field" style="margin-top:var(--s5)"><label data-i18n="o.2.custom"></label>
   <div class="addrow"><input type="text" id="oCustom" data-i18n-ph="o.2.custom.ph">
   <button class="btn btn-ghost" id="addCustom">{i("plus")}</button></div></div>
  {nav()}
 </div>

 <div class="step" data-step="3">
  <h2 data-i18n="o.3.t"></h2>
  <div class="qlabel" data-i18n="o.3.easy"></div><div class="chips" id="easyC"></div>
  <div class="qlabel" data-i18n="o.3.hard"></div><div class="chips" id="hardC"></div>
  {nav()}
 </div>

 <div class="step" data-step="4">
  <h2 data-i18n="o.4.t"></h2>
  <div class="opts" id="oTime">
   {opt("time","time","15","zap","o.time.15")}{opt("time","time","30","flame","o.time.30")}{opt("time","time","45","gem","o.time.45")}
  </div>
  <div class="qlabel" data-i18n="o.4.pref"></div>
  <div class="opts" id="oAP">
   {opt("ap","ap","short","clock","o.ap.short")}{opt("ap","ap","long","book","o.ap.long")}{opt("ap","ap","mix","refresh","o.ap.mix")}
  </div>
  {nav()}
 </div>

 <div class="step" data-step="5">
  <h2 data-i18n="o.5.t"></h2>
  <div class="qlabel" data-i18n="o.5.goal"></div>
  <div class="opts" id="oWO">
   {opt("wo","wo","strength","activity","wo.strength")}{opt("wo","wo","cardio","trending","wo.cardio")}
   {opt("wo","wo","flex","seedling","wo.flex")}{opt("wo","wo","general","sparkles","wo.general")}
  </div>
  <div class="qlabel" data-i18n="o.5.exp"></div>
  <div class="opts" id="oFL">
   {opt("fl","fl","beginner","seedling","fl.beginner")}{opt("fl","fl","basic","flame","fl.basic")}{opt("fl","fl","inter","gem","fl.inter")}
  </div>
  {nav()}
 </div>

 <div class="step" data-step="6">
  <h2 data-i18n="o.6.t"></h2>
  <div class="qlabel" data-i18n="o.6.skin"></div>
  <div class="opts" id="oSkin">
   {opt("skin","skin","normal","user","sk.type.normal")}{opt("skin","skin","oily","drop","sk.type.oily")}
   {opt("skin","skin","dry","sun","sk.type.dry")}{opt("skin","skin","combo","refresh","sk.type.combo")}
   {opt("skin","skin","dunno","compass","sk.type.dunno")}
  </div>
  {nav()}
 </div>

 <div class="step" data-step="7">
  <h2 data-i18n="o.7.t"></h2><p class="sub" data-i18n="o.7.s"></p>
  <div class="opts" id="oDiff">
   {opt("diff","diff","easy","seedling","fl.beginner")}{opt("diff","diff","mid","flame","fl.basic")}{opt("diff","diff","hard","gem","fl.inter")}
  </div>
  {nav()}
 </div>

 <div class="step" data-step="8">
  <h2 data-i18n="o.8.t"></h2>
  <div class="field"><label data-i18n="o.8.dream"></label><input type="text" id="oDream" data-i18n-ph="o.8.dream.ph"></div>
  <div class="qlabel" data-i18n="o.8.goals"></div>
  <div class="field"><input type="text" id="oG1" data-i18n-ph="o.8.g1.ph"></div>
  <div class="field"><input type="text" id="oG2" data-i18n-ph="o.8.g2.ph"></div>
  <div class="field"><input type="text" id="oG3" data-i18n-ph="o.8.g3.ph"></div>
  {nav(finish_id="oFinish")}
 </div>

 <div class="step" data-step="9">
  <h2 data-i18n="o.9.t"></h2><p class="sub" data-i18n="o.9.s"></p>
  <div class="built" id="builtList"></div>
  <div class="plans">{plan_card("monthly")}{plan_card("annual", True)}</div>
  <p class="trust" data-i18n="l.pr.trust"></p>
  <div class="nav" style="flex-direction:column;gap:var(--s2)">
   <button class="btn btn-ghost btn-block" id="skipPay" data-i18n="o.9.later"></button>
   <p class="trust" style="margin:0" data-i18n="o.9.laternote"></p>
  </div>
 </div>
</div></div>'''

    # ---------- app ----------
    app = f'''
<div id="app"><div class="wrap">
 <div class="trialbar" id="trialBar">
  {i("flame")}<span id="trialTxt"></span>
  <button id="trialCta" data-i18n="trial.cta"></button>
 </div>

 <header class="apphead">
  <div class="who"><img src="{logo}" alt="">
   <div><h1 id="greetName"></h1><p class="quote" id="proQuote"></p><p class="date" id="dateStr"></p></div>
  </div>
  <div class="lvl">
   <div class="row">
    <span class="lab"><span data-i18n="a.level"></span><span class="num" id="lvl">1</span></span>
    <span class="stage" id="stg"></span>
   </div>
   <div class="xp"><i id="xpF" style="width:0%"></i></div>
  </div>
 </header>

 <nav class="tabs">
  <button class="tab on" data-page="home">{i("home")}<span data-i18n="a.tab.home"></span></button>
  <button class="tab" data-page="goals">{i("target")}<span data-i18n="a.tab.goals"></span></button>
  <button class="tab" data-page="week">{i("calendar")}<span data-i18n="a.tab.week"></span></button>
  <button class="tab" data-page="body">{i("activity")}<span data-i18n="a.tab.body"></span></button>
  <button class="tab" data-page="why">{i("brain")}<span data-i18n="a.tab.why"></span></button>
 </nav>

 <div class="page on" id="page-home">
  <div id="dIns"></div>
  <div class="ringbox">
   <div class="ringwrap"><svg viewBox="0 0 132 132" id="rSvg"></svg>
    <div class="ringmid"><div class="pct" id="rPct">0%</div><div class="cap" data-i18n="h.done"></div></div></div>
   <div class="ringtxt">
    <h2 data-i18n="h.ring.t"></h2><p data-i18n="h.ring.s"></p>
    <div class="stats">
     <div class="stat"><div class="v">{i("flame")}<span id="skV">0</span></div><div class="k" data-i18n="h.streak"></div></div>
     <div class="stat"><div class="v">{i("star")}<span id="ptV">0</span></div><div class="k" data-i18n="h.points"></div></div>
     <div class="stat"><div class="v">{i("check")}<span class="numf"><span id="dnV">0</span>/<span id="tlV">0</span></span></div><div class="k" data-i18n="h.tasks"></div></div>
    </div>
   </div>
  </div>
  <div class="chal">
   <div><div class="lab" data-i18n="h.ch.label"></div><div class="txt" id="chTxt"></div></div>
   <button class="btn btn-primary btn-sm" id="chBtn">{i("check")}<span data-i18n="h.ch.btn"></span></button>
  </div>
  <div class="catgrid" id="catGrid"></div>
 </div>

 <div class="page" id="page-goals">
  <h2 class="ptitle" data-i18n="g.t"></h2><p class="psub" data-i18n="g.s"></p>
  <div id="goalsCont"></div>
  <div class="newrow"><input type="text" id="nGoalIn" data-i18n-ph="g.new.ph">
   <button class="btn btn-primary" id="aGoalBtn">{i("plus")}<span data-i18n="c.add"></span></button></div>
 </div>

 <div class="page" id="page-week">
  <h2 class="ptitle" data-i18n="w.t"></h2><p class="psub" data-i18n="w.s"></p>
  <div class="wkbar">
   <div><span data-i18n="w.met"></span> <span class="numf"><b id="wMet">0</b>/<span id="wTot">0</span></span></div>
   <button class="btn btn-ghost btn-sm" id="rWkBtn">{i("refresh")}<span data-i18n="w.reset"></span></button>
  </div>
  <div class="scroller"><table class="grid"><thead><tr id="wHead"></tr></thead><tbody id="wBody"></tbody></table></div>
  <div class="addrow" style="margin-top:var(--s3)">
   <input type="text" id="nMis" data-i18n-ph="w.new.ph">
   <select id="nMisCat" style="max-width:150px"></select>
   <input type="number" id="nMisT" min="1" max="7" value="3">
   <button class="btn btn-primary" id="aMisBtn">{i("plus")}</button>
  </div>
  <div class="review">
   <h3 data-i18n="w.rev.t"></h3><p data-i18n="w.rev.s"></p>
   <button class="btn btn-ghost btn-sm" id="rvBtn">{i("flag")}<span data-i18n="w.rev.btn"></span></button>
   <div class="rvout" id="rvRes"></div>
  </div>
 </div>

 <div class="page wide" id="page-body">

  <div class="mini-view on" data-mini="hub">
   <h2 class="ptitle" data-i18n="m.hub.t"></h2><p class="psub" data-i18n="m.hub.s"></p>
   <div class="mini-hub" id="hubGrid"></div>
   <h2 class="ptitle sechead" data-i18n="bd.hy.t"></h2><p class="psub" data-i18n="bd.hy.s"></p>
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
     <input type="text" id="frAdd" data-i18n-ph="fr.custom.ph">
     <button class="btn btn-ghost" id="frAddBtn">{i("plus")}</button>
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

 <div class="page" id="page-why">
  <h2 class="ptitle" data-i18n="y.t"></h2><p class="psub" data-i18n="y.s"></p>
  <div class="thgrid" id="thGrid"></div>
 </div>

 <footer data-i18n="l.footer"></footer>
</div></div>

<div class="toast" id="toast"></div>

<div class="modal-bg" id="camModal"><div class="modal">
 <h3 data-i18n="cam.t"></h3><p id="camTN"></p>
 <video class="cam-v" id="camV" autoplay playsinline muted></video>
 <img class="cam-p" id="camP" alt="">
 <input type="file" accept="image/*" capture="environment" class="hidden-file" id="camF">
 <div class="modal-btns" id="camBtns"></div>
</div></div>

<div class="modal-bg" id="payModal"><div class="modal">
 <h3 data-i18n="pay.soon.t"></h3><p id="paySoonBody"></p>
 <div class="modal-btns"><button class="btn btn-primary" id="paySoonOk" data-i18n="pay.soon.ok"></button></div>
</div></div>'''

    return f'<div class="langbar">{L}</div>{landing}{onb}{app}'
