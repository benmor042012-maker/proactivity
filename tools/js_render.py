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
    if(goalEditId===g.id){
      card.innerHTML='<h3>'+ic('target')+'<span>'+esc(t('ge.btn'))+'</span></h3>'+goalEditForm(g);
      box.appendChild(card); bindGoalEdit(card,g);
      return;
    }
    card.innerHTML=
      '<h3>'+ic('target')+'<span>'+esc(g.title)+'</span>'+
      '<button class="icon-btn" data-ge-open="'+g.id+'" aria-label="'+esc(t('ge.btn'))+'">'+ic('edit')+'</button>'+
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
  box.querySelectorAll('[data-ge-open]').forEach(function(b){
    b.addEventListener('click',function(){ goalEditId=Number(b.dataset.geOpen); renderGoals(); renderMyGoal(); });
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
  renderDashStats(); renderAvatarCard();
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
/* Deliberately narrow: the next step first, then one quiet line of numbers.
   Big tiles full of zeros told a beginner nothing but "zero". The full task
   list, the avatar and the profile live on their own tabs. */
function renderDashStats(){
  var box=document.getElementById('dashStats');
  if(!box) return;
  var s=stageInfo(), li=levelInfo();
  var cells=[
    {ic:'star',   v:t('a.level')+' '+s.level, k:s.stage},
    {ic:'flame',  v:shownStreak(),            k:t('d.streak')},
    {ic:'target', v:(S.goals||[]).length,     k:t('d.goals')}
  ];
  box.innerHTML='<h2 class="sr">'+esc(t('d.progress'))+'</h2>'+
    '<div class="dstrip-row">'+cells.map(function(c){
      return '<div class="dchip">'+ic(c.ic)+'<b class="numf">'+esc(String(c.v))+'</b>'+
        '<span>'+esc(c.k)+'</span></div>';
    }).join('')+'</div>'+
    '<div class="xp"><i style="width:'+s.progress+'%"></i></div>'+
    '<p class="xp-n">'+esc(t('av.next',{n:li.need, l:li.level+1}))+'</p>';
}

/* ---- the five-minute starter, on the goal card's step ---- */
var fiveTimer=null, fiveLeft=0, fiveGid=null;   // which goal the running five minutes belong to
function clearFive(){
  if(fiveTimer){ clearInterval(fiveTimer); fiveTimer=null; }
}
function startFiveMinutes(labelText){
  clearFive();
  fiveLeft=5*60;
  markActiveToday(); tip('task.skip');
  goPage('home');
  renderMyGoal();
  fiveTimer=setInterval(function(){
    fiveLeft--;
    var el=document.getElementById('fiveTxt');
    if(el){
      var m=Math.floor(fiveLeft/60), sec=String(fiveLeft%60).padStart(2,'0');
      el.textContent=t('d.running',{t:m+':'+sec});
    }
    if(fiveLeft<=0){ clearFive(); toast(t('d.timeup')); renderMyGoal(); }
  },1000);
}

/* ---- asked once on Home if it was never answered ----
   Accounts made before the question was required still read "מתחיל/ה".
   One tap answers it, and the card does not come back. */
function renderGenderAsk(){
  var box=document.getElementById('gndBox'); if(!box) return;
  box.hidden = GENDERS.indexOf(P.gender)>=0;
  if(box.dataset.bound) return;
  box.dataset.bound='1';
  box.querySelectorAll('[data-hgnd]').forEach(function(o){
    o.addEventListener('click',function(){ setGender(o.dataset.hgnd); save(); box.hidden=true; toast(t('gl.saved')); });
  });
}

/* ---- my day: the same small ritual for everyone, every morning ----
   Three things that matter today, written by the user, before the
   personal step. A new day starts with three empty lines. */
function today3(){
  var d=dayKey();
  if(!S.today3 || S.today3.day!==d)
    S.today3={day:d, items:[0,1,2].map(function(){ return {t:'', done:false, paid:false, gid:null}; })};
  return S.today3;
}
/* In the order they were made, so a new goal joins the list under the
   others instead of pushing the first one down. */
function liveGoals(){
  return (S.goals||[]).filter(function(g){ return !g.archived; }).sort(function(a,b){ return a.id-b.id; });
}
/* The day's record, rewritten on every change so the last state of a day is
   what stays: the three lines (text, done, which goal they serve) and which
   goals' own step was done. That is what My week reads. */
var LOG_DAYS=120;
function logDay(){
  var td=today3();
  if(!S.log) S.log={};
  var prev=S.log[td.day]||{};
  S.log[td.day]={
    note: prev.note||'', feel: prev.feel||'',
    items: td.items.filter(function(x){ return x.t.trim(); })
             .map(function(x){ return {t:x.t.trim(), done:!!x.done, gid:x.gid||null}; }),
    steps: (S.goals||[]).filter(function(g){ return g.doneDay===td.day; }).map(function(g){ return g.id; })
  };
  var days=Object.keys(S.log).sort();
  while(days.length>LOG_DAYS) delete S.log[days.shift()];
}
function renderToday3(){
  var box=document.getElementById('todayBox'); if(!box) return;
  var td=today3(), goals=liveGoals();
  var n=td.items.filter(function(x){ return x.done; }).length;
  box.innerHTML='<div class="boxh-row"><h2 class="boxh">'+ic('sun')+'<span>'+esc(t('t3.t'))+'</span></h2>'+
      '<span class="boxh-n numf">'+n+'/3</span></div>'+
    '<p class="psub">'+esc(t('t3.s'))+'</p>'+
    td.items.map(function(it,i){
      var ph=t('t3.ph',{n:i+1}), lg=it.gid ? goalById(it.gid) : null;
      return '<div class="t3row'+(it.done?' done':'')+'">'+
        '<button type="button" class="t3chk" data-t3="'+i+'" aria-pressed="'+(it.done?'true':'false')+'"'+
          ' aria-label="'+esc(t('t3.mark'))+'"'+(it.t.trim()?'':' disabled')+'>'+ic('check')+'</button>'+
        '<input type="text" maxlength="80" data-t3in="'+i+'" value="'+esc(it.t)+'"'+
          ' placeholder="'+esc(ph)+'" aria-label="'+esc(ph)+'">'+
        (goals.length ? '<button type="button" class="t3goal'+(lg?' on':'')+'" data-t3g="'+i+'"'+
          ' aria-pressed="'+(lg?'true':'false')+'" aria-label="'+esc(t('t3.link'))+'" title="'+esc(t('t3.link'))+'">'+ic('target')+'</button>' : '')+
        '</div>'+
        (lg ? '<div class="t3tag">'+ic('target')+'<span>'+esc(lg.title)+'</span></div>' : '');
    }).join('')+
    (goals.length ? '<p class="hint t3hint">'+esc(t('t3.link.h'))+'</p>' : '');
  box.querySelectorAll('[data-t3in]').forEach(function(inp){
    inp.addEventListener('input',function(){
      var i=Number(inp.dataset.t3in), it=today3().items[i];
      it.t=inp.value; logDay(); save();
      box.querySelector('[data-t3="'+i+'"]').disabled=!inp.value.trim();
    });
  });
  box.querySelectorAll('[data-t3]').forEach(function(b){
    b.addEventListener('click',function(){
      var td=today3(), it=td.items[Number(b.dataset.t3)];
      it.done=!it.done;
      if(it.done){
        markActiveToday();
        if(!it.paid){ it.paid=true; addPts(10); }
        var all=td.items.every(function(x){ return x.done; });
        toast(all ? t('t3.all') : t('t.pts',{n:10}));
        if(all) celebrate();
      }
      logDay(); save(); renderToday3(); renderEvening(); renderDashStats(); checkAchievements();
    });
  });
  /* Tapping the target walks through the live goals and back to none, so
     with one goal it is a plain on/off. */
  box.querySelectorAll('[data-t3g]').forEach(function(b){
    b.addEventListener('click',function(){
      var it=today3().items[Number(b.dataset.t3g)], ids=liveGoals().map(function(g){ return g.id; });
      var k=ids.indexOf(it.gid);
      it.gid = k<0 ? ids[0] : (k+1<ids.length ? ids[k+1] : null);
      logDay(); save(); renderToday3();
    });
  });
}

/* ---- the end of the day: one line about yourself ----
   From five in the evening, or earlier once the day's three things are all
   done, Home asks how the day was: a feeling in one tap and one optional
   line. Both go into the day's record and show up in My week. At the end
   of the week (Friday and Saturday) the same card points to the week's
   reflection until it is written. */
var FEELS=[{k:'energy',e:'⚡'},{k:'calm',e:'🌿'},{k:'proud',e:'🌟'},{k:'tired',e:'🌙'}];
var eveEdit=false;
function weekKey(d){
  d=d?new Date(d):new Date(); d.setDate(d.getDate()-d.getDay());   // the week starts on Sunday
  return dayKey(d);
}
function eveTime(){
  var td=today3(), all=td.items.filter(function(x){ return x.t.trim(); });
  return new Date().getHours()>=17 || (all.length && all.every(function(x){ return x.done; }));
}
function renderEvening(){
  var box=document.getElementById('eveBox'); if(!box) return;
  var wd=new Date().getDay(), weekEnd=(wd===5||wd===6), weekDone=!!(S.weeks&&S.weeks[weekKey()]);
  var showWeek=weekEnd && !weekDone;
  if(!eveTime() && !showWeek){ box.hidden=true; return; }
  box.hidden=false;
  logDay();
  var L=S.log[dayKey()];
  var weekNudge = showWeek
    ? '<div class="eve-week">'+ic('calendar')+'<span>'+esc(t('ev.week'))+'</span>'+
        '<button class="btn btn-ghost btn-sm" data-eve-week>'+esc(t('ev.week.go'))+'</button></div>' : '';
  if(!eveTime()){ box.innerHTML=weekNudge; bindEveWeek(); return; }
  var head='<h2 class="boxh">'+ic('moon')+'<span>'+esc(t('ev.t'))+'</span></h2>';
  if((L.note||L.feel) && !eveEdit){
    var f=FEELS.filter(function(x){ return x.k===L.feel; })[0];
    box.innerHTML=head+
      '<p class="eve-saved">'+(f?'<span class="eve-e">'+f.e+'</span>'+esc(t('ev.f.'+f.k)):'')+
        (L.note?(f?' · ':'')+'<q>'+esc(L.note)+'</q>':'')+'</p>'+
      '<p class="next-sub">'+esc(t('ev.thanks'))+'</p>'+
      '<button class="btn btn-quiet btn-sm" data-eve-edit>'+ic('edit')+'<span>'+esc(t('ge.btn'))+'</span></button>'+
      weekNudge;
    box.querySelector('[data-eve-edit]').addEventListener('click',function(){ eveEdit=true; renderEvening(); });
    bindEveWeek(); return;
  }
  box.innerHTML=head+'<p class="psub">'+esc(t('ev.s'))+'</p>'+
    '<div class="eve-feels">'+FEELS.map(function(x){
      return '<button type="button" class="opt'+(L.feel===x.k?' on':'')+'" data-feel="'+x.k+'" aria-pressed="'+(L.feel===x.k)+'">'+
        '<span class="eve-e">'+x.e+'</span><span>'+esc(t('ev.f.'+x.k))+'</span></button>';
    }).join('')+'</div>'+
    '<div class="field"><label for="eveNote">'+esc(t('ev.q'))+'</label>'+
      '<input type="text" id="eveNote" maxlength="140" value="'+esc(L.note||'')+'" placeholder="'+esc(t('ev.ph'))+'"></div>'+
    '<button class="btn btn-primary btn-sm" data-eve-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
    weekNudge;
  var pick=L.feel;
  box.querySelectorAll('[data-feel]').forEach(function(b){
    b.addEventListener('click',function(){
      pick = pick===b.dataset.feel ? '' : b.dataset.feel;
      box.querySelectorAll('[data-feel]').forEach(function(o){
        var on=o.dataset.feel===pick; o.classList.toggle('on',on); o.setAttribute('aria-pressed',on); });
    });
  });
  box.querySelector('[data-eve-save]').addEventListener('click',function(){
    var L=S.log[dayKey()];
    L.note=document.getElementById('eveNote').value.trim(); L.feel=pick||'';
    if(!L.note && !L.feel){ document.getElementById('eveNote').focus(); return; }
    eveEdit=false; markActiveToday(); save(); toast(t('ev.thanks')); renderEvening();
  });
  bindEveWeek();
}
function bindEveWeek(){
  var b=document.querySelector('[data-eve-week]');
  if(b) b.addEventListener('click',function(){
    goPage('progress');
    var r=document.getElementById('weekRefl'); if(r) r.scrollIntoView({block:'start',behavior:'smooth'});
  });
}

/* ---- my week: what the days held, next to what the goal asked ----
   The last seven days from the log. Under the table, three plain readings:
   how much of what got done served the goal, how many days the goal's own
   step happened, and which lines keep coming back - a line that returns
   every day and serves no goal is often the real goal. */
function weekDays(){
  var out=[], d=new Date();
  for(var i=6;i>=0;i--){ var x=new Date(d); x.setDate(d.getDate()-i); out.push(dayKey(x)); }
  return out;
}
function normLine(s){ return String(s||'').trim().toLowerCase().replace(/\s+/g,' '); }
function renderMyWeek(){
  var box=document.getElementById('weekBox'); if(!box) return;
  var log=S.log||{}, days=weekDays().filter(function(d){ var L=log[d]; return L && (L.items.length || L.steps.length || L.note || L.feel); });
  var head='<h3 class="boxh">'+ic('calendar')+'<span>'+esc(t('wk3.t'))+'</span></h3><p class="psub">'+esc(t('wk3.s'))+'</p>';
  if(!days.length){ box.innerHTML=head+'<p class="hint">'+esc(t('wk3.none'))+'</p>'+weekReflection(); bindWeekReflection(box); return; }
  var goals=liveGoals();
  function dayName(k){
    try{ return new Date(k+'T00:00:00').toLocaleDateString(cur,{weekday:'short',day:'numeric',month:'numeric'}); }catch(e){ return k; }
  }
  var rows=days.slice().reverse().map(function(d){
    var L=log[d];
    var chips=L.items.map(function(x){
      var lg=x.gid && goalById(x.gid);
      return '<span class="wk3chip'+(x.done?' done':'')+(lg?' goal':'')+'">'+
        (x.done?ic('check'):'')+esc(x.t)+(lg?ic('target'):'')+'</span>';
    }).join('');
    var stepped=goals.filter(function(x){ return L.steps.indexOf(x.id)>=0; }).length;
    var f=FEELS.filter(function(x){ return x.k===L.feel; })[0];
    var note=(f||L.note) ? '<div class="wk3note">'+(f?f.e+' ':'')+(L.note?esc(L.note):esc(t('ev.f.'+f.k)))+'</div>' : '';
    return '<tr><th scope="row">'+esc(dayName(d))+'</th><td>'+(chips||'<span class="wk3dash">·</span>')+note+'</td>'+
      (goals.length?'<td class="wk3step">'+(stepped?ic('check')+(goals.length>1?'<b class="numf">'+stepped+'</b>':''):'<span class="wk3dash">·</span>')+'</td>':'')+'</tr>';
  }).join('');
  var all=[], done=0, served=0, rep={}, stepDays={};
  days.forEach(function(d){
    var L=log[d];
    L.items.forEach(function(x){
      all.push(x);
      var ok=x.gid && goalById(x.gid);
      if(x.done){ done++; if(ok) served++; }
      var k=normLine(x.t); if(!rep[k]) rep[k]={t:x.t, n:0, goal:false};
      rep[k].n++; if(ok) rep[k].goal=true;
    });
    L.steps.forEach(function(id){ stepDays[id]=(stepDays[id]||0)+1; });
  });
  var lines=[];
  if(done<3) lines.push('<p>'+esc(t('wk3.early'))+'</p>');
  else {
    lines.push('<p class="wk3sum">'+esc(t('wk3.sum',{n:done, m:served}))+'</p>');
    var r=served/done;
    lines.push('<p>'+esc(t(r>=.5?'wk3.good':r>=.25?'wk3.mid':'wk3.low'))+'</p>');
    if(r<.25 && goals.length) lines.push('<button class="btn btn-ghost btn-sm" data-wk3-fix>'+ic('edit')+'<span>'+esc(t('wk3.fix'))+'</span></button>');
  }
  /* per goal, and only goals whose step happened - a zero only reads as a reproach */
  goals.forEach(function(x){
    if(stepDays[x.id]) lines.push('<p>'+esc(t(goals.length>1?'wk3.steps.g':'wk3.steps',{g:x.title, k:stepDays[x.id], d:days.length}))+'</p>');
  });
  var back=Object.keys(rep).map(function(k){ return rep[k]; }).filter(function(x){ return x.n>=2; })
    .sort(function(a,b){ return b.n-a.n; }).slice(0,3);
  if(back.length){
    lines.push('<p>'+esc(t('wk3.rep'))+' '+back.map(function(x){ return '<b>'+esc(x.t)+'</b> ('+x.n+')'; }).join(' · ')+'</p>');
    var free=back.filter(function(x){ return !x.goal; })[0];
    if(free) lines.push('<p class="wk3idea">'+ic('sparkles')+'<span>'+esc(t('wk3.idea',{x:free.t}))+'</span></p>'+
      '<button class="btn btn-ghost btn-sm" data-wk3-new="'+esc(free.t)+'">'+ic('target')+'<span>'+esc(t('wk3.mk'))+'</span></button>');
  }
  box.innerHTML=head+
    '<div class="scroller"><table class="wk3"><thead><tr><th scope="col">'+esc(t('wk3.c.day'))+'</th>'+
      '<th scope="col">'+esc(t('wk3.c.did'))+'</th>'+(goals.length?'<th scope="col">'+esc(t('wk3.c.step'))+'</th>':'')+'</tr></thead>'+
      '<tbody>'+rows+'</tbody></table></div>'+
    (goals.length?'<p class="hint">'+ic('target')+'<span>'+esc(t(goals.length>1?'wk3.goals':'wk3.goal',{g:goals.map(function(x){ return x.title; }).join(' · ')}))+'</span></p>':'')+
    '<div class="wk3read">'+lines.join('')+'</div>'+
    (done ? '<button class="btn btn-primary btn-sm wk3share" data-wk3-share>'+ic('share')+'<span>'+esc(t('sh.btn'))+'</span></button>' : '')+
    weekReflection();
  bindWeekReflection(box);
  var shb=box.querySelector('[data-wk3-share]');
  if(shb) shb.addEventListener('click',function(){
    var feels={}; days.forEach(function(d){ var f=log[d].feel; if(f) feels[f]=(feels[f]||0)+1; });
    var top=Object.keys(feels).sort(function(a,b){ return feels[b]-feels[a]; })[0];
    var steps=0; Object.keys(stepDays).forEach(function(k){ steps+=stepDays[k]; });
    shareWeek({done:done, served:served, steps:steps, days:days.length, feel:top});
  });
  var fx=box.querySelector('[data-wk3-fix]');
  if(fx) fx.addEventListener('click',sharpenGoals);
  var nw=box.querySelector('[data-wk3-new]');
  if(nw) nw.addEventListener('click',function(){ openChainAt('goals', nw.dataset.wk3New); });
}

function sharpenGoals(){
  var gs=liveGoals();
  if(gs.length!==1){ goPage('goals'); return; }
  goalEditId=gs[0].id; goPage('home'); renderMyGoal();
  document.getElementById('myGoal').scrollIntoView({block:'start',behavior:'smooth'});
}

/* ---- the week as a picture to share ----
   Only numbers and the week's most common feeling - never the lines
   themselves, which may be private. */
function shareWeek(w){
  var W=1080,H=1350,c=document.createElement('canvas'); c.width=W; c.height=H;
  var x=c.getContext('2d'), rtl=document.documentElement.dir==='rtl';
  var g=x.createLinearGradient(0,H,W,0); g.addColorStop(0,'#E9F0E2'); g.addColorStop(1,'#FBF8F1');
  x.fillStyle=g; x.fillRect(0,0,W,H);
  x.direction=rtl?'rtl':'ltr'; x.textAlign='center';
  var serif=getComputedStyle(document.body).getPropertyValue('--f-display')||'sans-serif';
  function txt(s,y,size,col,weight){ x.font=(weight||700)+' '+size+'px '+serif; x.fillStyle=col; x.fillText(s,W/2,y); }
  txt(t('sh.title'),250,64,'#173F2A',800);
  /* zeros are left off: the picture is something to be proud of */
  var cells=[[w.done,t('sh.done')],[w.served,t('sh.served')],[w.steps,t('sh.steps')]].filter(function(cl){ return cl[0]>0; });
  var top=430+(3-cells.length)*125;
  cells.forEach(function(cl,i){
    var y=top+i*250;
    x.fillStyle='#FFFFFF'; x.beginPath(); (x.roundRect||function(a,b,c2,d){ this.rect(a,b,c2,d); }).call(x,140,y-120,W-280,200,40); x.fill();
    txt(String(cl[0]),y+5,110,'#3D7B5E',800);
    txt(cl[1],y+60,38,'#3E5A4A',600);
  });
  var f=w.feel && FEELS.filter(function(z){ return z.k===w.feel; })[0];
  if(f) txt(f.e+'  '+t('ev.f.'+f.k),1150,52,'#173F2A',700);
  txt('Proacty · '+t('n.hero.lead'),1270,40,'#3E5A4A',600);
  var img=new Image();
  img.onload=function(){ x.drawImage(img,W/2-60,40,120,120); out(); };
  img.onerror=out;
  img.src='icon-192.png';
  function out(){
    c.toBlob(function(blob){
      var file=new File([blob],'proacty-week.png',{type:'image/png'});
      if(navigator.canShare && navigator.canShare({files:[file]})){
        navigator.share({files:[file], text:t('sh.text')}).catch(function(){});
      } else {
        var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='proacty-week.png';
        document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },0);
        toast(t('sh.saved'));
      }
    },'image/png');
  }
}

