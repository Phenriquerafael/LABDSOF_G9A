const migration = require('./config/issue-migration.json');

// Derive a comparison view only. Never rewrite source history or infer sprint/status.
function normalizeHistoryIdentity(history, config = migration) {
  if (!Array.isArray(history)) return history;
  const mapping = new Map(config.mapping.map(item => [item.oldId, item.newId]));
  if (mapping.size !== config.mapping.length || new Set(mapping.values()).size !== mapping.size) throw new Error('Ambiguous issue migration mapping.');
  const oldEnd = Date.parse(config.oldLastSnapshot), newStart = Date.parse(config.newFirstSnapshot);
  return history.map(snapshot => {
    const time = Date.parse(snapshot?.date);
    if (!Number.isFinite(time) || !Array.isArray(snapshot?.issues)) return snapshot;
    if (time > oldEnd && time < newStart) throw new Error(`Repository identity is unconfirmed for snapshot ${snapshot.date}; verify its raw titles before comparison.`);
    if (time >= newStart) return snapshot;
    return { ...snapshot, issues: snapshot.issues.map(issue => {
      if (!Number.isSafeInteger(issue?.id)) return issue; // Structural validator reports this.
      if (!mapping.has(issue.id)) throw new Error(`No verified migration mapping for old issue #${issue.id} at ${snapshot.date}.`);
      return { ...issue, id: mapping.get(issue.id) };
    }) };
  });
}
module.exports = { normalizeHistoryIdentity, migration };