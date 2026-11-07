const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const directory = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(directory, 'burndown.html'), 'utf8');
const model = html.match(/<script id="burndown-model">([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({});
vm.runInContext(model, context);
const build = (history, sprint = 'A', done = 'Done', issueSprint = sprint, type = 'all') => context.buildBurndown(history, sprint, done, issueSprint, type);
const { readHistory, historyFiles, appendSnapshot, sprintForDate, issueType, SPRINTS } = require('../history-files.js');
const issue = (id, status = 'Ready', sprint = 'A') => ({ id, status, sprint });
const snapshot = (day, issues) => ({ date: day.includes('T') ? day + 'T12:00:00Z' : day + 'T12:00:00Z', issues });
const row = (rows, date) => rows.find(row => row.date === date);

test('presets use confirmed dates, including the year boundary', () => {
  assert.deepEqual(JSON.parse(JSON.stringify(context.periodFor('A'))), {start:'2026-10-10',end:'2026-10-31'});
  assert.deepEqual(JSON.parse(JSON.stringify(context.periodFor('B'))), {start:'2026-11-01',end:'2026-12-05'});
  const rows=build([snapshot('2026-12-06',[issue(1,'Ready','C')]),snapshot('2027-01-03',[issue(1,'Done','C')])],'C');
  assert.equal(rows.length,29);assert.equal(rows.at(-1).remaining,0);assert.equal(rows.at(-1).ideal,0);
});
test('selected sprint includes the latest collected snapshot after its scheduled end', () => {
  const rows = build([snapshot('2026-10-31', [issue(1, 'Ready', 'A'), issue(2, 'Ready', 'A')]), snapshot('2026-11-01', [issue(1, 'Done', 'A')])]);
  assert.equal(rows.at(-1).date, '2026-11-01');
  assert.equal(rows.at(-1).remaining, 0);
});
test('full calendar can filter by one sprint', () => {
  const rows = build([snapshot('2026-10-10', [issue(1, 'Ready', 'A'), issue(2, 'Ready', 'B')]), snapshot('2026-11-01', [issue(1, 'Done', 'A'), issue(2, 'Ready', 'B')])], 'all', 'Done', 'A');
  assert.equal(rows.length, 86);
  const latest = rows.find(row => row.date === '2026-11-01');
  assert.equal(latest.remaining, 0);
  assert.equal(latest.scope, 1);
});
test('sprint filtering accepts A and Sprint A, while all includes unassigned issues', () => {
  const history=[snapshot('2026-10-10',[issue(1),issue(2,'Done',' sprint a '),issue(3,'Ready','B'),issue(4,'Ready',null)])];
  const filtered=build(history)[0];assert.equal(filtered.scope,2);assert.equal(filtered.done,1);assert.equal(filtered.remaining,1);
  assert.equal(build(history,'all')[0].scope,4);
});
test('daily scope reflects additions and transfers separately from completion', () => {
  const rows=build([snapshot('2026-10-10',[issue(1)]),snapshot('2026-10-11',[issue(1),issue(2)]),snapshot('2026-10-12',[issue(1,'Ready','B'),issue(2)])]);
  assert.equal(rows[0].scope,1);assert.equal(rows[1].scope,2);assert.equal(rows[2].scope,1);assert.equal(rows[2].done,0);
  assert.ok(rows[2].ideal<1); // Scope additions do not reset the reference line.
});
test('latest daily snapshot wins, reopened work increases remaining', () => {
  const rows=build([{date:'2026-10-10T08:00:00Z',issues:[issue(1)]},{date:'2026-10-10T18:00:00Z',issues:[issue(1,'Done')]},snapshot('2026-10-11',[issue(1)])]);
  assert.equal(rows[0].remaining,0);assert.equal(rows[1].remaining,1);assert.equal(rows[2].remaining,null);
});
test('legacy sprint membership is a gap, not zero or an inferred assignment', () => {
  const history=[snapshot('2026-10-10',[{id:1,status:'Done'}])];
  assert.equal(build(history)[0].remaining,null);assert.match(build(history)[0].quality,/not recorded/);
  assert.equal(build(history,'all')[0].remaining,0);
});
test('unassigned issues give a known empty sprint; duplicates and unknown statuses give gaps', () => {
  assert.equal(build([snapshot('2026-10-10',[issue(1,'Done',null)])])[0].scope,0);
  assert.equal(build([snapshot('2026-10-10',[issue(1),issue(1)])])[0].remaining,null);
  assert.equal(build([snapshot('2026-10-10',[issue(1,'Unknown')])])[0].remaining,null);
});
test('late reference starts at first non-empty observation and does not decrease over weekends', () => {
  const rows=build([snapshot('2026-10-15',[issue(1)])]);
  assert.equal(rows[0].ideal,null);assert.equal(row(rows,'2026-10-15').ideal,1);
  assert.equal(row(rows,'2026-10-16').ideal,row(rows,'2026-10-18').ideal);assert.equal(rows.at(-1).ideal,0);
  assert.equal(build([snapshot('2026-10-31',[issue(1)])]).at(-1).ideal,null);
});
test('completed status is case insensitive and validates input', () => {
  assert.equal(build([snapshot('2026-10-10',[issue(1,' CLOSED ')])],'A','Closed')[0].done,1);
  assert.throws(()=>build([], 'A'),/non-empty/);
  assert.throws(()=>build([snapshot('2026-10-10',[{id:1,status:'Ready',sprint:7}])]),/string or null/);
});

async function collect({fail=false}={}) {
  const source=fs.readFileSync(path.join(directory,'snapshot.js'),'utf8').replace(/main\(\)\.catch\([\s\S]*$/, '');
  const writes=new Map(), queries=[];
  const item=(id,sprint,labels=['Story','frontend'],repository='Phenriquerafael/LABDSOF_G9A')=>({content:{__typename:'Issue',number:id,title:'Issue '+id,repository:{nameWithOwner:repository},labels:{nodes:labels.map(name=>({name})),pageInfo:{hasNextPage:false}}},status:{name:'Ready'},sprint});
  const responses=[{user:{projectV2:{id:'p9',number:9,title:'Project'}}},{node:{items:{nodes:[item(1,{name:'Sprint A'}),item(2,{title:'B'}),item(99,{name:'C'},['Task'],'other/repo')],pageInfo:{hasNextPage:true,endCursor:'next'}}}},{node:{items:{nodes:[item(3,{text:' C '},['Sub-Task']),item(4,null,[])],pageInfo:{hasNextPage:false}}}}];
  // Only the sprint file for today's collection exists, holding one older snapshot.
  const existingDay=new Date().toISOString().slice(0,10);
  const existing=historyFiles().find(file=>file.key===sprintForDate(existingDay+'T12:00:00Z')).file;
  const fakeFs={existsSync:file=>file===existing,readFileSync:()=>JSON.stringify([{date:existingDay+'T00:00:00.000Z',issues:[{id:1,status:'Ready'}]}]),mkdirSync:()=>{},writeFileSync:(file,text)=>writes.set(file,JSON.parse(text)),renameSync:(a,b)=>{writes.set(b,writes.get(a));writes.delete(a);}};
  let calls=0;
  const ctx=vm.createContext({require:name=>name==='node:fs'?fakeFs:require(name.startsWith('./')?path.join(directory,name):name),__dirname:directory,process:{env:{GITHUB_TOKEN:'mock'},pid:42},console:{log(){},warn(){}},AbortSignal,fetch:async(url,options)=>{
    queries.push(JSON.parse(options.body));
    if(fail && calls===2) return {ok:false,status:403};
    return {ok:true,json:async()=>({data:responses[calls++]})};
  }});
  vm.runInContext(source,ctx);
  if(fail) { await assert.rejects(vm.runInContext('main()',ctx),/403/);assert.equal(writes.size,0);return; }
  await vm.runInContext('main()',ctx);
  return {writes,queries};
}
test('collector preserves per-issue sprint in history and raw across pages and field types',async()=>{
  const {writes,queries}=await collect();
  const [historyFile,history]=[...writes].find(([file])=>/history-sprint-[abc]\.json$/.test(file));
  assert.equal(path.basename(historyFile),`history-sprint-${sprintForDate(history[1].date).toLowerCase()}.json`);
  assert.equal(history.length,2);assert.equal(history[0].issues[0].sprint,undefined);assert.equal(history[0].issues[0].labels,undefined);
  assert.deepEqual(history[1].issues.map(item=>item.sprint),['Sprint A','B','C',null]);
  assert.deepEqual(history[1].issues.map(item=>item.labels),[['frontend','Story'],['frontend','Story'],['Sub-Task'],[]]);
  const [filename,raw]=[...writes].find(([file])=>file.includes(path.sep+'raw'+path.sep));
  const items=raw.data.repository.projectsV2.nodes[0].items.nodes;
  assert.deepEqual(items.map(item=>item.sprint),['Sprint A','B','C',null]);
  assert.deepEqual(items[2].labels,['Sub-Task']);
  assert.match(queries[1].query,/labels\(first: 100\)/);
  assert.deepEqual(items[0].fieldValues.nodes[1],{name:'Sprint A',field:{name:'Sprint'}});
  assert.equal(items[3].fieldValues.nodes.length,1);
  assert.equal(raw.date,history[1].date);assert.equal(path.basename(filename),raw.date.replace(/:/g,'-')+'-42.json');
  assert.equal(queries[1].variables.sprintField,'Sprint');assert.equal(queries[2].variables.after,'next');
  assert.match(queries[1].query,/ProjectV2ItemFieldIterationValue/);
});
test('API failures preserve history and avoid partial raw exports',async()=>{await collect({fail:true});});

test('page loads local JSON, filters automatically and keeps tables/CSV without Chart.js',async()=>{
  const elements=new Map();
  function element() {return {value:'',files:[],children:[],listeners:{},textContent:'',className:'',disabled:false,append(child){this.children.push(child);},replaceChildren(){this.children=[];},addEventListener(name,fn){this.listeners[name]=fn;},remove(){},click(){}};}
  const get=id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id);};
  get('sprint').value='all';get('done-status').value='Done';get('history-url').value='./data/history.json';
  const ctx=vm.createContext({document:{getElementById:get,createElement:element,body:element()},location:{protocol:'file:'},console});
  for(const script of html.matchAll(/<script(?: id="burndown-model")?>([\s\S]*?)<\/script>/g))vm.runInContext(script[1],ctx);
  assert.match(get('message').textContent,/Choose your/);
  get('history-file').files=[{text:async()=>JSON.stringify([snapshot('2026-10-10',[issue(1),issue(2,'Done','B'),issue(3,'Custom done',null)])])}];
  await get('history-file').listeners.change();
  assert.equal(get('issue-rows').children.length,3);assert.equal(get('export').disabled,false);assert.match(get('message').textContent,/Chart.js could not load/);
  assert.ok(get('done-status').children.some(option=>option.value==='Custom done'));
  get('sprint').value='A';get('sprint').listeners.change();
  assert.equal(get('issue-rows').children.length,1);assert.equal(get('rows').children.length,86);
  get('history-file').files=[{text:async()=>'{invalid'}];await get('history-file').listeners.change();
  assert.equal(get('message').className,'error');assert.equal(get('export').disabled,true);assert.equal(get('issue-rows').children.length,0);
});
test('CFD filters issue sprint assignments independently of dates and preserves unknown-data gaps', () => {
  const cfd=fs.readFileSync(path.join(directory,'chart.html'),'utf8');
  const script=cfd.match(/<script>([\s\S]*?)<\/script>/)[1];
  const elements=new Map();
  const get=id=>{if(!elements.has(id))elements.set(id,{value:id==='sprint'?'all':'',textContent:'',className:'',addEventListener(){}});return elements.get(id);};
  const charts=[];
  const ctx=vm.createContext({document:{getElementById:get},location:{protocol:'file:'},Chart:function(canvas,config){charts.push(config);this.destroy=()=>{};}});
  vm.runInContext(script.replace(/main\(\);\s*$/, ''),ctx);
  const history=[
    {date:'2026-12-15T12:00:00Z',issues:[{id:1,status:'Done',sprint:' sprint a '},{id:2,status:'Ready',sprint:'B'},{id:3,status:'Ready',sprint:null}]},
    {date:'2026-12-16T12:00:00Z',issues:[{id:1,status:'Done'}]},
    {date:'2026-12-17T12:00:00Z',Ready:3},
    {date:'2026-12-18T12:00:00Z',issues:[{id:2,status:'Ready',sprint:'B'}]}
  ];
  const filtered=ctx.filterSprint(history,'A');
  assert.equal(filtered[0].issues.length,1);assert.equal(filtered[0].issues[0].id,1);
  assert.equal(ctx.countByStatus(filtered[1],'Done'),null);
  assert.equal(ctx.countByStatus(filtered[2],'Ready'),null);
  assert.equal(ctx.countByStatus(filtered[3],'Ready'),0);
  assert.equal(ctx.filterSprint(history,'all')[0].issues.length,3);
  assert.equal(history[0].issues.length,3);
  ctx.testHistory=history;vm.runInContext('loadedHistory = testHistory',ctx);
  get('sprint').value='A';ctx.render();
  assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Done').data),[1,null,null,0]);
  get('sprint').value='B';ctx.render();
  assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Ready').data),[1,null,null,1]);
  get('sprint').value='all';ctx.render();
  assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Ready').data),[2,0,3,1]);
});
test('Sprint B reconstructed baseline shows 13 Backlog issues on November 1 and 2 with explicit provenance',()=>{
 const history=readHistory();
 const affected=history.filter(s=>/^2026-11-0[12]/.test(s.date));
 assert.equal(affected.length,5);
 for(const snapshot of affected){
  const issues=snapshot.issues.filter(i=>i.sprint==='Sprint B');
  assert.equal(issues.length,13);assert.ok(issues.every(i=>i.status==='Backlog'));
  assert.equal(new Set(snapshot.issues.map(i=>i.id)).size,snapshot.issues.length);
  assert.equal(snapshot.reconstruction.kind,'planned-scope');
 }
 const rows=build(history,'B');
 for(const date of ['2026-11-01','2026-11-02']){
  const day=row(rows,date);assert.equal(day.scope,13);assert.equal(day.remaining,13);assert.equal(day.done,0);
  assert.equal(day.reconstructed,true);assert.match(day.quality,/not observed/);
 }
 assert.match(row(rows,'2026-11-02').quality,/synthetic day/);
 const raw=JSON.parse(fs.readFileSync(path.join(directory,'data/raw/2026-11-01T21-47-09.987Z-2388.json'),'utf8'));
 assert.equal(raw.data.repository.projectsV2.nodes[0].items.nodes.filter(i=>i.sprint==='Sprint B').length,6);
});
test('history is split into one file per sprint by UTC snapshot day, and files stay in their sprint',()=>{
 assert.equal(sprintForDate('2026-10-01T10:00:00Z'),'A');assert.equal(sprintForDate('2026-10-31T23:59:59Z'),'A');
 assert.equal(sprintForDate('2026-11-01T00:00:00Z'),'B');assert.equal(sprintForDate('2026-12-06T00:00:00Z'),'C');assert.equal(sprintForDate('2027-02-01T00:00:00Z'),'C');
 for(const key of Object.keys(SPRINTS)) assert.ok(html.includes(SPRINTS[key].start)&&html.includes(SPRINTS[key].end));
 const files={};const fakeFs={existsSync:file=>file in files,readFileSync:file=>files[file],mkdirSync(){},writeFileSync:(file,text)=>{files[file]=text;},renameSync:(a,b)=>{files[b]=files[a];delete files[a];}};
 const dir=path.join(directory,'tmp-test');
 appendSnapshot({date:'2026-11-02T00:00:00Z',issues:[]},{directory:dir,fsImpl:fakeFs,runId:'x'});
 appendSnapshot({date:'2026-10-30T00:00:00Z',issues:[]},{directory:dir,fsImpl:fakeFs,runId:'x'});
 assert.deepEqual(Object.keys(files).map(f=>path.basename(f)).sort(),['history-sprint-a.json','history-sprint-b.json']);
 assert.deepEqual(readHistory({directory:dir,fsImpl:fakeFs}).map(s=>s.date),['2026-10-30T00:00:00Z','2026-11-02T00:00:00Z']);
 files[path.join(dir,'history-sprint-c.json')]=JSON.stringify([{date:'2026-11-03T00:00:00Z',issues:[]}]);
 assert.throws(()=>readHistory({directory:dir,fsImpl:fakeFs}),/belongs to Sprint B/);
 const stored=readHistory();
 for(const {key,file} of historyFiles()) assert.ok(JSON.parse(fs.readFileSync(file,'utf8')).every(s=>sprintForDate(s.date)===key));
 assert.ok(stored.length>0);assert.ok(!fs.existsSync(path.join(directory,'data/history.json')));
});
test('issue type requires exactly one of Epic, Story, Task or Sub-Task',()=>{
 assert.equal(issueType(['frontend','Story']),'Story');assert.equal(issueType([' sub-task ']),'Sub-Task');
 assert.equal(issueType(['Story','Task']),null);assert.equal(issueType(['bug']),null);assert.equal(issueType(undefined),null);
 assert.equal(context.issueType(['Epic','ai']),'Epic');assert.equal(context.issueType(['Epic','Task']),null);
});
test('burndown filters by Epic, Story & Task, Sub-Task; unrecorded labels are gaps, not zero',()=>{
 const typed=(id,labels,status='Ready')=>({id,status,sprint:'A',labels});
 const history=[snapshot('2026-10-10',[{id:1,status:'Ready',sprint:'A'}]),snapshot('2026-10-11',[typed(1,['Epic']),typed(2,['Story'],'Done'),typed(3,['Task']),typed(4,['Sub-Task']),typed(5,['bug'])])];
 const rows=(type)=>build(history,'A','Done','A',type);
 assert.equal(rows('all')[1].scope,5);assert.equal(rows('all')[0].scope,1);
 assert.equal(rows('epic')[1].scope,1);assert.equal(rows('story-task')[1].scope,2);assert.equal(rows('story-task')[1].remaining,1);assert.equal(rows('sub-task')[1].scope,1);
 assert.equal(rows('epic')[0].scope,null);assert.match(rows('epic')[0].quality,/Labels were not recorded/);
 assert.throws(()=>rows('bug'),/issue type/);
});
test('CFD filters issue types and leaves gaps for snapshots without labels',()=>{
 const cfd=fs.readFileSync(path.join(directory,'chart.html'),'utf8');
 const script=cfd.match(/<script>([\s\S]*?)<\/script>/)[1];
 const elements=new Map();
 const get=id=>{if(!elements.has(id))elements.set(id,{value:id==='sprint'||id==='issue-type'?'all':'',textContent:'',className:'',addEventListener(){}});return elements.get(id);};
 const charts=[];
 const ctx=vm.createContext({document:{getElementById:get},location:{protocol:'file:'},Chart:function(canvas,config){charts.push(config);this.destroy=()=>{};}});
 vm.runInContext(script.replace(/main\(\);\s*$/, ''),ctx);
 const history=[
  {date:'2026-11-05T12:00:00Z',issues:[{id:1,status:'Ready',sprint:'B'}]},
  {date:'2026-11-06T12:00:00Z',issues:[{id:1,status:'Ready',sprint:'B',labels:['Epic']},{id:2,status:'Ready',sprint:'B',labels:['Story']},{id:3,status:'Ready',sprint:'A',labels:['Task']},{id:4,status:'Ready',sprint:'B',labels:['Sub-Task']}]}
 ];
 ctx.testHistory=history;vm.runInContext('loadedHistory = testHistory',ctx);
 get('issue-type').value='story-task';ctx.render();
 assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Ready').data),[null,2]);
 get('sprint').value='B';ctx.render();
 assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Ready').data),[null,1]);
 get('issue-type').value='all';ctx.render();
 assert.deepEqual(Array.from(charts.at(-1).data.datasets.find(d=>d.label==='Ready').data),[1,3]);
});

test('stored history is fully labelled with exactly one type; Sprint A types follow title codes',()=>{
 const history=readHistory();
 for(const s of history)for(const i of s.issues){assert.ok(issueType(i.labels),`#${i.id} at ${s.date}`);}
 const a=history.find(s=>s.date.startsWith('2026-10-31'));
 const type=id=>issueType(a.issues.find(i=>i.id===id).labels);
 assert.equal(type(29),'Epic');assert.equal(type(26),'Task');assert.equal(type(23),'Sub-Task');
 assert.ok(a.labelsBackfill);
 const b=history.find(s=>s.date.startsWith('2026-11-06'));
 assert.equal(issueType(b.issues.find(i=>i.id===58).labels),'Story');
 assert.deepEqual(b.issues.find(i=>i.id===12).labels,['security','Sub-Task']);
});
