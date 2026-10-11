<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>PyVerse 3D – Python Snake Algorithm Animation</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#050a14;--blue:#3776ab;--blue2:#5fa8e8;--yellow:#ffd43b;--ink:#e8f1ff;--dim:#8aa4c4;--panel:rgba(8,18,34,.82);--line:rgba(95,168,232,.3);
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
nav{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end;align-items:flex-start;pointer-events:auto;max-width:66%}
nav button{font:inherit;font-size:11px;color:var(--dim);background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:6px 10px;cursor:pointer}
nav button.on{color:#05101f;font-weight:700;border-color:transparent;background:linear-gradient(90deg,var(--blue2),var(--yellow))}
.card{max-width:560px;background:#ffffff;border:2px solid #3776ab;border-radius:14px;overflow:hidden}
.bar{display:flex;align-items:center;gap:6px;padding:8px 12px;border-bottom:1px solid var(--line);font-size:11px;color:#000;font-weight:700;background:#eaf2fb}
.bar i{width:9px;height:9px;border-radius:50%;background:var(--blue2)}.bar i:nth-child(2){background:var(--yellow)}.bar i:nth-child(3){background:var(--blue)}
.bar em{margin-left:auto;font-style:normal;color:#7a4b00}
.card pre{margin:0;padding:10px 14px;font:inherit;font-size:12px;line-height:1.55;white-space:pre-wrap;overflow-x:auto;background:#ffffff;color:#000}
#log{border-top:1px dashed #3776ab;color:#000;min-height:4.6em;font-size:11.5px;background:#f1f6fc}#why{background:#fff4c2;color:#000;font-weight:700;border-top:1px solid #e0c13a}
.c{color:#46607c;font-style:italic}.s{color:#7a5200;font-style:normal}.k{color:#0b4f9c;font-weight:700;font-style:normal}.n{color:#a33d00;font-style:normal}
#err{position:fixed;inset:0;display:grid;place-items:center;color:var(--yellow)}
@media(max-width:700px){#top{flex-direction:column}nav{flex-wrap:nowrap;overflow-x:auto;max-width:100%;padding-bottom:4px;justify-content:flex-start}nav button{white-space:nowrap}.card pre{font-size:11px;padding:8px 12px}.sub{display:none}}
</style>
</head>
<body>
<div id="top" class="hud">
  <div><h1>PY<b>VERSE</b> 3D</h1><p class="sub">Python snake · live 3D animations of all 16 programs in your <b>python-programming</b> repo</p></div>
  <nav id="nav"></nav>
</div>
<div id="bot" class="hud">
  <div class="card"><div class="bar"><i></i><i></i><i></i><span id="file"></span><em id="cx"></em></div><pre id="code"></pre><pre id="why"></pre><pre id="log"></pre></div>
</div>
<div id="err"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const R=Math.random,$=id=>document.getElementById(id),RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const BLUE=0x3776ab,BLUE2=0x5fa8e8,YEL=0xffd43b,ORG=0xff8a3d,GRN=0x3ee59a;
let renderer;try{renderer=new THREE.WebGLRenderer({antialias:true})}catch(e){$('err').textContent='WebGL is not available in this browser.';throw e}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));document.body.prepend(renderer.domElement);

/* ---------- graph data (from breathfirstsearch.py / depthfirstsearch.py) ---------- */
const BN={50:[0,8.2],30:[-4.2,5.4],70:[4.2,5.4],20:[-6.3,2.6],40:[-2.1,2.6],60:[2.1,2.6],80:[6.3,2.6]},G={50:[30,70],30:[20,40],70:[60,80],20:[],40:[],60:[],80:[]};
const BS=[],DS=[];
{const q=[50],vis=[50],out=[];while(q.length){const n=q.shift();out.push(n);const kids=[];G[n].forEach(c=>{if(!vis.includes(c)){vis.push(c);q.push(c);kids.push(c)}});BS.push({n,ed:kids.map(c=>n+'-'+c),qd:kids,logs:['print: '+out.join('->')+'->','queue=['+q.join(', ')+']']})}}
{const vis=[],out=[];(function d(n,p){if(vis.includes(n))return;out.push(n);vis.push(n);DS.push({n,ed:p?[p+'-'+n]:[],qd:[],logs:['print: '+out.join('->')+'->']});G[n].forEach(c=>d(c,n))})(50,0)}

/* ---------- the 16 stations: one per .py file in the ZIP ---------- */
const ST=[
{n:'Data Structures',cx:'list · set · dict',f:'datastructures.py',k:'e',gen:()=>ds(),cfg:{lay:'row',w:3.1,g:3.6,fs:26},code:'numbers=[10,20,30,40]\nnumbers.append(50)\nfruits.remove("orange")\nstudent["age"]=17'},
{n:'Student ADT',cx:'class · display · update',f:'studentADT.py',k:'e',gen:()=>stu(90,95),cfg:{lay:'row',w:4.4,g:5,fs:24},code:'class student():\n    def update(self,new_marks):\n        self.marks=new_marks\nstudent.update(95)'},
{n:'ADT Time/Space',cx:'perf_counter · getsizeof',f:'ADTwithtimeandspacecomplexity.py',k:'e',gen:()=>stu(92,97,1),cfg:{lay:'row',w:4.4,g:5,fs:24},code:'start_time=time.perf_counter()\nstudent.update(97)\nend_time=time.perf_counter()\nspace_used=sys.getsizeof(student)'},
{n:'Array',cx:'fixed size MAX=3',f:'arraycomparision.py',k:'e',gen:()=>arrcmp(),cfg:{lay:'row',w:2.8,g:3.4,fs:26},code:'if self.count<MAX:\n    self.student[self.count]={...}\nelse:\n    print("array is full")'},
{n:'Stack',cx:'LIFO · push/pop O(1)',f:'stackimplementation.py',k:'e',gen:()=>stack(),cfg:{lay:'col',w:4,fs:34},code:'def push(self,x):\n    if self.size == self.limit:\n        print("stack overflow")\n    self.stack.append(x)'},
{n:'Queue',cx:'FIFO · enqueue/dequeue',f:'queueimplementation.py',k:'e',gen:()=>queue(),cfg:{lay:'row',w:2.2,g:3,fs:34},code:'def enqueue(self,x):\n    if len(self.queue)==self.limit:\n        print("queue overflow")\n    self.queue.append(x)\n# dequeue → self.queue.pop(0)'},
{n:'Priority Queue',cx:'sort by priority',f:'priorityqueue.py',k:'e',gen:()=>pq(),cfg:{lay:'row',w:2.6,g:3.3,fs:28},code:'queue.append((priority,data))\nqueue.sort()\nitem=queue.pop(0)'},
{n:'Factorial',cx:'recursion · call stack',f:'factorial.py',k:'e',gen:()=>fact(),cfg:{lay:'col',w:4,fs:34},code:'def fact(n):\n    if n==1:\n        return 1\n    return n*fact(n-1)'},
{n:'Linear Search',cx:'O(n) · best/avg/worst',f:'linearseach.py',k:'e',gen:()=>linear(),cfg:{lay:'bars',sc:.12,fs:36},code:'for i in range(len(a)):\n    comparisons += 1\n    if a[i] == key:\n        return i, comparisons'},
{n:'Bubble Sort',cx:'O(n²) time · O(1) space',f:'bubblesort.py',k:'e',gen:()=>bubble([76,54,24,14,9]),cfg:{lay:'bars',sc:.1,hop:1,fs:36},code:'for i in range(n-1):\n    for j in range(n-i-1):\n        if arr[j]>arr[j+1]:\n            arr[j],arr[j+1]=arr[j+1],arr[j]'},
{n:'Selection Sort',cx:'O(n²) · min each pass',f:'selectionsort.py',k:'e',gen:()=>select([65,72,23,14,34]),cfg:{lay:'bars',sc:.1,hop:1,fs:36},code:'for j in range(i+1,len(arr)):\n    if arr[j]<arr[min_index]:\n        min_index=j\narr[i],arr[min_index]=arr[min_index],arr[i]'},
{n:'Insertion Sort',cx:'O(n²) · Sorted | Unsorted',f:'insertionsort.py',k:'e',gen:()=>insert([7,3,5,4,2]),cfg:{lay:'bars',sc:1,hop:1,fs:36},code:'key=arr[i]\nwhile j>=0 and arr[j]>key:\n    arr[j+1]=arr[j]\n    j-=1\narr[j+1]=key'},
{n:'Quick Sort',cx:'O(n log n) avg · pivot',f:'quicksort.py',k:'e',gen:()=>quick([33,24,46,42,14,20]),cfg:{lay:'bars',sc:.15,hop:1,fs:36},code:'pivot=arr[-1]\nleft=[x for x in arr[:-1] if x<pivot]\nright=[x for x in arr[:-1] if x>pivot]\nreturn quicksort(left)+[pivot]+quicksort(right)'},
{n:'Tower of Hanoi',cx:'O(2ⁿ) moves',f:'towerofhonoi.py',k:'h',code:'hanoi(n-1,A,C,B,s,d,a)\ndisk=A.pop()\nC.append(disk)\nhanoi(n-1,B,A,C,a,s,d)'},
{n:'BFS',cx:'O(V+E) · queue',f:'breathfirstsearch.py',k:'g',st:BS,code:'node=queue.pop(0)\nprint(node,end="->")\nfor n in graph[node]:\n    if n not in visited:\n        queue.append(n)'},
{n:'DFS',cx:'O(V+E) · recursion',f:'depthfirstsearch.py',k:'g',st:DS,code:'def dfs(n):\n    if n not in visited:\n        visited.append(n)\n        for i in graph[n]:\n            dfs(i)'}];
ST.forEach((s,i)=>s.x=i*32);

/* ---------- scene ---------- */
const scene=new THREE.Scene();scene.background=new THREE.Color(0x050a14);scene.fog=new THREE.FogExp2(0x050a14,.014);
const cam=new THREE.PerspectiveCamera(55,1,.1,600);
scene.add(new THREE.AmbientLight(0x6f8fbf,.85));
const L1=new THREE.PointLight(BLUE2,2.4,70),L2=new THREE.PointLight(YEL,2.2,70);scene.add(L1,L2);
const dl=new THREE.DirectionalLight(0xffffff,.55);dl.position.set(5,12,8);scene.add(dl);
const mkMat=(c,e=.4)=>new THREE.MeshStandardMaterial({color:c,emissive:c,emissiveIntensity:e,metalness:.4,roughness:.4});
const setC=(m,c,e)=>{m.material.color.setHex(c);m.material.emissive.setHex(c);m.material.emissiveIntensity=e};
function glowTex(){const c=document.createElement('canvas');c.width=c.height=64;const g=c.getContext('2d'),r=g.createRadialGradient(32,32,0,32,32,32);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.3,'rgba(255,255,255,.5)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,64,64);return new THREE.CanvasTexture(c)}
const GLOW=glowTex();
function tag(t,col='#ffd43b',fs=34,op=1){const c=document.createElement('canvas'),g=c.getContext('2d');g.font=`700 ${fs}px monospace`;const w=Math.ceil(g.measureText(t).width)+24;c.width=w;c.height=fs+20;g.font=`700 ${fs}px monospace`;g.textBaseline='middle';g.fillStyle=col;g.shadowColor=col;g.shadowBlur=12;g.fillText(t,12,c.height/2);const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),transparent:true,opacity:op,depthWrite:false}));sp.scale.set(w/40,c.height/40,1);return sp}
const TC=new Map();function tx(t,fs){const k=t+'|'+fs;let o=TC.get(k);if(!o){const s=tag(t,'#ffffff',fs);o={m:s.material,w:s.scale.x,h:s.scale.y};TC.set(k,o)}return o}
const FAR=ST.length*32;
const grid=new THREE.GridHelper(FAR+240,(FAR+240)/2,BLUE,0x14304f);grid.position.set(FAR/2-16,0,0);grid.material.transparent=true;grid.material.opacity=.45;scene.add(grid);
{const n=1500,a=new Float32Array(n*3);for(let i=0;i<n;i++)a.set([-120+R()*(FAR+240),8+R()*170,-260+R()*220],i*3);
const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(a,3));scene.add(new THREE.Points(g,new THREE.PointsMaterial({color:0xbcd6ff,size:1.4,sizeAttenuation:false,fog:false})))}
const rings=[];
ST.forEach((s,i)=>{
  const p=new THREE.Mesh(new THREE.CylinderGeometry(8,8.4,.4,6),new THREE.MeshStandardMaterial({color:0x0e2442,metalness:.6,roughness:.3,emissive:BLUE,emissiveIntensity:.15}));p.position.set(s.x,.2,0);scene.add(p);
  const r=new THREE.Mesh(new THREE.TorusGeometry(8.7,.07,8,6),new THREE.MeshBasicMaterial({color:YEL}));r.rotation.x=Math.PI/2;r.rotation.z=Math.PI/6;r.position.set(s.x,.45,0);scene.add(r);
  const pl=new THREE.Mesh(new THREE.RingGeometry(8,8.2,64),new THREE.MeshBasicMaterial({color:BLUE2,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide}));pl.rotation.x=-Math.PI/2;pl.position.set(s.x,.5,0);scene.add(pl);
  const b=new THREE.Mesh(new THREE.CylinderGeometry(8,8,24,6,1,true),new THREE.MeshBasicMaterial({color:BLUE,transparent:true,opacity:.05,side:THREE.DoubleSide,blending:THREE.AdditiveBlending,depthWrite:false}));b.position.set(s.x,12,0);scene.add(b);
  rings.push({r,pl,i});
  const t=tag(String(i+1).padStart(2,'0')+' · '+s.n.toUpperCase(),'#5fa8e8',34,.9);t.position.set(s.x,-1.4,7.5);scene.add(t);
});
const toks=[],bases=['def','class','self','import','for','while','return','push()','pop()','enqueue()','pivot','hanoi()','dfs()','bfs()','swap','arr[j]','queue','stack','graph','visited','None','True','range()','print()','O(n log n)','lambda','__init__','len()'].map((w,i)=>tag(w,['#ffd43b','#5fa8e8','#ffffff'][i%3],34,.8));
for(let i=0;i<96;i++){const s=bases[i%bases.length].clone();s.position.set(-14+R()*(FAR+20),2+R()*12,-6-R()*14);s.userData={y:s.position.y,p:R()*6,sp:.4+R()};scene.add(s);toks.push(s)}

/* particles */
const PN=700,pp=new Float32Array(PN*3).fill(-999),pc=new Float32Array(PN*3),pb=new Float32Array(PN*3),pv=new Float32Array(PN*3),pl=new Float32Array(PN);let pk=0;
const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(pp,3));pg.setAttribute('color',new THREE.BufferAttribute(pc,3));
const pts=new THREE.Points(pg,new THREE.PointsMaterial({size:.55,map:GLOW,vertexColors:true,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));pts.frustumCulled=false;scene.add(pts);
const cB=new THREE.Color(BLUE2),cY=new THREE.Color(YEL);
function emit(p,c,sp=1){const i=pk++%PN;pp.set([p.x,p.y,p.z],i*3);pv.set([(R()-.5)*1.4*sp,R()*.9*sp,(R()-.5)*1.4*sp],i*3);pl[i]=1;c.toArray(pb,i*3)}

/* ---------- THE PYTHON SNAKE ---------- */
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
  tongue.scale.z=.15+1.3*Math.pow(Math.max(0,Math.sin(T*3.2)),6);
  emit(head.position,cB,.6);emit(head.position,cB,.6);const i=Math.floor(R()*N);emit(bp[i],i/N<.55?cB:cY,.8);
}

