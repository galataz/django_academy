import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {createWorld} from './world.js';
// Export actual 3D geometry into small local WebP illustrations.
const holder=document.createElement('div');holder.style.cssText='width:640px;height:420px';document.body.append(holder);
const world=createWorld(holder,()=>{});world.stopAnimation();
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true});renderer.setSize(640,420);renderer.setPixelRatio(1);renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
const materials=new Map();function mat(c){if(!materials.has(c))materials.set(c,new THREE.MeshStandardMaterial({color:c,roughness:.85}));return materials.get(c);}
function mesh(g,c,x,y,z,p){const m=new THREE.Mesh(g,mat(c));m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;p.add(m);return m;}
const box=(w,h,d,c,x,y,z,p,r=.04)=>mesh(new RoundedBoxGeometry(w,h,d,2,r),c,x,y,z,p);
const cyl=(r,h,c,x,y,z,p)=>mesh(new THREE.CylinderGeometry(r,r,h,24),c,x,y,z,p);
const ball=(r,c,x,y,z,p)=>mesh(new THREE.IcosahedronGeometry(r,1),c,x,y,z,p);
function group(p,x=0,y=0,z=0){const g=new THREE.Group();g.position.set(x,y,z);p.add(g);return g;}
function tree(p,x,z,s=1){const g=group(p,x,0,z);cyl(.11,1,'#9e865b',0,.9,0,g);for(let i=0;i<3;i++)mesh(new THREE.ConeGeometry((.65-i*.12)*s,.95*s,7),['#629b75','#81b287','#a2c394'][i],0,1.2+i*.45*s,0,g);}
function station(p,key,scale=1,x=0,z=0){const original=world.scene.children.find(g=>g.isGroup&&g.children.some(c=>c.userData.station===key));const clone=original.clone(true);clone.position.set(x,0,z);clone.scale.setScalar(scale);p.add(clone);return clone;}
function key(p,x=0,y=0,z=0,s=1){const g=group(p,x,y,z);mesh(new THREE.TorusGeometry(.35,.13,8,24),'#e8b85b',0,1.8,0,g);box(.18,.9,.18,'#e8b85b',0,1.18,0,g);box(.3,.15,.2,'#e8b85b',.18,.93,0,g);box(.3,.15,.2,'#e8b85b',.18,1.22,0,g);g.scale.setScalar(s);g.rotation.z=-.42;return g;}
function shield(p,x=0,y=0,z=0,s=1){const g=group(p,x,y,z),shape=new THREE.Shape();shape.moveTo(-.8,.6);shape.lineTo(0,.95);shape.lineTo(.8,.6);shape.lineTo(.65,-.4);shape.lineTo(0,-.95);shape.lineTo(-.65,-.4);shape.closePath();const m=mesh(new THREE.ExtrudeGeometry(shape,{depth:.22,bevelEnabled:true,bevelSize:.07,bevelThickness:.06,bevelSegments:2,steps:1}),'#7db69c',0,1.8,0,g);const c=box(.14,.52,.14,'#fff0c9',-.12,1.72,.32,g);c.rotation.z=.65;const d=box(.14,.82,.14,'#fff0c9',.22,1.86,.32,g);d.rotation.z=-.55;g.scale.setScalar(s);return g;}
function server(p,x=0,z=0,s=1){const g=group(p,x,0,z);box(1.3,2.9,1.15,'#769e9e',0,2.1,0,g,.15);for(let i=0;i<4;i++){box(1.1,.5,.13,'#315f65',0,1.2+i*.63,.61,g);ball(.06,'#f1cc80',.37,1.2+i*.63,.71,g);for(let k=0;k<3;k++)box(.45,.025,.02,'#b2caba',-.12,1.08+i*.63+k*.1,.69,g,0);}g.scale.setScalar(s);return g;}
function cloud(p,x=0,y=0,z=0,s=1){const g=group(p,x,y,z);for(const [a,b,r] of [[-.6,0,.6],[0,.3,.85],[.7,0,.55]])ball(r,'#fff3d5',a,3+b,0,g);g.scale.setScalar(s);return g;}
function sensor(p,x=0,z=0,s=1){const g=group(p,x,0,z);cyl(.45,.18,'#bfaf84',0,.76,0,g);cyl(.055,2.3,'#5f8d7c',0,1.95,0,g);box(.85,1.05,.55,'#f1e9c9',0,2.2,.1,g,.12);box(.6,.36,.1,'#4c9284',0,2.35,.42,g,.04);ball(.065,'#e8ae61',0,1.92,.43,g);for(let i=0;i<2;i++){const arc=mesh(new THREE.TorusGeometry(.55+i*.3,.045,6,30,Math.PI),'#7dac92',0,3.25,0,g);arc.rotation.z=0;}g.scale.setScalar(s);return g;}
function parcel(p,x=0,z=0,s=1){const g=group(p,x,0,z);box(1,1,.9,'#dfae72',0,1.2,0,g,.08);box(.16,1.04,.94,'#f6e6b8',0,1.2,0,g,.02);g.scale.setScalar(s);return g;}
function board(p,type='chart',x=0,z=0,s=1){const g=group(p,x,0,z);box(2.5,1.9,.25,'#f7efce',0,2.2,0,g,.12);box(.18,1.1,.18,'#a5a781',-.8,1.1,0,g);box(.18,1.1,.18,'#a5a781',.8,1.1,0,g);if(type==='chart'){for(let i=0;i<4;i++)box(.32,.3+i*.26,.15,['#8db899','#6e9f91','#e6b776','#d59b74'][i],-.75+i*.5,1.7+i*.13,.23,g);}else{for(let i=0;i<3;i++){box(1.4,.09,.12,'#89a68d',.17,2.68-i*.4,.22,g);ball(.08,'#daa564',-.86,2.68-i*.4,.24,g);}}g.scale.setScalar(s);return g;}
function envelope(p,x=0,z=0,s=1){const g=group(p,x,0,z);box(1.8,1.3,.25,'#fff0cf',0,1.6,0,g,.08);for(const a of [-1,1]){const b=box(1.03,.065,.065,'#d2a676',a*.4,1.72,.18,g);b.rotation.z=a*.62;}g.scale.setScalar(s);return g;}
function clock(p,x=0,z=0,s=1){const g=group(p,x,0,z);const ring=cyl(.74,.2,'#eedeb0',0,1.5,0,g);ring.rotation.x=Math.PI/2;const face=cyl(.62,.22,'#fff4d5',0,1.5,.02,g);face.rotation.x=Math.PI/2;box(.06,.47,.06,'#507e6b',0,1.7,.17,g);box(.37,.06,.06,'#507e6b',.16,1.5,.17,g);g.scale.setScalar(s);return g;}
function gear(p,x=0,z=0,s=1){const g=group(p,x,0,z);mesh(new THREE.TorusGeometry(.53,.16,8,20),'#dba96e',0,1.6,0,g);for(let i=0;i<8;i++){const a=i*Math.PI/4,b=box(.27,.3,.27,'#dba96e',Math.cos(a)*.58,1.6+Math.sin(a)*.58,0,g);b.rotation.z=a;}g.scale.setScalar(s);return g;}
function blocks(p,x=0,z=0,s=1){const g=group(p,x,0,z);for(const [a,b,c] of [[-.6,1,'#85b2a0'],[.6,1,'#dfb483'],[0,1.9,'#e9d7a2']])box(.96,.83,.96,c,a,b,0,g,.08);g.scale.setScalar(s);return g;}
function gate(p){station(p,'cqs',1);shield(p,0,.25,1.2,.72);key(p,1.2,.2,.5,.65);}
function toolbox(p){box(2.4,1.1,1.45,'#709f8d',0,1.2,0,p,.12);box(2.5,.2,1.55,'#9bbc9d',0,1.85,0,p,.08);mesh(new THREE.TorusGeometry(.45,.08,6,20,Math.PI),'#ede4c0',0,2.05,0,p);box(.32,.28,.1,'#e2b96e',0,1.48,.79,p);gear(p,1.2,.7,.75);}
function main(p,type){if(['front','cqs','service','repo','db'].includes(type)){station(p,type);return;}if(type==='shield'){gate(p);return;}if(type==='cloud'){server(p,-.7,0,.9);server(p,.85,-.45,.72);cloud(p,0,.3,0);return;}if(type==='sensor'){sensor(p,-.4,0,1.05);station(p,'db',.5,1.3,.65);return;}if(type==='board'){board(p,'chart',0,0,1.3);return;}if(type==='check'){board(p,'check',0,0,1.2);shield(p,-1.15,-.1,1.1,.65);return;}if(type==='mail'){envelope(p,0,0,1.7);parcel(p,1.1,1,.6);return;}if(type==='blocks'){blocks(p,0,0,1.5);return;}if(type==='tool'){toolbox(p);return;}if(type==='identity'){gate(p);return;}}
const propFns={key:(p,x,z,s)=>key(p,x,0,z,s),shield:(p,x,z,s)=>shield(p,x,0,z,s),sensor,parcel,chart:(p,x,z,s)=>board(p,'chart',x,z,s),check:(p,x,z,s)=>board(p,'check',x,z,s),mail:envelope,clock,gear,blocks,server,cloud:(p,x,z,s)=>cloud(p,x,-1,z,s)};
window.renderCard=({type,prop,variant=0,unit=1})=>{
 const scene=new THREE.Scene();scene.background=new THREE.Color('#dceae1');scene.add(new THREE.HemisphereLight('#fff5d6','#699583',2.7));const sun=new THREE.DirectionalLight('#fff1d7',4);sun.position.set(-8,16,10);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);sun.shadow.camera.left=-8;sun.shadow.camera.right=8;sun.shadow.camera.top=8;sun.shadow.camera.bottom=-8;sun.shadow.normalBias=.045;sun.shadow.radius=4;scene.add(sun);
 const plane=mesh(new THREE.PlaneGeometry(200,200),'#dceae1',0,-.08,0,scene);plane.rotation.x=-Math.PI/2;plane.castShadow=false;
 cyl(3.75,.24,'#e6cf9f',0,.07,0,scene);cyl(3.65,.18,'#ebdfb5',0,.27,0,scene);cyl(3.48,.18,'#becd94',0,.44,0,scene);
 const content=group(scene,-.25,0,-.15);main(content,type);
 if(prop&&propFns[prop]){const pad=cyl(.82,.1,'#f2e7c2',2,.6,1.45,scene);propFns[prop](scene,2,1.45,.65);}
 tree(scene,-2.4,-.7,.8);if(variant%2===0)tree(scene,1.6,-2.2,.6);
 for(let i=0;i<5;i++){const a=i*.9+variant*.17,x=Math.cos(a)*3.1,z=Math.sin(a)*3.1;if(z>0&&x>1.5)continue;ball(.16,'#90b078',x,.66,z,scene);cyl(.025,.22,'#769362',x+.18,.68,z+.15,scene);ball(.075,['#f2ca79','#faf1ce','#dca583'][i%3],x+.18,.83,z+.15,scene);}
 for(let i=0;i<3;i++){const slab=box(.65,.035,.42,'#f1e6c1',-1.4+i*.1,.56,1.7+i*.45,scene,0);slab.rotation.y=.2;}
 const camera=new THREE.PerspectiveCamera(type==='service'?31:28,640/420,.1,100);camera.position.set(8.5+variant%3*.15,8.3,12.4);camera.lookAt(0,type==='service'?1.45:1.1,0);renderer.render(scene,camera);const output=renderer.domElement.toDataURL('image/webp',.86);
 // Preserve shared station geometry and dispose only this export's independent geometry.
 const shared=new Set();world.scene.traverse(o=>{if(o.geometry)shared.add(o.geometry);});scene.traverse(o=>{if(o.geometry&&!shared.has(o.geometry))o.geometry.dispose();});sun.shadow.map?.dispose();return output;
};
window.cardRendererReady=true;
