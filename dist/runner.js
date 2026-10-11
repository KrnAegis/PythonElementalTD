// Dedicated worker. Messages contain snapshots, never direct game references.
self.onmessage = ({data}) => {
 const actions = [], logs = [];
 const {code, state, mode} = data;
 try {
  const fn = new Function('gold','wave','towers','enemies','build','upgrade','sell','attack','distance','log', '"use strict";\n' + code);
  fn(state.gold,state.wave,state.towers,state.enemies,
   (element,pad)=>actions.push({type:'build',element,pad}),
   (pad,element)=>actions.push({type:'upgrade',pad,element}),
   pad=>actions.push({type:'sell',pad}),
   (tower,enemy)=>actions.push({type:'attack',tower,enemy}),
   (a,b)=>Math.hypot(a.x-b.x,a.y-b.y),
   (...args)=>{if(logs.length<20) logs.push(args.map(a=>typeof a==='object'?JSON.stringify(a):String(a)).join(' '));});
  postMessage({actions:actions.slice(0,200),logs,mode});
 } catch(error) {postMessage({error:error.message,mode});}
};
