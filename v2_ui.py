"""v2_ui.py - HTML/JS templates for the animated app_v2.py (no external JS libraries)."""

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900'
         '&family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&family=Cairo:wght@600;700;800;900&display=swap" rel="stylesheet">')
BASE_CSS = """
*{box-sizing:border-box} html,body{margin:0;background:transparent;color:#EBECEF;
  font-family:Inter,'IBM Plex Sans Arabic',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.hud:after{content:"";position:absolute;inset:7px;pointer-events:none;z-index:6;opacity:.9;
  background:
   linear-gradient(#FF2D55,#FF2D55) top left/16px 2px no-repeat, linear-gradient(#FF2D55,#FF2D55) top left/2px 16px no-repeat,
   linear-gradient(#FF2D55,#FF2D55) top right/16px 2px no-repeat, linear-gradient(#FF2D55,#FF2D55) top right/2px 16px no-repeat,
   linear-gradient(#FF2D55,#FF2D55) bottom left/16px 2px no-repeat, linear-gradient(#FF2D55,#FF2D55) bottom left/2px 16px no-repeat,
   linear-gradient(#FF2D55,#FF2D55) bottom right/16px 2px no-repeat, linear-gradient(#FF2D55,#FF2D55) bottom right/2px 16px no-repeat}
.ttl,.ht,h1,.t2{font-family:'Cairo','IBM Plex Sans Arabic',Inter,sans-serif}
"""
PROJ_JS = """
function makeProj(W,H,pad){const k=Math.cos(24*Math.PI/180),lon0=34.3,lon1=56.0,lat0=16.0,lat1=32.5;
 const sc=Math.min((W-2*pad)/((lon1-lon0)*k),(H-2*pad)/(lat1-lat0));
 const ox=(W-(lon1-lon0)*k*sc)/2,oy=(H-(lat1-lat0)*sc)/2;return (lon,lat)=>[ox+(lon-lon0)*k*sc,oy+(lat1-lat)*sc];}
const NS='http://www.w3.org/2000/svg';
function el(t,a,p){const e=document.createElementNS(NS,t);for(const x in a)e.setAttribute(x,a[x]);if(p)p.appendChild(e);return e;}
"""

