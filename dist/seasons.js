export const SEASONS={
 spring:{base:'#283c30',forest:['#304b36','#365740'],ground:['#74905c','#799c64'],road:['#82734f','#8b7c55'],trees:['#405c37','#6c8850','#bd9b9e'],accent:'#e4c4cb',grass:['#aec48188','#48694088'],particle:['#dfb4bd','#a8c87d']},
 summer:{base:'#192b20',forest:['#253e2b','#223726'],ground:['#47643a','#49693c'],road:['#82784d','#8b8055'],trees:['#1a3821','#2a4c2b','#3b6031'],accent:'#76955a',grass:['#79915b88','#263e2588'],particle:['#a4b66a','#90aa65']},
 autumn:{base:'#302b20',forest:['#4b3829','#433226'],ground:['#666b42','#71764b'],road:['#9b8559','#a58e63'],trees:['#754329','#ae6234','#d59443'],accent:'#e8b86a',grass:['#c0a16388','#69533988'],particle:['#ed8651','#b84a32','#f3bf54','#da6970','#d6ac53','#b4ae61']},
 winter:{base:'#26343d',forest:['#8fa8ad','#9ab1b8'],ground:['#d0dbe0','#dbe3e5'],road:['#97896c','#a39579'],trees:['#3b5755','#71908a','#d9e6e5'],accent:'#f3f7f5',grass:['#ffffff88','#9fb3bd88'],particle:['#f4f7f7','#d7e5eb']}
};
export function seasonPalette(value){return SEASONS[value]||SEASONS.summer;}
export const AUTUMN_TREES=[['#713126','#b84a32','#ed8651'],['#795022','#c7832e','#f3bf54'],['#612c37','#9d3d48','#da6970'],['#65502b','#9a7936','#d6ac53'],['#3e5132','#718447','#b4ae61']];
export function treePalette(look,seed){return look==='autumn'?AUTUMN_TREES[Math.floor(seed*AUTUMN_TREES.length)%AUTUMN_TREES.length]:seasonPalette(look).trees;}
export function drawSeasonParticles(c,look,seconds,bounds,screen,scale,enabled=true,reducedMotion=false){
 if(!enabled||reducedMotion)return 0;
 const p=seasonPalette(look),snow=look==='winter',count=snow?60:look==='autumn'?42:18,width=bounds[2]-bounds[0],height=bounds[3]-bounds[1],pixelRatio=c.canvas.width/(c.canvas.clientWidth||c.canvas.width);
 c.save();c.globalAlpha=snow?.68:.72;
 for(let i=0;i<count;i++){
  const seed=(i*7919%997)/997,speed=snow?18+(i%4)*4:12+(i%3)*4,wx=bounds[0]+((seed*width+seconds*speed+Math.sin(seconds*.65+i)*40)%width),wy=bounds[3]-((i*431+seconds*(snow?65:48))%height),pos=screen(wx,wy),r=Math.max((snow?5:7)*scale,(snow?1.4:2.4)*pixelRatio);
  c.fillStyle=p.particle[i%p.particle.length];
  if(snow){c.beginPath();c.arc(pos.x,pos.y,r*(.65+(i%3)*.2),0,Math.PI*2);c.fill();}
  else{c.save();c.translate(pos.x,pos.y);c.rotate(seconds*.55+i);c.beginPath();c.moveTo(-r,0);c.quadraticCurveTo(0,-r*.9,r,0);c.quadraticCurveTo(0,r*.9,-r,0);c.fill();c.strokeStyle='#714523';c.globalAlpha=.45;c.lineWidth=Math.max(.5,pixelRatio*.45);c.beginPath();c.moveTo(-r*.65,0);c.lineTo(r*.7,0);c.stroke();c.restore();}
 }
 c.restore();return count;
}