/* ---------- generic 3D array / stack / queue engine ---------- */
const box=new THREE.BoxGeometry(1,1,1),allG=L=>Object.fromEntries(L.map(x=>[x[0],GRN]));
const mk=(L,col,log,d)=>({it:L.map(([id,v,t])=>[id,v,(col&&col[id]!=null)?col[id]:BLUE,t]),log,d});
const vals=L=>L.map(x=>x[1]).join(', ');
function apply(E,st){
  const c=E.cfg,n=st.it.length;E.objs.forEach(o=>{o.on=0;o.sx=o.sy=.001;o.ty=9;o.tz=0});
  st.it.forEach(([id,v,col,t],i)=>{
    const bar=c.lay=='bars',w=c.w||1.8,lx=c.lay=='col'?E.X:E.X+(i-(n-1)/2)*(c.g||2.5);let h,y;
    if(bar){h=v*c.sc;y=.4+h/2}else if(c.lay=='col'){h=1.1;y=.95+i*1.2}else{h=w*.75;y=.7+h/2}
    let o=E.objs.get(id);
    if(!o){o={m:new THREE.Mesh(box,mkMat(BLUE,.5)),l:new THREE.Sprite(),tx:lx,ty:y+4,tz:0,bar};o.m.scale.set(.001,.001,.001);o.m.position.set(lx,y+4,0);scene.add(o.m,o.l);E.objs.set(id,o)}
    const dx=lx-o.tx;o.tz=c.hop&&Math.abs(dx)>.1?(dx>0?1.9:-1.9):0;
    o.on=1;o.tx=lx;o.ty=y;o.sx=bar?1.8:w;o.sy=h;
    setC(o.m,col,col==BLUE?.5:1.3);
    if(col==ORG)for(let k=0;k<8;k++)emit(o.m.position,cY);
    if(t!=null&&t!==o.t){o.t=t;const L=tx(t,c.fs||36),s=Math.min(1,(bar?3:o.sx*1.15)/L.w);o.l.material=L.m;o.l.scale.set(L.w*s,L.h*s,1)}
  })}