/* ---- the week's reflection: what worked, what changes next week ----
   Kept per week (by its Sunday) in S.weeks; earlier ones fold away below,
   so it is possible to look back and see how the answers moved. */
function weekReflection(){
  var W=(S.weeks||{})[weekKey()]||{};
  var past=Object.keys(S.weeks||{}).filter(function(k){ return k!==weekKey(); }).sort().reverse().slice(0,8);
  return '<div class="wk3refl" id="weekRefl">'+
    '<h4>'+ic('sparkles')+'<span>'+esc(t('wr.t'))+'</span></h4>'+
    '<div class="field"><label for="wrGood">'+esc(t('wr.q1'))+'</label>'+
      '<textarea id="wrGood" rows="2" maxlength="300" placeholder="'+esc(t('wr.ph1'))+'">'+esc(W.good||'')+'</textarea></div>'+
    '<div class="field"><label for="wrNext">'+esc(t('wr.q2'))+'</label>'+
      '<textarea id="wrNext" rows="2" maxlength="300" placeholder="'+esc(t('wr.ph2'))+'">'+esc(W.next||'')+'</textarea></div>'+
    '<div class="row-btns">'+
      '<button class="btn btn-primary btn-sm" data-wr-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
      (liveGoals().length?'<button class="btn btn-ghost btn-sm" data-wr-fix>'+ic('edit')+'<span>'+esc(t('wk3.fix'))+'</span></button>':'')+
    '</div>'+
    (past.length ? '<details class="wr-past"><summary>'+esc(t('wr.past'))+'</summary>'+past.map(function(k){
        var w=S.weeks[k];
        return '<div class="wr-item"><b>'+esc(t('wr.of',{d:fmtDay(k)}))+'</b>'+
          (w.good?'<p><span>'+esc(t('wr.q1'))+'</span> '+esc(w.good)+'</p>':'')+
          (w.next?'<p><span>'+esc(t('wr.q2'))+'</span> '+esc(w.next)+'</p>':'')+'</div>';
      }).join('')+'</details>' : '')+
    '</div>';
}
function bindWeekReflection(box){
  var sv=box.querySelector('[data-wr-save]');
  if(sv) sv.addEventListener('click',function(){
    var good=document.getElementById('wrGood').value.trim(), next=document.getElementById('wrNext').value.trim();
    if(!good && !next){ document.getElementById('wrGood').focus(); return; }
    if(!S.weeks) S.weeks={};
    S.weeks[weekKey()]={good:good, next:next, at:dayKey()};
    markActiveToday(); save(); toast(t('wr.saved')); celebrate(); renderEvening();
  });
  var fx=box.querySelector('[data-wr-fix]');
  if(fx) fx.addEventListener('click',sharpenGoals);
}

