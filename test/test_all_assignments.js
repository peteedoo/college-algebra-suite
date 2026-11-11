#!/usr/bin/env node
/**
 * test_all_assignments.js — automated headless verification harness.
 *
 * Loads the REAL production engine (the <script> inside dashboard.html),
 * stubs the DOM, and drives every question of every assignment sheet plus
 * the full SQLite catalog through the live pipeline:
 *
 *   parseQuestionCard -> extractGraphableFromQuestion / extractInitialEditableExpr
 *                     -> parseEquationSyntax -> runToolOnParsed
 *                     -> buildGraphDataFromParsed
 *
 * PASS classes (every question must land in exactly one):
 *   ast           — typed AST + tool output (+ graph data where graphable)
 *   compile-graph — no AST, but compiles to a real rendered curve
 *   info-*        — conceptual: prose / answer-echo / notation / applet
 *
 * Boundary conditions (per the hardening spec):
 *   B1 rational-inequality poles ALWAYS bound OPEN intervals
 *   B2 inequality endpoints render as integers or exact p/q fractions
 *   B3 t-variable (projectile) inequalities report a Time Period
 *   B4 rendered <span class="frac"> chips keep "/" when re-extracted
 *   B5 solver output matches the sheet's stated interval / solution set
 *
 * Escape-depth note: TESTS is a template literal eval'd a second time by
 * new Function, so a regex \s inside TESTS is written \\s at file level.
 *
 * Exit 0 iff every check passes. Writes test/report.json.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'dashboard.html'), 'utf8');

function jsonBlock(id) {
  const tag = '<script id="' + id + '" type="application/json">';
  const i = html.indexOf(tag);
  if (i < 0) throw new Error('missing embedded block: ' + id);
  const j = html.indexOf('</script>', i);
  return html.slice(i + tag.length, j).trim();
}

const sStart = html.lastIndexOf('<script>');
const sEnd = html.lastIndexOf('</script>');
let engine = html.slice(sStart + '<script>'.length, sEnd);
const cut = engine.indexOf('// Startup Initialization');
if (cut < 0) throw new Error('cannot find startup marker');
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

const TESTS = `
var __R = { totals: { questions: 0, ast: 0, compileGraph: 0, tool: 0, graph: 0,
                     info: 0, sheetInterval: 0, omni: 0, omniParse: 0 },
            pass: {}, assignments: {}, boundary: {}, failures: [],
            infoList: [] };
(function () {
  var R = __R, F = R.failures;
  R.pass = { ast: 0, 'compile-graph': 0, 'info-prose': 0, 'info-echo': 0,
             'info-notation': 0, 'info-applet': 0 };
  function fail(file, q, kind, detail) {
    F.push({ file: file, q: String(q), kind: kind,
             detail: String(detail == null ? '' : detail).slice(0, 260) });
  }

  var GRAPHABLE = { quadratic: 1, quad_vertex: 1, circle_std: 1, circle_gen: 1,
    ellipse: 1, hyperbola: 1, rational: 1, rat_ineq: 1, synthetic: 1,
    polynomial: 1, poly_ineq: 1, exp_func: 1, log_func: 1, system_2x2: 1,
    abs: 1, abs_double: 1, two_points: 1, poly_points: 1, log_eval: 1,
    linear: 1, complex_verify_quad: 1, sqrt_func: 1, abs_func: 1,
    exp_eq: 1, log_eq2: 1 };

  function normIv(s) {
    // backslashes + backticks die first so LaTeX words match plainly
    var t = String(s)
      .split(String.fromCharCode(92)).join('')
      .split(String.fromCharCode(96)).join('')
      .replace(/\\*\\*/g, '')
      .replace(/\\u221E/g, 'inf')
      .replace(/\\u222A/g, 'U')
      .replace(/\\u2205/g, 'EMPTY')
      .replace(/[\\u2212\\u2013\\u2014]/g, '-');
    t = t.replace(/\\s+/g, '').toLowerCase();
    return t.replace(/infty/g, 'inf')
            .replace(/cup/g, 'u')
            .replace(/varnothing/g, 'empty')
            .replace(/emptyset/g, 'empty')
            .replace(/empty/g, 'empty')
            .replace(/le(?![a-z])/g, '<=')
            .replace(/ge(?![a-z])/g, '>=');
  }
  function ivTokens(s) {
    var out = String(s).match(/[\\[({][^\\[(){}]*,[^\\])}]*[\\])}]/g) || [];
    return out.map(normIv).filter(Boolean);
  }
  function hasInterval(s) {
    return ivTokens(s).length > 0 || normIv(s).indexOf('EMPTY') >= 0;
  }

  function classifyInfo(expr) {
    var e = String(expr || '').trim();
    if (!e) return 'info-applet';
    if (/^\\d+(?:\\.\\d+)?\\s*%$/.test(e.replace(/\\s+/g, ''))) return 'info-echo';
    if (/^_+$/.test(e)) return 'info-echo';
    if (!/[a-zA-Z]/.test(e)) return 'info-echo';
    if (/\\\\neq|\\\\pm|\\\\bar|\\\\iff|\\\\text|\\\\quad|\\\\stackrel|\\\\to/.test(e)) return 'info-notation';
    if (/f\\^\\s*\\(?-1\\)?/.test(e)) return 'info-notation';
    if (/^[+-]?[\\d.]+\\s*(?:<|<=)\\s*[^|]+(?:<|<=)\\s*[+-]?[\\d.]+$/.test(e) && !/\\|/.test(e)) {
      return 'info-notation';
    }
    if (!/\\d/.test(e)) return 'info-echo';
    if (/^(?:[fghpqr]\\(x\\)|y)\\s*=\\s*[-\\d.]+$/i.test(e)) return 'info-echo';
    if (/[A-Za-z]{3,}[\\s,]+[A-Za-z]{3,}[\\s,]+[A-Za-z]{3,}/.test(e) && !/[=^\\/|]/.test(e)) {
      return 'info-prose';
    }
    // __H4__: definitional echoes — blank fills, i-sqrt notation,
    // f^(-1) pairs, y = f(x) usage, e-limit definition
    if (/_{3,}/.test(e)) return 'info-prose';
    if (/isqrt/.test(e)) return 'info-notation';
    if (/1\\/n\\)\\)\\^n|\\(1\\s*\\+/.test(e)) return 'info-notation';
    if (/f\\(-?\\d+\\)\\s*=\\s*\\d+\\s*;/.test(e)) return 'info-notation';
    if (/^y\\s*=\\s*f\\(x\\)/i.test(e)) return 'info-notation';
    if (/^\s*a\^\s*(x|2|n)\s*$/i.test(e)) return 'info-notation';
    return null;
  }

  function tries(x, fn) { try { return fn(); } catch (e) { return null; } }

  var fileNames = Object.keys(answersData);
  var catalogByAssignment = {};
  (courseDatabase.catalog || []).forEach(function (c) {
    (catalogByAssignment[c.assignment] = catalogByAssignment[c.assignment] || []).push(c);
  });

  fileNames.forEach(function (fname) {
    var md = answersData[fname];
    var name = fname.replace(' - Answers.md', '');
    var A = { questions: 0, pass: {}, info: {} };
    R.assignments[name] = A;

    try {
      var rendered = renderMarkdownToHtml(md);
      if (/=\\s*(?:undefined|NaN)\\b/.test(rendered)) {
        fail(name, 'RENDER', 'render-js-artifact', JSON.stringify(rendered.match(/.{40}(?:undefined|NaN).{20}/s)));
      }
    } catch (e) { fail(name, 'RENDER', 'render-crash', e.message); }

    var rawSections = md.split(/(?=\\n\\*\\s+\\*\\*Question\\s+\\d+:?|\\n\\*\\s+\\*\\*Q\\d+:?|\\n###\\s+\\*?\\*?Questions?\\s+)/i);
    var qIndex = 0;

    function processSec(secRaw, idx) {
      var sec = String(secRaw).trim();
      if (!sec) return;
      var titleM = sec.match(/(?:###\\s+\\*?\\*?(Questions?[^\\n*#]+)\\*?\\*?|\\*\\s+\\*?\\*?(question\\s+\\d+[a-za-z0-9\\u2013-]*:?|Q\\d+:?)\\*?\\*?)/i);
      if (!titleM) { fail(name, idx, 'no-title', sec.slice(0, 60)); return; }
      var qTitle = (titleM[1] || titleM[2] || '').replace(/:$/, '').trim();
      var numM = qTitle.match(/\\b(?:Question|Q)\\s*(\\d+)\\b/i);
      var key = numM ? numM[1] : String(idx);

      Object.keys(originalCardStates).forEach(function (k) { delete originalCardStates[k]; });
      try { parseQuestionCard(sec, idx); }
      catch (e) { fail(name, key, 'card-crash', e.message); return; }
      var st = originalCardStates[key];
      if (!st) { fail(name, key, 'card-nokey', qTitle); return; }

      var expr = (st.initialExpr || '').trim();
      var graphEq = (st.graphEq || '').trim();
      A.questions++; R.totals.questions++;

      var info = classifyInfo(expr);
      if (info) {
        R.pass[info]++; R.totals.info++;
        A.info[info] = (A.info[info] || 0) + 1;
        R.infoList.push({ file: name, q: key, cls: info, expr: expr.slice(0, 100) });
        return;
      }

      var p = null;
      try { p = parseEquationSyntax(expr); }
      catch (e) { fail(name, key, 'PARSE-crash', e.message); return; }

      if (p) {
        if (typeof p.type !== 'string') { fail(name, key, 'PARSE-noType', expr); return; }
        var tool = null;
        try { tool = runToolOnParsed(p, expr); }
        catch (e) { fail(name, key, 'TOOL-crash', p.type + ' :: ' + e.message); return; }
        if (!tool || !tool.title || !tool.outputVal) {
          fail(name, key, 'TOOL-null', p.type + ' :: ' + expr); return;
        }
        R.totals.tool++;
        if (GRAPHABLE[p.type]) {
          var gd = null;
          try { gd = buildGraphDataFromParsed(p, expr); }
          catch (e) { fail(name, key, 'GRAPH-crash', e.message); return; }
          if (!gd) { fail(name, key, 'GRAPH-null', p.type + ' :: ' + expr); return; }
          R.totals.graph++;
        }
        R.pass.ast++; R.totals.ast++;
        if (p.type === 'poly_ineq' || p.type === 'rat_ineq') checkIneq(name, key, p, sec, expr);
        if (p.type === 'abs' || p.type === 'abs_double') checkAbs(name, key, sec, tool);
        return;
      }

      var fn1 = null, fn2 = null;
      try { fn1 = expr ? compileMathFunction(expr) : null; } catch (e) { fn1 = null; }
      try { fn2 = graphEq ? compileMathFunction(graphEq) : null; } catch (e) { fn2 = null; }
      var realCurve = fn1 && tries(null, function () { return isFinite(fn1(1.3) + fn1(-0.7)); });
      var geCurve = fn2 && tries(null, function () { return isFinite(fn2(1.3) + fn2(-0.7)); });
      if ((realCurve && (graphEq || isFinite(fn1(0)))) || (geCurve && graphEq)) {
        R.pass['compile-graph']++; R.totals.compileGraph++;
        return;
      }
      fail(name, key, 'UNSOLVED-solvable-shape', expr);
    }

    for (var i = 1; i < rawSections.length; i++) {
      var sec2 = rawSections[i];
      var s2 = sec2.trim();
      if (!s2) continue;
      var groupMatch = s2.match(/^###\\s+\\*?\\*?(questions?\\s+[^\\n*#]+)\\*?\\*?/i);
      if (groupMatch && !s2.includes('* **Problem:')) {
        var subItems = s2.split(/(?=\\n\\*\\s+\\*\\*question|\\n\\*\\s+\\*\\*Q\\d+)/i);
        for (var j = 1; j < subItems.length; j++) processSec(subItems[j], ++qIndex);
        continue;
      }
      processSec(sec2, ++qIndex);
    }
  });

  function checkIneq(name, key, p, sec, expr) {
    var isRat = p.type === 'rat_ineq';
    var numC = isRat ? p.numCoeffs : p.coeffs;
    var denC = isRat ? p.denCoeffs : [1];
    var sc = null;
    try { sc = solveSignChartInequalityJS(numC, denC, p.op); }
    catch (e) { fail(name, key, 'INEQ-crash', e.message); return; }

    if (isRat) {
      R.boundary.poleChecks = (R.boundary.poleChecks || 0) + sc.denRoots.length;
      sc.denRoots.forEach(function (dr) {
        sc.intervals.forEach(function (iv) {
          if (Math.abs(iv.from - dr) < 1e-6 && iv.inclusiveFrom)
            fail(name, key, 'POLE-closed-from', 'pole ' + dr + ' interval ' + sc.intervalStr);
          if (Math.abs(iv.to - dr) < 1e-6 && iv.inclusiveTo)
            fail(name, key, 'POLE-closed-to', 'pole ' + dr + ' interval ' + sc.intervalStr);
        });
      });
    }

    var ends = [];
    sc.intervals.forEach(function (iv) {
      if (isFinite(iv.from)) ends.push(iv.from);
      if (isFinite(iv.to)) ends.push(iv.to);
    });
    (sc.isolatedPoints || []).forEach(function (e2) { ends.push(e2); });
    ends.forEach(function (e2) {
      var s2 = formatEndpoint(e2);
      if (/\\.\\d/.test(s2)) fail(name, key, 'FRAC-float', 'endpoint ' + e2 + ' -> "' + s2 + '" in ' + sc.intervalStr);
    });

    if (p.variable === 't') {
      R.boundary.tChecks = (R.boundary.tChecks || 0) + 1;
      var tool = null;
      try { tool = runToolOnParsed(p, expr); } catch (e) { tool = null; }
      if (!/Time Period/.test(String(tool && tool.outputVal)))
        fail(name, key, 'T-noperiod', expr);
    }

    var ansM = sec.match(/\\*\\s+\\*\\*Answers?:\\*\\*\\s*(.*?)(?=\\n\\*\\s+\\*\\*|\\n---|$)/s);
    if (!ansM) return;
    var sheetN = normIv(ansM[1]);
    var toolN = normIv(sc.intervalStr);
    if (!hasInterval(ansM[1])) return;
    R.boundary.sheetChecks = (R.boundary.sheetChecks || 0) + 1;
    if (sheetN.indexOf(toolN) === -1) {
      var pts = [];
      sc.intervals.forEach(function (iv) {
        if (isFinite(iv.from) && isFinite(iv.to)) pts.push(iv.from, iv.to);
      });
      var tOk = pts.length === 2 && pts.every(function (v) {
        return sheetN.indexOf(String(Number(v.toFixed(2))) + 'sec') !== -1;
      });
      if (!(p.variable === 't' && tOk))
        fail(name, key, 'SHEET-interval', 'tool="' + sc.intervalStr + '" sheet="' + String(ansM[1]).trim().slice(0, 160) + '"');
      else R.totals.sheetInterval++;
    } else R.totals.sheetInterval++;
  }

  function checkAbs(name, key, sec, tool) {
    if (!tool) return;
    var ansM = sec.match(/\\*\\s+\\*\\*Answers?:\\*\\*\\s*(.*?)(?=\\n\\*\\s+\\*\\*|\\n---|$)/s);
    if (!ansM) return;
    var sheetN = normIv(ansM[1]);
    var partM = String(tool.outputVal).match(/Part 2 \\(Interval Notation\\):\\*\\*<\\/strong>\\s*<strong>([^<]*)<\\/strong>/s)
            || String(tool.outputVal).match(/<strong>\\{([^<]*)\\}<\\/strong>/s);
    if (!partM) return;
    var toolIv = normIv(partM[1]);
    if (!hasInterval(ansM[1])) return;
    R.boundary.absSheetChecks = (R.boundary.absSheetChecks || 0) + 1;
    if (sheetN.indexOf(toolIv) === -1)
      fail(name, key, 'SHEET-abs', 'tool="' + toolIv + '" sheet="' + String(ansM[1]).trim().slice(0, 160) + '"');
    else R.totals.sheetInterval++;
  }

  (courseDatabase.catalog || []).forEach(function (item) {
    var ge = '';
    try {
      ge = extractGraphableFromQuestion(item.problem, item.answer,
                                        (item.equations && item.equations[0]) || '', '');
    } catch (e) { fail(item.assignment, item.qNum, 'OMNI-crash', e.message); return; }
    if (!ge) return;
    R.totals.omni++;
    var p = null, gd = null;
    try { p = parseEquationSyntax(ge); } catch (e) { fail(item.assignment, item.qNum, 'OMNI-parse-crash', e.message); return; }
    if (p) {
      R.totals.omniParse++;
      try { gd = buildGraphDataFromParsed(p, ge); } catch (e) { gd = null; }
      if (!gd) {
        var fnG = null;
        try { fnG = compileMathFunction(ge); } catch (e) { fnG = null; }
        if (!fnG) fail(item.assignment, item.qNum, 'OMNI-graph-null', ge);
      }
    } else {
      var fnG2 = null;
      try { fnG2 = compileMathFunction(ge); } catch (e) { fnG2 = null; }
      var real = fnG2 && tries(null, function () { return isFinite(fnG2(1.3) + fnG2(-0.7)); });
      // generic placeholder notation (e.g. a^x) is conceptual, not solvable
      var g2 = String(ge).split(' ').join('').toLowerCase();
      var isPh = g2.length === 3 && g2.charCodeAt(0) >= 97 && g2.charCodeAt(0) <= 122 &&
                 g2.charAt(1) === String.fromCharCode(94) && g2.charCodeAt(2) >= 97 && g2.charCodeAt(2) <= 122;
      if (!real && isPh) { R.pass['info-notation']++; R.totals.info++; return; }
      if (!real) fail(item.assignment, item.qNum, 'OMNI-unusable', ge);
    }
  });

  // ---- explicit boundary unit tests ----
  var B = R.boundary;
  function u(label, fn) {
    try { fn(); B[label] = 'pass'; }
    catch (e) { B[label] = 'FAIL: ' + e.message; fail('UNIT', label, 'UNIT', e.message); }
  }
  function eq(label, a, b) {
    if (a !== b) throw new Error(label + ': ' + JSON.stringify(a) + ' !== ' + JSON.stringify(b));
  }

  u('B1-pole-open-rat-ineq', function () {
    var p = parseEquationSyntax('(x - 2)/(x + 3) > 1');
    if (!p || p.type !== 'rat_ineq') throw new Error('not rat_ineq: ' + JSON.stringify(p && p.type));
    var sc = solveSignChartInequalityJS(p.numCoeffs, p.denCoeffs, p.op);
    eq('pole x=-3 open', normIv(sc.intervalStr), normIv('(-INF, -3)'));
    eq('numerator has no zero', sc.numRoots.length, 0);
  });
  u('B2-exact-fraction', function () {
    var p = parseEquationSyntax('5x^2 + 3x <= 2');
    var sc = solveSignChartInequalityJS(p.coeffs, [1], p.op);
    eq('interval exact fractions', normIv(sc.intervalStr), normIv('[-1, 2/5]'));
    eq('formatEndpoint(0.4)', formatEndpoint(0.4), '2/5');
    eq('formatEndpoint(-1)', formatEndpoint(-1), '-1');
  });
  u('B3-t-variable', function () {
    var p = parseEquationSyntax('-16t^2 + 36t + 5 >= 25');
    if (!p || p.type !== 'poly_ineq' || p.variable !== 't')
      throw new Error('t mis-parsed: ' + JSON.stringify(p && p.type) + ' var=' + JSON.stringify(p && p.variable));
    var tool = runToolOnParsed(p, '-16t^2 + 36t + 5 >= 25');
    if (!/between \\(and inclusive of\\) 1 sec and 1\\.25 sec/i.test(String(tool.outputVal)))
      throw new Error('time period wrong: ' + String(tool.outputVal).slice(0, 200));
  });
  u('B4-frac-span-slash', function () {
    var T = function (s) { return { nodeType: 3, textContent: s }; };
    var frac = {
      nodeType: 1,
      classList: { contains: function (c) { return c === 'frac'; } },
      querySelector: function (sel) { return sel === '.num' ? T('3') : T('4'); },
      childNodes: [],
    };
    var out = extractDomMathText(frac);
    if (out !== '((3)/(4))') throw new Error('frac DOM lost "/": ' + JSON.stringify(out));
    var fm = formatMath('\\\\frac{3}{4}');
    if (fm.indexOf('class="frac"') < 0 || fm.indexOf('class="num"') < 0 || fm.indexOf('class="den"') < 0)
      throw new Error('formatMath lost frac spans');
    eq('parse 3/4', parsePolyCoeffs('3/4')[0], 0.75);
  });
  u('B5-sign-chart-closure', function () {
    var p = parseEquationSyntax('((x + 11)(x - 13))/(x + 9) <= 0');
    if (!p || p.type !== 'rat_ineq') throw new Error('mis-parsed: ' + JSON.stringify(p && p.type));
    var sc = solveSignChartInequalityJS(p.numCoeffs, p.denCoeffs, p.op);
    eq('sheet interval', normIv(sc.intervalStr), normIv('(-INF, -11] U (-9, 13]'));
  });
  u('V4-exp-equations', function () {
    var cases = [
      ['256^(3x) = 64^(x + 2)', '2/3'],
      ['e^(8x - 1) = (e^6)^x', '1/2'],
      ['(sqrt(2))^(x + 8) = 16^x', '8/7'],
      ['16^(3x - 3) = 64^(x + 2)', '4'],
      ['((5)/(2))^x = ((8)/(125))', '-3'],
      ['((1)/(e))^(-x) = ((1)/(e^3))^(x + 1)', '-3/4'],
      ['2^x = ((1)/(16))', '-4'],
      ['((1)/(9))^x = 81', '-2'],
      ['6^x = ((1)/(216))', '-3'],
      ['((1)/(4))^x = 64', '-3']
    ];
    cases.forEach(function (c) {
      var p = parseEquationSyntax(c[0]);
      if (!p || (p.type !== 'exp_eq' && p.type !== 'exp_func')) throw new Error('exp eq not parsed: ' + c[0] + ' -> ' + JSON.stringify(p && p.type));
      eq('exp_eq ' + c[0], String(p.type === 'exp_func' ? Math.round(p.solX * 1e6) / 1e6 : p.xStr), c[1]);
    });
    var mix = parseEquationSyntax('0.06 * (1.16)^x = 6');
    if (!mix || (mix.type !== 'exp_eq' && mix.type !== 'exp_func')) throw new Error('mixed form: ' + JSON.stringify(mix && mix.type));
    eq('mixed 0.06(1.16)^x = 6', String(mix.type === 'exp_func' ? Math.round(mix.solX * 1e3) / 1e3 : mix.xStr), '31.028');
    var f7 = parseEquationSyntax('3 * 3^(x-2) + 1 = 103');
    if (!f7 || (f7.type !== 'exp_eq' && f7.type !== 'exp_func')) throw new Error('mixed 3*3^(x-2): ' + JSON.stringify(f7 && f7.type));
    eq('mixed 3*3^(x-2)+1=103', String(f7.type === 'exp_func' ? Math.round(f7.solX * 1e3) / 1e3 : f7.xStr), '5.21');
  });
  u('V4-log-equations', function () {
    var a1 = parseEquationSyntax('log_5 x = 2');
    if (!a1 || a1.type !== 'log_func') throw new Error('log_5 x = 2: ' + JSON.stringify(a1 && a1.type));
    eq('log_5 x = 2', a1.solX, 25);
    var a2 = parseEquationSyntax('log_36 x = ((3)/(2))');
    eq('log_36 x = 3/2', a2.solX, 216);
    var a3 = parseEquationSyntax('log_1/4(x + 2) = -3');
    eq('log_1/4(x+2) = -3', a3.solX, 62);
    var a4 = parseEquationSyntax('log_(x + 7) 13 = 1');
    if (!a4 || a4.type !== 'log_eq2') throw new Error('var base: ' + JSON.stringify(a4 && a4.type));
    eq('log_(x + 7) 13 = 1', a4.roots[0], 6);
  });
  u('V4-conic-general', function () {
    var c1 = parseEquationSyntax('(x^2 + 12x) + (y^2 - 14y) = 5');
    if (!c1 || c1.type !== 'circle_gen') throw new Error('grouped form: ' + JSON.stringify(c1 && c1.type));
    var t1 = runToolOnParsed(c1, '');
    var plain1 = String(t1.outputVal).replace(/<[^>]+>/g, '');
    if (plain1.indexOf('(-6, 7)') < 0 || plain1.indexOf('9.49') < 0)
      throw new Error('center (-6, 7), r = sqrt(90) ~ 9.49: ' + plain1.slice(0, 160));
    var c2 = parseEquationSyntax('4x^2 + 4x + 4y^2 - 32y - 79 = 0');
    var t2 = runToolOnParsed(c2, '');
    var plain2 = String(t2.outputVal).replace(/<[^>]+>/g, '');
    if ((plain2.indexOf('(-0.5, 4)') < 0 && plain2.indexOf('(-1/2, 4)') < 0) || plain2.indexOf('Radius: 6') < 0)
      throw new Error('center (-0.5, 4), r = 6: ' + plain2.slice(0, 200));
  });
  u('V4-log-sum', function () {
    var e1 = parseEquationSyntax('log(2x + 1) + log 3 = log(5x + 6)');
    if (!e1 || e1.type !== 'log_eq2') throw new Error('log sum: ' + JSON.stringify(e1 && e1.type));
    eq('log(2x+1)+log3=log(5x+6)', e1.roots[0], 3);
    var e2 = parseEquationSyntax('ln(4 - x) + ln(-3 - x) = ln(2 - 6x)');
    eq('ln(4-x)+ln(-3-x)=ln(2-6x)', e2.roots[0], -7);
    var e3 = parseEquationSyntax('log_5(x + 10) + log_5(x - 10) = 3');
    eq('log_5(x+10)+log_5(x-10)=3', e3.roots[0], 15);
  });
  u('V4-log-expr-eval', function () {
    var v1 = parseEquationSyntax('log 10^(-7)');
    if (!v1 || v1.type !== 'log_expr' || v1.mode !== 'eval') throw new Error('log10^-7: ' + JSON.stringify(v1 && v1.type) + '/' + (v1 && v1.mode));
    eq('log 10^-7 = -7', v1.value, -7);
    var v2 = parseEquationSyntax('5log_4 x - 6log_4 y');
    if (!v2 || v2.type !== 'log_expr') throw new Error('5log4x-6log4y: ' + JSON.stringify(v2 && v2.type));
  });

  try {
    var hits = searchCourseCatalog('vertex', null);
    if (!hits.length) fail('SEARCH', 'vertex', 'SEARCH-empty', '');
    var none = searchCourseCatalog('zzzzqqqq', null);
    if (none.length) fail('SEARCH', 'garbage', 'SEARCH-noise', none.length + ' hits');
  } catch (e) { fail('SEARCH', 'smoke', 'SEARCH-crash', e.message); }

  R.totals.failures = F.length;
})();
return JSON.parse(JSON.stringify(__R));
`;

const run = new Function('document', 'window', engine + TESTS);
const report = run(document, window);

fs.writeFileSync(path.join(__dirname, 'report.json'), JSON.stringify(report, null, 1));

const t = report.totals;
console.log('=== HEADLESS ENGINE TEST - dashboard.html ===');
console.log('sheets:          ' + Object.keys(report.assignments).length);
console.log('questions:       ' + t.questions);
console.log('  ast solved:      ' + report.pass.ast);
console.log('  compile-graph:  ' + report.pass['compile-graph']);
console.log('  informational:  ' + t.info + '  (prose ' + report.pass['info-prose'] + ', echo ' + report.pass['info-echo'] + ', notation ' + report.pass['info-notation'] + ', applet ' + report.pass['info-applet'] + ')');
console.log('  tool outputs:   ' + t.tool);
console.log('  graph data:     ' + t.graph);
console.log('omni cards:      ' + t.omni + ' (ast ' + t.omniParse + ')');
console.log('sheet matches:   ' + t.sheetInterval);
console.log('boundary:        ' + JSON.stringify(report.boundary));
console.log('FAILURES:        ' + report.failures.length);

const byKind = {};
report.failures.forEach(f => { byKind[f.kind] = (byKind[f.kind] || 0) + 1; });
console.log('failure kinds:   ' + JSON.stringify(byKind));
report.failures.slice(0, 40).forEach(f =>
  console.log('  [' + f.kind + '] ' + f.file + ' :: Q' + f.q + ' - ' + f.detail));
if (report.failures.length > 40)
  console.log('  ... ' + (report.failures.length - 40) + ' more (see test/report.json)');

process.exit(report.failures.length === 0 ? 0 : 1);