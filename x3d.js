// Xbox-era 3D renderer for the TV game (Three.js, WebGL).
// Reads the same match state the 2D game uses (window.M etc.) and draws it in 3D.
// World units: map x,y (0..1000) become three.js x,z. Heights are in the same units.
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const G = window; let S = {};
let R = null, scene, cam, sun, hemi, built = null, guys = new Map(), fxGroup, stormMesh, waterMesh, terrain, dropGroup, lambGroup, chestGroup;
let tmpV = new THREE.Vector3();

function canvasTex(w, h, paint) { const c = document.createElement('canvas'); c.width = w; c.height = h; paint(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t; }
function noiseTex(base, var1, n = 128) { return canvasTex(n, n, (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h); for (let i = 0; i < w * h / 3; i++) { g.fillStyle = var1[i % var1.length]; g.globalAlpha = Math.random() * .35; g.fillRect(Math.random() * w, Math.random() * h, 1 + Math.random() * 2, 1 + Math.random() * 2); } g.globalAlpha = 1; }); }

function heightAt(x, z) {
  const M = S.M; if (!M) return 0; let h = 0;
  const dc = Math.hypot(x - M.cx0, z - M.cy0); if (dc > M.isR - 4) h -= Math.min(6, (dc - M.isR + 4) * .25);
  if (M.mtn) { const d = Math.hypot(x - M.mtn.x, (z - M.mtn.y) * 1.3); if (d < 100) h += Math.pow(1 - d / 100, 1.6) * 70; }
  if (M.lake) { const d = Math.hypot((x - M.lake.x) / 1.4, z - M.lake.y); if (d < 34) h -= (1 - d / 34) * 4; }
  return h;
}
G.x3dHeight = heightAt;