/* ---- editing a goal: the name and its ladder, in one small form ----
   The weekly mission made when the goal started carries the goal's name,
   so it is renamed with it. */
var goalEditId=null;
function goalEditForm(g){
  function row(f,lab,ph){
    return '<div class="field"><label for="ge-'+f+'">'+esc(t(lab))+'</label>'+
      '<input type="text" id="ge-'+f+'" data-ge="'+f+'" maxlength="100" value="'+esc(g[f]||'')+'"'+
      (ph?' placeholder="'+esc(t(ph))+'"':'')+'></div>';
  }
  return '<div class="gedit">'+
    row('title','gl.goal')+row('week','gl.week','gl.wk.ph')+
    row('today','gl.today','gl.td.ph')+row('now','gl.now','ge.now.ph')+
    '<div class="row-btns">'+
      '<button class="btn btn-primary btn-sm" data-ge-save>'+ic('check')+'<span>'+esc(t('c.save'))+'</span></button>'+
      '<button class="btn btn-ghost btn-sm" data-ge-cancel>'+esc(t('c.cancel'))+'</button>'+
    '</div></div>';
}
function bindGoalEdit(host,g){
  host.querySelector('[data-ge-save]').addEventListener('click',function(){
    var v={};
    host.querySelectorAll('[data-ge]').forEach(function(i){ v[i.dataset.ge]=i.value.trim(); });
    if(!v.title){ toast(t('t.writegoal')); host.querySelector('[data-ge="title"]').focus(); return; }
    g.title=v.title; g.week=v.week; g.today=v.today; g.now=v.now;
    (S.missions||[]).forEach(function(m){ if(m.goalId===g.id) m.title=g.title; });
    goalEditId=null;
    save(); renderGoals(); renderWeek(); renderDash(); toast(t('gl.saved'));
  });
  host.querySelector('[data-ge-cancel]').addEventListener('click',function(){
    goalEditId=null; renderGoals(); renderDash();
  });
}

