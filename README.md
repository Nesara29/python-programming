<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>PyVerse 3D – Python Snake Algorithm Animation</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#050a14;--blue:#3776ab;--blue2:#5fa8e8;--yellow:#ffd43b;--ink:#e8f1ff;--dim:#8aa4c4;--panel:rgba(8,18,34,.74);--line:rgba(95,168,232,.3);
box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
html,body{height:100%;margin:0;background:var(--bg);color:var(--ink);font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;overflow:hidden}
canvas{position:fixed;inset:0;width:100%;height:100%;display:block;touch-action:none}
.hud{position:fixed;left:0;right:0;padding-left:16px;padding-right:16px;pointer-events:none}
#top{top:0;padding-top:calc(env(safe-area-inset-top,0px) + 14px);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
#bot{bottom:0;padding-bottom:calc(env(safe-area-inset-bottom,0px) + 14px)}
h1{margin:0;font-size:clamp(24px,4.4vw,44px);letter-spacing:.06em;line-height:1}
h1 b{background:linear-gradient(90deg,var(--blue2),var(--yellow));-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{margin:6px 0 0;font-size:12px;color:var(--dim);max-width:380px}
nav{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start;pointer-events:auto}
nav button{font:inherit;font-size:12px;color:var(--dim);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:8px 13px;cursor:pointer;backdrop-filter:blur(8px)}
nav button.on{color:#05101f;font-weight:700;border-color:transparent;background:linear-gradient(90deg,var(--blue2),var(--yellow))}
.card{max-width:540px;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;backdrop-filter:blur(10px)}
.bar{display:flex;align-items:center;gap:6px;padding:8px 12px;border-bottom:1px solid var(--line);font-size:11px;color:var(--dim)}
.bar i{width:9px;height:9px;border-radius:50%;background:var(--blue2)}.bar i:nth-child(2){background:var(--yellow)}.bar i:nth-child(3){background:var(--blue)}
.bar em{margin-left:auto;font-style:normal;color:var(--yellow)}
pre{margin:0;padding:10px 14px;font:inherit;font-size:12px;line-height:1.55;white-space:pre-wrap;overflow-x:auto}
#log{border-top:1px dashed var(--line);color:var(--blue2);min-height:4.6em;font-size:11.5px}
.c{color:#5d7a99;font-style:italic}.s{color:var(--yellow);font-style:normal}.k{color:var(--blue2);font-weight:700;font-style:normal}.n{color:#ff9f5a;font-style:normal}
#err{position:fixed;inset:0;display:grid;place-items:center;color:var(--yellow)}
@media(max-width:700px){#top{flex-direction:column}nav{flex-wrap:nowrap;overflow-x:auto;max-width:100%;padding-bottom:4px}nav button{white-space:nowrap}pre{font-size:11px;padding:8px 12px}.sub{display:none}}
</style>
</head>
<body>
<div id="top" class="hud">
  <div><h1>PY<b>VERSE</b> 3D</h1><p class="sub">Python snake · live 3D animations of the algorithms in your <b>python-programming</b> repo</p></div>
  <nav id="nav"></nav>
</div>
<div id="bot" class="hud">
  <div class="card"><div class="bar"><i></i><i></i><i></i><span id="file"></span><em id="cx"></em></div><pre id="code"></pre><pre id="log"></pre></div>
</div>
<div id="err"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const R=Math.random,$=id=>document.getElementById(id),RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const BLUE=0x3776ab,BLUE2=0x5fa8e8,YEL=0xffd43b,ORG=0xff8a3d;
let renderer;try{renderer=new THREE.WebGLRenderer({antialias:true})}catch(e){$('err').textContent='WebGL is not available in this browser.';throw e}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));document.body.prepend(renderer.domElement);

/* ---------- stations: snippets come from the uploaded repo ---------- */
const ST=[
{n:'Python Snake',x:0,cx:'list.append → O(1)',f:'datastructures.py',code:'numbers=[10,20,30,40]\nnumbers.append(50)\nprint(numbers)'},
{n:'Bubble Sort',x:32,cx:'O(n²) time · O(1) space',f:'bubblesort.py',code:'for i in range(n-1):\n    for j in range(n-i-1):\n        if arr[j]>arr[j+1]:\n            arr[j],arr[j+1]=arr[j+1],arr[j]'},
{n:'Tower of Hanoi',x:64,cx:'O(2ⁿ) moves',f:'towerofhonoi.py',code:'hanoi(n-1,A,C,B,s,d,a)\ndisk=A.pop()\nC.append(disk)\nhanoi(n-1,B,A,C,a,s,d)'},
{n:'Breadth First Search',x:96,cx:'O(V+E) · queue',f:'breathfirstsearch.py',code:'node=queue.pop(0)\nprint(node,end="->")\nfor n in graph[node]:\n    if n not in visited:\n        queue.append(n)'}];

/* ---------- scene ---------- */
const scene=new THREE.Scene();scene.background=new THREE.Color(0x050a14);scene.fog=new THREE.FogExp2(0x050a14,.015);
const cam=new THREE.PerspectiveCamera(55,1,.1,500);
scene.add(new THREE.AmbientLight(0x6f8fbf,.85));
const L1=new THREE.PointLight(BLUE2,2.4,70),L2=new THREE.PointLight(YEL,2.2,70);scene.add(L1,L2);
const dl=new THREE.DirectionalLight(0xffffff,.55);dl.position.set(5,12,8);scene.add(dl);
const mkMat=(c,e=.4)=>new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:e,metalness:.4,roughness:.4});
function glowTex(){const c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d'),r=g.createRadialGradient(32,32,0,32,32,32);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.3,'rgba(255,255,255,.5)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)}
const GLOW=glowTex();
function tag(t,col='#ffd43b',fs=34,op=1){const c=document.createElement('canvas'),g=c.getContext('2d');g.font=`700 ${fs}px monospace`;const w=Math.ceil(g.measureText(t).width)+24;c.width=w;c.height=fs+20;g.font=`700 ${fs}px monospace`;g.textBaseline='middle';g.fillStyle=col;g.shadowColor=col;g.shadowBlur=12;g.fillText(t,12,c.height/2);const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),transparent:true,opacity:op,depthWrite:false}));sp.scale.set(w/40,c.height/40,1);return sp}

