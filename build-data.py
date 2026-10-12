import pathlib,json,re,struct,heapq,math,sys
src=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path('/workspace/element-td-data/recreation');out=pathlib.Path(__file__).parent/'dist/data';out.mkdir(parents=True,exist_ok=True)
towers=json.loads((src/'towers.json').read_text());abilities=json.loads((src/'abilities-all.json').read_text());rules=json.loads((src/'game-rules.json').read_text());arrays=json.loads((src/'constant-array-assignments.json').read_text());units=json.loads((src/'units-all.json').read_text());layout=json.loads((src/'layout.json').read_text());index=json.loads((src/'rawcode-function-index.json').read_text())
research={'R000':'water','R001':'darkness','R002':'earth','R003':'fire','R004':'light','R005':'nature'}
def num(v,default=0):
 try:return float(v)
 except:return default
families={'h000':'clone','h01K':'clone','h030':'clone','h002':'helix','h00Y':'helix','h02X':'helix','h003':'chain','h01L':'chain','h02U':'chain','h004':'quark','h00R':'quark','h02Y':'quark','h005':'life','h00V':'life','h02W':'life','h006':'magic','h01I':'magic','h034':'magic','h007':'bomb','h00T':'bomb','h032':'bomb','h008':'smith','h011':'smith','h031':'smith','h009':'poison','h01J':'poison','h036':'poison','h00A':'vapor','h01G':'vapor','h035':'vapor','h00B':'hydro','h00O':'hydro','h02Z':'hydro','h00C':'disease','h00P':'disease','h02T':'disease','h00D':'flame','h01F':'flame','h033':'flame','h00E':'boomerang','h01M':'boomerang','h02V':'boomerang','h00F':'well','h01H':'well','h02S':'well','h00N':'zealot','h02M':'zealot','h00Q':'quaker','h02I':'quaker','h00U':'laser','h02N':'laser','h00W':'oblivion','h029':'oblivion','h00X':'polar','h02R':'polar','h00Z':'drowning','h02B':'drowning','h010':'orbit','h02J':'orbit','h012':'napalm','h02F':'napalm','h013':'voodoo','h02D':'voodoo','h014':'muck','h02P':'muck','h015':'corrosion','h02H':'corrosion','h017':'roots','h02E':'roots','h018':'nova','h02L':'nova','h019':'gold','h02Q':'gold','h01A':'storm','h02O':'storm','h01B':'hail','h02A':'hail','h01C':'tidal','h02G':'tidal','h01D':'enchant','h02K':'enchant','h01E':'impulse','h02C':'impulse','n01C':'golem','n021':'golem'}
parsed=[]
for t in towers:
 w,b,tip=t['weapon_data'],t['balance_data'],t['tooltip'];req={research[x]:int(num(t['requirement_levels_raw'].split(',')[i] if i<len(t['requirement_levels_raw'].split(',')) else 1,1)) for i,x in enumerate(t['requirements_raw'].split(',')) if x in research}
 element=tip['Type'].lower();element=element if element in list(research.values())+['composite'] else 'composite'
 dice=num(w.get('dice1'));sides=num(w.get('sides1'));bonus=num(w.get('dmgplus1'));damage=bonus+dice*(sides+1)/2
 tooltip_damage=num(tip['Damage'],damage)
 if tooltip_damage>0:damage=tooltip_damage
 tier=max(req.values(),default=1)
 if t['name'].startswith('Amplified'):tier=1
 parsed.append({'id':t['id'],'name':t['name'],'requirements':req,'elements':[re.sub(r' \d+$','',x).lower() for x in t['elements']],'element':element,'cost':int(num(t['gold_cost'])),'lumber':int(num(t['lumber_cost'])),'investment':num(b.get('HP')),'essence':int(num(b.get('fused'))),'range':num(w.get('rangeN1'),num(tip['Range'],700)),'interval':num(w.get('cool1'),num(tip['Speed'],1)),'damage':damage,'displayDamage':tip['Damage'],'moveSpeed':num(b.get('spd'),300),'nativeAttack':w.get('atkType1',''),'splash':{'full':num(w.get('Farea1')),'half':num(w.get('Harea1')),'quarter':num(w.get('Qarea1')),'halfFactor':num(w.get('Hfact1'),.5),'quarterFactor':num(w.get('Qfact1'),.25)},'family':families.get(t['id'],'basic'),'tier':tier,'ability':tip['Ability'],'upgrades':[x['id'] for x in t['upgrade_options']],'abilities':t['abilities_raw'].get('abilList','').split(','),'source':'Element TD Survivor 4.3b: '+t['id']})
byid={x['id']:x for x in parsed}
# Infer element association for prerequisite-free amplified upgrades from their incoming parent.
for t in parsed:
 if not t['elements']:
  parents=[v for v in parsed if t['id'] in v['upgrades']]
  if parents and parents[0]['elements']:t['elements']=parents[0]['elements'][:]
