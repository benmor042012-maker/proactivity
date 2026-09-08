# -*- coding: utf-8 -*-
"""The goal chain and the micro-tips.

  pick an area -> what exactly -> how often -> what gets in the way
  -> a target composed from those answers -> the ladder -> "start the target"

The chain renders into any host element, so the same screens serve onboarding
(step 6) and the Goals tab. Its answers live under their own storage key while
it is in flight, so Back keeps them and a refresh does not lose them.
"""

JS_CHAIN = r"""
/* ================= areas ================= */
var AREAS=[
 {id:'sport',  icon:'activity', cat:'sport',   lesson:null},
 {id:'study',  icon:'book',     cat:'study',   lesson:7},
 {id:'time',   icon:'clock',    cat:'study',   lesson:5},
 {id:'goals',  icon:'target',   cat:'hobby',   lesson:6},
 {id:'habits', icon:'refresh',  cat:'hobby',   lesson:7},
 {id:'init',   icon:'rocket',   cat:'hobby',   lesson:2},
 {id:'sleep',  icon:'moon',     cat:'sleep',   lesson:7},
 {id:'social', icon:'users',    cat:'friends', lesson:3},
 {id:'learn',  icon:'sparkles', cat:'hobby',   lesson:4}
];
var OBSTACLES=['start','delay','time','keep','what','other'];
function areaById(id){ for(var i=0;i<AREAS.length;i++) if(AREAS[i].id===id) return AREAS[i]; return null; }

/* "Homework on time" means nothing to a 35-year-old: the study options have an
   adult set. The rest read the same at any age. */
function kindKeys(area){
  var adult = area==='study' && ageBand(P.age)!=='a13';
  var out=[];
  for(var n=1;n<=6;n++) out.push(adult ? 'gk.study.a.'+n : 'gk.'+area+'.'+n);
  return out;
}

/* ================= chain state ================= */
/* step: 0 area · 1 kind · 2 freq · 3 obstacle · 4 result */
var CH=null;
function emptyChain(){ return {step:0, area:null, kind:null, kindText:'', freq:null, obst:null}; }
function saveChain(){ try{ localStorage.setItem('proactive_chain', JSON.stringify(CH)); }catch(e){} }
function loadChain(){
  try{ var raw=localStorage.getItem('proactive_chain'); if(raw){ var c=JSON.parse(raw); if(c && typeof c.step==='number') CH=c; } }catch(e){}
  if(!CH) CH=emptyChain();
}
function resetChain(){ CH=emptyChain(); saveChain(); }
var chainHostId=null;

/* ================= composing the target ================= */
function kindLabel(){
  if(!CH) return '';
  if(CH.kind==='other') return CH.kindText||t('gc.other');
  return CH.kind ? t(CH.kind) : '';
}
function chainTitle(){ return t('gt.title',{kind:kindLabel(), freq:t('gf.'+(CH.freq||3))}); }
function chainWeek(){  return t('gw.line',{freq:t('gf.'+(CH.freq||3)), kind:kindLabel()}); }
function chainToday(){ return t('gd.'+(CH.area||'goals'),{kind:kindLabel()}); }
function chainNow(){   return t('gn.'+(CH.obst||'other')); }

/* A goal built here carries where it came from, so the ladder can be
   regenerated in another language and the weekly mission knows its area. */
function goalFromChain(){
  var g=newGoal(chainTitle());
  g.area=CH.area; g.kind=CH.kind; g.kindText=CH.kindText; g.freq=CH.freq||3; g.obst=CH.obst;
  g.week=chainWeek(); g.today=chainToday(); g.now=chainNow();
  g.actions=[
    {id:uid++, key:null, text:chainNow(),   done:false},
    {id:uid++, key:null, text:chainToday(), done:false},
    {id:uid++, key:null, text:chainWeek(),  done:false}
  ];
  return g;
}

/* ================= rendering ================= */
function optBtn(attr,val,label,icon,on){
  return '<button type="button" class="opt'+(on?' on':'')+'" data-'+attr+'="'+esc(val)+'" aria-pressed="'+(on?'true':'false')+'">'+
    (icon?ic(icon):'')+'<span>'+esc(label)+'</span></button>';
}
function chainHead(n){
  return '<div class="ch-head">'+
    (n>0 ? '<button type="button" class="btn btn-quiet btn-sm" data-ch-back>'+ic('chevron','flip')+'<span>'+esc(t('c.back'))+'</span></button>' : '<span></span>')+
    '<span class="ch-count numf">'+(n+1)+'/5</span></div>'+
    '<div class="bar ch-bar"><i style="width:'+Math.round((n+1)/5*100)+'%"></i></div>';
}
function renderChain(hostId){
  var host=document.getElementById(hostId||chainHostId);
  if(!host) return;
  chainHostId=hostId||chainHostId;
  if(!CH) loadChain();
  var s=CH.step, html='';

  if(s===0){
    html=chainHead(0)+'<h3 class="ch-q">'+esc(t('gc.t'))+'</h3><p class="psub">'+esc(t('gc.s'))+'</p>'+
      '<div class="opts ch-areas">'+AREAS.map(function(a){
        return optBtn('area',a.id,t('ga.'+a.id),a.icon,CH.area===a.id); }).join('')+'</div>';
  } else if(s===1){
    html=chainHead(1)+'<h3 class="ch-q">'+esc(t('gc.kind.q'))+'</h3><p class="psub">'+esc(t('gc.kind.s'))+'</p>'+
      '<div class="opts">'+kindKeys(CH.area).map(function(k){ return optBtn('kind',k,t(k),null,CH.kind===k); }).join('')+
      optBtn('kind','other',t('gc.other'),'plus',CH.kind==='other')+'</div>'+
      '<div class="field ch-other'+(CH.kind==='other'?'':' hidden')+'"><input type="text" id="chKindText" value="'+esc(CH.kindText||'')+'" placeholder="'+esc(t('gc.other.ph'))+'" aria-label="'+esc(t('gc.other'))+'"></div>'+
      '<div class="nav"><button type="button" class="btn btn-primary" data-ch-next'+(CH.kind?'':' disabled')+'><span>'+esc(t('c.next'))+'</span>'+ic('arrow')+'</button></div>';
  } else if(s===2){
    html=chainHead(2)+'<h3 class="ch-q">'+esc(t('gc.freq.q'))+'</h3><p class="psub">'+esc(t('gc.freq.s'))+'</p>'+
      '<div class="opts ch-freq">'+[1,2,3,4,5].map(function(n){ return optBtn('freq',n,t('gf.'+n),null,CH.freq===n); }).join('')+'</div>';
  } else if(s===3){
    html=chainHead(3)+'<h3 class="ch-q">'+esc(t('gc.obst.q'))+'</h3><p class="psub">'+esc(t('gc.obst.s'))+'</p>'+
      '<div class="opts ch-obst">'+OBSTACLES.map(function(o){ return optBtn('obst',o,t('go.'+o),null,CH.obst===o); }).join('')+'</div>';
  } else {
    var a=areaById(CH.area)||AREAS[3];
    html=chainHead(4)+'<h3 class="ch-q">'+esc(t('gc.result.t'))+'</h3><p class="psub">'+esc(t('gc.result.s'))+'</p>'+
      '<div class="ladder ch-ladder">'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.goal'))+'</span><span class="rung-v strong">'+esc(chainTitle())+'</span></div>'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.week'))+'</span><span class="rung-v">'+esc(chainWeek())+'</span></div>'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.today'))+'</span><span class="rung-v">'+esc(chainToday())+'</span></div>'+
        '<div class="rung now"><span class="rung-k">'+esc(t('gl.now'))+'</span><span class="rung-v">'+esc(chainNow())+'</span></div>'+
      '</div>'+
      '<p class="hint">'+ic('shield')+'<span>'+esc(t('gc.start.n'))+'</span></p>'+
      '<div class="nav ch-nav">'+
        '<button type="button" class="btn btn-ghost" data-ch-save><span>'+esc(t('gc.later'))+'</span></button>'+
        '<button type="button" class="btn btn-primary" data-ch-start>'+ic('play')+'<span>'+esc(t('gc.start'))+'</span></button>'+
      '</div>'+
      '<div class="ch-plan"><span>'+esc(t('gc.plan.q'))+'</span> '+
        '<button type="button" class="btn btn-quiet btn-sm" data-ch-plan>'+ic(a.lesson?'book':'activity')+'<span>'+esc(t('gp.'+a.id))+'</span></button></div>';
  }
  host.innerHTML=html;
  bindChain(host);
}

function bindChain(host){
  host.querySelectorAll('[data-ch-back]').forEach(function(b){
    b.addEventListener('click',function(){ CH.step=Math.max(0,CH.step-1); saveChain(); renderChain(); });
  });
  host.querySelectorAll('[data-area]').forEach(function(b){
    b.addEventListener('click',function(){
      if(CH.area!==b.dataset.area){ CH.kind=null; CH.kindText=''; }
      CH.area=b.dataset.area; CH.step=1; saveChain(); renderChain();
    });
  });
  host.querySelectorAll('[data-kind]').forEach(function(b){
    b.addEventListener('click',function(){
      CH.kind=b.dataset.kind; saveChain();
      if(CH.kind==='other'){ renderChain(); var inp=document.getElementById('chKindText'); if(inp) inp.focus(); return; }
      CH.step=2; saveChain(); renderChain();
    });
  });
  var kt=host.querySelector('#chKindText');
  if(kt){
    kt.addEventListener('input',function(){ CH.kindText=kt.value; saveChain();
      var nx=host.querySelector('[data-ch-next]'); if(nx) nx.disabled=!kt.value.trim(); });
    kt.addEventListener('keydown',function(e){ if(e.key==='Enter' && kt.value.trim()){ e.preventDefault(); CH.step=2; saveChain(); renderChain(); } });
  }
  host.querySelectorAll('[data-ch-next]').forEach(function(b){
    b.addEventListener('click',function(){
      if(CH.kind==='other' && !(CH.kindText||'').trim()) return;
      CH.step=Math.min(4,CH.step+1); saveChain(); renderChain();
    });
  });
  host.querySelectorAll('[data-freq]').forEach(function(b){
    b.addEventListener('click',function(){ CH.freq=Number(b.dataset.freq); CH.step=3; saveChain(); renderChain(); });
  });
  host.querySelectorAll('[data-obst]').forEach(function(b){
    b.addEventListener('click',function(){ CH.obst=b.dataset.obst; CH.step=4; saveChain(); renderChain(); });
  });
  host.querySelectorAll('[data-ch-save]').forEach(function(b){
    b.addEventListener('click',function(){ commitChain(false); });
  });
  host.querySelectorAll('[data-ch-start]').forEach(function(b){
    b.addEventListener('click',function(){ commitChain(true); });
  });
  host.querySelectorAll('[data-ch-plan]').forEach(function(b){
    b.addEventListener('click',function(){ openPlanFor(CH.area); });
  });
}

/* The one exit from the chain. During onboarding the goal is parked on the
   profile and seeded when setup finishes; in the app it is added directly. */
function commitChain(start){
  var g=goalFromChain();
  var dup=(S.goals||[]).some(function(x){ return x.title===g.title; });
  if(dup && !onbActive){ toast(t('gc.dup')); return; }
  if(onbActive){
    P.chainGoal={goal:g, start:!!start};
    resetChain();
    showStep(7);
    return;
  }
  S.goals.unshift(g);
  if(start) startGoal(g); else { save(); tip('goal.new'); }
  resetChain();
  var host=document.getElementById('goalChain'); if(host){ host.innerHTML=''; host.hidden=true; }
  var nb=document.getElementById('newGoalBtn'); if(nb) nb.hidden=false;
  renderGoals(); renderDash(); checkAchievements();
}

/* Sport already has an age-adapted training plan in the Body tab; every other
   area has a lesson that fits. Neither is invented for this - they are the
   parts of the app that were already there. */
function openPlanFor(area){
  var a=areaById(area);
  if(!a) return;
  if(onbActive){ P.planAfter=area; toast(t('gl.saved')); return; }
  if(!a.lesson){ goPage('body'); showMini('sport'); return; }
  goPage('learn');
  var d=document.querySelectorAll('#lsGrid details')[a.lesson-1];
  if(d){ d.open=true; d.scrollIntoView({block:'start'}); }
}

/* ================= starting a target ================= */
/* Creating a target changes nothing. THIS is what starts the counters: the
   goal is marked started, its weekly mission appears on the grid with the
   frequency the user chose, and only now does the day count. */
function startGoal(g){
  if(!g || g.started) return;
  g.started=true; g.startedAt=dayKey();
  var a=areaById(g.area);
  var target=Math.min(7,Math.max(1, g.freq===5 ? 6 : (g.freq||3)));
  S.missions.push({id:uid++, catId:a?a.cat:'hobby', titleKey:null, title:g.title,
                   target:target, goalId:g.id,
                   days:[false,false,false,false,false,false,false]});
  markActiveToday();
  save();
  toast(t('gc.started.t'));
  tip('goal.start');
  renderGoals(); renderWeek(); renderDash(); checkAchievements();
}

/* ================= micro-tips ================= */
/* One short line tied to the action that just happened, at most once per
   action type per day, so it reads as the app noticing rather than nagging. */
var TIPS={'task.done':1,'goal.new':1,'goal.start':1,'goal.done':1,'task.skip':1,'streak':1,'lesson':1};
var tipT;
function tip(kind){
  if(!TIPS[kind]) return;
  if(!S.tips) S.tips={};
  var day=dayKey();
  if(S.tips[kind]===day) return;
  S.tips[kind]=day; save();
  var el=document.getElementById('tipCard');
  if(!el) return;
  el.innerHTML='<span class="tip-lab">'+ic('sparkles')+esc(t('tip.lab'))+'</span><span class="tip-tx">'+esc(t('tip.'+kind))+'</span>';
  el.classList.add('on');
  clearTimeout(tipT); tipT=setTimeout(function(){ el.classList.remove('on'); },5200);
}
"""