HERO = FONTS + """<style>""" + BASE_CSS + """
.hero{position:relative;height:540px;border-radius:18px;overflow:hidden;direction:__DIR__;
  background:radial-gradient(900px 520px at 78% 45%,#2B1A1E 0%,#1B1D27 46%,#0C0D11 100%);border:1px solid #2A2D38}
canvas{position:absolute;inset:0;width:100%;height:100%}
.aur{position:absolute;inset:-45%;background:conic-gradient(from 0deg,rgba(232,12,56,0),rgba(232,12,56,.20),
  rgba(220,70,145,.12),rgba(232,12,56,0));filter:blur(70px);animation:rot 20s linear infinite;opacity:.75}
@keyframes rot{to{transform:rotate(360deg)}}
.grid{position:relative;z-index:2;display:grid;grid-template-columns:1.45fr 1fr;height:calc(100% - 46px);padding:30px 48px 10px;gap:18px;align-items:center}
.scan{position:absolute;left:0;right:0;top:-140px;height:140px;z-index:1;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(255,45,85,.10) 70%,rgba(255,45,85,.35) 99%,transparent);animation:scan 7s linear infinite}
@keyframes scan{to{top:100%}}
.lines{position:absolute;inset:0;z-index:1;pointer-events:none;opacity:.35;
  background:repeating-linear-gradient(0deg,rgba(255,255,255,.025) 0 1px,transparent 1px 4px)}
.tick{position:absolute;z-index:5;left:0;right:0;bottom:0;height:46px;display:flex;align-items:center;direction:__DIR__;
  background:linear-gradient(90deg,rgba(255,45,85,.16),rgba(255,45,85,.05));border-top:1px solid rgba(255,45,85,.45)}
.tick .lb{flex:none;height:100%;display:flex;align-items:center;gap:8px;padding:0 18px;background:#FF2D55;color:#fff;
  font-family:'Cairo',sans-serif;font-weight:800;font-size:14px;letter-spacing:.3px}
.tick .lb i{width:8px;height:8px;border-radius:50%;background:#fff;animation:bl 1s infinite}
@keyframes bl{50%{opacity:.2}}
.tw{flex:1;overflow:hidden;height:100%;position:relative;direction:ltr;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.tt{position:absolute;top:0;height:100%;display:flex;align-items:center;white-space:nowrap;animation:mq 60s linear infinite}
.tt span{display:inline-flex;gap:8px;align-items:center;padding:0 22px;font-size:13.5px;color:#E3E4E8;direction:__DIR__;border-inline-end:1px solid rgba(255,255,255,.12)}
.tt span b{color:#fff;font-weight:700}.tt span em{font-style:normal;color:#FF8FA3}.tt span em.n{direction:ltr;font-variant-numeric:tabular-nums}
@keyframes mq{from{transform:translateX(-50%)}to{transform:translateX(0)}}
.badge{display:inline-flex;gap:8px;align-items:center;padding:6px 14px;border-radius:999px;background:rgba(232,12,56,.12);
  border:1px solid rgba(232,12,56,.45);color:#F88493;font-size:13px;font-weight:600}
.badge i{width:8px;height:8px;border-radius:50%;background:#FF2D55;animation:pulse 1.6s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(255,26,72,.7)}70%{box-shadow:0 0 0 10px rgba(255,26,72,0)}100%{box-shadow:0 0 0 0 rgba(255,26,72,0)}}
h1{font-size:104px;line-height:1.05;margin:8px 0 0;font-weight:900;letter-spacing:0;filter:drop-shadow(0 0 28px rgba(255,45,85,.35));
  background:linear-gradient(90deg,#fff 0%,#FBB2BC 35%,#FF335C 60%,#fff 100%);background-size:200% auto;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 5s linear infinite}
@keyframes shine{to{background-position:200% center}}
.t2{font-size:26px;font-weight:300;color:#EBECEF;letter-spacing:.5px;margin-bottom:12px}
.type{font-size:18px;color:#CACCD3;height:30px;font-weight:500}
.type .cur{display:inline-block;width:2px;height:1.05em;background:#FF335C;vertical-align:-3px;animation:blink 1s steps(1) infinite;margin-inline-start:3px}
@keyframes blink{50%{opacity:0}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:24px}
.st{position:relative;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-top:2px solid #FF2D55;border-radius:6px;padding:12px 14px;
  backdrop-filter:blur(6px);opacity:0;transform:translateY(14px);animation:up .7s cubic-bezier(.2,.8,.3,1) forwards}
@keyframes up{to{opacity:1;transform:none}}
.st b{display:flex;gap:4px;align-items:baseline;font-size:32px;font-weight:800;color:#fff;direction:ltr}
.rtl .st b{justify-content:flex-end}
.st b small{font-size:14px;color:#F76478;font-weight:700}
.st > span{font-size:12.5px;color:#9FA1AC}
.pw{display:flex;justify-content:center;align-items:center;position:relative;height:100%}
.rings{position:absolute;width:400px;height:400px}
.rings i{position:absolute;inset:0;border-radius:50%;border:1.5px solid rgba(255,51,92,.4);opacity:0}
.rings.go i{animation:wave 2.4s ease-out}
.rings.go i:nth-child(2){animation-delay:.35s}.rings.go i:nth-child(3){animation-delay:.7s}
@keyframes wave{0%{transform:scale(.3);opacity:.9}100%{transform:scale(1.05);opacity:0}}
.phone{position:relative;width:212px;height:410px;border-radius:40px;background:#070709;border:2px solid #393B47;
  box-shadow:0 30px 80px rgba(0,0,0,.65),0 0 60px rgba(255,26,72,.08),inset 0 0 0 6px #121319;padding:13px;transition:box-shadow .5s}
.phone.alert{box-shadow:0 30px 80px rgba(0,0,0,.65),0 0 80px rgba(255,20,67,.45),inset 0 0 0 6px #121319}
.phone.okay{box-shadow:0 30px 80px rgba(0,0,0,.65),0 0 70px rgba(60,200,100,.35),inset 0 0 0 6px #121319}
.phone.buzz{animation:buzz .42s linear 3}
@keyframes buzz{0%,100%{transform:translateX(0) rotate(0)}25%{transform:translateX(-5px) rotate(-2.5deg)}75%{transform:translateX(5px) rotate(2.5deg)}}
.scr{position:relative;height:100%;border-radius:29px;overflow:hidden;background:linear-gradient(180deg,#2A2C38 0%,#121319 65%);direction:__DIR__}
.scr:after{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 35%,rgba(255,20,67,.45),transparent 60%);opacity:0;transition:opacity .4s}
.phone.alert .scr:after{opacity:1;animation:strobe 1s ease-in-out infinite}
@keyframes strobe{50%{opacity:.25}}
.notch{position:absolute;top:8px;left:50%;transform:translateX(-50%);width:74px;height:20px;background:#000;border-radius:12px;z-index:4}
.clock{position:relative;z-index:2;text-align:center;margin-top:50px;font-size:50px;font-weight:300;color:#fff;direction:ltr}
.date{position:relative;z-index:2;text-align:center;font-size:12px;color:#B2B3BB}
.nt{position:absolute;z-index:3;left:9px;right:9px;top:150px;border-radius:17px;padding:11px 12px;background:rgba(36,20,24,.94);
  border:1px solid rgba(255,26,72,.6);box-shadow:0 12px 30px rgba(0,0,0,.45);transform:translateY(-50px) scale(.92);opacity:0;
  transition:all .55s cubic-bezier(.2,.9,.3,1.25)}
.nt.show{transform:none;opacity:1}
.nt .h{display:flex;gap:6px;align-items:center;font-size:11px;font-weight:800;color:#F76478;letter-spacing:.3px}
.nt .b{font-size:12.5px;color:#fff;margin-top:5px;line-height:1.4}
.nt .eta{font-size:11px;color:#FBB2BC;margin-top:7px}
.nt .pr{height:4px;border-radius:4px;background:rgba(255,255,255,.12);margin-top:6px;overflow:hidden}
.nt .pr i{display:block;height:100%;width:0;background:linear-gradient(90deg,#F50031,#E80C38)}
.nt.ok{border-color:rgba(81,207,102,.65);background:rgba(14,34,22,.95)}
.nt.ok .h{color:#69DB7C}
.demo{position:absolute;z-index:3;bottom:16px;left:0;right:0;text-align:center;font-size:10px;color:#777984}
@media (max-width:820px){.grid{grid-template-columns:1fr;padding:26px}.pw{display:none}h1{font-size:56px}.stats{grid-template-columns:repeat(2,1fr)}}
</style>
<div class="hero hud __DIR__"><canvas id="cv"></canvas><div class="aur"></div><div class="lines"></div><div class="scan"></div>
 <div class="grid">
  <div>
   <span class="badge"><i></i>__BADGE__</span>
   <h1>__TITLE__</h1><div class="t2">__T2__</div>
   <div class="type"><span id="ty"></span><span class="cur"></span></div>
   <div class="stats" id="stats"></div>
  </div>
  <div class="pw"><div class="rings" id="rg"><i></i><i></i><i></i></div>
   <div class="phone" id="ph"><div class="scr"><div class="notch"></div>
     <div class="clock" id="clk">02:14</div><div class="date" id="dt"></div>
     <div class="nt" id="nt"><div class="h" id="nh"></div><div class="b" id="nb"></div><div class="eta" id="ne"></div><div class="pr"><i id="np"></i></div></div>
     <div class="demo">__DEMO__</div></div></div></div>
 </div>
 <div class="tick"><div class="lb"><i></i>__LIVE__</div><div class="tw"><div class="tt" id="tt"></div></div></div>
</div>
<script>
const C=__CFG__;
// live ticker of the latest alerts (content duplicated for a seamless loop)
(function(){const h=C.ticker.map(x=>`<span>🔴 <b>${x.r}</b> <em>${x.d}</em><em class="n">${x.t}</em> · ${x.m}</span>`).join('');
 document.getElementById('tt').innerHTML=h+h;})();
// starfield
const cv=document.getElementById('cv'),cx=cv.getContext('2d');let W,H,stars=[];
function rs(){W=cv.width=cv.offsetWidth*devicePixelRatio;H=cv.height=cv.offsetHeight*devicePixelRatio;
 stars=Array.from({length:140},()=>({x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.4+.2,s:Math.random()*.25+.05,a:Math.random()}));}
rs();addEventListener('resize',rs);
(function loop(){cx.clearRect(0,0,W,H);for(const s of stars){s.y+=s.s;if(s.y>H)s.y=0;s.a+=.02;
 cx.globalAlpha=.35+.35*Math.sin(s.a);cx.fillStyle='#fff';cx.beginPath();cx.arc(s.x,s.y,s.r*devicePixelRatio,0,7);cx.fill();}
 requestAnimationFrame(loop);})();
// stats count-up
const sEl=document.getElementById('stats');
C.stats.forEach((s,i)=>{const d=document.createElement('div');d.className='st';d.style.animationDelay=(0.3+i*0.12)+'s';
 d.innerHTML=`<b><span>0</span>${s.u?`<small>${s.u}</small>`:''}</b><span>${s.l}</span>`;sEl.appendChild(d);
 const n=d.querySelector('b span'),t0=performance.now()+300+i*120;
 (function up(t){const p=Math.min(1,Math.max(0,(t-t0)/1400));n.textContent=Math.round(s.v*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(up);})(t0);});
// typewriter
const ty=document.getElementById('ty');let li=0;
async function typeLoop(){while(true){const s=C.lines[li%C.lines.length];
 for(let i=1;i<=s.length;i++){ty.textContent=s.slice(0,i);await new Promise(r=>setTimeout(r,45));}
 await new Promise(r=>setTimeout(r,1700));
 for(let i=s.length;i>=0;i--){ty.textContent=s.slice(0,i);await new Promise(r=>setTimeout(r,18));}li++;}}
typeLoop();
// phone loop
const ph=document.getElementById('ph'),nt=document.getElementById('nt'),rg=document.getElementById('rg');
const nh=document.getElementById('nh'),nb=document.getElementById('nb'),ne=document.getElementById('ne'),np=document.getElementById('np');
function tick(){const d=new Date();document.getElementById('clk').textContent=d.toTimeString().slice(0,5);
 document.getElementById('dt').textContent=d.toLocaleDateString(C.loc,{weekday:'long',day:'numeric',month:'long'});}
tick();setInterval(tick,10000);
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function phoneLoop(){let k=0;await wait(1200);while(true){const R=C.regions[k%C.regions.length];k++;
 nt.className='nt';np.style.transition='none';np.style.width='0';
 nh.textContent='⚠️ '+C.ph_h;nb.textContent=C.ph_b.replace('{r}',R.n);ne.textContent=C.ph_eta.replace('{m}',R.m);
 ph.classList.remove('okay');void ph.offsetWidth;ph.classList.add('alert','buzz');
 rg.classList.remove('go');void rg.offsetWidth;rg.classList.add('go');
 await wait(250);nt.classList.add('show');await wait(400);
 np.style.transition='width 3.6s linear';np.style.width='100%';await wait(3900);
 ph.classList.remove('alert','buzz');nt.classList.remove('show');await wait(450);
 nt.classList.add('ok');nh.textContent='✅ '+C.ph_ok_h;nb.textContent=C.ph_ok_b.replace('{r}',R.n);ne.textContent='';np.style.transition='none';np.style.width='0';
 ph.classList.add('okay');nt.classList.add('show');await wait(2600);
 nt.classList.remove('show');ph.classList.remove('okay');await wait(1400);}}
phoneLoop();
</script>"""

