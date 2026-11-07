// Shared sprint calendar, per-sprint history files and issue type labels.
// CommonJS keeps this runnable on Node 20 without a root package.json.
const fs = require('node:fs');
const path = require('node:path');

// Inclusive UTC dates; keep aligned with burndown.html (a regression test checks this).
const SPRINTS = {
  A: { start: '2026-10-10', end: '2026-10-31' },
  B: { start: '2026-11-01', end: '2026-12-05' },
  C: { start: '2026-12-06', end: '2027-01-03' },
};
const SPRINT_KEYS = Object.keys(SPRINTS);
const dataDirectory = path.join(__dirname, 'data');
const historyFileName = key => `history-sprint-${key.toLowerCase()}.json`;

// Exactly one of these labels identifies an issue's type.
const TYPE_LABELS = ['Epic', 'Story', 'Task', 'Sub-Task'];
const typeKey = value => String(value).trim().toLowerCase();
const TYPE_BY_KEY = new Map(TYPE_LABELS.map(label => [typeKey(label), label]));

// Snapshots are filed by their UTC collection day; days outside the calendar go to the nearest sprint.
function sprintForDate(date) {
  const time = Date.parse(date);
  if (!Number.isFinite(time)) throw new Error(`Invalid snapshot date: ${date}`);
  const day = new Date(time).toISOString().slice(0, 10);
  if (day < SPRINTS.A.start) return 'A';
  return SPRINT_KEYS.find(key => day <= SPRINTS[key].end) ?? SPRINT_KEYS.at(-1);
}

// Returns the canonical type label, or null when the issue has none or more than one.
function issueType(labels) {
  if (!Array.isArray(labels)) return null;
  const types = new Set(labels.map(label => TYPE_BY_KEY.get(typeKey(label))).filter(Boolean));
  return types.size === 1 ? [...types][0] : null;
}

function historyFiles(directory = dataDirectory) {
  return SPRINT_KEYS.map(key => ({ key, file: path.join(directory, historyFileName(key)) }));
}

function parseHistoryText(text, name) {
  const history = JSON.parse(String(text).replace(/^\uFEFF/, ''));
  if (!Array.isArray(history)) throw new Error(`${name} is not an array.`);
  return history;
}

// Reads all sprint files into one chronological array. Missing files count as empty;
// unreadable files and snapshots stored in the wrong sprint file throw.
function readHistory({ directory = dataDirectory, fsImpl = fs } = {}) {
  const history = [];
  for (const { key, file } of historyFiles(directory)) {
    if (!fsImpl.existsSync(file)) continue;
    const name = path.basename(file);
    for (const snapshot of parseHistoryText(fsImpl.readFileSync(file, 'utf8'), name)) {
      let expected = null;
      try { expected = sprintForDate(snapshot?.date); } catch { /* the structural validator reports invalid dates */ }
      if (expected && expected !== key) throw new Error(`${name} contains snapshot ${snapshot.date}, which belongs to Sprint ${expected}.`);
      history.push(snapshot);
    }
  }
  return history.sort((a, b) => Date.parse(a?.date) - Date.parse(b?.date));
}

// Appends one snapshot to its sprint file atomically (temporary file, then rename).
function appendSnapshot(snapshot, { directory = dataDirectory, fsImpl = fs, runId = `${Date.now()}-${process.pid}` } = {}) {
  const key = sprintForDate(snapshot.date);
  const file = path.join(directory, historyFileName(key));
  const name = path.basename(file);
  const history = fsImpl.existsSync(file) ? parseHistoryText(fsImpl.readFileSync(file, 'utf8'), name) : [];
  history.push(snapshot);
  fsImpl.mkdirSync(directory, { recursive: true });
  const temporaryFile = path.join(directory, `history-${runId}.tmp`);
  fsImpl.writeFileSync(temporaryFile, JSON.stringify(history, null, 2));
  fsImpl.renameSync(temporaryFile, file);
  return { key, file };
}

module.exports = { SPRINTS, SPRINT_KEYS, TYPE_LABELS, dataDirectory, historyFileName, historyFiles, sprintForDate, issueType, readHistory, appendSnapshot };
