# -*- coding: utf-8 -*-
JS_RENDER = r"""
/* ================= camera ================= */
var camStream=null;
function openCam(name,cb){
  var modal=document.getElementById('camModal'), v=document.getElementById('camV'),
      pv=document.getElementById('camP'), fi=document.getElementById('camF'),
      bar=document.getElementById('camBtns');
  document.getElementById('camTN').textContent=name;
  pv.style.display='none'; v.style.display='block'; modal.classList.add('on');
  var shot=null;

  function stop(){ if(camStream){ camStream.getTracks().forEach(function(t){t.stop();}); camStream=null; } }
  function close(){ stop(); modal.classList.remove('on'); }
  function mk(cls,html){ var b=document.createElement('button'); b.className='btn '+cls; b.innerHTML=html; return b; }

  function buttons(mode){
    bar.innerHTML='';
    if(mode==='live'){
      var s=mk('btn-primary', ic('camera')+'<span>'+esc(t('c.takephoto'))+'</span>'),
          g=mk('btn-ghost',   ic('image')+'<span>'+esc(t('c.gallery'))+'</span>'),
          c=mk('btn-quiet',   esc(t('c.cancel')));
      s.onclick=function(){
        var cv=document.createElement('canvas');
        cv.width=v.videoWidth||640; cv.height=v.videoHeight||480;
        cv.getContext('2d').drawImage(v,0,0,cv.width,cv.height);
        shot=cv.toDataURL('image/jpeg',0.6);
        pv.src=shot; pv.style.display='block'; v.style.display='none'; stop(); buttons('ok');
      };
      g.onclick=function(){ fi.click(); };
      c.onclick=close;
      bar.append(s,g,c);
    } else if(mode==='upload'){
      var u=mk('btn-primary', ic('image')+'<span>'+esc(t('c.choosephoto'))+'</span>'),
          c2=mk('btn-quiet', esc(t('c.cancel')));
      u.onclick=function(){ fi.click(); }; c2.onclick=close;
      bar.append(u,c2);
    } else {
      var ok=mk('btn-primary', ic('check')+'<span>'+esc(t('c.use'))+'</span>'),
          re=mk('btn-ghost', esc(t('c.retake')));
      ok.onclick=function(){ close(); cb(shot); };
      re.onclick=function(){ pv.style.display='none'; start(); };
      bar.append(ok,re);
    }
  }
  fi.onchange=function(e){
    var f=e.target.files[0]; if(!f) return;
    var r=new FileReader();
    r.onload=function(ev){ shot=ev.target.result; pv.src=shot; pv.style.display='block';
      v.style.display='none'; stop(); buttons('ok'); };
    r.readAsDataURL(f); fi.value='';
  };
  function start(){
    v.style.display='block';
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
      navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'}})
        .then(function(s){ camStream=s; v.srcObject=s; buttons('live'); })
        .catch(function(){ v.style.display='none'; buttons('upload'); });
    } else { v.style.display='none'; buttons('upload'); }
  }
  start();
}

/* ================= home ================= */
function fmtMin(m){ return !m ? '' : (m>=60 ? Math.floor(m/60)+t('c.hr') : m+' '+t('c.min')); }

function addTask(catId,title,min){
  if(!String(title||'').trim()) return;
  S.tasks.push({id:uid++,catId:catId,titleKey:null,title:String(title).trim(),
                min:Number(min)||0,done:false,photo:null});
  save(); renderTasks(); renderStats(); renderDash();
}
function toggleTask(id){
  var task=null;
  S.tasks.forEach(function(x){ if(x.id===id) task=x; });
  if(!task) return;
  if(task.done){
    task.done=false; task.photo=null; addPts(-10);
    S.stats.tasksDone=Math.max(0,(S.stats.tasksDone||0)-1);
    save(); renderTasks(); renderStats(); renderDash(); return;
  }
  openCam(label(task), function(photo){
    task.photo=photo; task.done=true; addPts(10);
    S.stats.tasksDone=(S.stats.tasksDone||0)+1;
    markActiveToday();
    toast(praise()); save(); tip('task.done');
    renderTasks(); renderStats(); renderDash(); checkAchievements();
  });
}
function delTask(id){
  S.tasks=S.tasks.filter(function(x){ return x.id!==id; });
  save(); renderTasks(); renderStats(); renderDash();
}

function renderRing(){
  var svg=document.getElementById('rSvg');
  var r=54, cx=66, cy=66, sw=10, circ=2*Math.PI*r;
  var track=cssVar('--ink-3')||'#333947', fill=cssVar('--acc')||'#3DDCA8';
  var total=S.tasks.length;
  if(!total){
    svg.innerHTML='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+track+'" stroke-width="'+sw+'" stroke-dasharray="3 7"/>';
    document.getElementById('rPct').textContent='0%'; return;
  }
  var out='', off=0;
  CATS.forEach(function(cat){
    var ct=S.tasks.filter(function(x){ return x.catId===cat.id; });
    if(!ct.length) return;
    var done=ct.filter(function(x){ return x.done; }).length;
    var seg=(ct.length/total)*circ, filled=seg*(done/ct.length);
    out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+track+'" stroke-width="'+sw+'" stroke-dasharray="'+(seg-2)+' '+(circ-seg+2)+'" stroke-dashoffset="'+(-off)+'"/>';
    if(filled>0)
      out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="'+fill+'" stroke-width="'+sw+'" stroke-linecap="round" stroke-dasharray="'+Math.max(0,filled-2)+' '+(circ-filled+2)+'" stroke-dashoffset="'+(-off)+'"/>';
    off+=seg;
  });
  svg.innerHTML=out;
  var d=S.tasks.filter(function(x){ return x.done; }).length;
  document.getElementById('rPct').textContent=Math.round(d/total*100)+'%';
}

function renderCats(){
  var grid=document.getElementById('catGrid'); grid.innerHTML='';
  CATS.forEach(function(cat){
    var ct=S.tasks.filter(function(x){ return x.catId===cat.id; });
    var done=ct.filter(function(x){ return x.done; }).length;
    var card=document.createElement('div'); card.className='cat';

    var rows = ct.length ? ct.map(function(x){
      return '<div class="task">'+
        '<input type="checkbox" class="cb" data-id="'+x.id+'"'+(x.done?' checked':'')+'>'+
        (x.photo?'<img class="thumb" src="'+x.photo+'" alt="">':'')+
        '<div class="body"><div class="ttl'+(x.done?' done':'')+'">'+esc(label(x))+'</div>'+
        '<div class="meta">'+ic('camera')+'<span>'+esc(t('c.proof'))+'</span>'+
        (x.min?ic('clock')+'<span>'+esc(fmtMin(x.min))+'</span>':'')+'</div></div>'+
        (x.min?'<button class="tmr" data-tid="'+x.id+'" data-min="'+x.min+'" aria-label="'+esc(t('c.timer'))+'">'+ic('play')+'</button>':'')+
        '<button class="icon-btn" data-del="'+x.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button>'+
        '</div>';
    }).join('') : '<div class="empty">'+esc(t('h.empty'))+'</div>';

    var sugs=(cat.sg||['sg.generic']).map(function(k){
      return '<button class="sug" data-cat="'+cat.id+'" data-sug="'+esc(t(k))+'">'+esc(t(k))+'</button>';
    }).join('');

    card.innerHTML=
      '<div class="cathead"><div class="nm">'+ic(cat.icon)+'<span>'+esc(catName(cat))+'</span></div>'+
      '<div class="ct numf"><b>'+done+'</b>/'+ct.length+'</div></div>'+
      rows+
      '<div class="sugs">'+sugs+'</div>'+
      '<div class="addrow"><input type="text" class="nt" data-cat="'+cat.id+'" placeholder="'+esc(t('h.add.ph'))+'">'+
      '<input type="number" class="ntmin" data-cat="'+cat.id+'" min="0" placeholder="'+esc(t('h.add.min'))+'">'+
      '<button class="btn btn-primary" data-add="'+cat.id+'">'+ic('plus')+'</button></div>';
    grid.appendChild(card);
  });

  grid.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){ toggleTask(Number(e.target.dataset.id)); });
  });
  grid.querySelectorAll('[data-del]').forEach(function(b){
    b.addEventListener('click',function(){ delTask(Number(b.dataset.del)); });
  });
  grid.querySelectorAll('[data-add]').forEach(function(b){
    b.addEventListener('click',function(){
      var c=b.dataset.add;
      addTask(c, grid.querySelector('.nt[data-cat="'+c+'"]').value,
                 grid.querySelector('.ntmin[data-cat="'+c+'"]').value);
    });
  });
  grid.querySelectorAll('.nt').forEach(function(inp){
    inp.addEventListener('keydown',function(e){
      if(e.key!=='Enter') return;
      var c=inp.dataset.cat;
      addTask(c, inp.value, grid.querySelector('.ntmin[data-cat="'+c+'"]').value);
    });
  });
  grid.querySelectorAll('.sug').forEach(function(b){
    b.addEventListener('click',function(){ addTask(b.dataset.cat,b.dataset.sug,0); });
  });
  grid.querySelectorAll('.tmr').forEach(function(b){
    b.addEventListener('click',function(){ startTimer(b,Number(b.dataset.min)); });
  });
}

var timers={};
function startTimer(btn,minutes){
  var id=btn.dataset.tid;
  if(timers[id]){ clearInterval(timers[id]); delete timers[id];
    btn.classList.remove('run'); btn.innerHTML=ic('play'); return; }
  var left=minutes*60;
  btn.classList.add('run');
  timers[id]=setInterval(function(){
    left--;
    btn.textContent=Math.floor(left/60)+':'+String(left%60).padStart(2,'0');
    if(left<=0){
      clearInterval(timers[id]); delete timers[id];
      btn.classList.remove('run'); btn.innerHTML=ic('play'); toast(t('t.timerdone'));
    }
  },1000);
}

/* ================= goals ================= */
/* The point of this screen is the ladder: a goal is only real once it says
   what it means this week, what it means today, and what you do right now. */
function goalById(id){
  var g=null;
  (S.goals||[]).forEach(function(x){ if(x.id===id) g=x; });
  return g;
}
function goalPct(g){
  if(!g.actions.length) return 0;
  var done=g.actions.filter(function(a){ return a.done; }).length;
  return Math.round(done/g.actions.length*100);
}
/* A finished target is kept, not deleted: it is the evidence the app exists to
   produce. It folds down to one line and can be reopened. */
function archivedCard(g){
  var card=document.createElement('article'); card.className='goal archived';
  card.innerHTML='<h3>'+ic('check')+'<span>'+esc(g.title)+'</span>'+
    '<button class="icon-btn" data-dg="'+g.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('trash')+'</button></h3>'+
    '<span class="gstate done">'+ic('check')+esc(t('gc.done',{d:fmtDay(g.doneAt)}))+'</span>'+
    '<div class="gtools"><button class="btn btn-ghost btn-sm" data-gback="'+g.id+'">'+ic('refresh')+
      '<span>'+esc(t('gc.reopen'))+'</span></button></div>';
  return card;
}
function renderGoals(){
  var box=document.getElementById('goalsCont'); box.innerHTML='';
  if(!S.goals.length){
    box.innerHTML='<div class="empty-state">'+ic('target')+
      '<p>'+esc(t('n.empty.goals'))+'</p></div>';
    return;
  }
  /* live targets first, finished ones folded to the bottom */
  var ordered=S.goals.slice().sort(function(a,b){ return (a.archived?1:0)-(b.archived?1:0); });
  ordered.forEach(function(g){
    if(g.archived){ box.appendChild(archivedCard(g)); return; }
    var done=g.actions.filter(function(a){ return a.done; }).length;
    var pct=goalPct(g);
    var started=!!g.started && !g.paused;
    var card=document.createElement('article');
    card.className='goal'+(started?'':' unstarted')+(g.paused?' paused':'');
    /* Until "start the target" is pressed the card is a written target and
       nothing else: no percentage, no counter, no bar. */
    var state = g.paused
      ? '<span class="gstate off">'+ic('clock')+esc(t('gc.paused'))+'</span>'
      : started
      ? '<span class="gstate on">'+ic('play')+esc(t('gc.started',{d:fmtDay(g.startedAt)}))+'</span>'
      : '<span class="gstate">'+ic('clock')+esc(t('gc.notstarted'))+'</span>';
    card.innerHTML=
      '<h3>'+ic('target')+'<span>'+esc(g.title)+'</span>'+
      '<button class="icon-btn" data-dg="'+g.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('trash')+'</button></h3>'+
      state+

      '<div class="ladder">'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.goal'))+'</span>'+
          '<span class="rung-v strong">'+esc(g.title)+'</span></div>'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.week'))+'</span>'+
          '<input type="text" class="rung-in" data-lad="week" data-gid="'+g.id+'" '+
          'value="'+esc(g.week||'')+'" placeholder="'+esc(t('gl.wk.ph'))+'" aria-label="'+esc(t('gl.week'))+'"></div>'+
        '<div class="rung"><span class="rung-k">'+esc(t('gl.today'))+'</span>'+
          '<input type="text" class="rung-in" data-lad="today" data-gid="'+g.id+'" '+
          'value="'+esc(g.today||'')+'" placeholder="'+esc(t('gl.td.ph'))+'" aria-label="'+esc(t('gl.today'))+'"></div>'+
        '<div class="rung now"><span class="rung-k">'+esc(t('gl.now'))+'</span>'+
          (g.now?'<span class="rung-v">'+esc(g.now)+'</span>':'')+
          (started
            ? '<button class="btn btn-primary btn-sm" data-gnow="'+g.id+'">'+ic('play')+'<span>'+esc(t('gl.now.btn'))+'</span></button>'
            : '<button class="btn btn-primary btn-sm" data-gstart="'+g.id+'">'+ic('play')+'<span>'+esc(t('gc.start'))+'</span></button>')+
        '</div>'+
      '</div>'+
      (started||g.paused?'':'<p class="hint gstart-n">'+ic('shield')+'<span>'+esc(t('gc.start.n'))+'</span></p>')+
      (g.started
        ? '<div class="gtools">'+
            '<button class="btn btn-ghost btn-sm" data-gpause="'+g.id+'">'+ic(g.paused?'play':'clock')+
              '<span>'+esc(t(g.paused?'gc.resume':'gc.pause'))+'</span></button>'+
            '<button class="btn btn-ghost btn-sm" data-gdone="'+g.id+'">'+ic('check')+
              '<span>'+esc(t('gc.finish'))+'</span></button>'+
            '<button class="btn btn-ghost btn-sm" data-gcal="'+g.id+'">'+ic('calendar')+
              '<span>'+esc(t('cal.add'))+'</span>'+(isPro()?'':ic('lock','mini'))+'</button>'+
          '</div>'
        : '')+

      '<div class="acts-h">'+esc(t('gl.steps'))+'</div>'+
      '<div class="acts">'+g.actions.map(function(a){
        return '<label><input type="checkbox" class="cb" data-gid="'+g.id+'" data-aid="'+a.id+'"'+
          (a.done?' checked':'')+'><span'+(a.done?' class="done"':'')+'>'+esc(actLabel(a))+'</span></label>';
      }).join('')+'</div>'+
      '<div class="addrow"><input type="text" class="na" data-gid="'+g.id+'" placeholder="'+esc(t('g.step.ph'))+'" aria-label="'+esc(t('g.step.ph'))+'">'+
      '<button class="btn btn-ghost" data-na="'+g.id+'" aria-label="'+esc(t('c.add'))+'">'+ic('plus')+'</button></div>'+
      (started
        ? '<div class="gmeta"><span class="numf">'+done+'/'+g.actions.length+'</span><span class="numf">'+pct+'%</span></div>'+
          '<div class="gbar"><i style="width:'+pct+'%"></i></div>'
        : '');
    box.appendChild(card);
  });
  box.querySelectorAll('[data-gstart]').forEach(function(b){
    b.addEventListener('click',function(){ startGoal(goalById(Number(b.dataset.gstart))); });
  });
  box.querySelectorAll('[data-gpause]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gpause)); if(!g) return;
      g.paused=!g.paused; save(); renderGoals(); renderDash();
      toast(t(g.paused?'t.gpaused':'t.gresumed'));
    });
  });
  box.querySelectorAll('[data-gdone]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gdone)); if(!g) return;
      g.archived=true; g.doneAt=dayKey();
      S.stats.challenges=(S.stats.challenges||0)+1;
      markActiveToday(); save(); renderGoals(); renderDash(); checkAchievements();
      toast(t('t.gdone')); tip('goal.done');
    });
  });
  box.querySelectorAll('[data-gcal]').forEach(function(b){
    b.addEventListener('click',function(){
      if(!isPro()){ openPlans(); return; }
      var g=goalById(Number(b.dataset.gcal)); if(g) downloadICS(g);
    });
  });
  box.querySelectorAll('[data-gback]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gback)); if(!g) return;
      if(goalLimitReached()){ openPlans(); return; }
      g.archived=false; g.doneAt=null; save(); renderGoals(); renderDash();
    });
  });

  box.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){
      var g=goalById(Number(e.target.dataset.gid)), a=null;
      if(!g) return;
      g.actions.forEach(function(x){ if(x.id===Number(e.target.dataset.aid)) a=x; });
      if(!a) return;
      a.done=e.target.checked;
      if(g.started){
        addPts(a.done?12:-12);
        if(a.done){ toast(t('t.step')); markActiveToday(); }
        if(a.done && goalPct(g)===100) tip('goal.done');
      }
      save(); renderGoals(); renderStats(); renderDash(); checkAchievements();
    });
  });
  box.querySelectorAll('[data-dg]').forEach(function(b){
    b.addEventListener('click',function(){
      S.goals=S.goals.filter(function(g){ return g.id!==Number(b.dataset.dg); });
      save(); renderGoals(); renderDash();
    });
  });
  box.querySelectorAll('[data-na]').forEach(function(b){
    b.addEventListener('click',function(){
      var gid=Number(b.dataset.na), g=goalById(gid);
      if(!g) return;
      var inp=box.querySelector('.na[data-gid="'+gid+'"]'), v=inp.value.trim();
      if(!v) return;
      g.actions.push({id:uid++,key:null,text:v,done:false});
      inp.value=''; save(); renderGoals();
    });
  });
  /* The ladder inputs save on blur rather than on every keystroke: a full
     re-render mid-typing would steal the caret. */
  box.querySelectorAll('.rung-in').forEach(function(inp){
    inp.addEventListener('change',function(){
      var g=goalById(Number(inp.dataset.gid));
      if(!g) return;
      g[inp.dataset.lad]=inp.value.trim();
      save(); renderDash(); toast(t('gl.saved'));
    });
  });
  box.querySelectorAll('[data-gnow]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.gnow));
      if(!g) return;
      startFiveMinutes(g.today || g.week || g.title);
    });
  });
}
document.getElementById('aGoalBtn').addEventListener('click',addGoalFromInput);
document.getElementById('nGoalIn').addEventListener('keydown',function(e){
  if(e.key==='Enter'){ e.preventDefault(); addGoalFromInput(); }
});
function addGoalFromInput(){
  var inp=document.getElementById('nGoalIn'), v=inp.value.trim();
  if(!v){ toast(t('t.writegoal')); return; }
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  S.goals.unshift(newGoal(v));
  inp.value=''; save(); renderGoals(); renderDash(); checkAchievements();
  toast(t('t.goaladded')); tip('goal.new');
}
document.getElementById('newGoalBtn').addEventListener('click',function(){
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  resetChain();
  var host=document.getElementById('goalChain'); host.hidden=false;
  document.getElementById('newGoalBtn').hidden=true;
  renderChain('goalChain');
  host.scrollIntoView({block:'start',behavior:'smooth'});
});
function fmtDay(k){
  if(!k) return '';
  try{ return new Date(k+'T00:00:00').toLocaleDateString(cur,{day:'numeric',month:'short'}); }catch(e){ return k; }
}

/* ================= week ================= */
function dayNames(){
  var base=new Date(2024,0,7); // a Sunday
  var out=[];
  for(var i=0;i<7;i++){
    var d=new Date(base); d.setDate(base.getDate()+i);
    out.push(d.toLocaleDateString(cur,{weekday:'short'}));
  }
  return out;
}
function missionState(m){
  var c=m.days.filter(Boolean).length;
  if(m.target>0 && c>=m.target) return {txt:t('w.st.win'), cls:'win', met:true};
  if(c>0 && c>=Math.ceil(m.target/2)) return {txt:t('w.st.close'), cls:'mid', met:false};
  if(c>0) return {txt:t('w.st.going'), cls:'mid', met:false};
  return {txt:t('w.st.none'), cls:'none', met:false};
}
function renderWeek(){
  var days=dayNames(), today=new Date().getDay();
  document.getElementById('wHead').innerHTML=
    '<th class="mcol">'+esc(t('w.col.mission'))+'</th>'+
    days.map(function(d,i){ return '<th'+(i===today?' class="today"':'')+'>'+esc(d)+'</th>'; }).join('')+
    '<th>'+esc(t('w.col.status'))+'</th>';

  var body=document.getElementById('wBody'); body.innerHTML='';
  var met=0;
  S.missions.forEach(function(m){
    var cat=catById(m.catId)||{icon:'star'};
    var st=missionState(m); if(st.met) met++;
    var count=m.days.filter(Boolean).length;
    var tr=document.createElement('tr');
    var html='<td class="mcol"><div class="mrow">'+ic(cat.icon)+
      '<div><div class="mt">'+esc(label(m))+'</div>'+
      '<div class="mm">'+esc(t('w.target'))+' <span class="numf">'+count+'/'+m.target+'</span></div></div>'+
      '<button class="icon-btn" data-dm="'+m.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('x')+'</button></div></td>';
    m.days.forEach(function(on,di){
      html+='<td class="dcell'+(on?' on':'')+'" data-mid="'+m.id+'" data-day="'+di+'">'+
            '<span class="mk">'+ic('check')+'</span></td>';
    });
    html+='<td class="scell '+st.cls+'">'+esc(st.txt)+'</td>';
    tr.innerHTML=html; body.appendChild(tr);
  });
  if(!S.missions.length)
    body.innerHTML='<tr><td colspan="9" class="empty" style="padding:var(--s4)">'+esc(t('w.empty'))+'</td></tr>';

  document.getElementById('wMet').textContent=met;
  document.getElementById('wTot').textContent=S.missions.length;

  body.querySelectorAll('.dcell').forEach(function(cell){
    cell.addEventListener('click',function(){
      var m=null;
      S.missions.forEach(function(x){ if(x.id===Number(cell.dataset.mid)) m=x; });
      if(!m) return;
      var d=Number(cell.dataset.day);
      m.days[d]=!m.days[d];
      addPts(m.days[d]?6:-6);
      if(m.days[d]){ toast(praise()); markActiveToday(); }
      save(); renderWeek(); renderStats(); renderDash(); checkAchievements();
    });
  });
  body.querySelectorAll('[data-dm]').forEach(function(b){
    b.addEventListener('click',function(){
      S.missions=S.missions.filter(function(m){ return m.id!==Number(b.dataset.dm); });
      save(); renderWeek();
    });
  });
}
function fillMissionCats(){
  document.getElementById('nMisCat').innerHTML=
    CATS.map(function(c){ return '<option value="'+c.id+'">'+esc(catName(c))+'</option>'; }).join('');
}
document.getElementById('aMisBtn').addEventListener('click',function(){
  var inp=document.getElementById('nMis'), v=inp.value.trim();
  if(!v) return;
  S.missions.push({id:uid++, catId:document.getElementById('nMisCat').value, titleKey:null, title:v,
    target:Math.min(7,Math.max(1,Number(document.getElementById('nMisT').value)||3)),
    days:[false,false,false,false,false,false,false]});
  inp.value=''; save(); renderWeek();
});
document.getElementById('rvBtn').addEventListener('click',function(){
  var met=0;
  S.missions.forEach(function(m){ if(missionState(m).met) met++; });
  var total=S.missions.length, reward=met*50;
  addPts(reward); save(); renderStats();
  var msg = total && met===total ? t('w.rev.perfect')
          : met>=total/2 && met>0 ? t('w.rev.strong') : t('w.rev.start');
  var out=document.getElementById('rvRes');
  out.innerHTML='<div class="big numf">'+met+'/'+total+'</div>'+
    '<div class="msg">'+esc(msg)+'</div>'+
    '<div class="pts">'+esc(t('t.pts',{n:reward}))+'</div>';
  out.classList.add('on');
});
document.getElementById('rWkBtn').addEventListener('click',function(){
  S.missions.forEach(function(m){ m.days=[false,false,false,false,false,false,false]; });
  document.getElementById('rvRes').classList.remove('on');
  save(); renderWeek(); toast(t('t.newweek'));
});

/* ================= body plans ================= */
function renderPlan(gridId,blocks,prefix){
  var grid=document.getElementById(gridId); grid.innerHTML='';
  blocks.forEach(function(block,bi){
    var card=document.createElement('div'); card.className='pcard';
    var title = block.k ? t(block.k) : block.label;
    var items=block.items.map(function(item,ii){
      var key=prefix+'-'+bi+'-'+ii;
      var checked=S.plan[key]?' checked':'';
      var name = item.k ? t(item.k) : item.n;
      var cam  = item.k ? false : !!item.cam;   // workout items are not photo-gated
      var meta = item.r ? '<span class="pr">'+ic('clock')+esc(item.r)+'</span>'
               : cam    ? '<span class="pr">'+ic('camera')+'</span>' : '';
      return '<div class="pitem">'+
        '<input type="checkbox" class="cb" data-key="'+key+'" data-cam="'+(cam?1:0)+'" data-name="'+esc(name)+'"'+checked+'>'+
        '<div class="pb"><span class="px'+(checked?' done':'')+'">'+esc(name)+'</span>'+
        (item.d?'<div class="pd">'+esc(item.d)+'</div>':'')+'</div>'+meta+'</div>';
    }).join('');
    card.innerHTML='<h3><span>'+esc(title)+'</span><span class="dnum">'+t('c.day')+' '+(bi+1)+'</span></h3>'+
      (block.sub?'<div class="psub2">'+esc(block.sub)+'</div>':'')+items;
    grid.appendChild(card);
  });

  grid.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){
      var key=e.target.dataset.key;
      if(e.target.checked){
        if(e.target.dataset.cam==='1'){
          e.target.checked=false;
          openCam(e.target.dataset.name,function(){
            S.plan[key]=true; addPts(8); toast(t('t.proof'));
            save(); renderPlan(gridId,blocks,prefix); renderStats();
          });
        } else {
          S.plan[key]=true; addPts(8); toast(praise()); save(); renderStats();
          var px=e.target.closest('.pitem').querySelector('.px'); if(px) px.classList.add('done');
        }
      } else {
        delete S.plan[key]; addPts(-8); save(); renderStats();
        var px2=e.target.closest('.pitem').querySelector('.px'); if(px2) px2.classList.remove('done');
      }
    });
  });
}

/* ================= why it works ================= */
function renderTheories(){
  var g=document.getElementById('thGrid');
  g.innerHTML=THEORIES.map(function(th,i){
    return '<div class="th"><div class="n">'+String(i+1).padStart(2,'0')+'</div>'+
      ic(th.icon)+
      '<h4>'+esc(t(th.n))+'</h4><div class="au">'+esc(t(th.a))+'</div>'+
      '<div class="pr2">'+esc(t(th.p))+'</div>'+
      '<div class="hw">'+esc(t(th.h))+'</div>'+
      '<dl><dt>'+esc(t('y.where'))+'</dt><dd>'+esc(t(th.f))+'</dd></dl></div>';
  }).join('');
}

/* ================= stats + insight ================= */
function renderStats(){
  var s=stageInfo();
  document.getElementById('lvl').textContent=s.level;
  document.getElementById('stg').textContent=s.stage;
  document.getElementById('xpF').style.width=s.progress+'%';
  document.getElementById('skV').textContent=shownStreak();
  document.getElementById('ptV').textContent=S.points;
  document.getElementById('dnV').textContent=S.tasks.filter(function(x){return x.done;}).length;
  document.getElementById('tlV').textContent=S.tasks.length;
}
function renderInsight(){
  var ins=pick(INSIGHTS);
  document.getElementById('dIns').innerHTML=
    '<div class="insight">'+ic('sparkles')+'<div>'+
    '<div class="lab">'+esc(t('h.insight'))+'</div>'+
    '<div class="txt">'+esc(t(ins.t))+'</div>'+
    '<div class="src">'+esc(t(ins.s))+'</div></div></div>';
}

/* ================= the dashboard ================= */
/* Deliberately narrow: four numbers, one next step, one profile summary. The
   full task list lives on its own tab so the first screen never turns into a
   wall of twenty things. */
function renderDashStats(){
  var box=document.getElementById('dashStats');
  if(!box) return;
  var cells=[
    {ic:'flame',    v:shownStreak(),                                 k:'d.streak'},
    {ic:'target',   v:(S.goals||[]).length,                          k:'d.goals'},
    {ic:'check',    v:(S.stats.tasksDone||0),                        k:'d.done'},
    {ic:'gauge',    v:hasProfile()? profileIndex()+'%' : '—',        k:'d.index'}
  ];
  box.innerHTML='<h2 class="sr">'+esc(t('d.progress'))+'</h2>'+
    cells.map(function(c){
      return '<div class="dstat">'+ic(c.ic)+
        '<div class="dv numf">'+esc(String(c.v))+'</div>'+
        '<div class="dk">'+esc(t(c.k))+'</div></div>';
    }).join('')+
    '<p class="dstreak">'+esc(streakLine())+'</p>';
}

/* ---- the single next step, and the five-minute starter ---- */
var fiveTimer=null, fiveLeft=0;
function clearFive(){
  if(fiveTimer){ clearInterval(fiveTimer); fiveTimer=null; }
}
function startFiveMinutes(labelText){
  clearFive();
  fiveLeft=5*60;
  markActiveToday(); tip('task.skip');
  goPage('home');
  renderNextCard(labelText);
  fiveTimer=setInterval(function(){
    fiveLeft--;
    var el=document.getElementById('fiveTxt');
    if(el){
      var m=Math.floor(fiveLeft/60), sec=String(fiveLeft%60).padStart(2,'0');
      el.textContent=t('d.running',{t:m+':'+sec});
    }
    if(fiveLeft<=0){ clearFive(); toast(t('d.timeup')); renderNextCard(); }
  },1000);
}
/* If the user has started a target, its "right now" rung IS the next step -
   that is the whole point of the chain. Only without one does the app fall
   back to the profile-driven suggestion. */
function activeGoalNow(){
  var g=(S.goals||[]).filter(function(x){ return x.started && x.now; })[0];
  return g ? {text:g.now, theme:g.title} : null;
}
function renderNextCard(overrideText){
  var box=document.getElementById('nextCard');
  if(!box) return;
  var step=pickNextStep();
  var ag=activeGoalNow();
  if(ag && !step.done){ step.theme=ag.theme; }
  var txt = overrideText || (ag && !step.done ? ag.text : t(step.key));
  if(step.done && !overrideText){
    box.innerHTML='<div class="next done">'+ic('check')+
      '<div><div class="next-lab">'+esc(t('d.next'))+'</div>'+
      '<p class="next-tx">'+esc(t('d.allclear'))+'</p></div></div>';
    return;
  }
  var running = !!fiveTimer;
  box.innerHTML='<div class="next">'+
    '<div class="next-lab">'+ic('rocket')+'<span>'+esc(t('d.next'))+'</span>'+
      (step.theme?'<span class="next-th">'+esc(step.theme)+'</span>':'')+'</div>'+
    '<p class="next-tx">'+esc(txt)+'</p>'+
    '<p class="next-sub">'+esc(t('d.next.s'))+'</p>'+
    '<div class="next-btns">'+
      '<button class="btn btn-primary" id="fiveBtn"'+(running?' disabled':'')+'>'+ic('play')+
        '<span id="fiveTxt">'+esc(running?t('d.running',{t:'5:00'}):t('d.start5'))+'</span></button>'+
      '<button class="btn btn-ghost" id="nextDone">'+ic('check')+'<span>'+esc(t('d.mark'))+'</span></button>'+
    '</div></div>';
  var fb=document.getElementById('fiveBtn');
  if(fb) fb.addEventListener('click',function(){ startFiveMinutes(txt); });
  document.getElementById('nextDone').addEventListener('click',function(){
    clearFive();
    if(!S.next || S.next.done) return;
    S.next.done=true;
    S.stats.challenges=(S.stats.challenges||0)+1;
    addPts(25); markActiveToday();
    toast(t('t.pts',{n:25}));
    save(); renderNextCard(); renderDashStats(); renderStats(); checkAchievements();
  });
}

/* The areas the user chose during setup, shown back to them so the dashboard
   answers "what am I even aiming at" without opening another tab. */
function renderDashFocus(){
  var box=document.getElementById('dashFocus');
  if(!box) return;
  var goal=(S.goals||[])[0];
  var chips=CATS.map(function(c){
    return '<span class="fchip">'+ic(c.icon)+esc(catName(c))+'</span>';
  }).join('');
  var ladder='';
  if(goal){
    ladder='<div class="mini-ladder">'+
      '<div><span>'+esc(t('gl.goal'))+'</span><b>'+esc(goal.title)+'</b></div>'+
      (goal.week?'<div><span>'+esc(t('gl.week'))+'</span><b>'+esc(goal.week)+'</b></div>':'')+
      (goal.today?'<div><span>'+esc(t('gl.today'))+'</span><b>'+esc(goal.today)+'</b></div>':'')+
      '</div>'+
      (goal.started ? '' :
        '<button class="btn btn-primary btn-sm" data-gstart="'+goal.id+'">'+ic('play')+'<span>'+esc(t('gc.start'))+'</span></button>');
  }
  box.innerHTML=ladder+'<div class="fchips">'+chips+'</div>'+
    '<button class="btn btn-ghost btn-sm" data-goto="goals">'+ic('target')+
    '<span>'+esc(t('a.tab.goals'))+'</span></button>'+
    '<button class="btn btn-quiet btn-sm" data-goto="tasks">'+esc(t('d.seeall'))+'</button>';
  box.querySelectorAll('[data-goto]').forEach(function(b){
    b.addEventListener('click',function(){ goPage(b.dataset.goto); });
  });
  box.querySelectorAll('[data-gstart]').forEach(function(b){
    b.addEventListener('click',function(){ startGoal(goalById(Number(b.dataset.gstart))); });
  });
}
/* The same three facts onboarding asked for, editable later. Age feeds the
   check-in band and the training plan; gender re-renders every string. */
function renderSettings(){
  var n=document.getElementById('pfName'), a=document.getElementById('pfAge');
  if(n && document.activeElement!==n) n.value=P.name||'';
  if(a && document.activeElement!==a) a.value=P.age||'';
  var hint=document.getElementById('pfAgeBand');
  if(hint) hint.textContent = P.age ? t('ab.'+ageBand(P.age)) : '';
  var rm=document.getElementById('pfRemind');
  if(rm && document.activeElement!==rm) rm.value=P.remind||'17:00';
  renderLicState();
  document.querySelectorAll('#pfGender [data-pfg]').forEach(function(o){
    var on=o.dataset.pfg===P.gender;
    o.classList.toggle('on',on); o.setAttribute('aria-pressed',on?'true':'false');
  });
}
function bindSettings(){
  var n=document.getElementById('pfName'), a=document.getElementById('pfAge');
  if(n) n.addEventListener('change',function(){ P.name=n.value.trim(); save(); startApp(); });
  if(a) a.addEventListener('change',function(){
    var v=parseInt(a.value,10);
    if(!(v>=13 && v<=120)){ toast(t('t.agerange')); a.value=P.age||''; return; }
    P.age=String(v); save(); startApp(); toast(t('gl.saved'));
  });
  document.querySelectorAll('#pfGender [data-pfg]').forEach(function(o){
    o.addEventListener('click',function(){ setGender(o.dataset.pfg); });
  });
  var rm=document.getElementById('pfRemind');
  if(rm) rm.addEventListener('change',function(){
    P.remind=rm.value||'17:00'; save(); toast(t('gl.saved'));
  });
}
function renderDash(){
  renderDashStats(); renderNextCard(); renderDashFocus();
  renderProfile('dashProfile', true);
}


/* ================= the Body tab gate =================
   The mini-apps are the one large block of value that is not the proactivity
   core, so they are where Pro sits. The tab still opens, still says what is
   inside, and offers the way in - it never just refuses. */
function renderBodyGate(){
  var lock=document.getElementById('bodyLock'), wrap=document.getElementById('bodyViews');
  if(!lock||!wrap) return;
  var open=isPro();
  wrap.hidden=!open; lock.hidden=open;
  if(!open) lock.innerHTML=lockHtml('pro.f.body');
}

/* ================= the trend =================
   One series - the proactivity score, check-in by check-in - so there is no
   legend to read and no second axis to confuse it with. Only the first and last
   points carry a printed number; the rest are on hover. */
var TREND={w:320,h:130,pt:14,pb:22,pl:30,pr:12};
function trendPoints(){
  var h=(S.hist||[]).slice(-12);
  var n=h.length, g=TREND;
  var iw=g.w-g.pl-g.pr, ih=g.h-g.pt-g.pb;
  return h.map(function(e,i){
    var v=checkinAvg(e);
    return { x: g.pl + (n===1 ? iw/2 : iw*i/(n-1)), y: g.pt + ih*(1-v/100), v: v, d: e.d };
  });
}
function renderTrend(){
  var box=document.getElementById('trendBox'); if(!box) return;
  if(!isPro()){ box.innerHTML=lockHtml('pro.f.trend'); return; }
  var h=S.hist||[];
  if(h.length<2){
    box.innerHTML='<div class="empty-state">'+ic('trending')+
      '<p>'+esc(t(h.length?'tr.one':'tr.none'))+'</p>'+
      (h.length?'<button class="btn btn-ghost btn-sm" data-retake>'+esc(t('tr.retake'))+'</button>':'')+
      '</div>';
    bindRetake(box); return;
  }
  var p=trendPoints(), g=TREND;
  var line=p.map(function(q,i){ return (i?'L':'M')+q.x.toFixed(1)+' '+q.y.toFixed(1); }).join(' ');
  var first=p[0], last=p[p.length-1], delta=last.v-first.v;
  /* grid at 0/50/100 only - enough to read the height, quiet enough to ignore */
  var grid=[0,50,100].map(function(v){
    var y=g.pt+(g.h-g.pt-g.pb)*(1-v/100);
    return '<line class="tg" x1="'+g.pl+'" y1="'+y.toFixed(1)+'" x2="'+(g.w-g.pr)+'" y2="'+y.toFixed(1)+'"/>'+
           '<text class="tl" x="'+(g.pl-6)+'" y="'+(y+3.5).toFixed(1)+'" text-anchor="end">'+v+'</text>';
  }).join('');
  var dots=p.map(function(q,i){
    var edge=(i===0||i===p.length-1);
    return '<circle class="td'+(edge?' edge':'')+'" cx="'+q.x.toFixed(1)+'" cy="'+q.y.toFixed(1)+'" r="'+(edge?4.5:3.5)+'" data-i="'+i+'"/>';
  }).join('');
  var labs=[first,last].map(function(q,i){
    return '<text class="tv" x="'+q.x.toFixed(1)+'" y="'+(q.y-9).toFixed(1)+'" text-anchor="'+(i?'end':'start')+'">'+q.v+'</text>';
  }).join('');
  box.innerHTML=
    '<p class="trend-head">'+esc(t('tr.t'))+
      '<span class="trend-delta '+(delta>0?'up':delta<0?'down':'')+'">'+(delta>0?'+':'')+delta+'</span></p>'+
    '<svg class="trend" viewBox="0 0 '+g.w+' '+g.h+'" role="img" '+
      'aria-label="'+esc(t('tr.aria',{a:first.v,b:last.v,n:p.length}))+'">'+
      grid+'<path class="tline" d="'+line+'"/>'+dots+labs+
      '<rect id="trendHit" x="'+g.pl+'" y="0" width="'+(g.w-g.pl-g.pr)+'" height="'+g.h+'" fill="transparent"/>'+
    '</svg>'+
    '<div class="trend-tip" id="trendTip" hidden></div>'+
    '<div class="dimdelta">'+dimDeltas()+'</div>'+
    '<p class="hint">'+esc(t('tr.since',{d:fmtDay(first.d)}))+'</p>'+
    '<button class="btn btn-ghost btn-sm" data-retake>'+esc(t('tr.retake'))+'</button>';
  bindTrendHover(box, p);
  bindRetake(box);
}
/* The five dimensions as text rather than a second series: five lines on one
   chart would be unreadable, and a second y-axis would be a lie. */
function dimDeltas(){
  var h=S.hist||[]; if(h.length<2) return '';
  var a=h[0].s, b=h[h.length-1].s;
  return ['init','goal','time','solve','plan'].map(function(k){
    var d=(b[k]|0)-(a[k]|0);
    return '<div class="dd"><span class="dd-k">'+esc(t('dim.'+k))+'</span>'+
      '<span class="dd-v '+(d>0?'up':d<0?'down':'')+'">'+(d>0?'+':'')+d+'</span></div>';
  }).join('');
}
function bindTrendHover(box, p){
  var hit=box.querySelector('#trendHit'), tip=box.querySelector('#trendTip');
  var svg=box.querySelector('svg.trend');
  if(!hit||!tip||!svg) return;
  function near(evt){
    var r=svg.getBoundingClientRect();
    var x=(evt.clientX-r.left)/r.width*TREND.w;
    var best=0, bd=1e9;
    p.forEach(function(q,i){ var d=Math.abs(q.x-x); if(d<bd){ bd=d; best=i; } });
    return best;
  }
  function show(evt){
    var i=near(evt), q=p[i]; if(!q) return;
    var r=svg.getBoundingClientRect();
    tip.hidden=false;
    tip.textContent=fmtDay(q.d)+' · '+q.v;
    tip.style.insetInlineStart=(q.x/TREND.w*r.width)+'px';
    svg.querySelectorAll('.td').forEach(function(c){ c.classList.toggle('hot', Number(c.dataset.i)===i); });
  }
  hit.addEventListener('pointermove',show);
  hit.addEventListener('pointerdown',show);
  hit.addEventListener('pointerleave',function(){
    tip.hidden=true; svg.querySelectorAll('.td').forEach(function(c){ c.classList.remove('hot'); });
  });
}
function bindRetake(box){
  var b=box.querySelector('[data-retake]');
  if(b) b.addEventListener('click',function(){
    restartQuiz();
    document.getElementById('app').style.display='none';
    document.getElementById('onboarding').style.display='block';
    showStep(4);
    renderQuiz();
  });
}

/* ================= tabs ================= */
/* One <nav> serves as top tabs on a wide screen and as the bottom bar on a
   phone, so there is a single set of buttons and a single source of truth. */
function goPage(name){
  document.querySelectorAll('.tab').forEach(function(x){
    var on=x.dataset.page===name;
    x.classList.toggle('on', on);
    x.setAttribute('aria-selected', on?'true':'false');
  });
  document.querySelectorAll('.page').forEach(function(p){
    p.classList.toggle('on', p.id==='page-'+name);
  });
  try{ localStorage.setItem('proactive_tab', name); }catch(e){}
  if(name==='home') renderDash();
  if(name==='progress'){ renderProfile('profBody'); renderAchievements(); renderSettings(); renderTrend(); }
  if(name==='body') renderBodyGate();
  window.scrollTo(0,0);
}
document.querySelectorAll('.tab').forEach(function(tab){
  tab.addEventListener('click',function(){ goPage(tab.dataset.page); });
});
function lastTab(){
  try{
    var v=localStorage.getItem('proactive_tab');
    if(v && document.getElementById('page-'+v)) return v;
  }catch(e){}
  return 'home';
}

/* ================= boot ================= */
function renderTasks(){ renderRing(); renderCats(); }
function renderHome(){ renderTasks(); }   // kept: other modules still call it

function startApp(){
  var name=P.name || t('a.greet.anon');
  document.getElementById('greetName').textContent=t('a.greet',{name:name});
  document.getElementById('proQuote').textContent=t(pick(QUOTES));
  try{
    document.getElementById('dateStr').textContent=
      new Date().toLocaleDateString(cur,{weekday:'long',day:'numeric',month:'long'});
  }catch(e){ document.getElementById('dateStr').textContent=''; }

  var wp=buildWorkout(P.age,P.workout,P.fitLevel);
  document.getElementById('woSub').textContent=
    t(wp.ageBandKey)+' · '+t(wp.levelKey)+' · '+t('wo.'+P.workout);
  document.getElementById('woInfo').innerHTML=ic('sliders')+'<span>'+esc(wp.note)+'</span>';

  fillMissionCats(); renderInsight(); renderTasks(); renderGoals(); renderWeek();
  renderPlan('woGrid', wp.blocks, 'w');   // the "my weekly plan" section of the sport mini-app
  renderPlan('hyGrid', buildHygiene(), 'hy');
  renderTheories(); renderLessons(); renderAchievements(); renderSettings();
  renderStats(); renderTrial(); renderTrend(); renderBodyGate(); renderCheckout();
  revalidateLicense(); showInstall();
  renderMini();                            // the skincare routine lives in its mini-app
  renderDash();
  checkAchievements();
  goPage(lastTab());
}

document.querySelectorAll('.langbtn').forEach(function(b){
  b.addEventListener('click',function(){ setLang(b.dataset.lang); });
});

bindMini();
bindAccentPick();
bindGenderPick();
bindAgeInput();
bindSettings();
bindLicense();
bindBackup();
bindInstall();
loadLic();
registerSW();
loadGender();
loadChain();
loadLook();
applyTheme();
loadQuiz();
applyLang();
renderGoalOpts();
['oTime','oWO','oFL','oSkin'].forEach(function(id){
  var attr={oTime:'time',oWO:'wo',oFL:'fl',oSkin:'skin'}[id];
  var field={oTime:'time',oWO:'workout',oFL:'fitLevel',oSkin:'skinType'}[id];
  singleSelect(id,attr,field);
});
markSelected();

if(load()){
  loadLook(); loadGender(); applyTheme();     // the profile may carry an older look; the keys win
  buildCats();
  document.getElementById('landing').style.display='none';
  document.body.classList.remove('has-sticky');
  document.getElementById('stickyCta').style.display='none';
  document.getElementById('app').style.display='block';
  document.body.classList.add('in-app');
  renderGoalOpts(); markSelected();
  startApp();
}
"""