REPLAY = FONTS + """<style>""" + BASE_CSS + """
.w{position:relative;height:700px;border-radius:14px;overflow:hidden;direction:__DIR__;border:1px solid #2A2D38;
  background:radial-gradient(800px 500px at 35% 45%,#242631 0%,#13141B 65%,#0C0D11 100%)}
.sky{position:absolute;inset:0;background:radial-gradient(900px 500px at 50% -20%,rgba(248,127,143,.16),transparent 60%);opacity:0;transition:opacity 1.2s}
.w:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:30px 30px}
.hd{position:absolute;z-index:3;top:18px;left:24px;right:24px;display:flex;justify-content:space-between;align-items:flex-start}
.ttl{font-size:18px;font-weight:800;color:#fff}.sub{font-size:12.5px;color:#9FA1AC;margin-top:3px}
.clockbox{text-align:end}
.d{font-size:24px;font-weight:800;color:#fff;font-variant-numeric:tabular-nums}
.tm{font-size:13px;color:#F88493;font-variant-numeric:tabular-nums;direction:ltr;display:inline-block}
.dn{font-size:12px;color:#9FA1AC}
.mp{position:absolute;top:70px;bottom:120px;inset-inline-start:0;width:62%}
.mp svg{width:100%;height:100%;direction:ltr}
.land{fill:rgba(255,255,255,.04);stroke:#5E6170;stroke-width:1.5}
.rd{fill:#484A56;transition:fill .3s}
.lb{fill:#9FA1AC;font-size:11.5px;font-weight:600}
.rp{transform-box:fill-box;transform-origin:center;animation:rp 1.8s ease-out forwards}
@keyframes rp{0%{transform:scale(.2);opacity:1}100%{transform:scale(3.2);opacity:0}}
.pn{position:absolute;z-index:3;top:76px;bottom:122px;inset-inline-end:22px;width:34%;display:flex;flex-direction:column;gap:14px}
.big{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:12px 16px}
.big b{font-size:40px;font-weight:900;color:#fff;font-variant-numeric:tabular-nums;line-height:1}
.big span{font-size:12.5px;color:#9FA1AC;margin-inline-start:6px}
.h4{font-size:12px;font-weight:700;color:#9FA1AC;letter-spacing:.4px;margin-bottom:6px}
.race{position:relative;height:216px}
.row{position:absolute;left:0;right:0;height:24px;display:grid;grid-template-columns:96px 1fr 34px;gap:8px;align-items:center;transition:top .45s cubic-bezier(.2,.8,.3,1)}
.row .n{font-size:12.5px;color:#CACCD3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.row .t{height:9px;border-radius:9px;background:#282A34;overflow:hidden}
.row .t i{display:block;height:100%;width:0;border-radius:9px;background:linear-gradient(90deg,#F50031,#E80C38);transition:width .35s}
.row .c{font-size:12.5px;font-weight:800;color:#fff;text-align:end;font-variant-numeric:tabular-nums}
.row.hit .n{color:#F88493}
.log{flex:1;overflow:hidden}
.li{display:flex;justify-content:space-between;font-size:12px;color:#CACCD3;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.05);animation:li .4s ease}
.li .x{color:#777984}.li .x i{font-style:normal;direction:ltr;unicode-bidi:isolate}
@keyframes li{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
.ft{position:absolute;z-index:3;left:22px;right:22px;bottom:14px;height:98px}
.ctl{display:flex;gap:8px;align-items:center;margin-bottom:8px}
button{font-family:inherit;cursor:pointer;border:1px solid #383B47;background:#1C1D25;color:#EBECEF;border-radius:11px;padding:6px 12px;font-size:13px;font-weight:700}
button:hover{border-color:#E80C38} button.on{background:rgba(232,12,56,.18);border-color:#E80C38;color:#F88493}
.hint{margin-inline-start:auto;font-size:11.5px;color:#777984}
.hist{position:relative;height:54px;display:flex;align-items:flex-end;gap:2px;cursor:pointer;direction:ltr}
.hist i{flex:1;background:#31333D;border-radius:3px 3px 0 0;transition:background .3s;min-height:2px}
.hist i.p{background:linear-gradient(180deg,#F76478,#E80C38)}
.ph{position:absolute;top:-4px;bottom:0;width:2px;background:#fff;box-shadow:0 0 10px #FF335C;left:0}
.end{position:absolute;inset:0;z-index:5;display:flex;align-items:center;justify-content:center;background:rgba(12,13,17,.55);
  backdrop-filter:blur(3px);opacity:0;pointer-events:none;transition:opacity .6s}
.end.on{opacity:1;pointer-events:auto}
.end div{text-align:center}.end b{display:block;font-size:30px;font-weight:900;color:#fff;margin-bottom:12px}
@media (max-width:820px){.mp{width:100%;bottom:330px}.pn{top:auto;bottom:122px;width:auto;left:22px;right:22px;height:200px}.race{display:none}}
</style>
<div class="w hud __DIR__" id="w"><div class="sky" id="sky"></div>
 <div class="hd"><div><div class="ttl">__T__</div><div class="sub">__S__</div></div>
  <div class="clockbox"><div class="d" id="d"></div><div><span class="dn" id="dn"></span> · <span class="tm" id="tm"></span></div></div></div>
 <div class="mp"><svg id="svg"></svg></div>
 <div class="pn"><div class="big"><b id="cnt">0</b><span>__C__</span></div>
  <div><div class="h4">__RK__</div><div class="race" id="race"></div></div>
  <div class="log"><div class="h4">__LG__</div><div id="log"></div></div></div>
 <div class="ft"><div class="ctl"><button id="pp">⏸</button><button id="rs">↺</button>
   <button data-s="0.5">0.5×</button><button data-s="1" class="on">1×</button><button data-s="2">2×</button><button data-s="4">4×</button>
   <span class="hint">__H__</span></div>
  <div class="hist" id="hist"><div class="ph" id="ph"></div></div></div>
 <div class="end" id="end"><div><b id="endt"></b><button id="again">↺</button></div></div>
</div>
<script>
""" + PROJ_JS + """
const C=__CFG__;const $=id=>document.getElementById(id);
const EV=C.events, RG=C.regions, DAYS=C.days, START=new Date(C.start), END=DAYS*1440;
let cur=0,run=true,mult=1,last=performance.now(),idx=0,counts=RG.map(()=>0),P,dots=[],rows=[];
const BASE=1440*1.6; // simulated minutes per real second at 1x (about 40 s for the whole period)
function build(){const box=document.querySelector('.mp'),W=box.clientWidth,H=box.clientHeight;if(!W)return false;
 const svg=$('svg');svg.setAttribute('viewBox',`0 0 ${W} ${H}`);P=makeProj(W,H,26);
 el('path',{d:C.outline.map((q,i)=>(i?'L':'M')+P(q[0],q[1]).map(v=>v.toFixed(1)).join(' ')).join(' ')+'Z',class:'land'},svg);
 RG.forEach((r,i)=>{const[x,y]=P(r.lon,r.lat);const g=el('g',{},svg);
  dots[i]={g,x,y,c:el('circle',{cx:x,cy:y,r:5,class:'rd'},g)};
  const tx=el('text',{x:r.side==='l'?x-10:x+10,y:y+4+r.dy,class:'lb','text-anchor':r.side==='l'?'end':'start'},svg);tx.textContent=r.name;});
 return true;}
// region race rows
RG.forEach((r,i)=>{const d=document.createElement('div');d.className='row';d.innerHTML=`<div class="n">${r.name}</div><div class="t"><i></i></div><div class="c">0</div>`;
 $('race').appendChild(d);rows[i]=d;});
// daily histogram
const daily=Array(DAYS).fill(0);EV.forEach(e=>daily[Math.min(DAYS-1,Math.floor(e[0]/1440))]++);const dmax=Math.max(...daily);
const bars=daily.map(v=>{const b=document.createElement('i');b.style.height=(v/dmax*100)+'%';$('hist').insertBefore(b,$('ph'));return b;});
function race(hit){const mx=Math.max(1,...counts);const order=counts.map((c,i)=>[c,i]).sort((a,b)=>b[0]-a[0]);
 order.forEach(([c,i],rank)=>{rows[i].style.top=(rank*27)+'px';rows[i].querySelector('i').style.width=(c/mx*100)+'%';
  rows[i].querySelector('.c').textContent=c;rows[i].classList.toggle('hit',i===hit);});}
function pulse(i){const d=dots[i];if(!d)return;
 const c=el('circle',{cx:d.x,cy:d.y,r:9,fill:'none',stroke:'#FF335C','stroke-width':2.5,class:'rp'},d.g);setTimeout(()=>c.remove(),1900);
 const f=el('circle',{cx:d.x,cy:d.y,r:12,fill:'rgba(255,26,72,.35)',class:'rp'},d.g);setTimeout(()=>f.remove(),1900);
 d.c.style.fill='#FF335C';d.c.setAttribute('r',7);clearTimeout(d.to);d.to=setTimeout(()=>{d.c.style.fill='';d.c.setAttribute('r',5);},900);}
function stamp(m){const t=new Date(START.getTime()+m*60000);return t;}
function fmtT(t){return String(t.getHours()).padStart(2,'0')+':'+String(t.getMinutes()).padStart(2,'0');}
function logLine(e){const t=stamp(e[0]);const d=document.createElement('div');d.className='li';
 d.innerHTML=`<span>${RG[e[1]].name}</span><span class="x">${t.toLocaleDateString(C.loc,{day:'numeric',month:'short'})} <i>${fmtT(t)}</i> · <i>${e[2]}'</i></span>`;
 const lg=$('log');lg.insertBefore(d,lg.firstChild);while(lg.children.length>6)lg.lastChild.remove();}
function hud(){const t=stamp(cur),day=Math.min(DAYS,Math.floor(cur/1440)+1);
 $('d').textContent=t.toLocaleDateString(C.loc,{day:'numeric',month:'long',year:'numeric'});
 $('tm').textContent=fmtT(t);const h=t.getHours(),night=h>=22||h<6;$('sky').style.opacity=night?0:1;
 $('dn').textContent=(night?'🌙 ':'☀️ ')+C.day.replace('{d}',day).replace('{n}',DAYS);
 $('cnt').textContent=idx;$('ph').style.left=(Math.min(1,cur/END)*100)+'%';
 bars.forEach((b,i)=>b.classList.toggle('p',i<day));}
function seek(m){cur=m;idx=0;counts=RG.map(()=>0);$('log').innerHTML='';
 while(idx<EV.length&&EV[idx][0]<=cur){counts[EV[idx][1]]++;idx++;}
 EV.slice(Math.max(0,idx-6),idx).forEach(logLine);race(-1);hud();$('end').classList.remove('on');}
function finish(){run=false;$('pp').textContent='▶';$('endt').textContent=C.done;$('end').classList.add('on');}
function loop(t){const dt=Math.min(.1,(t-last)/1000);last=t;
 if(run){cur+=dt*BASE*mult;let hit=-1;
  while(idx<EV.length&&EV[idx][0]<=cur){const e=EV[idx];counts[e[1]]++;pulse(e[1]);logLine(e);hit=e[1];idx++;}
  if(hit>=0)race(hit);if(cur>=END){cur=END;hud();finish();}else hud();}
 requestAnimationFrame(loop);}
function start(){if(!build()){requestAnimationFrame(start);return;}race(-1);hud();requestAnimationFrame(loop);}
$('pp').onclick=()=>{if(cur>=END){seek(0);run=true;$('pp').textContent='⏸';return;}run=!run;$('pp').textContent=run?'⏸':'▶';};
$('rs').onclick=$('again').onclick=()=>{seek(0);run=true;$('pp').textContent='⏸';};
document.querySelectorAll('.ctl button[data-s]').forEach(b=>b.onclick=()=>{mult=+b.dataset.s;
 document.querySelectorAll('.ctl button[data-s]').forEach(x=>x.classList.toggle('on',x===b));});
$('hist').onclick=ev=>{const r=$('hist').getBoundingClientRect();seek(Math.max(0,Math.min(1,(ev.clientX-r.left)/r.width))*END);};
start();
</script>"""


