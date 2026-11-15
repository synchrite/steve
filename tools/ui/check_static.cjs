const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('index.html','utf8'),script=source.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);fs.writeFileSync('tools/ui/preview/extracted-script.js',script);console.log('Extracted script parses (also run node --check tools/ui/preview/extracted-script.js).');
const scrollSource=script.slice(script.indexOf('const phoneScroll=new Map()'),script.indexOf('function paintPhone()'));
const screen={scrollTop:0,log:null,querySelector(){return this.log;}};
const ctx={run:{},view:null,$:()=>screen,paintPhone(){screen.scrollTop=0;screen.log=ctx.view?{scrollTop:999,scrollHeight:1000,clientHeight:200}:null;}};
vm.createContext(ctx);vm.runInContext(scrollSource,ctx);
ctx.renderPhone();screen.scrollTop=140;ctx.renderPhone();assert.equal(screen.scrollTop,140);
ctx.view={type:'contacts'};ctx.renderPhone();assert.equal(screen.log.scrollTop,0);screen.log.scrollTop=45;ctx.renderPhone();assert.equal(screen.log.scrollTop,45);
ctx.view={type:'thread',item:{id:1}};ctx.renderPhone();assert.equal(screen.log.scrollTop,1000);screen.log.scrollTop=120;ctx.renderPhone();assert.equal(screen.log.scrollTop,120);
screen.log.scrollTop=800;ctx.renderPhone();assert.equal(screen.log.scrollTop,1000);
ctx.view=null;ctx.renderPhone();assert.equal(screen.scrollTop,140);
console.log('Inbox, independent views, conversation scroll and bottom-follow pass.');
const scaleSource=script.slice(script.indexOf('function scaleUI(){'),script.indexOf("addEventListener('resize',scaleUI)"));
for(const [w,h] of [[1280,720],[1920,1080],[800,600],[844,390]])for(const canvasWidth of [960,1440]){
 let props={};const c={document:{body:{classList:{toggle(){}}},documentElement:{style:{setProperty(k,v){props[k]=v;}}}},matchMedia:()=>({matches:false}),winW:()=>w,winH:()=>h,cv:{width:canvasWidth},fitTXK(){}};vm.createContext(c);vm.runInContext(scaleSource,c);c.scaleUI();
 const k=props['--ui'];assert((canvasWidth+360)*k<=w-17.9);assert(720*k<=h-11.9);assert.equal(props['--game-w'],canvasWidth);
}
const assets=[...script.matchAll(/\['(tv|combos|pickaxe|shop|phone|pizza|skills|bills|simba|house|stats|graphics)','/g)].map(m=>m[1]);assert.equal(new Set(assets).size,12);
for(const name of new Set(assets))assert(fs.existsSync(`assets/ui/tips/${name}.png`));
console.log('Shared scale math fits all four viewports, both canvas aspects; all 12 card PNGs exist.');
console.log('Browser layout/console checks require running check_pda.cjs on a machine permitting Chrome IPC.');
