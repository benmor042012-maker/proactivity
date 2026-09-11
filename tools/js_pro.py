# -*- coding: utf-8 -*-
JS_PRO = r"""
/* ================= billing =================
   One block to configure. Paste the Payment Link for each plan and, if the
   provider issues licence keys, the app can verify a subscription for real -
   see PAYMENTS.md at the repository root.

   While `checkout` is empty the app runs in OPEN mode: nothing is locked, no
   upsell appears anywhere, and the pricing section says plainly that payment is
   not open yet. Gating a feature when nobody can possibly pay would just be
   taking the app away from people. */
var BILLING={
  provider:'lemonsqueezy',
  checkout:{monthly:'', annual:''},
  portal:''                              /* "manage my subscription" page */
};
var GOAL_FREE_MAX=3;                     /* active targets on the free tier */
/* The one address on the site. Until checkout is configured this is how someone
   who wants to pay actually reaches you; after it, it is where questions go. */
var CONTACT_EMAIL='ben.mor.04.2012@gmail.com';

function billingOn(){ return !!(BILLING.checkout.monthly||BILLING.checkout.annual); }

/* ================= licence =================
   Lemon Squeezy's License API takes no secret key and answers CORS, so a page
   with no server behind it can still ask the provider whether a subscription is
   really live. That is the whole reason this is a licence key and not a
   "?paid=1" flag in the URL: one can be checked, the other cannot. */
var LIC={key:'', inst:'', ok:false, exp:null, checked:0};

function loadLic(){
  try{
    var raw=localStorage.getItem('proactive_lic');
    if(raw){ var j=JSON.parse(raw); if(j&&typeof j==='object') LIC=Object.assign(LIC,j); }
  }catch(e){}
}
function saveLic(){ try{ localStorage.setItem('proactive_lic', JSON.stringify(LIC)); }catch(e){} }

function licExpired(){
  if(!LIC.exp) return false;
  var t0=Date.parse(LIC.exp);
  return !isNaN(t0) && Date.now()>t0;
}
/* Verified once, then trusted offline until it expires - an app that stops
   working on a train is worse than one that trusts a paying customer. */
function licActive(){ return !!(LIC.ok && LIC.key && !licExpired()); }

function lsPost(op, data){
  var body=Object.keys(data).filter(function(k){ return data[k]; })
    .map(function(k){ return encodeURIComponent(k)+'='+encodeURIComponent(data[k]); }).join('&');
  return fetch('https://api.lemonsqueezy.com/v1/licenses/'+op, {
    method:'POST',
    headers:{'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'},
    body:body
  }).then(function(r){ return r.json(); });
}
/* Every provider answers in its own shape; everything above this line speaks
   one shape. Swapping to Paddle or Stripe later is another adapter, not a
   rewrite of the app. */
var LICENSE_ADAPTERS={
  lemonsqueezy:{
    activate:  function(key,name){ return lsPost('activate',  {license_key:key, instance_name:name}); },
    validate:  function(key,inst){ return lsPost('validate',  {license_key:key, instance_id:inst}); },
    deactivate:function(key,inst){ return lsPost('deactivate',{license_key:key, instance_id:inst}); },
    norm: function(j){
      var lk=(j&&j.license_key)||{};
      var live = lk.status ? (lk.status==='active') : true;
      return {
        ok:  !!(j && (j.activated || j.valid || j.deactivated) && live),
        exp: lk.expires_at || null,
        inst:(j && j.instance && j.instance.id) || '',
        err: (j && j.error) || null
      };
    }
  }
};
function licAdapter(){ return LICENSE_ADAPTERS[BILLING.provider] || LICENSE_ADAPTERS.lemonsqueezy; }
function deviceName(){
  var n=(P.name||'').trim();
  return (n? n+' · ':'')+'proactivity-'+(navigator.platform||'web');
}

function activateLicense(key){
  var a=licAdapter();
  return a.activate(String(key||'').trim(), deviceName()).then(function(j){
    var r=a.norm(j);
    if(!r.ok) return {ok:false, err:r.err||t('pro.lic.bad')};
    LIC={key:String(key).trim(), inst:r.inst, ok:true, exp:r.exp, checked:Date.now()};
    saveLic(); return {ok:true};
  }).catch(function(){ return {ok:false, err:t('pro.lic.net')}; });
}
function releaseLicense(){
  var a=licAdapter(), key=LIC.key, inst=LIC.inst;
  LIC={key:'', inst:'', ok:false, exp:null, checked:0}; saveLic();
  if(key&&inst) { try{ a.deactivate(key,inst).catch(function(){}); }catch(e){} }
}
/* A dead network is not a verdict: only the provider actually saying "no"
   revokes access. */
var LIC_RECHECK_MS=7*86400000;
function revalidateLicense(){
  if(!billingOn() || !LIC.key || !LIC.ok) return;
  if(Date.now()-(LIC.checked||0) < LIC_RECHECK_MS) return;
  var a=licAdapter();
  a.validate(LIC.key, LIC.inst).then(function(j){
    var r=a.norm(j);
    LIC.checked=Date.now();
    if(r.exp) LIC.exp=r.exp;
    if(!r.ok){ LIC.ok=false; }
    saveLic();
    if(!r.ok && typeof redrawAll==='function') redrawAll();
  }).catch(function(){});
}

/* ================= who gets what ================= */
function proState(){
  if(!billingOn())        return 'open';     /* payment not configured at all */
  if(P.founder)           return 'founder';  /* here before Pro existed */
  if(licActive())         return 'pro';
  if(trialDaysLeft()>0)   return 'trial';
  return 'free';
}
function isPro(){ return proState()!=='free'; }
function goalLimitReached(){
  if(isPro()) return false;
  return (S.goals||[]).filter(function(g){ return !g.archived; }).length >= GOAL_FREE_MAX;
}

/* A lock is never a dead end: it says what the thing is and offers the way in. */
function lockHtml(whatKey){
  return '<div class="lockcard">'+ic('lock')+
    '<h3>'+esc(t('pro.lock.t'))+'</h3>'+
    '<p>'+esc(t(whatKey))+'</p>'+
    '<button class="btn btn-primary" data-go-plans>'+esc(t('pro.lock.cta'))+'</button>'+
    '<button class="btn btn-ghost btn-sm" data-lic-open>'+esc(t('pro.have'))+'</button>'+
    '</div>';
}

/* ================= checkout ================= */
function startCheckout(planId){
  var url=BILLING.checkout[planId];
  if(!url) return;
  P.plan=planId; if(!P.trialStart) P.trialStart=Date.now(); save();
  window.open(url,'_blank','noopener');
}
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-buy]');
  if(b){ startCheckout(b.dataset.buy); return; }
  if(e.target.closest('[data-go-plans]')){ openPlans(); return; }
  if(e.target.closest('[data-lic-open]')){ openPlans(); focusLicense(); return; }
});
function openPlans(){
  document.getElementById('app').style.display='none';
  document.getElementById('onboarding').style.display='block';
  showStep(8);
}
function focusLicense(){
  var d=document.getElementById('licBox');
  if(d){ d.open=true; var i=document.getElementById('licKey'); if(i) i.focus(); }
}
/* Buy buttons exist only when there is somewhere for them to go. */
function renderCheckout(){
  var any=billingOn();
  document.querySelectorAll('[data-buy]').forEach(function(b){
    b.hidden = !BILLING.checkout[b.dataset.buy];
  });
  document.querySelectorAll('[data-i18n="l.pr.trust"]').forEach(function(el){ el.hidden=!any; });
  document.querySelectorAll('.plans-soon').forEach(function(el){ el.hidden=any; });
  document.querySelectorAll('[data-contact]').forEach(function(a){
    a.textContent=CONTACT_EMAIL;
    a.href='mailto:'+CONTACT_EMAIL+'?subject='+encodeURIComponent(t('l.pr.ask.sub'));
  });
  var lb=document.getElementById('licBox'); if(lb) lb.hidden=!any;
  var pt=document.getElementById('portalLink');
  if(pt){ pt.hidden=!(BILLING.portal && licActive()); pt.href=BILLING.portal||'#'; }
  renderLicState();
}
function renderLicState(){
  var el=document.getElementById('licState'); if(!el) return;
  var st=proState();
  el.className='lic-state '+st;
  if(st==='pro'){
    el.textContent = LIC.exp ? t('pro.state.pro.exp',{d:fmtDay(String(LIC.exp).slice(0,10))}) : t('pro.state.pro');
  } else if(st==='founder'){ el.textContent=t('pro.state.founder'); }
  else if(st==='trial'){ el.textContent=t('pro.state.trial',{n:trialDaysLeft()}); }
  else if(st==='open'){ el.textContent=''; }
  else { el.textContent=t('pro.state.free'); }
  var rel=document.getElementById('licRelease');
  if(rel) rel.hidden = !licActive();
}
function bindLicense(){
  var btn=document.getElementById('licGo');
  if(btn) btn.addEventListener('click',function(){
    var inp=document.getElementById('licKey'), msg=document.getElementById('licMsg');
    var key=(inp&&inp.value||'').trim();
    if(!key){ if(msg) msg.textContent=t('pro.lic.empty'); return; }
    btn.disabled=true; if(msg) msg.textContent=t('pro.lic.checking');
    activateLicense(key).then(function(r){
      btn.disabled=false;
      if(msg) msg.textContent = r.ok ? t('pro.lic.ok') : (r.err||t('pro.lic.bad'));
      if(r.ok){ if(inp) inp.value=''; renderCheckout(); if(typeof redrawAll==='function') redrawAll(); }
    });
  });
  var rel=document.getElementById('licRelease');
  if(rel) rel.addEventListener('click',function(){
    releaseLicense(); renderCheckout();
    if(typeof redrawAll==='function') redrawAll();
    if(typeof toast==='function') toast(t('pro.lic.released'));
  });
}
"""