export function init() {
  const c = document.createElement('canvas');
  try { R = new THREE.WebGLRenderer({ canvas: c, antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' }); } catch (e) { return false; }
  R.setPixelRatio(1); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap; R.outputColorSpace = THREE.SRGBColorSpace; R.toneMapping = THREE.ACESFilmicToneMapping; R.toneMappingExposure = 1.05;
  scene = new THREE.Scene();
  scene.background = canvasTex(4, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#3a78d8'); gr.addColorStop(.55, '#9ccaf0'); gr.addColorStop(1, '#e8f0f4'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  scene.fog = new THREE.Fog(0xcfe2f0, 140, 520);
  cam = new THREE.PerspectiveCamera(62, 16 / 9, .5, 1400);
  hemi = new THREE.HemisphereLight(0xcfe8ff, 0x5a7a3a, .75); scene.add(hemi);
  sun = new THREE.DirectionalLight(0xfff1d6, 2.2); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -120, right: 120, top: 120, bottom: -120, near: 1, far: 500 }); sun.shadow.bias = -.0006; scene.add(sun); scene.add(sun.target);
  G.x3dCanvas = c; return true;
}

function clearBuilt() { if (!built) return; scene.remove(built); built.traverse(o => { o.geometry && o.geometry.dispose(); }); built = null; guys.forEach(g => scene.remove(g)); guys.clear(); }

function buildWorld(M) {
  clearBuilt(); built = new THREE.Group(); scene.add(built);
  // terrain: the generated island map as the colour texture, displaced for the mountain and coast
  const seg = 200, geo = new THREE.PlaneGeometry(1000, 1000, seg, seg); geo.rotateX(-Math.PI / 2); geo.translate(500, 0, 500);
  const pos = geo.attributes.position; for (let i = 0; i < pos.count; i++) pos.setY(i, heightAt(pos.getX(i), pos.getZ(i)));
  geo.computeVertexNormals();
  const mt = new THREE.CanvasTexture(S.mapC); mt.colorSpace = THREE.SRGBColorSpace; mt.anisotropy = 8; mt.magFilter = THREE.LinearFilter;
  const detail = noiseTex('#808080', ['#000', '#fff', '#606060']); detail.wrapS = detail.wrapT = THREE.RepeatWrapping; detail.repeat.set(120, 120);
  const tm = new THREE.MeshStandardMaterial({ map: mt, roughness: .95, metalness: 0, bumpMap: detail, bumpScale: .6 });
  terrain = new THREE.Mesh(geo, tm); terrain.receiveShadow = true; built.add(terrain);
  // sea
  const wg = new THREE.PlaneGeometry(4000, 4000); wg.rotateX(-Math.PI / 2);
  waterMesh = new THREE.Mesh(wg, new THREE.MeshPhongMaterial({ color: 0x2a6ab0, specular: 0xbfe0ff, shininess: 90, transparent: true, opacity: .92 })); waterMesh.position.set(500, -1.2, 500); waterMesh.receiveShadow = true; built.add(waterMesh);
  // trees (instanced): pines in the snow, round trees elsewhere
  const trunkG = new THREE.CylinderGeometry(.6, .9, 5, 6), pineG = new THREE.ConeGeometry(4.2, 11, 7), leafG = new THREE.IcosahedronGeometry(4.6, 1);
  const trunkM = new THREE.MeshStandardMaterial({ color: 0x6a4a2a, roughness: 1 }), pineM = new THREE.MeshStandardMaterial({ color: 0x24603a, roughness: .9, flatShading: true }), leafM = new THREE.MeshStandardMaterial({ color: 0x2f8a3a, roughness: .9, flatShading: true });
  const n = M.trees.length, trunks = new THREE.InstancedMesh(trunkG, trunkM, n), pines = new THREE.InstancedMesh(pineG, pineM, n), leaves = new THREE.InstancedMesh(leafG, leafM, n);
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(); let np = 0, nl = 0;
  M.trees.forEach((t, i) => { const y = heightAt(t.x, t.y), s = .8 + ((t.x * 7 + t.y) % 10) / 20; m4.compose(tmpV.set(t.x, y + 2.5 * s, t.y), q, sc.set(s, s, s)); trunks.setMatrixAt(i, m4);
    if (t.y < M.cy0 - 250) { m4.compose(tmpV.set(t.x, y + 9 * s, t.y), q, sc.set(s, s, s)); pines.setMatrixAt(np++, m4); } else { m4.compose(tmpV.set(t.x, y + 8 * s, t.y), q, sc.set(s, s * .9, s)); leaves.setMatrixAt(nl++, m4); } });
  pines.count = np; leaves.count = nl; [trunks, pines, leaves].forEach(o => { o.castShadow = true; o.receiveShadow = true; built.add(o); });
  // bushes
  const bushG = new THREE.IcosahedronGeometry(3.2, 1), bushes = new THREE.InstancedMesh(bushG, new THREE.MeshStandardMaterial({ color: 0x3f9a3a, roughness: 1, flatShading: true }), M.bushes.length);
  M.bushes.forEach((b, i) => { m4.compose(tmpV.set(b.x, heightAt(b.x, b.y) + 1.6, b.y), q, sc.set(1.2, .8, 1.2)); bushes.setMatrixAt(i, m4); }); bushes.castShadow = true; built.add(bushes);
  // buildings from the collision boxes, with windows and roofs
  const wallTex = canvasTex(64, 64, (g, w, h) => { g.fillStyle = '#c9b38f'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 4) { g.fillStyle = 'rgba(0,0,0,.08)'; g.fillRect(0, y, w, 1); } g.fillStyle = '#3a4a5a'; g.fillRect(10, 18, 14, 14); g.fillRect(40, 18, 14, 14); g.fillStyle = '#9ad4f5'; g.fillRect(12, 20, 10, 10); g.fillRect(42, 20, 10, 10); g.fillStyle = '#5a3a22'; g.fillRect(26, 40, 12, 24); });
  wallTex.wrapS = wallTex.wrapT = THREE.RepeatWrapping;
  M.buildMeshes = [];
  for (const sb of M.solids) { const [x, y, w, d, hh] = sb, H = hh * 7, gy = heightAt(x + w / 2, y + d / 2); const t = wallTex.clone(); t.needsUpdate = true; t.repeat.set(Math.max(1, w / 12), Math.max(1, H / 10));
    const box = new THREE.Mesh(new THREE.BoxGeometry(w, H, d), new THREE.MeshStandardMaterial({ map: t, roughness: .85 })); box.position.set(x + w / 2, gy + H / 2, y + d / 2); box.castShadow = box.receiveShadow = true; box.userData.key = sb.join(','); built.add(box);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(Math.hypot(w, d) * .55, H * .5, 4), new THREE.MeshStandardMaterial({ color: [0x8a3a2a, 0x4a5a7a, 0x6a4a3a][(x | 0) % 3], roughness: .8, flatShading: true }));
    roof.rotation.y = Math.PI / 4; roof.scale.set(w / Math.hypot(w, d) * 1.4, 1, d / Math.hypot(w, d) * 1.4); roof.position.set(x + w / 2, gy + H + H * .25, y + d / 2); roof.castShadow = true; built.add(roof); M.buildMeshes.push({ key: box.userData.key, box, roof }); }
  // cars
  const carG = new THREE.BoxGeometry(12, 3.4, 6), cabG = new THREE.BoxGeometry(6, 2.6, 5.4);
  M.cars.forEach(cr => { const g = new THREE.Group(), col = new THREE.Color(cr.col); const body = new THREE.Mesh(carG, new THREE.MeshStandardMaterial({ color: col, roughness: .35, metalness: .4 })); body.position.y = 2.4; const cab = new THREE.Mesh(cabG, new THREE.MeshStandardMaterial({ color: 0x33404a, roughness: .2, metalness: .6 })); cab.position.set(-1, 5, 0);
    g.add(body, cab); for (const [ax, az] of [[-4, -3.2], [4, -3.2], [-4, 3.2], [4, 3.2]]) { const wh = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 1, 10), new THREE.MeshStandardMaterial({ color: 0x111111 })); wh.rotation.x = Math.PI / 2; wh.position.set(ax, 1.3, az); g.add(wh); }
    g.position.set(cr.x, heightAt(cr.x, cr.y), cr.y); g.traverse(o => { o.castShadow = true; }); cr.mesh = g; built.add(g); });
  // chests, vending machines
  chestGroup = new THREE.Group(); built.add(chestGroup);
  M.chests.forEach(ch => { const m = new THREE.Mesh(new THREE.BoxGeometry(3.4, 2.4, 2.2), new THREE.MeshStandardMaterial({ color: 0xb07a20, emissive: 0x3a2400, roughness: .5, metalness: .3 })); m.position.set(ch.x, heightAt(ch.x, ch.y) + 1.2, ch.y); m.castShadow = true; ch.mesh = m; chestGroup.add(m); });
  (M.vends || []).forEach(v => { const m = new THREE.Mesh(new THREE.BoxGeometry(3, 7, 2.4), new THREE.MeshStandardMaterial({ color: 0xc02020, emissive: 0x200000, roughness: .4 })); m.position.set(v.x, heightAt(v.x, v.y) + 3.5, v.y); m.castShadow = true; built.add(m); });
  dropGroup = new THREE.Group(); lambGroup = new THREE.Group(); built.add(dropGroup, lambGroup);
  // storm wall
  stormMesh = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 260, 64, 1, true), new THREE.MeshBasicMaterial({ color: 0x9a3ad8, transparent: true, opacity: .28, side: THREE.DoubleSide, depthWrite: false })); built.add(stormMesh);
  fxGroup = new THREE.Group(); built.add(fxGroup);
  built.userData.match = M;
}

