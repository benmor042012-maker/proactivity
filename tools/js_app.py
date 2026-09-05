# -*- coding: utf-8 -*-
JS_APP = r"""
/* ================= state ================= */
var P={name:'',age:'15',email:'',goals:['study','sport','sleep','food'],customCats:[],
       diff:'mid',workout:'general',fitLevel:'beginner',time:'30',actPref:'mix',
       easy:[],hard:[],dream:'',skinType:'normal',userGoals:[],
       plan:null, trialStart:null,
       gender:'', accent:'mint', theme:''};   // theme '' = follow the device
var S={points:0,streak:0,chDone:false,tasks:[],missions:[],plan:{},goals:[]};
var CATS=[], uid=1;

/* ================= theme ================= */
/* The gender answer only picks a DEFAULT accent - the top bar can change it
   at any time, so nobody is locked into a colour. */
var ACCENTS=['flame','bloom','mint'];
var GENDER_ACCENT={boy:'flame', girl:'bloom', na:'mint'};

function prefersLight(){
  try{ return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches; }
  catch(e){ return false; }
}
function activeTheme(){ return P.theme || (prefersLight() ? 'light' : 'dark'); }

function applyTheme(){
  var d=document.documentElement;
  d.setAttribute('data-theme', activeTheme());
  d.setAttribute('data-accent', ACCENTS.indexOf(P.accent)>=0 ? P.accent : 'mint');
  document.querySelectorAll('[data-set-accent]').forEach(function(b){
    b.classList.toggle('on', b.dataset.setAccent===P.accent);
  });
  var mb=document.getElementById('modeBtn');
  if(mb) mb.classList.toggle('is-light', activeTheme()==='light');
  var meta=document.querySelector('meta[name="theme-color"]');
  if(meta) meta.setAttribute('content', activeTheme()==='light' ? '#FBF9F5' : '#14161C');
}
/* Appearance is stored under its own keys, not inside the profile: the profile
   is only written once onboarding completes, and a colour picked on the landing
   page must still survive a refresh. */
function saveLook(){
  try{
    localStorage.setItem('proactive_accent', P.accent||'mint');
    localStorage.setItem('proactive_theme', P.theme||'');
  }catch(e){}
}
function loadLook(){
  try{
    var a=localStorage.getItem('proactive_accent');
    if(ACCENTS.indexOf(a)>=0) P.accent=a;
    var th=localStorage.getItem('proactive_theme');
    if(th==='light'||th==='dark'||th==='') P.theme=th||'';
  }catch(e){}
}
function setAccent(a){
  if(ACCENTS.indexOf(a)<0) return;
  P.accent=a; saveLook(); applyTheme(); redrawColoured();
}
function setTheme(mode){ P.theme=mode; saveLook(); applyTheme(); redrawColoured(); }

/* the progress ring paints with real colour values, so it has to be redrawn
   whenever the palette changes */
function redrawColoured(){
  if(document.getElementById('app').style.display==='block'){ renderRing(); renderMini(); }
}
function cssVar(name){
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

document.addEventListener('click',function(e){
  var a=e.target.closest('[data-set-accent]');
  if(a){ setAccent(a.dataset.setAccent); return; }
  var m=e.target.closest('#modeBtn');
  if(m){ setTheme(activeTheme()==='light' ? 'dark' : 'light'); }
});

/* Local calendar day, not UTC - with UTC the day would roll over at the wrong
   hour and break every streak for anyone not on GMT. */
function dayKey(d){
  d = d || new Date();
  return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
}
function daysBetween(a,b){
  return Math.round((new Date(b+'T00:00:00') - new Date(a+'T00:00:00'))/86400000);
}
/* Shared by the sport and skincare mini-apps: same day is a no-op, yesterday
   extends the run, any longer gap starts over. */
function bumpStreak(o,day){
  day = day || dayKey();
  if(o.lastDay === day) return o.streak;
  o.streak = (o.lastDay && daysBetween(o.lastDay, day) === 1) ? (o.streak||0)+1 : 1;
  o.lastDay = day;
  return o.streak;
}
/* A run that was broken before today should read as 0, not as its stale value. */
function liveStreak(o){
  if(!o || !o.lastDay) return 0;
  var gap = daysBetween(o.lastDay, dayKey());
  return (gap === 0 || gap === 1) ? (o.streak||0) : 0;
}

function emptyMini(){
  return {
    view:'hub',
    sport: {sessions:[], streak:0, lastDay:null},
    skin:  {setup:null, routine:null, log:{}, streak:0, lastDay:null},
    fridge:{pantry:[], favs:[], history:[], photo:null}
  };
}

var STORE_V=3;
function save(){ try{
  saveLook();
  localStorage.setItem('proactive_v',STORE_V);
  localStorage.setItem('proactive_p',JSON.stringify(P));
  localStorage.setItem('proactive_s',JSON.stringify(S));
  localStorage.setItem('proactive_uid',uid);
}catch(e){} }

/* ids must never collide with ids already sitting in storage, whatever their
   origin - a stale counter silently makes one checkbox toggle another row. */
function reseedUid(){
  var max=0;
  function seen(n){ n=Number(n); if(n>max) max=n; }
  (S.tasks||[]).forEach(function(x){ seen(x.id); });
  (S.missions||[]).forEach(function(x){ seen(x.id); });
  (S.goals||[]).forEach(function(g){ seen(g.id); (g.actions||[]).forEach(function(a){ seen(a.id); }); });
  (P.customCats||[]).forEach(function(c){ var m=/^custom_(\d+)$/.exec(c.id||''); if(m) seen(m[1]); });
  var stored=Number(localStorage.getItem('proactive_uid'))||1;
  uid=Math.max(stored,max+1,1);
}

/* v1 stored every task, mission and category label as a hardcoded Hebrew
   string and category icons as emoji, so carrying that straight into the new
   build leaves Hebrew text in the other four languages and icon references
   that resolve to nothing. Keep the progress, rebuild the labelled parts. */
function migrateV1(){
  P.customCats=(P.customCats||[]).map(function(c){
    return {id:c.id, name:c.name, icon:'star', custom:true, sg:['sg.generic']};
  });
  P.easy=[]; P.hard=[];                 // v1 stored these as Hebrew literals
  S.tasks=[]; S.missions=[]; S.plan={}; // re-seeded below from the new schema
  S.goals=(S.goals||[]).map(function(g){
    return {id:g.id, title:g.title,     // the user typed these, so they stay
            actions:guessSteps(g.title).map(function(k){
              return {id:0,key:k,text:'',done:false};
            })};
  });
  if(!P.trialStart) P.trialStart=Date.now();
}

/* v2 predates the mini-apps. Additive only: nothing stored by v2 is touched. */
function migrateV2(){
  if(!S.mini) S.mini=emptyMini();
}

function load(){ try{
  var p=localStorage.getItem('proactive_p'), s=localStorage.getItem('proactive_s');
  if(!p||!s) return false;
  P=Object.assign(P,JSON.parse(p)); S=Object.assign(S,JSON.parse(s));
  reseedUid();                          // before anything hands out a new id
  var v=Number(localStorage.getItem('proactive_v'))||1;
  if(v<2){
    migrateV1();
    buildCats();
    seedTasks(); seedMissions();        // rebuilt in the new shape; goals kept
    S.goals.forEach(function(g){
      g.id=uid++; g.actions.forEach(function(a){ a.id=uid++; });
    });
  }
  if(v<3) migrateV2();                  // chains, so a v1 save lands on v3
  if(!S.mini) S.mini=emptyMini();       // belt and braces for a hand-edited save
  if(v<STORE_V) save();
  return true;
}catch(e){ return false; } }

function buildCats(){
  CATS = ALL_CATS.filter(function(c){ return P.goals.indexOf(c.id)>=0; });
  P.customCats.forEach(function(cc){ if(!CATS.some(function(c){return c.id===cc.id;})) CATS.push(cc); });
  if(!CATS.length) CATS = ALL_CATS.slice();
}
function catById(id){
  var all=ALL_CATS.concat(P.customCats);
  for(var i=0;i<all.length;i++) if(all[i].id===id) return all[i];
  return null;
}
function catName(c){ return c ? (c.custom ? c.name : t(c.k)) : ''; }
function pick(a){ return a[Math.floor(Math.random()*a.length)]; }

var toastT;
function toast(msg){
  var el=document.getElementById('toast');
  el.textContent=msg; el.classList.add('on');
  clearTimeout(toastT); toastT=setTimeout(function(){ el.classList.remove('on'); },2400);
}
function addPts(n){ S.points=Math.max(0,S.points+n); save(); }
function stageInfo(){
  var c=STAGES[0];
  STAGES.forEach(function(s){ if(S.points>=s.min) c=s; });
  return { stage:t(c.k), level:Math.floor(S.points/100)+1, progress:S.points%100 };
}
function praise(){ return t(pick(PRAISE)); }

/* ================= pricing ================= */
var PRICES={
  he:{sym:'₪', m:29,  y:17,  ytot:199},
  en:{sym:'$', m:7.99,y:4.99,ytot:59},
  fr:{sym:'€', m:7.99,y:4.99,ytot:59},
  ru:{sym:'₽', m:599, y:349, ytot:4190},
  ar:{sym:'$', m:7.99,y:4.99,ytot:59}
};
function money(n){
  var p=PRICES[cur]||PRICES.en;
  var s=(n%1===0)? String(n) : n.toFixed(2);
  return cur==='ru' ? (s+' '+p.sym) : (p.sym+s);
}
function renderPrices(){
  var p=PRICES[cur]||PRICES.en;
  document.querySelectorAll('[data-price]').forEach(function(el){
    el.textContent = money(el.dataset.price==='annual' ? p.y : p.m);
  });
  document.querySelectorAll('[data-bill]').forEach(function(el){
    el.textContent = el.dataset.bill==='annual'
      ? money(p.ytot)+' · '+t('l.pr.billedy')
      : t('l.pr.billedm');
  });
}
/* Checkout is a STUB. No payment provider is wired up in this project, so this
   opens an explanatory modal and grants the full trial instead of charging. */
function startCheckout(planId){
  var p=PRICES[cur]||PRICES.en;
  var label = planId==='annual'
    ? t('l.pr.annual')+' · '+money(p.ytot)
    : t('l.pr.monthly')+' · '+money(p.m);
  document.getElementById('paySoonBody').textContent = t('pay.soon.b',{plan:label});
  document.getElementById('payModal').classList.add('on');
  P.plan=planId; if(!P.trialStart) P.trialStart=Date.now(); save();
}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-buy]'); if(!b) return;
  startCheckout(b.dataset.buy);
});
document.getElementById('paySoonOk').addEventListener('click',function(){
  document.getElementById('payModal').classList.remove('on');
  if(document.getElementById('onboarding').style.display==='block'){
    finishOnboarding();                       // paid from the paywall step
  } else if(document.getElementById('app').style.display==='block'){
    renderTrial();                            // upgraded from inside the app
  } else {
    goOnboarding();                           // paid straight off the landing page
  }
});

/* ================= trial strip ================= */
var TRIAL_DAYS=14;
function trialDaysLeft(){
  if(!P.trialStart) return TRIAL_DAYS;
  var used=Math.floor((Date.now()-P.trialStart)/86400000);
  return Math.max(0, TRIAL_DAYS-used);
}
function renderTrial(){
  var bar=document.getElementById('trialBar'), n=trialDaysLeft();
  bar.classList.add('on');
  document.getElementById('trialTxt').textContent =
    n>1 ? t('trial.left',{n:n}) : n===1 ? t('trial.last') : t('trial.over');
}
document.getElementById('trialCta').addEventListener('click',function(){
  document.getElementById('app').style.display='none';
  document.getElementById('onboarding').style.display='block';
  showStep(9);
});

/* ================= landing ================= */
function goOnboarding(){
  document.getElementById('landing').style.display='none';
  document.body.classList.remove('has-sticky');
  document.getElementById('stickyCta').style.display='none';
  document.getElementById('onboarding').style.display='block';
  window.scrollTo(0,0);
  showStep(1);
}
['ctaTop','ctaBottom','ctaSticky'].forEach(function(id){
  document.getElementById(id).addEventListener('click',goOnboarding);
});
document.body.classList.add('has-sticky');

/* ================= onboarding ================= */
var os=1, TOTAL=9;
function showStep(n){
  os=n;
  document.querySelectorAll('.step').forEach(function(s){ s.classList.remove('on'); });
  var el=document.querySelector('.step[data-step="'+n+'"]');
  if(el) el.classList.add('on');
  document.getElementById('onbBar').style.width=Math.round(n/TOTAL*100)+'%';
  document.getElementById('stepCount').textContent=t('o.step',{n:n,t:TOTAL});
  if(n===9) renderBuilt();
  window.scrollTo(0,0);
}
function renderGoalOpts(){
  var box=document.getElementById('oGoals'); box.innerHTML='';
  ALL_CATS.concat(P.customCats).forEach(function(c){
    var d=document.createElement('div');
    d.className='opt'+(P.goals.indexOf(c.id)>=0?' on':'');
    d.innerHTML=ic(c.icon)+'<span>'+esc(catName(c))+'</span>';
    d.onclick=function(){
      var i=P.goals.indexOf(c.id);
      if(i>=0) P.goals.splice(i,1); else P.goals.push(c.id);
      d.classList.toggle('on');
    };
    box.appendChild(d);
  });
}
function renderChips(id,arr){
  var box=document.getElementById(id); box.innerHTML='';
  TRAITS.forEach(function(k){
    var c=document.createElement('div');
    c.className='chip'+(arr.indexOf(k)>=0?' on':'');
    c.textContent=t(k);
    c.onclick=function(){
      var i=arr.indexOf(k);
      if(i>=0) arr.splice(i,1); else arr.push(k);
      c.classList.toggle('on');
    };
    box.appendChild(c);
  });
}
function singleSelect(boxId,attr,field){
  document.querySelectorAll('#'+boxId+' .opt').forEach(function(o){
    o.addEventListener('click',function(){
      document.querySelectorAll('#'+boxId+' .opt').forEach(function(x){ x.classList.remove('on'); });
      o.classList.add('on'); P[field]=o.dataset[attr];
    });
  });
}
/* choosing here sets the default accent straight away, so the rest of the
   questionnaire is already in the user's colour */
function bindGender(){
  document.querySelectorAll('#oGender .opt').forEach(function(o){
    o.addEventListener('click',function(){
      document.querySelectorAll('#oGender .opt').forEach(function(x){ x.classList.remove('on'); });
      o.classList.add('on');
      P.gender=o.dataset.g;
      setAccent(GENDER_ACCENT[P.gender]||'mint');
    });
  });
}

function markSelected(){
  document.querySelectorAll('#oGender .opt').forEach(function(o){
    o.classList.toggle('on', o.dataset.g===P.gender);
  });
  [['oTime','time','time'],['oAP','ap','actPref'],['oWO','wo','workout'],
   ['oFL','fl','fitLevel'],['oSkin','skin','skinType'],['oDiff','diff','diff']]
  .forEach(function(x){
    document.querySelectorAll('#'+x[0]+' .opt').forEach(function(o){
      o.classList.toggle('on', o.dataset[x[1]]===P[x[2]]);
    });
  });
}
function renderBuilt(){
  var box=document.getElementById('builtList');
  box.innerHTML =
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built1',{n:Math.max(1,P.goals.length)}))+'</span></div>'+
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built2'))+'</span></div>'+
    '<div>'+ic('check')+'<span>'+esc(t('o.9.built3',{n:P.userGoals.length||1}))+'</span></div>';
}

document.querySelectorAll('[data-next]').forEach(function(b){
  b.addEventListener('click',function(){
    if(os===1){
      P.name=document.getElementById('oName').value.trim();
      P.age=document.getElementById('oAge').value;
      P.email=document.getElementById('oEmail').value.trim();
      if(!P.age){ toast(t('t.pickage')); return; }
    }
    if(os===2 && !P.goals.length){ toast(t('t.pickarea')); return; }
    showStep(os+1);
  });
});
document.querySelectorAll('[data-back]').forEach(function(b){
  b.addEventListener('click',function(){ showStep(Math.max(1,os-1)); });
});
document.getElementById('addCustom').addEventListener('click',function(){
  var inp=document.getElementById('oCustom'), v=inp.value.trim();
  if(!v) return;
  var id='custom_'+(uid++);
  P.customCats.push({id:id,name:v,icon:'star',custom:true,sg:['sg.generic']});
  P.goals.push(id); inp.value='';
  renderGoalOpts(); toast(t('t.added',{x:v}));
});
document.getElementById('oFinish').addEventListener('click',function(){
  P.dream=document.getElementById('oDream').value.trim();
  P.userGoals=[];
  ['oG1','oG2','oG3'].forEach(function(id){
    var v=document.getElementById(id).value.trim(); if(v) P.userGoals.push(v);
  });
  save(); showStep(9);
});
document.getElementById('skipPay').addEventListener('click',function(){
  if(!P.trialStart) P.trialStart=Date.now();
  finishOnboarding();
});
function finishOnboarding(){
  document.getElementById('payModal').classList.remove('on');
  buildCats(); seedState(); save();
  document.getElementById('onboarding').style.display='none';
  document.getElementById('app').style.display='block';
  window.scrollTo(0,0);
  startApp();
}

function difficultyMult(){ return ({easy:1,mid:1.4,hard:2})[P.diff]||1; }

function seedTasks(){
  var mult=difficultyMult();
  S.tasks=[];
  CATS.forEach(function(cat){
    S.tasks.push({id:uid++, catId:cat.id, titleKey:cat.dk||null,
      title:cat.custom?cat.name:'',
      min: cat.id==='study' ? Math.round(20*mult)
         : cat.id==='sport' ? Math.round(Number(P.time)||30) : 0,
      done:false, photo:null});
  });
}

function seedMissions(){
  var target=Math.max(2,Math.round(3*difficultyMult()));
  S.missions=[];
  CATS.forEach(function(cat){
    S.missions.push({id:uid++, catId:cat.id, titleKey:cat.custom?null:cat.k,
      title:cat.custom?cat.name:'', target:Math.min(7,target),
      days:[0,0,0,0,0,0,0].map(function(){return false;})});
  });
}

function seedGoals(){
  S.goals=[];
  P.userGoals.forEach(function(g){
    S.goals.push({id:uid++, title:g, actions:guessSteps(g).map(function(k){
      return {id:uid++, key:k, text:'', done:false};
    })});
  });
}

function seedState(){
  seedTasks(); seedMissions(); seedGoals();
  if(!S.mini) S.mini=emptyMini();
}
/* task/mission/action labels may be a translation key or user text */
function label(o){ return o.titleKey ? t(o.titleKey) : (o.title||''); }
function actLabel(a){ return a.key ? t(a.key) : (a.text||''); }
"""
