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
function emptyQuiz(){ return {answers:{}, scores:null, i:0, done:false, band:null}; }

/* ================= scoring ================= */
function scoreQuiz(){
  var q=S.quiz||emptyQuiz(), sum={}, count={};
  DIMS.forEach(function(d){ sum[d.id]=0; count[d.id]=0; });
  QUESTIONS.forEach(function(Q){
    var pick=q.answers[Q.n];
    var idx=QLETTERS.indexOf(pick);
    if(idx<0) return;
    sum[Q.dim]+=Q.v[idx]; count[Q.dim]++;
  });
  var out={};
  DIMS.forEach(function(d){
    out[d.id]= count[d.id] ? Math.round(sum[d.id]/count[d.id]) : 0;
  });
  return out;
}
function quizAnswered(){
  var q=S.quiz||{}, n=0;
  QUESTIONS.forEach(function(Q){ if(q.answers && q.answers[Q.n]) n++; });
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
function quizOptionRow(Q,letter,i){
  var chosen = (S.quiz.answers[Q.n]===letter);
  return '<button class="qz-opt'+(chosen?' on':'')+'" type="button" data-qa="'+letter+'" '+
    'aria-pressed="'+(chosen?'true':'false')+'">'+
    '<span class="qz-let" aria-hidden="true">'+letter.toUpperCase()+'</span>'+
    '<span class="qz-tx">'+esc(t(qk(quizBand(),Q.n,letter)))+'</span>'+
    '<span class="qz-tick" aria-hidden="true">'+ic('check')+'</span></button>';
}
function renderQuiz(){
  if(!S.quiz) S.quiz=emptyQuiz();
  var i=Math.min(Math.max(0,S.quiz.i),QUESTIONS.length-1);
  S.quiz.i=i;
  var Q=QUESTIONS[i], total=QUESTIONS.length;

  var count=document.getElementById('qzCount');
  if(count) count.textContent=t('qz.count',{n:i+1,t:total});
  var bar=document.getElementById('qzBar');
  if(bar){ bar.style.width=Math.round((i+1)/total*100)+'%'; }
  /* The overlay header keeps showing where the user is in SETUP; the question
     counter lives inside the card. Printing the question count in both places
     read as two different progress bars for the same thing. */
  var top=document.getElementById('stepCount');
  if(top) top.textContent=t('o.step',{n:4,t:ONB_TOTAL});
  var onb=document.getElementById('onbBar');
  if(onb) onb.style.width=Math.round((3+(i+1)/total)/ONB_TOTAL*100)+'%';
  /* One question at a time means the question should be the first thing on
     screen. The title and the "no right answers" note have done their job
     after question one. */
  var intro=document.getElementById('qzIntro');
  if(intro) intro.hidden = i>0;

  var tag=document.getElementById('qzDim');
  if(tag) tag.textContent=t(dimById(Q.dim).k);

  document.getElementById('qzQ').textContent=t(qk(quizBand(),Q.n,'q'));
  var box=document.getElementById('qzOpts');
  box.innerHTML=QLETTERS.map(function(L,ix){ return quizOptionRow(Q,L,ix); }).join('');
  box.querySelectorAll('[data-qa]').forEach(function(b){
    b.addEventListener('click',function(){ answerQuiz(b.dataset.qa); });
  });
  var prev=document.getElementById('qzPrev');
  if(prev) prev.style.visibility = i===0 ? 'hidden' : 'visible';
}
function answerQuiz(letter){
  var Q=QUESTIONS[S.quiz.i];
  S.quiz.answers[Q.n]=letter;
  S.quiz.band=quizBand();
  saveQuiz();
  if(S.quiz.i < QUESTIONS.length-1){
    S.quiz.i++;
    renderQuiz();
  } else {
    finishQuiz();
  }
}
function finishQuiz(){
  S.quiz.scores=scoreQuiz();
  S.quiz.done=true;
  S.quiz.band=quizBand();
  applyProfileToPlan();
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
        S.quiz=q;
      }
    }
  }catch(e){}
  if(!S.quiz) S.quiz=emptyQuiz();
}
function restartQuiz(){
  S.quiz=emptyQuiz(); saveQuiz();
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
      if(S.lessons[n]){ addPts(5); markActiveToday(); }
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