function updE(E,dt){
  E.w-=dt;if(E.w<=0){const st=E.steps[E.k];E.k=(E.k+1)%E.steps.length;apply(E,st);log(E.si,st.log);E.w=st.d||.8}
  const k=Math.min(1,dt*8);
  E.objs.forEach(o=>{const m=o.m;m.position.x+=(o.tx-m.position.x)*k;m.position.y+=(o.ty-m.position.y)*k;m.position.z+=(o.tz-m.position.z)*k;m.scale.x+=(o.sx-m.scale.x)*k;m.scale.z=m.scale.x;m.scale.y+=(o.sy-m.scale.y)*k;
    o.l.visible=!!o.on&&o.t!=null&&m.scale.y>.2;o.l.position.set(m.position.x,o.bar?m.position.y+m.scale.y/2+.9:m.position.y,m.position.z+(o.bar?.2:m.scale.x/2+.06));m.visible=m.scale.y>.03})}

/* ---------- step generators (they replay each program's own logic) ---------- */
function bubble(arr){const L=arr.map((v,i)=>[i,v,String(v)]),S=[],fx={},n=L.length;S.push(mk(L,fx,'original array: ['+arr+']',1.2));
  for(let i=0;i<n-1;i++){S.push(mk(L,fx,'pass,'+(i+1),.4));for(let j=0;j<n-i-1;j++){const a=L[j],b=L[j+1];S.push(mk(L,{...fx,[a[0]]:YEL,[b[0]]:YEL},null,.5));if(a[1]>b[1]){L[j]=b;L[j+1]=a;S.push(mk(L,{...fx,[a[0]]:ORG,[b[0]]:ORG},`swapping ${a[1]} with ${b[1]}`,.9))}}fx[L[n-i-1][0]]=GRN}
  S.push(mk(L,allG(L),'sorted array: ['+vals(L)+']',2.8));return S}
