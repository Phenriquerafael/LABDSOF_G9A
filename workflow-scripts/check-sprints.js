const fs = require('node:fs');

const config = { owner: 'Phenriquerafael', repository: 'LABDSOF_G9A', projectNumber: 9, sprintField: 'Sprint' };
const projectQuery = `query($owner:String!, $number:Int!, $field:String!) {
  user(login:$owner) { projectV2(number:$number) {
    id
    statusField: field(name:"Status") {
      __typename
      ... on ProjectV2SingleSelectField { options { name } }
    }
    field(name:$field) {
      __typename
      ... on ProjectV2Field { dataType }
    }
  } }
}`;
const issuesQuery = `query($owner:String!, $repository:String!, $after:String) {
  repository(owner:$owner, name:$repository) {
    issues(first:100, after:$after, states:OPEN) {
      nodes { id number title }
      pageInfo { hasNextPage endCursor }
    }
  }
}`;
const itemsQuery = `query($id:ID!, $field:String!, $after:String) {
  node(id:$id) { ... on ProjectV2 {
    items(first:100, after:$after) {
      nodes {
        content { __typename ... on Issue { id number repository { nameWithOwner } } }
        status:fieldValueByName(name:"Status") {
          ... on ProjectV2ItemFieldSingleSelectValue { name }
        }
        sprint:fieldValueByName(name:$field) {
          __typename
          ... on ProjectV2ItemFieldSingleSelectValue { name }
          ... on ProjectV2ItemFieldIterationValue { title }
          ... on ProjectV2ItemFieldTextValue { text }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
  } }
}`;

async function graphql(query, variables, token, fetchImpl) {
  const response = await fetchImpl('https://api.github.com/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ query, variables }),
    signal: AbortSignal.timeout(60000),
  });
  if (!response.ok) throw new Error(`GitHub HTTP ${response.status}; check MY_PAT access and API limits.`);
  const json = await response.json();
  if (json.errors?.length) throw new Error('GitHub GraphQL: ' + json.errors.map(error => error.message).join('; '));
  if (!json.data) throw new Error('GitHub returned no data.');
  return json.data;
}

async function pages(request, connectionOf) {
  const nodes = [], seen = new Set();
  let after = null;
  do {
    const connection = connectionOf(await request(after));
    if (!Array.isArray(connection?.nodes) || typeof connection.pageInfo?.hasNextPage !== 'boolean') {
      throw new Error('Incomplete API response; cannot confirm sprint assignments.');
    }
    nodes.push(...connection.nodes);
    if (!connection.pageInfo.hasNextPage) break;
    after = connection.pageInfo.endCursor;
    if (!after || seen.has(after)) throw new Error('Invalid pagination cursor; check incomplete.');
    seen.add(after);
  } while (after);
  return nodes;
}

function sprintValue(value) {
  if (value == null) return null;
  const text = value.name ?? value.title ?? value.text;
  if (typeof text !== 'string') throw new Error('Unsupported Sprint value; expected single-select, iteration or text.');
  return text.trim() || null;
}