// low-poly person built from boxes; colors come from the 2D skins
function makeGuy(o) {
  const g = new THREE.Group(), mat = c => new THREE.MeshStandardMaterial({ color: new THREE.Color(c), roughness: .7, flatShading: true });
  const skin = mat(o.skin || '#c08a5a'), body = mat(o.body || '#888'), legs = mat(o.legs || '#2a2a30'), acc = mat(o.acc || '#222');
  const part = (w, h, d, m, x, y, z) => { const p = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); p.position.set(x, y, z); p.castShadow = true; g.add(p); return p; };
  g.userData.lL = part(1.1, 3, 1.1, legs, -.7, 1.5, 0); g.userData.lR = part(1.1, 3, 1.1, legs, .7, 1.5, 0);
  part(2.8, 3.2, 1.6, body, 0, 4.6, 0);
  g.userData.aL = part(.9, 2.8, .9, body, -1.9, 4.6, 0); g.userData.aR = part(.9, 2.8, .9, body, 1.9, 4.6, 0);
  part(1.8, 1.8, 1.8, skin, 0, 7.1, 0);
  if (o.helmet) { const h = new THREE.Mesh(new THREE.SphereGeometry(1.45, 12, 10), new THREE.MeshStandardMaterial({ color: 0xdff0ff, transparent: true, opacity: .35, roughness: .05, metalness: .2 })); h.position.set(0, 7.2, 0); g.add(h); part(1.6, .6, .3, acc, 0, 7.2, -.95); }
  else part(1.9, .5, 1.9, acc, 0, 8.1, 0);
  if (o.pack) part(2, 2.4, .8, mat(o.pack), 0, 4.8, .9);
  const gun = part(.5, .5, 2.6, mat(o.gun || '#333'), 1.9, 4, -1.2); g.userData.gun = gun;
  g.userData.walk = 0; return g;
}
function guyFor(key, o) { let g = guys.get(key); if (!g) { g = makeGuy(o); guys.set(key, g); scene.add(g); } g.visible = true; return g; }
function poseGuy(g, x, z, face, moving, t, extra = {}) {
  const y = heightAt(x, z) + (extra.jump || 0); const last = g.userData.last || { x, z }; const sp = Math.hypot(x - last.x, z - last.z); g.userData.last = { x, z };
  g.position.set(x, y, z); if (face != null) g.rotation.y = -face - Math.PI / 2;
  const w = (g.userData.walk += sp * .5 + (moving ? .05 : 0)); const sw = Math.min(1, sp * 4) * Math.sin(w * 2.2) * .8;
  g.userData.lL.rotation.x = sw; g.userData.lR.rotation.x = -sw; g.userData.aL.rotation.x = -sw * .8; g.userData.aR.rotation.x = extra.aim ? -1.4 : sw * .8;
  if (extra.down) { g.rotation.z = Math.PI / 2; g.position.y = y + 1; } else g.rotation.z = 0;
}