function select(arr){const L=arr.map((v,i)=>[i,v,String(v)]),S=[],fx={},n=L.length;S.push(mk(L,fx,'original array ['+arr+']',1.2));
  for(let i=0;i<n;i++){let m=i;for(let j=i+1;j<n;j++){S.push(mk(L,{...fx,[L[i][0]]:BLUE2,[L[m][0]]:ORG,[L[j][0]]:YEL},null,.45));if(L[j][1]<L[m][1])m=j}
    if(m!=i){const a=L[i],b=L[m];L[i]=b;L[m]=a;S.push(mk(L,{...fx,[a[0]]:ORG,[b[0]]:ORG},`pass ${i+1}: swapping ${b[1]} with ${a[1]} -> [${vals(L)}]`,.9))}fx[L[i][0]]=GRN}
  S.push(mk(L,allG(L),'sorted array ['+vals(L)+']',2.8));return S}
function insert(arr){const L=arr.map((v,i)=>[i,v,String(v)]),S=[mk(L,{},'phases: Sorted | Unsorted',1.2)],n=L.length;
  for(let i=1;i<n;i++){const key=L[i];let j=i;S.push(mk(L,{[key[0]]:YEL},null,.5));while(j>0&&L[j-1][1]>L[j][1]){const t=L[j-1];L[j-1]=L[j];L[j]=t;j--;S.push(mk(L,{[key[0]]:ORG},null,.65))}
    S.push(mk(L,{[key[0]]:GRN},`pass:${i} [${vals(L.slice(0,i+1))}] | [${vals(L.slice(i+1))}]`,.6))}
  S.push(mk(L,allG(L),'sorted array ['+vals(L)+']',2.8));return S}
