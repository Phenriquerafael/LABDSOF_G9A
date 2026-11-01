const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {audit,validateHistory,validateLive,report,SPRINTS}=require('../validate-chart-data.js');
const now=new Date('2026-10-25T19:00:00Z');
const issue=(id,sprint='A',status='Ready')=>({id,sprint,status});
const snapshot=(date,issues=[issue(1)])=>({date,issues});
const live=(issues=[issue(1)])=>({checked:issues.length,liveIssues:issues,missing:[],statusOptions:['Backlog','Ready','Done'],activeNumbers:issues.map(i=>i.id)});
const errors=result=>result.findings.filter(f=>f.level==='error');
test('19h workflow is the single alert workflow and midnight metrics is not a dependency',()=>{
 const yml=fs.readFileSync(path.join(__dirname,'../../.github/workflows/check-sprints.yml'),'utf8');
 assert.match(yml,/cron: "0 19 \* \* \*"/);assert.match(yml,/timezone: "Europe\/Lisbon"/);
 assert.match(yml,/node workflow-scripts\/validate-chart-data.js/);assert.doesNotMatch(yml,/workflow_run:/);
 const html=fs.readFileSync(path.join(__dirname,'../burndown.html'),'utf8');
 for(const dates of Object.values(SPRINTS)) {assert.ok(html.includes(dates.start));assert.ok(html.includes(dates.end));}
});
test('valid live data and recent history pass all checks',async()=>{
 const result=await audit({now,historyText:JSON.stringify([snapshot('2026-10-25T00:00:00Z')]),loadLive:async()=>live()});
 assert.equal(result.findings.length,0);assert.match(report(result),/All checks passed/);
});
test('26-hour limit uses newest valid timestamp, not array position or a future entry',()=>{
 assert.equal(errors(validateHistory([snapshot('2026-10-24T17:00:00Z')],now)).length,0);
 const stale=validateHistory([snapshot('2026-10-24T16:59:00Z'),snapshot('2026-11-01T00:00:00Z')],now);
 assert.ok(stale.findings.some(f=>f.check==='Freshness'));assert.ok(stale.findings.some(f=>f.message.includes('future')));
});
test('rejects invalid shape, impossible dates, duplicate IDs, timestamps and chronological disorder',()=>{
 for(const h of [[],{},[snapshot('2026-02-30T00:00:00Z')],[snapshot('2026-10-25T00:00:00Z',[issue(1),issue(1)])],[{date:'2026-10-25T00:00:00Z',Ready:1}],[snapshot('2026-10-25T00:00:00Z'),snapshot('2026-10-25T00:00:00Z')],[snapshot('2026-10-25T00:00:00Z'),snapshot('2026-10-24T00:00:00Z')]]) assert.ok(errors(validateHistory(h,now)).length);
});
test('stored sprint and status limitations warn separately from current candidate errors',()=>{
 const h=[snapshot('2026-10-24T00:00:00Z',[{id:1,status:'Ready'}]),snapshot('2026-10-25T00:00:00Z')];
 assert.equal(errors(validateHistory(h,now)).length,0);assert.ok(validateHistory(h,now).findings.some(f=>f.level==='warning'));
 const stored=validateHistory([snapshot('2026-10-25T00:00:00Z',[issue(1,'Other','Bogus')])],now,['Ready']);
 assert.equal(errors(stored).length,0);assert.equal(stored.findings.filter(f=>f.level==='warning').length,2);
});
test('missing/unrecognised live sprints and statuses fail, outside-project issues are identified',()=>{
 const value=live([issue(1,null,null),issue(2,'Sprint X','Bogus')]);value.missing=[{number:1,reason:'Not an active item in project 9'}];
 const findings=validateLive(value,now,null);
 assert.equal(findings.filter(f=>f.check==='Sprint').length,2);assert.equal(findings.filter(f=>f.check==='Status').length,2);assert.ok(findings.some(f=>f.check==='Project membership'));
});
test('removed issues and empty current sprint warn without declaring completion',()=>{
 const h=validateHistory([snapshot('2026-10-24T00:00:00Z',[issue(1),issue(2)]),snapshot('2026-10-25T00:00:00Z')],now);
 assert.ok(h.findings.some(f=>f.check==='Scope'&&f.level==='warning'&&f.ids.includes(2)));
 const findings=validateLive(live([issue(2,'B')]),now,h.latest);
 assert.ok(findings.some(f=>f.check==='Current sprint'&&f.level==='warning'));assert.ok(findings.some(f=>f.check==='Scope'&&f.ids.includes(1)));
 assert.equal(findings.filter(f=>f.level==='error').length,0);
});
test('GitHub failures do not hide history failures; invalid JSON does not hide live findings',async()=>{
 let result=await audit({now,historyText:'{}',loadLive:async()=>{throw new Error('API denied');}});
 assert.ok(result.findings.some(f=>f.check==='GitHub access'));assert.ok(result.findings.some(f=>f.check==='History'));
 result=await audit({now,historyText:'{bad',loadLive:async()=>live([issue(1,null)])});
 assert.ok(result.findings.some(f=>f.check==='History'));assert.ok(result.findings.some(f=>f.check==='Sprint'));
});
test('current sprint uses Lisbon calendar; current sprint completed is only a warning',()=>{
 const value=live([issue(1,'B')]);
 const findings=validateLive(value,new Date('2026-10-10T00:00:00Z'),null);
 assert.ok(findings.some(f=>f.check==='Current sprint'&&f.message.includes('Sprint A')));
 const outside=validateLive(value,new Date('2027-02-01T19:00:00Z'),null);
 assert.ok(outside.some(f=>f.message.includes('outside')));
});
const {normalizeHistoryIdentity,migration}=require('../history-identity.js');
test('title mapping is unique and verified against all three raw sources',()=>{
 const raw=name=>JSON.parse(fs.readFileSync(path.join(__dirname,'../data/raw',name),'utf8'));
 const items=source=>raw(source).data.repository.projectsV2.nodes.find(p=>p.number===9).items.nodes;
 const old=items(migration.sources.old), recent=items(migration.sources.new), first=items(migration.sources.firstNew);
 assert.equal(migration.mapping.length,33);
 assert.equal(new Set(migration.mapping.map(m=>m.newId)).size,33);
 for(const m of migration.mapping){assert.equal(old.find(i=>i.content.number===m.oldId).content.title,m.title);assert.equal(recent.find(i=>i.content.number===m.newId).content.title,m.title);assert.equal(first.find(i=>i.content.number===m.newId).content.title,m.title);}
});
test('migration prevents ID collisions and false scope removals without mutating sprint/status',()=>{
 const original=[snapshot(migration.oldLastSnapshot,[issue(26,null,'Done')]),snapshot(migration.newFirstSnapshot,[issue(11,'A','Done')])];
 const copy=JSON.stringify(original), normalized=normalizeHistoryIdentity(original);
 assert.equal(normalized[0].issues[0].id,11);assert.equal(normalized[0].issues[0].sprint,null);assert.equal(normalized[0].issues[0].status,'Done');assert.equal(JSON.stringify(original),copy);
 const result=validateHistory(normalized,new Date('2026-10-21T19:00:00Z'));
 assert.ok(!result.findings.some(f=>f.check==='Scope'));
 assert.deepEqual(result.findings.find(f=>f.check==='Sprint history').ids,[11]);
 assert.throws(()=>normalizeHistoryIdentity([snapshot('2026-10-21T12:00:00Z')]),/unconfirmed/);
 assert.throws(()=>normalizeHistoryIdentity([snapshot(migration.oldLastSnapshot,[issue(999)])]),/No verified/);
});
test('closed project issues are validated even when all open issues have valid assignments',()=>{
 const value=live([issue(1)]);value.candidateIssues=[issue(1),issue(2,null,'Done')];value.activeNumbers=[1,2];
 const findings=validateLive(value,now,null);
 assert.ok(findings.some(f=>f.check==='Sprint'&&f.level==='error'&&f.ids.includes(2)));
});
test('fixing current assignments clears candidate errors without rewriting stored gaps',async()=>{
 const value=live([issue(1)]);value.candidateIssues=[issue(1)];
 const result=await audit({now,historyText:JSON.stringify([snapshot('2026-10-24T00:00:00Z',[issue(1,null)]),snapshot('2026-10-25T00:00:00Z',[issue(1,null)])]),loadLive:async()=>value});
 assert.equal(errors(result).length,0);assert.equal(result.findings.filter(f=>f.check==='Sprint history').length,1);
 assert.equal(result.findings[0].details.length,2);assert.match(report(result),/Historical sprint gaps/);
});
test('actual saved history produces one historical warning with corrected links, without changing source files',async()=>{
 const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/raw',migration.sources.new),'utf8'));
 const source=fs.readFileSync(path.join(__dirname,'../data/history.json'),'utf8');
 const historical=JSON.parse(source).filter(s=>s.date<=raw.date);
 const candidate=raw.data.repository.projectsV2.nodes.find(p=>p.number===9).items.nodes.map(i=>({id:i.content.number,sprint:i.sprint,status:i.fieldValues.nodes.find(f=>f.field?.name==='Status').name}));
 const value={...live(candidate),candidateIssues:candidate,statusOptions:[...new Set(candidate.map(i=>i.status))]};
 const result=await audit({now:new Date(Date.parse(raw.date)+60000),historyText:JSON.stringify(historical),loadLive:async()=>value});
 assert.equal(errors(result).length,0);
 const gaps=result.findings.filter(f=>f.check==='Sprint history');assert.equal(gaps.length,1);assert.equal(gaps[0].details.length,11);
 const first=gaps[0].details[0];assert.deepEqual([...first.ids].sort((a,b)=>a-b),[9,10,11,30]);
 assert.ok(!result.findings.some(f=>f.check==='Scope'));
 assert.equal(fs.readFileSync(path.join(__dirname,'../data/history.json'),'utf8'),source);
});