KSA_OUTLINE = [(34.95,29.36),(36.07,29.19),(37.0,30.5),(37.67,31.0),(39.2,32.16),(40.4,31.95),(42.1,31.1),
    (44.7,29.18),(46.55,29.1),(47.46,29.0),(48.4,28.55),(48.8,27.7),(49.3,27.2),(50.15,26.65),(50.2,25.7),
    (50.8,24.75),(51.6,24.25),(52.0,23.0),(55.0,22.7),(55.67,22.0),(55.0,20.0),(52.0,19.0),(49.1,18.6),(48.2,18.15),
    (47.5,17.1),(46.75,17.28),(45.4,17.33),(44.1,17.4),(43.4,17.5),(43.1,17.0),(42.8,16.4),(42.6,16.8),(41.2,19.0),
    (40.0,20.3),(39.1,21.6),(38.5,23.6),(37.5,24.6),(36.6,25.8),(35.2,27.6),(34.6,28.1)]
COORDS = {"Asir": (18.22, 42.50), "Najran": (17.49, 44.13), "Riyadh": (24.71, 46.68), "Jazan": (16.89, 42.55),
          "Makkah": (21.42, 39.83), "Madinah": (24.47, 39.61), "Eastern Province": (26.42, 50.09), "Tabuk": (28.38, 36.57)}
LABEL_SIDE = {"Asir": ("l", -14), "Jazan": ("l", 16), "Najran": ("r", 0), "Makkah": ("l", 0),
              "Madinah": ("l", 0), "Riyadh": ("r", 0), "Eastern Province": ("r", -6), "Tabuk": ("r", 0)}

