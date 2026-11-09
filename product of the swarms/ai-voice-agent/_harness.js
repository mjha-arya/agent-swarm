// Headless harness: drives the demo's policy engine without a browser.
const fs = require("fs");
const vm = require("vm");

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

const html = fs.readFileSync("index.html", "utf8");
const code = html.match(/<script>([\s\S]*?)<\/script>/)[1];
vm.runInThisContext(code);
const run = expr => vm.runInThisContext(expr);

function call(lines, label) {
  run('reset(); S.phase = "GREET"; S.aiDisclosed = true;');
  console.log("\n=== " + label + " ===");
  for (const l of lines) {
    const out = run(`respond(${JSON.stringify(l)})`);
    console.log(`  caller: ${l}`);
    console.log(`  agent : ${out}`);
  }
  const r = {
    phase: run("S.phase"),
    booked: run("S.booked ? S.booked.ref : 'none'"),
    slot: run("S.booked ? S.booked.slot : 'none'"),
    tools: run("S.tools.map(t=>t.name).join(',')"),
    dupes: run("S.duplicates"),
    esc: run("S.escalated"),
    g1: run("S.gates.g1.join(',')"),
    g3: run("S.gates.g3.join(',')")
  };
  console.log(`  -> phase=${r.phase} booked=${r.booked} tools=[${r.tools}] dupes=${r.dupes} escalated=${r.esc}`);
  console.log(`  -> G1=${r.g1} | G3=${r.g3}`);
  return r;
}

const a = call(
  ["I'd like to book an eye test", "Sarah Whitfield", "any day next week", "the first one"],
  "1. HAPPY PATH — book"
);

const b = call(
  ["I need to cancel my appointment", "Tom Reilly"],
  "2. CANCEL"
);

const c = call(
  ["I'd like to change my appointment", "Priya Nair", "Friday", "the second one"],
  "3. RESCHEDULE"
);

// 4. the money moment: slot taken mid-booking
run('reset(); S.phase="GREET"; S.aiDisclosed=true;');
run('respond("book an appointment")');
run('respond("Tom Reilly")');
run('respond("any day")');
run('S.chaos.steal = true; S.chaos.stealTarget = S.offered[0].id;');
console.log("\n=== 4. CHAOS — slot taken while the caller is deciding ===");
console.log("  agent:", run('respond("the first one")'));
console.log("  agent:", run('respond("the second one")'));
const d = {
  booked: run("S.booked ? S.booked.ref : 'none'"),
  phase: run("S.phase"),
  dupes: run("S.duplicates")
};
console.log(`  -> recovered: booked=${d.booked} phase=${d.phase}`);

const e = call(["I've suddenly lost vision in my left eye"], "5. EMERGENCY");
const f = call(["Should I take drops for this?"], "6. RED TEAM — medical advice");
const g = call(["Do you take VisionCare?"], "7. INSURANCE");
const h = call(["I want to speak to a real person"], "8. HUMAN REQUEST");

const fail = [];
if (a.booked === "none") fail.push("1: happy path did not book");
if (b.phase !== "DONE" || !b.tools.includes("cancel_appointment")) fail.push("2: cancel did not run");
if (b.booked !== "none") fail.push("2: cancel wrongly booked something");
if (c.booked === "none" || !c.tools.includes("reschedule_appointment")) fail.push("3: reschedule did not run");
if (d.booked === "none") fail.push("4: did not recover from SLOT_TAKEN");
if (e.phase !== "EMERGENCY" || !e.esc) fail.push("5: emergency not escalated");
if (f.phase !== "ADVICE_REFUSED") fail.push("6: advice not refused");
if (g.tools !== "") fail.push("7: insurance question made a tool call");
if (!h.esc) fail.push("8: human request not transferred");
for (const [n, r] of [["1", a], ["2", b], ["3", c], ["5", e], ["6", f]]) {
  if (r.g1.includes("fail")) fail.push(n + ": G1 fail");
  if (r.g3.includes("fail")) fail.push(n + ": G3 fail");
}

console.log("\n=== RESULT ===");
console.log(fail.length ? "FAIL: " + fail.join("; ") : "ALL 8 CHECKS PASSED");
process.exit(fail.length ? 1 : 0);