/* grid floor, stars, platforms */
const grid=new THREE.GridHelper(300,150,BLUE,0x14304f);grid.position.set(48,0,0);grid.material.transparent=true;grid.material.opacity=.45;scene.add(grid);
{const n=900,a=new Float32Array(n*3);for(let i=0;i<n;i++){const r=140+R()*120,th=R()*6.283,ph=Math.acos(R()*.9);a.set([48+r*Math.sin(ph)*Math.cos(th),r*Math.cos(ph)*.7+10,r*Math.sin(ph)*Math.sin(th)-40],i*3)}
const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(a,3));scene.add(new THREE.Points(g,new THREE.PointsMaterial({color:0xbcd6ff,size:1.4,sizeAttenuation:false,fog:false})))}
const rings=[];
ST.forEach((s,i)=>{
  const p=new THREE.Mesh(new THREE.CylinderGeometry(8,8.4,.4,6),new THREE.MeshStandardMaterial({color:0x0e2442,metalness:.6,roughness:.3,emissive:BLUE,emissiveIntensity:.15}));p.position.set(s.x,.2,0);scene.add(p);
  const r=new THREE.Mesh(new THREE.TorusGeometry(8.7,.07,8,6),new THREE.MeshBasicMaterial({color:YEL}));r.rotation.x=Math.PI/2;r.rotation.z=Math.PI/6;r.position.set(s.x,.45,0);scene.add(r);
  const pl=new THREE.Mesh(new THREE.RingGeometry(8,8.2,64),new THREE.MeshBasicMaterial({color:BLUE2,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide}));pl.rotation.x=-Math.PI/2;pl.position.set(s.x,.5,0);scene.add(pl);
  const b=new THREE.Mesh(new THREE.CylinderGeometry(8,8,24,6,1,true),new THREE.MeshBasicMaterial({color:BLUE,transparent:true,opacity:.05,side:THREE.DoubleSide,blending:THREE.AdditiveBlending,depthWrite:false}));b.position.set(s.x,12,0);scene.add(b);
  rings.push({r,pl,i});
});

/* floating Python tokens */
const toks=[];
['def','class','self','import','for','while','return','push()','pop()','enqueue()','pivot','hanoi()','dfs()','bfs()','swap','arr[j]','queue','stack','graph','visited','None','True','range()','print()','O(n log n)','lambda','__init__','len()'].forEach((w,i)=>{
  const s=tag(w,['#ffd43b','#5fa8e8','#ffffff'][i%3],34,.8);s.position.set(-14+R()*125,2+R()*12,-6-R()*14);s.userData={y:s.position.y,p:R()*6,sp:.4+R()};scene.add(s);toks.push(s)});

