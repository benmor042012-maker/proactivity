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
  save(); renderHome();
}
function toggleTask(id){
  var task=null;
  S.tasks.forEach(function(x){ if(x.id===id) task=x; });
  if(!task) return;
  if(task.done){
    task.done=false; task.photo=null; addPts(-10);
    S.streak=Math.max(0,S.streak-1); renderHome(); renderStats(); return;
  }
  openCam(label(task), function(photo){
    task.photo=photo; task.done=true; addPts(10); S.streak++;
    toast(praise()); save(); renderHome(); renderStats();
  });
}
function delTask(id){
  S.tasks=S.tasks.filter(function(x){ return x.id!==id; });
  save(); renderHome(); renderStats();
}

function renderRing(){
  var svg=document.getElementById('rSvg');
  var r=54, cx=66, cy=66, sw=10, circ=2*Math.PI*r;
  var total=S.tasks.length;
  if(!total){
    svg.innerHTML='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="#2A2A30" stroke-width="'+sw+'" stroke-dasharray="3 7"/>';
    document.getElementById('rPct').textContent='0%'; return;
  }
  var out='', off=0;
  CATS.forEach(function(cat){
    var ct=S.tasks.filter(function(x){ return x.catId===cat.id; });
    if(!ct.length) return;
    var done=ct.filter(function(x){ return x.done; }).length;
    var seg=(ct.length/total)*circ, filled=seg*(done/ct.length);
    out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="#2A2A30" stroke-width="'+sw+'" stroke-dasharray="'+(seg-2)+' '+(circ-seg+2)+'" stroke-dashoffset="'+(-off)+'"/>';
    if(filled>0)
      out+='<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" fill="none" stroke="#FF5A1F" stroke-width="'+sw+'" stroke-linecap="round" stroke-dasharray="'+Math.max(0,filled-2)+' '+(circ-filled+2)+'" stroke-dashoffset="'+(-off)+'"/>';
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
function renderGoals(){
  var box=document.getElementById('goalsCont'); box.innerHTML='';
  if(!S.goals.length){ box.innerHTML='<div class="empty">'+esc(t('g.empty'))+'</div>'; return; }
  S.goals.forEach(function(g){
    var done=g.actions.filter(function(a){ return a.done; }).length;
    var pct=g.actions.length ? Math.round(done/g.actions.length*100) : 0;
    var card=document.createElement('div'); card.className='goal';
    card.innerHTML=
      '<h3>'+ic('target')+'<span>'+esc(g.title)+'</span>'+
      '<button class="icon-btn" data-dg="'+g.id+'" aria-label="'+esc(t('c.delete'))+'">'+ic('trash')+'</button></h3>'+
      '<div class="acts">'+g.actions.map(function(a){
        return '<label><input type="checkbox" class="cb" data-gid="'+g.id+'" data-aid="'+a.id+'"'+
          (a.done?' checked':'')+'><span'+(a.done?' class="done"':'')+'>'+esc(actLabel(a))+'</span></label>';
      }).join('')+'</div>'+
      '<div class="addrow"><input type="text" class="na" data-gid="'+g.id+'" placeholder="'+esc(t('g.step.ph'))+'">'+
      '<button class="btn btn-ghost" data-na="'+g.id+'">'+ic('plus')+'</button></div>'+
      '<div class="gmeta"><span class="numf">'+done+'/'+g.actions.length+'</span><span class="numf">'+pct+'%</span></div>'+
      '<div class="gbar"><i style="width:'+pct+'%"></i></div>';
    box.appendChild(card);
  });
  box.querySelectorAll('.cb').forEach(function(cb){
    cb.addEventListener('change',function(e){
      var g=null,a=null;
      S.goals.forEach(function(x){ if(x.id===Number(e.target.dataset.gid)) g=x; });
      if(!g) return;
      g.actions.forEach(function(x){ if(x.id===Number(e.target.dataset.aid)) a=x; });
      if(!a) return;
      a.done=e.target.checked; addPts(a.done?12:-12);
      if(a.done) toast(t('t.step'));
      save(); renderGoals(); renderStats();
    });
  });
  box.querySelectorAll('[data-dg]').forEach(function(b){
    b.addEventListener('click',function(){
      S.goals=S.goals.filter(function(g){ return g.id!==Number(b.dataset.dg); });
      save(); renderGoals();
    });
  });
  box.querySelectorAll('[data-na]').forEach(function(b){
    b.addEventListener('click',function(){
      var gid=Number(b.dataset.na), g=null;
      S.goals.forEach(function(x){ if(x.id===gid) g=x; });
      if(!g) return;
      var inp=box.querySelector('.na[data-gid="'+gid+'"]'), v=inp.value.trim();
      if(!v) return;
      g.actions.push({id:uid++,key:null,text:v,done:false});
      inp.value=''; save(); renderGoals();
    });
  });
}
document.getElementById('aGoalBtn').addEventListener('click',function(){
  var inp=document.getElementById('nGoalIn'), v=inp.value.trim();
  if(!v){ toast(t('t.writegoal')); return; }
  S.goals.push({id:uid++,title:v,actions:guessSteps(v).map(function(k){
    return {id:uid++,key:k,text:'',done:false};
  })});
  inp.value=''; save(); renderGoals(); toast(t('t.goaladded'));
});

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
      if(m.days[d]) toast(praise());
      save(); renderWeek(); renderStats();
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
      '<h3>'+esc(t(th.n))+'</h3><div class="au">'+esc(t(th.a))+'</div>'+
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
  document.getElementById('skV').textContent=S.streak;
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

/* ================= tabs ================= */
document.querySelectorAll('.tab').forEach(function(tab){
  tab.addEventListener('click',function(){
    document.querySelectorAll('.tab').forEach(function(x){ x.classList.remove('on'); });
    document.querySelectorAll('.page').forEach(function(p){ p.classList.remove('on'); });
    tab.classList.add('on');
    document.getElementById('page-'+tab.dataset.page).classList.add('on');
  });
});
document.getElementById('chBtn').addEventListener('click',function(){
  if(S.chDone) return;
  S.chDone=true; addPts(25); toast(t('t.pts',{n:25}));
  var b=document.getElementById('chBtn');
  b.disabled=true; b.innerHTML=ic('check');
  save(); renderStats();
});

/* ================= boot ================= */
function renderHome(){ renderRing(); renderCats(); }

function startApp(){
  var name=P.name || t('a.greet.anon');
  document.getElementById('greetName').textContent=t('a.greet',{name:name});
  document.getElementById('proQuote').textContent=t(pick(QUOTES));
  try{
    document.getElementById('dateStr').textContent=
      new Date().toLocaleDateString(cur,{weekday:'long',day:'numeric',month:'long'});
  }catch(e){ document.getElementById('dateStr').textContent=''; }

  var ch=pick(CHALLENGES);
  document.getElementById('chTxt').innerHTML=
    esc(t(ch.t))+' <span class="theme">· '+esc(t(ch.th))+'</span>';
  var cb=document.getElementById('chBtn');
  cb.disabled=!!S.chDone;
  if(S.chDone) cb.innerHTML=ic('check');

  var wp=buildWorkout(P.age,P.workout,P.fitLevel);
  document.getElementById('woSub').textContent=
    t('c.age')+' '+wp.ageBand+' · '+t(wp.levelKey)+' · '+t('wo.'+P.workout);
  document.getElementById('woInfo').innerHTML=ic('sliders')+'<span>'+esc(wp.note)+'</span>';

  fillMissionCats(); renderInsight(); renderHome(); renderGoals(); renderWeek();
  renderPlan('woGrid', wp.blocks, 'w');   // now the "my weekly plan" section of the sport mini-app
  renderPlan('hyGrid', buildHygiene(), 'hy');
  renderTheories(); renderStats(); renderTrial();
  renderMini();                            // the skincare routine now lives in its mini-app
}

document.querySelectorAll('.langbtn').forEach(function(b){
  b.addEventListener('click',function(){ setLang(b.dataset.lang); });
});

bindMini();
applyLang();
renderGoalOpts();
renderChips('easyC',P.easy);
renderChips('hardC',P.hard);
['oTime','oAP','oWO','oFL','oSkin','oDiff'].forEach(function(id){
  var attr={oTime:'time',oAP:'ap',oWO:'wo',oFL:'fl',oSkin:'skin',oDiff:'diff'}[id];
  var field={oTime:'time',oAP:'actPref',oWO:'workout',oFL:'fitLevel',oSkin:'skinType',oDiff:'diff'}[id];
  singleSelect(id,attr,field);
});
markSelected();

if(load()){
  buildCats();
  document.getElementById('landing').style.display='none';
  document.body.classList.remove('has-sticky');
  document.getElementById('stickyCta').style.display='none';
  document.getElementById('app').style.display='block';
  renderGoalOpts(); renderChips('easyC',P.easy); renderChips('hardC',P.hard); markSelected();
  startApp();
}
"""
