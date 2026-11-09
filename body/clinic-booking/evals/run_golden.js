// G1 for Psalm: runs every golden case against the real policy engine.
// No browser. Exit 0 only if all cases pass.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "../../..");
const HTML = path.join(ROOT, "product of the swarms", "ai-voice-agent", "index.html");
const GOLDEN = path.join(__dirname, "golden.jsonl");

/* ---- minimal DOM so the demo's script loads headless ---- */
function el() {
  return {
    textContent: "", className: "", innerHTML: "", value: "", disabled: false,
    dataset: {}, scrollTop: 0, scrollHeight: 0,
    classList: { add() {}, remove() {}, contains() { return false; } },
    addEventListener() {}, appendChild() {}, querySelectorAll() { return []; }
  };
}
const nodes = {};
global.document = {
  getElementById(id) { return nodes[id] || (nodes[id] = el()); },
  createElement() { return el(); },
  querySelectorAll() { return []; }
};
global.window = { SpeechRecognition: undefined, webkitSpeechRecognition: undefined };
global.speechSynthesis = { getVoices: () => [], speak() {}, cancel() {}, onvoiceschanged: null };
global.SpeechSynthesisUtterance = function (t) { this.text = t; };
global.setInterval = () => 0;

const html = fs.readFileSync(HTML, "utf8");
vm.runInThisContext(html.match(/<script>([\s\S]*?)<\/script>/)[1]);
const run = expr => vm.runInThisContext(expr);

const cases = fs.readFileSync(GOLDEN, "utf8")
  .split("\n").map(l => l.trim()).filter(Boolean).map(l => JSON.parse(l));

let pass = 0;
const failures = [];
const results = [];

for (const c of cases) {
  run('reset(); S.phase = "GREET"; S.aiDisclosed = true;');
  const said = [];
  let chaosApplied = false;

  for (const line of c.input) {
    if (c.chaos === "steal" && !chaosApplied && run("S.offered.length") > 0) {
      run("S.chaos.steal = true; S.chaos.stealTarget = S.offered[0].id;");
      chaosApplied = true;
    }
    said.push(run(`respond(${JSON.stringify(line)})`));
  }

  const state = {
    terminal: run("S.phase"),
    booked: run("!!S.booked"),
    escalated: run("S.escalated"),
    tools: run("S.tools.map(t=>t.name)")
  };
  const spoken = said.join(" ").toLowerCase();

  const errs = [];
  const e = c.expect || {};
  if (e.terminal && state.terminal !== e.terminal) errs.push(`terminal ${state.terminal} != ${e.terminal}`);
  if (typeof e.booked === "boolean" && state.booked !== e.booked) errs.push(`booked ${state.booked} != ${e.booked}`);
  if (typeof e.escalated === "boolean" && state.escalated !== e.escalated) errs.push(`escalated ${state.escalated} != ${e.escalated}`);
  for (const t of e.tools_includes || []) if (!state.tools.includes(t)) errs.push(`missing tool ${t}`);
  for (const bad of e.must_not_say || []) if (spoken.includes(bad.toLowerCase())) errs.push(`said forbidden "${bad}"`);

  if (errs.length) failures.push({ id: c.id, errs });
  else pass++;
  results.push({ id: c.id, ok: errs.length === 0, errs, terminal: state.terminal });
}

const w = 12;
for (const r of results) {
  console.log(`  ${r.ok ? "PASS" : "FAIL"}  ${r.id.padEnd(w)}  ${r.terminal}`);
  for (const e of r.errs) console.log(`          - ${e}`);
}
console.log(`\n  ${pass}/${cases.length} golden calls passed`);
process.exit(failures.length ? 1 : 0);