# ---------------------------------------------------------------- tomorrow outlook: gauge + time-of-day clock + clear countdown
OUTLOOK = FONTS + """<style>""" + BASE_CSS + """
.wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;direction:__DIR__}
.pnl{position:relative;border-radius:14px;padding:18px 20px 16px;overflow:hidden;height:560px;
  background:linear-gradient(165deg,#1D1F28 0%,#171920 60%,#17131F 100%);border:1px solid #2F313C;
  opacity:0;transform:translateY(16px);animation:up .7s cubic-bezier(.2,.8,.3,1) forwards}
.pnl:nth-child(2){animation-delay:.12s}.pnl:nth-child(3){animation-delay:.24s}
@keyframes up{to{opacity:1;transform:none}}
.pnl:before{content:"";position:absolute;width:300px;height:300px;border-radius:50%;top:-120px;inset-inline-end:-100px;
  background:radial-gradient(circle,var(--glow,rgba(255,26,72,.18)) 0%,transparent 65%)}
.hdr{position:relative;display:flex;align-items:center;gap:10px}
.num{width:26px;height:26px;border-radius:4px;display:grid;place-items:center;font-size:13px;font-weight:800;
  background:rgba(232,12,56,.16);color:#F88493;border:1px solid rgba(232,12,56,.4)}
.ht{font-size:14.5px;font-weight:700;color:#EBECEF}
.sub{position:relative;font-size:12px;color:#9A9CA5;margin-top:3px;min-height:16px}
svg{display:block;margin:6px auto 0;overflow:visible}
.big{position:relative;text-align:center;font-size:52px;font-weight:900;color:#fff;line-height:1;font-variant-numeric:tabular-nums;direction:ltr}
.big small{font-size:20px;font-weight:700;margin-inline-start:2px}
.pill{display:inline-block;margin-top:10px;padding:5px 14px;border-radius:999px;font-size:13px;font-weight:800}
.cen{position:relative;text-align:center}
.foot{position:absolute;left:20px;right:20px;bottom:14px;font-size:12px;color:#9A9CA5;text-align:center;line-height:1.45}
.needle{transform-origin:150px 150px;transition:transform 1.8s cubic-bezier(.25,1.4,.4,1)}
.q{transition:opacity .6s}
.q.hot{animation:hot 1.6s ease-in-out infinite}
@keyframes hot{50%{opacity:.55}}
.hand{transform-origin:130px 130px;transition:transform 1.6s cubic-bezier(.25,1.3,.4,1)}
.lgd{position:relative;display:grid;gap:7px;margin-top:6px}
.lh{display:flex;justify-content:space-between;font-size:11px;color:#777984;padding:0 2px}
.lr{display:grid;grid-template-columns:104px 1fr 48px;gap:10px;align-items:center;font-size:13px;color:#CACCD3;
  padding:5px 8px;border-radius:10px;border:1px solid transparent}
.lr .bb{position:relative;height:10px;border-radius:10px;background:#282A34;overflow:hidden}
.lr .bb i{position:absolute;top:0;bottom:0;inset-inline-start:0;width:0;border-radius:10px;transition:width 1.2s cubic-bezier(.2,.8,.3,1)}
.lr b{font-size:17px;font-weight:900;color:#fff;text-align:end;font-variant-numeric:tabular-nums;direction:ltr}
.lr small{display:block;font-size:10.5px;color:#777984;font-weight:500}
.lr small.hs{color:#EBECEF;font-weight:700;border-bottom:1px dashed #9A9CA5;width:fit-content}
.lr.top{background:rgba(255,51,92,.08);border-color:rgba(255,51,92,.45);color:#FBB2BC}
.lr.top b{color:#F88493}
.cd{position:relative;width:250px;height:250px;margin:26px auto 0}
.cd svg{position:absolute;inset:0;margin:0}
.cd .in{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.mm{font-size:72px;font-weight:900;color:#fff;line-height:1;font-variant-numeric:tabular-nums;direction:ltr}
.cd .lb{font-size:14px;color:#CACCD3;margin-top:4px}
.iqr{position:relative;margin:16px auto 0;width:fit-content;font-size:13px;color:#FBB2BC;background:rgba(255,61,100,.1);
  border:1px solid rgba(255,61,100,.35);border-radius:999px;padding:7px 16px;text-align:center}
.iqr b{color:#fff}
@media (max-width:900px){.wrap{grid-template-columns:1fr}}
</style>
<div class="wrap __DIR__">
 <!-- 1. risk gauge -->
 <div class="pnl hud" id="p1"><div class="hdr"><span class="num">1</span><span class="ht" id="h1"></span></div><div class="sub" id="s1"></div>
  <svg width="300" height="185" viewBox="0 0 300 185" style="margin-top:34px">
   <defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" stop-color="#40C057"/><stop offset=".45" stop-color="#FFC233"/><stop offset="1" stop-color="#FF2D55"/></linearGradient></defs>
   <path d="M40 150 A110 110 0 0 1 260 150" fill="none" stroke="#292B35" stroke-width="26" stroke-linecap="round"/>
   <path d="M40 150 A110 110 0 0 1 260 150" fill="none" stroke="url(#gr)" stroke-width="16" stroke-linecap="round" opacity=".9"/>
   <g id="gt"></g>
   <g class="needle" id="nd" style="transform:rotate(-90deg)">
     <line x1="150" y1="150" x2="150" y2="58" stroke="#fff" stroke-width="4" stroke-linecap="round" style="filter:drop-shadow(0 0 6px rgba(255,255,255,.6))"/>
   </g>
   <circle cx="150" cy="150" r="11" fill="#101116" stroke="#fff" stroke-width="3"/>
  </svg>
  <div class="big" id="pc">0<small>%</small></div>
  <div class="cen"><span class="pill" id="lv"></span></div>
  <div class="foot" id="f1"></div></div>
 <!-- 2. time of day -->
 <div class="pnl hud" id="p2"><div class="hdr"><span class="num">2</span><span class="ht" id="h2"></span></div><div class="sub" id="s2"></div>
  <svg width="225" height="225" viewBox="0 0 260 260" id="clk"></svg>
  <div class="lgd" id="lg"><div class="lh"><span id="lh1"></span><span id="lh2"></span></div></div></div>
 <!-- 3. usual time until the all-clear (static) -->
 <div class="pnl hud" id="p3"><div class="hdr"><span class="num">3</span><span class="ht" id="h3"></span></div><div class="sub" id="s3"></div>
  <div class="cd"><svg viewBox="0 0 250 250" width="250" height="250" id="cring">
    <defs><linearGradient id="cg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#FFC233"/><stop offset="1" stop-color="#E80C38"/></linearGradient></defs>
    <circle cx="125" cy="125" r="96" fill="none" stroke="#292B35" stroke-width="20"/></svg>
   <div class="in"><div class="mm" id="mm"></div><div class="lb" id="cl"></div></div></div>
  <div class="iqr" id="iqr"></div>
  <div class="foot" id="f3"></div></div>
</div>
<script>
const C=__CFG__;const $=id=>document.getElementById(id);const NS='http://www.w3.org/2000/svg';
function el(t,a,p){const e=document.createElementNS(NS,t);for(const x in a)e.setAttribute(x,a[x]);if(p)p.appendChild(e);return e;}
['h1','s1','f1','h2','s2','h3','s3','f3','lh1','lh2'].forEach(k=>{$(k).innerHTML=C.txt[k]||'';});
// ---- 1. gauge
const LC={High:'#FF2D55',Medium:'#FFC233',Low:'#51CF66'};
[[C.th_med,'#FFC233'],[C.th_high,'#FF2D55']].forEach(([v,c])=>{const a=Math.PI*(1-v);
 el('line',{x1:150+128*Math.cos(a),y1:150-128*Math.sin(a),x2:150+140*Math.cos(a),y2:150-140*Math.sin(a),stroke:c,'stroke-width':3},$('gt'));
 const tx=el('text',{x:150+156*Math.cos(a),y:150-156*Math.sin(a)+4,fill:'#9A9CA5','font-size':11,'text-anchor':'middle'},$('gt'));tx.textContent=Math.round(v*100)+'%';});
$('lv').textContent=C.level_txt;$('lv').style.background=LC[C.level]+'26';$('lv').style.color=LC[C.level];
$('p1').style.setProperty('--glow',LC[C.level]+'30');
setTimeout(()=>{$('nd').style.transform=`rotate(${-90+C.p*180}deg)`;},250);
(function(){const t0=performance.now()+250,n=$('pc');(function f(t){const k=Math.min(1,Math.max(0,(t-t0)/1500));
 n.innerHTML=Math.round(C.p*100*(1-Math.pow(1-k,3)))+'<small>%</small>';if(k<1)requestAnimationFrame(f);})(t0);})();
// ---- 2. 24h clock with the four periods
const svg=$('clk'),cx=130,cy=130;const ang=h=>(h/24*360-90)*Math.PI/180;
function arcPath(r,h0,h1){const a0=ang(h0),a1=ang(h1);return `M${cx+r*Math.cos(a0)} ${cy+r*Math.sin(a0)} A${r} ${r} 0 0 1 ${cx+r*Math.cos(a1)} ${cy+r*Math.sin(a1)}`;}
const per=C.periods, mx=Math.max(...per.map(p=>p.m));
el('circle',{cx,cy,r:58,fill:'#16171E',stroke:'#2F313C'},svg);
per.forEach((p,i)=>{const h0=i*6+0.25,h1=i*6+5.75;
 const q=el('path',{d:arcPath(96,h0,h1),fill:'none',stroke:p.c,'stroke-width':30,'stroke-linecap':'butt',class:'q'+(p.hot?' hot':''),opacity:.18},svg);
 setTimeout(()=>q.setAttribute('opacity',(0.3+0.7*p.m/mx).toFixed(2)),300+i*120);
 const am=ang(i*6+3);
 const pt=el('text',{x:cx+96*Math.cos(am),y:cy+96*Math.sin(am)+5,'text-anchor':'middle',fill:'#fff','font-size':14,'font-weight':800,
   style:'paint-order:stroke;stroke:rgba(0,0,0,.45);stroke-width:3px'},svg);pt.textContent=Math.round(p.m*100)+'%';
 const ic=el('text',{x:cx+126*Math.cos(am),y:cy+126*Math.sin(am)+6,'text-anchor':'middle','font-size':17},svg);ic.textContent=p.icon;
 if(p.hist){el('path',{d:arcPath(115,h0,h1),fill:'none',stroke:'#EBECEF','stroke-width':2,'stroke-dasharray':'5 5',opacity:.85},svg);
  el('path',{d:arcPath(78,h0,h1),fill:'none',stroke:'#EBECEF','stroke-width':2,'stroke-dasharray':'5 5',opacity:.85},svg);}});
[0,6,12,18].forEach(h=>{const a=ang(h);const t=el('text',{x:cx+44*Math.cos(a),y:cy+44*Math.sin(a)+4,'text-anchor':'middle',fill:'#777984','font-size':10},svg);t.textContent=String(h).padStart(2,'0');});
const hand=el('g',{class:'hand',style:'transform:rotate(0deg)'},svg);
el('line',{x1:cx,y1:cy,x2:cx,y2:cy-62,stroke:'#F88493','stroke-width':3.5,'stroke-linecap':'round'},hand);
el('circle',{cx,cy,r:6,fill:'#F88493'},svg);
setTimeout(()=>{hand.style.transform=`rotate(${C.hand_h/24*360}deg)`;},400);
const lg=$('lg');[...per].sort((a,b)=>b.m-a.m).forEach((p,i)=>{const r=document.createElement('div');r.className='lr'+(p.hot?' top':'');
 r.innerHTML=`<span>${p.icon} ${p.name}<small${p.hist?' class="hs"':''}>${p.hist?C.txt.hist_tag+': '+Math.round(p.s*100)+'%':C.txt.past.replace('{s}',Math.round(p.s*100)+'%')}</small></span><span class="bb"><i style="background:${p.c}"></i></span><b>${Math.round(p.m*100)}%</b>`;lg.appendChild(r);
 setTimeout(()=>{r.querySelector('.bb i').style.width=(p.m/mx*100)+'%';},350+i*100);});
// ---- 3. usual time until the all-clear: static ring (median, with the middle-50% band)
(function(){const g=$('cring'),c=125,R=96,scale=Math.max(30,Math.ceil((C.q75+5)/5)*5),A=m=>(m/scale*360-90)*Math.PI/180;
 const arc=(m0,m1)=>{const a0=A(m0),a1=A(m1),big=(m1-m0)/scale>.5?1:0;return `M${c+R*Math.cos(a0)} ${c+R*Math.sin(a0)} A${R} ${R} 0 ${big} 1 ${c+R*Math.cos(a1)} ${c+R*Math.sin(a1)}`;};
 el('path',{d:arc(C.q25,C.q75),fill:'none',stroke:'rgba(255,61,100,.35)','stroke-width':20},g);
 el('path',{d:arc(0.01,C.clear),fill:'none',stroke:'url(#cg)','stroke-width':10,'stroke-linecap':'round'},g);
 const a=A(C.clear);el('circle',{cx:c+R*Math.cos(a),cy:c+R*Math.sin(a),r:8,fill:'#fff',style:'filter:drop-shadow(0 0 8px #FF335C)'},g);
 for(let m=0;m<scale;m+=5){const t=A(m),big=m%10===0;
  el('line',{x1:c+(R+14)*Math.cos(t),y1:c+(R+14)*Math.sin(t),x2:c+(R+(big?22:18))*Math.cos(t),y2:c+(R+(big?22:18))*Math.sin(t),stroke:'#484A56','stroke-width':big?2:1},g);
  if(big){const x=el('text',{x:c+(R+33)*Math.cos(t),y:c+(R+33)*Math.sin(t)+4,'text-anchor':'middle',fill:'#777984','font-size':10},g);x.textContent=m+"'";}}
 $('mm').textContent=C.clear_txt;$('cl').textContent=C.txt.cl;$('iqr').innerHTML=C.txt.iqr;})();
</script>"""

