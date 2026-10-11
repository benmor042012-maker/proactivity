# -*- coding: utf-8 -*-
"""XP, levels, the evolving avatar, and the friends-bring-friends programme.

S.points is the XP total; nothing here awards points, it only reads them and
decides what they mean. Everything is local: the avatar is drawn from the
tier, and a referral is verified with a hash the two devices can both compute,
because there is no server to ask.
"""

JS_AVATAR = r"""
/* ================= XP and levels =================
   Four ranks at fixed XP thresholds - 0, 500, 1500, 4000 - which is exactly
   where levels 1, 5, 10 and 20 have to land. The curve between them is
   piecewise linear so a level always costs a round number and the next one is
   always in sight: 125 XP a level to rank two, 200 to rank three, 250 to rank
   four, 300 after that. */
var RANKS=[
 {tier:1, lvl:1,  xp:0,    k:'av.r1', d:'av.r1.d'},
 {tier:2, lvl:5,  xp:500,  k:'av.r2', d:'av.r2.d'},
 {tier:3, lvl:10, xp:1500, k:'av.r3', d:'av.r3.d'},
 {tier:4, lvl:20, xp:4000, k:'av.r4', d:'av.r4.d'}
];
function levelXp(L){                       /* the XP at which level L begins */
  if(L<=1) return 0;
  if(L<=5) return (L-1)*125;
  if(L<=10) return 500+(L-5)*200;
  if(L<=20) return 1500+(L-10)*250;
  return 4000+(L-20)*300;
}
function levelFor(xp){ var L=1; while(levelXp(L+1)<=xp) L++; return L; }
function rankFor(xp){ var r=RANKS[0]; RANKS.forEach(function(x){ if(xp>=x.xp) r=x; }); return r; }
function levelInfo(){
  var xp=Math.max(0, Number(S.points)||0), L=levelFor(xp), a=levelXp(L), b=levelXp(L+1);
  var r=rankFor(xp), next=null;
  RANKS.forEach(function(x){ if(!next && x.xp>xp) next=x; });
  return {xp:xp, level:L, from:a, to:b, need:b-xp, pct:Math.round((xp-a)/(b-a)*100),
          rank:r, tier:r.tier, next:next};
}
/* kept for the callers that only ever wanted the label, the level and the bar */
function stageInfo(){ var i=levelInfo(); return {stage:t(i.rank.k), level:i.level, progress:i.pct}; }

/* ================= the avatar =================
   One figure, drawn four ways, on a 100x120 canvas. The same silhouette gets
   broader, better equipped and finally larger - so a level-up reads as growth
   of the same person, not a swap for a different sprite. Fills are CSS
   classes, so the figure follows the theme and the accent like everything
   else on the page. */
var AV_BODY={
 1: '<circle class="sk" cx="50" cy="20" r="8.5"/>'+
    '<rect class="sk" x="47.5" y="27.5" width="5" height="6"/>'+
    '<path class="cl" d="M43 33h14v30H43z"/>'+
    '<path class="sks" style="stroke-width:4.5" d="M43.5 35l-4 24M56.5 35l4 24"/>'+
    '<path class="cl" d="M44 63h5.2v33H44zM50.8 63h5.2v33h-5.2z"/>'+
    '<path class="le" d="M43 96h7v4h-7zM50 96h7v4h-7z"/>',
 2: '<circle class="sk" cx="50" cy="19" r="9"/>'+
    '<path class="le" d="M41 17.5c1.5-8.5 16.5-8.5 18 0-2.5-2.5-15.5-2.5-18 0z"/>'+
    '<rect class="sk" x="46.5" y="27" width="7" height="6"/>'+
    '<path class="cl" d="M38 33h24l-2.5 32h-19z"/>'+
    '<path class="les" style="stroke-width:3" d="M40 34L60 62"/>'+
    '<rect class="le" x="39" y="57" width="22" height="4.5" rx="1"/>'+
    '<rect class="ac" x="48" y="56.5" width="4" height="5.5" rx="1"/>'+
    '<path class="sks" style="stroke-width:5" d="M39 36l-9 13 9 8M61 36l9 13-9 8"/>'+
    '<path class="cl" d="M40.5 65h8l-2.5 30h-7zM51.5 65h8l1.5 30h-7z"/>'+
    '<path class="le" d="M38 95h9.5v6H37zM53 95h9.5v6H53z"/>',
 3: '<circle class="sk" cx="50" cy="19" r="10"/>'+
    '<path class="mt" d="M39 17c1.5-9.5 20.5-9.5 22 0v3.5H39z"/>'+
    '<path class="acs" style="stroke-width:3" d="M50 4v9"/>'+
    '<rect class="sk" x="45.5" y="28" width="9" height="5"/>'+
    '<path class="cl" d="M34 33h32l-2.5 35h-27z"/>'+
    '<path class="mt" d="M39.5 35h21v14L50 55l-10.5-6z"/>'+
    '<circle class="ac" cx="50" cy="43" r="3"/>'+
    '<circle class="mt" cx="34.5" cy="36" r="6.5"/><circle class="mt" cx="65.5" cy="36" r="6.5"/>'+
    '<path class="sks" style="stroke-width:7" d="M33 41l-4.5 19M67 41l4.5 19"/>'+
    '<rect class="mt" x="24.5" y="58" width="9" height="7" rx="2"/><rect class="mt" x="66.5" y="58" width="9" height="7" rx="2"/>'+
    '<path class="cl" d="M37.5 68h9.5v27h-8.5zM53 68h9.5l-1 27H53z"/>'+
    '<path class="mt" d="M37 95h11v8H36zM53 95h11v8H53z"/>'
};
/* the Titan is the Conqueror scaled up, with the crown, the lit eyes, the
   shoulder spikes and the aura - "giant, glowing" without a fifth drawing */
AV_BODY[4] =
  '<circle class="aura" cx="50" cy="62" r="58"/>'+
  '<g transform="translate(50 62) scale(1.15) translate(-50 -62)">'+AV_BODY[3]+
  '<path class="ac" d="M39 12l4-8 7 5 7-5 4 8z"/>'+
  '<circle class="ac" cx="46.5" cy="20" r="1.5"/><circle class="ac" cx="53.5" cy="20" r="1.5"/>'+
  '<path class="ac" d="M30.5 31l-5-8 9 3.5zM69.5 31l5-8-9 3.5z"/>'+
  '<path class="acs" style="stroke-width:2" d="M38.5 58h23"/>'+
  '</g>';
function avatarSvg(tier, label){
  tier=Math.min(4, Math.max(1, tier|0));
  return '<svg class="av t'+tier+'" viewBox="0 0 100 120" '+
    (label ? 'role="img" aria-label="'+esc(label)+'"' : 'aria-hidden="true"')+'>'+AV_BODY[tier]+'</svg>';
}
function avatarLabel(i){ return t('av.aria',{x:t(i.rank.k), n:i.level}); }

/* the header: the small figure next to the level, on every tab */
function renderAvatarMini(){
  var box=document.getElementById('avMini'); if(!box) return;
  var i=levelInfo();
  box.innerHTML=avatarSvg(i.tier);
  var n=document.getElementById('xpN');
  if(n) n.textContent=t('av.next',{n:i.need, l:i.level+1});
}
/* the Home card: the big figure, where it stands, and the four steps */
function renderAvatarCard(){
  var box=document.getElementById('avCard'); if(!box) return;
  var i=levelInfo();
  var ladder=RANKS.map(function(r){
    var on=i.xp>=r.xp;
    return '<li class="av-step'+(on?' on':'')+(r.tier===i.tier?' now':'')+'">'+
      '<span class="av-step-fig">'+avatarSvg(r.tier)+'</span>'+
      '<div><b>'+esc(t(r.k))+'</b><span class="numf">'+esc(t('av.at',{l:r.lvl, n:r.xp}))+'</span>'+
      '<em>'+esc(t(r.d))+'</em></div>'+
      (on?ic('check','av-step-ok'):'')+'</li>';
  }).join('');
  box.innerHTML=
    '<div class="av-hero"><div class="av-big t'+i.tier+'">'+avatarSvg(i.tier, avatarLabel(i))+'</div>'+
    '<div class="av-meta">'+
      '<div class="av-rank">'+esc(t(i.rank.k))+'</div>'+
      '<div class="av-lvl">'+esc(t('av.lvl',{n:i.level}))+' · <span class="numf">'+i.xp+'</span> XP</div>'+
      '<div class="xp big"><i style="width:'+i.pct+'%"></i></div>'+
      '<div class="av-next">'+esc(t('av.next',{n:i.need, l:i.level+1}))+'</div>'+
      '<div class="av-tier-next">'+esc(i.next ? t('av.tier.next',{n:i.next.xp-i.xp, x:t(i.next.k)}) : t('av.max'))+'</div>'+
    '</div></div>'+
    '<div class="acts-h">'+esc(t('av.ladder'))+'</div>'+
    '<ol class="av-ladder">'+ladder+'</ol>';
}

/* ================= friends bring friends =================
   A static site cannot be told by one device that another device signed up.
   What it can do is hand each user a code, and hand each invited friend a
   short token that only the inviter's code can verify: the friend's own code
   plus a four-character check computed from both. The friend sends it back
   (one tap, via the share sheet), the inviter pastes it, the app recomputes
   the check, and the bonus lands. No server, no account, nothing leaves the
   device that the user did not choose to send. */
var REF_BONUS=100;
var REF_ALPHA='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';     /* no 0/O, no 1/I */
function emptyRef(){ return {code:'', redeemed:[], invited:0, from:null, confirm:null, sent:false}; }
function refHash(s){
  var h=2166136261;
  for(var i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619)>>>0; }
  return h>>>0;
}
function refChk(inviter, friend){
  var h=refHash('proactivity:'+inviter+':'+friend), out='';
  for(var i=0;i<4;i++){ out+=REF_ALPHA.charAt(h%32); h=Math.floor(h/32); }
  return out;
}
function isRefCode(c){ return /^[A-HJ-NP-Z2-9]{6}$/.test(c||''); }
function normToken(s){ return String(s||'').toUpperCase().replace(/[^A-Z0-9]/g,''); }
function refCode(){
  if(!S.ref) S.ref=emptyRef();
  if(!S.ref.code){
    var arr=new Uint32Array(6), c='';
    if(window.crypto && crypto.getRandomValues) crypto.getRandomValues(arr);
    else for(var i=0;i<6;i++) arr[i]=Math.floor(Math.random()*4294967296);
    for(var j=0;j<6;j++) c+=REF_ALPHA.charAt(arr[j]%32);
    S.ref.code=c; save();
  }
  return S.ref.code;
}
function inviteLink(){ return location.origin+location.pathname+'?ref='+refCode(); }

/* the inviter's side: paste what the friend sent */
function redeemInvite(raw){
  var tok=normToken(raw);
  if(tok.length!==10) return 'bad';
  var friend=tok.slice(0,6), chk=tok.slice(6);
  if(!isRefCode(friend)) return 'bad';
  if(friend===refCode()) return 'self';
  if(chk!==refChk(refCode(), friend)) return 'bad';
  if(!S.ref.redeemed) S.ref.redeemed=[];
  if(S.ref.redeemed.indexOf(friend)>=0) return 'dup';
  S.ref.redeemed.push(friend); S.ref.invited=(S.ref.invited||0)+1;
  addPts(REF_BONUS); markActiveToday(); save();
  return 'ok';
}
/* the invited side, part one: remember who sent the link. Only a device with
   no profile yet counts as a new sign-up; an existing user opening a friend's
   link is not a referral. The parameter is removed from the address either
   way so a bookmark or a share does not carry it on. */
function captureRefParam(){
  try{
    var p=new URLSearchParams(location.search), r=normToken(p.get('ref'));
    if(!p.has('ref')) return;
    if(isRefCode(r) && !localStorage.getItem('proactive_p')) localStorage.setItem('proactive_ref', r);
    p.delete('ref'); var q=p.toString();
    history.replaceState(null, '', location.pathname+(q?'?'+q:'')+location.hash);
  }catch(e){}
}
/* part two, at the end of onboarding: mint the token the friend sends back */
function applyInvite(){
  var from=null;
  try{ from=localStorage.getItem('proactive_ref'); localStorage.removeItem('proactive_ref'); }catch(e){}
  if(!isRefCode(from)) return;
  if(!S.ref) S.ref=emptyRef();
  var mine=refCode();
  if(from===mine) return;
  S.ref.from=from; S.ref.confirm=mine+refChk(from, mine); S.ref.sent=false;
}

function copyText(text, okKey){
  function done(){ toast(t(okKey)); }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done).catch(function(){ legacyCopy(text); done(); });
  } else { legacyCopy(text); done(); }
}
function legacyCopy(text){
  var ta=document.createElement('textarea');
  ta.value=text; ta.setAttribute('readonly',''); ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select();
  try{ document.execCommand('copy'); }catch(e){}
  ta.remove();
}
function shareText(text, fallbackKey){
  if(navigator.share){
    navigator.share({text:text}).catch(function(){});
  } else copyText(text, fallbackKey);
}

function renderInvite(){
  var box=document.getElementById('inviteCard'); if(!box) return;
  if(!S.ref) S.ref=emptyRef();
  var link=inviteLink(), n=S.ref.invited||0;
  var from = (S.ref.from && S.ref.confirm && !S.ref.sent)
    ? '<div class="inv-from">'+ic('gift')+'<div>'+
        '<div class="inv-from-t">'+esc(t('inv.from.t'))+'</div>'+
        '<p>'+esc(t('inv.from.s',{n:REF_BONUS}))+'</p>'+
        '<div class="inv-code numf">'+esc(S.ref.confirm)+'</div>'+
        '<div class="inv-btns">'+
          '<button class="btn btn-primary btn-sm" data-inv-send>'+ic('share')+'<span>'+esc(t('inv.from.send'))+'</span></button>'+
          '<button class="btn btn-quiet btn-sm" data-inv-sent>'+esc(t('inv.from.done'))+'</button>'+
        '</div></div></div>'
    : '';
  box.innerHTML = from +
    '<p class="psub">'+esc(t('inv.s',{n:REF_BONUS}))+'</p>'+
    '<div class="inv-link">'+ic('link')+'<span class="inv-url">'+esc(link)+'</span></div>'+
    '<div class="inv-btns">'+
      '<button class="btn btn-primary btn-sm" data-inv-copy>'+ic('copy')+'<span>'+esc(t('inv.copy'))+'</span></button>'+
      '<button class="btn btn-ghost btn-sm" data-inv-share>'+ic('share')+'<span>'+esc(t('inv.share'))+'</span></button>'+
    '</div>'+
    '<details class="ch-free inv-how"><summary>'+ic('chevron')+'<span>'+esc(t('inv.how.t'))+'</span></summary>'+
      '<p class="hint">'+ic('shield')+'<span>'+esc(t('inv.how'))+'</span></p></details>'+
    '<div class="addrow inv-redeem">'+
      '<input type="text" id="invCode" autocomplete="off" autocapitalize="characters" spellcheck="false" '+
        'placeholder="'+esc(t('inv.code.ph'))+'" aria-label="'+esc(t('inv.code.ph'))+'">'+
      '<button class="btn btn-primary" id="invGo">'+esc(t('inv.redeem'))+'</button></div>'+
    '<p class="inv-count">'+ic('users')+'<span>'+esc(t('inv.count',{n:n}))+'</span></p>';

  var cp=box.querySelector('[data-inv-copy]');
  if(cp) cp.addEventListener('click',function(){ copyText(link,'inv.copied'); });
  var sh=box.querySelector('[data-inv-share]');
  if(sh) sh.addEventListener('click',function(){ shareText(t('inv.share.msg',{url:link}),'inv.copied'); });
  var sd=box.querySelector('[data-inv-send]');
  if(sd) sd.addEventListener('click',function(){ shareText(t('inv.msg',{c:S.ref.confirm}),'inv.code.copied'); });
  var st=box.querySelector('[data-inv-sent]');
  if(st) st.addEventListener('click',function(){ S.ref.sent=true; save(); renderInvite(); });
  var go=document.getElementById('invGo'), inp=document.getElementById('invCode');
  function redeem(){
    var r=redeemInvite(inp.value);
    if(r==='ok'){ inp.value=''; toast(t('inv.ok',{n:REF_BONUS})); renderInvite(); renderStats(); renderDash(); checkAchievements(); }
    else toast(t(r==='dup' ? 'inv.dup' : r==='self' ? 'inv.self' : 'inv.bad'));
  }
  if(go) go.addEventListener('click', redeem);
  if(inp) inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); redeem(); } });
}
"""
