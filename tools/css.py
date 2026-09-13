# -*- coding: utf-8 -*-
CSS = r"""
/* ============ TOKENS ============ */
/* base -> surfaces (dark/light) -> accent (flame/bloom/mint).
   The head script writes data-theme and data-accent before first paint. */
:root{
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px; --s8:64px;
  --r-ctl:8px; --r-card:16px; --r-pill:999px;
  /* one notch larger than before - this is a reading surface */
  --t-display:clamp(38px,8.5vw,68px); --t-h1:clamp(26px,4.5vw,34px); --t-h2:22px;
  --t-h3:17px; --t-body:16px; --t-sm:14px; --t-xs:12px;
  --f-display:'Secular One','Archivo Black','Noto Sans Arabic','Heebo',sans-serif;
  --f-ui:'Heebo','Inter','Noto Sans Arabic',system-ui,sans-serif;
}

/* fallback for the instant before the head script runs, and if JS is off */
:root{
  --ink-0:#14161C; --ink-1:#1B1E26; --ink-2:#242833; --ink-3:#333947; --ink-4:#454C5E;
  --fg:#E8EAF0; --fg-2:#A7AEBF; --fg-3:#8C94AA;
  --bar-bg:rgba(20,22,28,.88); --scrim:rgba(9,10,14,.88); color-scheme:dark; --num-dim:#626A80;
  --arrow-img:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238C94AA' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  --acc:#3DDCA8; --acc-hi:#63E8BC; --on-acc:#05130E; --acc-dim:rgba(61,220,168,.16);
  --ok:#4ADE80;
}

/* ---- dark surfaces ---- */
:root[data-theme="dark"]{
  --ink-0:#14161C; --ink-1:#1B1E26; --ink-2:#242833; --ink-3:#333947; --ink-4:#454C5E;
  --fg:#E8EAF0; --fg-2:#A7AEBF; --fg-3:#8C94AA;
  --bar-bg:rgba(20,22,28,.88); --scrim:rgba(9,10,14,.88); color-scheme:dark; --num-dim:#626A80;
  --ok:#4ADE80;
  --arrow-img:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%238C94AA' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
}
:root[data-theme="dark"][data-accent="flame"]{
  --acc:#FF7A47; --acc-hi:#FF9670; --on-acc:#0A0A0B; --acc-dim:rgba(255,122,71,.16);
}
:root[data-theme="dark"][data-accent="bloom"]{
  --acc:#FF7FB0; --acc-hi:#FF9BC3; --on-acc:#16050C; --acc-dim:rgba(255,127,176,.16);
}
:root[data-theme="dark"][data-accent="mint"]{
  --acc:#3DDCA8; --acc-hi:#63E8BC; --on-acc:#05130E; --acc-dim:rgba(61,220,168,.16);
}

/* ---- light surfaces ---- */
:root[data-theme="light"]{
  --ink-0:#FBF9F5; --ink-1:#FFFFFF; --ink-2:#F2EFE9; --ink-3:#E2DED6; --ink-4:#CFCABF;
  --fg:#1C1D22; --fg-2:#4A4F5C; --fg-3:#646A79;
  --bar-bg:rgba(251,249,245,.88); --scrim:rgba(28,29,34,.55); color-scheme:light; --num-dim:#948C7A;
  --ok:#1F7A45;
  --arrow-img:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23646A79' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
}
:root[data-theme="light"][data-accent="flame"]{
  --acc:#C2410C; --acc-hi:#9A3412; --on-acc:#FFFFFF; --acc-dim:rgba(194,65,12,.12);
}
:root[data-theme="light"][data-accent="bloom"]{
  --acc:#BE1D67; --acc-hi:#9D1050; --on-acc:#FFFFFF; --acc-dim:rgba(190,29,103,.12);
}
:root[data-theme="light"][data-accent="mint"]{
  --acc:#0F7A5C; --acc-hi:#0B6249; --on-acc:#FFFFFF; --acc-dim:rgba(15,122,92,.12);
}

*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;}
body{background:var(--ink-0);color:var(--fg);font-family:var(--f-ui);font-size:var(--t-body);
  line-height:1.65;min-height:100vh;-webkit-font-smoothing:antialiased;}
h1,h2,h3,.display{font-family:var(--f-display);font-weight:400;line-height:1.08;letter-spacing:-.02em;}
::selection{background:var(--acc);color:var(--on-acc);}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px;border-radius:4px;}
.tab:focus-visible{outline-offset:-3px;}
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
.btn-primary{background:var(--acc);color:var(--on-acc);}
.btn-primary:hover{background:var(--acc-hi);}
.btn-primary:disabled{background:var(--ink-3);color:var(--fg-2);cursor:not-allowed;transform:none;}
.btn-ghost{background:transparent;color:var(--fg);border:1px solid var(--ink-3);}
.btn-ghost:hover{border-color:var(--ink-4);background:var(--ink-1);}
.btn-quiet{background:transparent;color:var(--fg-2);padding:0 var(--s3);}
.btn-quiet:hover{color:var(--fg);}
.btn-sm{min-height:34px;padding:0 var(--s4);font-size:var(--t-xs);}
.btn-block{width:100%;}
.icon-btn{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;
  border:0;background:transparent;color:var(--fg-3);border-radius:var(--r-ctl);cursor:pointer;flex:none;}
.icon-btn:hover{color:var(--acc);background:var(--ink-2);}

/* ============ FIELDS ============ */
input[type=text],input[type=email],input[type=number],select,textarea{
  width:100%;background:var(--ink-2);border:1px solid var(--ink-3);border-radius:var(--r-ctl);
  color:var(--fg);padding:11px var(--s3);font-size:var(--t-body);font-family:var(--f-ui);
  min-height:44px;transition:border-color .14s;}
input:focus,select:focus,textarea:focus{border-color:var(--acc);outline:none;}
::placeholder{color:var(--fg-3);}
select{appearance:none;padding-inline-end:var(--s6);background-repeat:no-repeat;background-size:14px;
  background-position:calc(100% - 14px) center;background-image:var(--arrow-img);}
[dir=rtl] select{background-position:14px center;}
select option{background:var(--ink-2);color:var(--fg);}
.field{margin-bottom:var(--s3);}
.field>label{display:block;font-size:var(--t-sm);font-weight:600;color:var(--fg-2);margin-bottom:var(--s2);}

/* ============ LANG BAR ============ */
.langbar{position:fixed;inset-block-start:0;inset-inline:0;z-index:300;height:40px;
  background:var(--bar-bg);backdrop-filter:blur(12px);border-bottom:1px solid var(--ink-2);
  display:flex;align-items:center;justify-content:center;gap:var(--s1);padding:0 var(--s3);}
.langbtn{background:none;border:0;color:var(--fg-3);font-family:var(--f-ui);font-size:var(--t-xs);
  font-weight:600;padding:6px 10px;border-radius:var(--r-pill);cursor:pointer;
  min-height:32px;display:inline-flex;align-items:center;}
.langbtn:hover{color:var(--fg-2);}
.langbtn.on{color:var(--on-acc);background:var(--acc);}
.bar-sep{width:1px;height:16px;background:var(--ink-3);margin-inline:var(--s2);flex:none;}
.accdot{width:30px;height:30px;border-radius:50%;border:2px solid transparent;cursor:pointer;
  padding:0;flex:none;position:relative;background:transparent;}
.accdot::after{content:"";position:absolute;inset:4px;border-radius:50%;}
.accdot[data-set-accent="flame"]::after{background:#FF7A47;}
.accdot[data-set-accent="bloom"]::after{background:#FF7FB0;}
.accdot[data-set-accent="mint"]::after{background:#3DDCA8;}
.accdot:hover{border-color:var(--ink-4);}
.accdot.on{border-color:var(--fg);}
.modebtn{display:inline-grid;place-items:center;width:30px;height:30px;border:0;background:transparent;
  color:var(--fg-3);border-radius:50%;cursor:pointer;flex:none;margin-inline-start:var(--s1);}
.modebtn:hover{color:var(--fg);background:var(--ink-2);}
.modebtn svg{width:17px;height:17px;grid-area:1/1;}
.modebtn .ic-sun{display:none;}
.modebtn.is-light .ic-sun{display:block;}
.modebtn.is-light .ic-moon{display:none;}
@media(max-width:640px){
  .langbar{gap:2px;padding-inline:var(--s2);}
  .langbtn{padding:6px 6px;font-size:11px;}
  .bar-sep{margin-inline:4px;}
  .accdot{width:26px;height:26px;}
}
/* Below this the five full language names no longer fit across a phone, and a
   fixed bar that overflows drags the whole page sideways. Short codes fit. */
@media(max-width:560px){
  .langbtn{font-size:0;padding:6px 8px;}
  .langbtn::after{content:attr(data-short);font-size:12px;font-weight:700;}
}

/* ============ LANDING ============ */
.landing{padding-block-start:40px;}
.hero{padding:var(--s8) 0 var(--s7);}
.kicker{display:inline-flex;align-items:center;gap:var(--s2);font-size:var(--t-xs);font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--acc);margin-bottom:var(--s4);}
.hero h1{font-size:var(--t-display);margin-bottom:var(--s4);max-width:14ch;}
/* the one word the page is about, and the one sentence under it */
.hero-word{font-size:clamp(56px,14vw,124px);line-height:.95;letter-spacing:-.03em;margin-bottom:var(--s4);
  color:var(--acc);max-width:none;}
.hero-quote{margin:0 0 var(--s5);padding-inline-start:var(--s4);border-inline-start:3px solid var(--acc);max-width:60ch;}
.hero-quote p{font-family:var(--f-display);font-size:clamp(19px,3.4vw,28px);line-height:1.3;color:var(--fg);}
.hero-quote q{quotes:"\201C" "\201D";color:var(--acc);}
.hero-quote q::before{content:open-quote;} .hero-quote q::after{content:close-quote;}
[dir=rtl] .hero-quote q{quotes:"\201D" "\201C";}
.hero-def{color:var(--fg);font-weight:600;}
@media(max-width:520px){.hero-word{font-size:clamp(48px,17vw,72px);}.hero-quote p{font-size:19px;}}
.hero h1 .dim{color:var(--fg-3);}
.hero p.lead{font-size:clamp(15px,2.2vw,19px);color:var(--fg-2);max-width:48ch;margin-bottom:var(--s5);}
.hero .cta-row{display:flex;gap:var(--s3);flex-wrap:wrap;align-items:center;}
.hero .fineprint{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s4);}
.proof{display:flex;gap:var(--s7);flex-wrap:wrap;border-block:1px solid var(--ink-2);padding:var(--s5) 0;}
.proof .n{font-family:var(--f-display);font-size:34px;color:var(--acc);line-height:1;}
.proof .l{font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s1);}
section.blk{padding:var(--s7) 0;}
section.blk>h2{font-size:var(--t-h1);margin-bottom:var(--s5);max-width:18ch;}
.lede{font-size:clamp(16px,2.4vw,21px);color:var(--fg-2);max-width:56ch;line-height:1.6;}
.lede b{color:var(--fg);font-weight:600;}
.bengrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1px;background:var(--ink-2);
  border:1px solid var(--ink-2);border-radius:var(--r-card);overflow:hidden;}
.ben{background:var(--ink-0);padding:var(--s4);display:flex;gap:var(--s3);align-items:flex-start;font-size:var(--t-sm);}
.ben svg{color:var(--acc);margin-top:1px;}
.steps{display:grid;gap:var(--s5);}
.stp{display:grid;grid-template-columns:auto 1fr;gap:var(--s4);align-items:start;}
.stp .num{font-family:var(--f-display);font-size:44px;line-height:.9;color:var(--num-dim);width:1.6em;}
.stp h3{font-size:var(--t-h2);margin-bottom:var(--s2);}
.stp p{color:var(--fg-2);max-width:52ch;}

/* pricing */
.plans{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:var(--s3);}
.plan{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);display:flex;flex-direction:column;
  border:1px solid transparent;}
.plan.feature{border-color:var(--acc);}
.plan .tag{align-self:flex-start;display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--acc);background:var(--acc-dim);
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
.plan li svg{color:var(--acc);margin-top:2px;}
.plan .btn{margin-top:auto;}
.trust{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s4);text-align:center;}

/* faq */
.faq{border-top:1px solid var(--ink-2);}
.faq details{border-bottom:1px solid var(--ink-2);}
.faq summary{list-style:none;cursor:pointer;padding:var(--s4) 0;font-weight:600;
  display:flex;justify-content:space-between;align-items:center;gap:var(--s4);}
.faq summary::-webkit-details-marker{display:none;}
.faq summary svg{color:var(--fg-3);transition:transform .18s;flex:none;transform:rotate(90deg);}
.faq details[open] summary svg{transform:rotate(-90deg);color:var(--acc);}
.faq p{color:var(--fg-2);font-size:var(--t-sm);padding-bottom:var(--s4);max-width:64ch;}
.finale{text-align:center;padding:var(--s8) 0;border-top:1px solid var(--ink-2);}
.finale h2{font-size:var(--t-h1);margin-bottom:var(--s2);}
.finale p{color:var(--fg-2);margin-bottom:var(--s5);}
footer{text-align:center;color:var(--fg-3);font-size:var(--t-xs);padding:var(--s5) 0 var(--s7);border-top:1px solid var(--ink-2);}
.sticky-cta{position:fixed;inset-block-end:0;inset-inline:0;z-index:120;display:none;
  padding:var(--s3) var(--s4) calc(var(--s3) + env(safe-area-inset-bottom));
  background:var(--bar-bg);backdrop-filter:blur(12px);border-top:1px solid var(--ink-2);}

/* ============ ONBOARDING ============ */
.onb{display:none;position:fixed;inset:0;z-index:200;background:var(--ink-0);overflow-y:auto;
  padding:56px var(--s4) var(--s7);}
.onb-inner{max-width:560px;margin:0 auto;}
.onb-top{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);margin-bottom:var(--s3);}
.onb-top .mark{display:flex;align-items:center;gap:var(--s2);font-weight:700;font-size:var(--t-sm);}
.onb-top .mark img{width:28px;height:28px;border-radius:7px;}
.onb-top .count{font-size:var(--t-xs);color:var(--fg-3);}
.bar{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;margin-bottom:var(--s6);}
.bar>i{display:block;height:100%;background:var(--acc);border-radius:var(--r-pill);transition:width .3s ease;}
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
.opt.on{border-color:var(--acc);background:var(--acc-dim);color:var(--fg);}
.opt.on svg{color:var(--acc);}
.chips{display:flex;flex-wrap:wrap;gap:var(--s2);}
.chip{background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-pill);padding:8px 14px;
  font-size:var(--t-sm);cursor:pointer;user-select:none;transition:border-color .12s,background .12s;}
.chip:hover{border-color:var(--ink-4);}
.chip.on{border-color:var(--acc);background:var(--acc-dim);color:var(--acc);}
.nav{display:flex;gap:var(--s2);margin-top:var(--s6);}
.nav .btn-primary{flex:1;}
.note{background:var(--ink-1);border-inline-start:2px solid var(--acc);border-radius:var(--r-ctl);
  padding:var(--s3) var(--s4);font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s4);
  display:flex;gap:var(--s2);align-items:center;}
.note svg{color:var(--acc);}
.built{display:grid;gap:var(--s2);margin-bottom:var(--s5);}
.built div{display:flex;gap:var(--s2);align-items:center;font-size:var(--t-sm);color:var(--fg-2);}
.built svg{color:var(--acc);}

/* ============ APP ============ */
#app{display:none;padding-block:40px var(--s8);}
.trialbar{display:none;align-items:center;justify-content:center;gap:var(--s3);flex-wrap:wrap;
  background:var(--acc-dim);border-radius:var(--r-pill);padding:var(--s2) var(--s4);
  font-size:var(--t-xs);color:var(--acc);font-weight:600;margin:var(--s4) 0;}
.trialbar.on{display:flex;}
.trialbar button{background:var(--acc);color:var(--on-acc);border:0;border-radius:var(--r-pill);
  padding:5px 12px;font-family:var(--f-ui);font-weight:700;font-size:var(--t-xs);cursor:pointer;}
.apphead{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);flex-wrap:wrap;
  padding:var(--s5) 0 var(--s4);}
.apphead .who{display:flex;align-items:center;gap:var(--s3);min-width:0;}
.apphead img{width:40px;height:40px;border-radius:10px;flex:none;}
.apphead .greet{font-family:var(--f-display);font-weight:400;letter-spacing:-.02em;line-height:1.15;font-size:var(--t-h2);}
.apphead .quote{font-size:var(--t-xs);color:var(--fg-2);}
.apphead .date{font-size:var(--t-xs);color:var(--fg-3);}
.lvl{min-width:150px;}
.lvl .row{display:flex;align-items:baseline;justify-content:space-between;gap:var(--s3);margin-bottom:var(--s2);}
.lvl .lab{font-size:var(--t-xs);color:var(--fg-3);}
.lvl .num{font-family:var(--f-display);font-size:var(--t-h2);color:var(--fg);margin-inline-start:4px;}
.lvl .stage{font-size:var(--t-xs);color:var(--acc);font-weight:700;}
.xp{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;}
.xp>i{display:block;height:100%;background:var(--acc);transition:width .35s ease;}
.tabs{display:flex;gap:var(--s5);border-bottom:1px solid var(--ink-2);margin-bottom:var(--s5);
  overflow-x:auto;scrollbar-width:none;}
.tabs::-webkit-scrollbar{display:none;}
.tab{border:0;background:none;color:var(--fg-3);font-family:var(--f-ui);font-weight:700;font-size:var(--t-sm);
  padding:var(--s3) 0;cursor:pointer;white-space:nowrap;position:relative;display:inline-flex;align-items:center;gap:var(--s2);}
.tab:hover{color:var(--fg-2);}
.tab.on{color:var(--fg);}
.tab.on::after{content:"";position:absolute;inset-inline:0;inset-block-end:-1px;height:2px;background:var(--acc);}
.page{display:none;}
.page.on{display:block;animation:rise .2s ease both;}
.ptitle{font-size:var(--t-h1);margin-bottom:var(--s2);}
.psub{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s5);max-width:60ch;}
.card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);}

/* home: insight */
.insight{display:flex;gap:var(--s3);background:var(--ink-1);border-radius:var(--r-card);
  padding:var(--s4);margin-bottom:var(--s3);align-items:flex-start;}
.insight svg{color:var(--acc);flex:none;margin-top:2px;}
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
.stat .v svg{width:16px;height:16px;color:var(--acc);}
.stat .k{font-size:var(--t-xs);color:var(--fg-3);margin-top:2px;}

/* home: challenge */
.chal{display:flex;align-items:center;justify-content:space-between;gap:var(--s4);flex-wrap:wrap;
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);margin-bottom:var(--s5);}
.chal .lab{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--acc);font-weight:700;}
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
.cathead .ct b{color:var(--acc);}
.task{display:flex;align-items:center;gap:var(--s3);padding:var(--s2) 0;}
.task+.task{border-top:1px solid var(--ink-2);}
.cb{appearance:none;width:20px;height:20px;flex:none;border-radius:6px;border:1.5px solid var(--ink-4);
  cursor:pointer;display:grid;place-items:center;transition:background .12s,border-color .12s;}
.cb:hover{border-color:var(--acc);}
.cb:checked{background:var(--acc);border-color:var(--acc);}
.cb:checked::after{content:"";width:11px;height:6px;border-inline-start:2px solid var(--on-acc);
  border-bottom:2px solid var(--on-acc);transform:rotate(-45deg) translate(1px,-2px);}
.task .body{flex:1;min-width:0;}
.task .ttl{font-size:var(--t-body);}
.task .ttl.done{color:var(--fg-3);text-decoration:line-through;}
.task .meta{display:flex;align-items:center;gap:var(--s2);font-size:var(--t-xs);color:var(--fg-3);margin-top:2px;}
.task .meta svg{width:13px;height:13px;}
.task .thumb{width:32px;height:32px;border-radius:6px;object-fit:cover;flex:none;}
.tmr{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:26px;
  background:var(--ink-2);border:1px solid var(--ink-3);color:var(--fg-2);border-radius:var(--r-pill);
  font-size:11px;padding:0 8px;cursor:pointer;font-family:var(--f-ui);font-variant-numeric:tabular-nums;flex:none;}
.tmr:hover{border-color:var(--acc);color:var(--acc);}
.tmr svg{width:13px;height:13px;}
.tmr.run{background:var(--acc);border-color:var(--acc);color:var(--on-acc);}
.empty{font-size:var(--t-sm);color:var(--fg-3);padding:var(--s3) 0;}
.sugs{display:flex;flex-wrap:wrap;gap:var(--s1);margin:var(--s3) 0;}
.sug{background:transparent;border:1px dashed var(--ink-3);color:var(--fg-3);border-radius:var(--r-pill);
  padding:4px 10px;font-size:var(--t-xs);cursor:pointer;font-family:var(--f-ui);}
.sug:hover{border-color:var(--acc);color:var(--acc);border-style:solid;}
.addrow{display:flex;gap:var(--s2);margin-top:var(--s3);}
.addrow input[type=text]{flex:1;min-width:0;min-height:38px;font-size:var(--t-sm);}
.addrow input[type=number]{width:64px;min-height:38px;font-size:var(--t-sm);text-align:center;}
.addrow .btn{min-height:38px;padding:0 var(--s4);}

/* goals */
.goal{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);margin-bottom:var(--s3);}
.goal>h3{display:flex;align-items:center;gap:var(--s2);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-h3);letter-spacing:0;margin-bottom:var(--s3);}
.goal>h3 svg{color:var(--acc);flex:none;}
.goal>h3 .icon-btn{margin-inline-start:auto;}
.acts{display:grid;}
.acts label{display:flex;align-items:center;gap:var(--s3);padding:var(--s2) 0;cursor:pointer;font-size:var(--t-sm);}
.acts label+label{border-top:1px solid var(--ink-2);}
.acts .done{color:var(--fg-3);text-decoration:line-through;}
.gmeta{display:flex;align-items:center;justify-content:space-between;font-size:var(--t-xs);
  color:var(--fg-3);margin-top:var(--s3);font-variant-numeric:tabular-nums;}
.gbar{height:3px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;margin-top:var(--s2);}
.gbar>i{display:block;height:100%;background:var(--acc);transition:width .3s;}
.newrow{display:flex;gap:var(--s2);margin-top:var(--s4);}
.newrow input{flex:1;min-width:0;}

/* week */
.wkbar{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);flex-wrap:wrap;
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s3) var(--s4);margin-bottom:var(--s3);font-size:var(--t-sm);}
.wkbar b{font-family:var(--f-display);font-size:var(--t-h3);color:var(--acc);}
.scroller{overflow-x:auto;border-radius:var(--r-card);background:var(--ink-1);}
table.grid{border-collapse:collapse;width:100%;min-width:560px;}
table.grid th,table.grid td{padding:0;text-align:center;}
table.grid thead th{font-size:var(--t-xs);color:var(--fg-3);font-weight:600;padding:var(--s3) var(--s1);
  border-bottom:1px solid var(--ink-2);}
table.grid thead th.today{color:var(--acc);}
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
td.dcell.on .mk{background:var(--acc);border-color:var(--acc);color:var(--on-acc);}
td.dcell .mk svg{width:13px;height:13px;}
td.scell{font-size:var(--t-xs);font-weight:700;min-width:96px;padding-inline:var(--s3);}
td.scell.win{color:var(--acc);}
td.scell.mid{color:var(--fg-2);}
td.scell.none{color:var(--fg-3);}
.review{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);margin-top:var(--s3);text-align:center;}
.review h3{font-size:var(--t-h2);margin-bottom:var(--s2);}
.review p{color:var(--fg-2);font-size:var(--t-sm);margin-bottom:var(--s4);}
.rvout{display:none;margin-top:var(--s4);padding-top:var(--s4);border-top:1px solid var(--ink-2);}
.rvout.on{display:block;}
.rvout .big{font-family:var(--f-display);font-size:44px;line-height:1;}
.rvout .msg{color:var(--fg-2);font-size:var(--t-sm);margin:var(--s2) 0;}
.rvout .pts{color:var(--acc);font-weight:700;}

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
.infoline svg{color:var(--acc);flex:none;}
.sechead{font-size:var(--t-h2);margin:var(--s7) 0 var(--s2);}
.sechead:first-child{margin-top:0;}

/* why it works */
.thgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--s3);}
.th{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);position:relative;}
.th .n{color:var(--num-dim);position:absolute;inset-block-start:var(--s4);inset-inline-end:var(--s4);
  font-family:var(--f-display);font-size:34px;line-height:1;}
.th>svg{color:var(--acc);width:22px;height:22px;margin-bottom:var(--s3);}
.th h4{font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);letter-spacing:0;padding-inline-end:var(--s6);}
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
.modal-bg{position:fixed;inset:0;background:var(--scrim);backdrop-filter:blur(6px);
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

/* ============ NEW: LANDING EXPLAINER ============ */
.btn-lg{min-height:52px;padding:0 var(--s6);font-size:var(--t-body);}
.hero .fineprint{display:inline-flex;align-items:center;gap:var(--s2);}
.hero .fineprint svg{width:15px;height:15px;color:var(--acc);flex:none;}
.sc-hint{font-size:var(--t-sm);color:var(--fg-3);margin:var(--s5) 0 var(--s3);}

.scgrid{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:var(--s3);}
.sc{background:var(--ink-1);border:1px solid var(--ink-2);border-radius:var(--r-card);
  padding:var(--s4);display:flex;flex-direction:column;gap:var(--s3);
  transition:border-color .16s,transform .16s;}
.sc:hover{border-color:var(--ink-4);transform:translateY(-2px);}
.sc-h{display:flex;align-items:center;gap:var(--s2);font-weight:700;font-size:var(--t-sm);
  padding-bottom:var(--s3);border-bottom:1px solid var(--ink-2);}
.sc-h svg{color:var(--fg-3);width:16px;height:16px;}
.sc-tag{display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;margin-bottom:var(--s1);}
.sc-tag svg{width:13px;height:13px;}
.sc-r .sc-tag{color:var(--fg-3);}
.sc-p .sc-tag{color:var(--acc);}
.sc p{font-size:var(--t-sm);line-height:1.5;}
.sc-r p{color:var(--fg-3);}
.sc-p p{color:var(--fg);font-weight:600;}
.sc-p{border-inline-start:2px solid var(--acc);padding-inline-start:var(--s3);}
.sc-r{border-inline-start:2px solid var(--ink-3);padding-inline-start:var(--s3);}
.sc-close{display:flex;align-items:center;gap:var(--s2);margin-top:var(--s4);
  font-size:var(--t-sm);color:var(--fg-2);}
.sc-close svg{color:var(--acc);flex:none;}
.steps{list-style:none;}

/* ============ NEW: ONBOARDING ============ */
.welc{list-style:none;display:grid;gap:var(--s3);margin-bottom:var(--s4);}
.welc li{display:flex;gap:var(--s3);align-items:flex-start;font-size:var(--t-sm);color:var(--fg-2);}
.welc svg{color:var(--acc);flex:none;margin-top:2px;}
.agehint{min-height:1.2em;color:var(--acc);font-weight:600;}
#oAge{max-width:140px;}
.swatch .sw{width:22px;height:22px;border-radius:50%;display:block;border:2px solid var(--ink-3);}
.sw-flame{background:#FF7A47;} .sw-bloom{background:#FF7FB0;} .sw-mint{background:#3DDCA8;}
.swatch.on .sw{border-color:var(--fg);}

/* ---- the check-in ---- */
.qz-h{font-size:var(--t-h2)!important;}
.qz-meta{display:flex;align-items:baseline;justify-content:space-between;gap:var(--s3);
  margin-top:var(--s5);margin-bottom:var(--s2);}
.qz-count{font-size:var(--t-sm);font-weight:700;color:var(--acc);font-variant-numeric:tabular-nums;}
.qz-dim{font-size:var(--t-xs);color:var(--fg-3);text-transform:uppercase;letter-spacing:.08em;font-weight:700;}
.bar.qz-bar{height:6px;margin-bottom:var(--s5);}
.qz-q{font-family:var(--f-display);font-size:clamp(21px,4.4vw,30px);line-height:1.18;
  margin-bottom:var(--s4);min-height:2.2em;}
.qz-opts{display:grid;gap:var(--s2);}
.qz-opt{display:flex;align-items:center;gap:var(--s3);width:100%;text-align:start;
  background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-ctl);
  padding:var(--s3) var(--s4);min-height:56px;cursor:pointer;color:var(--fg);
  font-family:var(--f-ui);font-size:var(--t-body);line-height:1.35;
  transition:border-color .14s,background .14s,transform .08s;}
.qz-opt:hover{border-color:var(--acc);background:var(--ink-2);}
.qz-opt:active{transform:scale(.99);}
.qz-opt.on{border-color:var(--acc);background:var(--acc-dim);}
.qz-let{display:grid;place-items:center;width:26px;height:26px;flex:none;border-radius:8px;
  background:var(--ink-2);color:var(--fg-2);font-size:var(--t-xs);font-weight:700;}
.qz-opt.on .qz-let{background:var(--acc);color:var(--on-acc);}
.qz-tx{flex:1;min-width:0;}
.qz-tick{opacity:0;color:var(--acc);flex:none;transition:opacity .14s;}
.qz-opt.on .qz-tick{opacity:1;}
.qz-foot{display:flex;justify-content:flex-start;margin-top:var(--s4);}

/* ============ NEW: PROFILE ============ */
.profile{display:grid;gap:var(--s4);}
.pro-score{display:flex;align-items:center;gap:var(--s4);background:var(--acc-dim);
  border-radius:var(--r-card);padding:var(--s4) var(--s5);}
.pro-num{font-family:var(--f-display);font-size:52px;line-height:1;color:var(--acc);}
.pro-num span{font-size:24px;font-weight:600;}
.pro-lab{font-size:var(--t-xs);color:var(--fg-2);text-transform:uppercase;letter-spacing:.08em;font-weight:700;}
.pro-band{font-family:var(--f-display);font-size:var(--t-h2);margin-top:2px;}
.meters{display:grid;gap:var(--s3);}
.mtr-top{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);margin-bottom:6px;}
.mtr-n{display:inline-flex;align-items:center;gap:var(--s2);font-size:var(--t-sm);font-weight:600;}
.mtr-n svg{color:var(--acc);width:16px;height:16px;}
.mtr-v{font-size:var(--t-sm);color:var(--fg-2);font-variant-numeric:tabular-nums;}
.mtr-bar{height:8px;border-radius:var(--r-pill);background:var(--ink-2);overflow:hidden;}
.mtr-bar>i{display:block;height:100%;border-radius:var(--r-pill);background:var(--acc);
  transition:width .5s cubic-bezier(.2,.8,.3,1);}
.pro-blk{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);}
.pro-blk h3{font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);letter-spacing:0;margin-bottom:var(--s2);}
.pro-blk p{color:var(--fg-2);font-size:var(--t-sm);}
.pro-acts{margin:0;padding-inline-start:var(--s5);display:grid;gap:var(--s2);}
.pro-acts li{font-size:var(--t-sm);color:var(--fg-2);}
.pro-acts li::marker{color:var(--acc);font-weight:700;}

/* ============ NEW: DASHBOARD ============ */
.dash-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s2);margin-bottom:var(--s3);}
.dstat{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4) var(--s2);text-align:center;}
.dstat svg{color:var(--acc);width:18px;height:18px;}
.dstat .dv{font-family:var(--f-display);font-size:26px;line-height:1.1;margin-top:var(--s1);}
.dstat .dk{font-size:11px;color:var(--fg-3);margin-top:2px;line-height:1.25;}
.dstreak{grid-column:1/-1;font-size:var(--t-sm);color:var(--fg-2);text-align:center;
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s3);}

.nextcard{margin-bottom:var(--s3);}
.next{background:var(--ink-1);border:1px solid var(--acc);border-radius:var(--r-card);padding:var(--s5);}
.next-lab{display:flex;align-items:center;gap:var(--s2);font-size:10px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--acc);}
.next-lab svg{width:15px;height:15px;}
.next-th{margin-inline-start:auto;color:var(--fg-3);letter-spacing:.04em;}
.next-tx{font-family:var(--f-display);font-size:clamp(19px,3.4vw,26px);line-height:1.2;margin-top:var(--s3);}
.next-sub{font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s2);}
.next-btns{display:flex;gap:var(--s2);flex-wrap:wrap;margin-top:var(--s4);}
.next-btns .btn{flex:1;min-width:150px;}
.next.done{display:flex;gap:var(--s3);align-items:center;border-color:var(--ink-2);}
.next.done svg{color:var(--acc);flex:none;width:26px;height:26px;}
.next.done .next-tx{font-family:var(--f-ui);font-size:var(--t-body);margin-top:2px;}

.dash-two{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:var(--s3);margin-bottom:var(--s3);}
.dash-box{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s4);margin-bottom:var(--s3);}
.dash-two .dash-box{margin-bottom:0;}
.boxh{display:flex;align-items:center;gap:var(--s2);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-h3);letter-spacing:0;margin-bottom:var(--s3);}
.boxh svg{color:var(--acc);}
.boxh-row{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);}
.boxh-row .boxh{margin-bottom:var(--s3);}
.boxh-n{font-size:var(--t-xs);color:var(--fg-3);font-variant-numeric:tabular-nums;}
.dash-box .profile{gap:var(--s3);}
.dash-box .pro-blk{background:var(--ink-2);}
.fchips{display:flex;flex-wrap:wrap;gap:var(--s1);margin:var(--s3) 0;}
.fchip{display:inline-flex;align-items:center;gap:6px;background:var(--ink-2);border-radius:var(--r-pill);
  padding:5px 11px;font-size:var(--t-xs);color:var(--fg-2);}
.fchip svg{width:13px;height:13px;color:var(--fg-3);}
.mini-ladder{display:grid;gap:var(--s2);}
.mini-ladder div{display:flex;gap:var(--s3);align-items:baseline;font-size:var(--t-sm);}
.mini-ladder span{color:var(--fg-3);font-size:var(--t-xs);min-width:70px;flex:none;}
.mini-ladder b{color:var(--fg);font-weight:600;}

/* ============ NEW: GOAL CHAIN ============ */
.chain{margin-bottom:var(--s4);}
.ch-head{display:flex;align-items:center;justify-content:space-between;gap:var(--s3);margin-bottom:var(--s2);min-height:34px;}
.ch-count{font-size:var(--t-xs);color:var(--fg-3);font-weight:700;}
.bar.ch-bar{height:4px;margin-bottom:var(--s4);}
.ch-q{font-family:var(--f-display);font-size:clamp(20px,4vw,26px);line-height:1.2;margin-bottom:var(--s1);}
.ch-areas{grid-template-columns:repeat(3,1fr);}
.ch-freq,.ch-obst{grid-template-columns:repeat(auto-fit,minmax(130px,1fr));}
.ch-other.hidden{display:none;}
.ch-other{margin-top:var(--s3);}
.ch-ladder{margin-top:var(--s3);}
.ch-nav{margin-top:var(--s4);}
.ch-nav .btn{flex:1;}
.ch-plan{display:flex;align-items:center;gap:var(--s2);flex-wrap:wrap;margin-top:var(--s4);
  padding-top:var(--s3);border-top:1px solid var(--ink-2);font-size:var(--t-sm);color:var(--fg-2);}
.ch-free{margin:var(--s3) 0 var(--s4);}
.ch-free summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:var(--s2);
  font-size:var(--t-sm);color:var(--fg-2);padding:var(--s2) 0;}
.ch-free summary::-webkit-details-marker{display:none;}
.ch-free summary svg{transition:transform .18s;transform:rotate(90deg);color:var(--fg-3);}
.ch-free[open] summary svg{transform:rotate(-90deg);}
#newGoalBtn{margin-bottom:var(--s3);}
.pf-grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--s3);}
@media(max-width:520px){.pf-grid{grid-template-columns:1fr;}}
.gstate{display:inline-flex;align-items:center;gap:6px;font-size:var(--t-xs);font-weight:700;
  color:var(--fg-3);margin-bottom:var(--s3);}
.gstate svg{width:13px;height:13px;}
.gstate.on{color:var(--acc);}
.goal.unstarted{border:1px dashed var(--ink-3);}
.gstart-n{margin:0 0 var(--s3);}

/* the micro-tip: a short line that slides up, not a modal, not a lecture */
.tipcard{position:fixed;inset-inline:var(--s4);inset-block-end:calc(var(--s5) + 52px);z-index:390;
  margin-inline:auto;max-width:480px;background:var(--ink-1);border:1px solid var(--acc);
  border-radius:var(--r-card);padding:var(--s3) var(--s4);display:flex;flex-direction:column;gap:3px;
  box-shadow:0 8px 30px rgba(0,0,0,.25);opacity:0;transform:translateY(14px);pointer-events:none;
  transition:opacity .25s,transform .25s;}
.tipcard.on{opacity:1;transform:none;}
.tip-lab{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--acc);}
.tip-lab svg{width:13px;height:13px;}
.tip-tx{font-size:var(--t-sm);color:var(--fg);}

/* ============ NEW: GOAL LADDER ============ */
.ladder{display:grid;gap:0;margin-bottom:var(--s4);border-inline-start:2px solid var(--ink-3);
  padding-inline-start:var(--s4);}
.rung{position:relative;padding:var(--s2) 0;display:flex;align-items:center;gap:var(--s3);flex-wrap:wrap;}
.rung::before{content:"";position:absolute;inset-inline-start:calc(var(--s4) * -1 - 6px);top:50%;
  width:10px;height:10px;border-radius:50%;background:var(--ink-3);transform:translateY(-50%);}
.rung.now::before{background:var(--acc);}
.rung-k{font-size:10px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
  color:var(--fg-3);min-width:64px;flex:none;}
.rung-v{font-size:var(--t-sm);}
.rung-v.strong{font-weight:700;}
.rung-in{flex:1;min-width:140px;min-height:38px;font-size:var(--t-sm);background:var(--ink-2);}
.acts-h{font-size:10px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
  color:var(--fg-3);margin-bottom:var(--s1);}
.empty-state{text-align:center;padding:var(--s7) var(--s4);background:var(--ink-1);border-radius:var(--r-card);}
.empty-state svg{width:34px;height:34px;color:var(--ink-4);margin-bottom:var(--s3);}
.empty-state p{color:var(--fg-3);font-size:var(--t-sm);max-width:34ch;margin-inline:auto;}

/* ============ NEW: LESSONS ============ */
.lsgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:var(--s3);
  align-items:start;}
.lsn{background:var(--ink-1);border:1px solid var(--ink-2);border-radius:var(--r-card);overflow:hidden;
  transition:border-color .16s;}
.lsn:hover{border-color:var(--ink-4);}
.lsn[open]{border-color:var(--acc);}
.lsn summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:var(--s3);
  padding:var(--s4);font-weight:700;font-size:var(--t-sm);}
.lsn summary::-webkit-details-marker{display:none;}
.lsn-i{display:grid;place-items:center;width:32px;height:32px;border-radius:9px;flex:none;
  background:var(--acc-dim);color:var(--acc);}
.lsn-i svg{width:17px;height:17px;}
.lsn-t{flex:1;min-width:0;}
.lsn-m{font-size:var(--t-xs);color:var(--fg-3);font-weight:600;flex:none;}
.lsn-c{color:var(--fg-3);transition:transform .18s;flex:none;transform:rotate(90deg);}
.lsn[open] .lsn-c{transform:rotate(-90deg);color:var(--acc);}
.lsn.read .lsn-i{background:var(--acc);color:var(--on-acc);}
.lsn-b{padding:0 var(--s4) var(--s4);}
.lsn-b>p{font-size:var(--t-sm);color:var(--fg-2);line-height:1.6;}
.lsn-ex,.lsn-do{margin-top:var(--s3);padding:var(--s3);border-radius:var(--r-ctl);background:var(--ink-2);}
.lsn-do{background:var(--acc-dim);}
.lsn-ex .lab,.lsn-do .lab{display:flex;align-items:center;gap:6px;font-size:10px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;color:var(--fg-2);margin-bottom:var(--s1);}
.lsn-do .lab{color:var(--acc);}
.lsn-do .lab svg{width:13px;height:13px;}
.lsn-ex p,.lsn-do p{font-size:var(--t-sm);color:var(--fg-2);line-height:1.5;}
.lsn-do p{color:var(--fg);}
.lsn-b .btn{margin-top:var(--s3);}

/* ============ NEW: ACHIEVEMENTS ============ */
.achgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:var(--s2);}
.ach{display:flex;gap:var(--s3);align-items:center;background:var(--ink-2);border-radius:var(--r-ctl);
  padding:var(--s3);opacity:.78;}
.ach.on{opacity:1;background:var(--acc-dim);}
.ach-i{display:grid;place-items:center;width:34px;height:34px;border-radius:10px;flex:none;
  background:var(--ink-3);color:var(--fg-3);}
.ach.on .ach-i{background:var(--acc);color:var(--on-acc);}
.ach-i svg{width:17px;height:17px;}
.ach-t{font-size:var(--t-sm);font-weight:700;}
.ach-d{font-size:var(--t-xs);color:var(--fg-2);margin-top:1px;}

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
.mini-card:hover{border-color:var(--acc);}
.mini-card:active{transform:scale(.99);}
.mini-card .mc-ic{display:grid;place-items:center;width:48px;height:48px;border-radius:var(--r-ctl);
  background:var(--acc-dim);color:var(--acc);margin-bottom:var(--s2);}
.mini-card .mc-ic svg{width:24px;height:24px;}
.mini-card .mc-n{font-family:var(--f-display);font-size:var(--t-h2);}
.mini-card .mc-d{font-size:var(--t-sm);color:var(--fg-2);}
.mini-card .mc-s{font-size:var(--t-xs);color:var(--acc);font-weight:700;}
.mini-card .mc-go{display:flex;align-items:center;gap:var(--s2);font-size:var(--t-sm);font-weight:700;
  color:var(--fg-3);margin-top:var(--s2);}
.mini-card:hover .mc-go{color:var(--acc);}

.big-btn{display:flex;align-items:center;justify-content:center;gap:var(--s2);width:100%;min-height:56px;
  border:0;border-radius:var(--r-pill);background:var(--acc);color:var(--on-acc);
  font-family:var(--f-ui);font-weight:700;font-size:var(--t-h3);cursor:pointer;margin:var(--s4) 0;
  transition:background .14s,transform .08s;}
.big-btn:hover{background:var(--acc-hi);}
.big-btn:active{transform:scale(.985);}
.big-btn svg{width:20px;height:20px;}
.row-btns{display:flex;gap:var(--s2);flex-wrap:wrap;}
.sub-h{font-size:var(--t-h2);margin:var(--s6) 0 var(--s2);}
.mini-h{display:flex;align-items:center;gap:var(--s2);font-family:var(--f-ui);font-weight:700;
  font-size:var(--t-sm);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  margin:var(--s5) 0 var(--s3);}
.mini-h svg{width:15px;height:15px;color:var(--acc);}
.hint{display:flex;gap:var(--s2);align-items:flex-start;font-size:var(--t-sm);color:var(--fg-2);
  background:var(--ink-1);border-radius:var(--r-card);padding:var(--s3) var(--s4);margin:var(--s4) 0;}
.hint svg{color:var(--acc);flex:none;margin-top:2px;}
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
.pick-card:hover{border-color:var(--acc);}
.pick-card .pk-n{font-size:var(--t-h3);font-weight:700;}
.pick-card .pk-m{font-size:var(--t-xs);color:var(--fg-3);}
.pick-card svg{margin-inline-start:auto;color:var(--fg-3);}
.pick-card:hover svg{color:var(--acc);}

.dots{display:flex;gap:6px;justify-content:center;margin-bottom:var(--s4);}
.dots .dot{width:8px;height:8px;border-radius:50%;background:var(--ink-3);transition:background .2s,transform .2s;}
.dots .dot.done{background:var(--acc);}
.dots .dot.now{background:var(--acc);transform:scale(1.5);}

.ex-card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s6) var(--s5);text-align:center;
  transition:opacity .2s;}
.ex-card.resting{opacity:.35;pointer-events:none;}
.ex-card .ex-of{font-size:var(--t-xs);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.ex-card .ex-n{font-family:var(--f-display);font-size:clamp(26px,5vw,38px);margin:var(--s2) 0;}
.ex-card .ex-r{font-size:var(--t-h2);color:var(--acc);font-weight:700;font-variant-numeric:tabular-nums;}
.ex-card .ex-c{font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s3);max-width:38ch;margin-inline:auto;}

.rest{display:none;background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);text-align:center;margin-top:var(--s3);}
.rest.on{display:block;animation:rise .2s ease both;}
.rest .rest-l{font-size:var(--t-xs);letter-spacing:.08em;text-transform:uppercase;color:var(--fg-3);font-weight:700;}
.rest .rest-n{font-family:var(--f-display);font-size:54px;line-height:1;color:var(--acc);font-variant-numeric:tabular-nums;}
.rest .rest-x{font-size:var(--t-sm);color:var(--fg-2);margin:var(--s2) 0 var(--s3);}

.done-card{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s7) var(--s5);text-align:center;}
.done-card .big-check{width:44px;height:44px;color:var(--acc);margin-bottom:var(--s3);}
.done-card h3{font-size:var(--t-h1);}
.done-card .done-m{font-size:var(--t-h3);color:var(--acc);font-weight:700;margin-top:var(--s2);}
.done-card .done-msg{color:var(--fg-2);font-size:var(--t-sm);margin-top:var(--s3);}

.wk-board{display:grid;grid-template-columns:repeat(7,1fr);gap:var(--s1);}
.wk-cell{background:var(--ink-1);border-radius:var(--r-ctl);padding:var(--s2) 2px;text-align:center;min-height:56px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:var(--s1);}
.wk-cell.today{outline:1px solid var(--ink-4);}
.wk-cell.on{background:var(--acc);color:var(--on-acc);}
.wk-cell.half{background:var(--acc-dim);color:var(--acc);}
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
.do-btn:hover{border-color:var(--acc);}
.do-btn svg{width:18px;height:18px;color:var(--fg-3);}
.do-btn.done{background:var(--acc);border-color:var(--acc);color:var(--on-acc);}
.do-btn.done svg{color:var(--on-acc);}

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
.entry-btn:hover{border-color:var(--acc);}
.entry-btn svg{width:28px;height:28px;color:var(--acc);}

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
.fr-tab.on::after{content:"";position:absolute;inset-inline:0;inset-block-end:-1px;height:2px;background:var(--acc);}

.rec{background:var(--ink-1);border-radius:var(--r-card);padding:var(--s5);margin-bottom:var(--s3);}
.rec-h{display:flex;align-items:flex-start;gap:var(--s3);margin-bottom:var(--s3);}
.rec-n{font-family:var(--f-display);font-size:var(--t-h2);}
.rec-m{display:flex;align-items:center;gap:6px;font-size:var(--t-xs);color:var(--fg-3);margin-top:var(--s1);}
.rec-m svg{width:13px;height:13px;}
.rec-m b{color:var(--acc);}
.rec-h .fav{margin-inline-start:auto;}
.rec-h .fav.on{color:var(--acc);}
.rec-i{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:var(--s2);}
.rec-i .ri-h{font-size:var(--t-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  font-weight:700;margin-inline-end:var(--s1);}
.ri{display:inline-flex;align-items:center;gap:4px;font-size:var(--t-xs);border-radius:var(--r-pill);padding:3px 10px;}
.ri.ok{background:var(--acc-dim);color:var(--acc);}
.ri.ok svg{width:12px;height:12px;}
.ri.no{background:var(--ink-2);color:var(--fg-3);}
.rec-s{border-top:1px solid var(--ink-2);padding-top:var(--s3);margin-top:var(--s3);}
.rec-s .rs-h{font-size:var(--t-xs);letter-spacing:.06em;text-transform:uppercase;color:var(--fg-3);
  font-weight:700;margin-bottom:var(--s2);}
.rec-s ol{padding-inline-start:1.2em;display:grid;gap:var(--s2);}
.rec-s li{font-size:var(--t-sm);color:var(--fg-2);}

/* suggested-recipe library, always present at the bottom of the fridge app */
.sug{border-top:1px solid var(--ink-2);margin-top:var(--s6);padding-top:var(--s2);}
.sug-filters{display:flex;gap:var(--s2);flex-wrap:wrap;margin-bottom:var(--s4);}
.sug-f{background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-pill);
  color:var(--fg-2);font-family:var(--f-ui);font-weight:600;font-size:var(--t-sm);
  padding:9px 16px;cursor:pointer;min-height:38px;transition:border-color .14s,background .14s,color .14s;}
.sug-f:hover{border-color:var(--ink-4);color:var(--fg);}
.sug-f.on{background:var(--acc);border-color:var(--acc);color:var(--on-acc);}

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
/* ---- phone: the tab strip becomes a bottom bar ---- */
@media(max-width:760px){
  .tabs{position:fixed;inset-inline:0;inset-block-end:0;z-index:150;margin:0;gap:0;
    display:grid;grid-template-columns:repeat(6,1fr);overflow:visible;
    background:var(--bar-bg);backdrop-filter:blur(14px);
    border-top:1px solid var(--ink-2);border-bottom:0;
    padding-bottom:env(safe-area-inset-bottom);}
  .tab{flex-direction:column;gap:3px;justify-content:center;min-height:56px;
    padding:8px 2px 7px;font-size:10px;letter-spacing:-.01em;overflow:hidden;}
  .tab span{max-width:100%;overflow:hidden;text-overflow:ellipsis;}
  .tab svg{width:20px;height:20px;}
  .tab.on{color:var(--acc);}
  .tab.on::after{inset-block-start:0;inset-block-end:auto;inset-inline:14%;height:2px;border-radius:0 0 3px 3px;}
  #app{padding-block-end:calc(78px + env(safe-area-inset-bottom));}
  .toast{inset-block-end:calc(74px + env(safe-area-inset-bottom));}
  .tipcard{inset-block-end:calc(120px + env(safe-area-inset-bottom));}
  .ch-areas{grid-template-columns:repeat(2,1fr);}
  body.in-app .sticky-cta{display:none;}
}
@media(max-width:360px){
  .tab{font-size:9px;}
  .tab svg{width:18px;height:18px;}
}

/* ---- phone: the rest ---- */
@media(max-width:520px){
  .dash-grid{grid-template-columns:repeat(2,1fr);}
  .dstat .dv{font-size:23px;}
  .scgrid{grid-template-columns:1fr;}
  .lsgrid{grid-template-columns:1fr;}
  .achgrid{grid-template-columns:1fr;}
  .next{padding:var(--s4);}
  .next-btns .btn{min-width:100%;}
  .pro-num{font-size:42px;}
  .pro-score{padding:var(--s4);}
  .rung{gap:var(--s2);}
  .rung-k{min-width:100%;}
  .rung-in{min-width:100%;}
  .qz-q{min-height:0;}
  .qz-opt{padding:var(--s3);font-size:var(--t-sm);}
  /* the weekly-mission composer has four controls; stacked they stay tappable */
  #page-progress .addrow{flex-wrap:wrap;}
  #page-progress .addrow input[type=text]{flex:1 1 100%;}
  #page-progress .addrow select{max-width:none!important;flex:1;}
  .mini-ladder div{flex-direction:column;gap:2px;}
  .mini-ladder span{min-width:0;}
}

@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important;}
}

/* ============ CHECK-IN: AGE + MULTI ============ */
.qz-agefield{margin-top:var(--s4);}
.qz-agefield input{width:100%;font-size:var(--t-h2);text-align:center;font-variant-numeric:tabular-nums;}
.qz-multi{display:flex;align-items:center;gap:var(--s2);margin:calc(var(--s2) * -1) 0 var(--s3);color:var(--acc);}
.qz-multi .ic{width:15px;height:15px;flex:0 0 auto;}
/* a multi option stays lit and reads as a checkbox, so two taps look deliberate */
.qz-opt.multi .qz-let{border-radius:var(--r-ctl);}
.qz-opt.multi .qz-tick{opacity:.25;}
.qz-opt.multi.on .qz-tick{opacity:1;}
.qz-foot{display:flex;align-items:center;gap:var(--s2);}
.qz-foot #qzNext{margin-inline-start:auto;width:auto;flex:0 0 auto;}
/* what the check-in already told us, offered rather than imposed */
.opt.sug{border-color:var(--acc);}
.sug-dot{width:6px;height:6px;border-radius:var(--r-pill);background:var(--acc);
  flex:0 0 auto;margin-inline-start:auto;}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0;}

/* ============ HERO LINE ============ */
.hero-line{font-family:var(--f-display);font-size:clamp(20px,4.4vw,28px);line-height:1.25;
  color:var(--acc);margin:var(--s3) 0 var(--s2);letter-spacing:-.01em;}

.contact-line a{color:var(--acc);text-decoration:underline;text-underline-offset:2px;
  word-break:break-all;}

/* ============ PRO LOCKS ============ */
.lockwrap{padding:var(--s4) 0;}
.lockcard{background:var(--ink-1);border:1px solid var(--ink-3);border-radius:var(--r-card);
  padding:var(--s6) var(--s4);text-align:center;display:flex;flex-direction:column;
  align-items:center;gap:var(--s3);}
.lockcard .ic{width:28px;height:28px;color:var(--acc);}
.lockcard h3{font-size:var(--t-h3);}
.lockcard p{color:var(--fg-2);font-size:var(--t-sm);max-width:34ch;line-height:1.55;}
.lockcard .btn{width:auto;min-width:180px;}
.ic.mini{width:14px;height:14px;opacity:.7;margin-inline-start:var(--s1);}

/* ============ LICENCE ============ */
.lic{margin-top:var(--s3);text-align:start;background:var(--ink-2);
  border:1px solid var(--ink-3);border-radius:var(--r-ctl);padding:var(--s3);}
.lic>summary{cursor:pointer;font-size:var(--t-sm);color:var(--fg-2);}
.lic-row{display:flex;gap:var(--s2);margin-top:var(--s2);}
.lic-row input{flex:1;min-width:0;background:var(--ink-1);border:1px solid var(--ink-3);
  color:var(--fg);border-radius:var(--r-ctl);padding:10px var(--s3);font:inherit;font-size:var(--t-sm);}
.lic-row .btn{width:auto;flex:0 0 auto;}
.lic-state{font-size:var(--t-sm);color:var(--fg-2);margin-top:var(--s2);text-align:center;}
.lic-state.pro,.lic-state.founder{color:var(--acc);}

/* ============ BACKUP ============ */
.bk-row{display:flex;gap:var(--s2);flex-wrap:wrap;}
.bk-row .btn{width:auto;flex:1 1 auto;min-width:140px;cursor:pointer;}

/* ============ INSTALL STRIP ============ */
.installbar{display:none;align-items:center;gap:var(--s2);background:var(--acc-dim);
  border:1px solid var(--acc);border-radius:var(--r-ctl);padding:10px var(--s3);
  margin-bottom:var(--s3);font-size:var(--t-sm);}
.installbar.on{display:flex;}
.installbar .ic{width:18px;height:18px;color:var(--acc);flex:0 0 auto;}
.installbar span{flex:1;min-width:0;}
.installbar button{background:var(--acc);color:var(--on-acc);border:0;border-radius:var(--r-pill);
  padding:6px 14px;font:inherit;font-size:var(--t-xs);font-weight:700;cursor:pointer;flex:0 0 auto;}
.installbar button.x{background:transparent;color:var(--fg-3);padding:6px 8px;font-weight:500;}

/* ============ GOAL LIFECYCLE ============ */
.gtools{display:flex;gap:var(--s2);flex-wrap:wrap;margin-top:var(--s3);}
.gtools .btn{width:auto;flex:0 1 auto;}
.goal.paused{opacity:.72;}
.goal.archived{opacity:.8;}
.goal.archived h3 .ic{color:var(--ok);}
.gstate.off{color:var(--fg-3);}
.gstate.done{color:var(--ok);}

/* ============ TREND ============
   One series, so no legend: the heading names it. Grid and axis stay recessive,
   the numbers wear text tokens, and only the two end points are labelled. */
.trendbox{position:relative;}
.trend-head{display:flex;align-items:baseline;gap:var(--s2);font-size:var(--t-sm);
  color:var(--fg-2);margin-bottom:var(--s2);}
.trend-delta{font-weight:800;font-size:var(--t-h3);color:var(--fg-3);font-variant-numeric:tabular-nums;}
.trend-delta.up{color:var(--ok);} .trend-delta.down{color:var(--fg-3);}
svg.trend{width:100%;height:auto;display:block;overflow:visible;}
svg.trend .tg{stroke:var(--ink-3);stroke-width:1;}
svg.trend .tl{fill:var(--fg-3);font-size:9px;font-family:var(--f-ui);}
svg.trend .tv{fill:var(--fg-2);font-size:11px;font-weight:700;font-family:var(--f-ui);}
svg.trend .tline{fill:none;stroke:var(--acc);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
svg.trend .td{fill:var(--ink-1);stroke:var(--acc);stroke-width:2;}
svg.trend .td.edge{fill:var(--acc);}
svg.trend .td.hot{fill:var(--acc-hi);stroke:var(--acc-hi);r:5.5;}
.trend-tip{position:absolute;top:0;transform:translateX(-50%);background:var(--ink-0);
  border:1px solid var(--ink-3);border-radius:var(--r-ctl);padding:4px 8px;
  font-size:var(--t-xs);color:var(--fg);white-space:nowrap;pointer-events:none;}
.dimdelta{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));
  gap:var(--s2);margin:var(--s3) 0 var(--s2);}
.dd{background:var(--ink-2);border-radius:var(--r-ctl);padding:var(--s2);text-align:center;}
.dd-k{display:block;font-size:var(--t-xs);color:var(--fg-3);margin-bottom:2px;}
.dd-v{font-weight:800;font-variant-numeric:tabular-nums;color:var(--fg-3);}
.dd-v.up{color:var(--ok);} .dd-v.down{color:var(--fg-2);}

@media (max-width:380px){
  .bk-row .btn{min-width:100%;}
  .lic-row{flex-direction:column;}
  .lic-row .btn{width:100%;}
}

"""