function quick(arr){const Gx=arr.map((v,i)=>[i,v,String(v)]),S=[],fx={};S.push(mk(Gx,fx,'original list: ['+arr+']',1.2));
  (function q(lo,hi){if(lo>hi)return;if(lo==hi){fx[Gx[lo][0]]=GRN;S.push(mk(Gx,fx,null,.4));return}
    const sub=Gx.slice(lo,hi+1),p=sub[sub.length-1],l=sub.slice(0,-1).filter(x=>x[1]<p[1]),r=sub.slice(0,-1).filter(x=>x[1]>p[1]);
    const col={...fx,[p[0]]:ORG};l.forEach(x=>col[x[0]]=BLUE2);r.forEach(x=>col[x[0]]=YEL);
    S.push(mk(Gx,col,`pivot:${p[1]}, left:[${vals(l)}], right:[${vals(r)}]`,1.1));
    Gx.splice(lo,sub.length,...l,p,...r);fx[p[0]]=GRN;S.push(mk(Gx,{...col,[p[0]]:GRN},'pass: ['+vals(Gx)+']',1.1));
    q(lo,lo+l.length-1);q(lo+l.length+1,hi)})(0,Gx.length-1);
  S.push(mk(Gx,allG(Gx),'sorted list: ['+vals(Gx)+']',2.8));return S}
function linear(){const a=[10,20,30,40,50],key=40,L=a.map((v,i)=>[i,v,String(v)]),S=[mk(L,{},`a=[${a}]  key=${key}`,1.2)];
  for(let i=0;i<a.length;i++){const f=a[i]==key;S.push(mk(L,{[i]:f?GRN:YEL},f?'key is found: '+i:'comparisons: '+(i+1),.9));if(f){S.push(mk(L,{[i]:GRN},`case type: average case · comparisons: ${i+1}`,2.6));break}}return S}
function stack(){const S=[],a=[];const sn=(log,h,d)=>S.push(mk(a.map(v=>[v,null,String(v)]),h&&{[h]:YEL},log,d));
  sn('stack=[]',0,1);[1,2,3,4].forEach(v=>{if(a.length==3)sn('stack overflow',0,.9);else{a.push(v);sn(v+' pushed',v,.9)}});
  sn('display: '+[...a].reverse().join(' '),0,1.2);for(let i=0;i<4;i++){if(!a.length)sn('stack underflow',0,i==3?2.2:.9);else sn(a.pop()+' removed',0,.9)}return S}
