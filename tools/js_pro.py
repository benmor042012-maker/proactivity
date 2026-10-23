# -*- coding: utf-8 -*-
JS_PRO = r"""
/* ================= billing =================
   One block to configure; the whole card flow is already written around it.
   See PAYMENTS.md at the repository root for where each value comes from.

   `token` and `prices` are the card form. With them set, Paddle's own card
   fields open *inside this page* - no redirect to someone else's site. The
   token is a client-side token: it is designed to be published in front-end
   code, it can only start a checkout, and it cannot read or move money, which
   is why it can sit in a public repository.

   `licProvider` is the separate, optional licence-key path. A provider that
   issues keys (Lemon Squeezy) lets a buyer restore Pro on a second device and
   lets this page verify the subscription against the provider for real. Paddle
   has no licence API a browser can call, so with Paddle alone the key box stays
   hidden instead of pretending to check something.

   While `token` is empty the app runs in OPEN mode: nothing is locked, no
   upsell appears anywhere, paddle.js is never even fetched, and the pricing
   section says plainly that payment is not open yet. Gating a feature when
   nobody can possibly pay would just be taking the app away from people. */
var BILLING={
  provider:'paddle',
  token:'',                              /* client-side token: live_... / test_... */
  env:'production',                      /* 'sandbox' while you are testing */
  prices:{monthly:'', annual:''},        /* pri_... ids from the Paddle catalogue */
  portal:'',                             /* "manage my subscription" page */
  licProvider:''                         /* '' | 'lemonsqueezy' */
};
var PADDLE_JS='https://cdn.paddle.com/paddle/v2/paddle.js';
var GOAL_FREE_MAX=3;                     /* active targets on the free tier */
/* The one address on the site. Until checkout is configured this is how someone
   who wants to pay actually reaches you; after it, it is where questions go. */
var CONTACT_EMAIL='ben.mor.04.2012@gmail.com';

/* A price with no token cannot charge anything, and a token with no price has
   nothing to sell, so both have to be there before a buy button appears. */
function billingOn(){ return !!(BILLING.token && (BILLING.prices.monthly||BILLING.prices.annual)); }
function licOn(){ return !!(BILLING.licProvider && LICENSE_ADAPTERS[BILLING.licProvider]); }

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
function licAdapter(){ return LICENSE_ADAPTERS[BILLING.licProvider] || LICENSE_ADAPTERS.lemonsqueezy; }
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
  if(!licOn() || !LIC.key || !LIC.ok) return;
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

/* ================= paid on this device =================
   What the browser itself saw: Paddle told this page, in this tab, that the
   payment went through. It is kept in its own storage key so it survives a
   profile reset, and it is deliberately not mixed into the profile - someone
   can pay from the pricing section before they have set anything up.

   Be clear about what this is worth: it is a flag on the device, so it cannot
   notice a later cancellation and a determined person could write it by hand.
   That is the known limit of a page with no server behind it, and the licence
   key above is the path that is actually verified. */
var PAID={txn:'', at:0, plan:''};
function loadPaid(){
  try{
    var raw=localStorage.getItem('proactive_pay');
    if(raw){ var j=JSON.parse(raw); if(j&&typeof j==='object') PAID=Object.assign(PAID,j); }
  }catch(e){}
}
function savePaid(){ try{ localStorage.setItem('proactive_pay', JSON.stringify(PAID)); }catch(e){} }
function paidHere(){ return !!PAID.txn; }
/* Is there a save on this device at all? Buying from the pricing section
   happens before any setup, and writing a profile just because someone pressed
   "pay" would drop them into a half-built app on their next visit. */
function savedProfile(){ try{ return !!localStorage.getItem('proactive_p'); }catch(e){ return false; } }

/* ================= who gets what ================= */
function proState(){
  if(!billingOn())        return 'open';     /* payment not configured at all */
  if(P.founder)           return 'founder';  /* here before Pro existed */
  if(licActive())         return 'pro';
  if(paidHere())          return 'pro';
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

/* ================= the card form =================
   Paddle's inline checkout puts Paddle's own iframe inside an element on this
   page. The card number is typed here, on this site, but it is entered into
   Paddle's frame and never reaches this code, this origin or any storage of
   ours - which is the only way a page with no server is allowed anywhere near
   a card. Everything below is about opening that frame and listening for the
   one event that says the payment went through.

   paddle.js is fetched the first time someone presses a buy button, and only
   when a token is configured: nobody who cannot pay loads a payment script. */
var PADDLE={ready:false, p:null, plan:''};
/* Paddle translates its own checkout into a fixed list of languages. These
   three are on it; for Hebrew and Arabic the locale is left out so Paddle
   chooses, rather than being handed a code it does not know. */
var PADDLE_LOCALES={en:'en', fr:'fr', ru:'ru'};

function loadPaddle(){
  if(PADDLE.p) return PADDLE.p;
  if(!billingOn()) return Promise.resolve(false);
  PADDLE.p=new Promise(function(done){
    function init(){
      try{
        if(BILLING.env==='sandbox' && window.Paddle.Environment) window.Paddle.Environment.set('sandbox');
        window.Paddle.Initialize({token:BILLING.token, eventCallback:payEvent});
        PADDLE.ready=true; done(true);
      }catch(e){ done(false); }
    }
    if(window.Paddle){ init(); return; }
    var s=document.createElement('script');
    s.src=PADDLE_JS; s.async=true;
    s.onload=init;
    s.onerror=function(){ done(false); };
    document.head.appendChild(s);
  });
  return PADDLE.p;
}

function payMsg(s){ var el=document.getElementById('payMsg'); if(el) el.textContent=s||''; }
function payClose(){
  var m=document.getElementById('payModal'); if(m) m.classList.remove('on');
  try{ if(PADDLE.ready && window.Paddle.Checkout) window.Paddle.Checkout.close(); }catch(e){}
  var box=document.getElementById('payBox'); if(box) box.innerHTML='';
  document.body.classList.remove('no-scroll');
}
/* One modal, opened from the pricing section and from the plans screen alike,
   so there is a single place where a card is ever entered. */
function startCheckout(planId){
  var priceId=BILLING.prices[planId];
  if(!priceId) return;
  PADDLE.plan=planId;
  if(savedProfile()){                   /* never write a profile just to buy */
    P.plan=planId; if(!P.trialStart) P.trialStart=Date.now(); save();
  }
  var m=document.getElementById('payModal'); if(!m) return;
  var th=document.getElementById('payThanks'); if(th) th.hidden=true;
  var box=document.getElementById('payBox'); if(box){ box.hidden=false; box.innerHTML=''; }
  /* The plan and the amount that is about to be charged - the yearly total for
     the annual plan, not the per-month figure the card advertises it at. */
  var pr=PRICES[cur]||PRICES.en, pl=document.getElementById('payPlan');
  if(pl) pl.textContent=t('l.pr.'+planId)+' · '+money(planId==='annual' ? pr.ytot : pr.m);
  m.classList.add('on');
  document.body.classList.add('no-scroll');
  payMsg(t('pay.load'));
  var cb=document.getElementById('payCloseBtn'); if(cb) cb.focus();
  loadPaddle().then(function(ok){
    if(!ok){ payMsg(t('pay.err')); return; }
    try{
      window.Paddle.Checkout.open({
        items:[{priceId:priceId, quantity:1}],
        settings:paySettings()
      });
    }catch(e){ payMsg(t('pay.err')); }
  });
}
function paySettings(){
  var s={
    displayMode:'inline',
    theme:(typeof activeTheme==='function' && activeTheme()==='dark') ? 'dark' : 'light',
    frameTarget:'pay-box',
    frameInitialHeight:'450',
    frameStyle:'width:100%;min-width:312px;background-color:transparent;border:none;'
  };
  if(PADDLE_LOCALES[cur]) s.locale=PADDLE_LOCALES[cur];
  /* No successUrl on purpose: the frame shows its own "paid" state and the app
     unlocks in place, so nobody is bounced to another page mid-purchase. */
  return s;
}
/* Paddle reports back through the one callback registered at Initialize. */
function payEvent(ev){
  var n=ev&&ev.name;
  if(n==='checkout.loaded'||n==='checkout.customer.created'){ payMsg(''); return; }
  if(n==='checkout.completed'){ payDone(ev); return; }
  if(n==='checkout.error'){ payMsg(t('pay.err')); return; }
  if(n==='checkout.closed'){ payMsg(''); return; }
}
function payDone(ev){
  var d=(ev&&ev.data)||{};
  PAID={txn:String(d.transaction_id||d.id||'paid'), at:Date.now(), plan:PADDLE.plan||''};
  savePaid();
  if(savedProfile()){ P.plan=PADDLE.plan||P.plan; save(); }
  var box=document.getElementById('payBox'); if(box){ box.innerHTML=''; box.hidden=true; }
  payMsg('');
  var th=document.getElementById('payThanks'); if(th) th.hidden=false;
  if(typeof toast==='function') toast(t('pay.done.t'));
  renderCheckout();
  if(typeof redrawAll==='function') redrawAll();
}
function bindPay(){
  var cb=document.getElementById('payCloseBtn');
  if(cb) cb.addEventListener('click', payClose);
  var ok=document.getElementById('payOk');
  if(ok) ok.addEventListener('click', payClose);
  var bg=document.getElementById('payModal');
  if(bg) bg.addEventListener('click', function(e){ if(e.target===bg) payClose(); });
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape'){
      var m=document.getElementById('payModal');
      if(m && m.classList.contains('on')) payClose();
    }
  });
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
/* Buy buttons exist only when there is a price behind them, and the privacy
   line tells the truth about the card form only when there is one. */
function renderCheckout(){
  var any=billingOn();
  document.querySelectorAll('[data-buy]').forEach(function(b){
    b.hidden = !(BILLING.token && BILLING.prices[b.dataset.buy]);
  });
  document.querySelectorAll('[data-i18n="l.pr.trust"]').forEach(function(el){ el.hidden=!any; });
  document.querySelectorAll('.plans-soon').forEach(function(el){ el.hidden=any; });
  document.querySelectorAll('[data-contact]').forEach(function(a){
    a.textContent=CONTACT_EMAIL;
    a.href='mailto:'+CONTACT_EMAIL+'?subject='+encodeURIComponent(t('l.pr.ask.sub'));
  });
  /* "everything stays on your device" stops being the whole truth the moment a
     card can be entered, so the qualified version replaces it then. */
  document.querySelectorAll('[data-privacy]').forEach(function(el){
    el.textContent = t(any ? el.dataset.privacyOn : el.dataset.privacy);
  });
  var lb=document.getElementById('licBox'); if(lb) lb.hidden=!licOn();
  /* "manage my subscription" only once there is a subscription to manage: a
     trial and a grandfathered account have nothing behind that link. */
  var pt=document.getElementById('portalLink');
  if(pt){ pt.hidden=!(BILLING.portal && (licActive()||paidHere())); pt.href=BILLING.portal||'#'; }
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