# ---------------------------------------------------------------- all regions: risk map + animated ranking
RISKMAP = FONTS + """<style>""" + BASE_CSS + """
.w{position:relative;height:600px;border-radius:14px;overflow:hidden;direction:__DIR__;border:1px solid #2A2D38;
  background:radial-gradient(700px 450px at 35% 50%,#282A35 0%,#13141B 70%)}
.w:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
 linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:28px 28px}
.mp{position:absolute;top:0;bottom:0;inset-inline-start:0;width:60%}
.mp svg{width:100%;height:100%;direction:ltr}
.land{fill:rgba(255,255,255,.045);stroke:#6C6F7E;stroke-width:1.6;stroke-dasharray:2600;stroke-dashoffset:2600;animation:dr 2.4s ease forwards}
@keyframes dr{to{stroke-dashoffset:0}}
.sweep{animation:spin 6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}
@keyframes ring{0%{transform:scale(.3);opacity:.8}100%{transform:scale(1.7);opacity:0}}
.pt{opacity:0;animation:pop .6s cubic-bezier(.2,.9,.3,1.4) forwards}
@keyframes pop{to{opacity:1}}
.tg rect{fill:rgba(19,20,27,.9);stroke:rgba(255,255,255,.14)}
.tg text{fill:#fff;font-size:12px;font-weight:600}
.ls{position:absolute;top:18px;bottom:18px;inset-inline-end:20px;width:37%;display:flex;flex-direction:column;gap:6px}
.ttl{font-size:13px;font-weight:700;color:#9FA1AC;margin-bottom:4px}
.it{display:grid;grid-template-columns:22px 1fr 54px;gap:10px;align-items:center;padding:7px 12px;border-radius:14px;
  background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);opacity:0;transform:translateX(20px);animation:sl .6s cubic-bezier(.2,.8,.3,1) forwards}
.rtl .it{transform:translateX(-20px)}
@keyframes sl{to{opacity:1;transform:none}}
.it.sel{border-color:rgba(255,51,92,.6);background:rgba(255,51,92,.08)}
.rk{font-size:12px;font-weight:800;color:#777984}
.nm{font-size:13.5px;font-weight:700;color:#fff}.nm small{display:block;font-size:11px;font-weight:500;color:#9A9CA5}
.br{height:5px;border-radius:5px;background:#292B35;margin-top:5px;overflow:hidden}.br i{display:block;height:100%;width:0;border-radius:5px;transition:width 1.2s cubic-bezier(.2,.8,.3,1)}
.pc{font-size:18px;font-weight:900;text-align:end;font-variant-numeric:tabular-nums;direction:ltr}
.lgd{position:absolute;bottom:14px;inset-inline-start:20px;display:flex;gap:14px;font-size:12px;color:#B2B3BB}
.lgd i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-inline-end:6px;vertical-align:-1px}
@media (max-width:820px){.mp{width:100%;height:330px;bottom:auto}.ls{top:340px;width:auto;left:16px;right:16px}.w{height:900px}}
</style>
<div class="w hud __DIR__"><div class="mp"><svg id="svg"></svg></div><div class="ls" id="ls"><div class="ttl">__TTL__</div></div><div class="lgd" id="lgd"></div></div>
<script>
""" + PROJ_JS + """
const C=__CFG__;const $=id=>document.getElementById(id);
const LC={High:'#FF2D55',Medium:'#FFC233',Low:'#51CF66'};
C.items.forEach((x,i)=>{const d=document.createElement('div');d.className='it'+(x.sel?' sel':'');d.style.animationDelay=(0.15+i*0.07)+'s';
 d.innerHTML=`<span class="rk">${i+1}</span><div class="nm">${x.name}<small>${x.sub}</small><div class="br"><i style="background:${LC[x.lvl]}"></i></div></div><span class="pc" style="color:${LC[x.lvl]}">${Math.round(x.p*100)}%</span>`;
 $('ls').appendChild(d);setTimeout(()=>d.querySelector('.br i').style.width=(x.p*100)+'%',400+i*70);});
$('lgd').innerHTML=C.levels.map(l=>`<span><i style="background:${LC[l[0]]}"></i>${l[1]}</span>`).join('');
let drawn=false;
function draw(){const box=document.querySelector('.mp'),W=box.clientWidth,H=box.clientHeight;if(!W||drawn)return;drawn=true;
 const svg=$('svg');svg.setAttribute('viewBox',`0 0 ${W} ${H}`);const P=makeProj(W,H,34);
 const defs=el('defs',{},svg);const lg=el('linearGradient',{id:'cone',x1:0,y1:0,x2:1,y2:0},defs);
 el('stop',{offset:0,'stop-color':'#E80C38','stop-opacity':0},lg);el('stop',{offset:1,'stop-color':'#E80C38','stop-opacity':.3},lg);
 const d=C.outline.map((q,i)=>(i?'L':'M')+P(q[0],q[1]).map(v=>v.toFixed(1)).join(' ')).join(' ')+'Z';
 const cp=el('clipPath',{id:'c'},defs);el('path',{d},cp);el('path',{d,class:'land'},svg);
 const [cx,cy]=P(45,24),R=Math.max(W,H);const sg=el('g',{'clip-path':'url(#c)'},svg);
 const sw=el('path',{d:`M${cx} ${cy} L${cx+R} ${cy} A${R} ${R} 0 0 0 ${cx+R*Math.cos(-.7)} ${cy+R*Math.sin(-.7)} Z`,fill:'url(#cone)',class:'sweep'},sg);
 sw.style.transformOrigin=`${cx}px ${cy}px`;
 [...C.items].sort((a,b)=>a.p-b.p).forEach((x,i)=>{const[px,py]=P(x.lon,x.lat),s=7+x.p*14,c=LC[x.lvl];
  const g=el('g',{class:'pt',style:`animation-delay:${.9+i*.12}s`},svg);
  el('circle',{cx:px,cy:py,r:s*2.2,fill:c,class:'ring',style:`opacity:.5;animation-delay:${(i*.35)%2.6}s`},g);
  el('circle',{cx:px,cy:py,r:s*.55,fill:c,stroke:'#fff','stroke-width':x.sel?3:2,style:`filter:drop-shadow(0 0 8px ${c})`},g);
  const tg=el('g',{class:'tg'},g);const tx=el('text',{},tg);tx.textContent=x.name;const tp=el('text',{style:`fill:${c};font-weight:800`},tg);tp.textContent=Math.round(x.p*100)+'%';
  const w1=tx.getComputedTextLength(),w=w1+tp.getComputedTextLength()+22;let lx=x.side==='l'?px-s*.9-6-w:px+s*.9+6;
  if(lx+w>W-6)lx=px-s*.9-6-w;if(lx<6)lx=px+s*.9+6;const ly=py-12+x.dy;
  const rc=el('rect',{x:lx,y:ly,width:w,height:24,rx:8});tg.insertBefore(rc,tx);
  tx.setAttribute('x',lx+8);tx.setAttribute('y',ly+16.5);tp.setAttribute('x',lx+w1+14);tp.setAttribute('y',ly+16.5);});}
new ResizeObserver(draw).observe(document.querySelector('.mp'));draw();
</script>"""