function queue(){const S=[],a=[];const sn=(log,h,d)=>S.push(mk(a.map(v=>[v,null,String(v)]),h||(a.length?{[a[0]]:BLUE2}:0),log,d));
  sn('queue=[]',0,1);[1,2,3,4].forEach(v=>{if(a.length==3)sn('queue overflow',0,.9);else{a.push(v);sn(v+' inserted',{[v]:YEL},.9)}});
  sn('display: '+a.join(' '),0,1.2);for(let i=0;i<4;i++){if(!a.length)sn('queue underflow',0,i==3?2.2:.9);else sn(a.shift()+' removed',0,.9)}return S}
function pq(){const P=[[40,3],[10,1],[30,2],[20,4]],S=[],a=[];const sn=(log,d,h)=>S.push(mk(a.map(([x,p])=>[x,null,`${x} p${p}`]),h,log,d));
  sn('queue=[]',1);P.forEach(p=>{a.push(p);sn(`${p[0]} priority ${p[1]}`,.9,{[p[0]]:YEL})});
  a.sort((x,y)=>x[1]-y[1]);sn('queue.sort() → lowest priority first',1.4,{[a[0][0]]:ORG});const r=a.shift();sn('removed item: '+r[0],2.2)
  return S}
function arrcmp(){const nm='ABCDEF',a=[],S=[];const sn=(log,d,h)=>S.push(mk(a.map((n,i)=>[n,null,`${n},${i+1},${n}`]),h,log,d));
  sn('student=[None]*3',1);for(let i=0;i<6;i++){if(a.length<3){a.push(nm[i]);sn(`add_student("${nm[i]}",${i+1},"${nm[i]}")`,.9,{[nm[i]]:YEL})}else sn('array is full',.8)}
  a.forEach(n=>sn('display: '+n,.7,{[n]:GRN}));sn('time taken: 0.00001 · space used: 88',2.4);return S}
function fact(){const S=[],fr=[],n=4;const sn=(log,d,h)=>S.push(mk(fr.map(([k,t])=>[k,null,t]),h,log,d));
  sn('fact(4)',1);for(let k=n;k>=1;k--){fr.push([k,`fact(${k})`]);sn(k>1?`${k} * fact(${k-1})`:'=1',.9,{[k]:YEL})}
  let r=1;for(let k=1;k<=n;k++){r*=k;fr[fr.length-1]=[k,`fact(${k})=${r}`];sn(`fact(${k}) = ${r}`,.9,{[k]:GRN});if(k<n)fr.pop()}
  sn('=4*3*2*1 = 24',2.6,{[4]:GRN});return S}
function stu(m0,m1,tm){const M=m=>[['n',null,'name:Nesara'],['r',null,'rollno:20'],['m',null,'marks:'+m]],S=[];
  S.push(mk(M(m0),{},`display → Nesara, 20, ${m0}`,1.4),mk(M(m0),{m:YEL},`update(${m1})`,.8),mk(M(m1),{m:ORG},'marks updated',.9),mk(M(m1),{m:GRN},`display → Nesara, 20, ${m1}`,tm?1.2:2.6));
  if(tm)S.push(mk(M(m1),{m:GRN},'time taken: 0.00004 s · space used: 48 bytes',2.6));return S}
function ds(){const S=[],T=(L,h,log,d)=>S.push(mk(L.map(x=>[x,null,String(x)]),h,log,d)),nums=[10,20,30,40];
  T(nums,0,'numbers=[10, 20, 30, 40]',1.1);T([...nums,50],{50:YEL},'numbers.append(50)',1.1);T([...nums,50],{50:GRN},'[10, 20, 30, 40, 50]',1);
  T(['apple','banana','orange'],{orange:ORG},'fruits.remove("orange")',1.1);T(['apple','banana'],0,"['apple', 'banana']",.9);T(['apple','banana','papaya'],{papaya:YEL},'fruits.append("papaya")',1.1);
  T(['name:Nesara','age:20','course:python'],0,'student={name, age, course}',1.1);T(['name:Nesara','age:17','course:python'],{'age:17':ORG},'student["age"]=17',2.6);return S}

/* ---------- graph engine (BFS / DFS) ---------- */
function graph(si,steps){const X=ST[si].x,nodes={},ed={},np=k=>new THREE.Vector3(X+BN[k][0],BN[k][1]+.7,0),Y=new THREE.Vector3(0,1,0);
  for(const k in G)G[k].forEach(c=>{const a=np(k),b=np(c),e=new THREE.Mesh(new THREE.CylinderGeometry(.07,.07,a.distanceTo(b),8),mkMat(BLUE2,.35));e.position.copy(a).add(b).multiplyScalar(.5);e.quaternion.setFromUnitVectors(Y,b.clone().sub(a).normalize());scene.add(e);ed[k+'-'+c]=e});
  for(const k in BN){const m=new THREE.Mesh(new THREE.SphereGeometry(.85,24,16),mkMat(BLUE,.45));m.position.copy(np(k));scene.add(m);const l=tag(k,'#ffffff',40);l.position.set(m.position.x,m.position.y,.95);scene.add(l);nodes[k]=m}
  const E={si,X,steps,k:0,w:1,cur:null,nodes,ed,u:updG};E.reset=()=>{for(const k in nodes)setC(nodes[k],BLUE,.45);for(const k in ed)setC(ed[k],BLUE2,.35);E.cur=null};return E}