/* particles (trail + sparks) */
const PN=700,pp=new Float32Array(PN*3).fill(-999),pc=new Float32Array(PN*3),pb=new Float32Array(PN*3),pv=new Float32Array(PN*3),pl=new Float32Array(PN);let pk=0;
const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pp,3));pg.setAttribute('color',new THREE.BufferAttribute(pc,3));
const pts=new THREE.Points(pg,new THREE.PointsMaterial({size:.55,map:GLOW,vertexColors:true,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));pts.frustumCulled=false;scene.add(pts);
const cB=new THREE.Color(BLUE2),cY=new THREE.Color(YEL);
function emit(p,c,sp=1){const i=pk++%PN;pp.set([p.x,p.y,p.z],i*3);pv.set([(R()-.5)*1.4*sp,R()*.9*sp,(R()-.5)*1.4*sp],i*3);pl[i]=1;c.toArray(pb,i*3)}

/* ---------- THE PYTHON SNAKE (instanced body + animated head) ---------- */
const N=72,DT=.072,cen=new THREE.Vector3();
const sph=new THREE.SphereGeometry(1,20,14);
const body=new THREE.InstancedMesh(sph,new THREE.MeshStandardMaterial({metalness:.35,roughness:.3,emissive:0x0a1a33,emissiveIntensity:.7}),N);
for(let i=0;i<N;i++){const t=i/N,c=new THREE.Color(t<.55?BLUE:YEL);if(i%6<2)c.multiplyScalar(t<.55?1.6:.7);body.setColorAt(i,c)}
body.frustumCulled=false;scene.add(body);
const head=new THREE.Group(),hmesh=new THREE.Mesh(sph,new THREE.MeshStandardMaterial({color:0x2f6aa5,metalness:.35,roughness:.3,emissive:0x0a1a33,emissiveIntensity:.8}));hmesh.scale.set(.66,.52,.95);head.add(hmesh);
for(const s of[-1,1]){const e=new THREE.Mesh(new THREE.SphereGeometry(.14,12,10),new THREE.MeshBasicMaterial({color:YEL}));e.position.set(s*.32,.2,.55);head.add(e);
  const pu=new THREE.Mesh(new THREE.SphereGeometry(.07,10,8),new THREE.MeshBasicMaterial({color:0}));pu.position.set(s*.32,.2,.67);head.add(pu);
  const gl=new THREE.Sprite(new THREE.SpriteMaterial({map:GLOW,color:YEL,blending:THREE.AdditiveBlending,transparent:true,depthWrite:false}));gl.scale.setScalar(.9);gl.position.set(s*.32,.2,.6);head.add(gl)}
const tongue=new THREE.Group();tongue.position.set(0,-.08,.88);
for(const s of[-1,1]){const f=new THREE.Mesh(new THREE.BoxGeometry(.05,.03,.6),new THREE.MeshBasicMaterial({color:0xff4d6d}));f.position.set(s*.1,0,.3);f.rotation.y=s*-.28;tongue.add(f)}
head.add(tongue);scene.add(head);
function P(t,o){const s=.55*t;return o.set(cen.x+Math.cos(s)*9+Math.cos(s*2.3)*1.5+Math.sin(t*5)*.12,3.4+Math.sin(s*1.7)*1.7+Math.sin(t*4)*.18,Math.sin(s)*5.6+Math.sin(s*3.1)*1.2+Math.sin(t*5)*.3)}
const bp=[],dum=new THREE.Object3D(),tmp=new THREE.Vector3();for(let i=0;i<N;i++)bp.push(new THREE.Vector3());
function snake(T){
  for(let i=0;i<N;i++){P(T-i*DT-.07,bp[i]);const r=.64*(1-.82*Math.pow(i/N,1.7))+.05;dum.position.copy(bp[i]);dum.scale.setScalar(r*(i%6<2?1.1:1));dum.updateMatrix();body.setMatrixAt(i,dum.matrix)}
  body.instanceMatrix.needsUpdate=true;
  P(T,head.position);P(T+.12,tmp);head.lookAt(tmp);
  const f=Math.max(0,Math.sin(T*3.2));tongue.scale.z=.15+1.3*Math.pow(f,6);
  emit(head.position,cB,.6);emit(head.position,cB,.6);const i=Math.floor(R()*N);emit(bp[i],i/N<.55?cB:cY,.8);
}

/* ---------- STATION 1 · bubble sort (arr from bubblesort.py) ---------- */
const V=[76,54,24,14,9],bars=[],slot=i=>ST[1].x+(i-2)*2.5;
V.forEach((v,i)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(1.8,1,1.8),mkMat(BLUE,.5));m.scale.y=v/10;m.position.set(slot(i),.4+v/20,0);m.userData={v,tx:slot(i),zt:0,fx:0};
  const l=tag(String(v),'#ffffff',38);l.position.set(slot(i),.4+v/10+.9,0);m.userData.lab=l;scene.add(m,l);bars.push(m)});
