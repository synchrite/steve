// Read-only execution of the owner's house layout, in its default daylight state.
const fs=require('fs');
const source=fs.readFileSync('index.html','utf8');
let fn=source.slice(source.indexOf('function drawHouse(){'),source.indexOf('function drawSimba('));
const rects=[], lines=[];let ox=0,oy=0, path=[];
const HY=150,FLOOR=234,GX=200,HWW=660,VW=660,TH=130,camX=0,run=null;
const performance={now:()=>0};const inMatch=()=>false;
function R(x,y,w,h,c){rects.push([x+ox,y+oy,w,h,c]);}
const b={save(){},restore(){},beginPath(){path=[]},rect(){},clip(){},translate(x,y){ox+=x;oy+=y},moveTo(x,y){path.push([x+ox,y+oy])},lineTo(x,y){path.push([x+ox,y+oy])},stroke(){lines.push(path)}};
eval(fn);drawHouse();
fs.writeFileSync('tools/art/house_layout.json',JSON.stringify({origin:[0,144],rects,lines},null,2));
