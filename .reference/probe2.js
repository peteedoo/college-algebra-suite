#!/usr/bin/env node
'use strict';
const fs = require('fs');
const html = fs.readFileSync('/home/faulty/projects/college-algebra-suite/dashboard.html', 'utf8');
function jb(id) { const t = '<script id="' + id + '" type="application/json">'; const i = html.indexOf(t); const j = html.indexOf('</script>', i); return html.slice(i + t.length, j).trim(); }
const sStart = html.lastIndexOf('<script>'); const sEnd = html.lastIndexOf('</script>');
let engine = html.slice(sStart + 8, sEnd); engine = engine.slice(0, engine.indexOf('// Startup Initialization'));
function el(t) { return { textContent: t || '', innerHTML: '', value: '', style: {}, classList: { toggle() { return false; }, add() {}, remove() {}, contains() { return false; } }, addEventListener() {}, setAttribute() {}, getAttribute() { return null; }, appendChild() {}, querySelector() { return null; }, querySelectorAll() { return []; } }; }
const els = new Map(); const document = { getElementById(id) { if (!els.has(id)) els.set(id, el('')); return els.get(id); }, createElement() { return el(''); }, querySelector() { return null; }, querySelectorAll() { return []; }, addEventListener() {}, body: { appendChild() {} } };
els.set('embedded-data', el(jb('embedded-data'))); els.set('database-data', el(jb('database-data')));

const P = `
// 1. why does (x^2 + 12x) + (y^2 - 14y) = 5 fail?
var t1 = parseEquationSyntax('(x^2 + 12x) + (y^2 - 14y) = 5');
console.log('1. conic grouped:', JSON.stringify(t1 && t1.type));
var c1raw = '(x^2 + 12x) + (y^2 - 14y) = 5'.replace(/\\s+/g, '').replace(/\\(([^()]+)\\)/g, '$1');
console.log('   flattened:', c1raw);
try { console.log('   conicStd:', JSON.stringify(parseConicGeneralStd && parseConicGeneralStd('(x^2 + 12x) + (y^2 - 14y) = 5'))); } catch(e) { console.log('   conicStd ERR:', e.message); }

// 2. exp_eq e-base chain
var t2 = parseEquationSyntax('((1)/(e))^(-x) = ((1)/(e^3))^(x + 1)');
console.log('2. exp e-chain:', JSON.stringify(t2 && t2.type), JSON.stringify(t2 && t2.xStr));

// 3. log_expr vs log_eq2 order: log(2x+1)+log 3=log(5x+6)
var t3 = parseEquationSyntax('log(2x + 1) + log 3 = log(5x + 6)');
console.log('3. log-sum type:', JSON.stringify(t3 && t3.type), JSON.stringify(t3 && (t3.roots||t3.value)));
// what did 10a see?
var ls = 'log(2x + 1) + log 3 = log(5x + 6)';
console.log('   logSrc norm:', JSON.stringify(ls.replace(/^x\\s*=\\s*(?=[+-]?\\d*\\.?\\d*\\s*(?:ln|log)\\b)/i, '')));

// 4. log_2 16 (no rhs) — eval or expand?
var t4 = parseEquationSyntax('log_2 16');
console.log('4. log_2 16:', JSON.stringify(t4 && t4.type), JSON.stringify(t4 && t4.mode), JSON.stringify(t4 && t4.value));

// 5. log 10^(-7) parseConstValue power support
console.log('5. parseConstValue 10^(-7):', JSON.stringify(parseConstValue && parseConstValue('10^(-7)')));

// 6. the artifact false-positive: render PW 3.5 sheet, find what matched
var md = answersData['Pre-work 3.5 Rational Functions Graphs and Applica - Answers.md'];
var rendered = renderMarkdownToHtml(md);
var m = rendered.match(/.{30}(=\\s*(?:undefined|NaN)\\b|>(?:undefined|NaN)<\\/|(?:undefined|NaN)\\s*<\\/).{10}/s);
console.log('6. artifact match:', m ? JSON.stringify(m[0]) : 'NONE');

// 7. Q3 PW 4.1 initialExpr
Object.keys(originalCardStates).forEach(function(k){delete originalCardStates[k];});
var md7 = answersData['Pre-work 4.1 Inverse Functions - Answers.md'];
var secs = md7.split(/(?=\\n\\*\\s+\\*\\*Question\\s+\\d+:?|\\n\\*\\s+\\*\\*Q\\d+:?|\\n###\\s+\\*?\\*?Questions?\\s+)/i);
parseQuestionCard(secs[1], 1);
console.log('7. PW4.1 Q1 expr:', JSON.stringify((originalCardStates['1']||{}).initialExpr));
// Q3:
Object.keys(originalCardStates).forEach(function(k){delete originalCardStates[k];});
parseQuestionCard(secs[4] || secs[3], 3);
console.log('   Q3-ish expr:', JSON.stringify((originalCardStates['3']||{}).initialExpr));

// 8. PW 4.1 Q12 f(-4) = 16; f(4) = 16
console.log('8. f(-4)=16;f(4)=16:', JSON.stringify(parseEquationSyntax('f(-4) = 16; f(4) = 16')));

// 9. Q16 PW1.3 6 - isqrt(5)
console.log('9. 6 - isqrt(5); 6 + isqrt(5):', JSON.stringify(parseEquationSyntax('6 - isqrt(5); 6 + isqrt(5)')));
console.log('10. (1 + ((1)/(n)))^n:', JSON.stringify(parseEquationSyntax('(1 + ((1)/(n)))^n')));
console.log('11. log_sqrt(5) 625 = 8:', JSON.stringify(parseEquationSyntax('log_sqrt(5) 625 = 8')));
console.log('12. 5log_4 x - 6log_4 y:', JSON.stringify(parseEquationSyntax('5log_4 x - 6log_4 y') && parseEquationSyntax('5log_4 x - 6log_4 y').type));
console.log('13. 2log_b(z + 2) + log_b(3z + 3):', JSON.stringify(parseEquationSyntax('2log_b(z + 2) + log_b(3z + 3)') && parseEquationSyntax('2log_b(z + 2) + log_b(3z + 3)').type));
`;
new Function('document', 'window', engine + P)(document, { devicePixelRatio: 1 });