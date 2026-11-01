const fs = require('node:fs');
const path = require('node:path');
const { checkSprints, annotation, escapeMarkdown } = require('./check-sprints.js');
const SPRINTS = {
  A: { start: '2026-10-10', end: '2026-10-31' },
  B: { start: '2026-11-01', end: '2026-12-05' },
  C: { start: '2026-12-06', end: '2027-01-03' },
};
const { normalizeHistoryIdentity } = require('./history-identity.js');
const MAX_AGE_HOURS = 26;
const normalize = value => typeof value === 'string' ? value.trim().toLowerCase() : '';
const sprintKey = value => /^(?:sprint\s+)?([abc])$/i.exec(typeof value === 'string' ? value.trim() : '')?.[1].toUpperCase() ?? null;
const finding = (level, check, message, ids = []) => ({ level, check, message, ids });

function validateHistory(history, now, statusOptions = null) {
  const findings = [], valid = [];
  if (!Array.isArray(history) || !history.length) return { findings: [finding('error', 'History', 'History must be a non-empty array.')], latest: null };
  const timestamps = new Set();
  let previous = -Infinity;
  for (const [index, snapshot] of history.entries()) {
    const date = snapshot?.date;
    const time = typeof date === 'string' ? Date.parse(date) : NaN;
    const prefix = `Snapshot ${index + 1}`;
    if (!Number.isFinite(time) || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(date) || new Date(time).toISOString().slice(0,19) !== date.slice(0,19)) {
      findings.push(finding('error','History',`${prefix}: invalid UTC timestamp.`)); continue;
    }
    if (time > now.getTime() + 5 * 60000) { findings.push(finding('error','History',`${prefix}: timestamp is in the future (${date}).`)); continue; }
    if (timestamps.has(time)) findings.push(finding('error','History',`${prefix}: duplicate snapshot timestamp.`));
    timestamps.add(time);
    if (time < previous) findings.push(finding('error','History',`${prefix}: snapshots are out of chronological order.`));
    previous = time;
    if (!Array.isArray(snapshot.issues)) { findings.push(finding('error','History',`${prefix}: missing issues array (aggregate-only history cannot filter sprints).`)); continue; }
    const seen = new Set();
    let usable = true;
    for (const issue of snapshot.issues) {
      if (!Number.isSafeInteger(issue?.id) || issue.id <= 0 || seen.has(issue.id)) {
        findings.push(finding('error','History',`${prefix}: invalid or duplicate issue ID.`)); usable = false; continue;
      }
      seen.add(issue.id);
      if (!normalize(issue.status) || ['unknown','no_status'].includes(normalize(issue.status))) {
        findings.push(finding('error','History',`${prefix}: missing or unusable status.`,[issue.id])); usable = false;
      }
      if (issue.sprint !== undefined && issue.sprint !== null && typeof issue.sprint !== 'string') {
        findings.push(finding('error','History',`${prefix}: sprint must be text or null.`,[issue.id])); usable = false;
      }
    }
    if (usable) valid.push({ ...snapshot, time });
  }
  valid.sort((a,b) => a.time-b.time);
  const latest = valid.at(-1) ?? null;
  if (!latest) findings.push(finding('error','Freshness','No structurally valid snapshot is available.'));
  else {
    const age = (now.getTime()-latest.time)/3600000;
    if (age > MAX_AGE_HOURS) findings.push(finding('error','Freshness',`Latest valid snapshot is ${age.toFixed(1)} hours old (limit ${MAX_AGE_HOURS} hours): ${latest.date}.`));
    if (!latest.issues.length) findings.push(finding('warning','Scope','Latest snapshot contains zero issues.'));
    const gaps = valid.map(snapshot => ({ date: snapshot.date, ids: snapshot.issues.filter(issue=>!sprintKey(issue.sprint)).map(issue=>issue.id) })).filter(gap=>gap.ids.length);
    if (gaps.length) {
      const ids = [...new Set(gaps.flatMap(gap=>gap.ids))].sort((a,b)=>a-b);
      const warning = finding('warning','Sprint history',
        `Known data limitations in ${gaps.length} stored snapshots (${gaps[0].date} to ${gaps.at(-1).date}). These are recorded historical values, not evidence of a current missing assignment. Correct live data and collect a new snapshot; do not infer past sprints.`,ids);
      warning.details = gaps;
      findings.push(warning);
    }
    if (statusOptions) {
      const allowed = new Set(statusOptions.map(normalize));
      const unknown = latest.issues.filter(issue=>!allowed.has(normalize(issue.status))).map(issue=>issue.id);
      if (unknown.length) findings.push(finding('warning','Status history','Stored snapshot has statuses outside current project options; verify historical configuration. Live candidate statuses are checked separately.',unknown));
    }
    if (valid.length > 1) {
      const current = new Set(latest.issues.map(issue=>issue.id));
      const removed = valid.at(-2).issues.filter(issue=>!current.has(issue.id)).map(issue=>issue.id);
      if (removed.length) findings.push(finding('warning','Scope','Issues disappeared between the two latest valid snapshots. Check removals, archiving or transfers; this is not proof of completion.',removed));
    }
  }
  return { findings, latest };
}