let lastSize = '';
export function render(mode, w, h, st) {
  S = st || S; const M = S.M; if (!R || !M || !S.mapC) return null;
  if (!built || built.userData.match !== M) buildWorld(M);
  const sz = w + 'x' + h; if (sz !== lastSize) { R.setSize(w, h, false); cam.aspect = w / h; cam.updateProjectionMatrix(); lastSize = sz; }
  const t = performance.now() / 1000, me = M.squad[0];
  // removed buildings
  for (const b of M.buildMeshes || []) { const alive = M.solids.some(s => s.join(',') === b.key); b.box.visible = b.roof.visible = alive; }
  // characters
  guys.forEach(g => g.visible = false);
  const SK = G.mySkin ? G.mySkin() : { suit: '#f4f4f4', visor: '#2d5fa8', pack: '#ff8a2a' };
  M.squad.forEach((a, i) => { if (a.out) return; const g = guyFor('sq' + i + (a.me ? SK.suit : ''), a.me ? { skin: '#a8744a', body: SK.suit, legs: SK.suit, acc: SK.visor, pack: SK.pack, helmet: true, gun: (M.wpn ? M.wpn.c : S.GUNS[M.gun].c) } : { body: a.col, skin: '#e8b890', acc: '#3a2a1a' });
    const face = a.me && M.fps ? M.ang : Math.atan2(a.vy || 0, a.vx || 1);
    poseGuy(g, a.x, a.y, face, true, t, { down: a.down, jump: a.me ? (M.jz || 0) * .6 + (M.fly > 0 ? 6 : 0) : 0, aim: a.me && M.firing });
    if (a.me && M.fps) g.visible = true; });
  M.enemies.forEach((e, i) => { if (e.hidden) return; const sk = e.skin || {}; const g = guyFor('en' + e.name, { body: sk.b, skin: sk.h, acc: sk.a, legs: '#2a2a30' });
    poseGuy(g, e.x, e.y, Math.atan2(me.y - e.y, me.x - e.x), e.state === 'fight', t, { aim: e.state === 'fight' }); g.children.forEach(c => c.material && c.material.emissive && c.material.emissive.setHex(e.flash > 0 ? 0x884444 : 0)); });
  // pickups
  M.chests.forEach(ch => { if (ch.mesh) ch.mesh.visible = !ch.open; });
  while (dropGroup.children.length) dropGroup.remove(dropGroup.children[0]);
  (M.drops || []).forEach(d => { const m = new THREE.Mesh(new THREE.OctahedronGeometry(1.8), new THREE.MeshStandardMaterial({ color: new THREE.Color(d.w.c), emissive: new THREE.Color(d.w.c), emissiveIntensity: .6 })); m.position.set(d.x, heightAt(d.x, d.y) + 3 + Math.sin(t * 3) * .6, d.y); m.rotation.y = t * 2; dropGroup.add(m);
    const beam = new THREE.Mesh(new THREE.CylinderGeometry(.4, .4, 40, 6, 1, true), new THREE.MeshBasicMaterial({ color: new THREE.Color(d.w.c), transparent: true, opacity: .35, depthWrite: false })); beam.position.set(d.x, heightAt(d.x, d.y) + 20, d.y); dropGroup.add(beam); });
  while (lambGroup.children.length) lambGroup.remove(lambGroup.children[0]);
  (M.glambs || []).forEach(gl => { if (gl.taken) return; const m = new THREE.Mesh(new THREE.DodecahedronGeometry(1.4), new THREE.MeshStandardMaterial({ color: 0xffd25a, emissive: 0x6a4a00, metalness: .8, roughness: .25 })); m.position.set(gl.x, heightAt(gl.x, gl.y) + 2 + Math.sin(t * 2 + gl.x) * .5, gl.y); m.rotation.y = t; lambGroup.add(m); });
  // storm
  const sto = M.storm; stormMesh.position.set(sto.cx, 100, sto.cy); stormMesh.scale.set(Math.max(1, sto.r), 1, Math.max(1, sto.r));
  // effects: shots, explosions
  while (fxGroup.children.length) { const c = fxGroup.children[0]; fxGroup.remove(c); c.geometry && c.geometry.dispose(); }
  const pts = [], cols = [];
  for (const f of M.fx) { if ((f.t === 'shot' || f.t === 'laser' || f.t === 'rocket' || f.t === 'bub') && f.x2 != null) { const y1 = heightAt(f.x1, f.y1) + 4.5, y2 = heightAt(f.x2, f.y2) + 4.5; pts.push(f.x1, y1, f.y1, f.x2, y2, f.y2); const c = new THREE.Color(f.c || '#fff36a'); cols.push(c.r, c.g, c.b, c.r, c.g, c.b); }
    if (f.t === 'boom' || f.t === 'ring' || f.t === 'nade') { const k = 1 - f.life / .6, m = new THREE.Mesh(new THREE.SphereGeometry(2 + k * 10, 12, 8), new THREE.MeshBasicMaterial({ color: f.t === 'ring' ? 0xffc878 : 0xff8a3a, transparent: true, opacity: Math.max(0, f.life * 1.4), depthWrite: false })); m.position.set(f.x1, heightAt(f.x1, f.y1) + 3, f.y1); fxGroup.add(m); } }
  if (pts.length) { const gg = new THREE.BufferGeometry(); gg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3)); gg.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3)); fxGroup.add(new THREE.LineSegments(gg, new THREE.LineBasicMaterial({ vertexColors: true }))); }
  // camera
  let tx = me.x, tz = me.y;
  if (mode === 'play') { const a = M.ang || 0, p = (M.pitch || 0) / 60, back = 16, up = 7 - p * 6; const gy = heightAt(me.x, me.y) + (M.jz || 0) * .6;
    cam.position.set(me.x - Math.cos(a) * back + Math.cos(a + Math.PI / 2) * 2.5, gy + up, me.y - Math.sin(a) * back + Math.sin(a + Math.PI / 2) * 2.5);
    const ch = heightAt(cam.position.x, cam.position.z) + 2; if (cam.position.y < ch) cam.position.y = ch;
    cam.lookAt(me.x + Math.cos(a) * 30, gy + 5 + p * 22, me.y + Math.sin(a) * 30); }
  else { const v = M.view3d || {}, tg = v.e || v.p || me; tx = tg.x; tz = tg.y; const a = (v.a0 || 0) + (v.t || 0) * .35, rad = v.style === 'high' ? 40 : v.style === 'low' ? 14 : 24, hgt = v.style === 'high' ? 34 : v.style === 'low' ? 3 : 11;
    const gy = heightAt(tx, tz); cam.position.set(tx + Math.cos(a) * rad, gy + hgt, tz + Math.sin(a) * rad); cam.lookAt(tx, gy + 4, tz); }
  sun.position.set(tx + 120, 220, tz + 60); sun.target.position.set(tx, 0, tz); sun.target.updateMatrixWorld();
  waterMesh.material.color.setHSL(.58, .6, .38 + Math.sin(t * .7) * .015);
  R.render(scene, cam); return R.domElement;
}
G.X3D = { init, render };
