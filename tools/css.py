# -*- coding: utf-8 -*-
CSS = r"""
/* ============ TOKENS ============ */
:root{
  /* surfaces: true black, no navy tint */
  --ink-0:#09090A; --ink-1:#121214; --ink-2:#1C1C20; --ink-3:#2A2A30; --ink-4:#3A3A42;
  /* text */
  --fg:#FAFAFA; --fg-2:#A1A1AA; --fg-3:#85858F;
  /* single accent */
  --flame:#FF5A1F; --flame-hi:#FF7A47; --flame-dim:rgba(255,90,31,.14); --on-flame:#0A0A0B;
  --ok:#4ADE80;
  /* spacing scale */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px; --s8:64px;
  /* radius: two + pill */
  --r-ctl:8px; --r-card:16px; --r-pill:999px;
  /* type scale */
  --t-display:clamp(38px,8.5vw,68px); --t-h1:clamp(26px,4.5vw,34px); --t-h2:22px;
  --t-h3:16px; --t-body:15px; --t-sm:13px; --t-xs:11px;
  /* families: browser picks per script -> Heebo(he/latin) Inter(cyrillic) Noto(arabic) */
  --f-display:'Secular One','Archivo Black','Noto Sans Arabic','Heebo',sans-serif;
  --f-ui:'Heebo','Inter','Noto Sans Arabic',system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;}
body{background:var(--ink-0);color:var(--fg);font-family:var(--f-ui);font-size:var(--t-body);
  line-height:1.55;min-height:100vh;-webkit-font-smoothing:antialiased;}
h1,h2,h3,.display{font-family:var(--f-display);font-weight:400;line-height:1.08;letter-spacing:-.02em;}
::selection{background:var(--flame);color:var(--on-flame);}
:focus-visible{outline:2px solid var(--flame);outline-offset:2px;}
.wrap{max-width:1080px;margin:0 auto;padding:0 var(--s4);}
.narrow{max-width:720px;}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;}
svg.ic{width:1.25em;height:1.25em;flex:none;vertical-align:-.22em;}
[dir=rtl] .flip{transform:scaleX(-1);}
[dir=rtl] .tmr svg{transform:scaleX(-1);}
/* numeric fractions must not be reordered by the bidi algorithm in he/ar */
.numf{direction:ltr;unicode-bidi:isolate;display:inline-block;}

/* ============ BUTTONS ============ */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--s2);
  min-height:44px;padding:0 var(--s5);border:0;border-radius:var(--r-pill);
  font-family:var(--f-ui);font-weight:700;font-size:var(--t-sm);letter-spacing:.01em;
  cursor:pointer;transition:background .14s,color .14s,border-color .14s,transform .08s;
  text-decoration:none;white-space:nowrap;}
.btn:active{transform:scale(.975);}
.btn-primary{background:var(--flame);color:var(--on-flame);}
.btn-primary:hover{background:var(--flame-hi);}
.btn-primary:disabled{background:var(--ink-3);color:var(--fg-3);cursor:default;transform:none;}
.btn-ghost{background:transparent;color:var(--fg);border:1px solid var(--ink-3);}
.btn-ghost:hover{border-color:var(--ink-4);background:var(--ink-1);}
.btn-quiet{background:transparent;color:var(--fg-2);padding:0 var(--s3);}
.btn-quiet:hover{color:var(--fg);}
.btn-sm{min-height:34px;padding:0 var(--s4);font-size:var(--t-xs);}
.btn-block{width:100%;}
.icon-btn{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;
  border:0;background:transparent;color:var(--fg-3);border-radius:var(--r-ctl);cursor:pointer;flex:none;}
.icon-btn:hover{color:var(--flame);background:var(--ink-2);}

/* ============ FIELDS ============ */
input[type=text],input[type=email],input[type=number],select,textarea{
  width:100%;background:var(--ink-2);border:1px solid var(--ink-3);border-radius:var(--r-ctl);
  color:var(--fg);padding:11px var(--s3);font-size:var(--t-body);font-family:var(--f-ui);
  min-height:44px;transition:border-color .14s;}
input:focus,select:focus,textarea:focus{border-color:var(--flame);outline:none;}
::placeholder{color:var(--fg-3);}
select{appearance:none;padding-inline-end:var(--s6);background-repeat:no-repeat;background-size:14px;
  background-position:calc(100% - 14px) center;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2385858F' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");}
[dir=rtl] select{background-position:14px center;}
select option{background:var(--ink-2);color:var(--fg);}
.field{margin-bottom:var(--s3);}
.field>label{display:block;font-size:var(--t-sm);font-weight:600;color:var(--fg-2);margin-bottom:var(--s2);}

/* ============ LANG BAR ============ */
.langbar{position:fixed;inset-block-start:0;inset-inline:0;z-index:300;height:40px;
  background:rgba(9,9,10,.86);backdrop-filter:blur(12px);border-bottom:1px solid var(--ink-2);
  display:flex;align-items:center;justify-content:center;gap:var(--s1);padding:0 var(--s3);}
.langbtn{background:none;border:0;color:var(--fg-3);font-family:var(--f-ui);font-size:var(--t-xs);
  font-weight:600;padding:6px 10px;border-radius:var(--r-pill);cursor:pointer;}
.langbtn:hover{color:var(--fg-2);}
.langbtn.on{color:var(--on-flame);background:var(--flame);}

/* ============ LANDING ============ */
.landing{padding-block-start:40px;}
.hero{padding:var(--s8) 0 var(--s7);}
.kicker{display:inline-flex;align-items:center;gap:var(--s2);font-size:var(--t-xs);font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--flame);margin-bottom:var(--s4);}
.hero h1{font-size:var(--t-display);margin-bottom:var(--s4);max-width:14ch;}
.hero h1 .dim{color:var(--fg-3);}
.hero p.lead{font-size:clamp(15px,2.2vw,19px);color:var(--fg-2);max-width:48ch;margin-bottom:var(--s5);}
.hero .cta-row{display:flex;gap:var(--s3);flex-wrap:wrap;align-items:center;}
.hero .fineprint{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s4);}
.proof{display:flex;gap:var(--s7);flex-wrap:wrap;border-block:1px solid var(--ink-2);padding:var(--s5) 0;}
.proof .n{font-family:var(--f-display);font-size:34px;color:var(--flame);line-height:1;}
.proof .l{font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s1);}
section.blk{padding:var(--s7) 0;}
section.blk>h2{font-size:var(--t-h1);margin-bottom:var(--s5);max-width:18ch;}
.lede{font-size:clamp(16px,2.4vw,21px);color:var(--fg-2);max-width:56ch;line-height:1.6;}
.lede b{color:var(--fg);font-weight:600;}
.bengrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1px;background:var(--ink-2);
  border:1px solid var(--ink-2);border-radius:var(--r-card);overflow:hidden;}
.ben{background:var(--ink-0);padding:var(--s4);display:flex;gap:var(--s3);align-items:flex-start;font-size:var(--t-sm);}
.ben svg{color:var(--flame);margin-top:1px;}
.steps{display:grid;gap:var(--s5);}
.stp{display:grid;grid-template-columns:auto 1fr;gap:var(--s4);align-items:start;}
.stp .num{font-family:var(--f-display);font-size:44px;line-height:.9;color:var(--ink-3);width:1.6em;}
.stp h3{font-size:var(--t-h2);margin-bottom:var(--s2);}
.stp p{color:var(--fg-2);max-width:52ch;}

/* pricing */
.plans{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:var(--s3);}
.plan{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);display:flex;flex-direction:column;
  border:1px solid transparent;}
.plan.feature{border-color:var(--flame);}
.plan .tag{align-self:flex-start;display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--flame);background:var(--flame-dim);
  padding:4px 10px;border-radius:var(--r-pill);margin-bottom:var(--s3);}
.plan .tag .dot{width:3px;height:3px;border-radius:50%;background:currentColor;opacity:.6;}
.plan:not(.feature) .amt{color:var(--fg-2);}
.plan h3{font-size:var(--t-h3);font-family:var(--f-ui);font-weight:700;letter-spacing:0;color:var(--fg-2);margin-bottom:var(--s2);}
.plan .price{display:flex;align-items:baseline;gap:var(--s2);margin-bottom:var(--s1);}
.plan .amt{font-family:var(--f-display);font-size:46px;line-height:1;}
.plan .per{font-size:var(--t-sm);color:var(--fg-3);}
.plan .bill{font-size:var(--t-xs);color:var(--fg-3);margin-bottom:var(--s4);}
.plan ul{list-style:none;display:grid;gap:var(--s2);margin-bottom:var(--s5);}
.plan li{display:flex;gap:var(--s2);font-size:var(--t-sm);color:var(--fg-2);align-items:flex-start;}
.plan li svg{color:var(--flame);margin-top:2px;}
.plan .btn{margin-top:auto;}
.trust{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s4);text-align:center;}

/* faq */
.faq{border-top:1px solid var(--ink-2);}
.faq details{border-bottom:1px solid var(--ink-2);}
.faq summary{list-style:none;cursor:pointer;padding:var(--s4) 0;font-weight:600;
  display:flex;justify-content:space-between;align-items:center;gap:var(--s4);}
.faq summary::-webkit-details-marker{display:none;}
.faq summary svg{color:var(--fg-3);transition:transform .18s;flex:none;transform:rotate(90deg);}
.faq details[open] summary svg{transform:rotate(-90deg);color:var(--flame);}
.faq p{color:var(--fg-2);font-size:var(--t-sm);padding-bottom:var(--s4);max-width:64ch;}
.finale{text-align:center;padding:var(--s8) 0;border-top:1px solid var(--ink-2);}
.finale h2{font-size:var(--t-h1);margin-bottom:var(--s2);}
.finale p{color:var(--fg-2);margin-bottom:var(--s5);}
footer{text-align:center;color:var(--fg-3);font-size:var(--t-xs);padding:var(--s5) 0 var(--s7);border-top:1px solid var(--ink-2);}
.sticky-cta{position:fixed;inset-block-end:0;inset-inline:0;z-index:120;display:none;
  padding:var(--s3) var(--s4) calc(var(--s3) + env(safe-area-inset-bottom));
  background:rgba(9,9,10,.94);backdrop-filter:blur(12px);border-top:1px solid var(--ink-2);}

/* ============ ONBOARDING ============ */
.onb{display:none;position:fixed;inset:0;z-index:200;background:var(--ink-0);overflow-y:auto;
  padding:56px var(--s4) var(--s7);}
.onb-inner{max-width:560px;margin:0 auto;}
.onb-top{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);margin-bottom:var(--s3);}
.onb-top .mark{display:flex;align-items:center;gap:var(--s2);font-weight:700;font-size:var(--t-sm);}
.onb-top .mark img{width:28px;height:28px;border-radius:7px;}
.onb-top .count{font-size:var(--t-xs);color:var(--fg-3);}
.bar{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;margin-bottom:var(--s6);}
.bar>i{display:block;height:100%;background:var(--flame);border-radius:var(--r-pill);transition:width .3s ease;}
.step{display:none;}
.step.on{display:block;animation:rise .28s ease both;}
@keyframes rise{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
.step>h2{font-size:var(--t-h1);margin-bottom:var(--s2);}
.step>p.sub{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s5);}
.qlabel{font-size:var(--t-sm);font-weight:600;color:var(--fg-2);margin:var(--s5) 0 var(--s3);}
.qlabel:first-child{margin-top:0;}
.opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:var(--s2);}
.opt{background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-ctl);padding:var(--s3) var(--s2);
  text-align:center;cursor:pointer;font-size:var(--t-sm);font-weight:600;user-select:none;
  transition:border-color .12s,background .12s,color .12s;display:flex;flex-direction:column;align-items:center;gap:var(--s2);
  min-height:74px;justify-content:center;}
.opt svg{color:var(--fg-3);width:20px;height:20px;transition:color .12s;}
.opt:hover{border-color:var(--ink-4);}
.opt.on{border-color:var(--flame);background:var(--flame-dim);color:var(--fg);}
.opt.on svg{color:var(--flame);}
.chips{display:flex;flex-wrap:wrap;gap:var(--s2);}
.chip{background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-pill);padding:8px 14px;
  font-size:var(--t-sm);cursor:pointer;user-select:none;transition:border-color .12s,background .12s;}
.chip:hover{border-color:var(--ink-4);}
.chip.on{border-color:var(--flame);background:var(--flame-dim);color:var(--flame);}
.nav{display:flex;gap:var(--s2);margin-top:var(--s6);}
.nav .btn-primary{flex:1;}
.note{background:var(--ink-1);border-inline-start:2px solid var(--flame);border-radius:var(--r-ctl);
  padding:var(--s3) var(--s4);font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s4);
  display:flex;gap:var(--s2);align-items:center;}
.note svg{color:var(--flame);}
.built{display:grid;gap:var(--s2);margin-bottom:var(--s5);}
.built div{display:flex;gap:var(--s2);align-items:center;font-size:var(--t-sm);color:var(--fg-2);}
.built svg{color:var(--flame);}

/* ============ APP ============ */
#app{display:none;padding-block:40px var(--s8);}
.trialbar{display:none;align-items:center;justify-content:center;gap:var(--s3);flex-wrap:wrap;
  background:var(--flame-dim);border-radius:var(--r-pill);padding:var(--s2) var(--s4);
  font-size:var(--t-xs);color:var(--flame);font-weight:600;margin:var(--s4) 0;}
.trialbar.on{display:flex;}
.trialbar button{background:var(--flame);color:var(--on-flame);border:0;border-radius:var(--r-pill);
  padding:5px 12px;font-family:var(--f-ui);font-weight:700;font-size:var(--t-xs);cursor:pointer;}
.apphead{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);flex-wrap:wrap;
  padding:var(--s5) 0 var(--s4);}
.apphead .who{display:flex;align-items:center;gap:var(--s3);min-width:0;}
.apphead img{width:40px;height:40px;border-radius:10px;flex:none;}
.apphead h1{font-size:var(--t-h2);}
.apphead .quote{font-size:var(--t-xs);color:var(--fg-2);}
.apphead .date{font-size:var(--t-xs);color:var(--fg-3);}
.lvl{min-width:150px;}
.lvl .row{display:flex;align-items:baseline;justify-content:space-between;gap:var(--s3);margin-bottom:var(--s2);}
.lvl .lab{font-size:var(--t-xs);color:var(--fg-3);}
.lvl .num{font-family:var(--f-display);font-size:var(--t-h2);color:var(--fg);margin-inline-start:4px;}
.lvl .stage{font-size:var(--t-xs);color:var(--flame);font-weight:700;}
.xp{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;}
.xp>i{display:block;height:100%;background:var(--flame);transition:width .35s ease;}
.tabs{display:flex;gap:var(--s5);border-bottom:1px solid var(--ink-2);margin-bottom:var(--s5);
  overflow-x:auto;scrollbar-width:none;}
.tabs::-webkit-scrollbar{display:none;}
.tab{border:0;background:none;color:var(--fg-3);font-family:var(--f-ui);font-weight:700;font-size:var(--t-sm);
  padding:var(--s3) 0;cursor:pointer;white-space:nowrap;position:relative;display:inline-flex;align-items:center;gap:var(--s2);}
.tab:hover{color:var(--fg-2);}
.tab.on{color:var(--fg);}
.tab.on::after{content:"";position:absolute;inset-inline:0;inset-block-end:-1px;height:2px;background:var(--flame);}
.page{display:none;}
.page.on{display:block;animation:rise .2s ease both;}
.ptitle{font-size:var(--t-h1);margin-bottom:var(--s2);}
.psub{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s5);max-width:60ch;}
.card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);}

/* home: insight */
.insight{display:flex;gap:var(--s3);background:var(--ink-1);border-radius:var(--r-card);
  padding:var(--s4);margin-bottom:var(--s3);align-items:flex-start;}
.insight svg{color:var(--flame);flex:none;margin-top:2px;}
.insight .lab{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.insight .txt{font-size:var(--t-sm);margin-top:2px;}
.insight .src{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s1);}

/* home: ring */
.ringbox{display:flex;gap:var(--s5);align-items:center;flex-wrap:wrap;background:var(--ink-1);
  border-radius:var(--r-card);padding:var(--s5);margin-bottom:var(--s3);}
.ringwrap{position:relative;width:132px;height:132px;flex:none;}
.ringwrap svg{width:100%;height:100%;transform:rotate(-90deg);}
[dir=rtl] .ringwrap svg{transform:rotate(-90deg) scaleY(-1);}
.ringmid{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.ringmid .pct{font-family:var(--f-display);font-size:30px;line-height:1;}
.ringmid .cap{font-size:10px;color:var(--fg-3);letter-spacing:.08em;text-transform:uppercase;margin-top:2px;}
.ringtxt{flex:1;min-width:200px;}
.ringtxt h2{font-size:var(--t-h2);margin-bottom:var(--s2);}
.ringtxt p{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s4);max-width:44ch;}
.stats{display:flex;gap:var(--s5);flex-wrap:wrap;}
.stat .v{font-family:var(--f-display);font-size:var(--t-h2);line-height:1;display:flex;align-items:center;gap:6px;}
.stat .v svg{width:16px;height:16px;color:var(--flame);}
.stat .k{font-size:var(--t-xs);color:var(--fg-3);margin-top:2px;}

/* home: challenge */
.chal{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);flex-wrap:wrap;
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);margin-bottom:var(--s5);}
.chal .lab{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--flame);font-weight:700;}
.chal .txt{font-size:var(--t-body);font-weight:600;margin-top:2px;}
.chal .theme{font-size:var(--t-xs);color:var(--fg-3);font-weight:400;}

/* home: category cards */
.catgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:var(--s3);}
.cat{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);}
.cathead{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);
  padding-bottom:var(--s3);border-bottom:1px solid var(--ink-2);margin-bottom:var(--s2);}
.cathead .nm{display:flex;align-items:center;gap:var(--s2);font-weight:700;font-size:var(--t-h3);}
.cathead .nm svg{color:var(--fg-3);}
.cathead .ct{font-size:var(--t-xs);color:var(--fg-3);font-variant-numeric:tabular-nums;}
.cathead .ct b{color:var(--flame);}
.task{display:flex;align-items:center;gap:var(--s3);padding:var(--s2) 0;}
.task+.task{border-top:1px solid var(--ink-2);}
.cb{appearance:none;width:20px;height:20px;flex:none;border-radius:6px;border:1.5px solid var(--ink-4);
  cursor:pointer;display:grid;place-items:center;transition:background .12s,border-color .12s;}
.cb:hover{border-color:var(--flame);}
.cb:checked{background:var(--flame);border-color:var(--flame);}
.cb:checked::after{content:"";width:11px;height:6px;border-inline-start:2px solid var(--on-flame);
  border-bottom:2px solid var(--on-flame);transform:rotate(-45deg) translate(1px,-2px);}
.task .body{flex:1;min-width:0;}
.task .ttl{font-size:var(--t-body);}
.task .ttl.done{color:var(--fg-3);text-decoration:line-through;}
.task .meta{display:flex;align-items:center;gap:var(--s2);font-size:var(--t-xs);color:var(--fg-3);margin-top:2px;}
.task .meta svg{width:13px;height:13px;}
.task .thumb{width:32px;height:32px;border-radius:6px;object-fit:cover;flex:none;}
.tmr{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:26px;
  background:var(--ink-2);border:1px solid var(--ink-3);color:var(--fg-2);border-radius:var(--r-pill);
  font-size:11px;padding:0 8px;cursor:pointer;font-family:var(--f-ui);font-variant-numeric:tabular-nums;flex:none;}
.tmr:hover{border-color:var(--flame);color:var(--flame);}
.tmr svg{width:13px;height:13px;}
.tmr.run{background:var(--flame);border-color:var(--flame);color:var(--on-flame);}
.empty{font-size:var(--t-sm);color:var(--fg-3);padding:var(--s3) 0;}
.sugs{display:flex;flex-wrap:wrap;gap:var(--s1);margin:var(--s3) 0;}
.sug{background:transparent;border:1px dashed var(--ink-3);color:var(--fg-3);border-radius:var(--r-pill);
  padding:4px 10px;font-size:var(--t-xs);cursor:pointer;font-family:var(--f-ui);}
.sug:hover{border-color:var(--flame);color:var(--flame);border-style:solid;}
.addrow{display:flex;gap:var(--s2);margin-top:var(--s3);}
.addrow input[type=text]{flex:1;min-width:0;min-height:38px;font-size:var(--t-sm);}
.addrow input[type=number]{width:64px;min-height:38px;font-size:var(--t-sm);text-align:center;}
.addrow .btn{min-height:38px;padding:0 var(--s4);}

/* goals */
.goal{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);margin-bottom:var(--s3);}
.goal>h3{display:flex;align-items:center;gap:var(--s2);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-h3);letter-spacing:0;margin-bottom:var(--s3);}
.goal>h3 svg{color:var(--flame);flex:none;}
.goal>h3 .icon-btn{margin-inline-start:auto;}
.acts{display:grid;}
.acts label{display:flex;align-items:center;gap:var(--s3);padding:var(--s2) 0;cursor:pointer;font-size:var(--t-sm);}
.acts label+label{border-top:1px solid var(--ink-2);}
.acts .done{color:var(--fg-3);text-decoration:line-through;}
.gmeta{display:flex;align-items:center;justify-content:space-between;font-size:var(--t-xs);
  color:var(--fg-3);margin-top:var(--s3);font-variant-numeric:tabular-nums;}
.gbar{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;margin-top:var(--s2);}
.gbar>i{display:block;height:100%;background:var(--flame);transition:width .3s;}
.newrow{display:flex;gap:var(--s2);margin-top:var(--s4);}
.newrow input{flex:1;min-width:0;}

/* week */
.wkbar{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);flex-wrap:wrap;
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s3) var(--s4);margin-bottom:var(--s3);font-size:var(--t-sm);}
.wkbar b{font-family:var(--f-display);font-size:var(--t-h3);color:var(--flame);}
.scroller{overflow-x:auto;border-radius:var(--r-card);background:var(--ink-1);}
table.grid{border-collapse:collapse;width:100%;min-width:560px;}
table.grid th,table.grid td{padding:0;text-align:center;}
table.grid thead th{font-size:var(--t-xs);color:var(--fg-3);font-weight:600;padding:var(--s3) var(--s1);
  border-bottom:1px solid var(--ink-2);}
table.grid thead th.today{color:var(--flame);}
table.grid th.mcol,table.grid td.mcol{text-align:start;padding:var(--s2) var(--s4);min-width:180px;
  position:sticky;inset-inline-start:0;background:var(--ink-1);border-inline-end:1px solid var(--ink-2);z-index:1;}
table.grid tbody tr+tr td{border-top:1px solid var(--ink-2);}
.mrow{display:flex;align-items:center;gap:var(--s2);}
.mrow svg{color:var(--fg-3);flex:none;width:16px;height:16px;}
.mrow .mt{font-size:var(--t-sm);}
.mrow .mm{font-size:var(--t-xs);color:var(--fg-3);}
.mrow .icon-btn{margin-inline-start:auto;}
td.dcell{cursor:pointer;height:42px;transition:background .1s;}
td.dcell:hover{background:var(--ink-2);}
td.dcell .mk{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:6px;
  border:1.5px solid var(--ink-3);color:transparent;}
td.dcell.on .mk{background:var(--flame);border-color:var(--flame);color:var(--on-flame);}
td.dcell .mk svg{width:13px;height:13px;}
td.scell{font-size:var(--t-xs);font-weight:700;min-width:96px;padding-inline:var(--s3);}
td.scell.win{color:var(--flame);}
td.scell.mid{color:var(--fg-2);}
td.scell.none{color:var(--fg-3);}
.review{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);margin-top:var(--s3);text-align:center;}
.review h3{font-size:var(--t-h2);margin-bottom:var(--s2);}
.review p{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s4);}
.rvout{display:none;margin-top:var(--s4);padding-top:var(--s4);border-top:1px solid var(--ink-2);}
.rvout.on{display:block;}
.rvout .big{font-family:var(--f-display);font-size:44px;line-height:1;}
.rvout .msg{color:var(--fg-2);font-size:var(--t-sm);margin:var(--s2) 0;}
.rvout .pts{color:var(--flame);font-weight:700;}

/* body plans */
.plangrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--s3);}
.pcard{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);}
.pcard h3{font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);letter-spacing:0;
  display:flex;align-items:baseline;gap:var(--s2);}
.pcard h3 .dnum{font-size:var(--t-xs);color:var(--fg-3);font-weight:600;}
.pcard .psub2{font-size:var(--t-xs);color:var(--fg-3);margin:var(--s1) 0 var(--s3);}
.pitem{display:flex;align-items:flex-start;gap:var(--s3);padding:var(--s2) 0;font-size:var(--t-sm);}
.pitem+.pitem{border-top:1px solid var(--ink-2);}
.pitem .cb{margin-top:1px;}
.pitem .pb{flex:1;min-width:0;}
.pitem .pd{font-size:var(--t-xs);color:var(--fg-3);margin-top:1px;}
.pitem .pr{font-size:var(--t-xs);color:var(--fg-2);white-space:nowrap;font-variant-numeric:tabular-nums;
  display:flex;align-items:center;gap:4px;margin-inline-start:auto;}
.pitem .pr svg{width:13px;height:13px;color:var(--fg-3);}
.pitem .done{color:var(--fg-3);text-decoration:line-through;}
.infoline{display:flex;gap:var(--s2);align-items:center;background:var(--ink-1);border-radius:var(--r-card);
  padding:var(--s3) var(--s4);margin-bottom:var(--s3);font-size:var(--t-sm);color:var(--fg-2);}
.infoline svg{color:var(--flame);flex:none;}
.sechead{font-size:var(--t-h2);margin:var(--s7) 0 var(--s2);}
.sechead:first-child{margin-top:0;}

/* why it works */
.thgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--s3);}
.th{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);position:relative;}
.th .n{position:absolute;inset-block-start:var(--s4);inset-inline-end:var(--s4);
  font-family:var(--f-display);font-size:34px;color:var(--ink-3);line-height:1;}
.th>svg{color:var(--flame);width:22px;height:22px;margin-bottom:var(--s3);}
.th h3{font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);letter-spacing:0;padding-inline-end:var(--s6);}
.th .au{font-size:var(--t-xs);color:var(--fg-3);margin-bottom:var(--s3);}
.th .pr2{font-size:var(--t-sm);margin-bottom:var(--s2);}
.th .hw{font-size:var(--t-sm);color:var(--fg-2);margin-bottom:var(--s4);}
.th dl{border-top:1px solid var(--ink-2);padding-top:var(--s3);}
.th dt{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.th dd{font-size:var(--t-xs);color:var(--fg-2);margin-bottom:var(--s2);}

/* ============ OVERLAYS ============ */
.toast{position:fixed;inset-block-end:var(--s5);inset-inline:0;margin-inline:auto;width:max-content;max-width:88%;
  background:var(--fg);color:var(--ink-0);padding:10px 18px;border-radius:var(--r-pill);
  font-weight:700;font-size:var(--t-sm);z-index:400;opacity:0;transform:translateY(12px);
  transition:opacity .25s,transform .25s;pointer-events:none;text-align:center;}
.toast.on{opacity:1;transform:none;}
.modal-bg{position:fixed;inset:0;background:rgba(9,9,10,.88);backdrop-filter:blur(6px);
  display:none;align-items:center;justify-content:center;z-index:350;padding:var(--s4);}
.modal-bg.on{display:flex;}
.modal{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);max-width:380px;width:100%;}
.modal h3{font-size:var(--t-h2);margin-bottom:var(--s2);}
.modal p{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s4);}
.cam-v,.cam-p{width:100%;border-radius:var(--r-ctl);background:#000;aspect-ratio:4/3;object-fit:cover;margin-bottom:var(--s4);}
.cam-p{display:none;}
.modal-btns{display:flex;gap:var(--s2);flex-wrap:wrap;}
.modal-btns .btn{flex:1;}
.hidden-file{display:none;}

/* ============ RESPONSIVE ============ */
/* ============ MINI-APPS ============ */
.page.wide{max-width:1180px;margin-inline:auto;}
.mini-view{display:none;}
.mini-view.on{display:block;animation:rise .22s ease both;}
.mini-top{display:flex;align-items:center;gap:var(--s4);margin-bottom:var(--s5);}
.mini-top h2{font-size:var(--t-h1);}

.mini-hub{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:var(--s3);margin-bottom:var(--s6);}
.mini-card{display:grid;gap:var(--s2);text-align:start;background:var(--ink-1);border:1px solid transparent;
  border-radius:var(--r-card);padding:var(--s5);cursor:pointer;font-family:var(--f-ui);color:var(--fg);
  transition:border-color .14s,transform .1s;}
.mini-card:hover{border-color:var(--flame);}
.mini-card:active{transform:scale(.99);}
.mini-card .mc-ic{display:grid;place-items:center;width:48px;height:48px;border-radius:var(--r-ctl);
  background:var(--flame-dim);color:var(--flame);margin-bottom:var(--s2);}
.mini-card .mc-ic svg{width:24px;height:24px;}
.mini-card .mc-n{font-family:var(--f-display);font-size:var(--t-h2);}
.mini-card .mc-d{font-size:var(--t-sm);color:var(--fg-2);}
.mini-card .mc-s{font-size:var(--t-xs);color:var(--flame);font-weight:700;}
.mini-card .mc-go{display:flex;align-items:center;gap:var(--s2);font-size:var(--t-sm);font-weight:700;
  color:var(--fg-3);margin-top:var(--s2);}
.mini-card:hover .mc-go{color:var(--flame);}

.big-btn{display:flex;align-items:center;justify-content:center;gap:var(--s2);width:100%;min-height:56px;
  border:0;border-radius:var(--r-pill);background:var(--flame);color:var(--on-flame);
  font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);cursor:pointer;margin:var(--s4) 0;
  transition:background .14s,transform .08s;}
.big-btn:hover{background:var(--flame-hi);}
.big-btn:active{transform:scale(.985);}
.big-btn svg{width:20px;height:20px;}
.row-btns{display:flex;gap:var(--s2);flex-wrap:wrap;}
.sub-h{font-size:var(--t-h2);margin:var(--s6) 0 var(--s2);}
.mini-h{display:flex;align-items:center;gap:var(--s2);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-sm);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  margin:var(--s5) 0 var(--s3);}
.mini-h svg{width:15px;height:15px;color:var(--flame);}
.hint{display:flex;gap:var(--s2);align-items:flex-start;font-size:var(--t-sm);color:var(--fg-2);
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s3) var(--s4);margin:var(--s4) 0;}
.hint svg{color:var(--flame);flex:none;margin-top:2px;}
.hint.safe{background:transparent;padding-inline:0;}

.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:var(--s2);margin-bottom:var(--s3);}
.stat-box{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);text-align:center;}
.stat-box .v{font-family:var(--f-display);font-size:30px;line-height:1;}
.stat-box .k{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s1);}

.sp-screen,.sn-screen,.fr-screen{display:none;}
.sp-screen.on,.sn-screen.on,.fr-screen.on{display:block;animation:rise .2s ease both;}

.pick-grid{display:grid;gap:var(--s2);}
.pick-card{display:flex;align-items:center;gap:var(--s3);background:var(--ink-1);border:1px solid transparent;
  border-radius:var(--r-card);padding:var(--s4) var(--s5);cursor:pointer;font-family:var(--f-ui);
  color:var(--fg);text-align:start;min-height:64px;transition:border-color .14s;}
.pick-card:hover{border-color:var(--flame);}
.pick-card .pk-n{font-size:var(--t-h3);font-weight:700;}
.pick-card .pk-m{font-size:var(--t-xs);color:var(--fg-3);}
.pick-card svg{margin-inline-start:auto;color:var(--fg-3);}
.pick-card:hover svg{color:var(--flame);}

.dots{display:flex;gap:6px;justify-content:center;margin-bottom:var(--s4);}
.dots .dot{width:8px;height:8px;border-radius:50%;background:var(--ink-3);transition:background .2s,transform .2s;}
.dots .dot.done{background:var(--flame);}
.dots .dot.now{background:var(--flame);transform:scale(1.5);}

.ex-card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s6) var(--s5);text-align:center;
  transition:opacity .2s;}
.ex-card.resting{opacity:.35;pointer-events:none;}
.ex-card .ex-of{font-size:var(--t-xs);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.ex-card .ex-n{font-family:var(--f-display);font-size:clamp(26px,5vw,38px);margin:var(--s2) 0;}
.ex-card .ex-r{font-size:var(--t-h2);color:var(--flame);font-weight:700;font-variant-numeric:tabular-nums;}
.ex-card .ex-c{font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s3);max-width:38ch;margin-inline:auto;}

.rest{display:none;background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);text-align:center;margin-top:var(--s3);}
.rest.on{display:block;animation:rise .2s ease both;}
.rest .rest-l{font-size:var(--t-xs);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.rest .rest-n{font-family:var(--f-display);font-size:54px;line-height:1;color:var(--flame);font-variant-numeric:tabular-nums;}
.rest .rest-x{font-size:var(--t-sm);color:var(--fg-2);margin:var(--s2) 0 var(--s3);}

.done-card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s7) var(--s5);text-align:center;}
.done-card .big-check{width:44px;height:44px;color:var(--flame);margin-bottom:var(--s3);}
.done-card h3{font-size:var(--t-h1);}
.done-card .done-m{font-size:var(--t-h3);color:var(--flame);font-weight:700;margin-top:var(--s2);}
.done-card .done-msg{color:var(--fg-2);font-size:var(--t-sm);margin-top:var(--s3);}

.wk-board{display:grid;grid-template-columns:repeat(7,1fr);gap:var(--s1);}
.wk-cell{background:var(--ink-1);border-radius:var(--r-ctl);padding:var(--s2) 2px;text-align:center;min-height:56px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:var(--s1);}
.wk-cell.today{outline:1px solid var(--ink-4);}
.wk-cell.on{background:var(--flame);color:var(--on-flame);}
.wk-cell.half{background:var(--flame-dim);color:var(--flame);}
.wk-cell .wk-d{font-size:10px;opacity:.8;}
.wk-cell .wk-m{height:16px;}
.wk-cell .wk-m svg{width:16px;height:16px;}

.hist{display:grid;}
.hist-row{display:flex;align-items:baseline;gap:var(--s3);padding:var(--s3) 0;font-size:var(--t-sm);}
.hist-row+.hist-row{border-top:1px solid var(--ink-2);}
.hist-row .hr-n{font-weight:600;}
.hist-row .hr-m{color:var(--fg-2);font-size:var(--t-xs);}
.hist-row .hr-d{margin-inline-start:auto;color:var(--fg-3);font-size:var(--t-xs);font-variant-numeric:tabular-nums;}

.do-row{display:grid;grid-template-columns:1fr 1fr;gap:var(--s2);margin:var(--s4) 0;}
.do-btn{display:flex;align-items:center;justify-content:center;gap:var(--s2);min-height:60px;
  background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-card);color:var(--fg);
  font-family:var(--f-ui);font-weight:700;font-size:var(--t-sm);cursor:pointer;padding:var(--s3);
  transition:background .14s,border-color .14s,color .14s;}
.do-btn:hover{border-color:var(--flame);}
.do-btn svg{width:18px;height:18px;color:var(--fg-3);}
.do-btn.done{background:var(--flame);border-color:var(--flame);color:var(--on-flame);}
.do-btn.done svg{color:var(--on-flame);}

.sn-list{display:grid;}
.sn-step{display:flex;gap:var(--s3);padding:var(--s3) 0;}
.sn-step+.sn-step{border-top:1px solid var(--ink-2);}
.sn-step .sn-num{display:grid;place-items:center;width:26px;height:26px;flex:none;border-radius:50%;
  background:var(--ink-2);color:var(--fg-2);font-size:var(--t-xs);font-weight:700;}
.sn-step .sn-body{flex:1;min-width:0;}
.sn-step .sn-n{font-size:var(--t-body);font-weight:600;}
.sn-step .sn-d{font-size:var(--t-xs);color:var(--fg-3);margin-top:2px;}
.sn-step .sn-p{margin-top:var(--s2);min-height:38px;font-size:var(--t-sm);}

.entry-row{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3);margin:var(--s5) 0;}
.entry-btn{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:var(--s3);
  min-height:130px;background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-card);
  color:var(--fg);font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);cursor:pointer;
  padding:var(--s4);text-align:center;transition:border-color .14s;}
.entry-btn:hover{border-color:var(--flame);}
.entry-btn svg{width:28px;height:28px;color:var(--flame);}

.fr-photo{width:100%;max-height:260px;object-fit:cover;border-radius:var(--r-card);margin-bottom:var(--s2);}
.ing-group{margin-bottom:var(--s4);}
.ing-group .ing-h{font-size:var(--t-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  font-weight:700;margin-bottom:var(--s2);}
.fr-bar{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);
  font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s4);}

.fr-tabs{display:flex;gap:var(--s4);border-bottom:1px solid var(--ink-2);margin-bottom:var(--s4);}
.fr-tab{border:0;background:none;color:var(--fg-3);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-sm);padding:var(--s3) 0;cursor:pointer;position:relative;}
.fr-tab.on{color:var(--fg);}
.fr-tab.on::after{content:"";position:absolute;inset-inline:0;inset-block-end:-1px;height:2px;background:var(--flame);}

.rec{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);margin-bottom:var(--s3);}
.rec-h{display:flex;align-items:flex-start;gap:var(--s3);margin-bottom:var(--s3);}
.rec-n{font-family:var(--f-display);font-size:var(--t-h2);}
.rec-m{display:flex;align-items:center;gap:6px;font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s1);}
.rec-m svg{width:13px;height:13px;}
.rec-m b{color:var(--flame);}
.rec-h .fav{margin-inline-start:auto;}
.rec-h .fav.on{color:var(--flame);}
.rec-i{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:var(--s2);}
.rec-i .ri-h{font-size:var(--t-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  font-weight:700;margin-inline-end:var(--s1);}
.ri{display:inline-flex;align-items:center;gap:4px;font-size:var(--t-xs);border-radius:var(--r-pill);padding:3px 10px;}
.ri.ok{background:var(--flame-dim);color:var(--flame);}
.ri.ok svg{width:12px;height:12px;}
.ri.no{background:var(--ink-2);color:var(--fg-3);}
.rec-s{border-top:1px solid var(--ink-2);padding-top:var(--s3);margin-top:var(--s3);}
.rec-s .rs-h{font-size:var(--t-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  font-weight:700;margin-bottom:var(--s2);}
.rec-s ol{padding-inline-start:1.2em;display:grid;gap:var(--s2);}
.rec-s li{font-size:var(--t-sm);color:var(--fg-2);}

@media(max-width:720px){
  .mini-top h2{font-size:var(--t-h2);}
  .entry-row{grid-template-columns:1fr;}
  .do-row{grid-template-columns:1fr;}
  .ex-card{padding:var(--s5) var(--s4);}
  .wk-cell{min-height:50px;}
  .hero{padding:var(--s6) 0 var(--s5);}
  .proof{gap:var(--s5);}
  .proof .n{font-size:28px;}
  section.blk{padding:var(--s6) 0;}
  .stp{grid-template-columns:1fr;gap:var(--s2);}
  .stp .num{font-size:32px;}
  .ringbox{padding:var(--s4);}
  .apphead{padding-block:var(--s4) var(--s3);}
  .lvl{flex:0 0 100%;order:3;}
  .apphead .who{flex:1;}
  .tabs{gap:var(--s4);}
  .sticky-cta{display:block;}
  body.has-sticky .landing{padding-bottom:76px;}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important;}
}
"""
