// G1 (browser path): proves the in-page proof runner reproduces the golden cases.
// run_golden.js tests the engine; this tests the code the browser actually executes.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "../../..");
const DIR = path.join(ROOT, "product of the swarms", "ai-voice-agent");

function el() {
  return {
    textContent: "", className: "", innerHTML: "", value: "", disabled: false, title: "",
    dataset: {}, scrollTop: 0, scrollHeight: 0, style: {}, children: [],
    classList: { add() {}, remove() {}, contains() { return false; } },
    addEventListener() {}, appendChild() {}, querySelectorAll() { return []; }, click() {}
  };
}
const nodes = {};
global.document = {
  getElementById(id) { return nodes[id] || (nodes[id] = el()); },
  createElement() { return el(); },
  querySelectorAll() { return []; }
};
global.window = global;
global.SpeechRecognition = undefined;
global.webkitSpeechRecognition = undefined;
global.speechSynthesis = { getVoices: () => [], speak() {}, cancel() {}, onvoiceschanged: null };
global.SpeechSynthesisUtterance = function (t) { this.text = t; };
global.setInterval = () => 0;

vm.runInThisContext(fs.readFileSync(path.join(DIR, "golden.js"), "utf8"));
vm.runInThisContext(fs.readFileSync(path.join(DIR, "index.html"), "utf8")
  .match(/<script>([\s\S]*?)<\/script>/)[1]);

const cases = global.GOLDEN;
if (!cases || !cases.length) {
  console.log("  no golden cases in the browser artifact");
  process.exit(1);
}

let pass = 0;
const results = [];
for (const c of cases) {
  const r = runGoldenCase(c);
  if (r.ok) pass++;
  else console.log(`  FAIL  ${c.id}  ${r.errs.join("; ")}`);
  results.push(r);
}

// the modal must render from those results without throwing
showProof({ at: new Date().toISOString(), source: global.GOLDEN_SHA, ms: 0, results });

console.log(`  ${pass}/${cases.length} golden calls passed through the browser runner`);
process.exit(pass === cases.length ? 0 : 1);