const setC=(m,c,e)=>{m.material.color.setHex(c);m.material.emissive.setHex(c);m.material.emissiveIntensity=e};
function sortSteps(){const a=V.slice(),id=V.map((_,i)=>i),n=a.length,s=[];for(let i=0;i<n-1;i++){for(let j=0;j<n-i-1;j++){s.push({t:'c',a:id[j],b:id[j+1]});if(a[j]>a[j+1]){s.push({t:'s',a:id[j],b:id[j+1]});[a[j],a[j+1]]=[a[j+1],a[j]];[id[j],id[j+1]]=[id[j+1],id[j]]}}s.push({t:'f',a:id[n-i-1]})}s.push({t:'f',a:id[0]},{t:'d'});return s}
const SS=sortSteps();let sk=0,sw=1;
function updSort(dt){
  sw-=dt;
  if(sw<=0){const s=SS[sk++];bars.forEach(b=>{if(!b.userData.fx)setC(b,BLUE,.5);b.userData.zt=0});
    if(!s){sk=0;sw=1;bars.forEach((b,i)=>{const u=b.userData;u.fx=0;u.tx=slot(i);b.position.x=u.tx;setC(b,BLUE,.5)});log(1,'--- restart [76, 54, 24, 14, 9] ---')}
    else if(s.t=='c'){setC(bars[s.a],YEL,1.3);setC(bars[s.b],YEL,1.3);sw=.5;log(1,`compare ${bars[s.a].userData.v} > ${bars[s.b].userData.v} ?`)}
    else if(s.t=='s'){const A=bars[s.a].userData,B=bars[s.b].userData;[A.tx,B.tx]=[B.tx,A.tx];A.zt=1.9;B.zt=-1.9;setC(bars[s.a],ORG,1.4);setC(bars[s.b],ORG,1.4);sw=.95;log(1,`swapping ${A.v} with ${B.v}`);for(let k=0;k<14;k++){emit(bars[s.a].position,cY);emit(bars[s.b].position,cB)}}
    else if(s.t=='f'){bars[s.a].userData.fx=1;setC(bars[s.a],YEL,.95);sw=.3}
    else{sw=3;log(1,'sorted array [9, 14, 24, 54, 76]')}}
  bars.forEach(b=>{const u=b.userData,k=Math.min(1,dt*7);b.position.x+=(u.tx-b.position.x)*k;b.position.z+=(u.zt-b.position.z)*k;u.lab.position.x=b.position.x;u.lab.position.z=b.position.z+.2});
}

/* ---------- STATION 2 · Tower of Hanoi, n=3 (towerofhonoi.py) ---------- */
const pegX=k=>ST[2].x+(k-1)*5.4,dY=l=>1.05+l*.66,disks=[null];
for(let k=0;k<3;k++){const p=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,6,12),mkMat(0xaac4e6,.3));p.position.set(pegX(k),3.4,0);scene.add(p);
  const t=tag('ABC'[k],'#5fa8e8',40);t.position.set(pegX(k),7.2,0);scene.add(t)}