# Prepare exact pathing grid crop and a clearance-aware route for each original player region.
meta=json.loads((src/'pathing-metadata.json').read_text());raw=(src/'pathing-flags.bin').read_bytes();W,H=meta['width'],meta['height'];ox,oy=layout['world_origin'];regions=['RU','NU','AU','DU','IU','CU','OU','BU'];lanes=[]
for i,player in enumerate(layout['players']):
 bounds=layout['script_rectangles'][regions[i]];x0=max(0,int((bounds[0]-ox)/32));y0=max(0,int((bounds[1]-oy)/32));x1=min(W,int((bounds[2]-ox)/32));y1=min(H,int((bounds[3]-oy)/32));width,height=x1-x0,y1-y0;grid=[raw[y*W+x] for y in range(y0,y1) for x in range(x0,x1)]
 def cell(pt):return (min(width-1,max(0,int((pt[0]-ox)/32)-x0)),min(height-1,max(0,int((pt[1]-oy)/32)-y0)))
 start,goal=cell(player['spawn']),cell(player['exit']);heap=[(0,0,start)];dist={start:0};prev={};found=False
 while heap:
  _,cost,(x,y)=heapq.heappop(heap)
  if cost>dist.get((x,y),1e20):continue
  if (x,y)==goal:found=True;break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   xx,yy=x+dx,y+dy
   if not(0<=xx<width and 0<=yy<height) or grid[yy*width+xx]&2:continue
   # Prefer the center of the original corridors to approximate native collision clearance.
   blocked=sum(1 for a,b in [(xx+1,yy),(xx-1,yy),(xx,yy+1),(xx,yy-1)] if not(0<=a<width and 0<=b<height) or grid[b*width+a]&2)
   new=cost+1+blocked*2
   if new<dist.get((xx,yy),1e20):dist[xx,yy]=new;prev[xx,yy]=(x,y);heapq.heappush(heap,(new+abs(xx-goal[0])+abs(yy-goal[1]),new,(xx,yy)))
 assert found,(i,start,goal)
 path=[goal]
 while path[-1]!=start:path.append(prev[path[-1]])
 path.reverse();simple=[]
 for j,c in enumerate(path):
  if j==0 or j==len(path)-1 or (c[0]-path[j-1][0],c[1]-path[j-1][1])!=(path[j+1][0]-c[0],path[j+1][1]-c[1]):simple.append([ox+(x0+c[0]+.5)*32,oy+(y0+c[1]+.5)*32])
 lanes.append({'bounds':bounds,'origin':[ox+x0*32,oy+y0*32],'width':width,'height':height,'grid':grid,'path':simple,'spawn':player['spawn'],'exit':player['exit']});print('Lane',i+1,'path cells',len(path),'turns',len(simple))
def literal_array(name):return {v['index']:v.get('literal_value') for v in arrays[name] if 'literal_value' in v}
enemies=json.loads((src/'enemies.json').read_text())
for e in enemies:
 e['element']=e['element'].lower();e['armor']=num(e['object_armor']);e['speed']=num(e['object_move_speed'],300)
boss=json.loads((src/'bosses-and-ronald.json').read_text());bosses=[]
for e in boss['element_bosses']:
 u=e['unit_record'];element=['darkness','earth','fire','light','nature','water'][e['slot']%6]
 bosses.append({'id':e['id'],'element':element,'tier':e['tier'],'name':u.get('strings',{}).get('Name',e['id']),'speed':num(u.get('UnitBalance',{}).get('spd'),300),'hp':literal_array(e['hp_array'])})
result={'version':'4.3b','sourceSha256':json.loads((src/'provenance.json').read_text())['source_sha256'],'towers':parsed,'waves':enemies,'lanes':lanes,'bosses':bosses,'ronald':{'hp':literal_array('Y'),'speed':literal_array('Z'),'thresholds':boss['ronald']['upgrade_thresholds']},'essenceHP':literal_array('XV'),'damageMatrix':{k.lower():{kk.lower():vv for kk,vv in v.items()} for k,v in json.loads((src/'damage-matrix.json').read_text())['elemental_multipliers'].items()},'difficulty':rules['difficulty'],'bountyGrowth':rules['kill_bounty']['growth_bases'],'delays':rules['interwave_delays']['seconds_by_difficulty']}
(out/'game.json').write_text(json.dumps(result,separators=(',',':')))
# Reference is shipped separately so all displayed original stats and source facts remain inspectable.
(out/'tower-reference.json').write_text(json.dumps(towers,separators=(',',':')))
print('Wrote',len(parsed),'defenses,',len(enemies),'waves,',len(bosses),'bosses')