/* ---- my goal, and today's step toward it ----
   One card: the goal, the step for today taken from its own ladder (right
   now, else today, else this week), and the two ways to act on it. A
   separate "next step" card used to repeat the same line under it. With no
   goal yet it offers the areas and a free line; both go on into the same
   chain the Goals tab uses, so a goal made here has a full ladder. */
function openChainAt(area, kindText){
  if(goalLimitReached()){ toast(t('pro.goalmax',{n:GOAL_FREE_MAX})); openPlans(); return; }
  resetChain();
  CH.area=area; CH.step=1;
  if(kindText){ CH.kind='other'; CH.kindText=kindText; CH.step=2; }
  saveChain();
  goPage('goals');
  var host=document.getElementById('goalChain'); host.hidden=false;
  document.getElementById('newGoalBtn').hidden=true;
  renderChain('goalChain');
  host.scrollIntoView({block:'start',behavior:'smooth'});
}
function renderMyGoal(){
  var box=document.getElementById('myGoal'); if(!box) return;
  var goals=liveGoals();
  var head='<h2 class="boxh">'+ic('target')+'<span>'+esc(t(goals.length>1?'mg.tn':'mg.t'))+'</span></h2>';
  if(!goals.length){ renderGoalPicker(box,head,false); return; }
  var running=!!fiveTimer;
  var blocks=goals.map(function(g){
    if(goalEditId===g.id) return '<div class="mg-goal" data-gblock="'+g.id+'">'+goalEditForm(g)+'</div>';
    var step=g.now||g.today||g.week||'';
    var act = !step
      ? '<p class="next-sub">'+esc(t('mg.nostep'))+'</p>'
      : g.doneDay===dayKey()
      ? '<p class="mg-done">'+ic('check')+'<span>'+esc(t('mg.done'))+'</span></p>'
      : '<div class="next-btns">'+
          '<button class="btn btn-primary" data-mg-five="'+g.id+'"'+(running?' disabled':'')+'>'+ic('play')+
            '<span'+(fiveGid===g.id?' id="fiveTxt"':'')+'>'+esc(running&&fiveGid===g.id?t('d.running',{t:'5:00'}):t('d.start5'))+'</span></button>'+
          '<button class="btn btn-ghost" data-mg-done="'+g.id+'">'+ic('check')+'<span>'+esc(t('d.mark'))+'</span></button>'+
        '</div>';
    return '<div class="mg-goal" data-gblock="'+g.id+'">'+
      '<p class="mg-title">'+esc(g.title)+'</p>'+
      (step?'<div class="mg-lab">'+esc(t('mg.today'))+'</div><p class="next-tx">'+esc(step)+'</p>':'')+
      act+
      '<div class="row-btns mg-tools">'+
        (g.started ? '' : '<button class="btn btn-quiet btn-sm" data-mg-start="'+g.id+'">'+ic('flag')+'<span>'+esc(t('gc.start'))+'</span></button>')+
        '<button class="btn btn-quiet btn-sm" data-mg-edit="'+g.id+'">'+ic('edit')+'<span>'+esc(t('ge.btn'))+'</span></button>'+
      '</div></div>';
  }).join('');
  box.innerHTML=head+blocks+
    '<p class="next-sub">'+esc(streakLine())+'</p>'+
    '<div class="row-btns mg-tools">'+
      '<button class="btn btn-ghost btn-sm" data-mg-add>'+ic('plus')+'<span>'+esc(t('mg.add'))+'</span></button>'+
      '<button class="btn btn-ghost btn-sm" data-mg-all>'+ic('target')+'<span>'+esc(t('mg.all'))+'</span></button>'+
    '</div>';
  goals.forEach(function(g){
    if(goalEditId===g.id) bindGoalEdit(box.querySelector('[data-gblock="'+g.id+'"]'),g);
  });
  box.querySelectorAll('[data-mg-edit]').forEach(function(b){
    b.addEventListener('click',function(){ goalEditId=Number(b.dataset.mgEdit); renderMyGoal(); });
  });
  box.querySelectorAll('[data-mg-start]').forEach(function(b){
    b.addEventListener('click',function(){ startGoal(goalById(Number(b.dataset.mgStart))); });
  });
  box.querySelectorAll('[data-mg-five]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.mgFive)); fiveGid=g.id;
      startFiveMinutes(g.now||g.today||g.week);
    });
  });
  box.querySelectorAll('[data-mg-done]').forEach(function(b){
    b.addEventListener('click',function(){
      var g=goalById(Number(b.dataset.mgDone));
      if(fiveGid===g.id) clearFive();
      g.doneDay=dayKey(); logDay();
      S.stats.challenges=(S.stats.challenges||0)+1;
      addPts(25); markActiveToday();
      toast(t('t.pts',{n:25})); celebrate();
      save(); renderMyGoal(); renderDashStats(); renderStats(); checkAchievements();
    });
  });
  box.querySelector('[data-mg-add]').addEventListener('click',function(){ renderGoalPicker(box,head,true); });
  box.querySelector('[data-mg-all]').addEventListener('click',function(){ goPage('goals'); });
}
/* The areas and a free line - the way into a first goal, and into the next. */
function renderGoalPicker(box,head,more){
  box.innerHTML=head+'<p class="psub">'+esc(t(more?'mg.s2':'mg.s'))+'</p>'+
    '<div class="opts mg-areas">'+AREAS.map(function(a){
      return '<button type="button" class="opt" data-mg-area="'+a.id+'">'+ic(a.icon)+'<span>'+esc(t('ga.'+a.id))+'</span></button>';
    }).join('')+'</div>'+
    '<div class="addrow mg-free"><input type="text" id="mgText" maxlength="80"'+
      ' placeholder="'+esc(t('mg.ph'))+'" aria-label="'+esc(t('gc.free'))+'">'+
      '<button class="btn btn-primary" id="mgGo">'+esc(t('c.next'))+'</button></div>'+
    (more?'<button class="btn btn-quiet btn-sm mg-back" data-mg-back>'+esc(t('c.cancel'))+'</button>':'');
  box.querySelectorAll('[data-mg-area]').forEach(function(b){
    b.addEventListener('click',function(){ openChainAt(b.dataset.mgArea); });
  });
  var inp=document.getElementById('mgText');
  function go(){ var v=inp.value.trim(); if(!v){ inp.focus(); return; } openChainAt('goals', v); }
  document.getElementById('mgGo').addEventListener('click',go);
  inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); go(); } });
  var bk=box.querySelector('[data-mg-back]');
  if(bk) bk.addEventListener('click',renderMyGoal);
}

/* The same three facts onboarding asked for, editable later. Age feeds the
   check-in band and the training plan; gender re-renders every string. */
function renderSettings(){
  var n=document.getElementById('pfName'), a=document.getElementById('pfAge');
  if(n && document.activeElement!==n) n.value=P.name||'';
  if(a && document.activeElement!==a) a.value=P.age||'';
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
    if(!(v>=AGE_MIN && v<=AGE_MAX)){ toast(t('t.agerange')); a.value=P.age||''; return; }
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
  renderGenderAsk(); renderToday3(); renderMyGoal(); renderEvening(); renderDashStats();
  renderAvatarCard(); renderInvite();
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
  if(name==='progress'){ renderMyWeek(); renderProfile('profBody'); renderAchievements(); renderSettings(); renderTrend(); }
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

  var wp=buildWorkout(P.age,P.workout,P.fitLevel);
  document.getElementById('woSub').textContent=
    t(wp.levelKey)+' · '+t('wo.'+P.workout);
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
bindQuizAge();
bindSettings();
bindLicense();
bindPay();
bindBackup();
bindInstall();
loadLic();
loadPaid();
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
captureRefParam();                 /* before load(): a ?ref= only counts on a fresh device */

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