function updG(E,dt){
  E.w-=dt;
  if(E.w<=0){const s=E.steps[E.k++];
    if(!s){E.k=0;E.w=1;E.reset();log(E.si,'--- reset: visited=[] ---')}
    else{E.cur=E.nodes[s.n];setC(E.cur,YEL,1.4);s.qd.forEach(c=>setC(E.nodes[c],BLUE2,1));s.ed.forEach(k=>setC(E.ed[k],YEL,1.1));s.logs.forEach(t=>log(E.si,t));E.w=1.15;for(let i=0;i<22;i++)emit(E.cur.position,cY,1.2);if(E.k==E.steps.length)E.w=3.2}}
  for(const k in E.nodes)E.nodes[k].scale.setScalar(E.nodes[k]===E.cur?1.12+.1*Math.sin(clock*7):1);
}

/* ---------- Tower of Hanoi, n=3 ---------- */
function hanoi(si){const X=ST[si].x,pX=k=>X+(k-1)*5.4,dY=l=>1.05+l*.66,dk=[null];
  for(let k=0;k<3;k++){const p=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,6,12),mkMat(0xaac4e6,.3));p.position.set(pX(k),3.4,0);scene.add(p);const t=tag('ABC'[k],'#5fa8e8',40);t.position.set(pX(k),7.2,0);scene.add(t)}
  for(let d=1;d<=3;d++){const r=.8+d*.45,m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,.6,40),mkMat([0,YEL,BLUE2,BLUE][d],.55));scene.add(m);dk.push(m)}
  const E={si,X,w:1,hu:-1,u:updH,dk,pX,dY};
  E.init=()=>{E.HM=[];(function h(n,a,b,c){if(!n)return;h(n-1,a,c,b);E.HM.push([n,a,c]);h(n-1,b,a,c)})(3,0,1,2);E.hs=[[3,2,1],[],[]];E.hs.forEach((s,k)=>s.forEach((d,l)=>dk[d].position.set(pX(k),dY(l),0)));E.hm=0;E.hu=-1};E.init();return E}
const ez=x=>x*x*(3-2*x),lr=(a,b,t)=>a+(b-a)*t;
function updH(E,dt){
  if(E.w>0){E.w-=dt;return}
  const m=E.HM[E.hm];if(!m){E.init();E.w=.8;log(E.si,'--- reset  A:[3, 2, 1] | B:[] | C:[] ---');return}
  const d=E.dk[m[0]];
  if(E.hu<0){E.hu=0;E.h0=d.position.clone();E.h1=new THREE.Vector3(E.pX(m[2]),E.dY(E.hs[m[2]].length),0);log(E.si,`move disk ${m[0]} from ${'ABC'[m[1]]} to ${'ABC'[m[2]]}`)}
  E.hu+=dt/1.5;const u=Math.min(E.hu,1),a=E.h0,b=E.h1;
  if(u<.3)d.position.set(a.x,lr(a.y,7.4,ez(u/.3)),0);else if(u<.7)d.position.set(lr(a.x,b.x,ez((u-.3)/.4)),7.4,0);else d.position.set(b.x,lr(7.4,b.y,ez((u-.7)/.3)),0);
  if(u>.05&&u<.95)emit(d.position,cY,.5);
  if(E.hu>=1){E.hs[m[2]].push(E.hs[m[1]].pop());E.hm++;E.hu=-1;E.w=.2;if(E.hm==E.HM.length){E.w=3;log(E.si,'A:[] | B:[] | C:[3, 2, 1]')}}
}

/* ---------- build engines ---------- */
const ENG=[];
ST.forEach((s,i)=>{ENG.push(s.k=='g'?graph(i,s.st):s.k=='h'?hanoi(i):{si:i,X:s.x,cfg:s.cfg,steps:s.gen(),k:0,w:.5,objs:new Map(),u:updE})});

