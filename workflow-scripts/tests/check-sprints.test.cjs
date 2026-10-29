const { test } = require('node:test');
const assert = require('node:assert/strict');
const { checkSprints, summary, annotation } = require('../check-sprints.js');
const issue = n => ({ id: 'i'+n, number:n, title:'Issue '+n });
const item = (n,sprint) => ({content:{__typename:'Issue',id:'i'+n},sprint});
const page = (nodes,next=null) => ({nodes,pageInfo:{hasNextPage:next!==null,endCursor:next}});
function api({issues=[issue(1)],items=[item(1,{name:'A'})],field={__typename:'ProjectV2SingleSelectField'},fail=null}={}) {
  const calls=[];
  const fetchImpl=async(url,options)=>{
    const {query,variables}=JSON.parse(options.body);calls.push({query,variables});
    if(fail==='http') return {ok:false,status:403};
    if(fail==='graphql') return {ok:true,json:async()=>({errors:[{message:'denied'}]})};
    let data;
    if(query.includes('projectV2(number:')) data={user:{projectV2:{id:'p9',field}}};
    else if(query.includes('issues(first:')) {
      assert.match(query,/states:OPEN/);
      data={repository:{issues:Array.isArray(issues)?page(issues):issues(variables.after)}};
    } else data={node:{items:Array.isArray(items)?page(items):items(variables.after)}};
    return {ok:true,json:async()=>({data})};
  };
  return {fetchImpl,calls};
}
const run=options=>checkSprints({token:'test',fetchImpl:api(options).fetchImpl});
test('detects blank and absent sprint plus repository issues outside the active project',async()=>{
  const result=await run({issues:[issue(1),issue(2),issue(3),issue(4)],items:[item(1,{name:'A'}),item(2,{text:'  '}),item(3,null)]});
  assert.equal(result.checked,4);assert.deepEqual(result.missing.map(i=>i.number),[2,3,4]);
  assert.match(result.missing[2].reason,/Not an active/);assert.match(summary(result),/issues\/4/);
});
test('accepts select, iteration and text sprint values; ignores unrelated project issues and drafts',async()=>{
  const result=await run({issues:[issue(1),issue(2),issue(3)],items:[item(1,{name:'A'}),item(2,{title:'Sprint B'}),item(3,{text:'C'}),item(99,null),{content:{__typename:'DraftIssue'}}]});
  assert.equal(result.missing.length,0);
});
test('paginates repository issues and project items',async()=>{
  const mock=api({issues:after=>after?page([issue(2)]):page([issue(1)],'issues-next'),items:after=>after?page([item(2,null)]):page([item(1,{title:'A'})],'items-next')});
  const result=await checkSprints({token:'test',fetchImpl:mock.fetchImpl});
  assert.equal(mock.calls.length,5);assert.equal(result.checked,2);assert.deepEqual(result.missing.map(i=>i.number),[2]);
});
test('fails clearly on token, HTTP, GraphQL and configuration errors',async()=>{
  await assert.rejects(()=>checkSprints(),/GITHUB_TOKEN/);
  await assert.rejects(()=>run({fail:'http'}),/403/);
  await assert.rejects(()=>run({fail:'graphql'}),/denied/);
  await assert.rejects(()=>run({field:null}),/field is missing/);
  await assert.rejects(()=>run({field:{__typename:'ProjectV2Field',dataType:'NUMBER'}}),/single-select/);
});
test('incomplete or inaccessible data and repeated pagination cannot produce success',async()=>{
  await assert.rejects(()=>run({items:[{content:null}]}),/inaccessible/);
  await assert.rejects(()=>run({items:()=>page([],'same')}),/cursor/);
  await assert.rejects(()=>run({items:[item(1,null),item(1,null)]}),/duplicate/);
  await assert.rejects(()=>run({issues:()=>({nodes:[]})}),/Incomplete/);
});
test('empty repositories pass with explicit zero-issue message; report escapes issue titles',async()=>{
  const result=await run({issues:[],items:[]});assert.match(summary(result),/No open issues/);
  const text=summary({checked:1,missing:[{number:1,title:'<b> | [link]\n::error::',url:'https://github.com/Phenriquerafael/LABDSOF_G9A/issues/1',reason:'Sprint is empty'}]});
  assert.ok(!text.includes('<b>'));assert.ok(text.includes('\\|'));assert.ok(!text.includes('\n::error::'));
  assert.equal(annotation('x\n%'), 'x%0A%25');
});