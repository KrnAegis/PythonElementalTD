import {COLORS} from './engine.js';
// Three original golem silhouettes for each element, with articulated gait.
export function drawElementGolem(c,e,dir,frame){const tier=Math.max(1,Math.min(3,e.tier||1)),color=COLORS[e.element],dark={fire:'#663027',water:'#23475e',nature:'#30492b',earth:'#67533c',light:'#84763d',darkness:'#302546'}[e.element],bright={fire:'#ffe194',water:'#c7f6ff',nature:'#d0ed94',earth:'#efd1a1',light:'#fffbc9',darkness:'#dfbbff'}[e.element],step=Math.sin(frame*Math.PI/4),back=dir==='north',side=dir==='east'||dir==='west',w=12+tier*6,headY=15-tier*2-Math.abs(step),bodyY=headY+10;c.save();if(dir==='west'){c.translate(48,0);c.scale(-1,1);}const rect=(x,y,w,h,col)=>{c.fillStyle=col;c.fillRect(Math.round(x),Math.round(y),w,h);},poly=(points,col)=>{c.fillStyle=col;c.beginPath();points.forEach(([x,y],i)=>i?c.lineTo(Math.round(x),Math.round(y)):c.moveTo(Math.round(x),Math.round(y)));c.closePath();c.fill();},joint=(x,y,tx,ty,width)=>{poly([[x-width/2,y],[x+width/2,y],[tx+width/2,ty],[tx-width/2,ty]],'#142020');rect(tx-width/2+1,ty-3,width-2,6,dark);};
 joint(19,33,18+step*2,40,5+tier);joint(29,33,30-step*2,40,5+tier);rect(13+step*2,40,9,4,dark);rect(27-step*2,40,9,4,dark);
 rect(24-w/2-1,bodyY-1,w+2,15,'#152223');rect(24-w/2,bodyY,w,13,dark);rect(25-w/2,bodyY+1,w-2,4,color);rect(25-w/2,bodyY+5,4,7,color);
 const armY=bodyY+3;for(const sign of [-1,1]){const x=24+sign*(w/2+2);joint(x,armY,x+sign*2,armY+10+sign*step*3,5+tier);rect(x-3-tier/2,armY+7+sign*step*3,6+tier,7,dark);rect(x-2,armY+7+sign*step*3,4+tier,2,color);}
 rect(17,headY,14,10,'#132027');rect(18,headY+1,12,8,dark);rect(19,headY+1,10,2,color);if(!back){rect(side?25:20,headY+4,side?3:3,2,bright);if(!side)rect(26,headY+4,3,2,bright);rect(22,headY+8,5,1,bright);}
 if(!back){poly([[24,bodyY+3],[28,bodyY+7],[24,bodyY+11],[20,bodyY+7]],color);rect(23,bodyY+5,2,4,bright);}else rect(22,bodyY+3,4,8,color);
 if(tier>=2){for(const sign of [-1,1]){const x=24+sign*w/2;poly([[x-sign*7,bodyY+2],[x+sign*3,bodyY-5],[x+sign*6,bodyY+5]],color);}rect(18,headY-2,12,3,color);}
 if(tier===3){for(const sign of [-1,1]){poly([[24+sign*7,headY+1],[24+sign*12,headY-7],[24+sign*11,headY+6]],bright);rect(24+sign*13-2,bodyY-3,4,5,bright);}rect(22,headY-5,4,4,color);}
 if(e.element==='fire'){for(let i=0;i<tier+1;i++){const x=18+i*5,y=bodyY-2;poly([[x-2,y],[x+Math.sin(frame+i)*2,y-4-tier*2],[x+2,y]],i%2?bright:color);}rect(18,bodyY+10,2,4,bright);}
 if(e.element==='water'){poly([[17,bodyY+9],[20,bodyY+4],[22,bodyY+9]],bright);rect(29,bodyY+7,2,6,color);}
 if(e.element==='nature'){for(const sign of [-1,1])poly([[24+sign*8,headY],[24+sign*(11+tier),headY-4-tier],[24+sign*6,headY-1]],color);rect(21,bodyY+9,2,6,bright);}
 if(e.element==='earth'){rect(16,bodyY+4,3,4,bright);rect(28,bodyY+9,4,3,color);if(tier===3)rect(12,bodyY-4,4,7,bright);}
 if(e.element==='light'){rect(16,headY-5,16,1,bright);rect(14,headY-4,2,3,color);rect(32,headY-4,2,3,color);if(tier===3){poly([[7,bodyY],[2,bodyY-8],[4,bodyY+6],[10,bodyY+9]],bright);poly([[41,bodyY],[46,bodyY-8],[44,bodyY+6],[38,bodyY+9]],bright);}}
 if(e.element==='darkness'){rect(19,bodyY+8,2,3,bright);rect(27,bodyY+5,2,3,color);if(tier===3)poly([[20,headY-3],[24,headY-9],[28,headY-3]],color);}
 c.restore();}