/* ---------- UI ---------- */
const DESC=['Python stores data in a list, set or dict. append() adds one item at the end, remove() deletes one, and a dict value is changed by its key.','A student object keeps name, rollno and marks. update() changes only the marks (90 to 95); the name and rollno stay the same.','Same student update, but we measure time with perf_counter() and memory with getsizeof() to see how fast it runs and how much space it uses.','An array has a fixed size (3). Students A, B, C fit. When D, E, F come, there is no space, so it prints: array is full.','Stack = Last In, First Out. push puts a number on top, pop removes the top one. A 4th push is overflow, popping an empty stack is underflow.','Queue = First In, First Out. enqueue adds at the back, dequeue removes from the front. Too many adds = overflow, empty remove = underflow.','Every item has a priority. The queue is sorted, and the item with the lowest priority number is removed first.','Factorial uses recursion. fact(4) calls fact(3), then fact(2), then fact(1) = 1. Then each call returns and multiplies: 4*3*2*1 = 24.','Linear search checks the list one element at a time from the start until it finds the key. More comparisons = slower (O(n)).','Bubble sort compares neighbours and swaps them if they are in the wrong order. After each pass the biggest value reaches the end (green).','Selection sort finds the smallest value in the unsorted part (orange) and swaps it to the front. The green bars are already sorted.','Insertion sort takes one key (yellow) and slides it left into its correct place inside the sorted part, like arranging playing cards.','Quick sort picks the last value as pivot (orange). Smaller values go left (light blue), bigger go right (yellow). Then it repeats on both sides.','Move all disks from A to C. Only one disk at a time, and a big disk never goes on a small one. 3 disks need 7 moves (2 to the power n, minus 1).','BFS visits the graph level by level using a queue: 50, then 30 and 70, then 20, 40, 60, 80.','DFS goes as deep as possible first using recursion: 50, 30, 20, then back to 40, then 70, 60, 80.'];
const logs=ST.map(()=>[]);let cur=0,tgtX=0,camX=0,auto=true,lastSw=0,clock=0;
function log(i,t){if(!t)return;const a=logs[i];a.push('>>> '+t);if(a.length>4)a.shift();if(i===cur)$('log').textContent=a.join('\n')}
const hl=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/(#.*$)|("[^"]*"|'[^']*')|\b(def|class|for|if|while|return|import|in|not|else)\b|\b(\d+)\b/gm,(m,c,q,k)=>`<i class="${c?'c':q?'s':k?'k':'n'}">${m}</i>`);
function ui(){[...$('nav').children].forEach((b,i)=>b.classList.toggle('on',i===cur));$('file').textContent=ST[cur].f;$('cx').textContent=ST[cur].cx;$('code').innerHTML=hl(ST[cur].code);$('why').textContent='What is happening: '+DESC[cur];$('log').textContent=logs[cur].join('\n')}
function go(i){cur=(i+ST.length)%ST.length;tgtX=ST[cur].x;lastSw=clock;ui();const b=$('nav').children[cur];if(b&&b.scrollIntoView)b.scrollIntoView({block:'nearest',inline:'center'})}
ST.forEach((s,i)=>{const b=document.createElement('button');b.textContent=(i+1)+' · '+s.n;b.onclick=()=>go(i);$('nav').appendChild(b)});
{const b=document.createElement('button');b.textContent='AUTO TOUR: ON';b.onclick=()=>{auto=!auto;lastSw=clock;b.textContent='AUTO TOUR: '+(auto?'ON':'OFF')};$('nav').appendChild(b)}
addEventListener('keydown',e=>{if(e.key=='ArrowRight')go(cur+1);if(e.key=='ArrowLeft')go(cur-1)});
let mx=0,my=0;addEventListener('pointermove',e=>{mx=e.clientX/innerWidth*2-1;my=e.clientY/innerHeight*2-1});
let dist=17,ox=0;function rs(){renderer.setSize(innerWidth,innerHeight);cam.aspect=innerWidth/innerHeight;dist=cam.aspect<.8?30:cam.aspect<1.2?23:17;ox=cam.aspect>1.3?4:0;cam.updateProjectionMatrix()}addEventListener('resize',rs);rs();ui();

/* ---------- main loop ---------- */
const clk=new THREE.Clock();
function tick(){
  requestAnimationFrame(tick);
  const dt=Math.min(clk.getDelta(),.05)*(RM?.35:1);clock+=dt;
  if(auto&&clock-lastSw>11)go(cur+1);
  camX+=(tgtX-camX)*(1-Math.exp(-dt*2.2));const gap=tgtX-camX;
  cam.fov+=(55+Math.min(Math.abs(gap)*.12,26)-cam.fov)*.1;cam.updateProjectionMatrix();
  cam.position.set(camX-ox+mx*3+Math.sin(clock*.2)*1.5,4.8-my*1.4,dist);cam.lookAt(camX-ox,2.2,0);cam.rotateZ(Math.max(-.14,Math.min(.14,gap*.004)));
  cen.x=camX+Math.max(-30,Math.min(30,gap*.35));L1.position.set(camX-9,9,9);L2.position.set(camX+9,5,7);
  snake(clock*1.05);
  ENG.forEach(E=>{if(Math.abs(E.X-camX)<46)E.u(E,dt)});
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
