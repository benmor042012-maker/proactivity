# -*- coding: utf-8 -*-
JS_DATA = r"""
/* ================= backup =================
   Everything this app knows lives in localStorage on one device. One "clear
   browsing data" and months of streak are gone with no way back, so export and
   import are free for everyone, forever - charging someone for their own data
   back is not a business model. */
var STORE_KEYS=['proactive_v','proactive_p','proactive_s','proactive_uid',
                'proactive_lang','proactive_gender','proactive_accent',
                'proactive_theme','proactive_quiz','proactive_chain','proactive_tab'];

function exportBundle(){
  var out={app:'proactivity', v:STORE_V, at:new Date().toISOString(), keys:{}};
  STORE_KEYS.forEach(function(k){
    try{ var v=localStorage.getItem(k); if(v!==null) out.keys[k]=v; }catch(e){}
  });
  return out;
}
function downloadJSON(obj, name){
  var blob=new Blob([JSON.stringify(obj,null,1)],{type:'application/json'});
  var url=URL.createObjectURL(blob), a=document.createElement('a');
  a.href=url; a.download=name; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); },0);
}
function doExport(){
  var d=new Date(), pad=function(n){ return (n<10?'0':'')+n; };
  downloadJSON(exportBundle(), 'proactivity-'+d.getFullYear()+pad(d.getMonth()+1)+pad(d.getDate())+'.json');
  if(typeof toast==='function') toast(t('bk.done'));
}

/* A restore overwrites everything, so it says out loud what it is about to
   write before it writes it. */
function bundleSummary(b){
  var p={}, s={};
  try{ p=JSON.parse(b.keys['proactive_p']||'{}'); }catch(e){}
  try{ s=JSON.parse(b.keys['proactive_s']||'{}'); }catch(e){}
  return {
    name: p.name||'',
    points: Number(s.points)||0,
    streak: (s.day&&Number(s.day.streak))||0,
    goals: (s.goals||[]).length,
    at: b.at||''
  };
}
function applyBundle(b){
  STORE_KEYS.forEach(function(k){ try{ localStorage.removeItem(k); }catch(e){} });
  Object.keys(b.keys||{}).forEach(function(k){
    if(STORE_KEYS.indexOf(k)<0) return;               /* never write a key we do not own */
    try{ localStorage.setItem(k, b.keys[k]); }catch(e){}
  });
}
function bindBackup(){
  var ex=document.getElementById('bkExport');
  if(ex) ex.addEventListener('click', doExport);
  var inp=document.getElementById('bkFile');
  if(inp) inp.addEventListener('change', function(){
    var f=inp.files&&inp.files[0]; if(!f) return;
    var msg=document.getElementById('bkMsg');
    var fr=new FileReader();
    fr.onload=function(){
      var b;
      try{ b=JSON.parse(fr.result); }catch(e){ b=null; }
      if(!b || b.app!=='proactivity' || !b.keys){ if(msg) msg.textContent=t('bk.bad'); inp.value=''; return; }
      var sm=bundleSummary(b);
      if(!confirm(t('bk.confirm',{name:sm.name||'—', pts:sm.points, sk:sm.streak, g:sm.goals}))){ inp.value=''; return; }
      applyBundle(b);
      location.reload();
    };
    fr.readAsText(f);
  });
}

/* localStorage throwing is normally silent here; when the device is genuinely
   full the user needs to hear it once, with somewhere to go. */
var quotaWarned=false;
function warnQuota(){
  if(quotaWarned) return; quotaWarned=true;
  if(typeof toast==='function') toast(t('bk.full'));
}

/* ================= calendar =================
   No server means no push notification. A calendar file needs no server, works
   on every phone, and puts the target where the user already looks. */
function icsEscape(s){ return String(s).replace(/([,;\\])/g,'\\$1').replace(/\n/g,'\\n'); }
function icsStamp(d){
  function p(n){ return (n<10?'0':'')+n; }
  return d.getUTCFullYear()+p(d.getUTCMonth()+1)+p(d.getUTCDate())+'T'+
         p(d.getUTCHours())+p(d.getUTCMinutes())+'00Z';
}
var ICS_DAYS=['SU','MO','TU','WE','TH','FR','SA'];
/* freq times a week, spread out rather than stacked on consecutive days. */
function spreadDays(startIdx, n){
  n=Math.max(1,Math.min(7,n|0));
  var step=7/n, out=[];
  for(var i=0;i<n;i++) out.push(ICS_DAYS[(startIdx+Math.round(i*step))%7]);
  return out.filter(function(d,i,a){ return a.indexOf(d)===i; });
}
function goalICS(g, hour, minute){
  var start=new Date();
  start.setHours(hour, minute, 0, 0);
  if(start<new Date()) start.setDate(start.getDate()+1);
  var end=new Date(start.getTime()+30*60000);
  var freq=Number(g.freq)||3;
  var title=g.title||t('g.one');
  var body=[g.week||'', g.today||'', g.now||''].filter(Boolean).join('\n');
  return [
    'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Proactivity//HE','CALSCALE:GREGORIAN',
    'BEGIN:VEVENT',
    'UID:proactivity-'+(g.id||0)+'-'+Date.now()+'@proactivity',
    'DTSTAMP:'+icsStamp(new Date()),
    'DTSTART:'+icsStamp(start),
    'DTEND:'+icsStamp(end),
    'RRULE:FREQ=WEEKLY;BYDAY='+spreadDays(start.getDay(), freq).join(','),
    'SUMMARY:'+icsEscape(title),
    'DESCRIPTION:'+icsEscape(body),
    'BEGIN:VALARM','TRIGGER:-PT30M','ACTION:DISPLAY','DESCRIPTION:'+icsEscape(title),'END:VALARM',
    'END:VEVENT','END:VCALENDAR'
  ].join('\r\n');
}
function downloadICS(g){
  var parts=String(P.remind||'17:00').split(':');
  var text=goalICS(g, Number(parts[0])||17, Number(parts[1])||0);
  var blob=new Blob([text],{type:'text/calendar;charset=utf-8'});
  var url=URL.createObjectURL(blob), a=document.createElement('a');
  a.href=url; a.download='proactivity.ics'; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); },0);
  if(typeof toast==='function') toast(t('cal.done'));
}

/* ================= install =================
   A habit app that lives in a browser tab gets forgotten. Offered once,
   dismissed for good if the answer is no. */
var installEvt=null;
window.addEventListener('beforeinstallprompt', function(e){
  e.preventDefault(); installEvt=e; showInstall();
});
function installDismissed(){
  try{ return localStorage.getItem('proactive_install')==='no'; }catch(e){ return true; }
}
function showInstall(){
  var bar=document.getElementById('installBar');
  if(!bar || !installEvt || installDismissed()) return;
  if(document.getElementById('app').style.display!=='block') return;
  bar.classList.add('on');
}
function bindInstall(){
  var go=document.getElementById('installGo'), no=document.getElementById('installNo');
  if(go) go.addEventListener('click', function(){
    if(!installEvt) return;
    installEvt.prompt();
    installEvt.userChoice.then(function(){ installEvt=null;
      document.getElementById('installBar').classList.remove('on'); });
  });
  if(no) no.addEventListener('click', function(){
    try{ localStorage.setItem('proactive_install','no'); }catch(e){}
    document.getElementById('installBar').classList.remove('on');
  });
}
function registerSW(){
  if(!('serviceWorker' in navigator)) return;
  if(location.protocol==='file:') return;          /* local test runs, not a bug */
  try{ navigator.serviceWorker.register('sw.js'); }catch(e){}
}
"""