# ---------------------------------------------------------------- tomorrow outlook v3: three matching cockpit instruments
OUTLOOK3 = FONTS + """<style>""" + BASE_CSS + """
.wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;direction:__DIR__}
.card{position:relative;border-radius:14px;padding:18px 20px 16px;overflow:hidden;height:500px;display:flex;flex-direction:column;align-items:center;
  background:radial-gradient(420px 300px at 50% 46%,rgba(255,45,85,.10),transparent 70%),linear-gradient(170deg,#1D1F28 0%,#15161D 100%);
  border:1px solid #2F313C;opacity:0;transform:translateY(16px);animation:up .7s cubic-bezier(.2,.8,.3,1) forwards}
.card:nth-child(2){animation-delay:.12s}.card:nth-child(3){animation-delay:.24s}
@keyframes up{to{opacity:1;transform:none}}
.hd{align-self:stretch;display:flex;align-items:center;gap:10px}
.num{width:26px;height:26px;border-radius:4px;display:grid;place-items:center;font-size:13px;font-weight:800;background:rgba(255,45,85,.16);color:#FF8FA3;border:1px solid rgba(255,45,85,.45)}
.ht{font-size:15.5px;font-weight:800;color:#EBECEF}
.inst{position:relative;width:270px;height:270px;margin-top:30px}
.inst svg{position:absolute;inset:0;overflow:visible}
.ctr{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.big{font-family:Inter,sans-serif;font-size:62px;font-weight:900;color:#fff;line-height:1;font-variant-numeric:tabular-nums;direction:ltr}
.big small{font-size:22px;font-weight:800;margin-inline-start:2px;color:#FF8FA3}
.unit{font-size:13px;color:#9FA1AC;margin-top:4px}
.pn{font-family:'Cairo',sans-serif;font-size:30px;font-weight:900;color:#fff;line-height:1.1}
.pi{font-size:30px;line-height:1;margin-bottom:2px}
.ph{font-size:11.5px;color:#9FA1AC;margin-top:3px}
.pill{margin-top:8px;padding:5px 14px;border-radius:999px;font-size:13px;font-weight:800}
.sub{margin-top:auto;align-self:stretch;text-align:center;font-size:12.5px;color:#9FA1AC;line-height:1.5}
.sub b{color:#fff}
.chips{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:6px}
.chips span{font-size:12px;padding:4px 9px;border-radius:8px;background:#22242D;color:#CACCD3;border:1px solid #2F313C;direction:__DIR__}
.chips span b{color:#fff;direction:ltr;unicode-bidi:isolate}
.chips span.hot{background:rgba(255,45,85,.14);border-color:rgba(255,45,85,.55);color:#FF8FA3}
.chips span.hist{border-style:dashed;border-color:#8F919C}
.fill{transition:stroke-dashoffset 1.6s cubic-bezier(.2,.8,.3,1)}
.hand{transition:transform 1.6s cubic-bezier(.25,1.3,.4,1)}
@media (max-width:900px){.wrap{grid-template-columns:1fr}}
</style>
<div class="wrap __DIR__">
 <div class="card hud"><div class="hd"><span class="num">1</span><span class="ht" id="h1"></span></div>
  <div class="inst"><svg id="g1" viewBox="0 0 270 270"></svg><div class="ctr"><div class="big" id="v1"></div><span class="pill" id="lv"></span></div></div>
  <div class="sub" id="s1"></div></div>
 <div class="card hud"><div class="hd"><span class="num">2</span><span class="ht" id="h2"></span></div>
  <div class="inst"><svg id="g2" viewBox="0 0 270 270"></svg><div class="ctr"><div class="pi" id="pi"></div><div class="pn" id="pn"></div><div class="ph" id="ph"></div></div></div>
  <div class="chips" id="chips"></div>
  <div class="sub" id="s2"></div></div>
 <div class="card hud"><div class="hd"><span class="num">3</span><span class="ht" id="h3"></span></div>
  <div class="inst"><svg id="g3" viewBox="0 0 270 270"></svg><div class="ctr"><div class="big" id="v3"></div><div class="unit" id="u3"></div></div></div>
  <div class="sub" id="s3"></div></div>
</div>
<script>
const C=__CFG__,X=C.txt;const $=id=>document.getElementById(id);const NS='http://www.w3.org/2000/svg';
function el(t,a,p){const e=document.createElementNS(NS,t);for(const x in a)e.setAttribute(x,a[x]);if(p)p.appendChild(e);return e;}
['h1','h2','h3','s1','s2','s3'].forEach(k=>$(k).innerHTML=X[k]);
const c=135, START=-120, SWEEP=240;                       // 240-degree instrument arcs, open at the bottom
const P=(a,r)=>[c+r*Math.sin(a*Math.PI/180), c-r*Math.cos(a*Math.PI/180)];
function arc(r,a0,a1){const[x0,y0]=P(a0,r),[x1,y1]=P(a1,r);return `M${x0} ${y0} A${r} ${r} 0 ${a1-a0>180?1:0} 1 ${x1} ${y1}`;}
function defs(svg,id,stops){const d=el('defs',{},svg);const g=el('linearGradient',{id,x1:0,y1:1,x2:1,y2:0},d);
 stops.forEach(([o,col])=>el('stop',{offset:o,'stop-color':col},g));
 const f=el('filter',{id:id+'f',x:'-50%',y:'-50%',width:'200%',height:'200%'},d);el('feGaussianBlur',{stdDeviation:6},f);}
function ticks(svg,n,labels){for(let i=0;i<=n;i++){const a=START+SWEEP*i/n,big=i%(n/ (labels.length-1))===0;
  const[x0,y0]=P(a,120),[x1,y1]=P(a,big?132:127);el('line',{x1:x0,y1:y0,x2:x1,y2:y1,stroke:big?'#6B6E7B':'#3A3C47','stroke-width':big?2:1},svg);}
 labels.forEach((t,i)=>{const a=START+SWEEP*i/(labels.length-1),[x,y]=P(a,146);const tx=el('text',{x,y:y+4,'text-anchor':'middle',fill:'#777984','font-size':10.5},svg);tx.textContent=t;});}
function track(svg){el('path',{d:arc(104,START,START+SWEEP),fill:'none',stroke:'#24262F','stroke-width':18,'stroke-linecap':'round'},svg);}
function value(svg,frac,grad,delay){const d=arc(104,START,START+SWEEP),len=2*Math.PI*104*SWEEP/360;
 const glow=el('path',{d,fill:'none',stroke:`url(#${grad})`,'stroke-width':18,'stroke-linecap':'round',filter:`url(#${grad}f)`,opacity:.55,class:'fill','stroke-dasharray':len,'stroke-dashoffset':len},svg);
 const p=el('path',{d,fill:'none',stroke:`url(#${grad})`,'stroke-width':12,'stroke-linecap':'round',class:'fill','stroke-dasharray':len,'stroke-dashoffset':len},svg);
 setTimeout(()=>{[glow,p].forEach(e=>e.setAttribute('stroke-dashoffset',len*(1-Math.max(.005,Math.min(1,frac)))));},delay);
 const tip=el('circle',{r:7,fill:'#fff',style:'filter:drop-shadow(0 0 8px #FF2D55)',cx:P(START,104)[0],cy:P(START,104)[1]},svg);
 const t0=performance.now()+delay;(function f(t){const k=Math.min(1,Math.max(0,(t-t0)/1600)),e=1-Math.pow(1-k,3),[x,y]=P(START+SWEEP*frac*e,104);
  tip.setAttribute('cx',x);tip.setAttribute('cy',y);if(k<1)requestAnimationFrame(f);})(t0);}
function count(node,to,dec,suffix,delay){const t0=performance.now()+delay;(function f(t){const k=Math.min(1,Math.max(0,(t-t0)/1600));
 node.innerHTML=(to*(1-Math.pow(1-k,3))).toFixed(dec)+suffix;if(k<1)requestAnimationFrame(f);})(t0);}
// ---- 1. risk
(function(){const g=$('g1');defs(g,'gr',[[0,'#40C057'],[.5,'#FFC233'],[1,'#FF2D55']]);ticks(g,20,['0','25','50','75','100']);track(g);
 [[C.th_med,'#FFC233'],[C.th_high,'#FF2D55']].forEach(([v,col])=>{const a=START+SWEEP*v,[x0,y0]=P(a,92),[x1,y1]=P(a,116);el('line',{x1:x0,y1:y0,x2:x1,y2:y1,stroke:col,'stroke-width':3},g);});
 value(g,C.p,'gr',250);count($('v1'),C.p*100,0,'<small>%</small>',250);
 const LC={High:'#FF2D55',Medium:'#FFC233',Low:'#51CF66'};$('lv').textContent=C.level_txt;$('lv').style.background=LC[C.level]+'26';$('lv').style.color=LC[C.level];})();
// ---- 2. time of day: 24h dial (full circle), four period arcs, hand on the chosen period
(function(){const g=$('g2');const ang=h=>h/24*360;
 for(let h=0;h<24;h++){const[x0,y0]=P(ang(h),121),[x1,y1]=P(ang(h),h%6===0?133:127);el('line',{x1:x0,y1:y0,x2:x1,y2:y1,stroke:h%6===0?'#6B6E7B':'#3A3C47','stroke-width':h%6===0?2:1},g);}
 [0,6,12,18].forEach(h=>{const[x,y]=P(ang(h),146);const t=el('text',{x,y:y+4,'text-anchor':'middle',fill:'#777984','font-size':10.5},g);t.textContent=String(h).padStart(2,'0');});
 const mx=Math.max(...C.periods.map(p=>p.m));
 C.periods.forEach((p,i)=>{const a0=i*90+3,a1=i*90+87;
  el('path',{d:arc(104,a0,a1),fill:'none',stroke:'#24262F','stroke-width':18},g);
  const s=el('path',{d:arc(104,a0,a1),fill:'none',stroke:p.c,'stroke-width':p.hot?18:12,opacity:0,style:'transition:opacity .8s'},g);
  setTimeout(()=>s.setAttribute('opacity',(p.hot?1:.25+.55*p.m/mx).toFixed(2)),300+i*120);
  if(p.hot)el('path',{d:arc(104,a0,a1),fill:'none',stroke:p.c,'stroke-width':18,opacity:.5,style:'filter:blur(7px)'},g);
  if(p.hist)el('path',{d:arc(84,a0,a1),fill:'none',stroke:'#E3E4E8','stroke-width':2,'stroke-dasharray':'5 5',opacity:.8},g);
  const am=(a0+a1)/2,[tx,ty]=P(am,104);const pt=el('text',{x:tx,y:ty+4.5,'text-anchor':'middle',fill:'#fff','font-size':12,'font-weight':800,
   style:'paint-order:stroke;stroke:rgba(0,0,0,.55);stroke-width:3px'},g);pt.textContent=Math.round(p.m*100)+'%';});
 const hand=el('g',{class:'hand',style:`transform-origin:${c}px ${c}px;transform:rotate(0deg)`},g);
 el('path',{d:`M${c-7} ${c-66} L${c} ${c-90} L${c+7} ${c-66} Z`,fill:'#FF2D55',style:'filter:drop-shadow(0 0 8px #FF2D55)'},hand);
 setTimeout(()=>hand.style.transform=`rotate(${C.hand_h/24*360}deg)`,450);
 $('pi').textContent=C.verdict.icon;$('pn').textContent=C.verdict.name;$('ph').textContent=C.verdict.hours;
 $('chips').innerHTML=C.periods.map(p=>`<span class="${p.hot?'hot':''} ${p.hist?'hist':''}">${p.icon} <b>${Math.round(p.m*100)}%</b></span>`).join('');})();
// ---- 3. clear time: same arc style, scale 0..max
(function(){const g=$('g3');defs(g,'gc',[[0,'#FFC233'],[1,'#FF2D55']]);const scale=C.scale;
 ticks(g,scale/5*2,[0,scale/4,scale/2,scale*3/4,scale].map(v=>v+"'"));track(g);
 const f=m=>START+SWEEP*Math.min(1,m/scale);el('path',{d:arc(104,f(C.q25),f(C.q75)),fill:'none',stroke:'rgba(255,45,85,.25)','stroke-width':26},g);
 value(g,C.clear/scale,'gc',350);count($('v3'),C.clear,C.clear%1?1:0,'',350);$('u3').textContent=X.u3;})();
</script>"""
