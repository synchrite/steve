const fs=require('node:fs'),http=require('node:http'),{spawn}=require('node:child_process'),path=require('node:path');
const root=process.cwd(),out=path.join(root,'tools/ui/preview');fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{const p=path.join(root,decodeURIComponent(req.url.split('?')[0]==='/'?'/index.html':req.url.split('?')[0]));if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return;}fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return;}res.setHeader('Content-Type',p.endsWith('.html')?'text/html':p.endsWith('.png')?'image/png':'application/octet-stream');res.end(b);});});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{await new Promise(r=>server.listen(8124,'127.0.0.1',r));
 const chrome=spawn('C:/Program Files/Google/Chrome/Application/chrome.exe',['--headless=new','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=9337','--user-data-dir='+path.join(out,'chrome-profile'),'about:blank'],{windowsHide:true,stdio:'ignore'});
 let ws;try{let targets;for(let i=0;i<60;i++){try{targets=await (await fetch('http://127.0.0.1:9337/json')).json();break;}catch{await pause(200);}}if(!targets)throw Error('Chrome CDP unavailable');
 ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r));let id=0,pending=new Map(),errors=[];
 ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text+': '+(m.params.exceptionDetails.exception?.description||''));else if(m.method==='Log.entryAdded'&&m.params.entry.level==='error'&&!m.params.entry.url?.includes('fonts.googleapis'))errors.push(m.params.entry.text);});
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 const ev=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result.value;};
 await send('Runtime.enable');await send('Log.enable');await send('Page.enable');await send('Page.navigate',{url:'http://127.0.0.1:8124/'});await pause(1800);
 const results=[];
 for(const [w,h] of [[1280,720],[1920,1080],[800,600],[844,390]]){
  await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:false});await pause(150);
  for(const mode of ['classic','16']){
   await ev(`setGfx('${mode}');startRun(true);fitLayout()`);await pause(350);
   const layout=await ev(`(()=>{const ids=['stage','rcol','phone','cuWrap','rtop'];return {scale:+getComputedStyle(document.documentElement).getPropertyValue('--ui'),skin:document.body.className,rects:Object.fromEntries(ids.map(id=>{const r=$(id).getBoundingClientRect();return [id,{x:r.x,y:r.y,w:r.width,h:r.height}]}))}})()`);
   for(const [name,r] of Object.entries(layout.rects)){if(r.x<-.5||r.y<-.5||r.x+r.w>w+.5||r.y+r.h>h+.5)throw Error(`Out of viewport ${w}x${h} ${name}: ${JSON.stringify(r)}`);}
   if(Math.abs(layout.rects.stage.h/720-layout.scale)>.005)throw Error('Canvas scale differs');
   const snap=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,`${w}x${h}-${mode}.png`),Buffer.from(snap.data,'base64'));
   results.push({w,h,mode,...layout});
  }
 }
 const interactions=await ev(`(()=>{
  const assert=(v,m)=>{if(!v)throw Error(m)};
  view={type:'contacts'};renderPhone();let log=$('screen').querySelector('.log');log.scrollTop=45;const before=log.scrollTop;renderPhone();assert($('screen').querySelector('.log').scrollTop===before,'contacts scroll');
  view=null;run.inbox=Array.from({length:24},(_,i)=>({id:1000+i,kind:'vm',from:'Test '+i,msg:'A test message',icon:'*'}));renderPhone();$('screen').scrollTop=120;renderPhone();assert($('screen').scrollTop===120,'inbox scroll');
  UI.pz=true;const ph=$('phone');ph.dispatchEvent(new PointerEvent('pointerenter',{pointerType:'mouse'}));assert(ph.classList.contains('zoomed'),'zoom enters');ph.dispatchEvent(new PointerEvent('pointerleave',{pointerType:'mouse'}));assert(ph.classList.contains('zoomed'),'zoom remains');document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));assert(!ph.classList.contains('zoomed'),'outside closes');
  ph.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerType:'touch',clientX:10,clientY:10}));ph.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerType:'touch',clientX:10,clientY:70}));assert(!ph.classList.contains('zoomed'),'scroll does not zoom');
  tipsBtn.click();assert(UI.tips&&!tipsPage.hidden&&mode==='pause','tips on and pause');assert(JSON.parse(localStorage.steveUI).tips===true,'tips persisted');assert(tipsPage.querySelectorAll('.tipCard').length===12,'12 cards');closeTips();assert(mode==='play','tips resumes');tipsBtn.click();assert(!UI.tips,'tips off');
  return 'scroll, stable zoom, outside dismissal, swipe, tips persistence, cards, pause/resume passed';
 })()`);
 await pause(500);if(errors.length)throw Error(errors.join('\n'));
 fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({results,interactions,errors},null,2));console.log(interactions);console.log('Both modes started without console errors; all four viewport bounds and shared scale passed.');
 }finally{ws?.close();chrome.kill();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;server.close();});