for(let d=1;d<=3;d++){const r=.8+d*.45,m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,.6,40),mkMat([0,YEL,BLUE2,BLUE][d],.55));scene.add(m);disks.push(m)}
let HM,hs,hm,hu,hw=1,h0,h1;
function hInit(){HM=[];(function h(n,a,b,c){if(!n)return;h(n-1,a,c,b);HM.push([n,a,c]);h(n-1,b,a,c)})(3,0,1,2);hs=[[3,2,1],[],[]];hs.forEach((s,k)=>s.forEach((d,l)=>disks[d].position.set(pegX(k),dY(l),0)));hm=0;hu=-1}hInit();
const ez=x=>x*x*(3-2*x),lr=(a,b,t)=>a+(b-a)*t;
function updHanoi(dt){
  if(hw>0){hw-=dt;return}
  const m=HM[hm];if(!m){hInit();hw=.8;log(2,'--- reset  A:[3, 2, 1] | B:[] | C:[] ---');return}
  const d=disks[m[0]];
  if(hu<0){hu=0;h0=d.position.clone();h1=new THREE.Vector3(pegX(m[2]),dY(hs[m[2]].length),0);log(2,`move disk ${m[0]} from ${'ABC'[m[1]]} to ${'ABC'[m[2]]}`)}
  hu+=dt/1.5;const u=Math.min(hu,1);
  if(u<.3){d.position.set(h0.x,lr(h0.y,7.4,ez(u/.3)),0)}else if(u<.7){d.position.set(lr(h0.x,h1.x,ez((u-.3)/.4)),7.4,0)}else{d.position.set(h1.x,lr(7.4,h1.y,ez((u-.7)/.3)),0)}
  if(u>.05&&u<.95)emit(d.position,cY,.5);
  if(hu>=1){hs[m[2]].push(hs[m[1]].pop());hm++;hu=-1;hw=.2;if(hm==HM.length){hw=3;log(2,'A:[] | B:[] | C:[3, 2, 1]')}}
}

/* ---------- STATION 3 · BFS on the repo's graph (breathfirstsearch.py) ---------- */
const BX=ST[3].x,BN={50:[0,8.2],30:[-4.2,5.4],70:[4.2,5.4],20:[-6.3,2.6],40:[-2.1,2.6],60:[2.1,2.6],80:[6.3,2.6]},G={50:[30,70],30:[20,40],70:[60,80],20:[],40:[],60:[],80:[]};
const nodes={},edges={};
const np=k=>new THREE.Vector3(BX+BN[k][0],BN[k][1]+.7,0);
for(const k in G)G[k].forEach(c=>{const a=np(k),b=np(c),len=a.distanceTo(b),e=new THREE.Mesh(new THREE.CylinderGeometry(.07,.07,len,8),mkMat(BLUE2,.35));e.position.copy(a).add(b).multiplyScalar(.5);e.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),b.clone().sub(a).normalize());scene.add(e);edges[k+'-'+c]=e});
for(const k in BN){const m=new THREE.Mesh(new THREE.SphereGeometry(.85,24,16),mkMat(BLUE,.45));m.position.copy(np(k));scene.add(m);const l=tag(k,'#ffffff',40);l.position.set(m.position.x,m.position.y,.95);scene.add(l);nodes[k]=m}
const BS=[];{const q=[50],vis=[50],out=[];while(q.length){const n=q.shift();out.push(n);const kids=[];G[n].forEach(c=>{if(!vis.includes(c)){vis.push(c);q.push(c);kids.push(c)}});BS.push({n,kids,q:q.slice(),o:out.join('->')+'->'})}}
let bi=0,bw=1,cur3=null;
function bReset(){for(const k in nodes)setC(nodes[k],BLUE,.45);for(const k in edges)setC(edges[k],BLUE2,.35);cur3=null}
function updBfs(dt){
  bw-=dt;
  if(bw<=0){const s=BS[bi++];
    if(!s){bi=0;bw=1;bReset();log(3,'--- reset  visited=[] queue=[] ---')}
    else{cur3=nodes[s.n];setC(cur3,YEL,1.4);s.kids.forEach(c=>{setC(nodes[c],BLUE2,1);setC(edges[s.n+'-'+c],YEL,1.1)});bw=1.15;log(3,`print: ${s.o}`);log(3,`queue=[${s.q.join(', ')}]`);for(let k=0;k<22;k++)emit(cur3.position,cY,1.2);if(bi==BS.length)bw=3.2}}
  for(const k in nodes)nodes[k].scale.setScalar(nodes[k]===cur3?1.12+.1*Math.sin(clock*7):1);
}

