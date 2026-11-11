#!/usr/bin/env node
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = '/home/faulty/projects/college-algebra-suite';
const html = fs.readFileSync(path.join(ROOT, 'dashboard.html'), 'utf8');

function jsonBlock(id) {
  const tag = `<script id="${id}" type="application/json">`;
  const i = html.indexOf(tag);
  const j = html.indexOf('</script>', i);
  return html.slice(i + tag.length, j).trim();
}
const sStart = html.lastIndexOf('<script>');
const sEnd = html.lastIndexOf('</script>');
let engine = html.slice(sStart + '<script>'.length, sEnd);
console.log('engine length:', engine.length);
console.log('has parseQuestionCard:', engine.includes('function parseQuestionCard'));
console.log('has originalCardStates decl:', /const originalCardStates/.test(engine));
console.log('has Startup marker:', engine.indexOf('// Startup Initialization'));
console.log('engine tail:', JSON.stringify(engine.slice(-120)));

const cut = engine.indexOf('// Startup Initialization');
engine = engine.slice(0, cut);

function makeEl(text) {
  return {
    textContent: text || '', innerHTML: '', value: '', style: {},
    classList: { toggle() { return false; }, add() {}, remove() {}, contains() { return false; } },
    addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
    appendChild() {}, querySelector() { return null; }, querySelectorAll() { return []; },
  };
}
const els = new Map();
const document = {
  getElementById(id) { if (!els.has(id)) els.set(id, makeEl('')); return els.get(id); },
  createElement() { return makeEl(''); },
  querySelector() { return null; }, querySelectorAll() { return []; },
  addEventListener() {}, body: { appendChild() {} },
};
els.set('embedded-data', makeEl(jsonBlock('embedded-data')));
els.set('database-data', makeEl(jsonBlock('database-data')));
const window = { devicePixelRatio: 1, addEventListener() {} };

const PROBE = `
(function(){
  var answers = Object.keys(answersData);
  console.log('sheets loaded:', answers.length);
  var md = answersData[answers[0]];
  var rawSections = md.split(/(?=\\n\\*\\s+\\*\\*Question\\s+\\d+:?|\\n\\*\\s+\\*\\*Q\\d+:?|\\n###\\s+\\*?\\*?Questions?\\s+)/i);
  console.log('sections:', rawSections.length);
  var sec = rawSections[1].trim();
  console.log('sec head:', JSON.stringify(sec.slice(0, 70)));
  console.log('originalCardStates keys BEFORE:', Object.keys(originalCardStates).length);
  var out = parseQuestionCard(sec, 1);
  console.log('return type:', typeof out, 'len:', (out||'').length);
  console.log('originalCardStates keys AFTER:', Object.keys(originalCardStates).length);
  console.log('keys:', Object.keys(originalCardStates).slice(0,10));
  for (var k in originalCardStates) { console.log('entry', k, JSON.stringify(originalCardStates[k]).slice(0,160)); break; }
  console.log('return html head:', JSON.stringify(String(out).slice(0, 160)));
})();
`;
const run = new Function('document', 'window', engine + PROBE);
run(document, window);