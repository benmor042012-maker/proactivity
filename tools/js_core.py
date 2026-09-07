# -*- coding: utf-8 -*-
"""i18n runtime, data tables, workout/skincare builders."""

JS_CORE = r"""
/* ================= i18n runtime ================= */
var LANGS=['he','en','fr','ru','ar'], RTL={he:1,ar:1};
var cur = (function(){ try{var s=localStorage.getItem('proactive_lang');
  if(s&&I18N[s])return s;}catch(e){}
  var n=(navigator.language||'he').slice(0,2); return I18N[n]?n:'he'; })();

/* Grammatical gender lives INSIDE the string as {masculine|feminine} rather than
   in a parallel set of keys: '{אתה|את} {מתחיל|מתחילה}', 'בחר{|י}', 'prêt{|e}',
   'выбрал{|а}'. One string per key, so the two forms can never drift apart, and
   English simply contains no segments.

   ORDER MATTERS, and it is the opposite of what looks natural. Gender resolves
   FIRST, on the raw string straight out of the table, and only then are
   {placeholder} values substituted in. Several call sites pass text the user
   typed - a name, a goal title, a custom category - and if gender ran last, a
   user who typed "{a|b}" would have one of their own branches silently deleted.
   Resolving first is safe because a branch may not contain a brace, so no
   placeholder can ever hide inside one.

   Never resolve anywhere but here. esc() does not escape braces, so running
   this over an already-assembled HTML string could let one match span an
   attribute boundary. On the raw table string, before interpolation, it cannot. */
var GSEG=/\{([^{}|]*)\|([^{}|]*)\}/g;
var GENDERS=['m','f','n'];
var gnd=(function(){ try{
  var g=localStorage.getItem('proactive_gender');
  return GENDERS.indexOf(g)>=0 ? g : '';
}catch(e){ return ''; } })();

/* Hebrew and Arabic have no neutral second person. When the user has not said,
   the honest render is the slash form Israeli interfaces actually use -
   מתחיל/ה, בחר/י - built by keeping the shared prefix and appending only the
   part that differs. */
function gmerge(m,f){
  if(m===f) return m;
  if(!m) return f;
  if(!f) return m;
  var i=0;
  while(i<m.length && i<f.length && m.charAt(i)===f.charAt(i)) i++;
  var tail=f.slice(i);
  return (i>0 && tail && tail.length<=2) ? m+'/'+tail : m+'/'+f;
}
function gres(s){
  if(s.indexOf('|')<0) return s;
  return s.replace(GSEG, function(_,m,f){
    return gnd==='f' ? f : gnd==='m' ? m : gmerge(m,f);
  });
}
function t(k,vars){
  var s=(I18N[cur]&&I18N[cur][k]);
  if(s===undefined) s=(I18N.he&&I18N.he[k]);
  if(s===undefined) return k;
  s=gres(s);
  if(vars) for(var v in vars) s=s.split('{'+v+'}').join(vars[v]);
  return s;
}
function esc(s){var d=document.createElement('div');d.textContent=String(s==null?'':s);return d.innerHTML;}
function ic(n,cls){return '<svg class="ic'+(cls?' '+cls:'')+'" aria-hidden="true"><use href="#i-'+n+'"></use></svg>';}

function applyLang(){
  var dir = RTL[cur] ? 'rtl' : 'ltr';
  document.documentElement.lang = cur;
  document.documentElement.dir  = dir;
  document.querySelectorAll('.langbtn').forEach(function(b){ b.classList.toggle('on', b.dataset.lang===cur); });
  document.querySelectorAll('[data-i18n]').forEach(function(el){ el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll('[data-i18n-html]').forEach(function(el){ el.innerHTML = t(el.dataset.i18nHtml); });
  document.querySelectorAll('[data-i18n-ph]').forEach(function(el){ el.placeholder = t(el.dataset.i18nPh); });
  document.querySelectorAll('[data-i18n-title]').forEach(function(el){
    var s=t(el.dataset.i18nTitle); el.title=s; el.setAttribute('aria-label',s);
  });
  var mb=document.getElementById('modeBtn');
  if(mb) mb.setAttribute('data-i18n-title', activeTheme()==='light' ? 'th.dark' : 'th.light');
  document.title = t('seo.title');
  var md=document.querySelector('meta[name="description"]');
  if(md) md.setAttribute('content', t('seo.desc'));
  renderPrices();
}
/* Everything drawn by JS must be redrawn, not just the [data-i18n] nodes.
   Language and gender both change every string on screen, so they share one
   path rather than each remembering its own list of things to repaint. */
function redrawAll(){
  applyLang();
  if(document.getElementById('app').style.display==='block') startApp();
  if(document.getElementById('onboarding').style.display==='block'){
    renderGoalOpts(); markSelected(); renderBuilt(); showStep(os);
  }
}
function setLang(l){
  if(!I18N[l]) return;
  cur = l;
  try{ localStorage.setItem('proactive_lang', l); }catch(e){}
  redrawAll();
}
function setGender(g){
  if(GENDERS.indexOf(g)<0) return;
  gnd = g;
  P.gender = g;
  try{ localStorage.setItem('proactive_gender', g); }catch(e){}
  redrawAll();
}
/* '' means never asked, and reads as the neutral slash form. */
function genderValue(){ return GENDERS.indexOf(gnd)>=0 ? gnd : 'n'; }

/* ================= data ================= */
var ALL_CATS=[
 {id:'study',  icon:'book',    k:'cat.study',   dk:'dt.study',   sg:['sg.study.1','sg.study.2','sg.study.3','sg.study.4']},
 {id:'sport',  icon:'activity',k:'cat.sport',   dk:'dt.sport',   sg:['sg.sport.1','sg.sport.2','sg.sport.3','sg.sport.4']},
 {id:'friends',icon:'users',   k:'cat.friends', dk:'dt.friends', sg:['sg.friends.1','sg.friends.2','sg.friends.3']},
 {id:'sleep',  icon:'moon',    k:'cat.sleep',   dk:'dt.sleep',   sg:['sg.sleep.1','sg.sleep.2','sg.sleep.3']},
 {id:'money',  icon:'wallet',  k:'cat.money',   dk:'dt.money',   sg:['sg.money.1','sg.money.2','sg.money.3']},
 {id:'food',   icon:'apple',   k:'cat.food',    dk:'dt.food',    sg:['sg.food.1','sg.food.2','sg.food.3']},
 {id:'hobby',  icon:'palette', k:'cat.hobby',   dk:'dt.hobby',   sg:['sg.hobby.1','sg.hobby.2','sg.hobby.3']}
];
var STAGES=[{min:0,k:'st.1'},{min:300,k:'st.2'},{min:700,k:'st.3'},{min:1200,k:'st.4'},{min:2000,k:'st.5'}];
var QUOTES=['q.1','q.2','q.3','q.4','q.5','q.6','q.7'];
var PRAISE=['p.1','p.2','p.3','p.4','p.5'];
var INSIGHTS=[{t:'in.1.t',s:'in.1.s'},{t:'in.2.t',s:'in.2.s'},{t:'in.3.t',s:'in.3.s'},{t:'in.4.t',s:'in.4.s'}];
var CHALLENGES=[
 {t:'ch.1',th:'ch.th.reg'},{t:'ch.2',th:'ch.th.goal'},{t:'ch.3',th:'ch.th.reg'},
 {t:'ch.4',th:'ch.th.broad'},{t:'ch.5',th:'ch.th.broad'}];
var TRAITS=['tr.wake','tr.hw','tr.eat','tr.train','tr.social','tr.sleep','tr.save','tr.read','tr.time','tr.init','tr.groom','tr.water'];
var THEORIES=[
 {icon:'shield',  n:'th.1.n',a:'th.1.a',p:'th.1.p',h:'th.1.h',f:'th.1.f'},
 {icon:'compass', n:'th.2.n',a:'th.2.a',p:'th.2.p',h:'th.2.h',f:'th.2.f'},
 {icon:'sun',     n:'th.3.n',a:'th.3.a',p:'th.3.p',h:'th.3.h',f:'th.3.f'},
 {icon:'sliders', n:'th.4.n',a:'th.4.a',p:'th.4.p',h:'th.4.h',f:'th.4.f'},
 {icon:'target',  n:'th.5.n',a:'th.5.a',p:'th.5.p',h:'th.5.h',f:'th.5.f'},
 {icon:'rocket',  n:'th.6.n',a:'th.6.a',p:'th.6.p',h:'th.6.h',f:'th.6.f'},
 {icon:'seedling',n:'th.7.n',a:'th.7.a',p:'th.7.p',h:'th.7.h',f:'th.7.f'},
 {icon:'ruler',   n:'th.8.n',a:'th.8.a',p:'th.8.p',h:'th.8.h',f:'th.8.f'}];

/* Goal breakdown. Keywords are per-language so matching works in every language,
   not only Hebrew the way the old GOAL_MAP did. */
var GOAL_MAP=[
 {kw:{he:['אנגלית','שפה'],en:['english','language'],fr:['anglais','langue'],ru:['англ','язык'],ar:['انجليز','إنجليز','لغة']},
  steps:['gm.eng.1','gm.eng.2','gm.eng.3','gm.eng.4']},
 {kw:{he:['להתאמן','כושר','ספורט','שריר'],en:['train','fit','gym','sport','muscle','strong'],fr:['sport','muscl','forme','entra'],ru:['трениров','спорт','форм','мышц'],ar:['تمرين','رياض','لياقة','عضل']},
  steps:['gm.fit.1','gm.fit.2','gm.fit.3','gm.fit.4']},
 {kw:{he:['תכנות','קוד','מחשב'],en:['cod','program','develop','software'],fr:['cod','program','développ'],ru:['программ','код','разраб'],ar:['برمج','كود']},
  steps:['gm.code.1','gm.code.2','gm.code.3','gm.code.4']},
 {kw:{he:['זמן','סדר','ארגון'],en:['time','organis','organiz','schedul','productiv'],fr:['temps','organis','planifi'],ru:['врем','организ','планир'],ar:['وقت','تنظيم','ترتيب']},
  steps:['gm.time.1','gm.time.2','gm.time.3']},
 {kw:{he:['חבר','חברת','חברים','חברותי'],en:['friend','social','people'],fr:['ami','social'],ru:['друз','общен','социал'],ar:['صديق','أصدقاء','اجتماع']},
  steps:['gm.soc.1','gm.soc.2','gm.soc.3']},
 {kw:{he:['בריא','אוכל','תזונה'],en:['health','eat','food','diet','nutrition'],fr:['sant','manger','aliment','nutrition'],ru:['здоров','пита','ед'],ar:['صح','أكل','تغذية','طعام']},
  steps:['gm.heal.1','gm.heal.2','gm.heal.3']},
 {kw:{he:['לישון','שינה','לקום'],en:['sleep','wake','bed','rest'],fr:['dormir','sommeil','coucher','lever'],ru:['сон','спать','высып','вста'],ar:['نوم','أنام','استيقاظ']},
  steps:['gm.slp.1','gm.slp.2','gm.slp.3']}
];
function guessSteps(g){
  var s=String(g||'').toLowerCase();
  for(var i=0;i<GOAL_MAP.length;i++){
    var e=GOAL_MAP[i];
    for(var L in e.kw){
      var list=e.kw[L];
      for(var j=0;j<list.length;j++) if(s.indexOf(list[j])>=0) return e.steps.slice();
    }
  }
  return ['gm.def.1','gm.def.2','gm.def.3','gm.def.4'];
}

/* ================= age ================= */
/* The check-in asks a 14-year-old about school and a 40-year-old about work, so
   the band picks the wording. It is derived from P.age at render time and never
   cached: the user can go back from the questions, change their age, and come
   forward again, and the questions have to follow. */
var QBANDS=['a13','a18','a30','a50'];
function ageBand(a){
  var n=Number(a);
  if(!n || n<13) return 'a13';
  if(n<=17) return 'a13';
  if(n<=29) return 'a18';
  if(n<=49) return 'a30';
  return 'a50';
}

/* ================= workout builder ================= */
function reps(sets,n,unit){ return sets+'×'+n+(unit?' '+unit:''); }
function secs(n){ return n+' '+t('c.sec'); }
function mins(n){ return n+' '+t('c.min'); }

/* Two independent axes, where there used to be one "band" capped at 17-18.

   variant picks WHICH exercises (it still feeds every y / m2 / o ternary below,
   so none of the plan literals change); x scales HOW MUCH. Splitting them is
   what lets the plan serve a 70-year-old: 'young' is already the low-impact
   branch - knee push-ups, table rows, static lunges, fast squats instead of
   burpees - which is the right regression for a deconditioned older body, not
   just for a small one. A 13-18 year old gets exactly what they got before. */
function fitProfile(age){
  var a=Math.min(120, Math.max(13, Number(age)||15));
  if(a<=14) return {variant:'young', x:0.70, noteKey:'wo.n.a13', bandKey:'fb.a13'};
  if(a<=17) return {variant:'mid',   x:0.90, noteKey:'wo.n.a15', bandKey:'fb.a15'};
  if(a<=29) return {variant:'older', x:1.00, noteKey:'wo.n.a18', bandKey:'fb.a18'};
  if(a<=49) return {variant:'older', x:0.95, noteKey:'wo.n.a30', bandKey:'fb.a30'};
  if(a<=64) return {variant:'mid',   x:0.85, noteKey:'wo.n.a50', bandKey:'fb.a50'};
  return             {variant:'young', x:0.60, noteKey:'wo.n.a65', bandKey:'fb.a65'};
}
function buildWorkout(age,goal,level){
  var F=fitProfile(age), band=F.variant;
  /* Nobody over 50 gets handed four sets of burpees and pull-ups because they
     once ticked "experienced". Capping the level is the safer default. */
  if(Number(age)>=50 && level==='inter') level='basic';
  var R = ({beginner:{s:8,m:10,l:12,sets:2,hold:20},
            basic:   {s:10,m:12,l:15,sets:3,hold:30},
            inter:   {s:12,m:15,l:20,sets:4,hold:45}})[level] || {s:8,m:10,l:12,sets:2,hold:20};
  var band_x = F.x;
  var noteKey = F.noteKey;
  var restTxt = level==='inter' ? secs(60) : secs(90);
  var subRest = t('wo.s.rest',{r:restTxt});
  var y = band==='young', m2 = band==='mid', o = band==='older';
  var S=R.sets, perleg=t('c.perleg'), perside=t('c.perside');

  function E(k,r,cue){ return {k:k, r:r, d:cue||''}; }
  function D(k,sub,items){ return {k:k, sub:sub||'', items:items}; }

  var plans = {
    strength:[
      D('wo.d.chest', t(noteKey)+' '+subRest, [
        E(y?'ex.pushup.k':(o?'ex.pushup.w':'ex.pushup'), reps(S,y?R.s:R.m), t('cue.shwidth')),
        E(y?'ex.shoulderpr':'ex.diamond', reps(S,R.s), t('cue.triceps')),
        E(y?'ex.dips.chair':'ex.dips', reps(S,R.m)),
        E('ex.plank', secs(R.hold), t('cue.straight'))]),
      D('wo.d.legsf', subRest, [
        E(o?'ex.squat.w':'ex.squat', reps(S,R.l), o?t('cue.weight'):t('cue.deep')),
        E(y?'ex.lunge.stat':(m2?'ex.lunge.walk':'ex.lunge.bulg'), reps(S,R.m,perleg)),
        E('ex.calf', reps(S,R.l), t('cue.slowup')),
        E('ex.wallsit', secs(R.hold), t('cue.knee90'))]),
      D('wo.d.back', subRest, [
        E(y?'ex.row.table':'ex.pullup', reps(S,y?R.s:R.m), y?t('cue.undertab'):''),
        E(y?'ex.superman':'ex.band.row', reps(S,R.m)),
        E('ex.curl', reps(S,R.m)),
        E('ex.plank.side', reps(2,secs(Math.round(R.hold*.7))))]),
      D('wo.d.hiit', t('wo.s.3030'), [
        E('ex.jack', reps(S,R.l)),
        E(y?'ex.squat.fast':'ex.burpee', reps(S,R.s)),
        E('ex.highknee', reps(S,mins(1))),
        E('ex.mountain', reps(S,R.m), t('cue.kneechest'))]),
      D('wo.d.arms', subRest, [
        E('ex.shoulderpr', reps(S,R.m)),
        E('ex.latraise', reps(S,R.m), t('cue.armsout')),
        E('ex.dips.close', reps(S,R.m), t('cue.triceps')),
        E('ex.curl.hammer', reps(S,R.m), t('cue.thumbsup'))]),
      D('wo.d.legsb', '', [
        E(m2?'ex.bridge.one':'ex.bridge', reps(S,R.l), t('cue.hips')),
        E(o?'ex.rdl':'ex.squat.jump', reps(S,R.m)),
        E('ex.crunch', reps(S,R.m)),
        E('ex.legraise', reps(S,R.s)),
        E('ex.plank', secs(R.hold))]),
      D('wo.d.recov', t('wo.s.light'), [
        E('ex.stretch', mins(10), t('cue.each20')),
        E('ex.foamroll', mins(5), t('cue.sore')),
        E('ex.breathe', 10+' '+t('c.breaths'), t('cue.478')),
        E('ex.walk.light', mins(Math.round(15*band_x)), t('cue.noeffort'))])
    ],
    cardio:[
      D('wo.d.run', t(noteKey), [
        E('ex.warmup', mins(Math.round(5*band_x))),
        E('ex.run', mins(Math.round(20*band_x)), t('cue.comfort')),
        E('ex.sprint', reps(y?3:S, secs(30)), t('cue.rest60')),
        E('ex.cooldown', mins(5))]),
      D('wo.d.upper','',[E('ex.pushup',reps(S,R.m)),E('ex.dips',reps(S,R.s)),E('ex.plank',secs(R.hold))]),
      D('wo.d.hiit', t('wo.s.3030'), [
        E('ex.jack',reps(S,R.l)), E(y?'ex.squat.fast':'ex.burpee',reps(S,R.s)),
        E('ex.highknee',reps(S,mins(1))), E('ex.mountain',reps(S,R.m))]),
      D('wo.d.lower','',[E('ex.squat',reps(S,R.l)),E('ex.lunge',reps(S,R.m,perleg)),
        E('ex.bridge',reps(S,R.l)),E('ex.wallsit',secs(R.hold))]),
      D('wo.d.long','',[E('ex.warmup',mins(5)),
        E('ex.run.steady',mins(Math.round(30*band_x)),t('cue.steady')),E('ex.cooldown',mins(5))]),
      D('wo.d.core','',[E('ex.crunch',reps(S,R.m)),E('ex.superman',reps(S,R.m)),
        E('ex.plank.side',reps(2,secs(Math.round(R.hold*.7)))),E('ex.stretch',mins(10))]),
      D('wo.d.rest', t('wo.s.easy'), [E('ex.walk',mins(Math.round(20*band_x))),
        E('ex.stretch',mins(10)),E('ex.breathe',10+' '+t('c.breaths'))])
    ],
    flex:[
      D('wo.d.yoga1', t(noteKey), [
        E('ex.sun', Math.round(5*band_x)+' '+t('c.rounds')),
        E('ex.warrior1', secs(30)+' '+perside), E('ex.downdog', mins(1)),
        E('ex.breathe', 10+' '+t('c.breaths'), t('cue.478'))]),
      D('wo.d.strlow', t('wo.s.hold30'), [
        E('ex.st.ham', reps(2,secs(30),perleg)), E('ex.st.quad', reps(2,secs(30),perleg)),
        E('ex.st.hip', reps(2,secs(30)))]),
      D('wo.d.balance','',[E('ex.plank',secs(R.hold)),
        E('ex.oneleg',reps(2,secs(30),perleg)), E('ex.tree',reps(2,secs(20),perside)),
        E('ex.squat.slow',reps(S,R.s),t('cue.5down'))]),
      D('wo.d.strup','',[E('ex.st.shoulder',reps(2,secs(30))),
        E('ex.st.chest',reps(2,secs(30)),t('cue.behind')),
        E('ex.st.backtw',reps(2,secs(30),perside)), E('ex.st.neck','10')]),
      D('wo.d.yoga2','',[E('ex.sun.b',Math.round(5*band_x)+' '+t('c.rounds')),
        E('ex.warrior23',secs(30)+' '+perside), E('ex.pigeon',secs(30)+' '+perside),
        E('ex.bridgepose',reps(3,secs(15)))]),
      D('wo.d.free','',[E('ex.flow',mins(15),t('cue.natural')),E('ex.stretch',mins(10))]),
      D('wo.d.rest','',[E('ex.walk',mins(Math.round(20*band_x))),E('ex.meditate',mins(5))])
    ],
    general:[
      D('wo.d.move', t(noteKey), [E('ex.walk',mins(Math.round(20*band_x)),t('cue.nophone')),
        E('ex.stretch',mins(5)), E('ex.dance',mins(Math.round(10*band_x)))]),
      D('wo.d.upper','',[E('ex.pushup',reps(S,R.s)),E('ex.dips',reps(S,R.s)),E('ex.plank',secs(R.hold))]),
      D('wo.d.cardio','',[E('ex.runwalk',mins(Math.round(20*band_x))),E('ex.jack',reps(S,R.l))]),
      D('wo.d.lower','',[E('ex.squat',reps(S,R.m)),E('ex.lunge',reps(S,R.s,perleg)),E('ex.bridge',reps(S,R.l))]),
      D('wo.d.core','',[E('ex.crunch',reps(S,R.m)),E('ex.plank',secs(R.hold)),E('ex.superman',reps(S,R.m))]),
      D('wo.d.fun','',[E('ex.dance',mins(Math.round(30*band_x)),t('cue.anysport')),E('ex.stretch',mins(5))]),
      D('wo.d.rest', t('wo.s.easy'), [E('ex.walk.nature',mins(Math.round(20*band_x))),E('ex.stretch',mins(10))])
    ]
  };
  return { blocks: plans[goal]||plans.general,
           levelKey:'fl.'+(level==='inter'?'inter':level==='basic'?'basic':'beginner'),
           ageBandKey: F.bandKey,      // a translation key, not the literal "17-18"
           note: t(noteKey) };
}

/* ================= skincare + hygiene ================= */
function buildSkin(type){
  var base = (type==='dunno') ? 'normal' : type;
  var cl = t('sk.cl.'+(({normal:1,oily:1,dry:1,combo:1})[base]?base:'normal'));
  var mo = t('sk.mo.'+(({normal:1,oily:1,dry:1,combo:1})[base]?base:'normal'));
  var typeName = t('sk.type.'+(({normal:1,oily:1,dry:1,combo:1,dunno:1})[type]?type:'normal'));
  return [
   {label:t('sk.d.morning'), sub:t('sk.s.morning'), items:[
     {n:t('sk.i.cleanse',{x:cl}), cam:true,  d:t('sk.c.lukewarm')},
     {n:t('sk.i.moist',{x:mo}),   cam:true,  d:t('sk.c.damp')},
     {n:t('sk.i.spf'),            cam:false, d:t('sk.c.winter')}]},
   {label:t('sk.d.evening'), sub:t('sk.s.evening'), items:[
     {n:t('sk.i.micellar'),       cam:false, d:t('sk.c.dirt')},
     {n:t('sk.i.cleanse',{x:cl}), cam:true,  d:t('sk.c.deep')},
     {n:t('sk.i.moist',{x:mo}),   cam:false, d:t('sk.c.clean')}]},
   {label:t('sk.d.weekly'), sub:t('sk.s.weekly',{type:typeName}), items:[
     {n:base==='oily'?t('sk.i.mask.oily'):t('sk.i.mask.hyd'), cam:true,
      d:base==='oily'?t('sk.c.oilctrl'):t('sk.c.nourish')},
     {n:t('sk.i.peel'), cam:false, d:t('sk.c.circles')}]}
  ];
}
function buildHygiene(){
  return [
   {label:t('hy.d.morning'), sub:'', items:[
     {n:t('hy.water'), cam:true,  d:t('hy.water.c')},
     {n:t('hy.teeth'), cam:false, d:''},
     {n:t('hy.breakfast'), cam:true, d:''}]},
   {label:t('hy.d.evening'), sub:'', items:[
     {n:t('hy.shower'), cam:false, d:''},
     {n:t('hy.floss'),  cam:false, d:''},
     {n:t('hy.phone'),  cam:true,  d:''}]},
   {label:t('hy.d.weekly'), sub:'', items:[
     {n:t('hy.nails'), cam:false, d:''},
     {n:t('hy.hair'),  cam:false, d:''},
     {n:t('hy.laundry'), cam:true, d:''}]}
  ];
}
"""