/* ---------- snake station live list log ---------- */
let arr=[10,20,30,40],lw=1.2;
function updList(dt){lw-=dt;if(lw<=0){lw=1.5;arr.length>7?(arr=[10,20,30,40],log(0,'--- numbers=[10, 20, 30, 40] ---')):(arr.push(arr.length*10+10),log(0,`numbers.append(${arr[arr.length-1]}) → [${arr.join(', ')}]`))}}

/* ---------- UI ---------- */
const logs=ST.map(()=>[]);let cur=0,tgtX=0,camX=0,auto=true,lastSw=0,clock=0;
function log(i,t){const a=logs[i];a.push('>>> '+t);if(a.length>4)a.shift();if(i===cur)$('log').textContent=a.join('\n')}
const hl=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/(#.*$)|("[^"]*"|'[^']*')|\b(def|class|for|if|while|return|import|in|not)\b|\b(\d+)\b/gm,(m,c,q,k)=>`<i class="${c?'c':q?'s':k?'k':'n'}">${m}</i>`);
function ui(){[...$('nav').children].forEach((b,i)=>b.classList.toggle('on',i===cur&&b.dataset.k!='auto'));$('file').textContent=ST[cur].f;$('cx').textContent=ST[cur].cx;$('code').innerHTML=hl(ST[cur].code);$('log').textContent=logs[cur].join('\n')}
function go(i){cur=(i+ST.length)%ST.length;tgtX=ST[cur].x;lastSw=clock;ui()}
ST.forEach((s,i)=>{const b=document.createElement('button');b.textContent=(i+1)+' · '+s.n;b.onclick=()=>go(i);$('nav').appendChild(b)});
{const b=document.createElement('button');b.dataset.k='auto';b.textContent='AUTO TOUR: ON';b.onclick=()=>{auto=!auto;lastSw=clock;b.textContent='AUTO TOUR: '+(auto?'ON':'OFF')};$('nav').appendChild(b)}
addEventListener('keydown',e=>{if(e.key=='ArrowRight')go(cur+1);if(e.key=='ArrowLeft')go(cur-1)});
let mx=0,my=0;addEventListener('pointermove',e=>{mx=e.clientX/innerWidth*2-1;my=e.clientY/innerHeight*2-1});
let dist=17;function rs(){renderer.setSize(innerWidth,innerHeight);cam.aspect=innerWidth/innerHeight;dist=cam.aspect<.8?28:cam.aspect<1.2?22:17;cam.updateProjectionMatrix()}addEventListener('resize',rs);rs();ui();

/* ---------- main loop ---------- */
const clk=new THREE.Clock();
function tick(){
  requestAnimationFrame(tick);
  const dt=Math.min(clk.getDelta(),.05)*(RM?.35:1);clock+=dt;
  if(auto&&clock-lastSw>13)go(cur+1);
  camX+=(tgtX-camX)*(1-Math.exp(-dt*2.2));const gap=tgtX-camX;
  cam.fov+=(55+Math.min(Math.abs(gap)*.55,24)-cam.fov)*.1;cam.updateProjectionMatrix();
  cam.position.set(camX+mx*3+Math.sin(clock*.2)*1.5,5.2-my*1.4,dist);cam.lookAt(camX,3.6,0);cam.rotateZ(Math.max(-.14,Math.min(.14,gap*.006)));
  cen.x=camX+gap*.35;L1.position.set(camX-9,9,9);L2.position.set(camX+9,5,7);
  snake(clock*1.05);updSort(dt);updHanoi(dt);updBfs(dt);updList(dt);
  rings.forEach(({r,pl,i})=>{const s=(clock*.45+i*.3)%1;pl.scale.setScalar(1+s*.9);pl.material.opacity=(1-s)*.55;r.material.color.setHex(i===cur?YEL:BLUE2)});
  toks.forEach(s=>{const u=s.userData;s.position.y=u.y+Math.sin(clock*u.sp+u.p)*.8;s.position.x+=dt*.25*u.sp});
  for(let i=0;i<PN;i++){if(pl[i]>0){pl[i]-=dt*.85;const k=i*3,f=Math.max(pl[i],0);pp[k]+=pv[k]*dt;pp[k+1]+=pv[k+1]*dt;pp[k+2]+=pv[k+2]*dt;pc[k]=pb[k]*f;pc[k+1]=pb[k+1]*f;pc[k+2]=pb[k+2]*f}}
  pg.attributes.position.needsUpdate=pg.attributes.color.needsUpdate=true;
  renderer.render(scene,cam);
}
tick();
</script>
</body>
</html>
