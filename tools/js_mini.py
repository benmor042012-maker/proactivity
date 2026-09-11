# -*- coding: utf-8 -*-
"""The three mini-apps that live inside the Body tab: sport, skincare, fridge.

Everything here is local. No network call is made from any of this code -
the fridge photo is read with FileReader and never leaves the device.
"""

JS_MINI = r"""
/* ================= router ================= */
function miniState(){ if(!S.mini) S.mini=emptyMini(); return S.mini; }

function showMini(name){
  var M=miniState();
  M.view=name; save();
  document.querySelectorAll('.mini-view').forEach(function(v){
    v.classList.toggle('on', v.dataset.mini===name);
  });
  if(name==='hub')    renderHub();
  if(name==='sport')  renderSport();
  if(name==='skin')   renderSkinApp();
  if(name==='fridge') renderFridge();
  var host=document.getElementById('page-body');
  if(host && host.classList.contains('on')) host.scrollIntoView({block:'start'});
}

function renderMini(){
  var M=miniState();
  showMini(M.view||'hub');
}

function renderHub(){
  var M=miniState();
  var sp=M.sport, sk=M.skin, fr=M.fridge;
  var cards=[
    {id:'sport', icon:'dumbbell', n:'m.sport.n', d:'m.sport.d',
     stat: sp.sessions.length
        ? t('sp.total')+' '+sp.sessions.length+' · '+t('sp.streak')+' '+liveStreak(sp)
        : ''},
    {id:'skin', icon:'face', n:'m.skin.n', d:'m.skin.d',
     stat: sk.routine ? t('sp.streak')+' '+liveStreak(sk) : ''},
    {id:'fridge', icon:'fridge', n:'m.fridge.n', d:'m.fridge.d',
     stat: fr.pantry.length ? t('fr.count',{n:fr.pantry.length}) : ''}
  ];
  document.getElementById('hubGrid').innerHTML=cards.map(function(c){
    return '<button class="mini-card" data-mini-open="'+c.id+'">'+
      '<span class="mc-ic">'+ic(c.icon)+'</span>'+
      '<span class="mc-n">'+esc(t(c.n))+'</span>'+
      '<span class="mc-d">'+esc(t(c.d))+'</span>'+
      (c.stat?'<span class="mc-s">'+esc(c.stat)+'</span>':'')+
      '<span class="mc-go">'+esc(t('m.open'))+ic('arrow')+'</span></button>';
  }).join('');
}

document.addEventListener('click',function(e){
  var o=e.target.closest('[data-mini-open]'); if(o){ showMini(o.dataset.miniOpen); return; }
  var b=e.target.closest('[data-mini-back]'); if(b){ showMini('hub'); }
});

/* ================= sport ================= */
/* Built from the ex.* and cue.* keys that already ship translated in five
   languages. Nothing here is about weight, size or appearance. */
function E(k,r,cue){ return {k:k, r:r, cue:cue||''}; }

function workoutSets(){
  var S1=t('c.sec'), M1=t('c.min');
  function secs(n){ return n+' '+S1; }
  function reps(a,b){ return a+'×'+b; }
  return {
    general:[
      E('ex.warmup', '3 '+M1, 'cue.noeffort'),
      E('ex.squat', reps(2,10), 'cue.deep'),
      E('ex.pushup.k', reps(2,8), 'cue.shwidth'),
      E('ex.bridge', reps(2,12), 'cue.hips'),
      E('ex.plank', secs(20), 'cue.straight'),
      E('ex.stretch', '3 '+M1, 'cue.each20')
    ],
    strength:[
      E('ex.warmup', '3 '+M1, 'cue.noeffort'),
      E('ex.pushup', reps(3,8), 'cue.shwidth'),
      E('ex.squat', reps(3,12), 'cue.deep'),
      E('ex.dips.chair', reps(3,8), 'cue.triceps'),
      E('ex.lunge.stat', reps(2,8), 'cue.slowup'),
      E('ex.plank', secs(30), 'cue.straight'),
      E('ex.stretch', '3 '+M1, 'cue.each20')
    ],
    core:[
      E('ex.warmup', '2 '+M1, 'cue.noeffort'),
      E('ex.plank', secs(25), 'cue.straight'),
      E('ex.crunch', reps(2,12), 'cue.slowup'),
      E('ex.legraise', reps(2,10), 'cue.slowup'),
      E('ex.plank.side', secs(20), 'cue.straight'),
      E('ex.superman', reps(2,10), 'cue.hips'),
      E('ex.stretch', '2 '+M1, 'cue.each20')
    ],
    flex:[
      E('ex.sun', '3 '+t('c.rounds'), 'cue.natural'),
      E('ex.st.ham', secs(30), 'cue.each20'),
      E('ex.st.quad', secs(30), 'cue.each20'),
      E('ex.st.hip', secs(30), 'cue.each20'),
      E('ex.st.shoulder', secs(30), 'cue.each20'),
      E('ex.breathe', '10 '+t('c.breaths'), 'cue.478')
    ],
    short:[
      E('ex.jack', secs(30), 'cue.noeffort'),
      E('ex.squat', reps(1,12), 'cue.deep'),
      E('ex.pushup.k', reps(1,8), 'cue.shwidth'),
      E('ex.plank', secs(20), 'cue.straight')
    ]
  };
}
var SPORT_TYPES=['general','strength','core','flex','short'];
function workoutMinutes(list){ return Math.max(3, Math.round(list.length*1.6)); }

var run=null;          // live session, never persisted mid-way
var restTimer=null;

function sportScreen(name){
  document.querySelectorAll('#miniSport .sp-screen').forEach(function(s){
    s.classList.toggle('on', s.dataset.sp===name);
  });
}

function renderSport(){
  clearRest();
  var sp=miniState().sport;
  var today=dayKey();
  var wk=weekDays();
  var inWeek=sp.sessions.filter(function(x){ return wk.indexOf(x.d)>=0; }).length;
  document.getElementById('spTotal').textContent=sp.sessions.length;
  document.getElementById('spStreak').textContent=liveStreak(sp);
  document.getElementById('spWeek').textContent=inWeek+'/7';
  document.getElementById('spWeekBar').style.width=Math.min(100,inWeek/7*100)+'%';
  document.getElementById('spFirst').style.display=sp.sessions.length?'none':'block';
  sportScreen('home');
}

/* the seven dates of the current week, Sunday first */
function weekDays(){
  var now=new Date(), out=[];
  var start=new Date(now); start.setDate(now.getDate()-now.getDay());
  for(var i=0;i<7;i++){ var d=new Date(start); d.setDate(start.getDate()+i); out.push(dayKey(d)); }
  return out;
}

function renderSportPick(){
  var sets=workoutSets();
  document.getElementById('spPickGrid').innerHTML=SPORT_TYPES.map(function(id){
    var list=sets[id];
    return '<button class="pick-card" data-sp-type="'+id+'">'+
      '<span class="pk-n">'+esc(t('sp.w.'+id))+'</span>'+
      '<span class="pk-m">'+esc(t('sp.meta',{n:list.length, min:workoutMinutes(list)}))+'</span>'+
      ic('arrow')+'</button>';
  }).join('');
  sportScreen('pick');
}

function startRun(type){
  var list=workoutSets()[type];
  run={type:type, list:list, i:0, started:Date.now()};
  renderRun();
  sportScreen('run');
}

function renderRun(){
  clearRest();
  var ex=run.list[run.i], total=run.list.length;
  document.getElementById('spOf').textContent=t('sp.of',{n:run.i+1,t:total});
  document.getElementById('spExName').textContent=t(ex.k);
  document.getElementById('spExReps').textContent=ex.r;
  document.getElementById('spExCue').textContent=ex.cue?t(ex.cue):'';
  document.getElementById('spDots').innerHTML=run.list.map(function(_,i){
    return '<span class="dot'+(i<run.i?' done':'')+(i===run.i?' now':'')+'"></span>';
  }).join('');
  document.getElementById('spRest').classList.remove('on');
  document.getElementById('spExBody').classList.remove('resting');
}

function clearRest(){
  if(restTimer){ clearInterval(restTimer); restTimer=null; }
  var r=document.getElementById('spRest');
  if(r) r.classList.remove('on');
}

function finishExercise(){
  if(!run) return;
  if(run.i >= run.list.length-1){ endRun(); return; }
  var left=25;
  var nextName=t(run.list[run.i+1].k);
  var box=document.getElementById('spRest');
  var num=document.getElementById('spRestN');
  document.getElementById('spRestNext').textContent=t('sp.next',{x:nextName});
  document.getElementById('spExBody').classList.add('resting');
  box.classList.add('on');
  num.textContent=left;
  restTimer=setInterval(function(){
    left--;
    num.textContent=Math.max(0,left);
    if(left<=0) advance();
  },1000);
}
function advance(){
  clearRest();
  if(!run) return;
  run.i++;
  if(run.i>=run.list.length){ endRun(); return; }
  renderRun();
}

function endRun(){
  clearRest();
  if(!run) return;
  var sp=miniState().sport;
  var mins=Math.max(1, Math.round((Date.now()-run.started)/60000)) || 1;
  var n=run.list.length;
  sp.sessions.unshift({d:dayKey(), type:run.type, n:n, mins:mins});
  if(sp.sessions.length>60) sp.sessions.length=60;
  bumpStreak(sp);
  addPts(15);
  save();
  document.getElementById('spDoneN').textContent=t('sp.done.n',{n:n});
  document.getElementById('spDoneM').textContent=t('sp.done.m',{min:mins});
  document.getElementById('spDoneMsg').textContent=t(pick(['sp.enc.1','sp.enc.2','sp.enc.3','sp.enc.4']));
  run=null;
  renderStats();
  sportScreen('done');
}

function quitRun(){ clearRest(); run=null; renderSport(); }

function renderSportProgress(){
  var sp=miniState().sport;
  var wk=weekDays(), today=dayKey();
  var month=dayKey().slice(0,7);
  var inWeek=sp.sessions.filter(function(x){ return wk.indexOf(x.d)>=0; }).length;
  var inMonth=sp.sessions.filter(function(x){ return String(x.d).slice(0,7)===month; }).length;
  document.getElementById('spPrWeek').textContent=inWeek;
  document.getElementById('spPrMonth').textContent=inMonth;
  document.getElementById('spPrStreak').textContent=liveStreak(sp);

  var done={};
  sp.sessions.forEach(function(x){ done[x.d]=true; });
  var names=dayNames();
  document.getElementById('spBoard').innerHTML=wk.map(function(d,i){
    var on=!!done[d], isToday=(d===today);
    return '<div class="wk-cell'+(on?' on':'')+(isToday?' today':'')+'">'+
      '<span class="wk-d">'+esc(names[i])+'</span>'+
      '<span class="wk-m">'+(on?ic('check'):'')+'</span></div>';
  }).join('');

  var hist=sp.sessions.slice(0,10);
  document.getElementById('spHist').innerHTML = hist.length
    ? hist.map(function(x){
        return '<div class="hist-row"><span class="hr-n">'+esc(t('sp.w.'+x.type))+'</span>'+
          '<span class="hr-m">'+esc(t('sp.done.n',{n:x.n}))+' · '+esc(t('sp.done.m',{min:x.mins}))+'</span>'+
          '<span class="hr-d">'+esc(x.d)+'</span></div>';
      }).join('')
    : '<div class="empty">'+esc(t('sp.pr.empty'))+'</div>';
  sportScreen('progress');
}

/* ================= skincare ================= */
function renderSkinApp(){
  var sk=miniState().skin;
  if(!sk.routine){ renderSkinSetup(); return; }
  renderSkinRoutine();
}

function skinScreen(name){
  document.querySelectorAll('#miniSkin .sn-screen').forEach(function(s){
    s.classList.toggle('on', s.dataset.sn===name);
  });
}

var skinDraft={feel:'normal', react:'no', depth:'basic'};

function renderSkinSetup(){
  var sk=miniState().skin;
  if(sk.setup) skinDraft=Object.assign({},sk.setup);
  function group(id,key,opts){
    return '<div class="qlabel">'+esc(t(key))+'</div><div class="opts">'+
      opts.map(function(o){
        return '<div class="opt'+(skinDraft[id]===o.v?' on':'')+'" data-sn-set="'+id+'" data-sn-val="'+o.v+'">'+
          ic(o.i)+'<span>'+esc(t(o.k))+'</span></div>';
      }).join('')+'</div>';
  }
  document.getElementById('snSetup').innerHTML=
    group('feel','sn.q1',[
      {v:'normal',k:'sn.q1.normal',i:'user'},{v:'oily',k:'sn.q1.oily',i:'drop'},
      {v:'dry',k:'sn.q1.dry',i:'sun'},{v:'combo',k:'sn.q1.combo',i:'refresh'}])+
    group('react','sn.q2',[
      {v:'yes',k:'sn.q2.yes',i:'shield'},{v:'no',k:'sn.q2.no',i:'check'},
      {v:'dunno',k:'sn.q2.dunno',i:'compass'}])+
    group('depth','sn.q3',[
      {v:'basic',k:'sn.q3.basic',i:'seedling'},{v:'full',k:'sn.q3.full',i:'sparkles'}]);
  skinScreen('setup');
}

document.addEventListener('click',function(e){
  var o=e.target.closest('[data-sn-set]'); if(!o) return;
  skinDraft[o.dataset.snSet]=o.dataset.snVal;
  renderSkinSetup();
});

/* Reuses buildSkin(), so the wording and the per-step explanations stay the
   ones already translated for the routine that shipped before. */
/* The routine stores which steps were chosen, not their wording. It used to
   keep the resolved text, which meant a routine written in Hebrew stayed in
   Hebrew after switching the app to English and kept the old gender besides. */
function buildRoutine(){
  var d=skinDraft;
  var type=({normal:'normal',oily:'oily',dry:'dry',combo:'combo'})[d.feel]||'normal';
  var am=[0,1,2], pm=[0,1,2];
  if(d.depth==='basic'){ am=[0,2]; pm=[1,2]; }   // drop the optional middle step
  function step(k){ return {k:k, product:''}; }
  return {type:type, react:d.react, depth:d.depth, am:am.map(step), pm:pm.map(step)};
}
/* Resolves a stored routine against the current language and gender. */
function routineSteps(sk, which){
  var blocks=buildSkin((sk.routine&&sk.routine.type)||'normal');
  var items=(which==='am'?blocks[0]:blocks[1]).items;
  return (sk.routine[which]||[]).map(function(s){
    var it=items[s.k|0] || items[0];
    return {n:it.n, d:it.d, product:s.product||''};
  });
}
/* Routines written before the step references existed keep their products and
   their shape; only the wording starts following the language again. */
function migrateRoutine(sk){
  var r=sk && sk.routine; if(!r) return;
  ['am','pm'].forEach(function(w){
    var arr=r[w]; if(!arr || !arr.length || arr[0].k!==undefined) return;
    var idx = (w==='am')
      ? (arr.length===2 ? [0,2] : [0,1,2])
      : (arr.length===2 ? [1,2] : [0,1,2]);
    r[w]=arr.map(function(s,i){ return {k:(idx[i]!==undefined?idx[i]:i), product:s.product||''}; });
  });
}

function renderSkinRoutine(){
  var sk=miniState().skin, today=dayKey();
  var log=sk.log[today]||{};
  function list(which){
    return routineSteps(sk,which).map(function(s,i){
      return '<div class="sn-step">'+
        '<span class="sn-num">'+(i+1)+'</span>'+
        '<div class="sn-body"><div class="sn-n">'+esc(s.n)+'</div>'+
        (s.d?'<div class="sn-d">'+esc(s.d)+'</div>':'')+
        '<input type="text" class="sn-p" data-sn-w="'+which+'" data-sn-i="'+i+'" '+
        'value="'+esc(s.product||'')+'" placeholder="'+esc(t('sn.product.ph'))+'"></div></div>';
    }).join('');
  }
  document.getElementById('snAm').innerHTML=list('am');
  document.getElementById('snPm').innerHTML=list('pm');

  var amBtn=document.getElementById('snDoAm'), pmBtn=document.getElementById('snDoPm');
  amBtn.classList.toggle('done', !!log.am);
  pmBtn.classList.toggle('done', !!log.pm);
  amBtn.innerHTML=ic(log.am?'check':'sun')+'<span>'+esc(t(log.am?'sn.done.am':'sn.did.am'))+'</span>';
  pmBtn.innerHTML=ic(log.pm?'check':'moon')+'<span>'+esc(t(log.pm?'sn.done.pm':'sn.did.pm'))+'</span>';

  var wk=weekDays(), count=0;
  wk.forEach(function(d){ var l=sk.log[d]; if(l&&(l.am||l.pm)) count++; });
  document.getElementById('snStreak').textContent=liveStreak(sk);
  document.getElementById('snWeek').textContent=count+'/7';

  var names=dayNames();
  document.getElementById('snBoard').innerHTML=wk.map(function(d,i){
    var l=sk.log[d]||{};
    var full=l.am&&l.pm, part=l.am||l.pm;
    return '<div class="wk-cell'+(full?' on':(part?' half':''))+(d===today?' today':'')+'">'+
      '<span class="wk-d">'+esc(names[i])+'</span>'+
      '<span class="wk-m">'+(part?ic('check'):'')+'</span></div>';
  }).join('');

  var days=Object.keys(sk.log).sort().reverse().slice(0,7);
  document.getElementById('snHist').innerHTML = days.length
    ? days.map(function(d){
        var l=sk.log[d]||{};
        var parts=[];
        if(l.am) parts.push(t('sn.am'));
        if(l.pm) parts.push(t('sn.pm'));
        return '<div class="hist-row"><span class="hr-n">'+esc(d)+'</span>'+
               '<span class="hr-m">'+esc(parts.join(' · '))+'</span></div>';
      }).join('')
    : '<div class="empty">'+esc(t('sn.hist.empty'))+'</div>';
  skinScreen('routine');
}

function markSkin(which){
  var sk=miniState().skin, today=dayKey();
  if(!sk.log[today]) sk.log[today]={};
  var was=!!sk.log[today][which];
  sk.log[today][which]=!was;
  if(!was){ bumpStreak(sk); addPts(6); toast(praise()); }
  else { addPts(-6); }
  save(); renderSkinRoutine(); renderStats();
}

/* ================= fridge ================= */
var ING=[
  {g:'fg.protein', items:['ing.egg','ing.chicken','ing.tuna','ing.beans','ing.chickpea','ing.lentils','ing.tofu']},
  {g:'fg.veg',     items:['ing.tomato','ing.cucumber','ing.onion','ing.pepper','ing.carrot','ing.potato','ing.spinach','ing.mushroom','ing.zucchini','ing.avocado','ing.garlic']},
  {g:'fg.fruit',   items:['ing.banana','ing.apple','ing.berries','ing.lemon']},
  {g:'fg.grain',   items:['ing.bread','ing.rice','ing.pasta','ing.oats','ing.tortilla','ing.crackers']},
  {g:'fg.dairy',   items:['ing.cheese','ing.yogurt','ing.cottage','ing.milk']},
  {g:'fg.pantry',  items:['ing.oil','ing.honey','ing.nuts','ing.hummus']}
];

var RECIPES=[
  /* breakfast */
  {id:'shakshuka',     meal:'breakfast', mins:20, ing:['ing.egg','ing.tomato','ing.onion','ing.pepper','ing.bread','ing.oil'], steps:4},
  {id:'omelette',      meal:'breakfast', mins:10, ing:['ing.egg','ing.mushroom','ing.spinach','ing.oil'], steps:3},
  {id:'oatmeal',       meal:'breakfast', mins:8,  ing:['ing.oats','ing.milk','ing.banana','ing.nuts','ing.honey'], steps:3},
  {id:'yogurtbowl',    meal:'breakfast', mins:5,  ing:['ing.yogurt','ing.berries','ing.banana','ing.nuts','ing.honey'], steps:3},
  {id:'fruitsmooth',   meal:'breakfast', mins:5,  ing:['ing.banana','ing.berries','ing.milk','ing.yogurt'], steps:3},
  {id:'avocadotoast',  meal:'breakfast', mins:7,  ing:['ing.avocado','ing.bread','ing.tomato','ing.lemon'], steps:3},
  {id:'scrambleveg',   meal:'breakfast', mins:10, ing:['ing.egg','ing.pepper','ing.onion','ing.oil'], steps:3},
  {id:'cottagebowl',   meal:'breakfast', mins:5,  ing:['ing.cottage','ing.berries','ing.banana','ing.nuts','ing.honey'], steps:3},
  {id:'bananapancake', meal:'breakfast', mins:12, ing:['ing.banana','ing.egg','ing.oats'], steps:3},

  /* main meals */
  {id:'eggtoast',      meal:'meal', mins:8,  ing:['ing.egg','ing.bread','ing.tomato','ing.oil'], steps:3},
  {id:'tunasalad',     meal:'meal', mins:10, ing:['ing.tuna','ing.chickpea','ing.tomato','ing.cucumber','ing.onion','ing.oil','ing.lemon'], steps:3},
  {id:'pastagarlic',   meal:'meal', mins:15, ing:['ing.pasta','ing.garlic','ing.oil','ing.cheese'], steps:4},
  {id:'ricebowl',      meal:'meal', mins:25, ing:['ing.rice','ing.carrot','ing.pepper','ing.onion','ing.oil','ing.lemon'], steps:3},
  {id:'wrap',          meal:'meal', mins:12, ing:['ing.tortilla','ing.chicken','ing.spinach','ing.tomato','ing.cucumber','ing.yogurt'], steps:3},
  {id:'bakedpotato',   meal:'meal', mins:45, ing:['ing.potato','ing.cheese','ing.beans','ing.tuna'], steps:3},
  {id:'chickpeasalad', meal:'meal', mins:10, ing:['ing.chickpea','ing.tomato','ing.cucumber','ing.onion','ing.oil','ing.lemon'], steps:3},
  {id:'pastaveg',      meal:'meal', mins:22, ing:['ing.pasta','ing.tomato','ing.onion','ing.garlic','ing.zucchini','ing.pepper','ing.oil'], steps:4},
  {id:'grilledcheese', meal:'meal', mins:8,  ing:['ing.bread','ing.cheese','ing.tomato'], steps:3},
  {id:'tofustir',      meal:'meal', mins:18, ing:['ing.tofu','ing.pepper','ing.carrot','ing.garlic','ing.rice','ing.oil'], steps:4},
  {id:'beansrice',     meal:'meal', mins:20, ing:['ing.beans','ing.rice','ing.onion','ing.garlic','ing.oil'], steps:3},
  {id:'roastveg',      meal:'meal', mins:35, ing:['ing.potato','ing.carrot','ing.zucchini','ing.pepper','ing.oil','ing.garlic'], steps:3},
  {id:'lentilsoup',    meal:'meal', mins:30, ing:['ing.lentils','ing.onion','ing.carrot','ing.garlic','ing.oil','ing.lemon'], steps:4},
  {id:'chickenrice',   meal:'meal', mins:25, ing:['ing.chicken','ing.rice','ing.pepper','ing.carrot','ing.garlic','ing.lemon'], steps:4},
  {id:'tunapasta',     meal:'meal', mins:18, ing:['ing.tuna','ing.pasta','ing.tomato','ing.garlic','ing.oil','ing.lemon'], steps:4},
  {id:'pitastuff',     meal:'meal', mins:8,  ing:['ing.tortilla','ing.hummus','ing.egg','ing.tomato','ing.cucumber'], steps:3},
  {id:'veggiesoup',    meal:'meal', mins:28, ing:['ing.onion','ing.carrot','ing.potato','ing.zucchini','ing.oil'], steps:3},

  /* snacks */
  {id:'hummusplate',   meal:'snack', mins:5,  ing:['ing.hummus','ing.carrot','ing.cucumber','ing.pepper','ing.oil'], steps:3},
  {id:'applenut',      meal:'snack', mins:4,  ing:['ing.apple','ing.nuts'], steps:3},
  {id:'yogurthoney',   meal:'snack', mins:3,  ing:['ing.yogurt','ing.honey','ing.nuts'], steps:3},
  {id:'cheesecrackers',meal:'snack', mins:5,  ing:['ing.crackers','ing.cheese','ing.tomato','ing.oil'], steps:3}
];

/* "quick" is derived, not stored, so it can never drift from mins */
var MEAL_FILTERS=['all','breakfast','meal','snack','quick'];
function matchesFilter(r,f){
  if(f==='all')   return true;
  if(f==='quick') return r.mins<=10;
  return r.meal===f;
}

function fridgeScreen(name){
  document.querySelectorAll('#miniFridge .fr-screen').forEach(function(s){
    s.classList.toggle('on', s.dataset.fr===name);
  });
}

function renderFridge(){
  var fr=miniState().fridge;
  if(fr.pantry.length || fr.photo) renderPantry();
  else { fridgeScreen('entry'); renderSuggest(); }
}

function renderPantry(){
  var fr=miniState().fridge;
  var img=document.getElementById('frPhoto');
  if(fr.photo){ img.src=fr.photo; img.style.display='block';
                document.getElementById('frPhotoWrap').style.display='block'; }
  else { img.removeAttribute('src'); document.getElementById('frPhotoWrap').style.display='none'; }

  document.getElementById('frGroups').innerHTML=ING.map(function(g){
    return '<div class="ing-group"><div class="ing-h">'+esc(t(g.g))+'</div><div class="chips">'+
      g.items.map(function(k){
        var on=fr.pantry.indexOf(k)>=0;
        return '<button class="chip'+(on?' on':'')+'" data-ing="'+k+'">'+esc(t(k))+'</button>';
      }).join('')+'</div></div>';
  }).join('');

  var custom=fr.pantry.filter(function(k){ return k.indexOf('x:')===0; });
  document.getElementById('frCustom').innerHTML=custom.map(function(k){
    return '<button class="chip on" data-ing="'+esc(k)+'">'+esc(k.slice(2))+ic('x')+'</button>';
  }).join('');

  document.getElementById('frCount').textContent=t('fr.count',{n:fr.pantry.length});
  fridgeScreen('pantry');
  renderSuggest();
}

function toggleIng(key){
  var fr=miniState().fridge;
  var i=fr.pantry.indexOf(key);
  if(i>=0) fr.pantry.splice(i,1); else fr.pantry.push(key);
  save(); renderPantry();
}

function scoreRecipes(){
  var have=miniState().fridge.pantry;
  return RECIPES.map(function(r){
    var hit=r.ing.filter(function(k){ return have.indexOf(k)>=0; });
    var miss=r.ing.filter(function(k){ return have.indexOf(k)<0; });
    return {r:r, hit:hit, miss:miss, score:hit.length/r.ing.length};
  })
  .filter(function(x){ return x.hit.length>=2 && x.score>=0.5; })
  .sort(function(a,b){ return (b.score-a.score) || (a.miss.length-b.miss.length); });
}

function recipeCard(x){
  var fr=miniState().fridge;
  var r=x.r, fav=fr.favs.indexOf(r.id)>=0;
  var steps=[];
  for(var i=1;i<=r.steps;i++) steps.push(t('r.'+r.id+'.'+i));
  return '<div class="rec">'+
    '<div class="rec-h"><div><div class="rec-n">'+esc(t('r.'+r.id+'.n'))+'</div>'+
    '<div class="rec-m">'+ic('clock')+esc(t('fr.mins',{n:r.mins}))+' · '+
    (x.miss.length? esc(t('fr.almost',{n:x.miss.length})) : '<b>'+esc(t('fr.ready'))+'</b>')+'</div></div>'+
    '<button class="icon-btn fav'+(fav?' on':'')+'" data-fav="'+r.id+'" aria-label="'+esc(t('fr.save'))+'">'+ic('star')+'</button></div>'+
    (x.hit.length?'<div class="rec-i"><span class="ri-h">'+esc(t('fr.have'))+'</span>'+
      x.hit.map(function(k){ return '<span class="ri ok">'+ic('check')+esc(t(k))+'</span>'; }).join('')+'</div>':'')+
    (x.miss.length?'<div class="rec-i"><span class="ri-h">'+esc(t('fr.missing'))+'</span>'+
      x.miss.map(function(k){ return '<span class="ri no">'+esc(t(k))+'</span>'; }).join('')+'</div>':'')+
    '<div class="rec-s"><div class="rs-h">'+esc(t('fr.steps'))+'</div><ol>'+
    steps.map(function(s){ return '<li>'+esc(s)+'</li>'; }).join('')+'</ol></div></div>';
}

var frTab='ideas', frOffset=0;

function renderIdeas(){
  var fr=miniState().fridge;
  document.querySelectorAll('#miniFridge .fr-tab').forEach(function(b){
    b.classList.toggle('on', b.dataset.frTab===frTab);
  });
  var box=document.getElementById('frOut');
  var another=document.getElementById('frAnother');
  another.style.display='none';

  if(frTab==='ideas'){
    var all=scoreRecipes();
    if(!all.length){ box.innerHTML='<div class="empty">'+esc(t('fr.none'))+'</div>'; }
    else{
      if(frOffset>=all.length) frOffset=0;
      var show=all.slice(frOffset, frOffset+3);
      if(!show.length){ frOffset=0; show=all.slice(0,3); }
      show.forEach(function(x){
        var h=fr.history;
        var i=h.indexOf(x.r.id); if(i>=0) h.splice(i,1);
        h.unshift(x.r.id);
      });
      if(fr.history.length>20) fr.history.length=20;
      save();
      box.innerHTML=show.map(recipeCard).join('');
      if(all.length>3) another.style.display='';
    }
  } else if(frTab==='favs'){
    var favs=fr.favs.map(byId).filter(Boolean);
    box.innerHTML = favs.length ? favs.map(withMatch).map(recipeCard).join('')
      : '<div class="empty">'+esc(t('fr.favs.empty'))+'</div>';
  } else {
    var hist=fr.history.map(byId).filter(Boolean);
    box.innerHTML = hist.length ? hist.map(withMatch).map(recipeCard).join('')
      : '<div class="empty">'+esc(t('fr.hist.empty'))+'</div>';
  }
  fridgeScreen('ideas');
}
var sugFilter='all', sugShown=6;

/* Always-on browsable library. Reuses recipeCard()/withMatch(), so a card here
   marks what you have and saves to favourites exactly like a matched result. */
function renderSuggest(){
  var box=document.getElementById('frSugOut');
  if(!box) return;
  document.querySelectorAll('#frSugFilters .sug-f').forEach(function(b){
    b.classList.toggle('on', b.dataset.sugF===sugFilter);
  });
  var list=RECIPES.filter(function(r){ return matchesFilter(r,sugFilter); });
  if(!list.length){ box.innerHTML='<div class="empty">'+esc(t('fs.empty'))+'</div>'; }
  else box.innerHTML=list.slice(0,sugShown).map(withMatch).map(recipeCard).join('');
  var more=document.getElementById('frSugMore');
  more.style.display = list.length>sugShown ? '' : 'none';
}

function byId(id){ for(var i=0;i<RECIPES.length;i++) if(RECIPES[i].id===id) return RECIPES[i]; return null; }
function withMatch(r){
  var have=miniState().fridge.pantry;
  var hit=r.ing.filter(function(k){ return have.indexOf(k)>=0; });
  var miss=r.ing.filter(function(k){ return have.indexOf(k)<0; });
  return {r:r, hit:hit, miss:miss, score:r.ing.length?hit.length/r.ing.length:0};
}

/* ================= wiring ================= */
function bindMini(){
  document.getElementById('spStart').addEventListener('click', renderSportPick);
  document.getElementById('spProgress').addEventListener('click', renderSportProgress);
  document.getElementById('spPickBack').addEventListener('click', renderSport);
  document.getElementById('spPrBack').addEventListener('click', renderSport);
  document.getElementById('spDoneBack').addEventListener('click', renderSport);
  document.getElementById('spDid').addEventListener('click', finishExercise);
  document.getElementById('spSkipRest').addEventListener('click', advance);
  document.getElementById('spQuit').addEventListener('click', quitRun);
  document.getElementById('spPickGrid').addEventListener('click', function(e){
    var b=e.target.closest('[data-sp-type]'); if(b) startRun(b.dataset.spType);
  });

  document.getElementById('snBuild').addEventListener('click', function(){
    var sk=miniState().skin;
    sk.setup=Object.assign({},skinDraft);
    sk.routine=buildRoutine();
    save(); renderSkinRoutine();
  });
  document.getElementById('snRedo').addEventListener('click', renderSkinSetup);
  document.getElementById('snDoAm').addEventListener('click', function(){ markSkin('am'); });
  document.getElementById('snDoPm').addEventListener('click', function(){ markSkin('pm'); });
  document.getElementById('miniSkin').addEventListener('change', function(e){
    var inp=e.target.closest('.sn-p'); if(!inp) return;
    var sk=miniState().skin;
    sk.routine[inp.dataset.snW][Number(inp.dataset.snI)].product=inp.value.trim();
    save();
  });

  document.getElementById('frManual').addEventListener('click', renderPantry);
  document.getElementById('frPhotoBtn').addEventListener('click', function(){
    document.getElementById('frFile').click();
  });
  /* FileReader only - the image is turned into a local data URL and stored in
     localStorage. It is never uploaded and no request is made. */
  document.getElementById('frFile').addEventListener('change', function(e){
    var f=e.target.files[0]; if(!f) return;
    var rd=new FileReader();
    rd.onload=function(ev){
      shrinkPhoto(ev.target.result, function(small){
        miniState().fridge.photo=small; save(); renderPantry();
      });
    };
    rd.readAsDataURL(f);
    e.target.value='';
  });
  document.getElementById('frPhotoRm').addEventListener('click', function(){
    miniState().fridge.photo=null; save(); renderPantry();
  });
  document.getElementById('frGroups').addEventListener('click', function(e){
    var b=e.target.closest('[data-ing]'); if(b) toggleIng(b.dataset.ing);
  });
  document.getElementById('frCustom').addEventListener('click', function(e){
    var b=e.target.closest('[data-ing]'); if(b) toggleIng(b.dataset.ing);
  });
  document.getElementById('frAddBtn').addEventListener('click', addCustomIng);
  document.getElementById('frAdd').addEventListener('keydown', function(e){
    if(e.key==='Enter') addCustomIng();
  });
  document.getElementById('frClear').addEventListener('click', function(){
    miniState().fridge.pantry=[]; save(); renderPantry();
  });
  document.getElementById('frFind').addEventListener('click', function(){
    if(!miniState().fridge.pantry.length){ toast(t('fr.pickfirst')); return; }
    frTab='ideas'; frOffset=0; renderIdeas();
  });
  document.getElementById('frIdeasBack').addEventListener('click', renderPantry);
  document.getElementById('frAnother').addEventListener('click', function(){
    frOffset+=3; renderIdeas();
  });
  document.querySelectorAll('#miniFridge .fr-tab').forEach(function(b){
    b.addEventListener('click', function(){ frTab=b.dataset.frTab; renderIdeas(); });
  });
  document.getElementById('frSugFilters').addEventListener('click', function(e){
    var b=e.target.closest('[data-sug-f]'); if(!b) return;
    sugFilter=b.dataset.sugF; sugShown=6; renderSuggest();
  });
  document.getElementById('frSugMore').addEventListener('click', function(){
    sugShown+=6; renderSuggest();
  });
  document.getElementById('frSugOut').addEventListener('click', function(e){
    var b=e.target.closest('[data-fav]'); if(!b) return;
    var fr=miniState().fridge, id=b.dataset.fav, i=fr.favs.indexOf(id);
    if(i>=0) fr.favs.splice(i,1); else { fr.favs.unshift(id); toast(t('fr.saved')); }
    save(); renderSuggest(); if(frTab!=='ideas') renderIdeas();
  });
  document.getElementById('frOut').addEventListener('click', function(e){
    var b=e.target.closest('[data-fav]'); if(!b) return;
    var fr=miniState().fridge, id=b.dataset.fav, i=fr.favs.indexOf(id);
    if(i>=0) fr.favs.splice(i,1); else { fr.favs.unshift(id); toast(t('fr.saved')); }
    save(); renderIdeas();
  });
}

function addCustomIng(){
  var inp=document.getElementById('frAdd'), v=inp.value.trim();
  if(!v) return;
  var key='x:'+v;
  var fr=miniState().fridge;
  if(fr.pantry.indexOf(key)<0) fr.pantry.push(key);
  inp.value=''; save(); renderPantry();
}

/* Keep the stored photo small: localStorage is a few MB and a raw phone
   photo would blow the quota and lose everything else with it. */
function shrinkPhoto(dataUrl, cb){
  var img=new Image();
  img.onload=function(){
    var max=900, w=img.width, h=img.height;
    var s=Math.min(1, max/Math.max(w,h));
    var cv=document.createElement('canvas');
    cv.width=Math.round(w*s); cv.height=Math.round(h*s);
    cv.getContext('2d').drawImage(img,0,0,cv.width,cv.height);
    try{ cb(cv.toDataURL('image/jpeg',0.7)); }catch(e){ cb(dataUrl); }
  };
  img.onerror=function(){ cb(dataUrl); };
  img.src=dataUrl;
}
"""
