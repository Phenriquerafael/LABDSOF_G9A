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
test('old unknown sprint data warns; latest unknown sprint and unknown status fail',()=>{
 const h=[snapshot('2026-10-24T00:00:00Z',[{id:1,status:'Ready'}]),snapshot('2026-10-25T00:00:00Z')];
 assert.equal(errors(validateHistory(h,now)).length,0);assert.ok(validateHistory(h,now).findings.some(f=>f.level==='warning'));
 assert.ok(errors(validateHistory([snapshot('2026-10-25T00:00:00Z',[issue(1,'Other','Bogus')])],now,['Ready'])).length>=2);
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