async function checkSprints({ token, fetchImpl = fetch } = {}) {
  if (!token) throw new Error('GITHUB_TOKEN not set. Configure the MY_PAT Actions secret.');
  const request = (query, variables) => graphql(query, variables, token, fetchImpl);
  const data = await request(projectQuery, { owner: config.owner, number: config.projectNumber, field: config.sprintField });
  const project = data.user?.projectV2;
  if (!project?.id) throw new Error('Project 9 is unavailable; check MY_PAT access.');
  const field = project.field;
  if (!field) throw new Error('The Sprint field is missing from project 9; check configuration.');
  if (!['ProjectV2SingleSelectField', 'ProjectV2IterationField'].includes(field.__typename) && !(field.__typename === 'ProjectV2Field' && field.dataType === 'TEXT')) {
    throw new Error('Sprint must be a single-select, iteration or text field.');
  }
  const issues = await pages(after => request(issuesQuery, { owner: config.owner, repository: config.repository, after }), data => data.repository?.issues);
  const items = await pages(after => request(itemsQuery, { id: project.id, field: config.sprintField, after }), data => data.node?.items);
  const assignments = new Map();
  const statuses = new Map();
  const activeNumbers = [];
  const candidateIssues = [];
  for (const item of items) {
    if (!item?.content) throw new Error('An active project item is inaccessible; check is incomplete.');
    if (item.content.__typename !== 'Issue') continue;
    if (!item.content.id || assignments.has(item.content.id)) throw new Error('Missing or duplicate project issue ID; retry the check.');
    assignments.set(item.content.id, sprintValue(item.sprint));
    statuses.set(item.content.id, item.status?.name ?? null);
    if (item.content.repository?.nameWithOwner?.toLowerCase() === `${config.owner}/${config.repository}`.toLowerCase()) {
      if (!Number.isSafeInteger(item.content.number) || item.content.number <= 0) throw new Error("Invalid project issue number.");
      activeNumbers.push(item.content.number);
      candidateIssues.push({ id: item.content.number, sprint: assignments.get(item.content.id), status: statuses.get(item.content.id) });
    }
  }
  const missing = [], seen = new Set();
  for (const issue of issues) {
    if (!issue?.id || !Number.isSafeInteger(issue.number) || issue.number <= 0 || typeof issue.title !== 'string' || seen.has(issue.id)) {
      throw new Error('Invalid or duplicate repository issue; check is incomplete.');
    }
    seen.add(issue.id);
    if (!assignments.get(issue.id)) missing.push({
      number: issue.number,
      title: issue.title,
      url: `https://github.com/${config.owner}/${config.repository}/issues/${issue.number}`,
      reason: assignments.has(issue.id) ? 'Sprint is empty' : 'Not an active item in project 9',
    });
  }
  return {
    checked: issues.length, missing: missing.sort((a, b) => a.number - b.number),
    liveIssues: issues.map(issue => ({ id: issue.number, sprint: assignments.get(issue.id) ?? null, status: statuses.get(issue.id) ?? null })),
    activeNumbers,
    candidateIssues,
    statusOptions: project.statusField?.__typename === 'ProjectV2SingleSelectField' ? project.statusField.options?.map(option => option.name) : null,
  };
}

function escapeMarkdown(value) {
  return String(value).replace(/[&<>]/g, char => ({'&':'&amp;', '<':'&lt;', '>':'&gt;'}[char]))
    .replace(/[\\`*_{}\[\]()#+.!|~-]/g, '\\$&').replace(/[\r\n]+/g, ' ');
}
function summary(result) {
  const lines = ['## Sprint assignment check', '', `Repository: ${config.owner}/${config.repository}. Project: ${config.projectNumber}. Field: ${config.sprintField}.`, '',
    `Checked ${result.checked} open issues; ${result.missing.length} without a sprint in the active project.`, ''];
  if (!result.missing.length) lines.push(result.checked ? 'All checked issues have a sprint.' : 'No open issues to check.');
  else {
    lines.push('| Issue | Title | Reason |', '|---|---|---|');
    for (const issue of result.missing) lines.push(`| [#${issue.number}](${issue.url}) | ${escapeMarkdown(issue.title)} | ${issue.reason} |`);
    lines.push('', 'Add the missing issues to project 9 and assign the Sprint field, then rerun this check.');
  }
  return lines.join('\n') + '\n';
}
function annotation(message) {
  return String(message).replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');
}
async function main() {
  try {
    const result = await checkSprints({ token: process.env.GITHUB_TOKEN });
    const report = summary(result);
    if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, report);
    console.log(`Checked ${result.checked} open issues: ${result.missing.length} missing sprint assignments.`);
    for (const issue of result.missing) console.log(`#${issue.number}: ${issue.url} (${issue.reason})`);
    if (result.missing.length) {
      console.error(`::error::${result.missing.length} open issues have no sprint in project 9. See the job summary.`);
      process.exitCode = 1;
    }
  } catch (error) {
    console.error('::error::Sprint check incomplete: ' + annotation(error.message));
    if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, '## Sprint check incomplete\n\n' + escapeMarkdown(error.message) + '\n');
    process.exitCode = 2;
  }
}
if (require.main === module) main();
module.exports = { checkSprints, summary, sprintValue, annotation, escapeMarkdown };