function validateLive(live, now, latest) {
  const findings=[];
  if (!Array.isArray(live.statusOptions) || !live.statusOptions.length) findings.push(finding('error','Status','Project Status must be a single-select field with options.'));
  const allowed=new Set((live.statusOptions || []).map(normalize));
  const candidate = live.candidateIssues ?? live.liveIssues;
  const issuesToCheck = new Map(candidate.map(issue => [issue.id, issue]));
  for (const issue of live.liveIssues) if (!issuesToCheck.has(issue.id)) issuesToCheck.set(issue.id, issue);
  for (const issue of issuesToCheck.values()) {
    if (!sprintKey(issue.sprint)) findings.push(finding('error','Sprint','Issue has no recognised sprint in the current collection candidate. Use A/Sprint A, B/Sprint B or C/Sprint C in project 9.',[issue.id]));
    if (!normalize(issue.status) || ['unknown','no_status'].includes(normalize(issue.status)) || !allowed.has(normalize(issue.status))) findings.push(finding('error','Status','Issue has no valid project Status in the current collection candidate.',[issue.id]));
  }
  for (const missing of live.missing.filter(issue=>issue.reason==='Not an active item in project 9')) findings.push(finding('error','Project membership','Open issue is not an active item in project 9.',[missing.number]));
  const localDay = new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Lisbon',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
  const current = Object.entries(SPRINTS).find(([,dates])=>localDay>=dates.start && localDay<=dates.end)?.[0];
  if (current && live.liveIssues.length && !live.liveIssues.some(issue=>sprintKey(issue.sprint)===current)) findings.push(finding('warning','Current sprint',`No open issues assigned to current Sprint ${current} (${localDay}, Lisbon). They may all be completed; review before interpreting the chart.`));
  if (!current) findings.push(finding('warning','Current sprint','Today is outside the configured A/B/C periods. Review the sprint calendar.'));
  if (latest) {
    const active=new Set(live.activeNumbers);
    const removed=latest.issues.filter(issue=>!active.has(issue.id)).map(issue=>issue.id);
    if (removed.length) findings.push(finding('warning','Scope','Issues in the latest snapshot are no longer active items in this repository/project. Review before the midnight collection.',removed));
  }
  return findings;
}

async function audit({ historyText, now = new Date(), loadLive = () => checkSprints({token:process.env.GITHUB_TOKEN}) }) {
  const findings=[];
  let live=null, latest=null;
  try { live=await loadLive(); } catch(error) { findings.push(finding('error','GitHub access',`Live checks incomplete: ${error.message}`)); }
  try {
    const history=normalizeHistoryIdentity(JSON.parse(historyText.replace(/^\uFEFF/,'')));
    const result=validateHistory(history,now,live?.statusOptions);
    findings.push(...result.findings); latest=result.latest;
  } catch(error) { findings.push(finding('error','History',`Unable to validate history: ${error.message}`)); }
  if(live) findings.push(...validateLive(live,now,latest));
  return { findings, latestDate:latest?.date ?? null, checked:live?.checked ?? null, candidateCount:live?.candidateIssues?.length ?? null, now:now.toISOString() };
}

function report(result) {
  const errors=result.findings.filter(f=>f.level==='error').length;
  const warnings=result.findings.length-errors;
  const lines=['## Chart data validation','',`Checked at ${result.now}. Repository: Phenriquerafael/LABDSOF_G9A; project 9.`,
    `Open issues checked: ${result.checked ?? 'unavailable'}. Latest valid snapshot: ${result.latestDate ?? 'unavailable'}.`,
    `Active project issues in collection candidate (including closed): ${result.candidateCount ?? 'unavailable'}.`,
    `${errors} error(s), ${warnings} warning(s).`,''];
  if(!result.findings.length) lines.push('All checks passed. This validates current data, not the future midnight snapshot.');
  else {
    lines.push('| Severity | Check | Details | Issues |','|---|---|---|---|');
    for(const f of result.findings) lines.push(`| ${f.level} | ${escapeMarkdown(f.check)} | ${escapeMarkdown(f.message)} | ${f.ids.map(id=>`[#${id}](https://github.com/Phenriquerafael/LABDSOF_G9A/issues/${id})`).join(', ')} |`);
  }
  const historyGap = result.findings.find(f=>f.details);
  if(historyGap) {
    lines.push('', '<details><summary>Historical sprint gaps by snapshot (IDs mapped to the current repository)</summary>', '');
    for(const gap of historyGap.details) lines.push(`- ${gap.date}: ${gap.ids.map(id=>'#'+id).join(', ')}`);
    lines.push('', '</details>');
  }
  lines.push('','Errors fail the check. Scope/calendar warnings require review but do not fail it. Correct live assignments and rerun manually; retain historical evidence rather than inventing past values.');
  return lines.join('\n')+'\n';
}
async function main() {
  let historyText='';
  let readError=null;
  try {historyText=fs.readFileSync(path.join(__dirname,'data/history.json'),'utf8');} catch(error) {readError=error;}
  const result=await audit({historyText});
  if(readError) result.findings.push(finding('error','History file',readError.message));
  if(process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY,report(result));
  for(const f of result.findings) console.log(`::${f.level}::${annotation(`${f.check}: ${f.message}${f.ids.length?' Issues: '+f.ids.join(', '):''}`)}`);
  console.log(`${result.findings.filter(f=>f.level==='error').length} errors; ${result.findings.filter(f=>f.level==='warning').length} warnings.`);
  if(result.findings.some(f=>f.level==='error')) process.exitCode=1;
}
if(require.main===module) main().catch(error=>{console.error('::error::Validation could not finish: '+annotation(error.message));process.exitCode=2;});
module.exports={audit,validateHistory,validateLive,report,SPRINTS};