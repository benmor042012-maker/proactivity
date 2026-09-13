# -*- coding: utf-8 -*-
"""The proactivity check-in, the profile it produces, the micro-lessons,
the achievements and the daily "next step" picker.

Everything here reads and writes S.quiz / S.lessons / S.ach / S.day / S.stats,
all of which are created by migrateV3 so an older save simply gains them.
"""

JS_QUIZ = r"""
/* ================= dimensions ================= */
var DIMS=[
 {id:'init', k:'dim.init',  icon:'rocket',   em:'🚀'},
 {id:'goal', k:'dim.goal',  icon:'target',   em:'🎯'},
 {id:'time', k:'dim.time',  icon:'clock',    em:'⏱️'},
 {id:'solve',k:'dim.solve', icon:'brain',    em:'🧠'},
 {id:'plan', k:'dim.plan',  icon:'calendar', em:'📅'}
];
function dimById(id){ for(var i=0;i<DIMS.length;i++) if(DIMS[i].id===id) return DIMS[i]; return DIMS[0]; }

/* Ten questions, two per dimension. The four numbers are what each answer is
   worth, in the option order a-b-c-d. They are not a grade - they only decide
   which area the app leans on when it suggests something. */
var QUESTIONS=[
 {n:1,  dim:'time',  v:[100,40,15,60]},
 {n:2,  dim:'init',  v:[100,55,20,70]},
 {n:3,  dim:'goal',  v:[100,60,35,15]},
 {n:4,  dim:'plan',  v:[95,65,35,15]},
 {n:5,  dim:'solve', v:[95,65,25,15]},
 {n:6,  dim:'init',  v:[100,60,30,15]},
 {n:7,  dim:'goal',  v:[100,70,40,20]},
 {n:8,  dim:'plan',  v:[100,65,35,15]},
 {n:9,  dim:'solve', v:[100,65,40,15]},
 {n:10, dim:'time',  v:[100,80,30,15]}
];
var QLETTERS=['a','b','c','d'];

/* Four of the ten can honestly be true in more than one way at once - "I start
   a few days early" AND "it depends how much I care about the subject" are not
   contradictory, and forcing one of them is asking the user to lie. The other
   six ask for a single thing (what is your FIRST step, how tidy is your bag)
   and stay single-choice, so eight of the twelve screens still advance on one
   tap with no Continue to press. */
var MULTI_Q={1:true, 2:true, 9:true, 10:true};

/* Two closing questions that are multi-answer by nature and carry no score:
   they shape what the app suggests, not where the user sits on a scale. Both
   reuse the goal chain's own option sets, so there is nothing new to translate
   and the answers feed straight into the chain that follows. */
var QPROFILE=[{id:'areas', k:'qz.p.areas'}, {id:'blocks', k:'qz.p.blocks'}];
function profileOpts(id){
  if(id==='areas') return AREAS.map(function(a){ return {v:a.id, label:t('ga.'+a.id), icon:a.icon}; });
  return OBSTACLES.map(function(o){ return {v:o, label:t('go.'+o), icon:null}; });
}
function profilePicks(id){
  if(!S.quiz) return [];
  if(!S.quiz[id]) S.quiz[id]=[];
  return S.quiz[id];
}

/* Screen 0 is the age. It is asked here rather than only in setup because the
   age is what picks the wording of every question below it, and a retake used
   to re-ask ten questions worded for whatever age was typed months ago with no
   way to correct it. */
function qTotal(){ return QUESTIONS.length + QPROFILE.length; }
function screenAt(i){
  if(i<=0) return {kind:'age'};
  if(i<=QUESTIONS.length) return {kind:'q', Q:QUESTIONS[i-1]};
  return {kind:'p', P:QPROFILE[i-1-QUESTIONS.length]};
}
function lastScreen(){ return qTotal(); }

/* Question text is looked up per age band. This probes I18N.he rather than
   t(), because t() returns the key on a miss and so cannot say "missing"; and a
   key present in I18N.he is present in all five languages, since build.py
   rejects any key with fewer. The fallback to a13 is belt and braces - build.py
   already fails on a band with a hole in it. */
function qk(band,n,part){
  var k='qz.'+band+'.'+n+'.'+part;
  return (I18N.he && I18N.he[k]!==undefined) ? k : 'qz.a13.'+n+'.'+part;
}
function quizBand(){ return ageBand(P.age); }

/* band records which wording the answers were given against. The scores stay
   valid across bands - question number -> dimension -> score vector does not
   depend on wording - so a changed age never throws a profile away; it only
   offers a retake. */
function emptyQuiz(){ return {answers:{}, areas:[], blocks:[], scores:null, i:0, done:false, band:null}; }

/* ================= scoring ================= */
/* An answer is a letter, or - on a multi question - a list of them, and a list
   scores the mean of what was picked. One selection therefore scores exactly
   what it scored before this existed, which is what keeps a new check-in
   comparable with every entry already in the history. */
function answerValue(Q, pick){
  if(pick===undefined || pick===null) return null;
  var list = (pick instanceof Array) ? pick : [pick];
  var sum=0, n=0;
  list.forEach(function(L){
    var ix=QLETTERS.indexOf(L);
    if(ix>=0){ sum+=Q.v[ix]; n++; }
  });
  return n ? sum/n : null;
}
function scoreQuiz(){
  var q=S.quiz||emptyQuiz(), sum={}, count={};
  DIMS.forEach(function(d){ sum[d.id]=0; count[d.id]=0; });
  QUESTIONS.forEach(function(Q){
    var v=answerValue(Q, q.answers[Q.n]);
    if(v===null) return;
    sum[Q.dim]+=v; count[Q.dim]++;
  });
  var out={};
  DIMS.forEach(function(d){
    out[d.id]= count[d.id] ? Math.round(sum[d.id]/count[d.id]) : 0;
  });
  return out;
}
function quizAnswered(){
  var q=S.quiz||{}, n=0;
  QUESTIONS.forEach(function(Q){
    if(q.answers && answerValue(Q,q.answers[Q.n])!==null) n++;
  });
  return n;
}
function hasProfile(){ return !!(S.quiz && S.quiz.scores); }
function profileIndex(){
  if(!hasProfile()) return 0;
  var t=0; DIMS.forEach(function(d){ t+=S.quiz.scores[d.id]||0; });
  return Math.round(t/DIMS.length);
}
function bandKey(v){ return v>=80?'rs.b4' : v>=65?'rs.b3' : v>=40?'rs.b2' : 'rs.b1'; }

/* Ties resolve by DIMS order rather than by whichever key the engine happens to
   walk first, so the same answers always produce the same profile text. */
function extremeDim(want){
  if(!hasProfile()) return DIMS[0].id;
  var best=DIMS[0].id, bv=S.quiz.scores[DIMS[0].id]||0;
  DIMS.forEach(function(d){
    var v=S.quiz.scores[d.id]||0;
    if(want==='high' ? v>bv : v<bv){ bv=v; best=d.id; }
  });
  return best;
}
function strongDim(){ return extremeDim('high'); }
function weakDim(){ return extremeDim('low'); }

/* The check-in is also what sets the challenge level, so someone who is
   already organised is not handed beginner-sized tasks and someone who is
   drowning is not handed a wall of them. */
function applyProfileToPlan(){
  var v=profileIndex();
  P.diff = v>=72 ? 'hard' : v>=45 ? 'mid' : 'easy';
}

/* ================= the check-in screen ================= */
/* A single-choice option is a radio in all but name; a multi one is a checkbox
   and must say so to a screen reader, or the only thing telling anyone they may
   pick two is a line of small print. */
function optRow(opts){
  var cls='qz-opt'+(opts.multi?' multi':'')+(opts.on?' on':'');
  var a11y = opts.multi
    ? 'role="checkbox" aria-checked="'+(opts.on?'true':'false')+'"'
    : 'aria-pressed="'+(opts.on?'true':'false')+'"';
  var badge = opts.icon ? ic(opts.icon) :
    '<span class="qz-let" aria-hidden="true">'+String(opts.letter||'').toUpperCase()+'</span>';
  return '<button class="'+cls+'" type="button" data-qa="'+opts.v+'" '+a11y+'>'+
    badge+'<span class="qz-tx">'+esc(opts.label)+'</span>'+
    '<span class="qz-tick" aria-hidden="true">'+ic('check')+'</span></button>';
}
function picksFor(Q){
  var p=S.quiz.answers[Q.n];
  if(p===undefined||p===null) return [];
  return (p instanceof Array) ? p.slice() : [p];
}

function renderQuiz(){
  if(!S.quiz) S.quiz=emptyQuiz();
  var i=Math.min(Math.max(0,S.quiz.i), lastScreen());
  S.quiz.i=i;
  var sc=screenAt(i), total=qTotal();

  /* the age screen is a preamble, not question 1 of 12 */
  var count=document.getElementById('qzCount');
  if(count) count.textContent = (i===0) ? '' : t('qz.count',{n:i,t:total});
  var bar=document.getElementById('qzBar');
  if(bar) bar.style.width=Math.round(Math.max(i,0.4)/total*100)+'%';
  /* The overlay header keeps showing where the user is in SETUP; the question
     counter lives inside the card. Printing the question count in both places
     read as two different progress bars for the same thing. */
  var top=document.getElementById('stepCount');
  if(top) top.textContent=t('o.step',{n:4,t:ONB_TOTAL});
  var onb=document.getElementById('onbBar');
  if(onb) onb.style.width=Math.round((3+Math.max(i,0)/total)/ONB_TOTAL*100)+'%';
  var intro=document.getElementById('qzIntro');
  if(intro) intro.hidden = i>0;

  var ageBox=document.getElementById('qzAge'), body=document.getElementById('qzBody');
  if(ageBox) ageBox.hidden = (sc.kind!=='age');
  if(body)   body.hidden   = (sc.kind==='age');

  var prev=document.getElementById('qzPrev');
  if(prev) prev.style.visibility = i===0 ? 'hidden' : 'visible';

  if(sc.kind==='age'){ renderQuizAge(); return; }

  var multi = (sc.kind==='p') || !!MULTI_Q[sc.Q && sc.Q.n];
  var tag=document.getElementById('qzDim');
  if(tag) tag.textContent = (sc.kind==='q') ? t(dimById(sc.Q.dim).k) : '';
  var hint=document.getElementById('qzMulti');
  if(hint) hint.hidden = !multi;

  var rows, chosen;
  if(sc.kind==='q'){
    document.getElementById('qzQ').textContent=t(qk(quizBand(),sc.Q.n,'q'));
    chosen=picksFor(sc.Q);
    rows=QLETTERS.map(function(L){
      return optRow({v:L, letter:L, label:t(qk(quizBand(),sc.Q.n,L)),
                     multi:multi, on:chosen.indexOf(L)>=0});
    });
  } else {
    document.getElementById('qzQ').textContent=t(sc.P.k);
    chosen=profilePicks(sc.P.id);
    rows=profileOpts(sc.P.id).map(function(o){
      return optRow({v:o.v, label:o.label, icon:o.icon, multi:true, on:chosen.indexOf(o.v)>=0});
    });
  }
  var box=document.getElementById('qzOpts');
  box.innerHTML=rows.join('');
  box.querySelectorAll('[data-qa]').forEach(function(b){
    b.addEventListener('click',function(){ pickQuiz(b.dataset.qa); });
  });
  renderQuizNext();
}

/* Single-choice keeps advancing on the tap itself. A multi screen cannot, so it
   grows a Continue button - disabled until something is chosen, because an
   empty answer is not an answer. */
function renderQuizNext(){
  var btn=document.getElementById('qzNext'); if(!btn) return;
  var sc=screenAt(S.quiz.i);
  if(sc.kind==='age'){
    btn.hidden=false;
    btn.disabled = !ageOK(document.getElementById('qAge'));
    return;
  }
  var multi = (sc.kind==='p') || !!MULTI_Q[sc.Q && sc.Q.n];
  btn.hidden = !multi;
  if(!multi) return;
  var n = (sc.kind==='p') ? profilePicks(sc.P.id).length : picksFor(sc.Q).length;
  btn.disabled = n===0;
}

function ageOK(el){
  var n=parseInt(el&&el.value,10);
  return n>=13 && n<=120;
}
function renderQuizAge(){
  var el=document.getElementById('qAge');
  if(el && !el.value && P.age) el.value=P.age;
  var hint=document.getElementById('qAgeBand');
  if(hint) hint.textContent = ageOK(el) ? t('ab.'+ageBand(el.value)) : '';
  renderQuizNext();
}
function bindQuizAge(){
  var el=document.getElementById('qAge');
  if(el) el.addEventListener('input', renderQuizAge);
  var btn=document.getElementById('qzNext');
  if(btn) btn.addEventListener('click', nextQuiz);
}

/* One tap: single-choice answers and moves on, multi toggles and waits. */
function pickQuiz(v){
  var sc=screenAt(S.quiz.i);
  if(sc.kind==='p'){
    var list=profilePicks(sc.P.id), at=list.indexOf(v);
    if(at>=0) list.splice(at,1); else list.push(v);
    saveQuiz(); renderQuiz(); return;
  }
  var Q=sc.Q;
  if(MULTI_Q[Q.n]){
    var picks=picksFor(Q), ix=picks.indexOf(v);
    if(ix>=0) picks.splice(ix,1); else picks.push(v);
    S.quiz.answers[Q.n]=picks;
    S.quiz.band=quizBand();
    saveQuiz(); renderQuiz(); return;
  }
  S.quiz.answers[Q.n]=v;
  S.quiz.band=quizBand();
  saveQuiz();
  nextQuiz();
}
function nextQuiz(){
  var sc=screenAt(S.quiz.i);
  if(sc.kind==='age'){
    var el=document.getElementById('qAge');
    if(!ageOK(el)){ toast(t('t.agerange')); return; }
    P.age=String(parseInt(el.value,10));
    save();
  }
  if(S.quiz.i < lastScreen()){ S.quiz.i++; saveQuiz(); renderQuiz(); }
  else finishQuiz();
}
/* kept: other modules and older handlers still call answerQuiz(letter) */
function answerQuiz(letter){ pickQuiz(letter); }
function finishQuiz(){
  S.quiz.scores=scoreQuiz();
  S.quiz.done=true;
  S.quiz.band=quizBand();
  recordCheckin();
  applyProfileToPlan();
  /* CH is built at boot, before any of this was known. If it is still
     untouched, rebuild it so the chain opens on what was just said. */
  if(typeof CH==='object' && CH && CH.step===0 && !CH.area){ CH=emptyChain(); saveChain(); }
  saveQuiz();
  unlock('ach.quiz');
  if(document.getElementById('onboarding').style.display==='block'){
    showStep(5);
  } else {
    renderProfile('profBody');
    toast(t('rs.updated'));
  }
}
/* The check-in runs before onboarding finishes, i.e. before save() is allowed
   to write a profile, so its answers get their own key and are folded back in
   by load(). Losing ten answers to a mistimed refresh would be the one thing
   nobody would re-enter. */
function saveQuiz(){
  try{ localStorage.setItem('proactive_quiz', JSON.stringify(S.quiz)); }catch(e){}
}
function loadQuiz(){
  try{
    var raw=localStorage.getItem('proactive_quiz');
    if(raw){
      var q=JSON.parse(raw);
      if(q && q.answers){
        if(!q.band) q.band='a13';   // every save before bands existed was teen-worded
        /* Before the age screen existed, index 0 WAS question 1. Shift a
           part-finished quiz forward so it resumes on the same question rather
           than throwing the user back to the start. */
        if(q.areas===undefined && typeof q.i==='number') q.i=q.i+1;
        if(!q.areas)  q.areas=[];
        if(!q.blocks) q.blocks=[];
        S.quiz=q;
      }
    }
  }catch(e){}
  if(!S.quiz) S.quiz=emptyQuiz();
}
function restartQuiz(){
  S.quiz=emptyQuiz(); saveQuiz();
}

/* ================= check-in history =================
   A retake used to overwrite the result and the earlier one was simply gone,
   which threw away the only thing the app could ever show that really moves
   someone: proof they changed. Recorded for everybody - the chart that reads it
   may be a Pro view, but the data is the user's and is never not kept. */
function recordCheckin(){
  if(!S.hist) S.hist=[];
  var sc=S.quiz.scores||{};
  var last=S.hist[S.hist.length-1];
  var entry={d:dayKey(), band:S.quiz.band||'a13', s:{
    init:sc.init|0, goal:sc.goal|0, time:sc.time|0, solve:sc.solve|0, plan:sc.plan|0}};
  /* two goes at the same check-in on one day is one data point, the later one */
  if(last && last.d===entry.d) S.hist[S.hist.length-1]=entry;
  else S.hist.push(entry);
  if(S.hist.length>60) S.hist=S.hist.slice(-60);
  save();
}
function checkinAvg(e){
  var s=e.s; return Math.round((s.init+s.goal+s.time+s.solve+s.plan)/5);
}
function daysSinceCheckin(){
  if(!S.hist||!S.hist.length) return 0;
  return daysBetween(S.hist[S.hist.length-1].d, dayKey());
}

/* ================= the profile ================= */
function meterRow(d){
  var v=(S.quiz.scores && S.quiz.scores[d.id])||0;
  return '<div class="mtr">'+
    '<div class="mtr-top"><span class="mtr-n">'+ic(d.icon)+'<span>'+esc(t(d.k))+'</span></span>'+
    '<span class="mtr-v numf">'+v+'%</span></div>'+
    '<div class="mtr-bar"><i style="width:'+v+'%"></i></div></div>';
}
/* On a perfectly flat profile strongest and weakest are the same dimension, and
   the sentence still reads correctly: "you are good at X, but sometimes X". */
function profileMeaning(){
  return t('rs.line',{strong:t('rs.st.'+strongDim()), grow:t('rs.gr.'+weakDim())});
}
function profileActions(){
  var w=weakDim();
  return [1,2,3].map(function(n){ return t('rs.ac.'+w+'.'+n); });
}
/* compact:true is the dashboard version - the score and the five bars only.
   The reading of it, and the three things to try, live on the Progress tab so
   the first screen does not turn into a report. */
function renderProfile(boxId, compact){
  var box=document.getElementById(boxId);
  if(!box) return;
  if(!hasProfile()){
    box.innerHTML='<div class="empty">'+esc(t('rs.none'))+'</div>'+
      '<button class="btn btn-primary" data-goquiz>'+esc(t('n.hero.cta'))+'</button>';
    bindGoQuiz(box);
    return;
  }
  var idx=profileIndex();
  var head=
   '<div class="pro-score">'+
     '<div class="pro-num numf">'+idx+'<span>%</span></div>'+
     '<div><div class="pro-lab">'+esc(t('rs.index'))+'</div>'+
     '<div class="pro-band">'+esc(t(bandKey(idx)))+'</div></div></div>'+
   '<div class="meters">'+DIMS.map(meterRow).join('')+'</div>';

  if(compact){
    box.innerHTML=head+
      '<button class="btn btn-ghost btn-sm" data-goprog>'+ic('trending')+
      '<span>'+esc(t('rs.mean'))+'</span></button>';
    box.querySelectorAll('[data-goprog]').forEach(function(b){
      b.addEventListener('click',function(){ goPage('progress'); });
    });
    return;
  }

  var stale = S.quiz.band && S.quiz.band!==quizBand()
    ? '<p class="hint">'+ic('refresh')+'<span>'+esc(t('rs.ageband'))+'</span></p>' : '';
  box.innerHTML=head+stale+
   '<div class="pro-blk"><h3>'+esc(t('rs.mean'))+'</h3><p>'+esc(profileMeaning())+'</p></div>'+
   '<div class="pro-blk"><h3>'+esc(t('rs.try'))+'</h3><ol class="pro-acts">'+
     profileActions().map(function(a){ return '<li>'+esc(a)+'</li>'; }).join('')+
   '</ol></div>'+
   '<button class="btn btn-ghost btn-sm" data-goquiz>'+ic('refresh')+'<span>'+esc(t('rs.again'))+'</span></button>';
  bindGoQuiz(box);
}
function bindGoQuiz(box){
  box.querySelectorAll('[data-goquiz]').forEach(function(b){
    b.addEventListener('click',function(){
      restartQuiz();
      document.getElementById('app').style.display='none';
      document.getElementById('onboarding').style.display='block';
      showStep(4);
    });
  });
}

/* ================= micro-lessons ================= */
var LESSONS=[
 {n:1, icon:'compass',  min:'ls.read'},
 {n:2, icon:'refresh',  min:'ls.read'},
 {n:3, icon:'zap',      min:'ls.read'},
 {n:4, icon:'seedling', min:'ls.read'},
 {n:5, icon:'clock',    min:'ls.read2'},
 {n:6, icon:'target',   min:'ls.read2'},
 {n:7, icon:'refresh',  min:'ls.read'},
 {n:8, icon:'shield',   min:'ls.read'}
];
function lessonsRead(){
  var n=0; for(var k in (S.lessons||{})) if(S.lessons[k]) n++;
  return n;
}
function renderLessons(){
  var g=document.getElementById('lsGrid');
  if(!g) return;
  g.innerHTML=LESSONS.map(function(L){
    var read=!!(S.lessons&&S.lessons[L.n]);
    return '<details class="lsn'+(read?' read':'')+'">'+
      '<summary><span class="lsn-i">'+ic(L.icon)+'</span>'+
      '<span class="lsn-t">'+esc(t('ls.'+L.n+'.t'))+'</span>'+
      '<span class="lsn-m">'+esc(t(L.min))+'</span>'+
      ic('chevron','lsn-c')+'</summary>'+
      '<div class="lsn-b"><p>'+esc(t('ls.'+L.n+'.b'))+'</p>'+
      '<div class="lsn-ex"><span class="lab">'+esc(t('ls.ex'))+'</span><p>'+esc(t('ls.'+L.n+'.e'))+'</p></div>'+
      '<div class="lsn-do"><span class="lab">'+ic('arrow')+esc(t('ls.do'))+'</span><p>'+esc(t('ls.'+L.n+'.d'))+'</p></div>'+
      '<button class="btn btn-ghost btn-sm" data-lsn="'+L.n+'">'+
        (read?ic('check'):'')+'<span>'+esc(t(read?'ls.done':'ls.mk'))+'</span></button>'+
      '</div></details>';
  }).join('');
  g.querySelectorAll('[data-lsn]').forEach(function(b){
    b.addEventListener('click',function(){
      var n=b.dataset.lsn;
      if(!S.lessons) S.lessons={};
      S.lessons[n]=!S.lessons[n];
      if(S.lessons[n]){ addPts(5); markActiveToday(); tip('lesson'); }
      save(); renderLessons(); renderStats(); checkAchievements();
    });
  });
}

/* ================= achievements ================= */
/* id is stable and stored, so renaming a badge never re-fires its toast. */
var ACHV=[
 {id:'ach.first',  n:1,  icon:'check',    test:function(){ return (S.stats.tasksDone||0)>=1; }},
 {id:'ach.s3',     n:2,  icon:'flame',    test:function(){ return (S.stats.bestStreak||0)>=3; }},
 {id:'ach.goal',   n:3,  icon:'target',   test:function(){ return (S.goals||[]).length>=1; }},
 {id:'ach.init',   n:4,  icon:'rocket',   test:function(){ return (S.stats.challenges||0)>=1; }},
 {id:'ach.plan',   n:5,  icon:'calendar', test:function(){
    return (S.missions||[]).some(function(m){ return missionState(m).met; }); }},
 {id:'ach.back',   n:6,  icon:'refresh',  test:function(){ return (S.stats.comebacks||0)>=1; }},
 {id:'ach.read',   n:7,  icon:'book',     test:function(){ return lessonsRead()>=3; }},
 {id:'ach.quiz',   n:8,  icon:'compass',  test:function(){ return hasProfile(); }},
 {id:'ach.s7',     n:9,  icon:'star',     test:function(){ return (S.stats.bestStreak||0)>=7; }},
 {id:'ach.t10',    n:10, icon:'gem',      test:function(){ return (S.stats.tasksDone||0)>=10; }}
];
function unlock(id){
  if(!S.ach) S.ach={};
  if(S.ach[id]) return false;
  S.ach[id]=dayKey();
  save();
  var a=null;
  ACHV.forEach(function(x){ if(x.id===id) a=x; });
  if(a) toast(t('ac.new',{x:t('ac.'+a.n+'.t')}));
  renderAchievements();
  return true;
}
function checkAchievements(){
  if(!S.ach) S.ach={};
  ACHV.forEach(function(a){
    var ok=false;
    try{ ok=a.test(); }catch(e){ ok=false; }
    if(ok) unlock(a.id);
  });
}
function renderAchievements(){
  var g=document.getElementById('acGrid');
  if(!g) return;
  var got=0;
  var html=ACHV.map(function(a){
    var on=!!(S.ach&&S.ach[a.id]);
    if(on) got++;
    return '<div class="ach'+(on?' on':'')+'">'+
      '<span class="ach-i">'+ic(on?a.icon:'lock')+'</span>'+
      '<div><div class="ach-t">'+esc(t('ac.'+a.n+'.t'))+'</div>'+
      '<div class="ach-d">'+esc(on?t('ac.'+a.n+'.d'):t('ac.locked'))+'</div></div></div>';
  }).join('');
  g.innerHTML=html;
  var c=document.getElementById('acCount');
  if(c) c.textContent=t('ac.got',{n:got,t:ACHV.length});
}

/* ================= the daily "next step" ================= */
/* One suggestion a day, drawn from the area the check-in flagged as weakest so
   the app leans where the user actually needs it. Without a profile it falls
   back to the generic challenge list. */
function pickNextStep(){
  var day=dayKey();
  if(S.next && S.next.day===day) return S.next;
  var key, theme='';
  if(hasProfile()){
    var w=weakDim();
    var seed=Math.abs(hashDay(day)) % 3 + 1;
    key='rs.ac.'+w+'.'+seed;
    theme=t(dimById(w).k);
  } else {
    var c=CHALLENGES[Math.abs(hashDay(day)) % CHALLENGES.length];
    key=c.t; theme=t(c.th);
  }
  S.next={day:day, key:key, theme:theme, done:false};
  save();
  return S.next;
}
/* A tiny string hash so the suggestion is stable for a given day instead of
   changing on every repaint. */
function hashDay(s){
  var h=0;
  for(var i=0;i<s.length;i++){ h=(h*31 + s.charCodeAt(i))|0; }
  return h;
}
"""
