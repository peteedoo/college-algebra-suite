#!/usr/bin/env python3
"""
Dashboard Generator & Synchronizer with Database-Backed Equation Solver
Bundles all answer sheets and the structured course database directly into `dashboard.html`.
Allows typing ANY equation to automatically solve it with built-in tools AND find matching course materials.
"""

import os
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

ANSWERS_DIR = BASE_DIR / "assignments" / "Answers"
DASHBOARD_FILE = BASE_DIR / "dashboard.html"

try:
    import build_database
except ImportError:
    build_database = None

def get_all_answers():
    import re
    answers = {}
    if not ANSWERS_DIR.exists():
        return answers

    def sort_key(path_obj):
        name = path_obj.name
        m = re.search(r'(\d+)\.(\d+)', name)
        if m:
            ch, sec = int(m.group(1)), int(m.group(2))
            # Put Build Understanding first (0), then Pre-work (1) for the same section
            kind = 0 if "Build Understanding" in name else (1 if "Pre-work" in name else 2)
            return (0, ch, sec, kind, name)
        return (1, 99, 99, 0, name)

    for f in sorted(ANSWERS_DIR.iterdir(), key=sort_key):
        if f.suffix == ".md":
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    answers[f.name] = fp.read()
            except Exception as e:
                print(f"Error reading {f.name}: {e}")
    return answers

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MAT 1340 College Algebra: Database & Universal Equation Solver</title>
  <style>
    :root {
      --bg: #0b0f19;
      --surface: #151d30;
      --surface-card: #1c2640;
      --surface-hover: #263558;
      --border: #2a3b61;
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --accent: #10b981;
      --accent-glow: rgba(16, 185, 129, 0.25);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --code-bg: #090d16;
      --ans-bg: #042f2e;
      --ans-border: #14b8a6;
      --rule-bg: #1e1b4b;
      --rule-border: #818cf8;
      --tip-bg: #451a03;
      --tip-border: #f59e0b;
      --dyn-bg: #0f172a;
      --dyn-border: #38bdf8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { background: var(--bg); color: var(--text); display: flex; height: 100vh; overflow: hidden; }

    /* Sidebar */
    #sidebar {
      width: 340px;
      background: var(--surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      transition: margin-left 0.2s ease, width 0.2s ease;
    }
    #sidebar.collapsed {
      display: none;
    }
    .btn-sidebar-toggle {
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #38bdf8;
      padding: 6px 11px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.15s;
    }
    .btn-sidebar-toggle:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }
    .top-picker-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-left: auto;
      padding: 6px 0;
    }
    .top-picker-label {
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      white-space: nowrap;
    }
    .top-picker-select {
      background: #0b0f19;
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #f8fafc;
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 0.84rem;
      font-weight: 600;
      max-width: 340px;
      outline: none;
      cursor: pointer;
    }
    .top-picker-select:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-glow);
    }
    .btn-step-asgn {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 5px 9px;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-step-asgn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
    .sidebar-header {
      padding: 16px;
      border-bottom: 1px solid var(--border);
      background: rgba(11, 15, 25, 0.9);
    }
    .brand-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .brand-sub {
      font-size: 0.74rem;
      color: var(--text-muted);
      margin-top: 3px;
    }
    .sidebar-db-badge {
      display: inline-block;
      margin-top: 8px;
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 12px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
      font-weight: 600;
    }
    .search-box {
      width: 100%;
      margin-top: 10px;
      padding: 8px 12px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-size: 0.84rem;
      outline: none;
    }
    .search-box:focus { border-color: var(--primary); box-shadow: 0 0 0 2px var(--primary-glow); }

    .file-list {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }
    .file-item {
      padding: 10px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: flex-start;
      gap: 10px;
      margin-bottom: 4px;
      color: var(--text-muted);
      transition: all 0.15s;
      font-size: 0.82rem;
      line-height: 1.35;
    }
    .file-item:hover {
      background: var(--surface-hover);
      color: var(--text);
    }
    .file-item.active {
      background: #0284c7;
      color: #ffffff;
      font-weight: 600;
      box-shadow: 0 2px 8px var(--primary-glow);
    }

    /* Solvers Launcher Box */
    .solver-shortcuts {
      padding: 12px;
      border-top: 1px solid var(--border);
      background: rgba(11, 15, 25, 0.7);
    }
    .solver-shortcuts h3 {
      font-size: 0.72rem;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 8px;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
    }
    .shortcut-btns {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .btn-shortcut {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 6px 8px;
      border-radius: 5px;
      font-size: 0.74rem;
      cursor: pointer;
      text-align: left;
      transition: all 0.15s;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .btn-shortcut:hover {
      border-color: var(--primary);
      color: var(--primary);
      background: var(--surface-hover);
    }

    /* Main Area */
    #main {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* OMNI-SEARCH HEADER */
    .omni-container {
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      z-index: 10;
    }
    .omni-input-wrap {
      display: flex;
      align-items: center;
      background: var(--bg);
      border: 1.5px solid var(--border);
      border-radius: 8px;
      padding: 4px 14px;
      transition: all 0.15s;
    }
    .omni-input-wrap:focus-within {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-glow);
    }
    .omni-icon {
      font-size: 1.25rem;
      margin-right: 10px;
    }
    .omni-input {
      flex: 1;
      background: none;
      border: none;
      color: #ffffff;
      font-size: 1.05rem;
      font-family: ui-monospace, Menlo, monospace;
      padding: 8px 0;
      outline: none;
    }
    .omni-input::placeholder {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 0.92rem;
      color: #64748b;
    }
    .omni-clear-btn {
      background: rgba(255,255,255,0.1);
      border: none;
      color: var(--text-muted);
      border-radius: 50%;
      width: 22px;
      height: 22px;
      font-size: 0.75rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .omni-clear-btn:hover { color: #fff; background: rgba(255,255,255,0.2); }

    .omni-pills-bar {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 10px;
      overflow-x: auto;
      padding-bottom: 4px;
    }
    .omni-pills-label {
      font-size: 0.72rem;
      text-transform: uppercase;
      font-weight: 700;
      color: var(--text-muted);
      margin-right: 4px;
      white-space: nowrap;
    }
    .omni-pill {
      background: rgba(56, 189, 248, 0.08);
      border: 1px solid rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.74rem;
      cursor: pointer;
      font-family: ui-monospace, Menlo, monospace;
      white-space: nowrap;
      transition: all 0.15s;
    }
    .omni-pill:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }

    .tabs-header {
      background: rgba(21, 29, 48, 0.75);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      padding: 0 20px;
      gap: 12px;
    }
    .tab-btn {
      padding: 12px 18px;
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.9rem;
      font-weight: 500;
      border-bottom: 2px solid transparent;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: color 0.15s;
    }
    .tab-btn:hover { color: var(--text); }
    .tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); font-weight: 600; }

    .tab-content {
      flex: 1;
      overflow-y: auto;
      padding: 24px 36px;
    }

    /* OMNI QUERY RESULTS VIEW */
    #omniResultsView {
      max-width: 980px;
      margin: 0 auto;
      padding-bottom: 60px;
      display: none;
    }
    .omni-section-heading {
      font-size: 1.15rem;
      font-weight: 800;
      color: #38bdf8;
      margin: 20px 0 12px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .omni-tool-card {
      background: linear-gradient(145deg, #162035, #121929);
      border: 1.5px solid #0284c7;
      border-radius: 10px;
      padding: 22px;
      box-shadow: 0 4px 16px rgba(2, 132, 199, 0.2);
      margin-bottom: 24px;
    }
    .omni-tool-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding-bottom: 10px;
    }
    .omni-tool-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: #fde047;
    }
    .omni-match-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 18px;
      margin-bottom: 16px;
      transition: border 0.15s;
    }
    .omni-match-card:hover {
      border-color: var(--primary);
    }
    .match-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .match-source {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--primary);
    }
    .match-chapter {
      font-size: 0.75rem;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      padding: 2px 8px;
      border-radius: 10px;
      font-weight: 600;
    }

    /* Study Card & Markdown Display */
    .study-container {
      max-width: 960px;
      margin: 0 auto;
      padding-bottom: 60px;
    }
    .sheet-title {
      font-size: 1.85rem;
      color: #38bdf8;
      font-weight: 800;
      margin-bottom: 6px;
    }
    .sheet-meta {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-bottom: 24px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }
    .q-card {
      background: var(--surface-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 22px 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .q-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      padding-bottom: 10px;
      gap: 10px;
      flex-wrap: wrap;
    }
    .q-title-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .q-number {
      font-size: 1.15rem;
      font-weight: 700;
      color: #fde047;
    }
    .q-badge {
      font-size: 0.72rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .q-actions {
      display: flex;
      gap: 8px;
    }
    .btn-dyn-toggle {
      background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(16, 185, 129, 0.2));
      border: 1px solid #0284c7;
      color: #38bdf8;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s;
    }
    .btn-dyn-toggle:hover {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 0 10px var(--primary-glow);
    }
    .btn-solve-link {
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 0.76rem;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-solve-link:hover {
      border-color: var(--primary);
      color: var(--text);
    }

    .q-problem {
      font-size: 1.04rem;
      line-height: 1.6;
      color: #f8fafc;
      margin-bottom: 12px;
      padding: 8px 10px;
      border-radius: 6px;
      border: 1px dashed transparent;
      transition: all 0.15s;
    }
    .q-problem[contenteditable="true"]:hover {
      border-color: rgba(56, 189, 248, 0.45);
      background: rgba(15, 23, 42, 0.5);
    }
    .q-problem[contenteditable="true"]:focus {
      outline: none;
      border-color: #38bdf8;
      background: rgba(15, 23, 42, 0.85);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }

    .inline-editor-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      background: linear-gradient(90deg, rgba(14, 165, 233, 0.12), rgba(16, 185, 129, 0.08));
      border: 1px solid rgba(56, 189, 248, 0.35);
      border-radius: 8px;
      padding: 8px 12px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }
    .inline-editor-label {
      font-size: 0.76rem;
      font-weight: 700;
      color: #38bdf8;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      display: flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }
    .inline-live-input {
      flex: 1;
      min-width: 220px;
      background: #090d16;
      border: 1px solid #334155;
      color: #fde047;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.92rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      outline: none;
      transition: all 0.15s;
    }
    .inline-live-input:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
    }
    .btn-inline-reset {
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.4);
      color: #fb7185;
      padding: 5px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-inline-reset:hover {
      background: #f43f5e;
      color: #ffffff;
    }
    .badge-live-edited {
      background: linear-gradient(135deg, #0284c7, #10b981) !important;
      color: #ffffff !important;
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
    }

    .box-answer {
      background: var(--ans-bg);
      border: 1px solid var(--ans-border);
      border-radius: 8px;
      padding: 14px 18px;
      margin: 12px 0;
    }
    .box-badge {
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      padding: 2px 8px;
      border-radius: 4px;
      margin-bottom: 6px;
    }
    .badge-ans { background: #059669; color: #ffffff; }
    .badge-rule { background: #4f46e5; color: #ffffff; }
    .badge-work { background: #0284c7; color: #ffffff; }
    .badge-tip { background: #d97706; color: #ffffff; }
    .badge-dyn { background: #0284c7; color: #ffffff; }

    .ans-value {
      font-size: 1.25rem;
      font-weight: 700;
      color: #34d399;
      font-family: ui-monospace, Menlo, monospace;
    }
    .box-rule {
      background: var(--rule-bg);
      border: 1px solid var(--rule-border);
      border-radius: 8px;
      padding: 14px 18px;
      margin: 12px 0;
      font-size: 0.92rem;
      line-height: 1.55;
    }
    .box-work {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 14px 18px;
      margin: 12px 0;
      font-size: 0.9rem;
      line-height: 1.55;
    }
    .box-tip {
      background: var(--tip-bg);
      border: 1px solid var(--tip-border);
      border-radius: 8px;
      padding: 14px 18px;
      margin: 12px 0;
      font-size: 0.9rem;
      line-height: 1.5;
    }

    /* Math formatting helpers */
    .math-sym { font-family: "Times New Roman", Times, serif; font-style: italic; }
    .frac { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; padding: 0 3px; font-size: 0.9em; }
    .num { border-bottom: 1.5px solid currentColor; padding-bottom: 1px; }
    .den { padding-top: 1px; }
    .radicand { border-top: 1.5px solid currentColor; padding-top: 1px; padding-left: 2px; }

    /* Interactive Solver Suite (Tab 2) */
    .solver-grid-layout {
      max-width: 1000px;
      margin: 0 auto;
      padding-bottom: 60px;
    }
    .solver-nav-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }
    .pill-btn {
      background: var(--surface-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 8px 14px;
      border-radius: 20px;
      font-size: 0.82rem;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s;
    }
    .pill-btn:hover { border-color: var(--primary); color: var(--text); }
    .pill-btn.active {
      background: #0284c7;
      border-color: #0284c7;
      color: #ffffff;
      box-shadow: 0 2px 8px var(--primary-glow);
    }

    .solver-card {
      background: var(--surface-card);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 26px 30px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }
    .solver-card h3 {
      font-size: 1.35rem;
      color: #38bdf8;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .solver-desc {
      font-size: 0.92rem;
      color: var(--text-muted);
      margin-bottom: 22px;
      line-height: 1.5;
    }
    .input-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
      background: rgba(0,0,0,0.25);
      padding: 18px;
      border-radius: 8px;
    }
    .input-group label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
    }
    .input-group input, .input-group select {
      width: 100%;
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 9px 12px;
      color: #38bdf8;
      font-family: ui-monospace, Menlo, monospace;
      font-size: 1rem;
      font-weight: 600;
      outline: none;
    }
    .input-group input:focus, .input-group select:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-glow);
    }

    .solver-out-box {
      background: rgba(4, 47, 46, 0.4);
      border: 1px solid var(--ans-border);
      border-radius: 8px;
      padding: 18px;
      margin-top: 14px;
    }
    .out-label {
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #14b8a6;
      margin-bottom: 6px;
    }
    .out-val {
      font-size: 1.35rem;
      font-weight: 700;
      color: #34d399;
      font-family: ui-monospace, Menlo, monospace;
      margin-bottom: 14px;
    }
    .out-steps { list-style-type: none; padding: 0; }
    .out-steps li {
      padding: 6px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 0.9rem;
      color: #e2e8f0;
      line-height: 1.5;
    }
    .out-steps li:last-child { border-bottom: none; }

    /* Tableau for synthetic division */
    .tableau-wrap {
      background: #090d16;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin: 16px 0;
      font-family: ui-monospace, Menlo, monospace;
      font-size: 1.05rem;
      overflow-x: auto;
    }
    .tab-row { display: flex; gap: 16px; padding: 6px 0; }
    .tab-cell { min-width: 44px; text-align: right; }
    .tab-c-box { border-right: 2px solid #38bdf8; border-bottom: 2px solid #38bdf8; padding-right: 12px; color: #fde047; font-weight: bold; }
    .tab-line { border-top: 2px solid #475569; padding-top: 4px; }

    /* Graphing Engine Styles */
    .graph-card {
      background: #070d19;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      margin: 16px 0;
      position: relative;
    }
    .graph-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }
    .graph-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .graph-controls {
      display: flex;
      gap: 6px;
    }
    .btn-ctrl {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.15);
      color: var(--text-muted);
      border-radius: 4px;
      font-size: 0.75rem;
      padding: 3px 8px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-ctrl:hover {
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border-color: #38bdf8;
    }
    .graph-legend {
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 10px;
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .legend-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }
    .legend-line {
      width: 14px;
      height: 2px;
      display: inline-block;
    }

  </style>
</head>
<body>

  <!-- SIDEBAR -->
  <div id="sidebar">
    <div class="sidebar-header">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
        <div class="brand-title"><span>📐</span> MAT 1340 Study Hub</div>
        <button class="btn-sidebar-toggle" onclick="toggleSidebar()" title="Hide sidebar (use top bar picker instead)">◀ Hide</button>
      </div>
      <div class="brand-sub">Indexed SQLite Database • Course References • Solvers</div>
      <div class="sidebar-db-badge" id="dbStatusBadge">● 39 Assignments • 802 Questions</div>
      <input type="text" id="search" class="search-box" placeholder="🔍 Filter assignments..." oninput="filterFiles()">
    </div>
    <div class="file-list" id="fileList"></div>
    <div class="solver-shortcuts">
      <h3><span>⚡ Dedicated Solvers</span> <span>16 Tools</span></h3>
      <div class="shortcut-btns">
        <button class="btn-shortcut" onclick="launchSolver('synthetic')">➗ Synthetic Div (3.3)</button>
        <button class="btn-shortcut" onclick="launchSolver('poly-zeros')">🎯 Poly Zeros & Graph (3.4)</button>
        <button class="btn-shortcut" onclick="launchSolver('rational')">📉 Rational & Holes (3.5)</button>
        <button class="btn-shortcut" onclick="launchSolver('ineq')">⚖️ Sign Chart Ineq (3.6)</button>
        <button class="btn-shortcut" onclick="launchSolver('quadratic')">📈 Parabola & Vertex (3.1)</button>
        <button class="btn-shortcut" onclick="launchSolver('quad-eq')">🎯 Quadratic Formula (1.4)</button>
        <button class="btn-shortcut" onclick="launchSolver('explog')">🚀 Exp / Log / Inv (Ch 4)</button>
        <button class="btn-shortcut" onclick="launchSolver('conics')">🪐 Ellipse & Hyperbola (Ch 10)</button>
        <button class="btn-shortcut" onclick="launchSolver('systems')">🔗 Systems 2x2 / Nonlin (Ch 9)</button>
        <button class="btn-shortcut" onclick="launchSolver('abs')">📏 Abs Value (1.6/1.8)</button>
        <button class="btn-shortcut" onclick="launchSolver('circle')">⭕ Circle Geometry (1.1)</button>
        <button class="btn-shortcut" onclick="launchSolver('complex')">🔢 Complex No. (1.3)</button>
      </div>
    </div>
  </div>

  <!-- MAIN AREA -->
  <div id="main">

    <!-- GLOBAL UNIVERSAL OMNI-SEARCH BAR -->
    <div class="omni-container">
      <div class="omni-input-wrap">
        <span class="omni-icon">⚡</span>
        <input type="text" id="omniInput" class="omni-input" placeholder="Type ANY equation, inequality, rational function, conic, log/exp, or topic (e.g. (x-2)/(x^2-x-2), x^3-3x-2 < 0, x^2/25 + y^2/9 = 1, 2^(x-1) - 3)..." oninput="handleOmniInput()" onkeydown="handleOmniKey(event)">
        <button class="omni-clear-btn" id="omniClearBtn" onclick="clearOmniSearch()" style="display:none;">✕</button>
      </div>
      <div class="omni-pills-bar">
        <span class="omni-pills-label">Quick Demo:</span>
        <button class="omni-pill" onclick="setOmniExample('2x^2 - 8x - 12')">3.1: 2x²-8x-12</button>
        <button class="omni-pill" onclick="setOmniExample('x^3 + x^2 - 36x - 36')">3.4 Quiz 2: x³+x²-36x-36</button>
        <button class="omni-pill" onclick="setOmniExample('(x - 2)/(x^2 - x - 2)')">3.5 Hole: (x-2)/(x²-x-2)</button>
        <button class="omni-pill" onclick="setOmniExample('(x^2 - 9)/(x + 1)')">3.5 Slant: (x²-9)/(x+1)</button>
        <button class="omni-pill" onclick="setOmniExample('(x - 2)/(x + 3) > 1')">3.6 Quiz 2: (x-2)/(x+3)>1</button>
        <button class="omni-pill" onclick="setOmniExample('x^3 - 3x - 2 < 0')">3.6 Ineq: x³-3x-2&lt;0</button>
        <button class="omni-pill" onclick="setOmniExample('|1 - 2x| < 5')">1.8 Abs: |1-2x|&lt;5</button>
        <button class="omni-pill" onclick="setOmniExample('2^(x - 1) - 3')">4.2 Exp: 2^(x-1)-3</button>
        <button class="omni-pill" onclick="setOmniExample('log_2(x - 1) + 2')">4.3 Log: log₂(x-1)+2</button>
        <button class="omni-pill" onclick="setOmniExample('x^2/25 + y^2/9 = 1')">10.2 Ellipse: x²/25+y²/9=1</button>
        <button class="omni-pill" onclick="setOmniExample('x^2/9 - y^2/16 = 1')">10.3 Hyperbola: x²/9-y²/16=1</button>
        <button class="omni-pill" onclick="setOmniExample('2x + 3y = 7, x - y = 1')">9.1 System: 2x+3y=7, x-y=1</button>
      </div>
    </div>

    <!-- TABS & TOP ASSIGNMENT PICKER BAR -->
    <div class="tabs-header" style="flex-wrap:wrap;">
      <button class="btn-sidebar-toggle" id="topToggleSidebarBtn" onclick="toggleSidebar()" title="Show or hide the left assignment sidebar">
        ◀ Hide Sidebar
      </button>
      <button class="tab-btn active" id="tabDocBtn" onclick="switchMainTab('doc')">📄 Answer Sheets</button>
      <button class="tab-btn" id="tabSolverBtn" onclick="switchMainTab('solver')">⚡ Solvers Suite (16 Tools)</button>
      <button class="tab-btn" id="tabGraphBtn" onclick="switchMainTab('graph')">📈 Function & Conic Grapher</button>
      <button class="tab-btn" id="tabOmniBtn" onclick="switchMainTab('omni')" style="display:none;">🔍 Omni Results</button>

      <!-- TOP BAR ASSIGNMENT PICKER -->
      <div class="top-picker-wrap">
        <span class="top-picker-label">📂 Assignment:</span>
        <button class="btn-step-asgn" onclick="stepAssignment(-1)" title="Previous Assignment">◀</button>
        <select id="topAssignmentSelect" class="top-picker-select" onchange="loadFile(this.value)"></select>
        <button class="btn-step-asgn" onclick="stepAssignment(1)" title="Next Assignment">▶</button>
      </div>
    </div>

    <!-- TAB 1: ANSWER SHEET VIEWER -->
    <div class="tab-content" id="tabDoc">
      <div class="study-container" id="docContainer">
        <!-- Rendered answer cards will appear here -->
      </div>
    </div>

    <!-- TAB: UNIVERSAL OMNI QUERY & DATABASE RESULTS -->
    <div class="tab-content" id="tabOmni" style="display: none;">
      <div id="omniResultsView">
        <!-- Live solver execution and database references rendered here -->
      </div>
    </div>

    <!-- TAB 3: DEDICATED INTERACTIVE FUNCTION & CONIC GRAPHER -->
    <div class="tab-content" id="tabGraph" style="display: none;">
      <div style="background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:24px; margin-bottom:24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
          <div>
            <h2 style="font-size:1.35rem; font-weight:700; color:#ffffff; margin:0 0 4px 0;">📈 Interactive Function & Conic Grapher</h2>
            <p style="color:var(--text-muted); font-size:0.88rem; margin:0;">
              High-precision Cartesian coordinate plotter for parabolas, rational functions with asymptotes & holes, polynomials, exponentials, logarithms, circles, ellipses, hyperbolas, and inequalities.
            </p>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn-ctrl" onclick="zoomActiveGraph('mainGraphCanvas', 0.8)">− Zoom Out</button>
            <button class="btn-ctrl" onclick="resetActiveGraph('mainGraphCanvas')">⟲ Reset View</button>
            <button class="btn-ctrl" onclick="zoomActiveGraph('mainGraphCanvas', 1.25)">+ Zoom In</button>
          </div>
        </div>

        <div style="display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap;">
          <input type="text" id="customGraphInput" class="search-box" style="flex:1; min-width:280px; margin-top:0; font-family:monospace; font-size:1rem;" placeholder="Type f(x), rational, conic, exp/log, or inequality (e.g. (x-2)/(x^2-x-2), x^2/25+y^2/9=1, x^2/9-y^2/16=1, 2^(x-1)-3)..." value="(x - 2)/(x^2 - x - 2)" onkeydown="if(event.key==='Enter') plotCustomFunction()">
          <button class="btn-dyn-toggle" onclick="plotCustomFunction()" style="padding:10px 24px; font-weight:700; font-size:0.95rem;">📊 Plot Graph</button>
        </div>

        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:16px;">
          <span style="font-size:0.75rem; text-transform:uppercase; color:var(--text-muted); font-weight:700; align-self:center; margin-right:4px;">Course Presets:</span>
          <button class="omni-pill" onclick="setGraphPreset('2x^2 - 8x - 12')">Parabola: 2x²-8x-12</button>
          <button class="omni-pill" onclick="setGraphPreset('-(x - 3)^2 + 2')">Vertex Form: -(x-3)²+2</button>
          <button class="omni-pill" onclick="setGraphPreset('(x - 2)/(x^2 - x - 2)')">Hole & VA: (x-2)/(x²-x-2)</button>
          <button class="omni-pill" onclick="setGraphPreset('(x^2 - 9)/(x + 1)')">Slant Asymp: (x²-9)/(x+1)</button>
          <button class="omni-pill" onclick="setGraphPreset('x^3 + x^2 - 36x - 36')">Quiz 2 Cubic: x³+x²-36x-36</button>
          <button class="omni-pill" onclick="setGraphPreset('3x^4 - 7x^3 - 6x^2 + 12x + 8')">Quartic: 3x⁴-7x³-6x²+12x+8</button>
          <button class="omni-pill" onclick="setGraphPreset('2^(x - 1) - 3')">Exponential: 2^(x-1)-3</button>
          <button class="omni-pill" onclick="setGraphPreset('log_2(x - 1) + 2')">Logarithm: log₂(x-1)+2</button>
          <button class="omni-pill" onclick="setGraphPreset('x^2 + y^2 + 10x + 6y + 30 = 0')">Circle: x²+y²+10x+6y+30=0</button>
          <button class="omni-pill" onclick="setGraphPreset('x^2/25 + y^2/9 = 1')">Ellipse: x²/25+y²/9=1</button>
          <button class="omni-pill" onclick="setGraphPreset('x^2/9 - y^2/16 = 1')">Hyperbola: x²/9-y²/16=1</button>
        </div>

        <!-- GRAPH CANVAS WRAPPER -->
        <div style="position:relative; width:100%; display:flex; justify-content:center; background:#070d19; border-radius:10px; border:1px solid #1e293b; padding:16px; overflow:hidden;">
          <canvas id="mainGraphCanvas" width="800" height="460" style="width:100%; max-width:800px; height:auto; border-radius:6px; display:block; cursor:crosshair;"></canvas>
          <div id="graphTooltip" style="position:absolute; display:none; background:rgba(15,23,42,0.95); border:1px solid #38bdf8; color:#f8fafc; font-family:monospace; font-size:0.75rem; padding:4px 8px; border-radius:4px; pointer-events:none; z-index:10; box-shadow:0 4px 12px rgba(0,0,0,0.5);"></div>
        </div>

        <!-- DETAILS CARD -->
        <div id="graphDetailsCard" style="margin-top:16px; display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px;">
          <!-- Dynamically populated analysis details -->
        </div>
      </div>
    </div>

    <!-- TAB 2: INTERACTIVE SOLVER SUITE -->
    <div class="tab-content" id="tabSolver" style="display: none;">
      <div class="solver-grid-layout">
        <div class="solver-nav-pills">
          <button class="pill-btn active" id="pill-synthetic" onclick="showSolver('synthetic')">➗ Synthetic Div (3.3)</button>
          <button class="pill-btn" id="pill-poly-zeros" onclick="showSolver('poly-zeros')">🎯 Poly Zeros & Graph (3.4)</button>
          <button class="pill-btn" id="pill-rational" onclick="showSolver('rational')">📉 Rational & Holes (3.5)</button>
          <button class="pill-btn" id="pill-ineq" onclick="showSolver('ineq')">⚖️ Poly/Rat Inequalities (3.6)</button>
          <button class="pill-btn" id="pill-quadratic" onclick="showSolver('quadratic')">📈 Parabola & Vertex (3.1)</button>
          <button class="pill-btn" id="pill-quad-eq" onclick="showSolver('quad-eq')">🎯 Quadratic Formula (1.4)</button>
          <button class="pill-btn" id="pill-explog" onclick="showSolver('explog')">🚀 Exp, Log & Inverse (Ch 4)</button>
          <button class="pill-btn" id="pill-conics" onclick="showSolver('conics')">🪐 Ellipses & Hyperbolas (Ch 10)</button>
          <button class="pill-btn" id="pill-systems" onclick="showSolver('systems')">🔗 Linear & Nonlin Systems (Ch 9)</button>
          <button class="pill-btn" id="pill-abs" onclick="showSolver('abs')">📏 Absolute Value (1.6/1.8)</button>
          <button class="pill-btn" id="pill-circle" onclick="showSolver('circle')">⭕ Circle Analyzer (1.1)</button>
          <button class="pill-btn" id="pill-radical" onclick="showSolver('radical')">🌿 Radicals & Sq Root</button>
          <button class="pill-btn" id="pill-complex" onclick="showSolver('complex')">🔢 Complex Numbers (1.3)</button>
          <button class="pill-btn" id="pill-projectile" onclick="showSolver('projectile')">🚀 Projectile Motion (3.1)</button>
          <button class="pill-btn" id="pill-dist-mid" onclick="showSolver('dist-mid')">🧮 Distance & Midpoint (1.1)</button>
          <button class="pill-btn" id="pill-poly-eval" onclick="showSolver('poly-eval')">⚡ Polynomial Evaluator</button>
        </div>

        <!-- 1. Synthetic Division -->
        <div class="solver-card" id="solver-synthetic">
          <h3>➗ Synthetic Division & Remainder / Factor Theorem (Ch 3.3)</h3>
          <p class="solver-desc">Enter polynomial coefficients in descending order (space-separated, e.g. "2 -11 13 -7 12") and divisor root c to see the tableau, quotient, remainder, factor verdict, and polynomial graph.</p>
          <div class="input-grid">
            <div class="input-group" style="grid-column: span 2;">
              <label>Polynomial Coefficients (descending order):</label>
              <input type="text" id="syn-coeffs" value="2 -11 13 -7 12" oninput="runSynthetic()">
            </div>
            <div class="input-group">
              <label>Divisor Root c:</label>
              <input type="number" id="syn-c" value="4" step="any" oninput="runSynthetic()">
            </div>
          </div>
          <div id="syn-out"></div>
        </div>

        <!-- 2. Polynomial Zeros, Multiplicities & Graph (Ch 3.3-3.4) -->
        <div class="solver-card" id="solver-poly-zeros" style="display: none;">
          <h3>🎯 Polynomial Zeros, Multiplicities, Rational Zero Theorem & Graph (Ch 3.3–3.4)</h3>
          <p class="solver-desc">Enter any polynomial expression (e.g. "x^3 + x^2 - 36x - 36" or "3x^4 - 7x^3 - 6x^2 + 12x + 8" or "-2(x-1)^2(x+2)") or space-separated coefficients. Finds all Rational Zero Theorem p/q candidates, exact zeros, multiplicities (crosses vs touches/turns), end behavior, and plots the curve.</p>
          <div class="input-grid">
            <div class="input-group" style="grid-column: span 3;">
              <label>Polynomial f(x) (Expression or Space-Separated Coefficients):</label>
              <input type="text" id="pzero-input" value="x^3 + x^2 - 36x - 36" oninput="runPolyZeros()">
            </div>
          </div>
          <div id="pzero-out"></div>
        </div>

        <!-- 3. Rational Function Analyzer & Grapher (Ch 3.5) -->
        <div class="solver-card" id="solver-rational" style="display: none;">
          <h3>📉 Rational Function Analyzer: Holes, Vertical/Horizontal/Slant Asymptotes & Graph (Ch 3.5)</h3>
          <p class="solver-desc">Enter the Numerator P(x) and Denominator Q(x) of f(x) = P(x)/Q(x). Automatically detects removable holes, vertical asymptotes, horizontal or oblique (slant) asymptotes, domain, x/y-intercepts, and plots all branches.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>Numerator P(x):</label>
              <input type="text" id="rat-num" value="x - 2" oninput="runRationalSolver()">
            </div>
            <div class="input-group">
              <label>Denominator Q(x):</label>
              <input type="text" id="rat-den" value="x^2 - x - 2" oninput="runRationalSolver()">
            </div>
          </div>
          <div id="rat-out"></div>
        </div>

        <!-- 4. Polynomial & Rational Inequalities + Sign Chart (Ch 3.6) -->
        <div class="solver-card" id="solver-ineq" style="display: none;">
          <h3>⚖️ Polynomial & Rational Inequality Sign Chart Solver (Ch 3.6)</h3>
          <p class="solver-desc">Enter any polynomial or rational inequality (e.g. "x^3 - 3x - 2 < 0", "(x - 2)/(x + 3) > 1", "(3x - 1)/(3x + 3) < 6", "x^2 - 6x > 27"). Moves all terms to LHS, finds boundary zeros and undefined points, builds the full interval Sign Chart, and plots the solution.</p>
          <div class="input-grid">
            <div class="input-group" style="grid-column: span 3;">
              <label>Inequality Expression:</label>
              <input type="text" id="ineq-input" value="(x - 2)/(x + 3) > 1" oninput="runIneqSolver()">
            </div>
          </div>
          <div id="ineq-out"></div>
        </div>

        <!-- 5. Exponential, Logarithmic & Inverse Solver (Ch 4.1-4.6) -->
        <div class="solver-card" id="solver-explog" style="display: none;">
          <h3>🚀 Exponential, Logarithmic & Inverse Function / Equation Solver (Ch 4.1–4.6)</h3>
          <p class="solver-desc">Analyze and graph exponential functions f(x) = a·b^(x - h) + k, logarithmic functions f(x) = a·log_b(x - h) + k, solve exponential/log equations, or compute compound interest & continuous growth.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>Mode:</label>
              <select id="explog-mode" onchange="runExpLogSolver()">
                <option value="exp">Exponential Function & Equation: a·b^(x - h) + k = y</option>
                <option value="log">Logarithmic Function & Equation: a·log_b(x - h) + k = y</option>
                <option value="finance">Compound / Continuous Growth & Half-Life (4.6)</option>
              </select>
            </div>
            <div class="input-group">
              <label>a (Multiplier / Principal P):</label>
              <input type="number" id="explog-a" value="1" step="any" oninput="runExpLogSolver()">
            </div>
            <div class="input-group">
              <label>Base b (or Rate r decimal):</label>
              <input type="number" id="explog-b" value="2" step="any" oninput="runExpLogSolver()">
            </div>
            <div class="input-group">
              <label>h (Horizontal Shift x - h / n comp/yr):</label>
              <input type="number" id="explog-h" value="1" step="any" oninput="runExpLogSolver()">
            </div>
            <div class="input-group">
              <label>k (Vertical Shift + k / Time t):</label>
              <input type="number" id="explog-k" value="-3" step="any" oninput="runExpLogSolver()">
            </div>
            <div class="input-group">
              <label>Target RHS y (for solving f(x) = y):</label>
              <input type="number" id="explog-rhs" value="5" step="any" oninput="runExpLogSolver()">
            </div>
          </div>
          <div id="explog-out"></div>
        </div>

        <!-- 6. Conic Sections: Ellipses & Hyperbolas (Ch 10.2-10.3) -->
        <div class="solver-card" id="solver-conics" style="display: none;">
          <h3>🪐 Conic Sections: Ellipses & Hyperbolas Analyzer & Plotter (Ch 10.2–10.3)</h3>
          <p class="solver-desc">Computes center (h, k), vertices, co-vertices, foci c, fundamental box, asymptote equations, domain, range, and renders the full conic graph.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>Conic Type:</label>
              <select id="conic-type" onchange="runConicsSolver()">
                <option value="ellipse">Ellipse: (x-h)²/a² + (y-k)²/b² = 1</option>
                <option value="hyp-h">Hyperbola (Horizontal): (x-h)²/a² - (y-k)²/b² = 1</option>
                <option value="hyp-v">Hyperbola (Vertical): (y-k)²/a² - (x-h)²/b² = 1</option>
              </select>
            </div>
            <div class="input-group">
              <label>Center h (x-coord):</label>
              <input type="number" id="conic-h" value="0" step="any" oninput="runConicsSolver()">
            </div>
            <div class="input-group">
              <label>Center k (y-coord):</label>
              <input type="number" id="conic-k" value="0" step="any" oninput="runConicsSolver()">
            </div>
            <div class="input-group">
              <label>a (semi-axis under first term, a &gt; 0):</label>
              <input type="number" id="conic-a" value="5" min="0.1" step="any" oninput="runConicsSolver()">
            </div>
            <div class="input-group">
              <label>b (semi-axis under second term, b &gt; 0):</label>
              <input type="number" id="conic-b" value="3" min="0.1" step="any" oninput="runConicsSolver()">
            </div>
          </div>
          <div id="conic-out"></div>
        </div>

        <!-- 7. Systems of Equations: Linear & Nonlinear (Ch 9.1 & 9.5) -->
        <div class="solver-card" id="solver-systems" style="display: none;">
          <h3>🔗 Systems of Equations: 2×2 Linear & Nonlinear Parabola/Circle-Line (Ch 9.1 & 9.5)</h3>
          <p class="solver-desc">Enter two equations separated by a comma (e.g. "2x + 3y = 7, x - y = 1" or "y = x^2 - 4, y = 2x - 1" or "x^2 + y^2 = 25, y = x + 1"). Solves for all real intersection points (x, y) and graphs both curves.</p>
          <div class="input-grid">
            <div class="input-group" style="grid-column: span 3;">
              <label>System of Two Equations (comma-separated):</label>
              <input type="text" id="sys-input" value="2x + 3y = 7, x - y = 1" oninput="runSystemsSolver()">
            </div>
          </div>
          <div id="sys-out"></div>
        </div>

        <!-- 8. Quadratic Functions & Parabola Analyzer -->
        <div class="solver-card" id="solver-quadratic" style="display: none;">
          <h3>📈 Quadratic Functions & Parabola Explorer (Ch 3.1)</h3>
          <p class="solver-desc">Supports both Standard Form f(x) = ax² + bx + c and Vertex Form a(x - h)² + k. Calculates vertex, axis, min/max, vertex form, intercepts, domain, range, and live parabola graph.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>a (leading coefficient):</label>
              <input type="number" id="quad-a" value="2" step="any" oninput="runQuad()">
            </div>
            <div class="input-group">
              <label>b (x coefficient):</label>
              <input type="number" id="quad-b" value="-8" step="any" oninput="runQuad()">
            </div>
            <div class="input-group">
              <label>c (constant term):</label>
              <input type="number" id="quad-c" value="-12" step="any" oninput="runQuad()">
            </div>
          </div>
          <div id="quad-out"></div>
        </div>

        <!-- 9. Quadratic Equation Formula & Exact Roots -->
        <div class="solver-card" id="solver-quad-eq" style="display: none;">
          <h3>🎯 Quadratic Equation Solver: ax² + bx + c = 0 (Ch 1.4)</h3>
          <p class="solver-desc">Solves any quadratic equation using the quadratic formula with discriminant analysis, exact simplified radical form, complex conjugate roots, and parabola root plot.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>a:</label>
              <input type="number" id="qeq-a" value="1" step="any" oninput="runQuadEq()">
            </div>
            <div class="input-group">
              <label>b:</label>
              <input type="number" id="qeq-b" value="2" step="any" oninput="runQuadEq()">
            </div>
            <div class="input-group">
              <label>c:</label>
              <input type="number" id="qeq-c" value="5" step="any" oninput="runQuadEq()">
            </div>
          </div>
          <div id="qeq-out"></div>
        </div>

        <!-- 10. Absolute Value Inequality & Equation -->
        <div class="solver-card" id="solver-abs" style="display: none;">
          <h3>📏 Absolute Value: |ax + b| [op] c (Ch 1.6 & 1.8)</h3>
          <p class="solver-desc">Solves absolute value inequalities and equations, properly handling positive, zero, and negative right-hand bounds with conjunctions, disjunctions, and number-line plot.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>a (x coefficient):</label>
              <input type="number" id="abs-a" value="2" step="any" oninput="runAbs()">
            </div>
            <div class="input-group">
              <label>b (inside constant):</label>
              <input type="number" id="abs-b" value="-3" step="any" oninput="runAbs()">
            </div>
            <div class="input-group">
              <label>Operator:</label>
              <select id="abs-op" onchange="runAbs()">
                <option value="<">&lt; (Less than - Conjunction)</option>
                <option value="<=" selected>&le; (Less than or equal)</option>
                <option value=">">&gt; (Greater than - Disjunction)</option>
                <option value=">=">&ge; (Greater than or equal)</option>
                <option value="=">= (Equation)</option>
              </select>
            </div>
            <div class="input-group">
              <label>c (bound):</label>
              <input type="number" id="abs-c" value="5" step="any" oninput="runAbs()">
            </div>
          </div>
          <div id="abs-out"></div>
        </div>

        <!-- 11. Circle Analyzer -->
        <div class="solver-card" id="solver-circle" style="display: none;">
          <h3>⭕ Circle Analyzer: General Form, Standard Form & Endpoints (Ch 1.1)</h3>
          <p class="solver-desc">Completes the square from General Form Ax² + Ay² + Bx + Cy + D = 0 into Standard Form (x - h)² + (y - k)² = r², finding Center, Radius, Domain, Range, Cardinal Points, and Circle Graph.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>A (x² & y² coeff):</label>
              <input type="number" id="circ-a" value="1" step="any" oninput="runCirc()">
            </div>
            <div class="input-group">
              <label>B (x coeff):</label>
              <input type="number" id="circ-b" value="10" step="any" oninput="runCirc()">
            </div>
            <div class="input-group">
              <label>C (y coeff):</label>
              <input type="number" id="circ-c" value="6" step="any" oninput="runCirc()">
            </div>
            <div class="input-group">
              <label>D (constant):</label>
              <input type="number" id="circ-d" value="30" step="any" oninput="runCirc()">
            </div>
          </div>
          <div id="circ-out"></div>
        </div>

        <!-- 12. Radical Simplifier & Square Root Property -->
        <div class="solver-card" id="solver-radical" style="display: none;">
          <h3>🌿 Radical Simplifier & Square Root Property</h3>
          <p class="solver-desc">Simplifies radicals √N or √(-N) into greatest square factor and real or imaginary unit i. Also solves x² = N.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>Integer inside radical:</label>
              <input type="number" id="rad-n" value="1875" step="1" oninput="runRad()">
            </div>
          </div>
          <div id="rad-out"></div>
        </div>

        <!-- 13. Complex Numbers Multi-Tool -->
        <div class="solver-card" id="solver-complex" style="display: none;">
          <h3>🔢 Complex Numbers: Multiplication, Division, Classification & Powers of i (Ch 1.3)</h3>
          <p class="solver-desc">Performs FOIL multiplication, conjugate division, and classifies numbers in standard form a + bi.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>a₁ (Real 1):</label>
              <input type="number" id="cplx-a1" value="3" step="any" oninput="runComplex()">
            </div>
            <div class="input-group">
              <label>b₁ (Imag 1):</label>
              <input type="number" id="cplx-b1" value="6" step="any" oninput="runComplex()">
            </div>
            <div class="input-group">
              <label>a₂ (Real 2):</label>
              <input type="number" id="cplx-a2" value="6" step="any" oninput="runComplex()">
            </div>
            <div class="input-group">
              <label>b₂ (Imag 2):</label>
              <input type="number" id="cplx-b2" value="2" step="any" oninput="runComplex()">
            </div>
            <div class="input-group">
              <label>Power of i (exponent n for iⁿ):</label>
              <input type="number" id="cplx-pow" value="45" step="1" oninput="runComplex()">
            </div>
          </div>
          <div id="cplx-out"></div>
        </div>

        <!-- 14. Projectile Motion & Optimization -->
        <div class="solver-card" id="solver-projectile" style="display: none;">
          <h3>🚀 Projectile Motion & Optimization: h(t) = -16t² + v₀t + h₀ (Ch 3.1)</h3>
          <p class="solver-desc">Analyzes vertical motion under gravity to calculate maximum height, time to reach vertex, total flight time before landing, and trajectory graph.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>Initial Velocity v₀ (ft/s):</label>
              <input type="number" id="proj-v0" value="96" step="any" oninput="runProjectile()">
            </div>
            <div class="input-group">
              <label>Initial Height h₀ (ft):</label>
              <input type="number" id="proj-h0" value="112" step="any" oninput="runProjectile()">
            </div>
          </div>
          <div id="proj-out"></div>
        </div>

        <!-- 15. Distance & Midpoint Formula -->
        <div class="solver-card" id="solver-dist-mid" style="display: none;">
          <h3>🧮 Distance & Midpoint Formula Between (x₁, y₁) and (x₂, y₂) (Ch 1.1)</h3>
          <p class="solver-desc">Calculates exact distance (simplified radical and decimal) and coordinates of the midpoint between two Cartesian points.</p>
          <div class="input-grid">
            <div class="input-group">
              <label>x₁:</label>
              <input type="number" id="dm-x1" value="-3" step="any" oninput="runDistMid()">
            </div>
            <div class="input-group">
              <label>y₁:</label>
              <input type="number" id="dm-y1" value="4" step="any" oninput="runDistMid()">
            </div>
            <div class="input-group">
              <label>x₂:</label>
              <input type="number" id="dm-x2" value="5" step="any" oninput="runDistMid()">
            </div>
            <div class="input-group">
              <label>y₂:</label>
              <input type="number" id="dm-y2" value="-2" step="any" oninput="runDistMid()">
            </div>
          </div>
          <div id="dm-out"></div>
        </div>

        <!-- 16. Universal Polynomial Evaluator -->
        <div class="solver-card" id="solver-poly-eval" style="display: none;">
          <h3>⚡ Universal Polynomial Evaluator & Factor Test</h3>
          <p class="solver-desc">Evaluate any polynomial P(x) at x = x₀ using Horner's method / Synthetic division.</p>
          <div class="input-grid">
            <div class="input-group" style="grid-column: span 2;">
              <label>Polynomial Coefficients:</label>
              <input type="text" id="peval-coeffs" value="4 1 1 -5" oninput="runPolyEval()">
            </div>
            <div class="input-group">
              <label>Evaluate at x =</label>
              <input type="number" id="peval-x" value="-1" step="any" oninput="runPolyEval()">
            </div>
          </div>
          <div id="peval-out"></div>
        </div>

      </div>
    </div>
  </div>

  <!-- EMBEDDED ANSWER SHEETS DATA -->
  <script id="embedded-data" type="application/json">
    ###EMBEDDED_JSON###
  </script>

  <!-- EMBEDDED STRUCTURED DATABASE CATALOG -->
  <script id="database-data" type="application/json">
    ###EMBEDDED_DB_JSON###
  </script>

  <script>

    // ==========================================================================
    // HIGH-PRECISION RETINA HTML5 CANVAS GRAPHING ENGINE
    // ==========================================================================

    const activeGraphStates = {};

    function getGraphState(canvasId) {
      if (!activeGraphStates[canvasId]) {
        activeGraphStates[canvasId] = {
          xMin: -10,
          xMax: 10,
          yMin: -10,
          yMax: 10,
          zoom: 1.0,
          fn: null,
          data: null
        };
      }
      return activeGraphStates[canvasId];
    }

    function zoomActiveGraph(canvasId, factor) {
      const state = getGraphState(canvasId);
      const xCenter = (state.xMin + state.xMax) / 2;
      const yCenter = (state.yMin + state.yMax) / 2;
      const xSpan = (state.xMax - state.xMin) / factor;
      const ySpan = (state.yMax - state.yMin) / factor;
      state.xMin = xCenter - xSpan / 2;
      state.xMax = xCenter + xSpan / 2;
      state.yMin = yCenter - ySpan / 2;
      state.yMax = yCenter + ySpan / 2;
      drawCurrentGraph(canvasId);
    }

    function resetActiveGraph(canvasId) {
      const state = getGraphState(canvasId);
      if (state.defaultBounds) {
        state.xMin = state.defaultBounds.xMin;
        state.xMax = state.defaultBounds.xMax;
        state.yMin = state.defaultBounds.yMin;
        state.yMax = state.defaultBounds.yMax;
      } else {
        state.xMin = -10; state.xMax = 10; state.yMin = -10; state.yMax = 10;
      }
      drawCurrentGraph(canvasId);
    }

    function setupCanvasHiDPI(canvas) {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      const w = rect.width || canvas.width || 760;
      const h = rect.height || canvas.height || 420;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      const ctx = canvas.getContext('2d');
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { ctx, width: w, height: h };
    }

    function drawCurrentGraph(canvasId) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const state = getGraphState(canvasId);
      if (!state.data) return;
      renderUniversalGraph(canvasId, state.data);
    }

    function renderUniversalGraph(canvasId, data) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const { ctx, width, height } = setupCanvasHiDPI(canvas);
      const state = getGraphState(canvasId);
      state.data = data;

      // Auto-set initial bounds if not already set or if different dataset
      if (!state.boundsInitialized || state.datasetId !== data.id) {
        state.datasetId = data.id;
        state.boundsInitialized = true;
        let bounds = calculateOptimalBounds(data);
        state.xMin = bounds.xMin;
        state.xMax = bounds.xMax;
        state.yMin = bounds.yMin;
        state.yMax = bounds.yMax;
        state.defaultBounds = { ...bounds };
      }

      const { xMin, xMax, yMin, yMax } = state;

      // 1. Clear background
      ctx.fillStyle = '#070d19';
      ctx.fillRect(0, 0, width, height);

      // Coordinate converter helpers
      const toScreenX = (x) => ((x - xMin) / (xMax - xMin)) * width;
      const toScreenY = (y) => height - ((y - yMin) / (yMax - yMin)) * height;

      // 2. Draw Grid
      drawCartesianGrid(ctx, width, height, xMin, xMax, yMin, yMax, toScreenX, toScreenY);

      // 3. Draw Number Line for 1D inequalities
      if (data.type === 'number_line') {
        drawNumberLinePlot(ctx, width, height, data, xMin, xMax, toScreenX);
        return;
      }

      // 4. Draw Conics (Circle, Ellipse, Hyperbola)
      if (data.type === 'circle' || data.circle) {
        drawCirclePlot(ctx, data, toScreenX, toScreenY);
      }
      if (data.type === 'ellipse' || data.ellipse) {
        drawEllipsePlot(ctx, data, toScreenX, toScreenY);
      }
      if (data.type === 'hyperbola' || data.hyperbola) {
        drawHyperbolaPlot(ctx, data, toScreenX, toScreenY, xMin, xMax, yMin, yMax);
      }
      if (data.mirrorLine) {
        ctx.save();
        ctx.setLineDash([5, 5]);
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(toScreenX(xMin), toScreenY(xMin));
        ctx.lineTo(toScreenX(xMax), toScreenY(xMax));
        ctx.stroke();
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 11px monospace';
        ctx.fillText('y = x', toScreenX(xMax * 0.7), toScreenY(xMax * 0.7) - 6);
        ctx.restore();
      }

      // 5. Draw Asymptotes (Vertical, Horizontal, Slant)
      if (data.vertAsymptotes) {
        ctx.save();
        ctx.setLineDash([6, 6]);
        ctx.strokeStyle = '#f43f5e'; // Bright Red
        ctx.lineWidth = 1.8;
        data.vertAsymptotes.forEach(va => {
          const sx = toScreenX(va.val);
          ctx.beginPath();
          ctx.moveTo(sx, 0);
          ctx.lineTo(sx, height);
          ctx.stroke();

          // Label
          ctx.fillStyle = '#f43f5e';
          ctx.font = 'bold 11px monospace';
          ctx.fillText(`x = ${va.label}`, sx + 4, 18);
        });
        ctx.restore();
      }

      if (data.horizAsymptote) {
        ctx.save();
        ctx.setLineDash([6, 6]);
        ctx.strokeStyle = '#38bdf8'; // Cyan
        ctx.lineWidth = 1.8;
        const sy = toScreenY(data.horizAsymptote.val);
        ctx.beginPath();
        ctx.moveTo(0, sy);
        ctx.lineTo(width, sy);
        ctx.stroke();

        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 11px monospace';
        ctx.fillText(data.horizAsymptote.eq, width - 65, sy - 6);
        ctx.restore();
      }

      if (data.slantAsymptote) {
        ctx.save();
        ctx.setLineDash([6, 6]);
        ctx.strokeStyle = '#fbbf24'; // Yellow
        ctx.lineWidth = 1.8;
        const m = data.slantAsymptote.m;
        const b = data.slantAsymptote.b;
        const yLeft = m * xMin + b;
        const yRight = m * xMax + b;
        ctx.beginPath();
        ctx.moveTo(toScreenX(xMin), toScreenY(yLeft));
        ctx.lineTo(toScreenX(xMax), toScreenY(yRight));
        ctx.stroke();

        ctx.fillStyle = '#fbbf24';
        ctx.font = 'bold 11px monospace';
        ctx.fillText(data.slantAsymptote.eq, width - 90, toScreenY(yRight) - 8);
        ctx.restore();
      }

      // 6. Draw Axis of Symmetry for Parabolas
      if (data.axisOfSymmetry !== undefined) {
        ctx.save();
        ctx.setLineDash([4, 4]);
        ctx.strokeStyle = '#a855f7'; // Purple
        ctx.lineWidth = 1.5;
        const sx = toScreenX(data.axisOfSymmetry);
        ctx.beginPath();
        ctx.moveTo(sx, 0);
        ctx.lineTo(sx, height);
        ctx.stroke();
        ctx.fillStyle = '#a855f7';
        ctx.font = 'bold 11px monospace';
        ctx.fillText(`Axis x = ${data.axisOfSymmetry}`, sx + 4, height - 12);
        ctx.restore();
      }

      // 7. Draw Continuous Function Curve
      if (data.fn) {
        ctx.save();
        ctx.strokeStyle = data.curveColor || '#38bdf8';
        ctx.lineWidth = 2.5;
        ctx.beginPath();

        const steps = width * 2;
        let lastY = null;
        let isDrawing = false;
        const vertVals = (data.vertAsymptotes || []).map(v => v.val);

        for (let i = 0; i <= steps; i++) {
          const x = xMin + (i / steps) * (xMax - xMin);
          // Check proximity to vertical asymptotes
          let nearAsymptote = false;
          for (const va of vertVals) {
            if (Math.abs(x - va) < (xMax - xMin) / 180) {
              nearAsymptote = true;
              break;
            }
          }

          if (nearAsymptote) {
            isDrawing = false;
            lastY = null;
            continue;
          }

          let y = data.fn(x);
          if (isNaN(y) || !isFinite(y)) {
            isDrawing = false;
            lastY = null;
            continue;
          }

          // Discontinuity check across poles
          if (lastY !== null && Math.abs(y - lastY) > (yMax - yMin) * 1.5) {
            isDrawing = false;
          }

          const sx = toScreenX(x);
          const sy = toScreenY(y);

          if (!isDrawing) {
            ctx.moveTo(sx, sy);
            isDrawing = true;
          } else {
            ctx.lineTo(sx, sy);
          }
          lastY = y;
        }
        ctx.stroke();
        ctx.restore();
      }

      // 7b. Draw Secondary Curve (for Systems or Inverse Functions)
      if (data.fn2) {
        ctx.save();
        ctx.strokeStyle = data.curve2Color || '#10b981';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        const steps2 = width * 2;
        let lastY2 = null;
        let isDrawing2 = false;
        for (let i = 0; i <= steps2; i++) {
          const x = xMin + (i / steps2) * (xMax - xMin);
          let y = data.fn2(x);
          if (isNaN(y) || !isFinite(y)) {
            isDrawing2 = false;
            lastY2 = null;
            continue;
          }
          if (lastY2 !== null && Math.abs(y - lastY2) > (yMax - yMin) * 1.5) {
            isDrawing2 = false;
          }
          const sx = toScreenX(x);
          const sy = toScreenY(y);
          if (!isDrawing2) {
            ctx.moveTo(sx, sy);
            isDrawing2 = true;
          } else {
            ctx.lineTo(sx, sy);
          }
          lastY2 = y;
        }
        ctx.stroke();
        ctx.restore();
      }

      // 8. Draw Critical Points (Vertex, Zeros, Intercepts)
      if (data.points) {
        data.points.forEach(pt => {
          const sx = toScreenX(pt.x);
          const sy = toScreenY(pt.y);
          if (sx < 0 || sx > width || sy < 0 || sy > height) return;

          ctx.save();
          if (pt.type === 'hole') {
            // Removable hole: open circle
            ctx.fillStyle = '#ffffff';
            ctx.strokeStyle = '#f43f5e';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.arc(sx, sy, 5.5, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
          } else {
            // Filled point
            ctx.fillStyle = pt.color || '#38bdf8';
            ctx.shadowColor = pt.color || '#38bdf8';
            ctx.shadowBlur = 8;
            ctx.beginPath();
            if (pt.type === 'vertex') {
              // Diamond for vertex
              ctx.moveTo(sx, sy - 6);
              ctx.lineTo(sx + 6, sy);
              ctx.lineTo(sx, sy + 6);
              ctx.lineTo(sx - 6, sy);
              ctx.closePath();
            } else {
              ctx.arc(sx, sy, 4.5, 0, Math.PI * 2);
            }
            ctx.fill();
          }
          ctx.restore();

          // Label
          if (pt.label) {
            ctx.fillStyle = '#f8fafc';
            ctx.font = '600 11px system-ui, sans-serif';
            ctx.shadowColor = '#000000';
            ctx.shadowBlur = 4;
            const xOffset = (pt.x > (xMin + xMax) / 2) ? -ctx.measureText(pt.label).width - 8 : 8;
            const yOffset = (pt.y > (yMin + yMax) / 2) ? 14 : -8;
            ctx.fillText(pt.label, sx + xOffset, sy + yOffset);
          }
        });
      }

      // Attach tooltip listener if not already bound
      attachCanvasTooltip(canvas, toScreenX, toScreenY, xMin, xMax, yMin, yMax, data);
    }

    function calculateOptimalBounds(data) {
      let xVals = [-6, 6];
      let yVals = [-6, 6];

      if (data.type === 'number_line' && data.intervals) {
        xVals = [-5, 5];
        data.intervals.forEach(iv => {
          if (isFinite(iv.from)) xVals.push(iv.from - 3, iv.from + 3);
          if (isFinite(iv.to)) xVals.push(iv.to - 3, iv.to + 3);
        });
      }

      if (data.points && data.points.length > 0) {
        data.points.forEach(p => {
          if (!isNaN(p.x) && isFinite(p.x) && Math.abs(p.x) < 200) xVals.push(p.x);
          if (!isNaN(p.y) && isFinite(p.y) && Math.abs(p.y) < 200) yVals.push(p.y);
        });
      }
      if (data.vertAsymptotes) {
        data.vertAsymptotes.forEach(v => xVals.push(v.val - 3, v.val + 3));
      }
      if (data.horizAsymptote) {
        yVals.push(data.horizAsymptote.val - 3, data.horizAsymptote.val + 3);
      }
      if (data.circle) {
        const { h, k, r } = data.circle;
        xVals.push(h - r - 2, h + r + 2);
        yVals.push(k - r - 2, k + r + 2);
      }
      if (data.ellipse) {
        const { h, k, rx, ry } = data.ellipse;
        xVals.push(h - rx - 2, h + rx + 2);
        yVals.push(k - ry - 2, k + ry + 2);
      }
      if (data.hyperbola) {
        const { h, k, a, b } = data.hyperbola;
        const spanX = Math.max(a, b) * 2.5;
        const spanY = Math.max(a, b) * 2.5;
        xVals.push(h - spanX, h + spanX);
        yVals.push(k - spanY, k + spanY);
      }

      let minX = Math.min(...xVals);
      let maxX = Math.max(...xVals);
      let minY = Math.min(...yVals);
      let maxY = Math.max(...yVals);

      const xPad = Math.max(2, (maxX - minX) * 0.25);
      const yPad = Math.max(2, (maxY - minY) * 0.25);

      return {
        xMin: Math.floor(minX - xPad),
        xMax: Math.ceil(maxX + xPad),
        yMin: Math.floor(minY - yPad),
        yMax: Math.ceil(maxY + yPad)
      };
    }

    function drawCartesianGrid(ctx, width, height, xMin, xMax, yMin, yMax, toScreenX, toScreenY) {
      // Step calculation
      const xRange = xMax - xMin;
      const yRange = yMax - yMin;
      const getStep = (r) => {
        if (r <= 12) return 1;
        if (r <= 25) return 2;
        if (r <= 60) return 5;
        if (r <= 120) return 10;
        return 20;
      };
      const xStep = getStep(xRange);
      const yStep = getStep(yRange);

      ctx.save();
      // Grid lines
      ctx.strokeStyle = '#152033';
      ctx.lineWidth = 1;

      const firstX = Math.ceil(xMin / xStep) * xStep;
      for (let x = firstX; x <= xMax; x += xStep) {
        const sx = toScreenX(x);
        ctx.beginPath();
        ctx.moveTo(sx, 0);
        ctx.lineTo(sx, height);
        ctx.stroke();
      }

      const firstY = Math.ceil(yMin / yStep) * yStep;
      for (let y = firstY; y <= yMax; y += yStep) {
        const sy = toScreenY(y);
        ctx.beginPath();
        ctx.moveTo(0, sy);
        ctx.lineTo(width, sy);
        ctx.stroke();
      }

      // X and Y Axes
      const originX = toScreenX(0);
      const originY = toScreenY(0);

      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 1.8;

      // X-Axis
      if (originY >= 0 && originY <= height) {
        ctx.beginPath();
        ctx.moveTo(0, originY);
        ctx.lineTo(width, originY);
        ctx.stroke();
      }

      // Y-Axis
      if (originX >= 0 && originX <= width) {
        ctx.beginPath();
        ctx.moveTo(originX, 0);
        ctx.lineTo(originX, height);
        ctx.stroke();
      }

      // Axis Ticks & Numbers
      ctx.fillStyle = '#64748b';
      ctx.font = '10px ui-monospace, Menlo, monospace';

      for (let x = firstX; x <= xMax; x += xStep) {
        if (x === 0) continue;
        const sx = toScreenX(x);
        const yPos = (originY >= 10 && originY <= height - 15) ? originY + 12 : (height - 6);
        ctx.fillText(x.toString(), sx - 6, yPos);
      }

      for (let y = firstY; y <= yMax; y += yStep) {
        if (y === 0) continue;
        const sy = toScreenY(y);
        const xPos = (originX >= 25 && originX <= width - 25) ? originX - 22 : 6;
        ctx.fillText(y.toString(), xPos, sy + 3);
      }

      ctx.restore();
    }

    function drawCirclePlot(ctx, data, toScreenX, toScreenY) {
      const { h, k, r } = data.circle;
      const centerSx = toScreenX(h);
      const centerSy = toScreenY(k);
      const radiusPx = Math.abs(toScreenX(h + r) - toScreenX(h));

      ctx.save();
      // Draw circular boundary
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.arc(centerSx, centerSy, radiusPx, 0, Math.PI * 2);
      ctx.stroke();

      // Radius line
      ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)';
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(centerSx, centerSy);
      ctx.lineTo(centerSx + radiusPx, centerSy);
      ctx.stroke();

      // Radius label
      ctx.fillStyle = '#10b981';
      ctx.font = 'bold 11px monospace';
      ctx.fillText(`r = ${r}`, centerSx + radiusPx / 2 - 8, centerSy - 6);

      // Center point
      ctx.fillStyle = '#34d399';
      ctx.beginPath();
      ctx.arc(centerSx, centerSy, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillText(`C(${h}, ${k})`, centerSx + 8, centerSy + 12);
      ctx.restore();
    }

    function drawEllipsePlot(ctx, data, toScreenX, toScreenY) {
      const { h, k, rx, ry } = data.ellipse;
      ctx.save();

      // Major & Minor axes dashed
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.35)';
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(toScreenX(h - rx), toScreenY(k));
      ctx.lineTo(toScreenX(h + rx), toScreenY(k));
      ctx.moveTo(toScreenX(h), toScreenY(k - ry));
      ctx.lineTo(toScreenX(h), toScreenY(k + ry));
      ctx.stroke();
      ctx.setLineDash([]);

      // Ellipse curve
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2.6;
      ctx.beginPath();
      const steps = 200;
      for (let i = 0; i <= steps; i++) {
        const theta = (i / steps) * Math.PI * 2;
        const x = h + rx * Math.cos(theta);
        const y = k + ry * Math.sin(theta);
        const sx = toScreenX(x);
        const sy = toScreenY(y);
        if (i === 0) ctx.moveTo(sx, sy);
        else ctx.lineTo(sx, sy);
      }
      ctx.closePath();
      ctx.stroke();
      ctx.restore();
    }

    function drawHyperbolaPlot(ctx, data, toScreenX, toScreenY, xMin, xMax, yMin, yMax) {
      const { h, k, a, b, transverse } = data.hyperbola;
      const isHoriz = (transverse !== 'vertical');
      const dx = isHoriz ? a : b;
      const dy = isHoriz ? b : a;

      ctx.save();

      // 1. Central fundamental box (2*dx by 2*dy)
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.45)';
      ctx.lineWidth = 1.4;
      const boxLeft = toScreenX(h - dx);
      const boxRight = toScreenX(h + dx);
      const boxTop = toScreenY(k + dy);
      const boxBot = toScreenY(k - dy);
      ctx.strokeRect(boxLeft, boxTop, boxRight - boxLeft, boxBot - boxTop);

      // 2. Asymptotes y - k = +- (dy/dx)(x - h)
      const slope = dy / dx;
      ctx.setLineDash([6, 6]);
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      ctx.moveTo(toScreenX(xMin), toScreenY(k + slope * (xMin - h)));
      ctx.lineTo(toScreenX(xMax), toScreenY(k + slope * (xMax - h)));
      ctx.moveTo(toScreenX(xMin), toScreenY(k - slope * (xMin - h)));
      ctx.lineTo(toScreenX(xMax), toScreenY(k - slope * (xMax - h)));
      ctx.stroke();
      ctx.setLineDash([]);

      // 3. Two Hyperbolic Branches parameterized by t in [-2.8, 2.8]
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 2.6;
      const steps = 160;
      const tMax = 2.8;

      for (const sign of [-1, 1]) {
        ctx.beginPath();
        for (let i = 0; i <= steps; i++) {
          const t = -tMax + (i / steps) * (2 * tMax);
          const ch = Math.cosh(t);
          const sh = Math.sinh(t);
          const x = isHoriz ? (h + sign * a * ch) : (h + b * sh);
          const y = isHoriz ? (k + b * sh) : (k + sign * a * ch);
          const sx = toScreenX(x);
          const sy = toScreenY(y);
          if (i === 0) ctx.moveTo(sx, sy);
          else ctx.lineTo(sx, sy);
        }
        ctx.stroke();
      }
      ctx.restore();
    }

    function drawNumberLinePlot(ctx, width, height, data, xMin, xMax, toScreenX) {
      const midY = height / 2;
      ctx.save();

      // Draw Main Horizontal Axis
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(30, midY);
      ctx.lineTo(width - 30, midY);
      ctx.stroke();

      // Arrows
      ctx.fillStyle = '#64748b';
      ctx.beginPath();
      ctx.moveTo(25, midY); ctx.lineTo(35, midY - 6); ctx.lineTo(35, midY + 6); ctx.closePath(); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(width - 25, midY); ctx.lineTo(width - 35, midY - 6); ctx.lineTo(width - 35, midY + 6); ctx.closePath(); ctx.fill();

      // Integer Ticks
      ctx.fillStyle = '#94a3b8';
      ctx.font = '11px ui-monospace, Menlo, monospace';
      for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
        const sx = toScreenX(x);
        if (sx < 40 || sx > width - 40) continue;
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(sx, midY - 8);
        ctx.lineTo(sx, midY + 8);
        ctx.stroke();
        ctx.fillText(x.toString(), sx - 5, midY + 24);
      }

      // Draw Shaded Intervals
      (data.intervals || []).forEach(iv => {
        const startX = iv.from === -Infinity ? 30 : toScreenX(iv.from);
        const endX = iv.to === Infinity ? width - 30 : toScreenX(iv.to);

        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 6;
        ctx.beginPath();
        ctx.moveTo(startX, midY);
        ctx.lineTo(endX, midY);
        ctx.stroke();

        // Endpoints
        if (iv.from !== -Infinity) {
          ctx.fillStyle = iv.inclusiveFrom ? '#10b981' : '#070d19';
          ctx.strokeStyle = '#10b981';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(startX, midY, 6, 0, Math.PI * 2);
          ctx.fill(); ctx.stroke();
          ctx.fillStyle = '#f8fafc';
          ctx.fillText(iv.fromLabel || iv.from.toString(), startX - 8, midY - 14);
        }
        if (iv.to !== Infinity) {
          ctx.fillStyle = iv.inclusiveTo ? '#10b981' : '#070d19';
          ctx.strokeStyle = '#10b981';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.arc(endX, midY, 6, 0, Math.PI * 2);
          ctx.fill(); ctx.stroke();
          ctx.fillStyle = '#f8fafc';
          ctx.fillText(iv.toLabel || iv.to.toString(), endX - 8, midY - 14);
        }
      });

      // Heading label
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 13px system-ui, sans-serif';
      ctx.fillText(`Solution Set Graph: ${data.intervalStr || ''}`, 40, 40);

      ctx.restore();
    }

    function attachCanvasTooltip(canvas, toScreenX, toScreenY, xMin, xMax, yMin, yMax, data) {
      if (canvas._tooltipAttached) return;
      canvas._tooltipAttached = true;
      const tooltip = document.getElementById('graphTooltip') || createGraphTooltip();

      canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        // Convert to Cartesian world coords
        const worldX = xMin + (mouseX / rect.width) * (xMax - xMin);
        const worldY = yMax - (mouseY / rect.height) * (yMax - yMin);

        let text = `x: ${worldX.toFixed(2)}, y: ${worldY.toFixed(2)}`;
        if (data.fn) {
          const fnY = data.fn(worldX);
          if (!isNaN(fnY) && isFinite(fnY)) {
            text = `x: ${worldX.toFixed(2)} | f(x) = ${fnY.toFixed(2)}`;
          }
        }

        tooltip.style.display = 'block';
        tooltip.style.left = (e.pageX + 12) + 'px';
        tooltip.style.top = (e.pageY - 24) + 'px';
        tooltip.textContent = text;
      });

      canvas.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
      });
    }

    function createGraphTooltip() {
      const tip = document.createElement('div');
      tip.id = 'graphTooltip';
      tip.style.position = 'absolute';
      tip.style.display = 'none';
      tip.style.background = 'rgba(15,23,42,0.95)';
      tip.style.border = '1px solid #38bdf8';
      tip.style.color = '#f8fafc';
      tip.style.fontFamily = 'monospace';
      tip.style.fontSize = '0.78rem';
      tip.style.padding = '4px 8px';
      tip.style.borderRadius = '4px';
      tip.style.pointerEvents = 'none';
      tip.style.zIndex = '9999';
      document.body.appendChild(tip);
      return tip;
    }

    // ==========================================================================
    // PARSER & GRAPH DATA BUILDER FOR FUNCTIONS & EQUATIONS
    // ==========================================================================

    function normalizeLatexToAscii(raw) {
      if (!raw) return '';
      let s = raw.trim();
      s = s.replace(/\$/g, '');
      s = s.replace(/\\left\s*\|/g, '|').replace(/\\right\s*\|/g, '|');
      s = s.replace(/\\left\s*\(/g, '(').replace(/\\right\s*\)/g, ')');
      s = s.replace(/\\left\s*\[/g, '[').replace(/\\right\s*\]/g, ']');
      s = s.replace(/\\pi\b/g, 'pi');
      // Replace inner sqrt{} first so nested \frac{\sqrt{...}}{...} has no inner curly braces!
      for (let i = 0; i < 4; i++) {
        s = s.replace(/\\sqrt\{([^{}]+)\}/g, 'sqrt($1)');
      }
      // Repeatedly convert \frac{A}{B} -> ((A)/(B))
      for (let i = 0; i < 4; i++) {
        s = s.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '(($1)/($2))');
      }
      s = s.replace(/\\sqrt\{([^{}]+)\}/g, 'sqrt($1)');
      s = s.replace(/\\le(?:q)?\b/g, '<=').replace(/\\ge(?:q)?\b/g, '>=');
      s = s.replace(/\\cdot/g, '*').replace(/\\times/g, '*');
      s = s.replace(/[•⋅·]/g, '*');
      s = s.replace(/\\ln\b/g, 'ln').replace(/\\log_\{([^{}]+)\}/g, 'log_$1').replace(/\\log_([0-9a-zA-Z]+)/g, 'log_$1').replace(/\\log\b/g, 'log');
      s = s.replace(/\^\{([^{}]+)\}/g, '^($1)');
      s = s.replace(/²/g, '^2').replace(/³/g, '^3').replace(/⁴/g, '^4').replace(/⁵/g, '^5');
      s = s.replace(/≤/g, '<=').replace(/≥/g, '>=').replace(/−/g, '-').replace(/–/g, '-');
      return s.trim();
    }

    function buildGraphDataFromParsed(parsed, rawStr) {
      if (!parsed) return null;

      // 1. Quadratic Function f(x) = ax^2 + bx + c
      if (parsed.type === 'quadratic') {
        const a = parsed.a;
        const b = parsed.b;
        const c = parsed.c;
        const vx = -b / (2 * a);
        const vy = a * vx * vx + b * vx + c;
        const fn = (x) => a * x * x + b * x + c;

        const disc = b * b - 4 * a * c;
        const pts = [
          { x: vx, y: vy, type: 'vertex', color: '#38bdf8', label: `V(${vx.toFixed(2)}, ${vy.toFixed(2)})` },
          { x: 0, y: c, type: 'point', color: '#a855f7', label: `(0, ${c})` }
        ];
        if (disc >= 0) {
          const r1 = (-b + Math.sqrt(disc)) / (2 * a);
          const r2 = (-b - Math.sqrt(disc)) / (2 * a);
          pts.push({ x: r1, y: 0, type: 'point', color: '#34d399', label: `(${r1.toFixed(2)}, 0)` });
          if (Math.abs(r1 - r2) > 1e-6) {
            pts.push({ x: r2, y: 0, type: 'point', color: '#34d399', label: `(${r2.toFixed(2)}, 0)` });
          }
        }

        return {
          id: `quad_${a}_${b}_${c}`,
          type: 'function',
          fn: fn,
          axisOfSymmetry: vx,
          points: pts,
          curveColor: '#38bdf8',
          label: `Parabola: f(x) = ${a}x² + (${b})x + (${c})`
        };
      }

      // 2. Vertex Form f(x) = a(x - h)^2 + k
      if (parsed.type === 'quad_vertex') {
        const { a, h, k } = parsed;
        const fn = (x) => a * Math.pow(x - h, 2) + k;
        const pts = [
          { x: h, y: k, type: 'vertex', color: '#38bdf8', label: `V(${h}, ${k})` },
          { x: 0, y: a * h * h + k, type: 'point', color: '#a855f7', label: `(0, ${(a * h * h + k).toFixed(2)})` }
        ];
        if (-k / a >= 0) {
          const dx = Math.sqrt(-k / a);
          pts.push({ x: h - dx, y: 0, type: 'point', color: '#34d399', label: `(${(h - dx).toFixed(2)}, 0)` });
          if (dx > 1e-6) {
            pts.push({ x: h + dx, y: 0, type: 'point', color: '#34d399', label: `(${(h + dx).toFixed(2)}, 0)` });
          }
        }
        return {
          id: `quad_v_${a}_${h}_${k}`,
          type: 'function',
          fn: fn,
          axisOfSymmetry: h,
          points: pts,
          curveColor: '#38bdf8',
          label: `Parabola (Vertex Form): f(x) = ${a}(x - ${h})² + ${k}`
        };
      }

      // 3. Circle Standard & General
      if (parsed.type === 'circle_std' || parsed.type === 'circle_gen') {
        let h = parsed.h || 0;
        let k = parsed.k || 0;
        let r = parsed.r || 1;
        if (parsed.type === 'circle_gen') {
          h = -parsed.b / (2 * parsed.a);
          k = -parsed.c / (2 * parsed.a);
          const rSq = (parsed.b * parsed.b + parsed.c * parsed.c - 4 * parsed.a * parsed.d) / (4 * parsed.a * parsed.a);
          r = Math.sqrt(Math.max(0, rSq));
        }
        return {
          id: `circle_${h}_${k}_${r}`,
          type: 'circle',
          circle: { h, k, r },
          points: [
            { x: h + r, y: k, type: 'point', color: '#38bdf8', label: `(${(h+r).toFixed(1)}, ${k.toFixed(1)})` },
            { x: h - r, y: k, type: 'point', color: '#38bdf8', label: `(${(h-r).toFixed(1)}, ${k.toFixed(1)})` },
            { x: h, y: k + r, type: 'point', color: '#38bdf8', label: `(${h.toFixed(1)}, ${(k+r).toFixed(1)})` },
            { x: h, y: k - r, type: 'point', color: '#38bdf8', label: `(${h.toFixed(1)}, ${(k-r).toFixed(1)})` }
          ],
          label: `Circle: Center (${h.toFixed(2)}, ${k.toFixed(2)}), Radius ${r.toFixed(2)}`
        };
      }

      // 3b. Ellipse (Ch 10.2)
      if (parsed.type === 'ellipse') {
        const { h, k, rx, ry } = parsed;
        const a = Math.max(rx, ry);
        const b = Math.min(rx, ry);
        const c = Math.sqrt(Math.max(0, a * a - b * b));
        const isHoriz = rx >= ry;
        const pts = [
          { x: h, y: k, type: 'point', color: '#a855f7', label: `C(${h}, ${k})` },
          { x: h + rx, y: k, type: 'vertex', color: '#38bdf8', label: `V(${(h+rx).toFixed(1)}, ${k})` },
          { x: h - rx, y: k, type: 'vertex', color: '#38bdf8', label: `V(${(h-rx).toFixed(1)}, ${k})` },
          { x: h, y: k + ry, type: 'point', color: '#34d399', label: `(${h}, ${(k+ry).toFixed(1)})` },
          { x: h, y: k - ry, type: 'point', color: '#34d399', label: `(${h}, ${(k-ry).toFixed(1)})` }
        ];
        if (c > 1e-4) {
          if (isHoriz) {
            pts.push({ x: h + c, y: k, type: 'point', color: '#fbbf24', label: `F(${(h+c).toFixed(2)}, ${k})` });
            pts.push({ x: h - c, y: k, type: 'point', color: '#fbbf24', label: `F(${(h-c).toFixed(2)}, ${k})` });
          } else {
            pts.push({ x: h, y: k + c, type: 'point', color: '#fbbf24', label: `F(${h}, ${(k+c).toFixed(2)})` });
            pts.push({ x: h, y: k - c, type: 'point', color: '#fbbf24', label: `F(${h}, ${(k-c).toFixed(2)})` });
          }
        }
        return {
          id: `ellipse_${h}_${k}_${rx}_${ry}`,
          type: 'ellipse',
          ellipse: { h, k, rx, ry },
          points: pts,
          label: `Ellipse: Center (${h}, ${k}), rx = ${rx.toFixed(2)}, ry = ${ry.toFixed(2)}`
        };
      }

      // 3c. Hyperbola (Ch 10.3)
      if (parsed.type === 'hyperbola') {
        const { h, k, a, b, transverse } = parsed;
        const c = Math.sqrt(a * a + b * b);
        const isHoriz = transverse !== 'vertical';
        const pts = [
          { x: h, y: k, type: 'point', color: '#a855f7', label: `C(${h}, ${k})` }
        ];
        if (isHoriz) {
          pts.push({ x: h + a, y: k, type: 'vertex', color: '#38bdf8', label: `V(${(h+a).toFixed(1)}, ${k})` });
          pts.push({ x: h - a, y: k, type: 'vertex', color: '#38bdf8', label: `V(${(h-a).toFixed(1)}, ${k})` });
          pts.push({ x: h + c, y: k, type: 'point', color: '#fbbf24', label: `F(${(h+c).toFixed(2)}, ${k})` });
          pts.push({ x: h - c, y: k, type: 'point', color: '#fbbf24', label: `F(${(h-c).toFixed(2)}, ${k})` });
        } else {
          pts.push({ x: h, y: k + a, type: 'vertex', color: '#38bdf8', label: `V(${h}, ${(k+a).toFixed(1)})` });
          pts.push({ x: h, y: k - a, type: 'vertex', color: '#38bdf8', label: `V(${h}, ${(k-a).toFixed(1)})` });
          pts.push({ x: h, y: k + c, type: 'point', color: '#fbbf24', label: `F(${h}, ${(k+c).toFixed(2)})` });
          pts.push({ x: h, y: k - c, type: 'point', color: '#fbbf24', label: `F(${h}, ${(k-c).toFixed(2)})` });
        }
        return {
          id: `hyp_${h}_${k}_${a}_${b}_${transverse}`,
          type: 'hyperbola',
          hyperbola: { h, k, a, b, transverse },
          points: pts,
          label: `Hyperbola (${transverse}): Center (${h}, ${k}), a = ${a.toFixed(2)}, b = ${b.toFixed(2)}`
        };
      }

      // 4. Rational Functions & Rational Inequalities
      if (parsed.type === 'rational' || parsed.type === 'rat_ineq' || parsed.type === 'synthetic') {
        const numC = parsed.numCoeffs || parseAnyPolyCoeffs(parsed.poly || '1');
        const denC = parsed.denCoeffs || [1, -(parsed.c || 0)];
        return buildRationalGraphData(numC, denC, rawStr);
      }

      // 5. Polynomial Functions & Polynomial Inequalities
      if (parsed.type === 'polynomial' || parsed.type === 'poly_ineq') {
        return buildPolynomialGraphData(parsed.coeffs, rawStr);
      }

      // 6. Exponential Functions & Equations (Ch 4.2, 4.5)
      if (parsed.type === 'exp_func') {
        const { a, base, h, k } = parsed;
        const fn = (x) => a * Math.pow(base, x - h) + k;
        const y0 = fn(0);
        const pts = [
          { x: h, y: a + k, type: 'vertex', color: '#38bdf8', label: `(${h}, ${(a + k).toFixed(2)})` }
        ];
        if (isFinite(y0) && Math.abs(y0) < 100) {
          pts.push({ x: 0, y: y0, type: 'point', color: '#a855f7', label: `(0, ${y0.toFixed(2)})` });
        }
        if (parsed.solX !== undefined && isFinite(parsed.solX)) {
          pts.push({ x: parsed.solX, y: parsed.rhs || 0, type: 'point', color: '#34d399', label: `Sol(${parsed.solX.toFixed(2)}, ${(parsed.rhs || 0).toFixed(2)})` });
        }
        return {
          id: `exp_${a}_${base}_${h}_${k}`,
          type: 'function',
          fn: fn,
          horizAsymptote: { eq: `y = ${k}`, val: k },
          points: pts,
          curveColor: '#38bdf8',
          label: `Exponential: f(x) = ${a === 1 ? '' : a + '·'}${base === Math.E ? 'e' : base}^(x - ${h}) + ${k}`
        };
      }

      // 6b. sqrt function graph (Ch 1.3 / radical functions)
      if (parsed.type === 'sqrt_func') {
        const { a, inside, lin, k } = parsed;
        const fn = (x) => { const v = lin.m * x + lin.b; return (v >= -1e-12) ? a * Math.sqrt(Math.max(0, v)) + k : NaN; };
        return {
          id: `sqrtfn_${a}_${lin.m}_${lin.b}_${k}`,
          type: 'function',
          fn: fn,
          points: [
            { x: -lin.b / lin.m, y: k, type: 'vertex', color: '#38bdf8', label: `(${Number((-lin.b / lin.m).toFixed(2))}, ${Number(k.toFixed(2))})` },
            { x: -lin.b / lin.m + Math.max(1, Math.abs(lin.m)), y: a * Math.sqrt(Math.abs(lin.m)) + k, type: 'point', color: '#34d399', label: `√${inside}` }
          ],
          curveColor: '#38bdf8',
          label: `f(x) = ${a === 1 ? '' : a}√(${inside})${k ? (k > 0 ? ' + ' + k : ' - ' + Math.abs(k)) : ''}`
        };
      }

      // 6c. Absolute value function graph (Ch 1.6 / 3.1 one-to-one checks)
      if (parsed.type === 'abs_func') {
        const { a, inside, lin, d } = parsed;
        const fn = (x) => a * Math.abs(lin.m * x + lin.b) + d;
        return {
          id: `absfn_${a}_${lin.m}_${lin.b}_${d}`,
          type: 'function',
          fn: fn,
          axisOfSymmetry: -lin.b / lin.m,
          points: [
            { x: -lin.b / lin.m, y: d, type: 'vertex', color: '#38bdf8', label: `V(${Number((-lin.b / lin.m).toFixed(2))}, ${Number(d.toFixed(2))})` }
          ],
          curveColor: '#38bdf8',
          label: `f(x) = ${a === 1 ? '' : a}|${inside}|${d ? (d > 0 ? ' + ' + d : ' - ' + Math.abs(d)) : ''}`
        };
      }

      // 6d. Exponential equation graph: root of b1^E1 = b2^E2
      if (parsed.type === 'exp_eq') {
        const f1 = compileMathFunction(parsed.lhs);
        const f2 = compileMathFunction(parsed.rhs);
        if (f1 && f2) {
          return {
            id: `expeq_${parsed.lhs}_${parsed.rhs}`,
            type: 'function',
            fn: (x) => f1(x) - f2(x),
            points: [
              { x: parsed.x, y: 0, type: 'vertex', color: '#34d399', label: `x = ${parsed.xStr}` }
            ],
            curveColor: '#fbbf24',
            label: `${parsed.lhs} − (${parsed.rhs}) → root x = ${parsed.xStr}`
          };
        }
        return null;
      }

      // 6e. Log equation (quadratic argument) graph
      if (parsed.type === 'log_eq2') {
        const pts = (parsed.roots || []).map(r => ({
          x: Number(r.toFixed(2)), y: 0, type: 'vertex', color: '#34d399',
          label: `x = ${rationalizeVal(r)}`
        }));
        return {
          id: `logeq2_${parsed.kind}_${(parsed.roots || []).join('_')}`,
          type: 'number_line',
          intervals: (parsed.roots || []).map(r => ({ from: r, to: r, inclusiveFrom: true, inclusiveTo: true })),
          intervalStr: `{${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}}`,
          label: `Log equation roots: {${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}}`
        };
      }

      // 7. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      if (parsed.type === 'log_func') {
        const { a, base, h, k } = parsed;
        const fn = (x) => (x > h) ? (a * (Math.log(x - h) / Math.log(base)) + k) : NaN;
        const pts = [
          { x: h + 1, y: k, type: 'vertex', color: '#38bdf8', label: `(${(h + 1).toFixed(2)}, ${k.toFixed(2)})` },
          { x: h + base, y: a + k, type: 'point', color: '#a855f7', label: `(${(h + base).toFixed(2)}, ${(a + k).toFixed(2)})` }
        ];
        if (parsed.solX !== undefined && isFinite(parsed.solX)) {
          pts.push({ x: parsed.solX, y: parsed.rhs || 0, type: 'point', color: '#34d399', label: `Sol(${parsed.solX.toFixed(2)}, ${(parsed.rhs || 0).toFixed(2)})` });
        }
        return {
          id: `log_${a}_${base}_${h}_${k}`,
          type: 'function',
          fn: fn,
          vertAsymptotes: [{ val: h, label: `${h}` }],
          points: pts,
          curveColor: '#38bdf8',
          label: `Logarithm: f(x) = ${a === 1 ? '' : a}${base === Math.E ? 'ln' : 'log_' + base}(x - ${h}) + ${k}`
        };
      }

      // 8. Systems of Equations (Ch 9.1 & 9.5)
      if (parsed.type === 'system_2x2') {
        return parsed.graphData || null;
      }

      // 9. Absolute Value Inequality / Equation Number Line & 2D Graph
      if (parsed.type === 'abs' || parsed.type === 'abs_double') {
        if (parsed.type === 'abs_double') {
          const { a1, b1, a2, b2, sols } = parsed;
          const fn1 = (x) => Math.abs(a1 * x + b1);
          const fn2 = (x) => Math.abs(a2 * x + b2);
          const pts = (sols || []).map(sx => ({
            x: sx,
            y: fn1(sx),
            type: 'vertex',
            color: '#34d399',
            label: `(${sx.toFixed(2)}, ${fn1(sx).toFixed(2)})`
          }));
          return {
            id: `abs2_${a1}_${b1}_${a2}_${b2}`,
            type: 'function',
            fn: fn1,
            fn2: fn2,
            points: pts,
            curveColor: '#38bdf8',
            curve2Color: '#fbbf24',
            label: `|${a1}x + ${b1}| vs |${a2}x + ${b2}|`
          };
        }

        const { a, b, op, c } = parsed;
        if (c < 0) {
          const isAll = (op === '>' || op === '>=');
          const ivStr = isAll ? '(-∞, ∞)' : '∅ (No Solution)';
          return {
            id: `abs_${a}_${b}_${c}`,
            type: 'number_line',
            intervals: isAll ? [{ from: -Infinity, to: Infinity }] : [],
            intervalStr: ivStr,
            label: `Number Line: ${isAll ? 'All Real Numbers (-∞, ∞)' : 'Empty Set ∅ (No Real Solution)'}`
          };
        }
        const leftB = (-c - b) / a;
        const rightB = (c - b) / a;
        const p1 = Math.min(leftB, rightB);
        const p2 = Math.max(leftB, rightB);
        const isStrict = (op === '<' || op === '>');

        let intervals = [];
        let ivStr = '';
        if (op === '<' || op === '<=') {
          intervals = [{ from: p1, to: p2, inclusiveFrom: !isStrict, inclusiveTo: !isStrict }];
          ivStr = isStrict ? `(${p1.toFixed(2)}, ${p2.toFixed(2)})` : `[${p1.toFixed(2)}, ${p2.toFixed(2)}]`;
        } else if (op === '>' || op === '>=') {
          intervals = [
            { from: -Infinity, to: p1, inclusiveTo: !isStrict },
            { from: p2, to: Infinity, inclusiveFrom: !isStrict }
          ];
          ivStr = isStrict ? `(-∞, ${p1.toFixed(2)}) ∪ (${p2.toFixed(2)}, ∞)` : `(-∞, ${p1.toFixed(2)}] ∪ [${p2.toFixed(2)}, ∞)`;
        } else if (op === '=') {
          intervals = [
            { from: p1, to: p1, inclusiveFrom: true, inclusiveTo: true },
            { from: p2, to: p2, inclusiveFrom: true, inclusiveTo: true }
          ];
          ivStr = `{${p1.toFixed(2)}, ${p2.toFixed(2)}}`;
        }

        return {
          id: `abs_${a}_${b}_${c}`,
          type: 'number_line',
          intervals: intervals,
          intervalStr: ivStr,
          label: `Number Line Solution Set: ${ivStr}`
        };
      }

      // 10. Two Coordinate Points (Ch 1.1 & 2.3–2.4): Distance, Midpoint, Line
      if (parsed.type === 'two_points') {
        const { x1, y1, x2, y2, mx, my, m, b } = parsed;
        const pts = [
          { x: x1, y: y1, type: 'vertex', color: '#38bdf8', label: `P1(${x1}, ${y1})` },
          { x: x2, y: y2, type: 'vertex', color: '#38bdf8', label: `P2(${x2}, ${y2})` },
          { x: mx, y: my, type: 'point', color: '#34d399', label: `Mid(${Number(mx.toFixed(2))}, ${Number(my.toFixed(2))})` }
        ];
        return {
          id: `pts_${x1}_${y1}_${x2}_${y2}`,
          type: 'function',
          fn: isFinite(m) ? (x) => m * x + b : null,
          vertAsymptotes: !isFinite(m) ? [{ val: x1, label: `${x1}` }] : [],
          points: pts,
          curveColor: '#38bdf8',
          label: `Points (${x1}, ${y1}) & (${x2}, ${y2}) • Midpoint (${Number(mx.toFixed(2))}, ${Number(my.toFixed(2))})`
        };
      }

      // 10b. Multi-Point Polynomial Interpolation (3+ Coordinate Points, e.g., A, B, C, D)
      if (parsed.type === 'poly_points') {
        const { pts, evalFn, factoredStr } = parsed;
        return {
          id: `polypts_${pts.map(p => p.x + '_' + p.y).join('_')}`,
          type: 'function',
          fn: evalFn,
          points: pts.map((p, idx) => ({
            x: p.x,
            y: p.y,
            type: p.y === 0 ? 'vertex' : 'point',
            color: p.y === 0 ? '#38bdf8' : '#34d399',
            label: `${p.name || 'P' + (idx + 1)}(${p.x}, ${p.y})`
          })),
          curveColor: '#38bdf8',
          label: `Polynomial Through Points: f(x) = ${factoredStr}`
        };
      }

      // 11. Numeric Logarithm Evaluation (Ch 4.3–4.4)
      if (parsed.type === 'log_eval') {
        const { a, base, argVal, resultVal } = parsed;
        const fn = (x) => (x > 0) ? a * (Math.log(x) / Math.log(base)) : NaN;
        return {
          id: `logeval_${a}_${base}_${argVal}`,
          type: 'function',
          fn: fn,
          vertAsymptotes: [{ val: 0, label: '0' }],
          points: [
            { x: 1, y: 0, type: 'point', color: '#a855f7', label: '(1, 0)' },
            { x: argVal, y: resultVal, type: 'vertex', color: '#34d399', label: `(${Number(argVal.toFixed(2))}, ${Number(resultVal.toFixed(3))})` }
          ],
          curveColor: '#38bdf8',
          label: `Log Evaluation: (${Number(argVal.toFixed(2))}, ${Number(resultVal.toFixed(4))})`
        };
      }

      // 12. Linear Function / Equation & Inverse (Ch 1.2, 2.3, 2.7)
      if (parsed.type === 'linear') {
        const { m, b } = parsed;
        const xInt = Math.abs(m) > 1e-9 ? -b / m : 0;
        return {
          id: `lin_${m}_${b}`,
          type: 'function',
          fn: (x) => m * x + b,
          fn2: Math.abs(m) > 1e-9 ? (x) => (x - b) / m : null,
          points: [
            { x: xInt, y: 0, type: 'vertex', color: '#34d399', label: `(${Number(xInt.toFixed(2))}, 0)` },
            { x: 0, y: b, type: 'point', color: '#a855f7', label: `(0, ${Number(b.toFixed(2))})` }
          ],
          curveColor: '#38bdf8',
          curve2Color: '#10b981',
          label: `Linear f(x) = ${m}x + (${b}) & Inverse f⁻¹(x)`
        };
      }

      // 13. Complex Quadratic Solution Verification Parabola (Ch 1.3 Q17–18)
      if (parsed.type === 'complex_verify_quad') {
        const a = 1, b = parsed.p, c = parsed.q;
        const vx = -b / (2 * a);
        const vy = a * vx * vx + b * vx + c;
        const fn = (x) => a * x * x + b * x + c;
        const pts = [
          { x: vx, y: vy, type: 'vertex', color: '#38bdf8', label: `Vertex (${vx.toFixed(2)}, ${vy.toFixed(2)})` },
          { x: 0, y: c, type: 'point', color: '#a855f7', label: `(0, ${c})` }
        ];
        return {
          id: `cplx_quad_${b}_${c}`,
          type: 'function',
          fn: fn,
          axisOfSymmetry: vx,
          points: pts,
          curveColor: '#38bdf8',
          label: `Parabola f(x) = x² ${b >= 0 ? '+ ' + b : '- ' + Math.abs(b)}x + ${c} (Complex Roots: ${parsed.u} ± ${Math.abs(parsed.v)}i)`
        };
      }

      return null;
    }

    function buildRationalGraphData(numCoeffs, denCoeffs, rawStr) {
      // Evaluate polynomial values
      const evalPoly = (c, x) => c.reduce((acc, val) => acc * x + val, 0);

      const numRoots = findRationalRootsJS(numCoeffs);
      const denRoots = findRationalRootsJS(denCoeffs);

      // Check for common root (Hole)
      const holes = [];
      const vertAsymp = [];
      const pts = [];

      denRoots.forEach(dr => {
        const matchIdx = numRoots.findIndex(nr => Math.abs(nr - dr) < 1e-4);
        if (matchIdx !== -1) {
          // Hole!
          const holeX = dr;
          // Approximate reduced value
          const eps = 1e-5;
          const yApprox = (evalPoly(numCoeffs, holeX + eps) / evalPoly(denCoeffs, holeX + eps) +
                           evalPoly(numCoeffs, holeX - eps) / evalPoly(denCoeffs, holeX - eps)) / 2;
          holes.push({ x: holeX, y: yApprox });
          pts.push({ x: holeX, y: yApprox, type: 'hole', label: `Hole(${holeX.toFixed(2)}, ${yApprox.toFixed(2)})` });
        } else {
          vertAsymp.push({ val: dr, label: dr.toFixed(2) });
        }
      });

      // Intercepts
      const distinctNumRoots = Array.from(new Set(numRoots.map(r => Number(r.toFixed(4)))));
      distinctNumRoots.forEach(nr => {
        if (!holes.some(h => Math.abs(h.x - nr) < 1e-4)) {
          pts.push({ x: nr, y: 0, type: 'point', color: '#34d399', label: `(${Number(nr.toFixed(2))}, 0)` });
        }
      });

      const d0 = evalPoly(denCoeffs, 0);
      if (Math.abs(d0) > 1e-7) {
        const y0 = evalPoly(numCoeffs, 0) / d0;
        if (!isNaN(y0) && isFinite(y0)) {
          if (!pts.some(p => p.x === 0 && Math.abs(p.y - y0) < 1e-4)) {
            pts.push({ x: 0, y: y0, type: 'point', color: '#a855f7', label: `(0, ${Number(y0.toFixed(2))})` });
          }
        }
      }

      // Horizontal Asymptote
      let horizAsymp = null;
      let slantAsymp = null;
      const degNum = numCoeffs.length - 1;
      const degDen = denCoeffs.length - 1;

      if (degNum < degDen) {
        horizAsymp = { eq: 'y = 0', val: 0 };
      } else if (degNum === degDen) {
        const yVal = numCoeffs[0] / denCoeffs[0];
        horizAsymp = { eq: `y = ${Number(yVal.toFixed(2))}`, val: yVal };
      } else if (degNum === degDen + 1) {
        // Slant/oblique asymptote: quotient of degree (d+1) by degree d is linear y = mx + b
        const a = numCoeffs[0], b = numCoeffs[1] || 0;
        const p = denCoeffs[0], q = denCoeffs[1] || 0;
        const m = a / p;
        const bSlant = (b - m * q) / p;
        const mStr = Math.abs(m - 1) < 1e-6 ? '' : (Math.abs(m + 1) < 1e-6 ? '-' : Number(m.toFixed(2)));
        let eq = `y = ${mStr}x`;
        if (Math.abs(bSlant) > 1e-6) {
          eq += ` ${bSlant > 0 ? '+' : '-'} ${Number(Math.abs(bSlant).toFixed(2))}`;
        }
        slantAsymp = { eq, m, b: bSlant };
      }

      const fn = (x) => {
        const dVal = evalPoly(denCoeffs, x);
        if (Math.abs(dVal) < 1e-7) return NaN;
        return evalPoly(numCoeffs, x) / dVal;
      };

      return {
        id: `rat_${numCoeffs.join('_')}_${denCoeffs.join('_')}`,
        type: 'function',
        fn: fn,
        vertAsymptotes: vertAsymp,
        horizAsymptote: horizAsymp,
        slantAsymptote: slantAsymp,
        points: pts,
        curveColor: '#38bdf8',
        label: `Rational Function: ${rawStr}`
      };
    }

    function buildPolynomialGraphData(coeffs, rawStr) {
      const evalPoly = (c, x) => c.reduce((acc, val) => acc * x + val, 0);
      const fn = (x) => evalPoly(coeffs, x);

      const roots = findRationalRootsJS(coeffs);
      const rootCounts = {};
      roots.forEach(r => {
        const key = r.toFixed(3);
        rootCounts[key] = (rootCounts[key] || 0) + 1;
      });

      const pts = [
        { x: 0, y: coeffs[coeffs.length - 1], type: 'point', color: '#a855f7', label: `(0, ${coeffs[coeffs.length - 1]})` }
      ];

      Object.keys(rootCounts).forEach(key => {
        const rVal = parseFloat(key);
        const mult = rootCounts[key];
        const isCross = (mult % 2 !== 0);
        pts.push({
          x: rVal,
          y: 0,
          type: isCross ? 'point' : 'vertex',
          color: isCross ? '#38bdf8' : '#fbbf24',
          label: `(${rVal.toFixed(2)}, 0) [${isCross ? 'crosses' : 'turns'}]`
        });
      });

      return {
        id: `poly_${coeffs.join('_')}`,
        type: 'function',
        fn: fn,
        points: pts,
        curveColor: '#38bdf8',
        label: `Polynomial: ${rawStr}`
      };
    }

    // ==========================================================================
    // DEDICATED GRAPHER TAB CONTROLLER
    // ==========================================================================

    function plotCustomFunction() {
      const inputEl = document.getElementById('customGraphInput');
      const raw = (inputEl ? inputEl.value : '').trim();
      if (!raw) return;

      const detailsEl = document.getElementById('graphDetailsCard');

      // Check if it matches parsed equation syntax
      let parsed = parseEquationSyntax(raw);
      let graphData = null;

      if (parsed) {
        graphData = buildGraphDataFromParsed(parsed, raw);
      }

      // If not parsed by standard regex, compile generic math function
      if (!graphData) {
        const compiled = compileMathFunction(raw);
        if (compiled) {
          graphData = {
            id: `custom_${raw}`,
            type: 'function',
            fn: compiled,
            points: [{ x: 0, y: compiled(0), type: 'point', color: '#a855f7', label: `(0, ${compiled(0).toFixed(2)})` }],
            curveColor: '#38bdf8',
            label: `f(x) = ${raw}`
          };
        }
      }

      if (graphData) {
        renderUniversalGraph('mainGraphCanvas', graphData);

        // Populate details card
        if (detailsEl) {
          let html = '';
          html += `
            <div style="background:var(--surface-card); padding:12px; border-radius:8px; border:1px solid var(--border);">
              <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Plotted Function</div>
              <div style="font-size:1.05rem; font-weight:700; color:#38bdf8; margin-top:4px;">${graphData.label || raw}</div>
            </div>
          `;

          if (graphData.points && graphData.points.length > 0) {
            html += `
              <div style="background:var(--surface-card); padding:12px; border-radius:8px; border:1px solid var(--border);">
                <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase;">Critical Points Plotted</div>
                <div style="font-size:0.92rem; color:#f8fafc; margin-top:4px;">${graphData.points.map(p => p.label).join(' &nbsp;•&nbsp; ')}</div>
              </div>
            `;
          }

          if (graphData.vertAsymptotes && graphData.vertAsymptotes.length > 0) {
            html += `
              <div style="background:var(--surface-card); padding:12px; border-radius:8px; border:1px solid var(--border);">
                <div style="font-size:0.75rem; color:#f43f5e; text-transform:uppercase;">Vertical Asymptotes</div>
                <div style="font-size:0.95rem; font-weight:700; color:#f43f5e; margin-top:4px;">${graphData.vertAsymptotes.map(v => v.label).join(', ')}</div>
              </div>
            `;
          }

          if (graphData.horizAsymptote || graphData.slantAsymptote) {
            const asymp = graphData.horizAsymptote || graphData.slantAsymptote;
            html += `
              <div style="background:var(--surface-card); padding:12px; border-radius:8px; border:1px solid var(--border);">
                <div style="font-size:0.75rem; color:#fbbf24; text-transform:uppercase;">End Behavior Asymptote</div>
                <div style="font-size:0.95rem; font-weight:700; color:#fbbf24; margin-top:4px;">${asymp.eq}</div>
              </div>
            `;
          }

          detailsEl.innerHTML = html;
        }
      } else {
        if (detailsEl) {
          detailsEl.innerHTML = `<div style="grid-column:1/-1; color:#ef4444; padding:12px; background:rgba(239,68,68,0.1); border-radius:8px;">Could not parse function "${raw}". Try standard expressions like "2x^2 - 8x - 12", "(x - 2)/(x^2 - 1)", or "x^3 - 3x".</div>`;
        }
      }
    }

    function setGraphPreset(expr) {
      const inputEl = document.getElementById('customGraphInput');
      if (inputEl) inputEl.value = expr;
      plotCustomFunction();
    }

    function openInDedicatedGrapher(expr) {
      const decoded = decodeURIComponent(expr || '');
      switchMainTab('graph');
      const inputEl = document.getElementById('customGraphInput');
      if (inputEl && decoded) {
        inputEl.value = decoded;
      }
      setTimeout(plotCustomFunction, 40);
    }

    function compileMathFunction(expr) {
      let s = normalizeLatexToAscii(expr)
        .replace(/^(?:[fghpqr]\(x\)|y)\s*=\s*/i, "")
        .replace(/\s*(?:<=|>=|<|>|=)\s*0\s*$/i, "")
        .replace(/\|([^|]+)\|/g, "abs($1)")
        .replace(/log_(\d+(?:\.\d+)?)\(([^)]+)\)/gi, "(Math.log($2)/Math.log($1))")
        .replace(/sqrt\(/gi, "Math.sqrt(")
        .replace(/abs\(/gi, "Math.abs(")
        .replace(/log\(/gi, "Math.log10(")
        .replace(/ln\(/gi, "Math.log(")
        .replace(/\be\b/g, "Math.E")
        .replace(/-\s*\(/g, "-1*(")
        .replace(/^-\s*x/g, "-1*x")
        .replace(/([+-])\s*x\^/g, "$1 1*x^")
        .replace(/(\d+)([a-zA-Z\(])/g, "$1*$2")
        .replace(/\)([a-zA-Z0-9\(])/g, ")*$1")
        .replace(/x\(/g, "x*(")
        .replace(/\^/g, "**");

      try {
        const fn = new Function("x", "Math", `
          try {
            with (Math) {
              return ${s};
            }
          } catch(e) {
            return NaN;
          }
        `);
        fn(2, Math);
        return (x) => fn(x, Math);
      } catch(e) {
        return null;
      }
    }

    // Load embedded answer sheets data and database catalog (100% offline & file:// safe)
    let answersData = {};
    let courseDatabase = { catalog: [], topics: [] };

    try {
      const rawAnswers = document.getElementById('embedded-data').textContent.trim();
      answersData = JSON.parse(rawAnswers);
    } catch (e) {
      console.error('Failed to parse embedded answers data', e);
    }

    try {
      const rawDb = document.getElementById('database-data').textContent.trim();
      courseDatabase = JSON.parse(rawDb);
      const dbBadge = document.getElementById('dbStatusBadge');
      if (dbBadge && courseDatabase.catalog) {
        const asgns = new Set(courseDatabase.catalog.map(c => c.assignment)).size;
        dbBadge.textContent = `● ${asgns} Assignments • ${courseDatabase.catalog.length} Questions`;
      }
    } catch (e) {
      console.error('Failed to parse database data', e);
    }

    const fileListEl = document.getElementById('fileList');
    const docContainer = document.getElementById('docContainer');
    let currentFileName = '';

    function countQuestionsInMd(md) {
      if (!md) return 0;
      const h3Matches = md.match(/^###\s+\*?\*?Question\s+\d+\b/gim);
      if (h3Matches && h3Matches.length > 0) return h3Matches.length;
      const bulletMatches = md.match(/^\*\s+\*?\*?(?:Question\s+\d+|Q\d+)\b/gim);
      return bulletMatches ? bulletMatches.length : 0;
    }

    function formatPickerLabel(name) {
      const cleanName = name.replace(' - Answers.md', '').replace('.md', '');
      const qCount = countQuestionsInMd(answersData[name]);
      const icon = cleanName.startsWith('Build Understanding') ? '📘' : (cleanName.startsWith('Pre-work') ? '📝' : '⭐');
      return `${icon} ${cleanName}${qCount ? ` (${qCount} Qs)` : ''}`;
    }

    function initFileList() {
      const fileNames = Object.keys(answersData);
      if (fileNames.length === 0) {
        fileListEl.innerHTML = '<div style="padding:16px; color:var(--text-muted);">No answer sheets found.</div>';
        return;
      }
      renderFiles(fileNames);
      const topSelect = document.getElementById('topAssignmentSelect');
      if (topSelect) {
        topSelect.innerHTML = fileNames.map(name => {
          return `<option value="${name.replace(/"/g, '&quot;')}">${formatPickerLabel(name)}</option>`;
        }).join('');
      }
      loadFile(fileNames[0]);
    }

    function toggleSidebar() {
      const sb = document.getElementById('sidebar');
      const topBtn = document.getElementById('topToggleSidebarBtn');
      if (!sb) return;
      const isCollapsed = sb.classList.toggle('collapsed');
      if (topBtn) {
        topBtn.innerHTML = isCollapsed ? '☰ Show Sidebar' : '◀ Hide Sidebar';
      }
      setTimeout(renderAllInlineGraphs, 50);
    }

    function stepAssignment(delta) {
      const fileNames = Object.keys(answersData);
      if (fileNames.length === 0) return;
      const idx = fileNames.indexOf(currentFileName);
      const nextIdx = ((idx === -1 ? 0 : idx) + delta + fileNames.length) % fileNames.length;
      loadFile(fileNames[nextIdx]);
    }

    function renderFiles(files) {
      fileListEl.innerHTML = files.map(name => {
        const cleanName = name.replace(' - Answers.md', '').replace('.md', '');
        const qCount = countQuestionsInMd(answersData[name]);
        const icon = cleanName.startsWith('Build Understanding') ? '📘' : (cleanName.startsWith('Pre-work') ? '📝' : '⭐');
        return `
          <div class="file-item" id="nav-${encodeURIComponent(name)}" onclick="loadFile('${name.replace(/'/g, "\\\\'")}')">
            <span>${icon}</span>
            <span style="flex:1;">${cleanName}</span>
            ${qCount ? `<span style="font-size:0.7rem; opacity:0.75; background:rgba(255,255,255,0.08); padding:1px 6px; border-radius:8px; white-space:nowrap;">${qCount} Qs</span>` : ''}
          </div>
        `;
      }).join('');
    }

    function filterFiles() {
      const q = document.getElementById('search').value.toLowerCase();
      const all = Object.keys(answersData);
      const filtered = all.filter(f => f.toLowerCase().includes(q));
      renderFiles(filtered);
    }

    // ==========================================
    // Universal Omni-Search & Live Solver
    // ==========================================

    function setOmniExample(eq) {
      const input = document.getElementById('omniInput');
      input.value = eq;
      handleOmniInput();
    }

    function clearOmniSearch() {
      const input = document.getElementById('omniInput');
      input.value = '';
      document.getElementById('omniClearBtn').style.display = 'none';
      switchMainTab('doc');
    }

    function handleOmniKey(e) {
      if (e.key === 'Enter') handleOmniInput();
    }

    function handleOmniInput() {
      const query = (document.getElementById('omniInput').value || '').trim();
      const clearBtn = document.getElementById('omniClearBtn');
      clearBtn.style.display = query ? 'flex' : 'none';

      if (!query) {
        switchMainTab('doc');
        return;
      }

      switchMainTab('omni');
      executeOmniQuery(query);
    }

    function executeOmniQuery(rawQuery) {
      const resultsView = document.getElementById('omniResultsView');
      resultsView.style.display = 'block';

      // 1. Parse equation syntax
      const parsed = parseEquationSyntax(rawQuery);

      // 2. Execute matching built-in tool
      const toolResult = runToolOnParsed(parsed, rawQuery);

      // 3. Query all questions in the database
      const dbMatches = searchCourseCatalog(rawQuery, parsed ? parsed.type : null);

      let html = '';

      // Render Tool Execution Card
      let graphData = parsed ? buildGraphDataFromParsed(parsed, rawQuery) : null;
      if (!graphData && !toolResult) {
        // Fallback: if the user typed a generic function of x, plot it!
        const compiled = compileMathFunction(rawQuery);
        if (compiled && rawQuery.toLowerCase().includes('x')) {
          graphData = {
            id: `omni_custom_${rawQuery}`,
            type: 'function',
            fn: compiled,
            points: [{ x: 0, y: compiled(0), type: 'point', color: '#a855f7', label: `(0, ${(compiled(0)||0).toFixed(2)})` }],
            curveColor: '#38bdf8',
            label: `f(x) = ${rawQuery}`
          };
        }
      }

      if (toolResult || graphData) {
        html += `
          <div class="omni-section-heading"><span>⚡</span> Automatic Mathematical Solver & Grapher Result</div>
          <div class="omni-tool-card">
            ${toolResult ? `
              <div class="omni-tool-header">
                <span class="omni-tool-title">${toolResult.title}</span>
                <div style="display:flex; gap:8px;">
                  <button class="btn-dyn-toggle" onclick="openInDedicatedGrapher('${encodeURIComponent(rawQuery)}')">
                    📈 Open in Full Grapher
                  </button>
                  <button class="btn-dyn-toggle" onclick="launchSolverWithParams('${toolResult.solverKey}', ${JSON.stringify(toolResult.params || {}).replace(/"/g, '&quot;')})">
                    ↗ Open in Full Solver
                  </button>
                </div>
              </div>
              <div class="out-label">Verified Solution:</div>
              <div class="out-val">${toolResult.outputVal}</div>
              <ul class="out-steps">
                ${(toolResult.steps || []).map(s => `<li>${s}</li>`).join('')}
              </ul>
            ` : `
              <div class="omni-tool-header">
                <span class="omni-tool-title">📈 Function Plotter: ${rawQuery}</span>
                <button class="btn-dyn-toggle" onclick="openInDedicatedGrapher('${encodeURIComponent(rawQuery)}')">
                  📈 Open in Full Grapher
                </button>
              </div>
            `}

            ${graphData ? `
              <div class="graph-card">
                <div class="graph-header">
                  <span class="graph-title">📊 Visual Function & Coordinate Graph (${graphData.label || rawQuery})</span>
                  <div class="graph-controls">
                    <button class="btn-ctrl" onclick="zoomActiveGraph('omniCanvas', 0.8)">− Zoom Out</button>
                    <button class="btn-ctrl" onclick="resetActiveGraph('omniCanvas')">⟲ Reset</button>
                    <button class="btn-ctrl" onclick="zoomActiveGraph('omniCanvas', 1.25)">+ Zoom In</button>
                  </div>
                </div>
                <canvas id="omniCanvas" width="760" height="400" style="width:100%; max-width:760px; height:auto; background:#070d19; border-radius:6px; cursor:crosshair; display:block; margin:0 auto;"></canvas>
              </div>
            ` : ''}
          </div>
        `;

        if (graphData) {
          setTimeout(() => {
            renderUniversalGraph('omniCanvas', graphData);
          }, 30);
        }
      }

      // Render Database Course References
      html += `
        <div class="omni-section-heading">
          <span>📚</span> Course Material References (${dbMatches.length} Matches Found in Database)
        </div>
      `;

      if (dbMatches.length === 0) {
        html += `
          <div class="omni-match-card" style="text-align:center; color:var(--text-muted); padding:30px;">
            No direct homework questions matched "${rawQuery}". Try typing specific coefficients or general topic keywords (e.g. "vertex", "zeros", "asymptote", "circle", "ellipse", "hyperbola", "inequality", "logarithm").
          </div>
        `;
      } else {
        html += dbMatches.map((m, idx) => {
          const qKey = `omni_${idx}`;
          const graphEq = extractGraphableFromQuestion(m.problem, m.answer, (m.equations && m.equations[0]) || '');
          const initialExpr = extractInitialEditableExpr(m.problem, m.answer, graphEq, '');
          const matchCanvasId = `qcanvas-${qKey}`;
          const probHtml = `<strong>Problem:</strong> ${formatMath(m.problem)}`;
          const ansHtml = formatMath(m.answer || '');
          const workHtml = formatMath(m.steps || '');

          originalCardStates[qKey] = {
            problemHtml: probHtml,
            answerHtml: ansHtml,
            workHtml: workHtml,
            graphEq: graphEq || '',
            initialExpr: initialExpr || ''
          };

          const safeAttrExpr = (initialExpr || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

          return `
            <div class="omni-match-card" id="qcard-${qKey}">
              <div class="match-header">
                <span class="match-source">${m.assignment} &nbsp;•&nbsp; ${m.qNum}</span>
                <span class="match-chapter">Chapter ${m.chapter}</span>
              </div>
              <div class="q-problem" id="qprob-${qKey}" contenteditable="true" spellcheck="false" oninput="onProblemTextEdited('${qKey}')" title="Click anywhere in this problem text to edit numbers or equations in real time!">
                ${probHtml}
              </div>
              <div class="inline-editor-bar">
                <span class="inline-editor-label">✏️ Live Edit Equation:</span>
                <input type="text" class="inline-live-input" id="qinput-${qKey}" value="${safeAttrExpr}" placeholder="Edit equation or numbers here to recalculate live..." oninput="updateQuestionCardRealtime('${qKey}')">
                <button class="btn-inline-reset" id="qreset-${qKey}" style="display:none;" onclick="resetQuestionCardRealtime('${qKey}')">↺ Reset Original</button>
              </div>
              <div class="box-answer" id="qanswrap-${qKey}" style="${m.answer ? '' : 'display:none;'}">
                <span class="box-badge badge-ans" id="qansbadge-${qKey}">Verified Answer</span>
                <div class="ans-value" id="qansval-${qKey}">${ansHtml}</div>
              </div>
              ${m.rule ? `
                <div style="font-size:0.84rem; color:#cbd5e1; margin-top:8px;">
                  <strong style="color:#818cf8;">Rule/Method:</strong> ${formatMath(m.rule)}
                </div>
              ` : ''}
              <div class="box-work" id="qworkwrap-${qKey}" style="${m.steps ? '' : 'display:none;'}">
                <span class="box-badge badge-work" id="qworkbadge-${qKey}">Step-by-Step Work</span>
                <div id="qworkval-${qKey}">${workHtml}</div>
              </div>
              <div class="graph-card" id="qgraphwrap-${qKey}" style="margin-top:12px; ${graphEq ? '' : 'display:none;'}">
                <div class="graph-header">
                  <span class="graph-title" id="qgraphtitle-${qKey}">📊 Reference Problem Graph: <code>${graphEq}</code></span>
                  <div class="graph-controls">
                    <button class="btn-ctrl" onclick="zoomActiveGraph('${matchCanvasId}', 0.8)">− Zoom Out</button>
                    <button class="btn-ctrl" onclick="resetActiveGraph('${matchCanvasId}')">⟲ Reset</button>
                    <button class="btn-ctrl" onclick="zoomActiveGraph('${matchCanvasId}', 1.25)">+ Zoom In</button>
                    <button class="btn-ctrl" onclick="openInDedicatedGrapher(encodeURIComponent(document.getElementById('qinput-${qKey}') ? document.getElementById('qinput-${qKey}').value : '${encodeURIComponent(graphEq)}'))">↗ Full Grapher</button>
                  </div>
                </div>
                <canvas id="${matchCanvasId}" class="inline-q-canvas" data-graph-eq="${encodeURIComponent(graphEq)}" width="700" height="320" style="width:100%; max-width:700px; height:auto; background:#070d19; border-radius:6px; cursor:crosshair; display:block; margin:0 auto;"></canvas>
              </div>
              <div style="margin-top:12px; display:flex; gap:8px;">
                <button class="btn-dyn-toggle" onclick="loadMatchedProblemIntoView('${m.assignment}')">
                  📄 Open In Answer Sheet
                </button>
              </div>
            </div>
          `;
        }).join('');
      }

      resultsView.innerHTML = html;
      setTimeout(renderAllInlineGraphs, 40);
    }

    const topicMap = {
      'powers_i': 'complex',
      'complex_mult': 'complex',
      'complex_div': 'complex',
      'synthetic': 'synthetic',
      'quadratic': 'quadratic',
      'quad_vertex': 'quadratic',
      'abs': 'abs',
      'abs_double': 'abs',
      'circle_std': 'circle',
      'circle_gen': 'circle',
      'ellipse': 'ellipse',
      'hyperbola': 'hyperbola',
      'radical': 'radical',
      'system_2x2': 'linear_system',
      'rational': 'rational',
      'rat_ineq': 'rational',
      'polynomial': 'polynomial',
      'poly_ineq': 'polynomial',
      'exp_func': 'exponential',
      'log_func': 'logarithmic'
    };

    function searchCourseCatalog(query, parsedType) {
      const qNorm = normalizeLatexToAscii(query).toLowerCase().replace(/[\$\s`\\{}]/g, '');
      const terms = query.toLowerCase().split(/[\s,]+/).filter(t => t.length > 1);
      const mappedTopic = parsedType ? (topicMap[parsedType] || parsedType) : null;

      const scored = [];
      for (const item of (courseDatabase.catalog || [])) {
        const fullText = (item.problem + ' ' + item.answer + ' ' + item.assignment + ' ' + item.topic + ' ' + (item.equations || []).join(' ')).toLowerCase();
        const fullClean = normalizeLatexToAscii(fullText).toLowerCase().replace(/[\$\s`\\{}]/g, '');

        let score = 0;
        if (qNorm.length >= 3 && fullClean.includes(qNorm)) {
          score += 50;
        }
        if (mappedTopic && (item.topic === mappedTopic || (item.assignment || '').toLowerCase().includes(mappedTopic))) {
          score += 25;
        }
        let matchedTerms = 0;
        for (const t of terms) {
          if (fullText.includes(t)) matchedTerms++;
        }
        if (terms.length > 0 && matchedTerms === terms.length) {
          score += 30;
        } else {
          score += (matchedTerms * 8);
        }

        if (score > 0) {
          scored.push({ item, score });
        }
      }

      scored.sort((a, b) => b.score - a.score);
      return scored.slice(0, 15).map(s => s.item);
    }

    function loadMatchedProblemIntoView(assignmentName) {
      const allFiles = Object.keys(answersData);
      const match = allFiles.find(f => f.includes(assignmentName) || assignmentName.includes(f.replace(' - Answers.md', '')));
      if (match) {
        loadFile(match);
      } else if (allFiles.length > 0) {
        loadFile(allFiles[0]);
      }
    }

    // ==========================================
    // Polynomial Algebra & Sign Chart Helpers
    // ==========================================

    function parsePolyCoeffs(str) {
      str = normalizeLatexToAscii(str || '').replace(/\s+/g, '').replace(/\*/g, '');
      if (!str) return [0];

      str = stripOuterParens(str);

      // Pure number check (e.g. "6", "-12", "-1/2", "5/6")
      if (/^[+-]?\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?$/.test(str)) {
        if (str.includes('/')) {
          const sp = str.split('/');
          return [parseFloat(sp[0]) / parseFloat(sp[1])];
        }
        return [parseFloat(str)];
      }

      // Pre-evaluate parenthesized fractions like (-5/6) or (1/2) into decimal strings
      str = str.replace(/\(([+-]?\d+(?:\.\d+)?)\/(\d+(?:\.\d+)?)\)/g, (m, n, d) => {
        const v = parseFloat(n) / parseFloat(d);
        return (v >= 0 ? '+' : '') + v.toString();
      });

      const coeffMap = {};
      let cleanStr = str;
      if (!cleanStr.startsWith('+') && !cleanStr.startsWith('-')) {
        cleanStr = '+' + cleanStr;
      }

      const terms = cleanStr.match(/[+-][^+-]*/g) || [];
      let maxDeg = 0;
      let matchedAny = false;

      for (let t of terms) {
        t = t.trim();
        if (!t) continue;
        const m = t.match(/^([+-])(\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?|\d*\.?\d*)?(?:([a-zA-Z])(?:\^\(?(\d+)\)?)?)?$/);
        if (!m) continue;
        const sign = m[1] === '-' ? -1 : 1;
        const numPart = m[2];
        const hasVar = !!m[3];
        const pwr = m[4];
        if (!numPart && !hasVar) continue;

        let numVal = 1;
        if (numPart) {
          if (numPart.includes('/')) {
            const sp = numPart.split('/');
            numVal = parseFloat(sp[0]) / parseFloat(sp[1]);
          } else {
            numVal = parseFloat(numPart);
          }
        }
        const cf = sign * numVal;
        const p = hasVar ? (pwr ? parseInt(pwr, 10) : 1) : 0;

        coeffMap[p] = (coeffMap[p] || 0) + cf;
        if (p > maxDeg) maxDeg = p;
        matchedAny = true;
      }

      if (!matchedAny) return [0];
      const res = [];
      for (let d = maxDeg; d >= 0; d--) {
        res.push(coeffMap[d] || 0);
      }
      return res;
    }

    function multiplyPolysJS(p1, p2) {
      const res = new Array(p1.length + p2.length - 1).fill(0);
      for (let i = 0; i < p1.length; i++) {
        for (let j = 0; j < p2.length; j++) {
          res[i + j] += p1[i] * p2[j];
        }
      }
      return res;
    }

    function subPolysJS(p1, p2) {
      const len = Math.max(p1.length, p2.length);
      const res = new Array(len).fill(0);
      for (let i = 0; i < p1.length; i++) res[len - p1.length + i] += p1[i];
      for (let j = 0; j < p2.length; j++) res[len - p2.length + j] -= p2[j];
      while (res.length > 1 && Math.abs(res[0]) < 1e-9) res.shift();
      return res;
    }

    function parseAnyPolyCoeffs(rawStr) {
      let s = normalizeLatexToAscii(rawStr || '').replace(/\s+/g, '');
      if (!s) return [0];
      s = stripOuterParens(s);

      // Check if factored form like -2(x-1)^2(x+2), 9*(x+3)^3*(x-3), (-1/2)*(x+2)...
      if (s.includes('(')) {
        let idx = 0;
        let acc = [1];
        let ok = true;
        let matchedFactor = false;

        const firstParen = s.indexOf('(');
        if (firstParen > 0) {
          let prefix = s.slice(0, firstParen);
          if (prefix.endsWith('*')) prefix = prefix.slice(0, -1);
          if (prefix === '-') acc = [-1];
          else if (prefix === '+') acc = [1];
          else {
            const pCfs = parsePolyCoeffs(prefix);
            if (pCfs && (pCfs.length > 1 || pCfs[0] !== 0)) acc = pCfs;
            else ok = false;
          }
          idx = firstParen;
        } else if (s.startsWith('-(')) {
          acc = [-1];
          idx = 1;
        } else if (s.startsWith('+(')) {
          acc = [1];
          idx = 1;
        }

        if (ok) {
          while (idx < s.length) {
            if (s[idx] === '*') { idx++; continue; }
            if (s[idx] !== '(') { ok = false; break; }
            let depth = 0;
            let closeIdx = -1;
            for (let i = idx; i < s.length; i++) {
              if (s[i] === '(') depth++;
              else if (s[i] === ')') {
                depth--;
                if (depth === 0) { closeIdx = i; break; }
              }
            }
            if (closeIdx === -1) { ok = false; break; }
            const inside = s.slice(idx + 1, closeIdx);
            const factorPoly = parsePolyCoeffs(inside);
            idx = closeIdx + 1;
            let exp = 1;
            if (idx < s.length && s[idx] === '^') {
              idx++;
              const expMatch = s.slice(idx).match(/^(\d+)/);
              if (expMatch) {
                exp = parseInt(expMatch[1], 10);
                idx += expMatch[1].length;
              }
            }
            for (let e = 0; e < exp; e++) {
              acc = multiplyPolysJS(acc, factorPoly);
            }
            matchedFactor = true;
          }
          if (ok && matchedFactor) return acc;
        }
      }

      return parsePolyCoeffs(s);
    }

    function stripOuterParens(str) {
      let s = (str || '').trim();
      while (s.startsWith('(') && s.endsWith(')')) {
        let depth = 0;
        let balancedOuter = true;
        for (let i = 0; i < s.length - 1; i++) {
          if (s[i] === '(') depth++;
          else if (s[i] === ')') depth--;
          if (depth === 0) { balancedOuter = false; break; }
        }
        if (balancedOuter) s = s.slice(1, -1).trim();
        else break;
      }
      return s;
    }

    // ===== Engine v4 hardening helpers: constants, powers, linear forms =====
    function parseConstValue(t) {
      // __ENGINE_V4_4__: strip ALL balanced outer paren pairs first (any
      // content), then accept e, e^k, b^k numeric powers, ints and A/B.
      t = String(t == null ? '' : t).replace(/\s+/g, '');
      if (!t) return null;
      while (t.startsWith('(') && t.endsWith(')')) {
        var d = 0, bal = true;
        for (var i = 0; i < t.length; i++) {
          if (t[i] === '(') d++;
          else if (t[i] === ')') { d--; if (d === 0 && i < t.length - 1) { bal = false; break; } }
        }
        if (!bal) break;
        t = t.slice(1, -1).replace(/^\s+|\s+$/g, '');
        if (!t) return null;
      }
      // __ENGINE_V4_4b__: layered numeric fractions like (8)/(125) inside
      // one paren pair are NOT a single wrapped token — strip all parens
      // when only numeric/rational content remains.
      if (/^[()+*/\d.\-]+$/.test(t)) t = t.replace(/[()]/g, '');
      if (/^e$/i.test(t)) return Math.E;
      var em = t.match(/^e\^\(?([+-]?\d+(?:\.\d+)?)\)?$/i);
      if (em) return Math.pow(Math.E, parseFloat(em[1]));
      // numeric power b^k with optional parens: 10^(-7), 10^-7, (10)^3
      var pm = t.match(/^([+-]?\d+(?:\.\d+)?)\^\(?([+-]?\d+(?:\.\d+)?)\)?$/);
      if (pm) { var bb = parseFloat(pm[1]), kk = parseFloat(pm[2]); return Math.pow(bb, kk); }
      if (/^[+-]?\d+(?:\.\d+)?$/.test(t)) return parseFloat(t);
      var rf = t.match(/^([+-]?\d+(?:\.\d+)?)\/([+-]?\d+(?:\.\d+)?)$/);
      if (rf && parseFloat(rf[2]) !== 0) return parseFloat(rf[1]) / parseFloat(rf[2]);
      return null;
    }

    function parseLnOfBase(t) {
      // __ENGINE_V4_3__: unwrap ALL balanced outer parens, and accept
      // constant quotients like (1)/(e) or (1)/(e^3) via ln(A/B)=ln A - ln B.
      t = String(t || '').trim();
      while (t.startsWith('(') && t.endsWith(')')) {
        var d = 0, bal = true;
        for (var i2 = 0; i2 < t.length; i2++) {
          if (t[i2] === '(') d++;
          else if (t[i2] === ')') { d--; if (d === 0 && i2 < t.length - 1) { bal = false; break; } }
        }
        if (!bal) break;
        t = t.slice(1, -1).trim();
      }
      var sm = t.match(/^sqrt\(\s*(\d+(?:\.\d+)?)\s*\)$/i);
      if (sm) return 0.5 * Math.log(parseFloat(sm[1]));
      var v = parseConstValue(t);
      if (v !== null && v > 0 && Math.abs(v - 1) > 1e-12) return Math.log(v);
      // quotient of constants: (A)/(B) at top level (parens already stripped)
      var sl = -1, dep = 0;
      for (var j = 0; j < t.length; j++) {
        if (t[j] === '(') dep++;
        else if (t[j] === ')') dep--;
        else if (t[j] === '/' && dep === 0) { sl = j; break; }
      }
      if (sl > 0) {
        var A2 = parseConstValue(t.slice(0, sl).trim());
        var B2 = parseConstValue(t.slice(sl + 1).trim());
        if (A2 !== null && B2 !== null && A2 > 0 && B2 > 0) return Math.log(A2) - Math.log(B2);
      }
      return null;
    }

    // split "base ^ exponent" at the FIRST ^ that sits outside any parens
    function splitPow(side) {
      side = String(side || '').trim();
      var depth = 0;
      for (var i = 0; i < side.length; i++) {
        var ch = side[i];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if (ch === '^' && depth === 0) return [side.slice(0, i).trim(), side.slice(i + 1).trim()];
      }
      return null;
    }

    // split an expression into top-level +/- terms (signs stay attached).
    // __ENGINE_V4_3__: operators may be preceded by whitespace — look back
    // past spaces ("4x^2 - 32y" must split, not just "4x^2-32y").
    function splitTopLevelOps(str) {
      var parts = [];
      var depth = 0, start = 0;
      for (var i = 0; i < str.length; i++) {
        var ch = str[i];
        if (ch === '(') depth++;
        else if (ch === ')') depth--;
        else if ((ch === '+' || ch === '-') && depth === 0 && i > 0 &&
                 // __ENGINE_V4_5__: any variable letter may precede an operator
                 /[0-9a-z)\]]\s*$/i.test(str.slice(0, i)) && i + 1 < str.length &&
                 !/[\^]\s*$/.test(str.slice(0, i))) {
          parts.push(str.slice(start, i).trim());
          start = i;
        }
      }
      parts.push(str.slice(start).trim());
      return parts.filter(Boolean);
    }

    // ===== __ENGINE_V4_2__: log expression arithmetic (Ch 4.3-4.4) =====
    // Parse "c1 log_b(A1) +/- c2 log_b2(A2) [= RHS]" into evaluated or
    // structurally-expanded form. Returns null when not all-log shaped.
    function parseLogExprShape(str) {
      var t = String(str || '').replace(/\s+/g, ' ').trim();
      if (!t) return null;
      var sides = t.split('=');
      if (sides.length > 2) return null;
      var lhs = sides[0].trim(), rhs = sides.length === 2 ? sides[1].trim() : null;
      function parseSide(side) {
        var parts = splitTopLevelOps(side);
        var terms = [], ok = true, anyLog = false;
        for (var i2 = 0; i2 < parts.length; i2++) {
          var raw = parts[i2];
          var sign = 1, s2 = raw.trim();
          if (s2.startsWith('-')) { sign = -1; s2 = s2.slice(1).trim(); }
          else if (s2.startsWith('+')) s2 = s2.slice(1).trim();
          var cm = s2.match(/^(\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
          var coef = sign, body = s2;
          if (cm) { coef = sign * parseFloat(cm[1]); body = cm[2].trim(); }
          // __ENGINE_V4_3__: "5log_4(x)" — implicit coefficient, no '*'
          else {
            // __ENGINE_V4_4__: \b fails before '_' — accept [_ ( after log
            var cm2 = s2.match(/^(\d+(?:\.\d+)?)\s*((?:ln|log)[_(].*)$/i)
                    || s2.match(/^(\d+(?:\.\d+)?)\s*((?:ln|log)\s.*)$/i);
            if (cm2) { coef = sign * parseFloat(cm2[1]); body = cm2[2].trim(); }
          }
          var lm = body.match(/^(?:ln|log)_?\(?\s*(?:([0-9]+(?:\.[0-9]+)?))?\s*\)?\s*(?:\(\s*(.+?)\s*\)|([A-Za-z0-9][^()]*))$/i)
                 || body.match(/^(?:ln|log)\s*(?:\(\s*(.+?)\s*\)|([A-Za-z0-9][^()]*))$/i);
          var vm = null;
          if (!lm) vm = body.match(/^(\d+(?:\.\d+)?)$/);
          if (lm) {
            anyLog = true;
            var baseS = lm[1] !== undefined ? lm[1] : null;
            var argS = (lm[2] !== undefined ? lm[2] : lm[3]).trim();
            var baseV = baseS !== null ? parseFloat(baseS) : 10;
            var argConst = parseConstValue(argS);
            var argLin = argConst === null ? polyToLin(parsePolyCoeffs(argS.replace(/[()]/g, ''))) : null;
            terms.push({ kind: 'log', coef: coef, base: baseV, argRaw: argS,
                         argConst: argConst, argLin: argLin });
          } else if (vm) {
            terms.push({ kind: 'const', v: coef * parseFloat(vm[1]) });
          } else { ok = false; break; }
        }
        if (!ok || !terms.length) return null;
        return { terms: terms, anyLog: anyLog };
      }
      var L = parseSide(lhs);
      var Rr = rhs !== null ? parseSide(rhs) : null;
      if (!L || !L.anyLog || (rhs !== null && !Rr)) return null;
      return { lhs: L, rhs: Rr, hasRhs: rhs !== null };
    }

    function Cnum2str(craw, rhsIsLog) {
      return rhsIsLog ? String(craw).trim() : String(parseConstValue(String(craw)));
    }
    function polyToLin(coeffs) {
      if (!coeffs || coeffs.length > 2) return null;
      var m = coeffs[0], b = coeffs.length === 2 ? coeffs[1] : 0;
      if (!isFinite(m) || !isFinite(b)) return null;
      return { m: m, b: b };
    }
    function linMul(k, lin) { return { m: k * lin.m, b: k * lin.b }; }
    function linSub(a, b) { return { m: a.m - b.m, b: a.b - b.b }; }

    function rationalizeVal(x) {
      if (!isFinite(x)) return String(x);
      for (var d = 1; d <= 64; d++) {
        var n = Math.round(x * d);
        if (Math.abs(x - n / d) < 1e-9) return fracStr(n, d);
      }
      return Number(x.toFixed(4)) + '';
    }

    // classify one +/- term as coeff*b^linearExp ("3 * 3^(x-2)") or constant
    function classifyPowTerm(t) {
      // __ENGINE_V4_2__: leading '-' signs the WHOLE term (coef included)
      t = String(t || '').trim();
      var sign = 1;
      if (t.startsWith('-')) { sign = -1; t = t.slice(1).trim(); }
      else if (t.startsWith('+')) { t = t.slice(1).trim(); }
      var coef = sign, rest = t;
      var cm = t.match(/^(\d+(?:\.\d+)?)\s*\*\s*(.+)$/);
      if (cm) { coef = sign * parseFloat(cm[1]); rest = cm[2].trim(); }
      var sp = splitPow(rest);
      if (sp) {
        var lnBase = parseLnOfBase(sp[0]);
        var lin = polyToLin(parsePolyCoeffs(sp[1]));
        if (lnBase !== null && lin) return { kind: 'pow', coef: coef, lnBase: lnBase, lin: lin };
      }
      var v = parseConstValue(t);
      if (v !== null) return { kind: 'const', v: sign * v };
      return null;
    }

    // Circle from grouped/general polynomial form (Ch 2.2 Q15/Q21):
    // (x^2 + 12x) + (y^2 - 14y) = 5   or   4x^2 + 4x + 4y^2 - 32y - 79 = 0
    function parseConicTermsSide(side) {
      var co = { x2: 0, y2: 0, x: 0, y: 0, c: 0 };
      var parts = splitTopLevelOps(side);
      for (var i = 0; i < parts.length; i++) {
        var raw = parts[i];
        var sign = 1, t = raw;
        if (t.startsWith('-')) { sign = -1; t = t.slice(1).trim(); }
        else if (t.startsWith('+')) { t = t.slice(1).trim(); }
        var m;
        if ((m = t.match(/^(?:(\d*\.?\d+)?)x\^2$/i))) co.x2 += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)y\^2$/i))) co.y2 += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)x$/i))) co.x += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(?:(\d*\.?\d+)?)y$/i))) co.y += sign * (m[1] ? parseFloat(m[1]) : 1);
        else if ((m = t.match(/^(\d*\.?\d+)$/))) co.c += sign * parseFloat(m[1]);
        else return null;
      }
      return co;
    }
    function parseConicGeneralStd(raw) {
      var t = String(raw).replace(/\s+/g, '').replace(/\(([^()]+)\)/g, '$1');
      var sides = t.split('=');
      if (sides.length !== 2) return null;
      var L = parseConicTermsSide(sides[0]);
      var R = parseConicTermsSide(sides[1]);
      if (!L || !R) return null;
      var A = L.x2 - R.x2, C = L.y2 - R.y2;
      var D = L.x - R.x, E = L.y - R.y, F = L.c - R.c;
      if (Math.abs(A) < 1e-12 || Math.abs(A - C) > 1e-9) return null;  // circle only
      return { type: 'circle_gen', a: 1, b: D / A, c: E / A, d: F / A };
    }
    // ===== __ENGINE_V4__ =====

    function formatEndpoint(val) {
      if (val === -Infinity) return '-∞';
      if (val === Infinity) return '∞';
      if (Math.abs(Math.round(val) - val) < 1e-4) return '' + Math.round(val);
      for (let d = 2; d <= 64; d++) {
        let n = Math.round(val * d);
        if (Math.abs(val - n / d) < 1e-3) return fracStr(n, d);
      }
      return Number(val.toFixed(3)) + '';
    }

    function solveSignChartInequalityJS(numCoeffs, denCoeffs, op) {
      const evalP = (c, x) => c.reduce((acc, v) => acc * x + v, 0);
      const numRoots = Array.from(new Set(findRationalRootsJS(numCoeffs).map(r => parseFloat(r.toFixed(4)))));
      const denRoots = Array.from(new Set(findRationalRootsJS(denCoeffs).map(r => parseFloat(r.toFixed(4)))));

      const allCrits = Array.from(new Set([...numRoots, ...denRoots])).sort((a, b) => a - b);
      const isStrict = (op === '<' || op === '>');
      const wantPos = (op === '>' || op === '>=');

      const intervals = [];
      const chartRows = [];
      const bounds = [-Infinity, ...allCrits, Infinity];

      for (let i = 0; i < bounds.length - 1; i++) {
        const left = bounds[i];
        const right = bounds[i + 1];
        let testX = 0;
        if (left === -Infinity && right === Infinity) testX = 0;
        else if (left === -Infinity) testX = right - 2;
        else if (right === Infinity) testX = left + 2;
        else testX = (left + right) / 2;

        const val = evalP(numCoeffs, testX) / evalP(denCoeffs, testX);
        const isPos = val > 0;
        const satisfies = wantPos ? isPos : !isPos;

        const leftInc = (left !== -Infinity) && !isStrict && !denRoots.some(dr => Math.abs(dr - left) < 1e-3);
        const rightInc = (right !== Infinity) && !isStrict && !denRoots.some(dr => Math.abs(dr - right) < 1e-3);

        const ivLabel = `${left === -Infinity ? '(-∞' : (leftInc ? '[' + formatEndpoint(left) : '(' + formatEndpoint(left))}, ${right === Infinity ? '∞)' : (rightInc ? formatEndpoint(right) + ']' : formatEndpoint(right) + ')')}`;
        chartRows.push({
          interval: ivLabel,
          testX: testX.toFixed(2),
          val: val.toFixed(2),
          sign: isPos ? '+ (Positive)' : '− (Negative)',
          satisfies
        });

        if (satisfies) {
          if (intervals.length > 0 && intervals[intervals.length - 1].to === left && intervals[intervals.length - 1].inclusiveTo && leftInc) {
            intervals[intervals.length - 1].to = right;
            intervals[intervals.length - 1].inclusiveTo = rightInc;
          } else {
            intervals.push({ from: left, to: right, inclusiveFrom: leftInc, inclusiveTo: rightInc });
          }
        }
      }

      const intervalStr = intervals.length === 0 ? '∅ (No Solution)' : intervals.map(iv => {
        const l = iv.from === -Infinity ? '(-∞' : `${iv.inclusiveFrom ? '[' : '('}${formatEndpoint(iv.from)}`;
        const r = iv.to === Infinity ? '∞)' : `${formatEndpoint(iv.to)}${iv.inclusiveTo ? ']' : ')'}`;
        return `${l}, ${r}`;
      }).join(' ∪ ');

      const isolatedPoints = [];
      if (!isStrict) {
        numRoots.forEach(nr => {
          const inInterval = intervals.some(iv => {
            const geLeft = iv.inclusiveFrom ? (nr >= iv.from - 1e-4) : (nr > iv.from + 1e-4);
            const leRight = iv.inclusiveTo ? (nr <= iv.to + 1e-4) : (nr < iv.to - 1e-4);
            return geLeft && leRight;
          });
          if (!inInterval && !denRoots.some(dr => Math.abs(dr - nr) < 1e-4)) {
            isolatedPoints.push(nr);
          }
        });
      }

      return { numRoots, denRoots, allCrits, chartRows, intervals, intervalStr, isolatedPoints };
    }

    // ==========================================
    // Parser for Universal Equation Input
    // ==========================================

    function parseEquationSyntax(rawInput) {
      let s = normalizeLatexToAscii(rawInput);
      if (!s) return null;

      // 0a. Two Coordinate Points (Ch 1.1, 2.3, 2.4): (x1, y1), (x2, y2)
      const twoPtsMatch = s.match(/^\(\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*\)\s*[,;]\s*\(\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*\)$/);
      if (twoPtsMatch) {
        const x1 = parseFloat(twoPtsMatch[1]), y1 = parseFloat(twoPtsMatch[2]);
        const x2 = parseFloat(twoPtsMatch[3]), y2 = parseFloat(twoPtsMatch[4]);
        const dx = x2 - x1, dy = y2 - y1;
        const distSq = dx * dx + dy * dy;
        const dist = Math.sqrt(distSq);
        const mx = 0.5 * (x1 + x2), my = 0.5 * (y1 + y2);
        const m = Math.abs(dx) > 1e-9 ? dy / dx : Infinity;
        const b = isFinite(m) ? (y1 - m * x1) : NaN;
        return { type: 'two_points', x1, y1, x2, y2, dx, dy, distSq, dist, mx, my, m, b };
      }

      // 0a2. Multi-Point Polynomial from 3+ Points (Ch 3.2–3.4): e.g. (-5, 0), (-3, 0), (-1, 0), (0, 2) or A(-3,0), B(-1,0), C(-5,0), D(0,2)
      if (s.includes('(') && s.includes(')') && !s.includes('=')) {
        const ptMatches = Array.from(s.matchAll(/([A-Za-z])?\s*\(\s*([+-]?\d+(?:\.\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?)\s*\)/g));
        if (ptMatches.length >= 3) {
          const pts = ptMatches.map(m => ({ name: m[1] || '', x: parseFloat(m[2]), y: parseFloat(m[3]) }));
          const zeros = pts.filter(p => Math.abs(p.y) < 1e-9).sort((a, b) => a.x - b.x);
          const nonZeros = pts.filter(p => Math.abs(p.y) >= 1e-9);
          if (zeros.length >= 2 && nonZeros.length >= 1) {
            const anchor = nonZeros[0];
            let prod = 1;
            zeros.forEach(z => { prod *= (anchor.x - z.x); });
            if (Math.abs(prod) > 1e-9) {
              const aVal = anchor.y / prod;
              const aFrac = fracStr(anchor.y * 1000, prod * 1000);
              const factorsStr = zeros.map(z => `(x ${z.x < 0 ? '+ ' + Math.abs(z.x) : '- ' + z.x})`).join('');
              const factoredStr = `${aFrac === '1' ? '' : (aFrac === '-1' ? '-' : aFrac)}${factorsStr}`;
              let basePoly = [1];
              zeros.forEach(z => { basePoly = multiplyPolysJS(basePoly, [1, -z.x]); });
              const evalFn = (x) => aVal * zeros.reduce((acc, z) => acc * (x - z.x), 1);
              return { type: 'poly_points', pts, zeros, anchor, prod, aVal, aFrac, factorsStr, factoredStr, basePoly, evalFn };
            }
          }
        }
      }

      // 0b. 3x3 Linear Systems of Equations (Ch 9.2): 3 equations with x, y, z
      if ((s.includes(',') || s.includes(';')) && s.includes('x') && s.includes('y') && s.includes('z') && s.includes('=')) {
        const parts3 = s.split(/[,;]/).map(p => p.trim()).filter(Boolean);
        if (parts3.length === 3) {
          const eval3D = (eqStr) => {
            const sides = eqStr.split('=');
            if (sides.length !== 2) return null;
            const prep = (expr) => expr
              .replace(/(\d)([xyz\(])/gi, '$1*$2')
              .replace(/([xyz])(\d)/gi, '$1*$2')
              .replace(/([xyz])\(/gi, '$1*(')
              .replace(/\^/g, '**');
            try {
              const fn = new Function('x', 'y', 'z', `return (${prep(sides[0])}) - (${prep(sides[1])});`);
              if (isNaN(fn(1, 1, 1))) return null;
              return fn;
            } catch (e) { return null; }
          };
          const f1 = eval3D(parts3[0]), f2 = eval3D(parts3[1]), f3 = eval3D(parts3[2]);
          if (f1 && f2 && f3) {
            const getCoeffs = (fn) => {
              const d = -fn(0, 0, 0);
              return { a: fn(1, 0, 0) + d, b: fn(0, 1, 0) + d, c: fn(0, 0, 1) + d, d };
            };
            const r1 = getCoeffs(f1), r2 = getCoeffs(f2), r3 = getCoeffs(f3);
            const det3 = (m) =>
              m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
              m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
              m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
            const D = det3([[r1.a, r1.b, r1.c], [r2.a, r2.b, r2.c], [r3.a, r3.b, r3.c]]);
            const Dx = det3([[r1.d, r1.b, r1.c], [r2.d, r2.b, r2.c], [r3.d, r3.b, r3.c]]);
            const Dy = det3([[r1.a, r1.d, r1.c], [r2.a, r2.d, r2.c], [r3.a, r3.d, r3.c]]);
            const Dz = det3([[r1.a, r1.b, r1.d], [r2.a, r2.b, r2.d], [r3.a, r3.b, r3.d]]);
            let solStr = '';
            if (Math.abs(D) > 1e-9) {
              solStr = `(${Number((Dx / D).toFixed(3))}, ${Number((Dy / D).toFixed(3))}, ${Number((Dz / D).toFixed(3))})`;
            } else {
              solStr = (Math.abs(Dx) < 1e-9 && Math.abs(Dy) < 1e-9 && Math.abs(Dz) < 1e-9)
                ? 'Infinitely Many Solutions (Dependent System)'
                : '∅ (Inconsistent System — No Solution)';
            }
            return { type: 'system_3x3', parts: parts3, r1, r2, r3, D, Dx, Dy, Dz, solStr };
          }
        }
      }

      // 0c. Semicolon or Comma-separated Polynomial Division / Remainder / Factor Theorem: P(x); x - c OR P(x); k = c (either order)
      if ((s.includes(';') || (s.includes(',') && !s.includes('('))) && s.includes('x') && !s.includes('y')) {
        const parts = s.split(/[;,]/).map(p => p.trim()).filter(Boolean);
        if (parts.length === 2) {
          const checkCandidate = (candPoly, candC) => {
            const pClean = candPoly.replace(/^(?:[fghpqr]\(x\)|y)\s*=\s*/i, '').trim();
            const pCfs = parseAnyPolyCoeffs(pClean);
            if (pCfs.length >= 3) {
              const kEq = candC.match(/^(?:k|c|x)\s*=\s*([+-]?\d+(?:\.\d+)?)$/i);
              const numOnly = candC.match(/^([+-]?\d+(?:\.\d+)?)$/);
              const binom = parsePolyCoeffs(candC);
              let val = NaN;
              if (kEq) val = parseFloat(kEq[1]);
              else if (numOnly) val = parseFloat(numOnly[1]);
              else if (binom.length === 2 && Math.abs(binom[0] - 1) < 1e-9) val = -binom[1];
              if (!isNaN(val)) return { poly: pClean, c: val, numCoeffs: pCfs };
            }
            return null;
          };

          const res1 = checkCandidate(parts[0], parts[1]);
          const res2 = res1 ? null : checkCandidate(parts[1], parts[0]);
          const chosen = res1 || res2;
          if (chosen) {
            return {
              type: 'synthetic',
              poly: chosen.poly,
              c: chosen.c,
              numCoeffs: chosen.numCoeffs,
              denCoeffs: [1, -chosen.c]
            };
          }
        }
      }

      // 1. 2x2 Systems of Equations (Ch 9.1 & 9.5): comma or semicolon separated with x and y
      if ((s.includes(',') || s.includes(';')) && s.includes('x') && s.includes('y') && s.includes('=')) {
        const parts = s.split(/[,;]/).map(p => p.trim()).filter(Boolean);
        if (parts.length === 2) {
          const eval2D = (eqStr) => {
            const sides = eqStr.split('=');
            if (sides.length !== 2) return null;
            const prep = (expr) => expr
              .replace(/(\d)([xy\(])/gi, '$1*$2')
              .replace(/([xy])(\d)/gi, '$1*$2')
              .replace(/([xy])\(/gi, '$1*(')
              .replace(/\^/g, '**');
            try {
              const fn = new Function('x', 'y', `return (${prep(sides[0])}) - (${prep(sides[1])});`);
              if (isNaN(fn(1, 1))) return null;
              return fn;
            } catch (e) { return null; }
          };
          const f1 = eval2D(parts[0]);
          const f2 = eval2D(parts[1]);
          if (f1 && f2) {
            const c1 = -f1(0, 0), a1 = f1(1, 0) - f1(0, 0), b1 = f1(0, 1) - f1(0, 0);
            const c2 = -f2(0, 0), a2 = f2(1, 0) - f2(0, 0), b2 = f2(0, 1) - f2(0, 0);
            const isLin1 = Math.abs(f1(2, 3) - (2 * a1 + 3 * b1 - c1)) < 1e-6 && Math.abs(f1(-2, 1) - (-2 * a1 + b1 - c1)) < 1e-6;
            const isLin2 = Math.abs(f2(2, 3) - (2 * a2 + 3 * b2 - c2)) < 1e-6 && Math.abs(f2(-2, 1) - (-2 * a2 + b2 - c2)) < 1e-6;
            if (isLin1 && isLin2) {
              const det = a1 * b2 - a2 * b1;
              const pts = [];
              let solStr = '';
              if (Math.abs(det) > 1e-9) {
                const sx = (c1 * b2 - c2 * b1) / det;
                const sy = (a1 * c2 - a2 * c1) / det;
                pts.push({ x: sx, y: sy, type: 'vertex', color: '#34d399', label: `(${Number(sx.toFixed(2))}, ${Number(sy.toFixed(2))})` });
                solStr = `(${Number(sx.toFixed(2))}, ${Number(sy.toFixed(2))})`;
              } else {
                solStr = (Math.abs(a1 * c2 - a2 * c1) < 1e-9) ? 'Infinitely Many Solutions (Dependent)' : 'No Solution (Inconsistent Parallel Lines)';
              }
              const fn1 = Math.abs(b1) > 1e-9 ? (x) => (c1 - a1 * x) / b1 : null;
              const fn2 = Math.abs(b2) > 1e-9 ? (x) => (c2 - a2 * x) / b2 : null;
              return {
                type: 'system_2x2',
                isLinear: true,
                eq1: parts[0], eq2: parts[1],
                a1, b1, c1, a2, b2, c2, det, solStr,
                graphData: {
                  id: `sys_${a1}_${b1}_${c1}_${a2}_${b2}_${c2}`,
                  type: 'function',
                  fn: fn1,
                  fn2: fn2,
                  points: pts,
                  curveColor: '#38bdf8',
                  curve2Color: '#10b981',
                  label: `System: ${parts[0]} and ${parts[1]}`
                }
              };
            } else {
              // Nonlinear system (Ch 9.5)
              const toExplicitOrConic = (eqStr, fn2d) => {
                // Check if linear in y: fn2d(x, y) = g(x) + b*y
                const bY1 = fn2d(1, 1) - fn2d(1, 0);
                const bY2 = fn2d(1, 2) - fn2d(1, 1);
                const bY3 = fn2d(2, 1) - fn2d(2, 0);
                if (Math.abs(bY1 - bY2) < 1e-6 && Math.abs(bY1 - bY3) < 1e-6 && Math.abs(bY1) > 1e-6) {
                  return { kind: 'fn', fn: (x) => -fn2d(x, 0) / bY1 };
                }
                const subParsed = parseEquationSyntax(eqStr);
                if (subParsed) {
                  if (subParsed.type === 'circle_std') return { kind: 'circle', circle: { h: subParsed.h, k: subParsed.k, r: subParsed.r } };
                  if (subParsed.type === 'ellipse') return { kind: 'ellipse', ellipse: { h: subParsed.h, k: subParsed.k, rx: subParsed.rx, ry: subParsed.ry } };
                  if (subParsed.type === 'hyperbola') return { kind: 'hyperbola', hyperbola: { h: subParsed.h, k: subParsed.k, a: subParsed.a, b: subParsed.b, transverse: subParsed.transverse } };
                }
                return null;
              };
              const p1 = toExplicitOrConic(parts[0], f1);
              const p2 = toExplicitOrConic(parts[1], f2);
              if (p1 || p2) {
                const gData = {
                  id: `nlsys_${parts[0]}_${parts[1]}`,
                  type: 'function',
                  points: [],
                  curveColor: '#38bdf8',
                  curve2Color: '#10b981',
                  label: `Nonlinear System: ${parts[0]}; ${parts[1]}`
                };
                if (p1 && p1.kind === 'fn') gData.fn = p1.fn;
                if (p2 && p2.kind === 'fn') { if (!gData.fn) gData.fn = p2.fn; else gData.fn2 = p2.fn; }
                [p1, p2].forEach(p => {
                  if (!p) return;
                  if (p.kind === 'circle') gData.circle = p.circle;
                  if (p.kind === 'ellipse') gData.ellipse = p.ellipse;
                  if (p.kind === 'hyperbola') gData.hyperbola = p.hyperbola;
                });
                // Find real intersections if at least one is explicit y = fn(x)
                const explicitFn = (p1 && p1.kind === 'fn') ? p1.fn : ((p2 && p2.kind === 'fn') ? p2.fn : null);
                const other2D = (p1 && p1.kind === 'fn') ? f2 : f1;
                if (explicitFn && other2D) {
                  const diff = (x) => other2D(x, explicitFn(x));
                  for (let x = -15; x <= 15; x += 0.25) {
                    const yA = diff(x), yB = diff(x + 0.25);
                    if (Math.abs(yA) < 1e-7) {
                      const py = explicitFn(x);
                      gData.points.push({ x: Number(x.toFixed(2)), y: Number(py.toFixed(2)), type: 'vertex', color: '#34d399', label: `(${Number(x.toFixed(2))}, ${Number(py.toFixed(2))})` });
                    } else if (yA * yB < 0) {
                      let lo = x, hi = x + 0.25;
                      for (let it = 0; it < 25; it++) {
                        const mid = 0.5 * (lo + hi);
                        if (diff(lo) * diff(mid) <= 0) hi = mid; else lo = mid;
                      }
                      const rx = 0.5 * (lo + hi), ry = explicitFn(rx);
                      gData.points.push({ x: Number(rx.toFixed(2)), y: Number(ry.toFixed(2)), type: 'vertex', color: '#34d399', label: `(${Number(rx.toFixed(2)), Number(ry.toFixed(2))})` });
                    }
                  }
                } else {
                  // Check if both equations are linear in x^2 and y^2: A1*x^2 + B1*y^2 = C1
                  const isSq1 = Math.abs(f1(2, 3) - (4 * a1 + 9 * b1 - c1)) < 1e-5 && Math.abs(f1(-2, -3) - (4 * a1 + 9 * b1 - c1)) < 1e-5;
                  const isSq2 = Math.abs(f2(2, 3) - (4 * a2 + 9 * b2 - c2)) < 1e-5 && Math.abs(f2(-2, -3) - (4 * a2 + 9 * b2 - c2)) < 1e-5;
                  if (isSq1 && isSq2) {
                    const detSq = a1 * b2 - a2 * b1;
                    if (Math.abs(detSq) > 1e-9) {
                      const xSq = (c1 * b2 - c2 * b1) / detSq;
                      const ySq = (a1 * c2 - a2 * c1) / detSq;
                      if (xSq >= -1e-7 && ySq >= -1e-7) {
                        const rx = Math.sqrt(Math.max(0, xSq));
                        const ry = Math.sqrt(Math.max(0, ySq));
                        const xs = rx > 1e-6 ? [rx, -rx] : [0];
                        const ys = ry > 1e-6 ? [ry, -ry] : [0];
                        xs.forEach(vx => ys.forEach(vy => {
                          gData.points.push({
                            x: Number(vx.toFixed(2)),
                            y: Number(vy.toFixed(2)),
                            type: 'vertex',
                            color: '#34d399',
                            label: `(${Number(vx.toFixed(2))}, ${Number(vy.toFixed(2))})`
                          });
                        }));
                      }
                    }
                  }
                }
                const solStr = gData.points.length > 0 ? gData.points.map(pt => pt.label).join(', ') : 'See algebraic solution';
                return {
                  type: 'system_2x2',
                  isLinear: false,
                  eq1: parts[0], eq2: parts[1],
                  a1, b1, c1, a2, b2, c2, det: a1 * b2 - a2 * b1, solStr,
                  graphData: gData
                };
              }
            }
          }
        }
      }

      // 2. Ellipse Standard & General Form (Ch 10.2)
      // e.g. (x-h)^2/a^2 + (y-k)^2/b^2 = 1 or x^2/25 + y^2/9 = 1 or 4x^2 + y^2 = 100
      const ellStd = s.replace(/\s+/g, '').match(/^\(?x([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)\+\(?y([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)=1$/i);
      if (ellStd) {
        const h = ellStd[1] ? -parseFloat(ellStd[1]) : 0;
        const rx = Math.sqrt(parseFloat(ellStd[2]));
        const k = ellStd[3] ? -parseFloat(ellStd[3]) : 0;
        const ry = Math.sqrt(parseFloat(ellStd[4]));
        return { type: 'ellipse', h, k, rx, ry };
      }
      const ellGen = s.replace(/\s+/g, '').match(/^(\d+(?:\.\d+)?)?x\^2\+(\d+(?:\.\d+)?)?y\^2=(\d+(?:\.\d+)?)$/i);
      if (ellGen) {
        const A = ellGen[1] ? parseFloat(ellGen[1]) : 1;
        const B = ellGen[2] ? parseFloat(ellGen[2]) : 1;
        const C = parseFloat(ellGen[3]);
        if (Math.abs(A - B) < 1e-9) {
          const rSq = C / A;
          return { type: 'circle_std', h: 0, k: 0, rSq, r: Math.sqrt(rSq) };
        }
        return { type: 'ellipse', h: 0, k: 0, rx: Math.sqrt(C / A), ry: Math.sqrt(C / B) };
      }

      // 3. Hyperbola Standard & General Form (Ch 10.3)
      // Horizontal: (x-h)^2/a^2 - (y-k)^2/b^2 = 1
      const hypH = s.replace(/\s+/g, '').match(/^\(?x([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)-\(?y([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)=1$/i);
      if (hypH) {
        const h = hypH[1] ? -parseFloat(hypH[1]) : 0;
        const a = Math.sqrt(parseFloat(hypH[2]));
        const k = hypH[3] ? -parseFloat(hypH[3]) : 0;
        const b = Math.sqrt(parseFloat(hypH[4]));
        return { type: 'hyperbola', h, k, a, b, transverse: 'horizontal' };
      }
      // Vertical: (y-k)^2/a^2 - (x-h)^2/b^2 = 1
      const hypV = s.replace(/\s+/g, '').match(/^\(?y([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)-\(?x([+-]\d+(?:\.\d+)?)?\)?\^2\/(\d+(?:\.\d+)?)=1$/i);
      if (hypV) {
        const k = hypV[1] ? -parseFloat(hypV[1]) : 0;
        const a = Math.sqrt(parseFloat(hypV[2]));
        const h = hypV[3] ? -parseFloat(hypV[3]) : 0;
        const b = Math.sqrt(parseFloat(hypV[4]));
        return { type: 'hyperbola', h, k, a, b, transverse: 'vertical' };
      }
      const hypGenH = s.replace(/\s+/g, '').match(/^(\d+(?:\.\d+)?)?x\^2-(\d+(?:\.\d+)?)?y\^2=(\d+(?:\.\d+)?)$/i);
      if (hypGenH) {
        const A = hypGenH[1] ? parseFloat(hypGenH[1]) : 1;
        const B = hypGenH[2] ? parseFloat(hypGenH[2]) : 1;
        const C = parseFloat(hypGenH[3]);
        return { type: 'hyperbola', h: 0, k: 0, a: Math.sqrt(C / A), b: Math.sqrt(C / B), transverse: 'horizontal' };
      }
      const hypGenV = s.replace(/\s+/g, '').match(/^(\d+(?:\.\d+)?)?y\^2-(\d+(?:\.\d+)?)?x\^2=(\d+(?:\.\d+)?)$/i);
      if (hypGenV) {
        const A = hypGenV[1] ? parseFloat(hypGenV[1]) : 1;
        const B = hypGenV[2] ? parseFloat(hypGenV[2]) : 1;
        const C = parseFloat(hypGenV[3]);
        return { type: 'hyperbola', h: 0, k: 0, a: Math.sqrt(C / A), b: Math.sqrt(C / B), transverse: 'vertical' };
      }

      // 4. Circle Standard & General (Ch 1.1)
      const circStd = s.replace(/\s+/g, '').match(/^\(?x([+-]\d+(?:\.\d+)?)?\)?\^2\+\(?y([+-]\d+(?:\.\d+)?)?\)?\^2=(\d+(?:\.\d+)?)$/i);
      if (circStd) {
        const h = circStd[1] ? -parseFloat(circStd[1]) : 0;
        const k = circStd[2] ? -parseFloat(circStd[2]) : 0;
        const rSq = parseFloat(circStd[3]);
        return { type: 'circle_std', h, k, rSq, r: Math.sqrt(rSq) };
      }
      const circGen = s.match(/(?:(\d*)x\^2\s*\+\s*(\d*)y\^2)\s*([+-]\s*\d+x)?\s*([+-]\s*\d+y)?\s*([+-]\s*\d+)?\s*=\s*([+-]?\s*\d+)/i);
      if (circGen && s.includes('y^2')) {
        const a = parseFloat(circGen[1]) || 1;
        const a2 = parseFloat(circGen[2]) || 1;
        const b = circGen[3] ? parseFloat(circGen[3].replace(/\s+|x/g, '')) : 0;
        const c = circGen[4] ? parseFloat(circGen[4].replace(/\s+|y/g, '')) : 0;
        const dLhs = circGen[5] ? parseFloat(circGen[5].replace(/\s+/g, '')) : 0;
        const rhsVal = parseFloat(circGen[6].replace(/\s+/g, '')) || 0;
        const d = dLhs - rhsVal;
        if (Math.abs(a - a2) < 1e-9) {
          return { type: 'circle_gen', a, b, c, d };
        }
      }

      // 4b. Circle from grouped/general polynomial form (Ch 2.2 Q15/Q21):
      // (x^2 + 12x) + (y^2 - 14y) = 5   or   4x^2 + 4x + 4y^2 - 32y - 79 = 0
      if (/x\^2/i.test(s) && /y\^2/i.test(s) && /=/.test(s) && !/[\/|;<>]/.test(s)) {
        const conicParsed = parseConicGeneralStd(s);
        if (conicParsed) return conicParsed;
      }

      // 5. Absolute Value Equations & Inequalities (Ch 1.6 & 1.8)
      // 5a. Double absolute value: |a1 x + b1| = |a2 x + b2|
      const absDouble = s.match(/^\|\s*([^|]+)\s*\|\s*=\s*\|\s*([^|]+)\s*\|$/i);
      if (absDouble) {
        const p1 = parsePolyCoeffs(absDouble[1]);
        const p2 = parsePolyCoeffs(absDouble[2]);
        const a1 = p1.length === 2 ? p1[0] : 0, b1 = p1[p1.length - 1] || 0;
        const a2 = p2.length === 2 ? p2[0] : 0, b2 = p2[p2.length - 1] || 0;
        const sols = [];
        if (Math.abs(a1 - a2) > 1e-9) sols.push((b2 - b1) / (a1 - a2));
        if (Math.abs(a1 + a2) > 1e-9) sols.push((-b2 - b1) / (a1 + a2));
        return { type: 'abs_double', a1, b1, a2, b2, sols };
      }
      // 5b. General single absolute value: (k)*|inside| (+/- shift) [op] rhs (Ch 1.8)
      const absGen = s.match(/^([+-]?\d+(?:\.\d+)?)?\*?\|\s*([^|]+)\s*\|\s*([+-]\s*\d+(?:\.\d+)?)?\s*(<=|>=|<|>|=)\s*([+-]?\s*\d+(?:\.\d+)?)$/i);
      if (absGen) {
        let k = (absGen[1] !== undefined && absGen[1] !== '') ? parseFloat(absGen[1]) : 1;
        if (isNaN(k)) k = 1;
        if (k !== 0) {
          const insidePoly = parsePolyCoeffs(absGen[2]);
          if (insidePoly && insidePoly.length === 2 && insidePoly[0] !== 0) {
            let a = insidePoly[0];
            let b = insidePoly[1];
            const shift = absGen[3] ? parseFloat(absGen[3].replace(/\s+/g, '')) : 0;
            let op = absGen[4];
            let c = parseFloat(absGen[5].replace(/\s+/g, '')) - shift;
            if (k < 0) {
              c = c / k;
              if (op === '<') op = '>';
              else if (op === '<=') op = '>=';
              else if (op === '>') op = '<';
              else if (op === '>=') op = '<=';
            } else {
              c = c / k;
            }
            if (a < 0) { a = -a; b = -b; }
            return { type: 'abs', a, b, op, c, origK: k };
          }
        }
      }

      // 5b. Quotient Sign Rules (Ch 3.6 Q18–19): e.g. (-a)/(-b) > 0, (-a)/(+b) < 0
      const signRuleMatch = s.match(/^\(?\s*([+-]?)\s*[a-zA-Z]\s*\)?\s*\/\s*\(?\s*([+-]?)\s*[a-zA-Z]\s*\)?(?:\s*(?:>|<|>=|<=|=)\s*0)?$/i);
      if (signRuleMatch && !s.includes('x') && !s.includes('^')) {
        const nSign = signRuleMatch[1] === '-' ? 'Negative' : 'Positive';
        const dSign = signRuleMatch[2] === '-' ? 'Negative' : 'Positive';
        const isSame = (nSign === dSign);
        const resSign = isSame ? 'Positive' : 'Negative';
        const ruleDesc = isSame ? 'A negative number divided by a negative number (like signs) is always a positive number.' : 'A negative number divided by a positive number (unlike signs) is always a negative number.';
        return { type: 'sign_rule', numSign: nSign, denSign: dSign, resSign, ruleDesc };
      }

      // 5c. Absolute value FUNCTION form: y = a*abs(bx + c) + d (graph only)
      const absFnSrc = s.replace(/^(?:y|[fgh]\(x\))\s*=\s*/i, '').trim();
      if (/^abs\(/i.test(absFnSrc) && !/\^/.test(absFnSrc)) {
        const absFnMatch = absFnSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*abs\(\s*([^|()]+)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?$/i);
        if (absFnMatch && /[a-zA-Z]/.test(absFnMatch[2])) {
          const insideLin = polyToLin(parsePolyCoeffs(absFnMatch[2]));
          if (insideLin && Math.abs(insideLin.m) > 1e-12) {
            const aStr = absFnMatch[1] || '';
            const aFn = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
            const dFn = absFnMatch[3] ? parseFloat(absFnMatch[3].replace(/\s+/g, '')) : 0;
            return { type: 'abs_func', a: aFn, inside: absFnMatch[2].trim(), lin: insideLin, d: dFn };
          }
        }
      }

      // 6. Rational Inequalities (Ch 3.6): N(x)/D(x) [op] RHS
      if ((s.includes('/') || s.includes('÷')) && /(<=|>=|<|>)/.test(s) && !s.includes('|')) {
        const ineqParts = s.match(/^(.*?)\s*(<=|>=|<|>)\s*([+-]?\s*\d+(?:\.\d+)?)$/);
        if (ineqParts) {
          const lhs = stripOuterParens(ineqParts[1]);
          const op = ineqParts[2];
          const rhsK = parseFloat(ineqParts[3].replace(/\s+/g, '')) || 0;
          const slashIdx = findTopLevelSlash(lhs);
          if (slashIdx !== -1) {
            const numRaw = lhs.slice(0, slashIdx).trim();
            const denRaw = lhs.slice(slashIdx + 1).trim();
            if (/[a-zA-Z]/.test(denRaw)) {
              const origNum = parseAnyPolyCoeffs(numRaw);
              const denCoeffs = parseAnyPolyCoeffs(denRaw);
              const numCoeffs = rhsK === 0 ? origNum : subPolysJS(origNum, denCoeffs.map(c => c * rhsK));
              return { type: 'rat_ineq', numRaw, denRaw, origNum, numCoeffs, denCoeffs, op, rhsK };
            }
          }
        }
      }

      // 7. Polynomial Inequalities (Ch 3.6): P(x) [op] RHS
      if (/(<=|>=|<|>)/.test(s) && !s.includes('/') && !s.includes('|') && /[a-zA-Z]/.test(s)) {
        const ineqParts = s.match(/^(.*?)\s*(<=|>=|<|>)\s*([+-]?\s*\d+(?:\.\d+)?)$/);
        if (ineqParts) {
          const lhsCoeffs = parseAnyPolyCoeffs(ineqParts[1]);
          const op = ineqParts[2];
          const rhsK = parseFloat(ineqParts[3].replace(/\s+/g, '')) || 0;
          if (lhsCoeffs.length >= 2) {
            const coeffs = [...lhsCoeffs];
            coeffs[coeffs.length - 1] -= rhsK;
            const varMatch = ineqParts[1].match(/[a-zA-Z]/);
            const variable = varMatch ? varMatch[0] : 'x';
            return { type: 'poly_ineq', coeffs, op, rhsK, rawLhs: ineqParts[1].trim(), variable };
          }
        }
      }

      // 8. Rational Functions & Synthetic Division: N(x) / D(x)
      if ((s.includes('/') || s.includes('÷')) && /[a-zA-Z]/.test(s)) {
        const cleanFn = stripOuterParens(s.replace(/^(?:[fghpqr]\(x\)|y)\s*=\s*/i, '').trim());
        const slashIdx = findTopLevelSlash(cleanFn);
        if (slashIdx !== -1) {
          const numStr = cleanFn.slice(0, slashIdx).trim();
          const denStr = cleanFn.slice(slashIdx + 1).trim();
          const numCoeffs = parseAnyPolyCoeffs(numStr);
          const denCoeffs = parseAnyPolyCoeffs(denStr);
          if (denCoeffs.length >= 2) {
            // If no f(x)= prefix and denominator is monic linear (x - c) and numerator degree >= 2, check if synthetic division
            const isFuncPrefix = /^(?:[fghpqr]\(x\)|y)\s*=/i.test(s);
            const cleanNum = stripOuterParens(numStr);
            if (!isFuncPrefix && denCoeffs.length === 2 && denCoeffs[0] === 1 && numCoeffs.length >= 3 && !cleanNum.includes('(')) {
              return {
                type: 'synthetic',
                poly: cleanNum,
                c: -denCoeffs[1],
                numCoeffs,
                denCoeffs
              };
            }
            return {
              type: 'rational',
              numStr,
              denStr,
              numCoeffs,
              denCoeffs
            };
          }
        }
      }

      // 9. Exponential Functions & Equations (Ch 4.2, 4.5)
      // e.g. 2^(x - 1) - 3, f(x) = 3^(x+2) + 1, 2^(x-1) = 8, e^(2x) = 7
      // HARDENED (v4): fractional / parenthesized / decimal bases like
      // (1/5)^x, (0.5)^x, (9/2)^x, -(1/4)^(x+3) - 2
      const expClean = s.replace(/^(?:[fghg]\(x\)|y)\s*=\s*/i, '').trim();
      const expCleanFlat = expClean
        .replace(/\(\(([+-]?\d+(?:\.\d+)?)\)\)/g, '($1)')
        .replace(/\(([+-]?\d+(?:\.\d+)?)\)\s*\/\s*\(([+-]?\d+(?:\.\d+)?)\)/g, '($1/$2)');
      const expMatch = expCleanFlat.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(e|\d+(?:\.\d+)?|\([\d.]+\)|\(\d+(?:\.\d+)?\s*\/\s*\d+(?:\.\d+)?\)|sqrt\(\d+(?:\.\d+)?\))\s*\^\s*(?:\(([^()]+)\)|([+-]?[0-9a-zA-Z+\-]+))\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (expMatch && (expMatch[3] || expMatch[4] || '').toLowerCase().includes('x')) {
        const aStr = expMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const baseRawM = expMatch[2];
        let base;
        if (/^e$/i.test(baseRawM)) base = Math.E;
        else if (/^sqrt\(/i.test(baseRawM)) base = Math.sqrt(parseFloat(baseRawM.replace(/[^\d.]/g, '')));
        else base = parseConstValue(baseRawM) !== null ? parseConstValue(baseRawM) : parseFloat(baseRawM);
        const expPoly = parsePolyCoeffs(expMatch[3] || expMatch[4]);
        const m = expPoly.length === 2 ? expPoly[0] : 1;
        const bShift = expPoly.length === 2 ? expPoly[1] : 0;
        const h = -bShift / m;
        const k = expMatch[5] ? parseFloat(expMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = expMatch[6] !== undefined;
        let rhs = undefined, rhsV = null;
        if (hasRhs) { rhsV = parseConstValue(expMatch[6]); rhs = rhsV !== null ? rhsV : parseFloat(expMatch[6]); }
        let solX = undefined;
        if (hasRhs && rhsV !== null && (rhs - k) / a > 0 && base > 0 && base !== 1) {
          solX = (Math.log((rhs - k) / a) / Math.log(base) - bShift) / m;
        }
        // __ENGINE_V4_2__: RHS present but not a constant (e.g. 256^(3x) = 64^(x+2))
        // means exponential EQUATION -> fall through to 9b, don't misreport.
        if (!hasRhs || rhsV !== null) {
          return { type: 'exp_func', a: a, base: base, h: h, k: k, m: m, bShift: bShift, hasRhs: hasRhs, rhs: rhs, solX: solX };
        }
      }

      // 9a. sqrt function form: a*sqrt(linear) + k (graph + domain)
      const sqrtFnMatch = expClean.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*sqrt\(\s*([^()]+)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (sqrtFnMatch && /x/i.test(sqrtFnMatch[2])) {
        const insideLin = polyToLin(parsePolyCoeffs(sqrtFnMatch[2]));
        if (insideLin) {
          const aStr = sqrtFnMatch[1] || '';
          const aSq = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
          const kSq = sqrtFnMatch[3] ? parseFloat(sqrtFnMatch[3].replace(/\s+/g, '')) : 0;
          return { type: 'sqrt_func', a: aSq, inside: sqrtFnMatch[2].trim(), lin: insideLin, k: kSq };
        }
      }

      // 9b. Exponential EQUATIONS (Ch 4.2 Q32-38, 4.5 Q2-Q8, PW 4.3 Q5-12):
      //   b1^E1 = b2^E2 | b^E = K | b1^E1 -/+ b2^E2 | A*b^E +/- C1 +/- C2
      if (/\^/.test(expClean) && /[0-9]/.test(expClean) && /x/i.test(expClean) &&
          !/x\s*\^/.test(expClean) && !/[|,;]/.test(expClean) && !/[<>]/.test(expClean)) {
        const eqParts = expClean.split('=');
        if (eqParts.length === 2) {
          const lTerms = splitTopLevelOps(eqParts[0]).map(classifyPowTerm);
          const rTerms = splitTopLevelOps(eqParts[1]).map(classifyPowTerm);
          if (lTerms.every(Boolean) && rTerms.every(Boolean)) {
            const pows = [].concat(lTerms, rTerms).filter(t => t && t.kind === 'pow');
            const consts = [].concat(lTerms, rTerms).filter(t => t && t.kind === 'const');
            if (pows.length === 2 && consts.length === 0) {
              // b1^E1 = b2^E2  ->  (ln b1)E1 = (ln b2)E2 (linear in x)
              const P1 = pows[0], P2 = pows[1];
              // __ENGINE_V4_2__: signs are intrinsic to each term now
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef, P2.lin));
              if (Math.abs(lin.m) > 1e-12) {
                const x = -lin.b / lin.m;
                return { type: 'exp_eq', lhs: eqParts[0].trim(), rhs: eqParts[1].trim(),
                         b1: P1.lnBase, b2: P2.lnBase, x: x, xStr: rationalizeVal(x) };
              }
            } else if (pows.length === 1 && consts.length >= 1) {
              // b^E = K1 - K2 ... -> b^E = C  (signs intrinsic)
              const P = pows[0];
              const idxP = lTerms.indexOf(P);
              const cL = lTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const cR = rTerms.filter(t => t.kind === 'const').reduce((s, t) => s + t.v, 0);
              const C = idxP >= 0 ? (cR - cL) : (cL - cR);   // move consts across =
              const A = P.coef;
              if (C * A > 0 && P.lnBase !== null) {
                const rhsT = Math.log(C * A) - Math.log(Math.abs(A));
                // A*b^E = C*A? No: A*b^E = C  -> b^E = C/A
                const lin = linMul(P.lnBase, P.lin);
                if (Math.abs(lin.m) > 1e-12) {
                  const x = (Math.log(C / A) - lin.b) / lin.m;
                  return { type: 'exp_eq', lhs: eqParts[0].trim(), rhs: eqParts[1].trim(),
                           b1: P.lnBase, b2: Math.log(C / A), x: x, xStr: rationalizeVal(x) };
                }
              }
            }
          }
        } else if (eqParts.length === 1) {
          // no '=': difference/sum or coeff*pow +/- consts  (Ch 4.5 Q4-Q8)
          const terms = splitTopLevelOps(expClean).map(classifyPowTerm);
          if (terms.every(Boolean)) {
            const powT = terms.filter(t => t.kind === 'pow');
            const constT = terms.filter(t => t.kind === 'const');
            if (powT.length === 2 && constT.length === 0) {
              const P1 = powT[0], P2 = powT[1];
              // __ENGINE_V4_2__: signs intrinsic; no positional neg2 hack
              const lin = linSub(linMul(P1.lnBase * P1.coef, P1.lin),
                                 linMul(P2.lnBase * P2.coef, P2.lin));
              if (Math.abs(lin.m) > 1e-12) {
                const x = -lin.b / lin.m;
                return { type: 'exp_eq', lhs: expClean.trim(), rhs: '0',
                         b1: P1.lnBase, b2: P2.lnBase, x: x, xStr: rationalizeVal(x) };
              }
            } else if (powT.length === 1) {
              const P = powT[0];
              const C = constT.reduce((s, t) => s + t.v, 0);
              // A*b^E + C = 0  ->  b^E = -C/A
              if (Math.abs(P.coef) > 1e-12) {
                const K = -C / P.coef;
                if (K > 0 && P.lnBase !== null) {
                  const lin = linMul(P.lnBase, P.lin);
                  if (Math.abs(lin.m) > 1e-12) {
                    const x = (Math.log(K) - lin.b) / lin.m;
                    return { type: 'exp_eq', lhs: expClean.trim(), rhs: '0',
                             b1: P.lnBase, b2: Math.log(K), x: x, xStr: rationalizeVal(x) };
                  }
                }
              }
            }
          }
        }
      }


      // 10. Logarithmic Functions & Equations (Ch 4.3, 4.5)
      // e.g. log_2(x - 1) + 2, ln(x + 3) = 4, log(x) - 1 = 2
      // HARDENED (v4): log10( -> log_10(, bare args (log_5 x = 2),
      // fractional bases (log_1/4(x+2) = -3), variable bases
      // (log_(x + 7) 13 = 1), rhs fractions, change-of-base division form
      // (ln(x)/ln(2) + k) and log-sum equations (log A + log B = log C | K).
      const logSrc = expClean
        // __ENGINE_V4_6__: reversed parameter forms 'K = log_b M' -> 'log_b M = K'
        // (no \b after log: '_' is a word char and kills the boundary)
        .replace(/^([+-]?\d+(?:\.\d+)?)\s*=\s*((?:ln|log)[\s\S]*)$/i, '$2 = $1')
        .replace(/\\?sqrt\[(\d+)\]\{([a-z0-9.]+)\}/gi, '$2^(1/$1)')
        .replace(/\\?sqrt\{([a-z0-9.]+)\}/gi, 'sqrt($1)')
        .replace(/\blog\s*10\s*\(/gi, 'log_10(')
        .replace(/\b(ln|log(?:_?\d+(?:\.\d+)?|_?sqrt\(\d+(?:\.\d+)?\)|_?[a-z])?)\s+(\([^()]*\)|[A-Za-z0-9][A-Za-z0-9.]*(?:\^\(?[+-]?\d+(?:\.\d+)?\)?)?)/gi, '$1($2)')
        // __ENGINE_V4_5__: bare numeric powers stay attached to their base:
        // 'log 10^(-7)' -> log(10^(-7)), never log(10)^(-7)
        .replace(/^x\s*=\s*(?=[+-]?\d*\.?\d*\s*(?:ln|log)\b)/i, '');
      // 10a0. __ENGINE_V4_6__: parameter-form log equations — solve for
      //      a letter base, a letter argument, or a letter value; verify
      //      all-numeric statements like log_sqrt(5) 625 = 8.
      const logParam = logSrc.match(/^log[_](\d+(?:\.\d+)?|sqrt\(\d+(?:\.\d+)?\)|[a-z])\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9][A-Za-z0-9.]*))\s*=\s*([0-9]+(?:\.[0-9]+)?|[a-z])\s*$/i);
      if (logParam) {
        const bpRaw = logParam[1];
        const bpVal = /^\d/.test(bpRaw) ? parseFloat(bpRaw)
                    : /^sqrt/i.test(bpRaw) ? Math.sqrt(parseFloat(bpRaw.replace(/^sqrt\(|\)$/g, '')))
                    : null;
        const apRaw = String(logParam[2] !== undefined ? logParam[2] : logParam[3]).trim();
        const apVal = /^[a-z]$/i.test(apRaw) ? null : parseConstValue(apRaw);
        const rpRaw = String(logParam[4]).trim();
        const rpVal = /^[a-z]$/i.test(rpRaw) ? null : parseFloat(rpRaw);
        if (bpVal !== null && apVal === null && /^[a-z]$/i.test(apRaw) && apRaw !== 'x' && apRaw !== 't' && rpVal !== null) {
          // log_b(M) = K  ->  M = b^K
          return { type: 'log_eq2', roots: [Math.pow(bpVal, rpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpVal, kind: 'param-arg' };
        } else if (bpVal === null && /^[a-z]$/i.test(bpRaw) && apVal !== null && rpVal !== null && rpVal !== 0) {
          // log_b(K) = C  ->  b = K^(1/C)
          return { type: 'log_eq2', roots: [Math.pow(apVal, 1 / rpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpVal, kind: 'param-base' };
        } else if (bpVal !== null && bpVal > 0 && bpVal !== 1 && apVal !== null && apVal > 0 && rpVal === null && /^[a-z]$/i.test(rpRaw)) {
          // log_b(K) = y  ->  y = ln K / ln b
          return { type: 'log_eq2', roots: [Math.log(apVal) / Math.log(bpVal)],
                   baseExpr: bpRaw, argExpr: apRaw, rhs: rpRaw, kind: 'param-value' };
        } else if (bpVal !== null && bpVal > 0 && bpVal !== 1 && apVal !== null && apVal > 0 && rpVal !== null) {
          // all numeric: verify ln K / ln b == rhs
          const lhsV = Math.log(apVal) / Math.log(bpVal);
          if (Math.abs(lhsV - rpVal) < 1e-9) {
            return { type: 'log_eq2', roots: [rpVal], baseExpr: bpRaw,
                     argExpr: apRaw, rhs: rpVal, kind: 'verify' };
          }
        }
      }

      const logMatch = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log(?:_(\d+(?:\.\d+)?))?)\s*\(\s*([^()]+?)\s*\)\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (logMatch && logMatch[4].includes('x')) {
        const aStr = logMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName = logMatch[2].toLowerCase();
        const base = fnName === 'ln' ? Math.E : (logMatch[3] ? parseFloat(logMatch[3]) : 10);
        const insideP = parsePolyCoeffs(logMatch[4]);
        const m = insideP.length === 2 ? insideP[0] : 1;
        const bShift = insideP.length === 2 ? insideP[1] : 0;
        const h = -bShift / m;
        const k = logMatch[5] ? parseFloat(logMatch[5].replace(/\s+/g, '')) : 0;
        const hasRhs = logMatch[6] !== undefined;
        const rhsV = hasRhs ? parseConstValue(logMatch[6]) : null;
        const rhs = hasRhs ? (rhsV !== null ? rhsV : parseFloat(logMatch[6])) : undefined;
        let solX = undefined;
        if (hasRhs && rhsV !== null) {
          solX = (Math.pow(base, (rhs - k) / a) - bShift) / m;
        }
        return { type: 'log_func', a, base, h, k, m, bShift, hasRhs, rhs, solX };
      }

      // 10a. Log EXPRESSION arithmetic (Ch 4.3-4.4): eval / expand / equation.
      //      Must run before 10b/10c/10d (it is the general shape).
      {
        const lshape = parseLogExprShape(logSrc);
        if (lshape) {
          // __ENGINE_V4_4__: routing order matters.
          //  (a) both sides pure logs AND an rhs -> log-sum EQUATION:
          //      defer to the 10d solver (condense A(+/-)B = C -> A*B = C).
          //  (b) every argument a constant -> numeric EVAL via change of base.
          //  (c) otherwise -> symbolic structural EXPAND (product/quotient).
          const allLogL = lshape.lhs.terms.every(t => t.kind === 'log');
          const allLogR = !lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'log');
          const allConst = lshape.lhs.terms.every(t => t.kind === 'const' || t.argConst !== null)
                        && (!lshape.rhs || lshape.rhs.terms.every(t => t.kind === 'const' || t.argConst !== null));
          if (allLogL && allLogR && lshape.hasRhs) {
            // fall through to 10d
          } else if (allConst) {
            function evalSide(sd) {
              return sd.terms.reduce(function (acc2, t2) {
                if (t2.kind === 'const') return acc2 + t2.v;
                return acc2 + t2.coef * Math.log(t2.argConst) / Math.log(t2.base);
              }, 0);
            }
            const val = evalSide(lshape.lhs) - (lshape.rhs ? evalSide(lshape.rhs) : 0);
            const exactish = Math.abs(Math.round(val) - val) < 1e-9 ? Math.round(val) : Number(val.toFixed(4));
            return { type: 'log_expr', mode: lshape.hasRhs ? 'equation' : 'eval',
                     value: exactish, hasRhs: lshape.hasRhs, raw: logSrc };
          } else if (!lshape.hasRhs) {
            return { type: 'log_expr', mode: 'expand', raw: logSrc, shape: lshape };
          }
          // mixed log + const with rhs: fall through to 10d as well
        }
      }

      // 10b. Bare-argument log equations: log_5 x = 2 | log_36 x = 3/2 |
      //      variable base log_(x + 7) 13 = 1 | fractional base log_1/4(x+2) = -3
      const logBare = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log)_?(?:\(\s*([^()]+?)\s*\)|([0-9]+(?:\/[0-9]+)?))?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9][A-Za-z0-9.^+\-]*))?\s*(?:(?:[+-]\s*\d+(?:\.\d+)?)\s*)?(?:=\s*(.+))?$/i);
      if (logBare) {
        const aStr = logBare[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName2 = logBare[2].toLowerCase();
        const baseRaw2 = logBare[3] !== undefined ? logBare[3] : (logBare[4] !== undefined ? logBare[4] : null);
        const argRaw2 = (logBare[5] !== undefined ? logBare[5] : (logBare[6] !== undefined ? logBare[6] : '')).trim();
        const hasRhs2 = logBare[7] !== undefined;
        const rhsV2 = hasRhs2 ? parseConstValue(logBare[7]) : null;
        if (argRaw2 && (hasRhs2 ? rhsV2 !== null : true)) {
          const baseVar = baseRaw2 !== null && /[a-z]/i.test(baseRaw2);
          let base2 = fnName2 === 'ln' ? Math.E : 10;
          if (baseRaw2 !== null && !baseVar) base2 = parseConstValue(baseRaw2) !== null ? parseConstValue(baseRaw2) : parseFloat(baseRaw2);
          if (base2 > 0 && base2 !== 1) {
            const argPoly2 = parseAnyPolyCoeffs(argRaw2);
            const argLin2 = polyToLin(argPoly2);
            if (baseVar) {
              // log_(x + 7) 13 = 1  ->  (x + 7)^rhs = 13
              const baseLin2 = polyToLin(parsePolyCoeffs(baseRaw2));
              const argV2 = parseConstValue(argRaw2);
              if (baseLin2 && argV2 !== null && hasRhs2 && rhsV2 !== null) {
                const target = Math.pow(argV2, 1 / rhsV2);
                if (isFinite(target)) {
                  const x = (target - baseLin2.b) / baseLin2.m;
                  if (Math.abs(baseLin2.m) > 1e-12) {
                    return { type: 'log_eq2', roots: [x], baseExpr: baseRaw2, argExpr: argRaw2,
                             rhs: rhsV2, kind: 'var-base', xStr: rationalizeVal(x) };
                  }
                }
              }
            } else if (argLin2 && argPoly2.length <= 2 && !hasRhs2) {
              // log_b(linear) with no rhs: plain function form
              return { type: 'log_func', a: a, base: base2, h: -argLin2.b / argLin2.m, k: 0,
                       m: 1, bShift: 0, hasRhs: false, rhs: undefined, solX: undefined };
            } else if (argLin2 && argPoly2.length <= 2 && hasRhs2) {
              const solX2 = (Math.pow(base2, (rhsV2 - 0) / a) - argLin2.b) / argLin2.m;
              return { type: 'log_func', a: a, base: base2, h: -argLin2.b / argLin2.m, k: 0,
                       m: 1, b: 0, hasRhs: true, rhs: rhsV2, solX: solX2 };
            } else if (argPoly2.length === 3 && hasRhs2) {
              // log_b(quadratic) = K  ->  quadratic = base^(K/a), then solve
              const target2 = Math.pow(base2, rhsV2 / a);
              const qa = argPoly2[0], qb = argPoly2[1], qc = argPoly2[2] - target2;
              const disc = qb * qb - 4 * qa * qc;
              if (disc >= 0) {
                const r1 = (-qb + Math.sqrt(disc)) / (2 * qa);
                const r2 = (-qb - Math.sqrt(disc)) / (2 * qa);
                const rad2 = simplifyRadical(disc);
                return { type: 'log_eq2', roots: [r1, r2], baseExpr: String(base2), argExpr: argRaw2,
                         rhs: rhsV2, kind: 'quadratic', radStr: rad2.str, qa, qb, qc };
              }
            }
          }
        }
      }

      // 10c. Change-of-base division form: a*ln(ARG)/ln(b) + k  (Ch 4.3 Q6/25/27/28)
      const cobM = logSrc.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log)\s*\(\s*(.+?)\s*\)\s*\/\s*(?:ln|log)(?:_?|\s*\()?\s*(\d+(?:\.\d+)?)\s*\)?\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*(.+))?$/i);
      if (cobM && /x/i.test(cobM[3])) {
        const aStr = cobM[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const base3 = parseFloat(cobM[4]);
        const argRaw3 = cobM[3].trim();
        const k3 = cobM[5] ? parseFloat(cobM[5].replace(/\s+/g, '')) : 0;
        const hasRhs3 = cobM[6] !== undefined;
        const rhsV3 = hasRhs3 ? parseConstValue(cobM[6]) : null;
        const argPoly3 = parseAnyPolyCoeffs(argRaw3);
        const argLin3 = polyToLin(argPoly3);
        if (base3 > 0 && base3 !== 1 && argLin3 && argPoly3.length <= 2 && (!hasRhs3 || rhsV3 !== null)) {
          const h3 = -argLin3.b / argLin3.m;
          const solX3 = hasRhs3 ? (h3 + Math.pow(base3, (rhsV3 - k3) / a)) : undefined;
          return { type: 'log_func', a: a, base: base3, h: h3, k: k3, m: 1,
                   bShift: 0, hasRhs: hasRhs3, rhs: rhsV3, solX: solX3 };
        }
      }

      // 10d. Log-sum / log-difference equations (Ch 4.5 Q18-21, 25-26):
      //      log A + log B = log C | K     (any common base, bare or parens)
      // __ENGINE_V4_3__: bases may be missing, numeric, or sqrt(d);
      // arguments may be parenthesized or bare.
      const logSum = logSrc.match(/^(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*([+-])\s*(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))\s*=\s*(?:(?:ln|log)(?:_?\(?([0-9]+(?:\.[0-9]+)?|sqrt\([0-9.]+\))\)?)?\s*(?:\(\s*([^()]+?)\s*\)|([A-Za-z0-9.^+\-]+))|([A-Za-z0-9][A-Za-z0-9.]*))$/i);
      if (logSum) {
        // __ENGINE_V4_3__: base tokens may be 'sqrt(5)' — use parseLnOfBase.
        function logBaseFrom(tok) {
          if (tok === undefined) return 10;
          const ln2 = parseLnOfBase(String(tok));
          return ln2 !== null ? Math.exp(ln2) : parseFloat(tok);
        }
        // __ENGINE_V4_5b__: unmatched optional regex groups are null in JS,
        // not undefined — treat null as missing throughout. ln sums default
        // to base e (matters when exponentiating a numeric rhs).
        const baseS = logBaseFrom(logSum[1] || logSum[5] || (/^ln/i.test(logSrc) ? Math.E : 10));
        const Araw = String(logSum[2] || logSum[3] || '').trim();
        const opS = logSum[4] === '-' ? -1 : 1;
        const Braw = String(logSum[6] || logSum[7] || '').trim();
        const rhsIsLog = !!(logSum[9] || logSum[10]);
        const baseS2 = rhsIsLog ? logBaseFrom(logSum[8] || (/^ln/i.test(logSrc) ? Math.E : 10)) : baseS;
        const Craw = rhsIsLog ? String(logSum[9] || logSum[10] || '').trim() : String(logSum[11] || '');
        const A2 = parseAnyPolyCoeffs(Araw);
        const Bv = parseConstValue(Braw);
        // __ENGINE_V4_5c__: second term may be a polynomial (log A + log B = K)
        const B2poly = Bv !== null ? [Bv] : parseAnyPolyCoeffs(Braw);
        const C2 = rhsIsLog ? parseAnyPolyCoeffs(Craw) : parseConstValue(String(Craw));
        if (A2 && B2poly && C2 !== null && baseS > 0 && baseS !== 1 && baseS === baseS2) {
          // log A ± log K = log C | number   ->  A * K^(±1) = C
          const lhsCo = opS > 0 ? multiplyPolysJS(A2, B2poly)
                       : (Bv !== null ? multiplyPolysJS(A2, [1 / Bv]) : null);
          // __ENGINE_V4_5c__: reject roots outside the log domains (all
          // arguments must stay strictly positive at the solution).
          function domOK(xv) {
            // __ENGINE_V4_5d__: coeffs are [leading, ..., constant] — Horner
            // must iterate FRONT to BACK.
            var pv = function (co) { var ac = 0; for (var ii = 0; ii < co.length; ii++) ac = ac * xv + co[ii]; return ac; };
            if (pv(A2) <= 1e-9 || pv(B2poly) <= 1e-9) return false;
            if (rhsIsLog && pv(C2) <= 1e-9) return false;
            return true;
          }
          let rhsCo = null;
          if (rhsIsLog) {
            const C2poly = C2;
            rhsCo = C2poly;
          } else {
            // __ENGINE_V4_5b__: numeric rhs means A·K = base^rhs (not rhs)
            const Cnum = C2;
            rhsCo = [Math.pow(baseS, Cnum)];
          }
          if (rhsCo && lhsCo) {
            const comb = subPolysJS(lhsCo, rhsCo);
            if (comb.length === 2) {
              const x = -comb[1] / comb[0];
              if (domOK(x)) {
                return { type: 'log_eq2', roots: [x], baseExpr: String(baseS),
                         argExpr: '(' + Araw + ')(' + Braw + ')', rhs: Cnum2str(Craw, rhsIsLog),
                         kind: 'sum-linear' };
              }
            } else if (comb.length === 3) {
              const qa = comb[0], qb = comb[1], qc = comb[2];
              const disc = qb * qb - 4 * qa * qc;
              if (disc >= 0) {
                const r1 = (-qb + Math.sqrt(disc)) / (2 * qa);
                const r2 = (-qb - Math.sqrt(disc)) / (2 * qa);
                const keep = [r1, r2].filter(domOK);
                if (keep.length) {
                  return { type: 'log_eq2', roots: keep, baseExpr: String(baseS),
                           argExpr: '(' + Araw + ')(' + Braw + ')', rhs: Cnum2str(Craw, rhsIsLog),
                           kind: 'sum-quadratic' };
                }
              }
            }
          }
        }
      }

      // 10b. Numeric Logarithm Evaluation (Ch 4.3–4.4): log_b(A), ln(A), log(A)
      const logEvalMatch = expClean.match(/^([+-]?\d*\.?\d*)?\s*\*?\s*(ln|log(?:_(\d+(?:\.\d+)?))?)\s*\(\s*([0-9./+-]+)\s*\)$/i);
      if (logEvalMatch) {
        const aStr = logEvalMatch[1] || '';
        const a = (aStr === '' || aStr === '+') ? 1 : (aStr === '-' ? -1 : parseFloat(aStr));
        const fnName = logEvalMatch[2].toLowerCase();
        const base = fnName === 'ln' ? Math.E : (logEvalMatch[3] ? parseFloat(logEvalMatch[3]) : 10);
        let argVal = NaN;
        const argRaw = logEvalMatch[4].trim();
        if (argRaw.includes('/')) {
          const sp = argRaw.split('/');
          argVal = parseFloat(sp[0]) / parseFloat(sp[1]);
        } else {
          argVal = parseFloat(argRaw);
        }
        if (argVal > 0 && base > 0 && base !== 1) {
          const resultVal = a * (Math.log(argVal) / Math.log(base));
          return { type: 'log_eval', a, base, argRaw, argVal, resultVal };
        }
      }

      // 11. Complex Numbers, Radicals, Standard Form Fractions, Solution Verification (Ch 1.3)
      // 11a. Complex Solution Verification: "a + bi; x^2 + px + q = 0" (Ch 1.3 Q17–18)
      const cplxVerify = s.match(/^(?:x\s*=\s*)?\(?([+-]?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\)?\s*(?:[;,]|in|for)\s*x\^2\s*([+-]\s*\d*(?:\.\d+)?)x\s*([+-]\s*\d+(?:\.\d+)?)\s*=\s*0$/i);
      if (cplxVerify) {
        const u = parseFloat(cplxVerify[1]);
        const vRaw = cplxVerify[2].replace(/\s+/g, '');
        const v = (vRaw === '+' || vRaw === '') ? 1 : (vRaw === '-' ? -1 : parseFloat(vRaw));
        const p = parseFloat(cplxVerify[3].replace(/\s+/g, ''));
        const q = parseFloat(cplxVerify[4].replace(/\s+/g, ''));
        return { type: 'complex_verify_quad', u, v, p, q };
      }

      // 11b. Complex Impedance E = IZ: "I = a + bi, Z = c + di" (Ch 1.3 Q19)
      const izMatch = s.match(/(?:E\s*=\s*I\s*\*?\s*Z\s*[,;]?\s*)?I\s*=\s*([+-]?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*[,;]\s*Z\s*=\s*([+-]?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i/i);
      if (izMatch) {
        const parseI = (raw) => {
          const r = raw.replace(/\s+/g, '');
          return (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        };
        return {
          type: 'complex_mult',
          a1: parseFloat(izMatch[1]),
          b1: parseI(izMatch[2]),
          a2: parseFloat(izMatch[3]),
          b2: parseI(izMatch[4])
        };
      }

      // 11c. Standard Form Complex / Radical Fraction: (A ± B*sqrt(C)) / D (Ch 1.3 Q11–13)
      let cleanFrac = s.replace(/\s+/g, '');
      while (cleanFrac.startsWith('(') && cleanFrac.endsWith(')')) {
        let depth = 0, wrapsAll = true;
        for (let i = 0; i < cleanFrac.length - 1; i++) {
          if (cleanFrac[i] === '(') depth++;
          else if (cleanFrac[i] === ')') {
            depth--;
            if (depth === 0) { wrapsAll = false; break; }
          }
        }
        if (wrapsAll) cleanFrac = cleanFrac.slice(1, -1);
        else break;
      }
      const stdFracMatch = cleanFrac.match(/^\(?([+-]?\d+)([+-]\d*\*?)(?:sqrt|√)\(?([+-]?\d+)\)?\)?\/\(?([+-]?\d+)\)?$/i);
      if (stdFracMatch) {
        const A = parseInt(stdFracMatch[1], 10);
        const bRaw = stdFracMatch[2].replace(/\*/g, '');
        const B = (bRaw === '+' || bRaw === '') ? 1 : (bRaw === '-' ? -1 : parseInt(bRaw, 10));
        const C = parseInt(stdFracMatch[3], 10);
        const D = parseInt(stdFracMatch[4], 10);
        if (D !== 0) {
          return { type: 'complex_std_frac', A, B, C, D };
        }
      }

      // 11d. Product of Two Radicals: (±sqrt(A)) * (±sqrt(B)) (Ch 1.3 Q9–10, Pre-work Q19)
      const radProdMatch = s.replace(/\s+/g, '').match(/^\(?([+-]?)(?:sqrt|√)\(?([+-]?\d+)\)?\)?(?:\*|·|⋅)?\(?([+-]?)(?:sqrt|√)\(?([+-]?\d+)\)?\)?(?:\s*=\s*.*)?$/i);
      if (radProdMatch) {
        const s1 = radProdMatch[1] === '-' ? -1 : 1;
        const n1 = parseInt(radProdMatch[2], 10);
        const s2 = radProdMatch[3] === '-' ? -1 : 1;
        const n2 = parseInt(radProdMatch[4], 10);
        return { type: 'radical_prod', s1, n1, s2, n2 };
      }

      // 11e. Conjugate / Radical Binomial Product: (sqrt(A) + B)(sqrt(A) - B) or (sqrt(A) + i)(sqrt(A) - i) or (A + i*sqrt(B))(A - i*sqrt(B)) (Ch 1.3 Q16, Pre-work Q11–12)
      const radConjMatch = s.replace(/\s+/g, '').match(/^\((?:sqrt|√)\(?(\d+)\)?([+-])(?:(?:sqrt|√)\(?(\d+)\)?|(\d*)i)\)\*?(\((?:sqrt|√)\(?(\d+)\)?([+-])(?:(?:sqrt|√)\(?(\d+)\)?|(\d*)i)\))$/i);
      if (radConjMatch) {
        const aRad = parseInt(radConjMatch[1], 10);
        const isImag = radConjMatch[4] !== undefined;
        const bVal = isImag ? (radConjMatch[4] === '' ? 1 : parseInt(radConjMatch[4], 10)) : parseInt(radConjMatch[3], 10);
        const resVal = isImag ? (aRad + bVal * bVal) : (aRad - bVal);
        return { type: 'radical_conj', aRad, isImag, bVal, resVal };
      }
      const radConjMatch2 = s.replace(/\s+/g, '').match(/^\((\d+)([+-])(?:i\*?(?:sqrt|√)\(?(\d+)\)?|(?:sqrt|√)\(?(\d+)\)?i)\)\*?\(\1([+-])(?:i\*?(?:sqrt|√)\(?\3\)?|(?:sqrt|√)\(?\4\)?i)\)$/i);
      if (radConjMatch2) {
        const aVal = parseInt(radConjMatch2[1], 10);
        const bRad = parseInt(radConjMatch2[3] || radConjMatch2[4], 10);
        const resVal = aVal * aVal + bRad;
        return { type: 'radical_conj', aRad: aVal * aVal, isImag: true, bVal: Math.sqrt(bRad), resVal };
      }

      // 11f. Complex Binomial Squared: (a + bi)^2
      const cplxSq = s.match(/^\(\s*(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*\)\^2$/i);
      if (cplxSq) {
        const parseI = (raw) => {
          const r = raw.replace(/\s+/g, '');
          return (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        };
        const a1 = parseFloat(cplxSq[1]);
        const b1 = parseI(cplxSq[2]);
        return {
          type: 'complex_mult',
          a1, b1, a2: a1, b2: b1,
          isSquared: true
        };
      }

      // 11g. Complex Multiplication (with optional implied 1 before i): (a1 + b1 i)(a2 + b2 i) (Ch 1.3 Q14–15, Q19)
      const cplxMult = s.match(/\(\s*(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*\)\s*(?:\*\s*)?\(\s*(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*\)/i);
      if (cplxMult) {
        const parseI = (raw) => {
          const r = raw.replace(/\s+/g, '');
          return (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        };
        return {
          type: 'complex_mult',
          a1: parseFloat(cplxMult[1]),
          b1: parseI(cplxMult[2]),
          a2: parseFloat(cplxMult[3]),
          b2: parseI(cplxMult[4])
        };
      }

      // 11g. Complex Addition / Subtraction: (a1 + b1 i) ± (a2 + b2 i) (Pre-work 1.3 Q20)
      const cplxAddSub = s.match(/^\(\s*(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*\)\s*([+-])\s*\(\s*(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\s*\)(?:\s*=\s*.*)?$/i);
      if (cplxAddSub) {
        const parseI = (raw) => {
          const r = raw.replace(/\s+/g, '');
          return (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        };
        const sign = cplxAddSub[3] === '-' ? -1 : 1;
        return {
          type: 'complex_addsub',
          a1: parseFloat(cplxAddSub[1]),
          b1: parseI(cplxAddSub[2]),
          op: cplxAddSub[3],
          a2: parseFloat(cplxAddSub[4]),
          b2: parseI(cplxAddSub[5]),
          real: parseFloat(cplxAddSub[1]) + sign * parseFloat(cplxAddSub[4]),
          imag: parseI(cplxAddSub[2]) + sign * parseI(cplxAddSub[5])
        };
      }

      // 11h. Complex Division: (a1 + b1 i) / (a2 + b2 i)
      const cplxDiv = s.match(/^\(?(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\)?\s*\/\s*\(?(-?\d+(?:\.\d+)?)\s*([+-]\s*\d*(?:\.\d+)?)i\)?$/i);
      if (cplxDiv) {
        const parseI = (raw) => {
          const r = raw.replace(/\s+/g, '');
          return (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        };
        return {
          type: 'complex_div',
          a1: parseFloat(cplxDiv[1]),
          b1: parseI(cplxDiv[2]),
          a2: parseFloat(cplxDiv[3]),
          b2: parseI(cplxDiv[4])
        };
      }

      // 11i. Powers of i: i^n
      const powI = s.match(/^i\^\(?(-?\d+)\)?$/i);
      if (powI) {
        return { type: 'powers_i', n: parseInt(powI[1], 10) };
      }

      // 11j. Single Radical (with optional sign/multiplier or squared inside): ±k*sqrt(±n) or sqrt(n^2)
      const radSqMatch = s.replace(/\s+/g, '').match(/^([+-]?)(?:sqrt|√)\(?([+-]?\d+)\^2\)?$/i);
      if (radSqMatch) {
        const sign = radSqMatch[1] === '-' ? -1 : 1;
        const base = Math.abs(parseInt(radSqMatch[2], 10));
        return { type: 'radical', mult: sign, n: base * base };
      }
      const radMatch = s.replace(/\s+/g, '').match(/^([+-]?\d*)\*?(?:sqrt|√)\(?(-?\d+)\)?(?:\s*=\s*.*)?$/i);
      if (radMatch) {
        const mRaw = radMatch[1];
        const mult = (mRaw === '' || mRaw === '+') ? 1 : (mRaw === '-' ? -1 : parseInt(mRaw, 10));
        return { type: 'radical', mult, n: parseInt(radMatch[2], 10) };
      }

      // 11k. Complex / Real / Pure Imaginary Number Classification & Simple Exponent Eval (Ch 1.3 Q1–5, Pre-work Q1)
      const negPowMatch = s.replace(/\s+/g, '').match(/^(-)?\(?([+-]?\d+)\)?\^(\d+)$/);
      if (negPowMatch) {
        const outerNeg = negPowMatch[1] === '-' && !s.trim().startsWith('(');
        const base = parseFloat(negPowMatch[2]);
        const exp = parseInt(negPowMatch[3], 10);
        const val = outerNeg ? -Math.pow(base, exp) : Math.pow(base, exp);
        return { type: 'num_classify', raw: s, a: val, b: 0, isEvalPow: true, base, exp, outerNeg, val };
      }
      const classifyMatch = s.replace(/\s+/g, '').match(/^(?:(pi|π)|([+-]?\d+(?:\.\d+)?)|([+-]?\d*(?:\.\d+)?)i|([+-]?\d+(?:\.\d+)?)([+-]\d*(?:\.\d+)?)i)$/i);
      if (classifyMatch) {
        let a = 0, b = 0;
        if (classifyMatch[1]) {
          a = Math.PI; b = 0;
        } else if (classifyMatch[2]) {
          a = parseFloat(classifyMatch[2]); b = 0;
        } else if (classifyMatch[3] !== undefined) {
          const r = classifyMatch[3];
          b = (r === '' || r === '+') ? 1 : (r === '-' ? -1 : parseFloat(r));
        } else {
          a = parseFloat(classifyMatch[4]);
          const r = classifyMatch[5];
          b = (r === '+' || r === '') ? 1 : (r === '-' ? -1 : parseFloat(r));
        }
        return { type: 'num_classify', raw: s, a, b };
      }

      // 12. Quadratic Vertex Form: a(x - h)^2 + k
      let qvClean = s.replace(/^(?:[fghpqrFGHsSA]\([a-zA-Z]\)|y|s|A)\s*=\s*/i, '').trim();
      // Pre-evaluate leading fraction like (-1/4), -(1/4), -((1)/(4)), or -1/4
      qvClean = qvClean.replace(/^(?:([+-]?)\s*\(+\s*\(?([+-]?\d+(?:\.\d+)?)\)?\s*\/\s*\(?(\d+(?:\.\d+)?)\)?\s*\)+|([+-]?\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?))/g, (m, s1, n1, d1, n2, d2) => {
        if (n1 !== undefined) {
          const sign = s1 === '-' ? -1 : 1;
          return (sign * (parseFloat(n1) / parseFloat(d1))).toString();
        } else {
          return (parseFloat(n2) / parseFloat(d2)).toString();
        }
      });

      const quadVert = qvClean.match(/^([+-]?\d*\.?\d*)\s*\*?\s*\(\s*([a-zA-Z])\s*([+-])\s*(\d+(?:\.\d+)?)\s*\)\^2\s*([+-]\s*\d+(?:\.\d+)?)?(?:\s*=\s*0)?$/i);
      if (quadVert) {
        let aRaw = quadVert[1].trim();
        let a = 1;
        if (aRaw === '-' || aRaw === '') a = (aRaw === '-' ? -1 : 1);
        else a = parseFloat(aRaw);
        const variable = quadVert[2];
        const h = quadVert[3] === '-' ? parseFloat(quadVert[4]) : -parseFloat(quadVert[4]);
        const k = quadVert[5] ? parseFloat(quadVert[5].replace(/\s+/g, '')) : 0;
        return { type: 'quad_vertex', a, h, k, variable };
      }

      // 13. General Polynomial, Quadratic, or Linear Function / Equation (factored or expanded!)
      let cleanP = s.replace(/^(?:[fghpqrFGHsSA]\([a-zA-Z]\)|y|s|A)\s*=\s*/i, '').trim();
      if ((cleanP.includes('x') || cleanP.includes('t')) && !cleanP.includes('y') && !s.includes('|') && !s.includes(';')) {
        // Reject isolated single variable (e.g. "x") or pure function notation (e.g. "y = f(x)" or "f(x)")
        if (/^[a-zA-Z]$/.test(cleanP) || /^(?:y\s*=\s*)?[fghpqrFGHsSA]\([a-zA-Z]\)$/i.test(s)) {
          return null;
        }

        // Check if there is a top-level division by an expression containing x or t (which would be a rational function)
        const slashIdx = findTopLevelSlash(cleanP);
        let isRationalWithVar = false;
        if (slashIdx !== -1) {
          const den = cleanP.slice(slashIdx + 1);
          if (/[a-zA-Z]/.test(den)) isRationalWithVar = true;
        }

        if (!isRationalWithVar) {
          let rhsVal = 0;
          let isEq = false;
          if (cleanP.includes('=')) {
            const eqParts = cleanP.split('=');
            if (eqParts.length === 2) {
              const rCoeffs = parseAnyPolyCoeffs(eqParts[1].trim());
              const lCoeffs = parseAnyPolyCoeffs(eqParts[0].trim());
              if (lCoeffs.length >= 2 || rCoeffs.length >= 2) {
                const combined = subPolysJS(lCoeffs, rCoeffs);
                if (combined.length === 2) {
                  return { type: 'linear', m: combined[0], b: combined[1], isEq: true };
                }
                if (combined.length === 3) {
                  return { type: 'quadratic', a: combined[0], b: combined[1], c: combined[2], isEq: true };
                }
                if (combined.length > 3) {
                  return { type: 'polynomial', coeffs: combined, raw: cleanP };
                }
              }
            }
          }
          const coeffs = parseAnyPolyCoeffs(cleanP);
          if (coeffs.length === 2) {
            return { type: 'linear', m: coeffs[0], b: coeffs[1] - rhsVal, isEq };
          }
          if (coeffs.length >= 3) {
            coeffs[coeffs.length - 1] -= rhsVal;
            if (coeffs.length === 3) {
              return { type: 'quadratic', a: coeffs[0], b: coeffs[1], c: coeffs[2], isEq };
            }
            return { type: 'polynomial', coeffs, raw: cleanP };
          }
        }
      }

      return null;
    }

    function findTopLevelSlash(str) {
      let depth = 0;
      for (let i = 0; i < str.length; i++) {
        if (str[i] === '(') depth++;
        else if (str[i] === ')') depth = Math.max(0, depth - 1);
        else if ((str[i] === '/' || str[i] === '÷') && depth === 0) return i;
      }
      return -1;
    }

    function runToolOnParsed(parsed, raw) {
      if (!parsed) return null;

      if (parsed.type === 'two_points') {
        const { x1, y1, x2, y2, dx, dy, distSq, dist, mx, my, m, b } = parsed;
        const rad = simplifyRadical(Math.round(distSq));
        const slopeStr = isFinite(m) ? `${fracStr(dy, dx)} (≈ ${Number(m.toFixed(3))})` : 'Undefined (Vertical Line)';
        const lineStr = isFinite(m) ? `y = ${fracStr(dy, dx)}x ${b >= 0 ? '+ ' + Number(b.toFixed(2)) : '- ' + Math.abs(Number(b.toFixed(2)))}` : `x = ${x1}`;
        return {
          title: `📍 Two-Point Coordinate Geometry Solver (Ch 1.1 & 2.3): (${x1}, ${y1}) and (${x2}, ${y2})`,
          solverKey: 'points',
          params: { x1, y1, x2, y2 },
          outputVal: `Distance: <strong>${rad.str} ≈ ${dist.toFixed(2)}</strong> &nbsp;|&nbsp; Midpoint: <strong>(${Number(mx.toFixed(2))}, ${Number(my.toFixed(2))})</strong> &nbsp;|&nbsp; Slope: <strong>m = ${slopeStr}</strong> &nbsp;|&nbsp; Line: <strong>${lineStr}</strong>`,
          steps: [
            `1. Changes in Coordinates: Δx = ${x2} - (${x1}) = ${dx}, Δy = ${y2} - (${y1}) = ${dy}`,
            `2. Distance Formula: d = √[(Δx)² + (Δy)²] = √(${dx * dx} + ${dy * dy}) = √(${distSq}) = ${rad.str} ≈ ${dist.toFixed(2)}`,
            `3. Midpoint Formula: M = ((x₁+x₂)/2, (y₁+y₂)/2) = (${Number(mx.toFixed(2))}, ${Number(my.toFixed(2))})`,
            `4. Slope & Line Equation: m = Δy/Δx = ${slopeStr} → Line: ${lineStr}`,
            `5. Circle with Diameter P₁P₂: (x - ${Number(mx.toFixed(2))})² + (y - ${Number(my.toFixed(2))})² = ${Number((distSq / 4).toFixed(2))}`
          ]
        };
      }

      if (parsed.type === 'poly_points') {
        const { pts, zeros, anchor, prod, aFrac, factorsStr, factoredStr, basePoly } = parsed;
        const expandedTerms = basePoly.map((c, idx) => {
          const deg = basePoly.length - 1 - idx;
          const cfStr = fracStr(c * anchor.y * 1000, prod * 1000);
          return `${cfStr}${deg > 1 ? 'x^' + deg : (deg === 1 ? 'x' : '')}`;
        }).join(' + ').replace(/\+\s*-/g, '- ');
        return {
          title: `📈 Polynomial Equation from Points / Zeros Solver (Ch 3.2–3.3): ${pts.map(p => `${p.name}(${p.x}, ${p.y})`).join(', ')}`,
          solverKey: 'poly-zeros',
          params: { expr: factoredStr },
          outputVal: `Factored Form: <strong>f(x) = ${factoredStr}</strong> &nbsp;|&nbsp; Expanded: <strong>f(x) = ${expandedTerms}</strong>`,
          steps: [
            `1. Identify x-intercepts (Zeros where y = 0): ${zeros.map(z => `x = ${z.x} → factor (x ${z.x < 0 ? '+ ' + Math.abs(z.x) : '- ' + z.x})`).join(', ')}`,
            `2. Write general factored form: f(x) = a${factorsStr}`,
            `3. Substitute non-zero point ${anchor.name || 'D'}(${anchor.x}, ${anchor.y}): ${anchor.y} = a${zeros.map(z => `(${anchor.x} ${z.x < 0 ? '+ ' + Math.abs(z.x) : '- ' + z.x})`).join('')} = ${prod}a`,
            `4. Solve for leading stretch factor a: a = ${anchor.y}/${prod} = <strong>${aFrac}</strong>`,
            `5. Final Equation: <strong>f(x) = ${factoredStr}</strong> (or expanded: <strong>f(x) = ${expandedTerms}</strong>)`
          ]
        };
      }

      if (parsed.type === 'system_3x3') {
        const { parts, D, Dx, Dy, Dz, solStr } = parsed;
        return {
          title: `🔗 3×3 Linear System Solver (Ch 9.2): ${parts.join(' ; ')}`,
          solverKey: 'systems',
          params: { sys: parts.join('; ') },
          outputVal: `Ordered Triple Solution (x, y, z): <strong>${solStr}</strong>`,
          steps: [
            `1. 3×3 System Equations: (1) ${parts[0]} &nbsp;|&nbsp; (2) ${parts[1]} &nbsp;|&nbsp; (3) ${parts[2]}`,
            `2. Coefficient Matrix Determinant: D = ${Number(D.toFixed(3))}`,
            `3. Cramer's Determinants: Dx = ${Number(Dx.toFixed(3))}, Dy = ${Number(Dy.toFixed(3))}, Dz = ${Number(Dz.toFixed(3))}`,
            `4. Solution Triple: (x, y, z) = (Dx/D, Dy/D, Dz/D) = <strong>${solStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'system_2x2') {
        const { isLinear, eq1, eq2, a1, b1, c1, a2, b2, c2, det, solStr } = parsed;
        return {
          title: `🔗 ${isLinear ? '2×2 Linear' : 'Nonlinear'} System Solver (Ch 9.1 / 9.5): ${eq1}, ${eq2}`,
          solverKey: 'systems',
          params: { sys: `${eq1}, ${eq2}` },
          outputVal: `Intersection Solution: <strong>${solStr}</strong>`,
          steps: isLinear ? [
            `1. Equation 1: ${a1}x + (${b1})y = ${c1} &nbsp;|&nbsp; Equation 2: ${a2}x + (${b2})y = ${c2}`,
            `2. System Determinant D = (${a1})(${b2}) - (${a2})(${b1}) = ${det}`,
            `3. Cramer's Rule / Elimination: Dx = ${c1 * b2 - c2 * b1}, Dy = ${a1 * c2 - a2 * c1}`,
            `4. Intersection Point (x, y) = ${solStr} plotted on the coordinate plane below.`
          ] : [
            `1. Nonlinear System: (1) ${eq1} &nbsp;|&nbsp; (2) ${eq2}`,
            `2. Substitution / Elimination of nonlinear terms yields real intersection points: <strong>${solStr}</strong>`,
            `3. Both curves and their intersection points are plotted interactively below.`
          ]
        };
      }

      if (parsed.type === 'ellipse') {
        const { h, k, rx, ry } = parsed;
        const a = Math.max(rx, ry);
        const b = Math.min(rx, ry);
        const c = Math.sqrt(Math.max(0, a * a - b * b));
        const isHoriz = rx >= ry;
        const verts = isHoriz ? `(${(h - rx).toFixed(2)}, ${k}) and (${(h + rx).toFixed(2)}, ${k})` : `(${h}, ${(k - ry).toFixed(2)}) and (${h}, ${(k + ry).toFixed(2)})`;
        const coverts = isHoriz ? `(${h}, ${(k - ry).toFixed(2)}) and (${h}, ${(k + ry).toFixed(2)})` : `(${(h - rx).toFixed(2)}, ${k}) and (${(h + rx).toFixed(2)}, ${k})`;
        const foci = isHoriz ? `(${(h - c).toFixed(2)}, ${k}) and (${(h + c).toFixed(2)}, ${k})` : `(${h}, ${(k - c).toFixed(2)}) and (${h}, ${(k + c).toFixed(2)})`;
        return {
          title: `🪐 Ellipse Analyzer & Grapher (Ch 10.2): ${raw}`,
          solverKey: 'conics',
          params: { type: 'ellipse', h, k, a: rx, b: ry },
          outputVal: `Center: <strong>(${h}, ${k})</strong> &nbsp;|&nbsp; Vertices: <strong>${verts}</strong> &nbsp;|&nbsp; Foci: <strong>${foci}</strong>`,
          steps: [
            `1. Standard Form: (x - ${h})²/${(rx * rx).toFixed(2)} + (y - ${k})²/${(ry * ry).toFixed(2)} = 1`,
            `2. Major Axis: ${isHoriz ? 'Horizontal (along x)' : 'Vertical (along y)'} with semi-major a = ${a.toFixed(2)}, semi-minor b = ${b.toFixed(2)}`,
            `3. Vertices: ${verts} &nbsp;|&nbsp; Co-Vertices (Endpoints of Minor Axis): ${coverts}`,
            `4. Foci distance c = √(a² - b²) = √(${(a * a - b * b).toFixed(2)}) ≈ ${c.toFixed(2)} → Foci: ${foci}`,
            `5. Domain: [${(h - rx).toFixed(2)}, ${(h + rx).toFixed(2)}] &nbsp;|&nbsp; Range: [${(k - ry).toFixed(2)}, ${(k + ry).toFixed(2)}]`
          ]
        };
      }

      if (parsed.type === 'hyperbola') {
        const { h, k, a, b, transverse } = parsed;
        const c = Math.sqrt(a * a + b * b);
        const isHoriz = transverse !== 'vertical';
        const verts = isHoriz ? `(${(h - a).toFixed(2)}, ${k}) and (${(h + a).toFixed(2)}, ${k})` : `(${h}, ${(k - a).toFixed(2)}) and (${h}, ${(k + a).toFixed(2)})`;
        const foci = isHoriz ? `(${(h - c).toFixed(2)}, ${k}) and (${(h + c).toFixed(2)}, ${k})` : `(${h}, ${(k - c).toFixed(2)}) and (${h}, ${(k + c).toFixed(2)})`;
        const slopeFrac = isHoriz ? fracStr(b, a) : fracStr(a, b);
        const asympEq = `y - ${k} = ±(${slopeFrac})(x - ${h})`;
        return {
          title: `🪐 Hyperbola Analyzer & Grapher (Ch 10.3): ${raw}`,
          solverKey: 'conics',
          params: { type: isHoriz ? 'hyp-h' : 'hyp-v', h, k, a, b },
          outputVal: `Vertices: <strong>${verts}</strong> &nbsp;|&nbsp; Foci: <strong>${foci}</strong> &nbsp;|&nbsp; Asymptotes: <strong>${asympEq}</strong>`,
          steps: [
            `1. Transverse Axis: ${isHoriz ? 'Horizontal (opens Left & Right)' : 'Vertical (opens Up & Down)'} with Center (${h}, ${k})`,
            `2. Semi-transverse axis a = ${a.toFixed(2)}, semi-conjugate axis b = ${b.toFixed(2)}`,
            `3. Vertices: ${verts}`,
            `4. Foci distance c = √(a² + b²) = √(${(a * a + b * b).toFixed(2)}) ≈ ${c.toFixed(2)} → Foci: ${foci}`,
            `5. Asymptotes: ${asympEq} (plotted with central fundamental box below)`
          ]
        };
      }

      if (parsed.type === 'exp_func') {
        const { a, base, h, k, hasRhs, rhs, solX } = parsed;
        const bLabel = base === Math.E ? 'e' : base;
        return {
          title: `🚀 Exponential Function & Equation Analyzer (Ch 4.2 / 4.5): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'exp', a, b: Number(base.toFixed(4)), h, k, rhs: rhs !== undefined ? rhs : 0 },
          outputVal: `Horizontal Asymptote: <strong>y = ${k}</strong> &nbsp;|&nbsp; Domain: <strong>(-∞, ∞)</strong> &nbsp;|&nbsp; Range: <strong>${a > 0 ? `(${k}, ∞)` : `(-∞, ${k})`}</strong>${solX !== undefined ? ` &nbsp;|&nbsp; Solution: <strong>x ≈ ${solX.toFixed(4)}</strong>` : ''}`,
          steps: [
            `1. Base b = ${bLabel} (${base > 1 ? 'Exponential Growth' : 'Exponential Decay'}), Multiplier a = ${a}`,
            `2. Transformations from ${bLabel}^x: Horizontal shift h = ${h}, Vertical shift k = ${k}`,
            `3. Horizontal Asymptote: y = ${k}`,
            `4. Key Anchor Point: (${h}, ${(a + k).toFixed(2)}) and y-intercept (0, ${(a * Math.pow(base, -h) + k).toFixed(3)})`,
            hasRhs ? `5. Solving ${raw}: Isolate exponential term = ${((rhs - k) / a).toFixed(4)} → x ≈ ${solX !== undefined ? solX.toFixed(4) : 'No real solution'}` : `5. Domain: (-∞, ∞) | Range: ${a > 0 ? `(${k}, ∞)` : `(-∞, ${k})`}`
          ]
        };
      }

      if (parsed.type === 'log_func') {
        const { a, base, h, k, hasRhs, rhs, solX } = parsed;
        const bLabel = base === Math.E ? 'e (Natural Log ln)' : base;
        return {
          title: `🚀 Logarithmic Function & Equation Analyzer (Ch 4.3 / 4.5): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a, b: Number(base.toFixed(4)), h, k, rhs: rhs !== undefined ? rhs : 0 },
          outputVal: `Vertical Asymptote: <strong>x = ${h}</strong> &nbsp;|&nbsp; Domain: <strong>(${h}, ∞)</strong> &nbsp;|&nbsp; Range: <strong>(-∞, ∞)</strong>${solX !== undefined ? ` &nbsp;|&nbsp; Solution: <strong>x = ${solX.toFixed(4)}</strong>` : ''}`,
          steps: [
            `1. Logarithm Base b = ${bLabel}`,
            `2. Domain Restriction: Inside argument x - ${h} > 0 → Domain is (${h}, ∞)`,
            `3. Vertical Asymptote: x = ${h} &nbsp;|&nbsp; Range: (-∞, ∞)`,
            `4. Key Anchor Points: (${(h + 1).toFixed(2)}, ${k}) and (${(h + base).toFixed(2)}, ${(a + k).toFixed(2)})`,
            hasRhs ? `5. Exponential Conversion: x - ${h} = ${base}^(${((rhs - k) / a).toFixed(3)}) → x = ${solX.toFixed(4)}` : `5. Plotted below with Vertical Asymptote x = ${h}.`
          ]
        };
      }

      if (parsed.type === 'sqrt_func') {
        const { a, inside, lin, k } = parsed;
        const vx = -lin.b / lin.m;
        const domMin = lin.m > 0 ? vx : -Infinity;
        return {
          title: `🌿 Square Root Function Analyzer: f(x) = ${a === 1 ? '' : a}√(${inside})${k ? (k > 0 ? ' + ' + k : ' - ' + Math.abs(k)) : ''}`,
          solverKey: 'radical',
          params: { n: Math.round(lin.b * lin.b) },
          outputVal: `Domain: <strong>${lin.m > 0 ? `[${Number(vx.toFixed(2))}, ∞)` : `(-∞, ${Number(vx.toFixed(2))}]`}</strong> &nbsp;|&nbsp; Range: <strong>${a > 0 ? `[${Number(k.toFixed(2))}, ∞)` : `(-∞, ${Number(k.toFixed(2))}]`}</strong> &nbsp;|&nbsp; Start point: <strong>(${Number(vx.toFixed(2))}, ${Number(k.toFixed(2))})</strong>`,
          steps: [
            `1. Radical functions require the inside ≥ 0: ${inside} ≥ 0 → x ${lin.m > 0 ? '≥' : '≤'} ${Number(vx.toFixed(3))}`,
            `2. Domain: ${lin.m > 0 ? `[${Number(vx.toFixed(3))}, ∞)` : `(-∞, ${Number(vx.toFixed(3))}]`}`,
            `3. The square root outputs ≥ 0, so Range: ${a > 0 ? `[${Number(k.toFixed(3))}, ∞)` : `(-∞, ${Number(k.toFixed(3))}]`} (a = ${a})`,
            `4. Inverse: f⁻¹(x) = ((x ${k >= 0 ? '- ' + k : '+ ' + Math.abs(k)})/${a})² ${lin.m > 0 ? 'with x ≥ ' + Number(k.toFixed(2)) : ''}`
          ]
        };
      }

      if (parsed.type === 'abs_func') {
        const { a, inside, lin, d } = parsed;
        const vx = -lin.b / lin.m;
        return {
          title: `📏 Absolute Value Function Analyzer (Ch 1.6): f(x) = ${a === 1 ? '' : a}|${inside}|${d ? (d > 0 ? ' + ' + d : ' - ' + Math.abs(d)) : ''}`,
          solverKey: 'abs',
          params: { a, b: lin.b, op: '=', c: 0 },
          outputVal: `Vertex: <strong>(${Number(vx.toFixed(3))}, ${Number(d.toFixed(3))})</strong> &nbsp;|&nbsp; Axis: <strong>x = ${Number(vx.toFixed(3))}</strong> &nbsp;|&nbsp; V-shape opens: <strong>${a > 0 ? 'Upward (Min)' : 'Downward (Max)'}</strong>`,
          steps: [
            `1. Vertex form: f(x) = a|x − h| + k with vertex (h, k) → here a = ${a}, h = ${Number(vx.toFixed(3))}, k = ${d}`,
            `2. Axis of symmetry: x = ${Number(vx.toFixed(3))}`,
            `3. ${a > 0 ? 'a > 0 → opens UPWARD → vertex is a MINIMUM' : 'a < 0 → opens DOWNWARD → vertex is a MAXIMUM'}`,
            `4. Range: ${a > 0 ? `[${Number(d.toFixed(3))}, ∞)` : `(-∞, ${Number(d.toFixed(3))}]`}`,
            `5. Horizontal line test: every horizontal line above y = ${Number(d.toFixed(2))} crosses the V twice → NOT one-to-one`
          ]
        };
      }

      if (parsed.type === 'exp_eq') {
        const xStr = parsed.xStr;
        return {
          title: `🚀 Exponential Equation Solver (common-base / logarithmic): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'exp', a: 1, b: 2, h: 0, k: 0, rhs: 0 },
          outputVal: `Solution: <strong>x = ${xStr}</strong>`,
          steps: [
            `1. Both sides are powers: ${parsed.lhs} = ${parsed.rhs}`,
            `2. Take the natural log of both sides: ln(${parsed.lhs}) = ln(${parsed.rhs})`,
            `3. Power rule brings exponents down: (${Number(parsed.b1.toFixed(4))})·(exponent of left) = (${Number(parsed.b2.toFixed(4))})·(exponent of right)`,
            `4. Expand exponents and collect x terms → linear equation in x`,
            `5. Solve: <strong>x = ${xStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'log_eq2') {
        const rootsStr = (parsed.roots || []).map(r => rationalizeVal(r)).join(', ');
        return {
          title: `🚀 Logarithmic Equation Solver (condense + quadratic): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a: 1, b: 2, h: 0, k: 0 },
          outputVal: `Solution set: <strong>{${rootsStr}}</strong>${(parsed.roots || []).length > 1 ? ' (after domain check)' : ''}`,
          steps: [
            `1. Condense the logs: ${parsed.argExpr} = base^rhs form`,
            `2. Expand: quadratic in x`,
            `3. Solve the quadratic → candidate roots: <strong>${(parsed.roots || []).map(r => rationalizeVal(r)).join(', ')}</strong>`,
            `4. Check the log domain (arguments > 0) and keep valid roots`,
            `5. Verified solution set: <strong>{${rootsStr}}</strong>`
          ]
        };
      }

      if (parsed.type === 'log_expr') {
        const dec = (v) => Number(v.toFixed(4));
        const steps = [];
        if (parsed.mode === 'eval') {
          steps.push(`1. Identify the base and argument of each logarithm.`);
          steps.push(`2. Change of base: log_b(A) = ln(A) / ln(b).`);
          steps.push(`3. Evaluate each term and combine.`);
          return {
            title: `🚀 Logarithm Expression Evaluator (Ch 4.3-4.4): ${raw}`,
            solverKey: 'explog',
            params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
            outputVal: `Exact / 4-Decimal Value: <strong>${parsed.value}</strong>`,
            steps
          };
        }
        if (parsed.mode === 'equation') {
          steps.push(`1. Evaluate the log side(s) numerically (change of base).`);
          steps.push(`2. Set the evaluated sides equal and solve the resulting linear equation.`);
          return {
            title: `🚀 Logarithmic Equation (numeric) Solver (Ch 4.5): ${raw}`,
            solverKey: 'explog',
            params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
            outputVal: `Solution: <strong>${parsed.value}</strong>`,
            steps
          };
        }
        // expand mode
        const sh = parsed.shape;
        const lines = [];
        sh.lhs.terms.forEach(function (t) {
          if (t.kind === 'const') { lines.push(`${t.v}`); return; }
          const bb = t.base === Math.E ? 'e' : t.base;
          const flat = t.argRaw.replace(/[()]/g, ' ').replace(/\s+/g, ' ').trim();
          const slash = t.argRaw.indexOf('/');
          let argNote = '';
          if (slash >= 0) {
            argNote = ` (quotient: log of a quotient = difference of logs)`;
          }
          lines.push(`${t.coef === 1 ? '' : t.coef + '·'}log_${bb}(${flat})${argNote}`);
        });
        (sh.rhs ? sh.rhs.terms : []).forEach(function (t) {
          if (t.kind !== 'log') return;
          const bb = t.base === Math.E ? 'e' : t.base;
          lines.push(`= ${t.coef === 1 ? '' : t.coef + '·'}log_${bb}(${t.argRaw.replace(/[()]/g, ' ').replace(/\s+/g, ' ').trim()})`);
        });
        steps.push(`1. Product Rule: log_b(M·N) = log_b M + log_b N.`);
        steps.push(`2. Quotient Rule: log_b(M/N) = log_b M − log_b N.`);
        steps.push(`3. Power Rule: log_b(N^k) = k·log_b N.`);
        steps.push(`4. Structural expansion of each term:`);
        steps.push(`   ${lines.join('<br>&nbsp;&nbsp;&nbsp;')}`);
        return {
          title: `🚀 Logarithm Property Expansion (Ch 4.3): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a: 1, b: 10, h: 0, k: 0 },
          outputVal: `Expression uses Product / Quotient / Power Rules — see expanded form in steps.`,
          steps
        };
      }

      if (parsed.type === 'sign_rule') {
        const { numSign, denSign, resSign, ruleDesc } = parsed;
        return {
          title: `📐 Quotient Sign Rule Analyzer (Ch 3.6): ${raw}`,
          solverKey: 'ineq',
          params: { expr: raw },
          outputVal: `Result Sign: <strong>${resSign}</strong>`,
          steps: [
            `1. Division Rule for Signs: ${ruleDesc}`,
            `2. Numerator is ${numSign}, Denominator is ${denSign}`,
            `3. Sign of Quotient: (${numSign === 'Negative' ? '−' : '+'}) ÷ (${denSign === 'Negative' ? '−' : '+'}) = <strong>${resSign === 'Positive' ? '+ (Positive)' : '− (Negative)'}</strong>`
          ]
        };
      }

      if (parsed.type === 'poly_ineq' || parsed.type === 'rat_ineq') {
        const isTime = (parsed.variable === 't' || /[-0-9]t\^/i.test(raw));
        const numC = parsed.type === 'poly_ineq' ? parsed.coeffs : parsed.numCoeffs;
        const denC = parsed.type === 'poly_ineq' ? [1] : parsed.denCoeffs;
        const sc = solveSignChartInequalityJS(numC, denC, parsed.op);
        const chartSummary = sc.chartRows.map(r => `Interval ${r.interval}: test ${isTime ? 't' : 'x'} = ${r.testX} → val = ${r.val} (${r.sign}) ${r.satisfies ? '✅ KEEP' : '❌'}`).join('<br>');
        
        let outStr = `Interval Notation: <strong>${sc.intervalStr}</strong>`;
        if (isTime && sc.intervals.length === 1 && isFinite(sc.intervals[0].from) && isFinite(sc.intervals[0].to)) {
          const fDec = Number(sc.intervals[0].from.toFixed(2));
          const tDec = Number(sc.intervals[0].to.toFixed(2));
          outStr = `Time Period: <strong>Between (and inclusive of) ${fDec} sec and ${tDec} sec</strong> &nbsp;|&nbsp; Interval: <strong>${sc.intervalStr}</strong>`;
        }
        if (sc.isolatedPoints && sc.isolatedPoints.length > 0) {
          outStr += ` &nbsp;|&nbsp; Isolated Point(s): <strong>{${sc.isolatedPoints.map(formatEndpoint).join(', ')}}</strong>`;
        }

        return {
          title: `⚖️ ${parsed.type === 'poly_ineq' ? (isTime ? 'Projectile Height Inequality' : 'Polynomial Inequality') : 'Rational Inequality'} Sign Chart Solver (Ch 3.6): ${raw}`,
          solverKey: 'ineq',
          params: { expr: raw },
          outputVal: outStr,
          steps: [
            `1. Standardize Inequality (RHS = 0): Numerator P(${isTime ? 't' : 'x'}) = ${formatPolyCoeffs(numC)}${parsed.type === 'rat_ineq' ? `, Denominator Q(x) = ${formatPolyCoeffs(denC)}` : ''} ${parsed.op} 0`,
            `2. Boundary Critical Zeros (Numerator = 0): ${sc.numRoots.length ? sc.numRoots.map(formatEndpoint).join(', ') : 'None'}${parsed.type === 'rat_ineq' ? ` &nbsp;|&nbsp; Undefined Poles (Denominator = 0, ALWAYS open parenthesis): ${sc.denRoots.length ? sc.denRoots.map(formatEndpoint).join(', ') : 'None'}` : ''}`,
            `3. Sign Chart Test Intervals:<br>${chartSummary}`,
            `4. Solution Set: <strong>${sc.intervalStr}</strong>${isTime && sc.intervals.length === 1 ? ` → Ball is at least target height between ${formatEndpoint(sc.intervals[0].from)} and ${formatEndpoint(sc.intervals[0].to)} seconds.` : ''}`
          ]
        };
      }

      if (parsed.type === 'abs_double') {
        const { a1, b1, a2, b2, sols } = parsed;
        return {
          title: `📏 Double Absolute Value Equation Solver (Ch 1.6): ${raw}`,
          solverKey: 'abs',
          params: { a: a1, b: b1, op: '=', c: 0 },
          outputVal: `Solution Set: <strong>{${sols.map(v => fracStr(v * 1000, 1000)).join(', ')}}</strong>`,
          steps: [
            `1. Rule: |A| = |B| splits into two linear equations: A = B  OR  A = -B`,
            `2. Case 1: ${a1}x + (${b1}) = ${a2}x + (${b2}) → (${a1 - a2})x = ${b2 - b1} → x = ${sols[0] !== undefined ? sols[0].toFixed(3) : 'None'}`,
            `3. Case 2: ${a1}x + (${b1}) = -(${a2}x + (${b2})) → (${a1 + a2})x = ${-b2 - b1} → x = ${sols[1] !== undefined ? sols[1].toFixed(3) : 'None'}`
          ]
        };
      }

      if (parsed.type === 'quad_vertex') {
        const { a, h, k } = parsed;
        const b = -2 * a * h;
        const c = a * h * h + k;
        const opensUp = a > 0;
        const rangeStr = opensUp ? `[${Number(k.toFixed(3))}, ∞)` : `(-∞, ${Number(k.toFixed(3))}]`;
        const incStr = opensUp ? `(${Number(h.toFixed(3))}, ∞)` : `(-∞, ${Number(h.toFixed(3))})`;
        const decStr = opensUp ? `(-∞, ${Number(h.toFixed(3))})` : `(${Number(h.toFixed(3))}, ∞)`;
        const xIntStr = (-k / a >= 0) ? (Math.sqrt(-k / a) === 0 ? `(${Number(h.toFixed(2))}, 0)` : `(${Number((h - Math.sqrt(-k / a)).toFixed(2))}, 0), (${Number((h + Math.sqrt(-k / a)).toFixed(2))}, 0)`) : 'None (no real x-intercepts)';
        return {
          title: `📈 Parabola Vertex Form Analyzer (Ch 3.1): f(x) = ${a}(x - ${h})² + ${k}`,
          solverKey: 'quadratic',
          params: { a, b, c },
          outputVal: `Vertex: <strong>(${h}, ${k})</strong> &nbsp;|&nbsp; Axis: <strong>x = ${h}</strong> &nbsp;|&nbsp; Range: <strong>${rangeStr}</strong> &nbsp;|&nbsp; Opens: <strong>${opensUp ? 'Upward (Min)' : 'Downward (Max)'}</strong>`,
          steps: [
            `1. Vertex Form f(x) = a(x - h)² + k gives Vertex (h, k) = <strong>(${h}, ${k})</strong>`,
            `2. Axis of Symmetry: vertical line <strong>x = ${h}</strong>`,
            `3. Leading coefficient a = ${a} ${opensUp ? '> 0 → Opens UPWARD (vertex is minimum)' : '< 0 → Opens DOWNWARD (vertex is maximum)'}`,
            `4. Domain: <strong>(-∞, ∞)</strong> &nbsp;|&nbsp; Range: <strong>${rangeStr}</strong>`,
            `5. Intervals: Increasing on <strong>${incStr}</strong> &nbsp;|&nbsp; Decreasing on <strong>${decStr}</strong>`,
            `6. Intercepts: y-intercept (0, ${Number(c.toFixed(2))}) &nbsp;|&nbsp; x-intercepts: ${xIntStr}`
          ]
        };
      }

      if (parsed.type === 'polynomial') {
        const coeffs = parsed.coeffs;
        const deg = coeffs.length - 1;
        const lead = coeffs[0];
        const constVal = coeffs[coeffs.length - 1];
        const roots = findRationalRootsJS(coeffs);
        const counts = {};
        roots.forEach(r => {
          const k = Number(r.toFixed(4));
          counts[k] = (counts[k] || 0) + 1;
        });

        const sortedKeys = Object.keys(counts).map(Number).sort((a, b) => a - b);
        const factorParts = [];
        sortedKeys.forEach(r => {
          const m = counts[r];
          const expStr = m > 1 ? `^${m}` : '';
          if (Math.abs(r) < 1e-9) {
            factorParts.push(m > 1 ? `x^${m}` : 'x');
          } else if (r > 0) {
            factorParts.push(`(x - ${Number(r.toFixed(3))})${expStr}`);
          } else {
            factorParts.push(`(x + ${Number(Math.abs(r).toFixed(3))})${expStr}`);
          }
        });

        // Put 'x' or 'x^k' first if present
        factorParts.sort((a, b) => (a.startsWith('x') ? -1 : b.startsWith('x') ? 1 : 0));

        let leadPrefix = '';
        if (Math.abs(lead - 1) < 1e-6) leadPrefix = '';
        else if (Math.abs(lead + 1) < 1e-6) leadPrefix = '-';
        else leadPrefix = `${Number(lead.toFixed(3))}`;

        const factoredStr = factorParts.length > 0 ? (leadPrefix + factorParts.join('')) : `${formatPolyCoeffs(coeffs)}`;

        const xIntsVals = sortedKeys.map(k => Number(k.toFixed(3))).join(', ') || 'None';
        const xIntsPoints = sortedKeys.map(k => `(${Number(k.toFixed(3))}, 0)`).join(', ') || 'None';
        const yIntPoint = `(0, ${Number(constVal.toFixed(3))})`;

        const crossZeros = sortedKeys.filter(k => counts[k] % 2 !== 0).map(k => Number(k.toFixed(3))).join(', ') || 'None';
        const touchZeros = sortedKeys.filter(k => counts[k] % 2 === 0).map(k => Number(k.toFixed(3))).join(', ') || 'None';

        const zerosDesc = sortedKeys.map(k => {
          const m = counts[k];
          return `x = ${Number(k.toFixed(3))} (mult ${m}: ${m % 2 !== 0 ? 'crosses' : 'touches & turns'})`;
        }).join(' &nbsp;•&nbsp; ') || 'No rational zeros found';

        const proto = (deg % 2 === 0)
          ? (lead > 0 ? 'Rises left & right (↖ ↗)' : 'Falls left & right (↙ ↘)')
          : (lead > 0 ? 'Falls left, rises right (↙ ↗)' : 'Rises left, falls right (↖ ↘)');

        return {
          title: `📈 Polynomial Function Analyzer & Factorer (Ch 3.3–3.4): f(x) = ${raw}`,
          solverKey: 'poly-zeros',
          params: { expr: raw },
          outputVal: `Factored Form: <strong>${factoredStr}</strong> &nbsp;|&nbsp; Intercepts: <strong>x = ${xIntsVals}</strong>, <strong>y = ${Number(constVal.toFixed(3))}</strong> &nbsp;|&nbsp; Zeros: <strong>${zerosDesc}</strong>`,
          steps: [
            `1. Factored Form: <strong>f(x) = ${factoredStr}</strong> (or equivalent factor ordering)`,
            `2. x-intercepts: <strong>${xIntsVals}</strong> &nbsp;[Points: ${xIntsPoints}] &nbsp;|&nbsp; y-intercept: <strong>${yIntPoint}</strong>`,
            `3. Zeros & Multiplicities: Crosses x-axis at x = <strong>${crossZeros}</strong> (odd multiplicity: 1); Touches and turns around at x = <strong>${touchZeros}</strong> (even multiplicity: 2)`,
            `4. End Behavior: <strong>${proto}</strong> (Degree: ${deg}, Leading Coeff: ${lead}) &nbsp;|&nbsp; Max turning points: ${deg - 1}`,
            `5. Expanded Form: f(x) = ${formatPolyCoeffs(coeffs)}`
          ]
        };
      }

      if (parsed.type === 'rational') {
        const graphData = buildRationalGraphData(parsed.numCoeffs, parsed.denCoeffs, raw);
        const vertStr = graphData.vertAsymptotes && graphData.vertAsymptotes.length > 0 ? graphData.vertAsymptotes.map(v => 'x = ' + v.label).join(', ') : 'None';
        const horizStr = graphData.horizAsymptote ? graphData.horizAsymptote.eq : (graphData.slantAsymptote ? graphData.slantAsymptote.eq : 'None');
        const holesStr = graphData.points.filter(p => p.type === 'hole').map(p => p.label).join(', ') || 'None';

        // Compute Domain from all roots of denominator (both VAs and holes)
        const denRoots = findRationalRootsJS(parsed.denCoeffs);
        const allDenExcl = Array.from(new Set(denRoots.map(r => Number(r.toFixed(3))))).sort((a, b) => a - b);
        let domainInterval = '(-∞, ∞)';
        let domainSetBuilder = '{x | x is all real numbers}';
        if (allDenExcl.length > 0) {
          domainSetBuilder = `{x | x ≠ ${allDenExcl.join(', ')}}`;
          const intervals = [];
          for (let i = 0; i <= allDenExcl.length; i++) {
            const left = i === 0 ? '-∞' : allDenExcl[i - 1];
            const right = i === allDenExcl.length ? '∞' : allDenExcl[i];
            intervals.push(`(${left}, ${right})`);
          }
          domainInterval = intervals.join(' ∪ ');
        }

        const distinctXInts = Array.from(new Set(graphData.points.filter(p => p.y === 0 && p.type !== 'hole').map(p => p.label))).join(', ') || 'None';
        const yIntPoint = graphData.points.find(p => p.x === 0 && p.type !== 'hole')?.label || 'None';

        return {
          title: `📉 Rational Function Analyzer & Grapher (Ch 3.5): f(x) = ${raw}`,
          solverKey: 'rational',
          params: { num: parsed.numStr, den: parsed.denStr },
          outputVal: `Domain: <strong>${domainInterval}</strong> &nbsp;|&nbsp; VA: <strong>${vertStr}</strong> &nbsp;|&nbsp; End Behavior: <strong>${horizStr}</strong> &nbsp;|&nbsp; Holes: <strong>${holesStr}</strong>`,
          steps: [
            `1. Domain: <strong>${domainInterval}</strong> &nbsp;(Set notation: <code>${domainSetBuilder}</code>)`,
            `2. Removable Discontinuities (Holes): <strong>${holesStr}</strong>`,
            `3. Vertical Asymptotes (non-canceled denominator roots): <strong>${vertStr}</strong>`,
            `4. Horizontal / Oblique (Slant) Asymptote: <strong>${horizStr}</strong>`,
            `5. Intercepts: x-intercepts: <strong>${distinctXInts}</strong> &nbsp;|&nbsp; y-intercept: <strong>${yIntPoint}</strong>`,
            `6. Expanded Form: P(x) = ${formatPolyCoeffs(parsed.numCoeffs)} &nbsp;|&nbsp; Q(x) = ${formatPolyCoeffs(parsed.denCoeffs)}`
          ]
        };
      }

      if (parsed.type === 'synthetic') {
        const coeffs = parseAnyPolyCoeffs(parsed.poly);
        const c = parsed.c;
        let resRow = [coeffs[0]];
        for (let i = 1; i < coeffs.length; i++) {
          resRow.push(coeffs[i] + resRow[resRow.length - 1] * c);
        }
        const qCoeffs = resRow.slice(0, -1);
        const rem = resRow[resRow.length - 1];
        const qStr = formatPolyCoeffs(qCoeffs);

        let extraZerosStep = '';
        let extraZerosVal = '';
        if (Math.abs(rem) < 1e-7 && qCoeffs.length === 3) {
          const [qa, qb, qc] = qCoeffs;
          const disc = qb * qb - 4 * qa * qc;
          const rad = simplifyRadical(disc);
          if (disc >= 0) {
            const r1 = (-qb + Math.sqrt(disc)) / (2 * qa);
            const r2 = (-qb - Math.sqrt(disc)) / (2 * qa);
            extraZerosVal = ` &nbsp;|&nbsp; All Zeros: <strong>x = ${c}, ${Number(r1.toFixed(3))}, ${Number(r2.toFixed(3))}</strong>`;
            extraZerosStep = `6. Depressed Quadratic q(x) = ${qStr} = 0 → Remaining Zeros: x = ${Number(r1.toFixed(3))}, ${Number(r2.toFixed(3))} (Exact: [${-qb} ± ${rad.str}]/${2 * qa})`;
          } else {
            extraZerosVal = ` &nbsp;|&nbsp; All Zeros: <strong>x = ${c}, [${-qb} ± ${rad.str}]/${2 * qa}</strong>`;
            extraZerosStep = `6. Depressed Quadratic q(x) = ${qStr} = 0 → Complex Zeros: x = [${-qb} ± ${rad.str}]/${2 * qa}`;
          }
        }

        const stepsArr = [
          `1. Divisor root in synthetic tableau: c = ${c}`,
          `2. Polynomial coefficients: [${coeffs.join(', ')}]`,
          `3. Division Algorithm: P(x) = (x ${c >= 0 ? '- ' + c : '+ ' + Math.abs(c)})(${qStr}) + (${rem})`,
          `4. Remainder Theorem: P(${c}) = ${rem}`,
          `5. Factor Theorem: Is x = ${c} a zero of P(x)? <strong>${Math.abs(rem) < 1e-7 ? 'YES (Remainder is 0)' : 'NO'}</strong>`
        ];
        if (extraZerosStep) stepsArr.push(extraZerosStep);

        return {
          title: `➗ Synthetic Division & Factor Theorem Solver: (${parsed.poly}) ÷ (x ${c >= 0 ? '- ' + c : '+ ' + Math.abs(c)})`,
          solverKey: 'synthetic',
          params: { coeffs: coeffs.join(' '), c },
          outputVal: `Quotient q(x) = <strong>${qStr}</strong> &nbsp;|&nbsp; Remainder R = <strong>${rem}</strong>${extraZerosVal}`,
          steps: stepsArr
        };
      }

      if (parsed.type === 'log_eval') {
        const { a, base, argRaw, argVal, resultVal } = parsed;
        const bStr = base === Math.E ? 'e' : base;
        return {
          title: `🚀 Logarithm Change-of-Base Evaluator (Ch 4.3–4.4): ${raw}`,
          solverKey: 'explog',
          params: { mode: 'log', a, b: Number(base.toFixed(4)), h: 0, k: 0 },
          outputVal: `Exact / 4-Decimal Value: <strong>${Number(resultVal.toFixed(4))}</strong>`,
          steps: [
            `1. Logarithm Base b = ${bStr}, Argument A = ${argRaw} (${Number(argVal.toFixed(4))}), Multiplier a = ${a}`,
            `2. Change-of-Base Formula: log_${bStr}(${argRaw}) = ln(${argRaw}) / ln(${bStr}) = ${Math.log(argVal).toFixed(5)} / ${Math.log(base).toFixed(5)}`,
            `3. Evaluated Result: <strong>${Number(resultVal.toFixed(4))}</strong>`
          ]
        };
      }

      if (parsed.type === 'linear') {
        const { m, b, isEq } = parsed;
        const rootX = Math.abs(m) > 1e-9 ? -b / m : NaN;
        const rootFrac = Math.abs(m) > 1e-9 ? fracStr(-b * 1000, m * 1000) : 'None';
        const invStr = Math.abs(m) > 1e-9 ? `f⁻¹(x) = (x ${b >= 0 ? '- ' + b : '+ ' + Math.abs(b)}) / ${m}` : 'No inverse (constant)';
        return {
          title: `📏 Linear Equation, Slope & Inverse Solver (Ch 1.2 / 2.3 / 2.7): ${raw}`,
          solverKey: 'points',
          params: {},
          outputVal: isEq
            ? `Solution: <strong>x = ${rootFrac} (≈ ${Number(rootX.toFixed(3))})</strong>`
            : `x-intercept / Zero: <strong>(${Number(rootX.toFixed(3))}, 0)</strong> &nbsp;|&nbsp; y-intercept: <strong>(0, ${b})</strong> &nbsp;|&nbsp; Slope: <strong>m = ${m}</strong> &nbsp;|&nbsp; Inverse: <strong>${invStr}</strong>`,
          steps: [
            `1. Linear Form: ${m}x + (${b}) ${isEq ? '= 0' : '= y'} (Slope m = ${m}, y-intercept b = ${b})`,
            `2. Solve for x-intercept / root: ${m}x = ${-b} → x = ${rootFrac} (≈ ${Number(rootX.toFixed(4))})`,
            `3. Inverse Function (swap x and y): x = ${m}y + (${b}) → <strong>${invStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'quadratic') {
        const { a, b, c } = parsed;
        const vx = -b / (2 * a);
        const vy = a * vx * vx + b * vx + c;
        const disc = b * b - 4 * a * c;
        const rad = simplifyRadical(disc);

        let rootsStr = "";
        if (Math.abs(b) < 1e-9 && a === 1) {
          // Pure Square Root Property form: x^2 = -c (Ch 1.3 Q6–7)
          const rhs = -c;
          const rSim = simplifyRadical(rhs);
          rootsStr = `{ -${rSim.str}, ${rSim.str} }  (or ${rSim.str}, -${rSim.str})`;
        } else if (disc > 0) {
          const r1 = (-b + Math.sqrt(disc)) / (2 * a);
          const r2 = (-b - Math.sqrt(disc)) / (2 * a);
          rootsStr = `x = ${Number(r1.toFixed(3))}, x = ${Number(r2.toFixed(3))} (Exact: [${-b} ± ${rad.str}]/${2 * a})`;
        } else if (disc === 0) {
          rootsStr = `x = ${Number(vx.toFixed(3))} (double root)`;
        } else {
          rootsStr = `x = [${-b} ± ${rad.str}] / ${2 * a} (complex conjugate roots)`;
        }

        return {
          title: `📈 Quadratic & Square Root Property Solver: f(x) = ${a}x² + (${b})x + (${c})`,
          solverKey: 'quadratic',
          params: { a, b, c },
          outputVal: `Solution / Roots: <strong>${rootsStr}</strong> &nbsp;|&nbsp; Vertex: <strong>(${Number(vx.toFixed(3))}, ${Number(vy.toFixed(3))})</strong>`,
          steps: [
            Math.abs(b) < 1e-9 ? `1. Square Root Property: x² = ${-c} → x = ±√(${-c}) = ±${simplifyRadical(-c).str}` : `1. Axis of Symmetry: x = -b/(2a) = ${Number(vx.toFixed(3))}`,
            `2. Parabola opens: ${a > 0 ? 'Upward (Minimum value ' + Number(vy.toFixed(3)) + ' at vertex)' : 'Downward (Maximum value ' + Number(vy.toFixed(3)) + ' at vertex)'}`,
            `3. Discriminant Δ = b² - 4ac = ${disc.toFixed(2)} (${disc > 0 ? '2 Real Roots' : disc === 0 ? '1 Real Root' : '2 Complex Roots'})`,
            `4. Vertex Form: f(x) = ${a}(x - ${Number(vx.toFixed(3))})² + (${Number(vy.toFixed(3))})`,
            `5. Domain: (-∞, ∞) &nbsp;|&nbsp; Range: ${a > 0 ? `[${Number(vy.toFixed(3))}, ∞)` : `(-∞, ${Number(vy.toFixed(3))}]`}`
          ]
        };
      }

      if (parsed.type === 'abs') {
        const { a, b, op, c, origK } = parsed;
        const exprInside = b === 0
          ? `${a === 1 ? 'x' : a + 'x'}`
          : (b > 0 ? `${a === 1 ? 'x' : a + 'x'} + ${b}` : `${a === 1 ? 'x' : a + 'x'} - ${Math.abs(b)}`);

        let rewriteForm = "";
        let intervalAns = "";
        let ruleSummary = "";
        const steps = [];

        if (origK && origK !== 1) {
          steps.push(`1. Isolate the absolute value expression by dividing both sides by ${origK}: |${exprInside}| ${op} ${c}`);
        }

        if (c < 0) {
          if (op === '<' || op === '<=' || op === '=') {
            intervalAns = "∅ (No Solution / Empty Set)";
            rewriteForm = "None (Absolute value cannot be negative)";
            ruleSummary = "❌ An absolute value |u| is always non-negative (≥ 0) and can never be less than a negative number.";
            steps.push(`Since |${exprInside}| ≥ 0 for all real numbers, it can never be ${op} ${c}.`);
            steps.push(`Therefore, the solution set is the empty set: <strong>∅</strong> (Choice B or C in MyMathLab).`);
          } else {
            intervalAns = "(-∞, ∞) (All Real Numbers)";
            rewriteForm = "All real numbers";
            ruleSummary = "✅ An absolute value |u| is always non-negative (≥ 0), which is always greater than any negative number.";
            steps.push(`Since |${exprInside}| ≥ 0 for all real numbers, the condition |${exprInside}| ${op} ${c} is ALWAYS true.`);
            steps.push(`Therefore, the solution set is an infinite set: <strong>(-∞, ∞)</strong> (Choice B in MyMathLab).`);
          }
        } else if (op === '<' || op === '<=') {
          // Conjunction / Sandwich
          rewriteForm = `-${c} ${op} ${exprInside} ${op} ${c}`;
          const left = (-c - b) / a;
          const right = (c - b) / a;
          const minVal = Math.min(left, right);
          const maxVal = Math.max(left, right);
          const br1 = op === '<=' ? '[' : '(';
          const br2 = op === '<=' ? ']' : ')';
          intervalAns = `${br1}${Number(minVal.toFixed(3))}, ${Number(maxVal.toFixed(3))}${br2}`;
          ruleSummary = `📐 <strong>LESS THAND Rule (Conjunction):</strong> |u| < c rewrites as the sandwiched compound inequality -c < u < c.`;
          steps.push(`Rewrite without absolute value bars (Part 1 in MyMathLab): <strong>${rewriteForm}</strong>`);
          steps.push(`Subtract ${b} from all parts: ${-c - b} ${op} ${a}x ${op} ${c - b}`);
          if (a !== 1) {
            steps.push(`Divide all parts by ${a}: ${Number(minVal.toFixed(3))} ${op} x ${op} ${Number(maxVal.toFixed(3))}`);
          }
          steps.push(`Interval notation solution (Part 2 in MyMathLab): <strong>${intervalAns}</strong>`);
        } else if (op === '>' || op === '>=') {
          // Disjunction / Wings
          const oppOp = op === '>' ? '<' : '<=';
          rewriteForm = `${exprInside} ${oppOp} -${c} or ${exprInside} ${op} ${c}`;
          const left = (-c - b) / a;
          const right = (c - b) / a;
          const minVal = Math.min(left, right);
          const maxVal = Math.max(left, right);
          const br1 = op === '>=' ? ']' : ')';
          const br2 = op === '>=' ? '[' : '(';
          intervalAns = `(-∞, ${Number(minVal.toFixed(3))}${br1} ∪ ${br2}${Number(maxVal.toFixed(3))}, ∞)`;
          ruleSummary = `🦅 <strong>GREAT OR Rule (Disjunction):</strong> |u| > c splits into two separate outer branches: u < -c OR u > c.`;
          steps.push(`Rewrite without absolute value bars (Part 1 in MyMathLab): <strong>${rewriteForm}</strong>`);
          steps.push(`Solve Branch 1: ${exprInside} ${oppOp} -${c} → x ${oppOp} ${Number(minVal.toFixed(3))}`);
          steps.push(`Solve Branch 2: ${exprInside} ${op} ${c} → x ${op} ${Number(maxVal.toFixed(3))}`);
          steps.push(`Union in interval notation (Part 2 in MyMathLab): <strong>${intervalAns}</strong>`);
        } else if (op === '=') {
          const x1 = (-c - b) / a;
          const x2 = (c - b) / a;
          rewriteForm = `${exprInside} = -${c} or ${exprInside} = ${c}`;
          intervalAns = `{${Number(Math.min(x1, x2).toFixed(3))}, ${Number(Math.max(x1, x2).toFixed(3))}}`;
          ruleSummary = `🎯 Equation: Split into positive and negative cases.`;
          steps.push(`Case 1: ${exprInside} = ${c} → x = ${Number(x2.toFixed(3))}`);
          steps.push(`Case 2: ${exprInside} = -${c} → x = ${Number(x1.toFixed(3))}`);
        }

        return {
          title: `📏 Absolute Value Solver (Ch 1.8): |${exprInside}| ${op} ${c}`,
          solverKey: 'abs',
          params: { a, b, op, c },
          outputVal: `
            <div style="display:flex; flex-direction:column; gap:6px; line-height:1.6;">
              <div>📝 <strong>Part 1 (Rewrite Form):</strong> <code>${rewriteForm}</code></div>
              <div>🎯 <strong>Part 2 (Interval Notation):</strong> <strong>${intervalAns}</strong></div>
              <div style="font-size:0.83rem; color:var(--text-muted); margin-top:2px;">${ruleSummary}</div>
            </div>
          `,
          steps
        };
      }

      if (parsed.type === 'circle_gen' || parsed.type === 'circle_std') {
        let h = 0, k = 0, r = 0, rSq = 0;
        if (parsed.type === 'circle_std') {
          h = parsed.h; k = parsed.k; r = parsed.r; rSq = parsed.rSq;
        } else {
          const { a, b, c, d } = parsed;
          h = -b / (2 * a);
          k = -c / (2 * a);
          rSq = (b * b + c * c - 4 * a * d) / (4 * a * a);
          r = Math.sqrt(Math.max(0, rSq));
        }

        return {
          title: `⭕ Circle Geometry Analyzer (Ch 1.1)`,
          solverKey: 'circle',
          params: { a: 1, b: -2 * h, c: -2 * k, d: h * h + k * k - rSq },
          outputVal: `Center: <strong>(${Number(h.toFixed(2))}, ${Number(k.toFixed(2))})</strong> &nbsp;|&nbsp; Radius: <strong>${Number(r.toFixed(2))}</strong>`,
          steps: [
            `Standard Form: (x - ${Number(h.toFixed(2))})² + (y - ${Number(k.toFixed(2))})² = ${Number(rSq.toFixed(2))}`,
            `Domain: [${Number((h - r).toFixed(2))}, ${Number((h + r).toFixed(2))}]`,
            `Range: [${Number((k - r).toFixed(2))}, ${Number((k + r).toFixed(2))}]`,
            `Cardinal Points: (${Number((h+r).toFixed(2))}, ${Number(k.toFixed(2))}), (${Number((h-r).toFixed(2))}, ${Number(k.toFixed(2))}), (${Number(h.toFixed(2))}, ${Number((k+r).toFixed(2))}), (${Number(h.toFixed(2))}, ${Number((k-r).toFixed(2))})`
          ]
        };
      }

      if (parsed.type === 'radical') {
        const mult = parsed.mult !== undefined ? parsed.mult : 1;
        const sim = simplifyRadical(parsed.n);
        const totalOut = mult * sim.outside;
        const signStr = totalOut < 0 ? '-' : '';
        const absOut = Math.abs(totalOut);
        let fmt1 = '';
        let fmt2 = '';
        if (parsed.n === 0) {
          fmt1 = '0'; fmt2 = '0';
        } else if (!sim.isImag) {
          fmt1 = sim.inside === 1 ? `${totalOut}` : `${signStr}${absOut === 1 ? '' : absOut}√${sim.inside}`;
          fmt2 = fmt1;
        } else {
          if (sim.inside === 1) {
            fmt1 = `${signStr}${absOut === 1 ? '' : absOut}i`;
            fmt2 = `0 ${totalOut >= 0 ? '+ ' + (absOut === 1 ? '' : absOut) : '- ' + (absOut === 1 ? '' : absOut)}i`;
          } else {
            fmt1 = `${signStr}${absOut === 1 ? '' : absOut}i√${sim.inside}`;
            fmt2 = `${signStr}${absOut === 1 ? '' : absOut}√${sim.inside}i`;
          }
        }
        const classStr = sim.isImag
          ? 'Complex, Nonreal complex, Pure imaginary'
          : 'Complex, Real (Real root exists)';
        return {
          title: `🌿 Radical & Imaginary Simplifier (Ch 1.3): ${mult === -1 ? '-' : (mult === 1 ? '' : mult)}√(${parsed.n})`,
          solverKey: 'radical',
          params: { n: parsed.n },
          outputVal: `Simplified: <strong>${fmt1}</strong>${fmt2 !== fmt1 ? ` &nbsp;(or <strong>${fmt2}</strong>)` : ''} &nbsp;|&nbsp; Classification: <strong>${classStr}</strong>`,
          steps: [
            `1. Factor radicand ${parsed.n}: largest perfect square factor is ${sim.outside * sim.outside}, remaining inside factor is ${sim.inside}${sim.isImag ? ', and √(-1) = i' : ''}`,
            `2. Extract root and multiply by outside factor (${mult}): ${mult} · ${sim.str} = <strong>${fmt1}</strong>`,
            `3. Number Classification: <strong>${classStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'radical_prod') {
        const { s1, n1, s2, n2 } = parsed;
        const sim1 = simplifyRadical(n1);
        const sim2 = simplifyRadical(n2);
        const iCount = (sim1.isImag ? 1 : 0) + (sim2.isImag ? 1 : 0);
        const iSign = iCount === 2 ? -1 : 1;
        const isFinalImag = iCount === 1;
        const totalSign = s1 * s2 * iSign;
        const absProd = Math.abs(n1 * n2);
        const prodSim = simplifyRadical(absProd);
        const outVal = totalSign * prodSim.outside;
        const sPrefix = outVal < 0 ? '-' : '';
        const absOut = Math.abs(outVal);
        let finalStr = '';
        if (isFinalImag) {
          finalStr = prodSim.inside === 1
            ? `${sPrefix}${absOut === 1 ? '' : absOut}i`
            : `${sPrefix}${absOut === 1 ? '' : absOut}i√${prodSim.inside}`;
        } else {
          finalStr = prodSim.inside === 1
            ? `${outVal}`
            : `${sPrefix}${absOut === 1 ? '' : absOut}√${prodSim.inside}`;
        }
        return {
          title: `🌿 Product of Radicals Solver (Ch 1.3): (${s1 < 0 ? '-' : ''}√(${n1}))(${s2 < 0 ? '-' : ''}√(${n2}))`,
          solverKey: 'radical',
          params: { n: n1 },
          outputVal: `Exact Product: <strong>${finalStr}</strong> ${!isFinalImag ? `(or <strong>${finalStr} + 0i</strong>)` : ''}`,
          steps: [
            `1. CRITICAL RULE: Rewrite square roots of negative numbers in terms of i FIRST before multiplying!`,
            `2. First factor: ${s1 < 0 ? '-' : ''}√(${n1}) = ${s1 < 0 ? '-' : ''}${sim1.str} &nbsp;|&nbsp; Second factor: ${s2 < 0 ? '-' : ''}√(${n2}) = ${s2 < 0 ? '-' : ''}${sim2.str}`,
            `3. Multiply factors: ${iCount === 2 ? `i · i = i² = -1, and √(${Math.abs(n1)})·√(${Math.abs(n2)}) = √(${absProd}) = ${prodSim.str}` : `√(${absProd}) = ${prodSim.str}`}`,
            `4. Simplified Result in a + bi form: <strong>${finalStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'complex_std_frac') {
        const { A, B, C, D } = parsed;
        const sim = simplifyRadical(C);
        const realStr = fracStr(A, D);
        const imagNum = B * sim.outside;
        const g = gcd(Math.abs(imagNum), Math.abs(D));
        const redNum = Math.abs(imagNum) / g;
        const redDen = Math.abs(D) / g;
        const signChar = (imagNum * D) >= 0 ? '+' : '-';

        let secondTerm1 = '';
        let secondTerm2 = '';
        const radPart = sim.inside === 1 ? '' : `√${sim.inside}`;
        const iPart = sim.isImag ? 'i' : '';
        if (redDen === 1) {
          const coeff = (redNum === 1 && (radPart || iPart)) ? '' : redNum;
          secondTerm1 = `${coeff}${radPart}${iPart}`.trim();
          secondTerm2 = `${coeff}${iPart}${radPart}`.trim();
        } else {
          const coeff = (redNum === 1 && (radPart || iPart)) ? '' : redNum;
          secondTerm1 = `(${coeff}${radPart})/${redDen} i`.trim();
          secondTerm2 = `(${coeff}${iPart}${radPart})/${redDen}`.trim();
        }
        return {
          title: `🔢 Standard Form a + bi Fraction Simplifier (Ch 1.3): (${A} ${B >= 0 ? '+ ' + (B === 1 ? '' : B) : '- ' + (Math.abs(B) === 1 ? '' : Math.abs(B))}√(${C})) / ${D}`,
          solverKey: 'complex',
          params: { a1: A, b1: B, a2: D, b2: 0 },
          outputVal: `Standard Form (a + bi): <strong>${realStr} ${signChar} ${secondTerm1}</strong> &nbsp;(or <strong>${realStr} ${signChar} ${secondTerm2}</strong>)`,
          steps: [
            `1. Simplify the radical: √(${C}) = √(${sim.outside * sim.outside} · ${sim.inside}${sim.isImag ? ' · (-1)' : ''}) = ${sim.str}`,
            `2. Substitute simplified radical into numerator: (${A} ${B >= 0 ? '+' : '-'} ${Math.abs(B * sim.outside)}${iPart}${radPart}) / ${D}`,
            `3. Split into real and imaginary fractions: (${A}/${D}) ${signChar} (${Math.abs(imagNum)}${iPart}${radPart})/${Math.abs(D)}`,
            `4. Reduce each fraction to lowest terms: <strong>${realStr} ${signChar} ${secondTerm1}</strong>`,
            `💡 <strong>MyMathLab Entry Tip:</strong> Enter in standard form a + bi with separate fractions: <code>${realStr} ${signChar} ${secondTerm1}</code>. Ensure the <strong>i</strong> is outside the radical (press right arrow after the radical) and outside the denominator.`
          ]
        };
      }

      if (parsed.type === 'radical_conj') {
        const { aRad, isImag, bVal, resVal } = parsed;
        return {
          title: `🔢 Conjugate Binomial Product Solver (Ch 1.3): (√${aRad} + ${isImag ? (bVal === 1 ? 'i' : bVal + 'i') : '√' + bVal})(√${aRad} - ${isImag ? (bVal === 1 ? 'i' : bVal + 'i') : '√' + bVal})`,
          solverKey: 'complex',
          params: { a1: Math.sqrt(aRad), b1: bVal, a2: Math.sqrt(aRad), b2: -bVal },
          outputVal: `Exact Product: <strong>${resVal}</strong> (or <strong>${resVal} + 0i</strong>)`,
          steps: [
            `1. Difference of Squares / Complex Conjugate Formula: (A + B)(A - B) = A² - B²`,
            `2. Square the first term: (√${aRad})² = ${aRad}`,
            isImag
              ? `3. Square the imaginary term: (${bVal === 1 ? '' : bVal}i)² = ${bVal * bVal}i² = -${bVal * bVal}`
              : `3. Square the second radical term: (√${bVal})² = ${bVal}`,
            `4. Subtract: ${aRad} - (${isImag ? -(bVal * bVal) : bVal}) = <strong>${resVal}</strong>`
          ]
        };
      }

      if (parsed.type === 'complex_verify_quad') {
        const { u, v, p, q } = parsed;
        const cStr = `${u} ${v >= 0 ? '+ ' + (v === 1 ? '' : v) : '- ' + (Math.abs(v) === 1 ? '' : Math.abs(v))}i`;
        const u2 = u * u;
        const uv2 = 2 * u * v;
        const v2 = v * v;
        const pu = p * u;
        const pv = p * v;
        const fmtTerm = (val, suffix = '') => `${val >= 0 ? '+ ' + val : '- ' + Math.abs(val)}${suffix}`;
        const uncombinedWithI2 = `${u2} ${fmtTerm(uv2, 'i')} + ${v2}i^2 ${fmtTerm(pu)} ${fmtTerm(pv, 'i')} ${fmtTerm(q)}`;
        const uncombinedWithNeg = `${u2} ${fmtTerm(uv2, 'i')} - ${v2} ${fmtTerm(pu)} ${fmtTerm(pv, 'i')} ${fmtTerm(q)}`;
        const realSum = u2 - v2 + pu + q;
        const imagSum = uv2 + pv;
        const finalComb = (realSum === 0 && imagSum === 0) ? '0' : `${realSum} ${fmtTerm(imagSum, 'i')}`;
        return {
          title: `🔢 Complex Quadratic Solution Verifier (Ch 1.3 Q17–18): x = ${cStr} in x² ${fmtTerm(p, 'x')} ${fmtTerm(q)} = 0`,
          solverKey: 'complex',
          params: { a1: u, b1: v, a2: u, b2: v },
          outputVal: `Sub: <strong>${cStr}</strong> &nbsp;|&nbsp; Expanded: <strong>${uncombinedWithI2}</strong> &nbsp;|&nbsp; Combined: <strong>${finalComb}</strong>`,
          steps: [
            `1. First step — Substitute for x: <strong>${cStr}</strong>`,
            `2. Perform substitution: 0 ≟ <strong>(${cStr})² ${fmtTerm(p)}(${cStr}) ${fmtTerm(q)}</strong>`,
            `3. Most useful next step: <strong>Expand the right side of the equation.</strong>`,
            `4. Apply expansion (do not combine like terms): 0 ≟ <strong>${uncombinedWithI2}</strong> &nbsp;(or <strong>${uncombinedWithNeg}</strong>)`,
            `5. Combine like terms: Real = (${u2} - ${v2} ${fmtTerm(pu)} ${fmtTerm(q)}) = ${realSum}, Imaginary = (${uv2} ${fmtTerm(pv)})i = ${imagSum}i → 0 ≟ <strong>${finalComb}</strong>`
          ]
        };
      }

      if (parsed.type === 'complex_addsub') {
        const { a1, b1, op, a2, b2, real, imag } = parsed;
        const imagStr = imag >= 0 ? `+ ${imag === 1 ? '' : imag}i` : `- ${Math.abs(imag) === 1 ? '' : Math.abs(imag)}i`;
        return {
          title: `🔢 Complex Addition / Subtraction (Ch 1.3): (${a1} + ${b1}i) ${op} (${a2} + ${b2}i)`,
          solverKey: 'complex',
          params: { a1, b1, a2, b2 },
          outputVal: `Result in Standard Form: <strong>${real} ${imagStr}</strong>`,
          steps: [
            `1. Combine real parts: ${a1} ${op} (${a2}) = ${real}`,
            `2. Combine imaginary parts: (${b1} ${op} (${b2}))i = ${imag}i`,
            `3. Standard Form a + bi: <strong>${real} ${imagStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'complex_div') {
        const { a1, b1, a2, b2 } = parsed;
        const den = a2 * a2 + b2 * b2;
        const rNum = a1 * a2 + b1 * b2;
        const iNum = b1 * a2 - a1 * b2;
        const rFrac = fracStr(rNum, den);
        const iFrac = fracStr(Math.abs(iNum), den);
        const sign = iNum >= 0 ? '+' : '-';
        return {
          title: `🔢 Complex Division via Conjugate (Ch 1.3): (${a1} + ${b1}i) / (${a2} + ${b2}i)`,
          solverKey: 'complex',
          params: { a1, b1, a2, b2 },
          outputVal: `Standard Form: <strong>${rFrac} ${sign} ${iFrac === '1' ? '' : iFrac}i</strong>`,
          steps: [
            `1. Multiply numerator and denominator by the complex conjugate (${a2} ${-b2 >= 0 ? '+ ' + (-b2) : '- ' + Math.abs(b2)}i)`,
            `2. Denominator: (${a2})² + (${b2})² = ${den}`,
            `3. Numerator: (${a1})(${a2}) + (${b1})(${b2}) + [(${b1})(${a2}) - (${a1})(${b2})]i = ${rNum} + (${iNum})i`,
            `4. Standard Form: <strong>${rFrac} ${sign} ${iFrac === '1' ? '' : iFrac}i</strong>`
          ]
        };
      }

      if (parsed.type === 'num_classify') {
        if (parsed.isEvalPow) {
          return {
            title: `🔢 Order of Operations & Exponent Evaluator (Ch 1.3): ${parsed.raw}`,
            solverKey: 'complex',
            params: { n: parsed.exp },
            outputVal: `Evaluated Value: <strong>${parsed.val}</strong>`,
            steps: [
              parsed.outerNeg
                ? `1. By order of operations, evaluate the exponent on the base ${parsed.base} first: ${parsed.base}^${parsed.exp} = ${Math.pow(parsed.base, parsed.exp)}`
                : `1. Base includes parentheses: (${parsed.base})^${parsed.exp} = ${parsed.val}`,
              parsed.outerNeg
                ? `2. Apply the leading negative sign: -(${Math.pow(parsed.base, parsed.exp)}) = <strong>${parsed.val}</strong>`
                : `2. Result: <strong>${parsed.val}</strong>`
            ]
          };
        }
        const { raw: rawNum, a, b } = parsed;
        const tags = ['Complex'];
        if (Math.abs(b) < 1e-9) {
          tags.push('Real');
        } else {
          tags.push('Nonreal complex');
          if (Math.abs(a) < 1e-9) tags.push('Pure imaginary');
        }
        return {
          title: `🔢 Complex Number System Classifier (Ch 1.3 Q1–5): ${rawNum}`,
          solverKey: 'complex',
          params: { a1: a, b1: b, a2: 1, b2: 0 },
          outputVal: `Applies to: <strong>${tags.join(', ')}</strong>`,
          steps: [
            `1. Write in standard form a + bi: a = ${a === Math.PI ? 'π' : a}, b = ${b}`,
            `2. Every real or imaginary number belongs to the <strong>Complex</strong> numbers (since a + bi includes b = 0).`,
            Math.abs(b) < 1e-9
              ? `3. Since imaginary part b = 0, the number is <strong>Real</strong> (and Complex).`
              : `3. Since imaginary part b ≠ 0, it is <strong>Nonreal complex</strong>${Math.abs(a) < 1e-9 ? ' AND <strong>Pure imaginary</strong> (because real part a = 0).' : ' (NOT pure imaginary since a ≠ 0).'}`
          ]
        };
      }

      if (parsed.type === 'complex_mult') {
        const { a1, b1, a2, b2 } = parsed;
        const real = a1 * a2 - b1 * b2;
        const imag = a1 * b2 + a2 * b1;
        const imagStr = imag === 0 ? '' : (imag > 0 ? ` + ${imag}i` : ` - ${Math.abs(imag)}i`);
        const fullForm = `${real} ${imag >= 0 ? '+ ' + imag : '- ' + Math.abs(imag)}i`;
        return {
          title: `🔢 Complex Multiplication (Ch 1.3): (${a1} ${b1 >= 0 ? '+ ' + b1 : '- ' + Math.abs(b1)}i)(${a2} ${b2 >= 0 ? '+ ' + b2 : '- ' + Math.abs(b2)}i)`,
          solverKey: 'complex',
          params: { a1, b1, a2, b2 },
          outputVal: `Product: <strong>${real}${imagStr}</strong> ${imag === 0 ? `(or <strong>${fullForm}</strong>)` : ''}`,
          steps: [
            `1. FOIL expansion: (${a1})(${a2}) + (${a1})(${b2}i) + (${b1}i)(${a2}) + (${b1}i)(${b2}i)`,
            `2. Substitute i² = -1: ${a1 * a2} + (${a1 * b2 + a2 * b1})i + (${b1 * b2})(-1)`,
            `3. Combine real and imaginary parts: (${a1 * a2} - ${b1 * b2}) + (${a1 * b2 + a2 * b1})i = <strong>${real}${imagStr}</strong>`
          ]
        };
      }

      if (parsed.type === 'powers_i') {
        const rem = ((parsed.n % 4) + 4) % 4;
        const valMap = { 0: '1', 1: 'i', 2: '-1', 3: '-i' };
        return {
          title: `🔢 Power of i: i^${parsed.n}`,
          solverKey: 'complex',
          params: { n: parsed.n },
          outputVal: `i^${parsed.n} = <strong>${valMap[rem]}</strong>`,
          steps: [
            `1. Exponent divided by 4: ${parsed.n} ÷ 4 = ${Math.floor(parsed.n/4)} with remainder ${rem}`,
            `2. Since i⁴ = 1, i^${parsed.n} = (i⁴)^${Math.floor(parsed.n/4)} · i^${rem} = <strong>${valMap[rem]}</strong>`
          ]
        };
      }

      return null;
    }

    function getFactorsJS(n) {
      n = Math.abs(Math.round(n));
      if (n === 0) return [1];
      const f = new Set();
      for (let i = 1; i <= Math.sqrt(n); i++) {
        if (n % i === 0) {
          f.add(i);
          f.add(Math.round(n / i));
        }
      }
      return Array.from(f).sort((a,b) => a - b);
    }

    function polySyntheticJS(poly, c) {
      const row = [poly[0]];
      for (let i = 1; i < poly.length; i++) {
        row.push(poly[i] + row[row.length - 1] * c);
      }
      return { quotient: row.slice(0, -1), remainder: row[row.length - 1] };
    }

    function polyEvalJS(poly, x) {
      return poly.reduce((acc, v) => acc * x + v, 0);
    }

    function findRationalRootsJS(poly) {
      let curr = [...poly];
      while (curr.length > 0 && Math.abs(curr[0]) < 1e-9) curr.shift();
      if (curr.length <= 1) return [];

      const roots = [];
      const lead = curr[0];
      const constVal = curr[curr.length - 1];

      if (Math.abs(constVal) < 1e-9) {
        roots.push(0);
        const { quotient } = polySyntheticJS(curr, 0);
        return roots.concat(findRationalRootsJS(quotient));
      }

      const pFacs = getFactorsJS(constVal);
      const qFacs = getFactorsJS(lead);
      const candidates = new Set();
      for (let p of pFacs) {
        for (let q of qFacs) {
          candidates.add(p / q);
          candidates.add(-p / q);
        }
      }

      const sortedCandidates = Array.from(candidates).sort((a,b) => a - b);
      for (let c of sortedCandidates) {
        while (curr.length > 1 && Math.abs(polyEvalJS(curr, c)) < 1e-6) {
          roots.push(c);
          const res = polySyntheticJS(curr, c);
          curr = res.quotient;
        }
      }

      if (curr.length === 3) {
        const a = curr[0], b = curr[1], c = curr[2];
        const disc = b * b - 4 * a * c;
        if (disc >= 0) {
          const r1 = (-b + Math.sqrt(disc)) / (2 * a);
          const r2 = (-b - Math.sqrt(disc)) / (2 * a);
          if (!roots.some(r => Math.abs(r - r1) < 1e-6)) roots.push(r1);
          if (!roots.some(r => Math.abs(r - r2) < 1e-6)) roots.push(r2);
        }
      }

      return roots.sort((a,b) => a - b);
    }

    function formatPolyCoeffs(coeffs) {
      const deg = coeffs.length - 1;
      const terms = [];
      coeffs.forEach((v, idx) => {
        const p = deg - idx;
        if (v !== 0 || (terms.length === 0 && p === 0)) {
          const s = (v === 1 && p > 0) ? '' : (v === -1 && p > 0 ? '-' : v);
          terms.push(p === 0 ? `${v}` : (p === 1 ? `${s}x` : `${s}x^${p}`));
        }
      });
      return terms.join(' + ').replace(/\+ -/g, '- ') || '0';
    }

    // ==========================================
    // Math Utilities & Algorithms
    // ==========================================

    function gcd(a, b) {
      a = Math.abs(Math.round(a));
      b = Math.abs(Math.round(b));
      while (b) { let t = b; b = a % b; a = t; }
      return a || 1;
    }

    function fracStr(num, den = 1) {
      if (den === 0) return 'undefined';
      if (num === 0) return '0';
      let n = Math.round(num);
      let d = Math.round(den);
      let g = gcd(n, d);
      n /= g; d /= g;
      if (d < 0) { n = -n; d = -d; }
      if (d === 1) return '' + n;
      return `${n}/${d}`;
    }

    function simplifyRadical(n) {
      if (n === 0) return { outside: 0, inside: 0, isImag: false, str: "0" };
      const isNeg = n < 0;
      let val = Math.abs(Math.round(n));
      let outside = 1;
      for (let d = 2; d * d <= val; d++) {
        while (val % (d * d) === 0) {
          outside *= d;
          val /= (d * d);
        }
      }
      let s = "";
      if (outside !== 1 || (outside === 1 && val === 1 && !isNeg)) s += outside;
      if (isNeg) s += "i";
      if (val > 1) s += "√" + val;
      if (isNeg && outside === 1 && val > 1) s = "i√" + val;
      return { outside, inside: val, isImag: isNeg, str: s || "1" };
    }

    // Markdown & Math Parser into clean Study Cards
    function renderMarkdownToHtml(mdText) {
      const rawSections = mdText.split(/(?=\n\*\s+\*\*Question\s+\d+:?|\n\*\s+\*\*Q\d+:?|\n###\s+\*?\*?Questions?\s+)/i);
      let html = '';
      const headerText = rawSections[0] || '';
      const titleMatch = headerText.match(/#\s+(.*?)(?:\n|$)/);
      const metaMatch = headerText.match(/\*\*Course:\*\*(.*?)(?=\n---|\n###|\n\*|$)/s);
      
      if (titleMatch) {
        html += `<h1 class="sheet-title">${formatMath(titleMatch[1].trim())}</h1>`;
      }
      if (metaMatch) {
        html += `<div class="sheet-meta">${metaMatch[0].replace(/\n/g, '<br>')}</div>`;
      }

      let qIndex = 0;
      for (let i = 1; i < rawSections.length; i++) {
        const sec = rawSections[i].trim();
        if (!sec) continue;

        const groupMatch = sec.match(/^###\s+\*?\*?(Questions?\s+[^\n]+)\*?\*?/i);
        if (groupMatch && !sec.includes('* **Problem:')) {
          html += `<div style="margin:26px 0 16px 0; padding:10px 16px; background:rgba(56,189,248,0.1); border-left:4px solid #38bdf8; border-radius:4px; font-weight:700; color:#38bdf8; font-size:1.05rem;">${formatMath(groupMatch[1])}</div>`;
          const subItems = sec.split(/(?=\n\*\s+\*\*Question|\n\*\s+\*\*Q\d+)/i);
          if (subItems.length > 1) {
            for (let j = 1; j < subItems.length; j++) {
              html += parseQuestionCard(subItems[j], ++qIndex);
            }
          }
          continue;
        }

        html += parseQuestionCard(sec, ++qIndex);
      }

      if (rawSections.length <= 1) {
        html += `<div style="line-height:1.7;">${formatGeneralMarkdown(mdText)}</div>`;
      }

      return html;
    }

    function extractGraphableFromQuestion(problem, answer, explicitEq = '', fullSec = '') {
      // 1. Check explicit * **Graph Equation:** `...` in fullSec or explicitEq
      if (fullSec) {
        const geMatch = fullSec.match(/\*\s+\*\*Graph\s+Equation:\*\*\s*`?([^`\n]+)`?/i);
        if (geMatch && geMatch[1].trim()) {
          const cand = normalizeLatexToAscii(geMatch[1].trim());
          if (cand.toLowerCase() === 'none') return '';
          return cand;
        }
        // Also allow * **Graph:** if the value is an actual equation (not Choice A/B/C/D or none)
        const altMatch = fullSec.match(/\*\s+\*\*Graph:\*\*\s*`?([^`\n]+)`?/i);
        if (altMatch && altMatch[1].trim()) {
          const cand = normalizeLatexToAscii(altMatch[1].trim());
          if (cand.toLowerCase() === 'none') return '';
          if (cand && !/^choice\s+[a-d]/i.test(cand) && !/^\(\s*[-+\d.∞inf]+\s*,\s*[-+\d.∞inf]+\s*\)$/i.test(cand)) {
            if (parseEquationSyntax(cand)) return cand;
          }
        }
      }
      if (explicitEq) {
        const cand = normalizeLatexToAscii(explicitEq);
        const p = parseEquationSyntax(cand);
        if (p && buildGraphDataFromParsed(p, cand)) return cand;
      }

      // 2. Scan $...$ and `...` blocks in problem & answer
      const combined = (problem || '') + '\n' + (answer || '');
      const mathBlocks = [];
      const dollarMatches = combined.matchAll(/\$([^$]+)\$/g);
      for (const m of dollarMatches) mathBlocks.push(m[1]);
      const tickMatches = combined.matchAll(/`([^`]+)`/g);
      for (const m of tickMatches) mathBlocks.push(m[1]);

      for (const rawBlock of mathBlocks) {
        let cand = normalizeLatexToAscii(rawBlock);
        // Strip leading f(x) =, g(x) =, R(x) =, P(x) =, h(x) =, y =
        cand = cand.replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '');
        if (!cand || cand.length < 2) continue;
        // Skip concept terms and coordinate intervals
        if (/x-intercept|y-intercept|x-axis|y-axis|turning-point/i.test(cand)) continue;
        if (/^\(\s*[-+\d.∞inf]+\s*,\s*[-+\d.∞inf]+\s*\)$/i.test(cand)) continue;
        const parsed = parseEquationSyntax(cand);
        if (parsed && buildGraphDataFromParsed(parsed, cand)) {
          return cand;
        }
        // Check if it's a function f(x) = ... in rawBlock
        if (/^[fghpqrFGH]\(x\)\s*=/i.test(normalizeLatexToAscii(rawBlock)) && cand.includes('x') && !cand.includes('y')) {
          const fn = compileMathFunction(cand);
          if (fn) return cand;
        }
      }
      return '';
    }

    function renderAllInlineGraphs() {
      const canvases = document.querySelectorAll('canvas.inline-q-canvas');
      canvases.forEach(canvas => {
        const rawEq = decodeURIComponent(canvas.getAttribute('data-graph-eq') || '');
        if (!rawEq || !canvas.id) return;
        const parsed = parseEquationSyntax(rawEq);
        let graphData = parsed ? buildGraphDataFromParsed(parsed, rawEq) : null;
        if (!graphData && rawEq.includes('x')) {
          const compiled = compileMathFunction(rawEq);
          if (compiled) {
            const y0 = compiled(0);
            graphData = {
              id: `inline_${canvas.id}_${rawEq}`,
              type: 'function',
              fn: compiled,
              points: (!isNaN(y0) && isFinite(y0)) ? [{ x: 0, y: y0, type: 'point', color: '#a855f7', label: `(0, ${y0.toFixed(2)})` }] : [],
              curveColor: '#38bdf8',
              label: `f(x) = ${rawEq}`
            };
          }
        }
        if (graphData) {
          renderUniversalGraph(canvas.id, graphData);
        }
      });
    }

    // ==========================================================================
    // INLINE REAL-TIME PROBLEM & EQUATION EDITOR (Tab 1 & Tab 4)
    // ==========================================================================

    const originalCardStates = {};

    function extractInitialEditableExpr(problem, answer, graphEq = '', fullSec = '') {
      if (fullSec) {
        const geMatch = fullSec.match(/\*\s+\*\*Graph\s+Equation:\*\*\s*`?([^`\n]+)`?/i);
        if (geMatch && geMatch[1].trim() && geMatch[1].trim().toLowerCase() === 'none') {
          return '';
        }
      }

      const probBlocks = [];
      if (problem) {
        for (const m of problem.matchAll(/\$([^$]+)\$/g)) probBlocks.push(normalizeLatexToAscii(m[1]).trim());
        for (const m of problem.matchAll(/`([^`]+)`/g)) probBlocks.push(normalizeLatexToAscii(m[1]).trim());
      }

      // 0a. Check Impedance E = IZ with I = ... and Z = ... (Ch 1.3 Q19)
      if (/impedance|voltage|current|E\s*=\s*IZ/i.test(problem)) {
        const izFind = problem.match(/I\s*=\s*([+-]?\d+(?:\.\d+)?\s*[+-]\s*\d*(?:\.\d+)?i).*?Z\s*=\s*([+-]?\d+(?:\.\d+)?\s*[+-]\s*\d*(?:\.\d+)?i)/i);
        if (izFind) {
          return `I = ${izFind[1].trim()}, Z = ${izFind[2].trim()}`;
        }
      }

      // 0b. Check Complex Quadratic Solution Verification: complex root + quadratic equation (Ch 1.3 Q17–18)
      const cplxRoot = probBlocks.find(b => /^[+-]?\d+\s*[+-]\s*\d*i$/i.test(b.replace(/\s+/g, '')));
      const quadEq = probBlocks.find(b => /x\^2\s*[+-]\s*\d*x\s*[+-]\s*\d+\s*=\s*0/i.test(b.replace(/\s+/g, '')));
      if (cplxRoot && quadEq) {
        return `${cplxRoot}; ${quadEq}`;
      }

      // 0c. Check Projectile / Height Inequality (Ch 3.6 Q17)
      if (/height|baseball|projectile|rocket|thrown|ball/i.test(problem) && /-16t\^2/i.test(problem)) {
        const hEqMatch = problem.match(/s\s*=\s*(-16t\^2\s*[+-]\s*\d+t\s*[+-]\s*\d+)/i);
        const atLeastMatch = problem.match(/at\s*least\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const atMostMatch = problem.match(/at\s*most\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const moreThanMatch = problem.match(/(?:more\s*than|above|exceeds?)\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const lessThanMatch = problem.match(/(?:less\s*than|below)\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        if (hEqMatch) {
          const quadPart = hEqMatch[1].trim();
          let op = '>=';
          let targetH = 0;
          if (atLeastMatch) { op = '>='; targetH = atLeastMatch[1]; }
          else if (atMostMatch) { op = '<='; targetH = atMostMatch[1]; }
          else if (moreThanMatch) { op = '>'; targetH = moreThanMatch[1]; }
          else if (lessThanMatch) { op = '<'; targetH = lessThanMatch[1]; }
          if (targetH) return `${quadPart} ${op} ${targetH}`;
        }
      }

      // 0d. Division Sign Rules (Ch 3.6 Q18–19)
      if (/negative.*divided.*by.*negative/i.test(problem)) return '(-a) / (-b) > 0';
      if (/negative.*divided.*by.*positive/i.test(problem)) return '(-a) / (+b) < 0';
      if (/positive.*divided.*by.*negative/i.test(problem)) return '(+a) / (-b) < 0';
      if (/positive.*divided.*by.*positive/i.test(problem)) return '(+a) / (+b) > 0';

      // 0e. If explicit graphEq is provided and parses cleanly, prefer it!
      if (graphEq) {
        if (parseEquationSyntax(graphEq)) return graphEq;
      }

      // 1. Check if problem has 2 or 3 equations in a system (x and y, or x, y, z)
      const sysEqs = probBlocks.filter(b => b.includes('=') && (b.includes('x') || b.includes('y')));
      if (sysEqs.length >= 2 && sysEqs.length <= 3 && sysEqs.some(b => b.includes('y'))) {
        const joinedSys = sysEqs.join('; ');
        if (parseEquationSyntax(joinedSys)) return joinedSys;
      }

      // 2. Check if problem has 2 coordinate points (x1, y1) and (x2, y2)
      const ptBlocks = probBlocks.filter(b => /^\(\s*[+-]?\d+(?:\.\d+)?\s*,\s*[+-]?\d+(?:\.\d+)?\s*\)$/.test(b));
      if (ptBlocks.length === 2) {
        return `${ptBlocks[0]}, ${ptBlocks[1]}`;
      }

      // 3. Check if problem is Synthetic Division / Remainder / Factor Theorem with P(x) and divisor (x - c or k = c)
      if (probBlocks.length >= 2 && /divide|synthetic|remainder|factor|zero/i.test(problem)) {
        const p0 = probBlocks[0].replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '').trim();
        const p1 = probBlocks[1].trim();
        const trySemi = `${p0}; ${p1}`;
        if (parseEquationSyntax(trySemi)) return trySemi;
        const tryRev = `${p1}; ${p0}`;
        if (parseEquationSyntax(tryRev)) return tryRev;
      }

      // 4. If graphEq is already extracted and parses cleanly, use it
      if (graphEq) {
        if (parseEquationSyntax(graphEq)) return graphEq;
      }

      // 5. Try candidate math blocks in problem
      // Filter out isolated single letters (like i, I, x, y, a, b, r) if richer expressions exist
      const nonTrivialBlocks = probBlocks.filter(b => (b.length > 1 && !/^[a-zA-Z]$/.test(b)) || /[+\-*/^=√]|sqrt/i.test(b));
      const candidatesToTry = nonTrivialBlocks.length > 0 ? nonTrivialBlocks : probBlocks;

      for (const b of candidatesToTry) {
        if (/^\d+$/.test(b.trim())) continue;
        const cleaned = b.replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '').trim();
        if (/^\d+$/.test(cleaned)) continue;
        if (parseEquationSyntax(cleaned)) return cleaned;
        if (parseEquationSyntax(b)) return b;
      }

      // Also try remaining probBlocks if none matched yet
      for (const b of probBlocks) {
        if (/^\d+$/.test(b.trim())) continue;
        const cleaned = b.replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '').trim();
        if (/^\d+$/.test(cleaned)) continue;
        if (parseEquationSyntax(cleaned)) return cleaned;
        if (parseEquationSyntax(b)) return b;
      }

      if (graphEq) return graphEq;
      if (nonTrivialBlocks.length > 0) return nonTrivialBlocks.join('; ');
      return normalizeLatexToAscii(problem || '').replace(/^.*?:\s*/, '').trim().substring(0, 80);
    }

    function normalizeEditedMathText(str) {
      if (!str) return '';
      const supRev = { '⁰':'^0', '¹':'^1', '²':'^2', '³':'^3', '⁴':'^4', '⁵':'^5', '⁶':'^6', '⁷':'^7', '⁸':'^8', '⁹':'^9' };
      let out = str
        .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]/g, ch => supRev[ch] || ch)
        .replace(/≤/g, '<=')
        .replace(/≥/g, '>=')
        .replace(/−/g, '-')
        .replace(/⋅|·/g, '*')
        .replace(/÷/g, '/');
      return normalizeLatexToAscii(out).trim();
    }

    function extractDomMathText(node) {
      if (!node) return '';
      if (node.nodeType === 3) return node.textContent || '';
      if (node.classList && node.classList.contains('frac')) {
        const num = node.querySelector('.num');
        const den = node.querySelector('.den');
        const numT = num ? extractDomMathText(num).trim() : '';
        const denT = den ? extractDomMathText(den).trim() : '';
        return `((${numT})/(${denT}))`;
      }
      let out = '';
      for (let ch of node.childNodes) {
        out += extractDomMathText(ch);
      }
      return out;
    }

    function onProblemTextEdited(qNum) {
      const probEl = document.getElementById(`qprob-${qNum}`);
      const inputEl = document.getElementById(`qinput-${qNum}`);
      if (!probEl || !inputEl) return;

      // Extract updated math chips from .math-sym, .math-chip, and code elements
      const chips = Array.from(probEl.querySelectorAll('.math-sym, .math-chip, code'))
        .map(el => normalizeEditedMathText(extractDomMathText(el)))
        .filter(Boolean);

      const nonTrivialChips = chips.filter(c => c.length > 2 || /[+\-*/^=√]|sqrt/i.test(c));
      const activeChips = nonTrivialChips.length > 0 ? nonTrivialChips : chips;

      let candidate = '';

      // Check Projectile / Height Inequality (Ch 3.6 Q17)
      const probText = probEl.textContent || '';
      if (/height|baseball|projectile|rocket|thrown|ball/i.test(probText) && /-16t\^2/i.test(probText)) {
        const hEqMatch = probText.match(/s\s*=\s*(-16t\^2\s*[+-]\s*\d+t\s*[+-]\s*\d+)/i);
        const atLeastMatch = probText.match(/at\s*least\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const atMostMatch = probText.match(/at\s*most\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const moreThanMatch = probText.match(/(?:more\s*than|above|exceeds?)\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        const lessThanMatch = probText.match(/(?:less\s*than|below)\s*(\d+(?:\.\d+)?)\s*(?:ft|feet)?/i);
        if (hEqMatch) {
          const quadPart = hEqMatch[1].trim();
          let op = '>=';
          let targetH = 0;
          if (atLeastMatch) { op = '>='; targetH = atLeastMatch[1]; }
          else if (atMostMatch) { op = '<='; targetH = atMostMatch[1]; }
          else if (moreThanMatch) { op = '>'; targetH = moreThanMatch[1]; }
          else if (lessThanMatch) { op = '<'; targetH = lessThanMatch[1]; }
          if (targetH) candidate = `${quadPart} ${op} ${targetH}`;
        }
      }

      // Check Quotient Sign Rules (Ch 3.6 Q18–19)
      if (!candidate) {
        if (/negative.*divided.*by.*negative/i.test(probText)) candidate = '(-a) / (-b) > 0';
        else if (/negative.*divided.*by.*positive/i.test(probText)) candidate = '(-a) / (+b) < 0';
        else if (/positive.*divided.*by.*negative/i.test(probText)) candidate = '(+a) / (-b) < 0';
        else if (/positive.*divided.*by.*positive/i.test(probText)) candidate = '(+a) / (+b) > 0';
      }

      // Check Impedance E = IZ
      if (!candidate && /impedance|voltage|current|E\s*=\s*IZ/i.test(probText)) {
        const izFind = probText.match(/I\s*=\s*([+-]?\d+(?:\.\d+)?\s*[+-]\s*\d*(?:\.\d+)?i).*?Z\s*=\s*([+-]?\d+(?:\.\d+)?\s*[+-]\s*\d*(?:\.\d+)?i)/i);
        if (izFind) candidate = `I = ${izFind[1].trim()}, Z = ${izFind[2].trim()}`;
      }

      // Check complex solution verification
      if (!candidate) {
        const cplxPart = activeChips.find(b => /^[+-]?\d+\s*[+-]\s*\d*i$/i.test(b.replace(/\s+/g, '')));
        const quadPart = activeChips.find(b => /x\^2\s*[+-]\s*\d*x\s*[+-]\s*\d+\s*=\s*0/i.test(b.replace(/\s+/g, '')));
        if (cplxPart && quadPart) candidate = `${cplxPart}; ${quadPart}`;
      }

      if (!candidate && activeChips.length >= 2) {
        // Check system of equations
        const sysEqs = activeChips.filter(b => b.includes('=') && (b.includes('x') || b.includes('y')));
        const ptBlocks = activeChips.filter(b => /^\(\s*[+-]?\d+(?:\.\d+)?\s*,\s*[+-]?\d+(?:\.\d+)?\s*\)$/.test(b));
        if (sysEqs.length >= 2 && sysEqs.some(b => b.includes('y'))) {
          candidate = sysEqs.join('; ');
        } else if (ptBlocks.length === 2) {
          candidate = `${ptBlocks[0]}, ${ptBlocks[1]}`;
        } else {
          const p0 = activeChips[0].replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '').trim();
          const trySemi = `${p0}; ${activeChips[1]}`;
          if (parseEquationSyntax(trySemi)) candidate = trySemi;
        }
      }
      if (!candidate && activeChips.length >= 1) {
        for (const c of activeChips) {
          const cl = c.replace(/^[fghpqrFGH]\([a-zA-Z]\)\s*=\s*/i, '').trim();
          if (parseEquationSyntax(cl)) { candidate = cl; break; }
          if (parseEquationSyntax(c)) { candidate = c; break; }
        }
        if (!candidate) candidate = activeChips[0];
      }

      if (!candidate) {
        // Try extracting specific math patterns directly from problem text
        const mathMatches = probText.match(/(?:[+-]?\d+(?:\.\d+)?\s*[+-]\s*\d*(?:\.\d+)?i|[+-]?\d*\.?\d*i|\(?[+-]?\d+\s*[+-]\s*\d*i\)?\s*(?:[+\-*/]|\^2)\s*\(?[+-]?\d+\s*[+-]\s*\d*i\)?|x\^2\s*=\s*[+-]?\d+|[+-]?\d*\.?\d*(?:sqrt|√)\(?[-]?\d+\)?)/i);
        if (mathMatches) candidate = normalizeEditedMathText(mathMatches[0]);
      }

      if (!candidate) {
        const rawText = normalizeEditedMathText((probEl.textContent || '').replace(/^Problem:\s*/i, ''));
        if (rawText) candidate = rawText;
      }

      if (candidate) {
        inputEl.value = candidate;
        updateQuestionCardRealtime(qNum, true);
      }
    }

    function updateQuestionCardRealtime(qNum, fromProbEdit = false) {
      const inputEl = document.getElementById(`qinput-${qNum}`);
      if (!inputEl) return;
      const rawExpr = (inputEl.value || '').trim();

      const resetBtn = document.getElementById(`qreset-${qNum}`);
      if (resetBtn) resetBtn.style.display = 'inline-flex';

      if (!rawExpr) return;

      const parsed = parseEquationSyntax(rawExpr);
      const toolResult = runToolOnParsed(parsed, rawExpr);
      let graphData = parsed ? buildGraphDataFromParsed(parsed, rawExpr) : null;

      if (!graphData && rawExpr.toLowerCase().includes('x') && !rawExpr.includes('y')) {
        const compiled = compileMathFunction(rawExpr);
        if (compiled) {
          const y0 = compiled(0);
          const pts = (!isNaN(y0) && isFinite(y0)) ? [{ x: 0, y: y0, type: 'point', color: '#a855f7', label: `(0, ${Number(y0.toFixed(2))})` }] : [];
          // Find real roots in [-15, 15]
          for (let x = -15; x < 15; x += 0.5) {
            const ya = compiled(x), yb = compiled(x + 0.5);
            if (Math.abs(ya) < 1e-7) {
              pts.push({ x: Number(x.toFixed(2)), y: 0, type: 'vertex', color: '#34d399', label: `(${Number(x.toFixed(2))}, 0)` });
            } else if (ya * yb < 0 && isFinite(ya) && isFinite(yb)) {
              let lo = x, hi = x + 0.5;
              for (let it = 0; it < 20; it++) {
                const mid = 0.5 * (lo + hi);
                if (compiled(lo) * compiled(mid) <= 0) hi = mid; else lo = mid;
              }
              const rx = 0.5 * (lo + hi);
              if (Math.abs(compiled(rx)) < 1e-2) {
                pts.push({ x: Number(rx.toFixed(2)), y: 0, type: 'vertex', color: '#34d399', label: `(${Number(rx.toFixed(2))}, 0)` });
              }
            }
          }
          graphData = {
            id: `live_${qNum}_${rawExpr}`,
            type: 'function',
            fn: compiled,
            points: pts,
            curveColor: '#38bdf8',
            label: `f(x) = ${rawExpr}`
          };
        }
      }

      const ansWrap = document.getElementById(`qanswrap-${qNum}`);
      const ansBadge = document.getElementById(`qansbadge-${qNum}`);
      const ansVal = document.getElementById(`qansval-${qNum}`);
      const workWrap = document.getElementById(`qworkwrap-${qNum}`);
      const workBadge = document.getElementById(`qworkbadge-${qNum}`);
      const workVal = document.getElementById(`qworkval-${qNum}`);

      if (toolResult) {
        if (ansWrap) ansWrap.style.display = 'block';
        if (ansBadge) {
          ansBadge.className = 'box-badge badge-live-edited';
          ansBadge.innerHTML = '⚡ Live Recalculated Answer (Edited)';
        }
        if (ansVal) {
          ansVal.innerHTML = `
            <div style="font-size:0.78rem; color:#38bdf8; margin-bottom:4px; font-weight:600;">${toolResult.title}</div>
            <div>${toolResult.outputVal}</div>
          `;
        }
        if (workWrap && workVal) {
          if (toolResult.steps && toolResult.steps.length > 0) {
            workWrap.style.display = 'block';
            if (workBadge) {
              workBadge.className = 'box-badge badge-live-edited';
              workBadge.innerHTML = '⚡ Live Step-by-Step Work (Recalculated)';
            }
            workVal.innerHTML = `<div style="line-height:1.7;">${toolResult.steps.join('<br>')}</div>`;
          } else {
            workWrap.style.display = 'none';
          }
        }
      } else if (graphData && graphData.fn) {
        const y0 = graphData.fn(0);
        const y1 = graphData.fn(1);
        const ym1 = graphData.fn(-1);
        const zeros = (graphData.points || []).filter(p => Math.abs(p.y) < 1e-5).map(p => p.label).join(', ') || 'None in [-15, 15]';
        if (ansWrap) ansWrap.style.display = 'block';
        if (ansBadge) {
          ansBadge.className = 'box-badge badge-live-edited';
          ansBadge.innerHTML = '⚡ Live Function Evaluation (Edited)';
        }
        if (ansVal) {
          ansVal.innerHTML = `y-intercept: <strong>(0, ${isFinite(y0) ? Number(y0.toFixed(3)) : 'Undef'})</strong> &nbsp;|&nbsp; Real Zeros: <strong>${zeros}</strong> &nbsp;|&nbsp; f(1) = <strong>${isFinite(y1) ? Number(y1.toFixed(3)) : 'Undef'}</strong>, f(-1) = <strong>${isFinite(ym1) ? Number(ym1.toFixed(3)) : 'Undef'}</strong>`;
        }
        if (workWrap) workWrap.style.display = 'none';
      } else {
        if (ansWrap) ansWrap.style.display = 'block';
        if (ansBadge) {
          ansBadge.className = 'box-badge badge-live-edited';
          ansBadge.innerHTML = '✏️ Live Input (Editing)';
        }
        if (ansVal) {
          ansVal.innerHTML = `<span style="color:var(--text-muted); font-size:0.85rem;">Input: <code>${rawExpr}</code> &nbsp;— type a complete expression (e.g. <code>2 + i</code>, <code>(-6 + sqrt(-54))/3</code>, <code>(2 + i)(2 - i)</code>, <code>x^2 = -9</code>) to calculate live results.</span>`;
        }
        if (workWrap) workWrap.style.display = 'none';
      }

      // Live Graph Update
      const graphWrap = document.getElementById(`qgraphwrap-${qNum}`);
      const graphTitle = document.getElementById(`qgraphtitle-${qNum}`);
      const canvasEl = document.getElementById(`qcanvas-${qNum}`);
      if (graphData && canvasEl) {
        if (graphWrap) graphWrap.style.display = 'block';
        if (graphTitle) graphTitle.innerHTML = `📊 Live Interactive Graph (Edited): <code>${rawExpr}</code>`;
        canvasEl.setAttribute('data-graph-eq', encodeURIComponent(rawExpr));
        renderUniversalGraph(canvasEl.id, graphData);
      } else if (graphWrap) {
        graphWrap.style.display = 'none';
      }
    }

    function resetQuestionCardRealtime(qNum) {
      const orig = originalCardStates[qNum];
      if (!orig) return;

      const probEl = document.getElementById(`qprob-${qNum}`);
      if (probEl && orig.problemHtml) probEl.innerHTML = orig.problemHtml;

      const inputEl = document.getElementById(`qinput-${qNum}`);
      if (inputEl) inputEl.value = orig.initialExpr || '';

      const resetBtn = document.getElementById(`qreset-${qNum}`);
      if (resetBtn) resetBtn.style.display = 'none';

      const ansBadge = document.getElementById(`qansbadge-${qNum}`);
      if (ansBadge) {
        ansBadge.className = 'box-badge badge-ans';
        ansBadge.innerHTML = 'Verified Answer';
      }
      const ansVal = document.getElementById(`qansval-${qNum}`);
      if (ansVal) ansVal.innerHTML = orig.answerHtml || '';

      const workWrap = document.getElementById(`qworkwrap-${qNum}`);
      const workBadge = document.getElementById(`qworkbadge-${qNum}`);
      const workVal = document.getElementById(`qworkval-${qNum}`);
      if (workBadge) {
        workBadge.className = 'box-badge badge-work';
        workBadge.innerHTML = 'Step-by-Step Work';
      }
      if (workVal) workVal.innerHTML = orig.workHtml || '';
      if (workWrap) workWrap.style.display = orig.workHtml ? 'block' : 'none';

      const graphWrap = document.getElementById(`qgraphwrap-${qNum}`);
      const graphTitle = document.getElementById(`qgraphtitle-${qNum}`);
      const canvasEl = document.getElementById(`qcanvas-${qNum}`);
      if (orig.graphEq && canvasEl) {
        if (graphWrap) graphWrap.style.display = 'block';
        if (graphTitle) graphTitle.innerHTML = `📊 Interactive Problem Graph: <code>${orig.graphEq}</code>`;
        canvasEl.setAttribute('data-graph-eq', encodeURIComponent(orig.graphEq));
        const parsed = parseEquationSyntax(orig.graphEq);
        let gData = parsed ? buildGraphDataFromParsed(parsed, orig.graphEq) : null;
        if (!gData && orig.graphEq.includes('x')) {
          const fn = compileMathFunction(orig.graphEq);
          if (fn) gData = { id: `inline_${canvasEl.id}`, type: 'function', fn, points: [], curveColor: '#38bdf8', label: orig.graphEq };
        }
        if (gData) renderUniversalGraph(canvasEl.id, gData);
      } else if (graphWrap) {
        graphWrap.style.display = 'none';
      }
    }

    function parseQuestionCard(sec, qNum) {
      const titleMatch = sec.match(/(?:###\s+\*?\*?(Questions?[^\n*#]+)\*?\*?|\*\s+\*?\*?(Question\s+\d+[a-zA-Z0-9–-]*:?|Q\d+:?)\*?\*?)/i);
      let qTitle = titleMatch ? (titleMatch[1] || titleMatch[2]).replace(/:$/, '').trim() : `Question ${qNum}`;
      const numMatch = qTitle.match(/\b(?:Question|Q)\s*(\d+)\b/i);
      const effectiveNum = numMatch ? numMatch[1] : qNum;

      let probMatch = sec.match(/\*\s+\*\*Problem:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
      let problem = probMatch ? probMatch[1].trim() : '';
      if (!problem) {
        const inlineProb = sec.match(/(?:\*\*Question\s+\d+:?|\*\*Q\d+:?)\s*([^\n*]+)/i);
        if (inlineProb) problem = inlineProb[1].trim();
      }

      const ansMatch = sec.match(/\*\s+\*\*Answer[s]?:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
      let answer = ansMatch ? ansMatch[1].trim() : '';
      if (!answer) {
        const rewriteMatch = sec.match(/\*\s+\*\*Rewrite(?:\s*\(.*?\))?:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
        const solMatch = sec.match(/\*\s+\*\*Solution(?:\s*\(.*?\))?:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
        if (rewriteMatch || solMatch) {
          const parts = [];
          if (rewriteMatch) parts.push(`* **Part 1 (Rewrite Form):** ${rewriteMatch[1].trim()}`);
          if (solMatch) parts.push(`* **Part 2 (Interval Notation):** ${solMatch[1].trim()}`);
          answer = parts.join('\n');
        }
      }

      const ruleMatch = sec.match(/\*\s+\*\*The (?:Universal )?Rule.*:\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
      const rule = ruleMatch ? ruleMatch[1].trim() : '';

      const workMatch = sec.match(/\*\s+\*\*(?:Step-by-Step\s+)?(?:Work|Check|Steps|Explanation):\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
      const work = workMatch ? workMatch[1].trim() : '';

      const tipMatch = sec.match(/\*\s+\*\*(?:Pro-Tip|Watch Out):\*\*\s*(.*?)(?=\n\*\s+\*\*|\n---|$)/s);
      const tip = tipMatch ? tipMatch[1].trim() : '';

      const graphEq = extractGraphableFromQuestion(problem, answer, '', sec);
      const initialExpr = extractInitialEditableExpr(problem, answer, graphEq, sec);
      const cardId = `qcard-${effectiveNum}`;
      const canvasId = `qcanvas-${effectiveNum}`;
      const queryTarget = initialExpr || graphEq || normalizeLatexToAscii(problem).substring(0, 60);

      const probHtml = `<strong>Problem:</strong> ${formatMath(problem)}`;
      const ansHtml = formatMath(answer);
      const workHtml = formatMath(work);

      originalCardStates[effectiveNum] = {
        problemHtml: probHtml,
        answerHtml: ansHtml,
        workHtml: workHtml,
        graphEq: graphEq || '',
        initialExpr: initialExpr || ''
      };

      const safeAttrExpr = (initialExpr || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

      return `
        <div class="q-card" id="${cardId}">
          <div class="q-card-header">
            <div class="q-title-wrap">
              <span class="q-number">${qTitle}</span>
              ${graphEq ? `<span class="q-badge">📊 Graph Attached</span>` : `<span class="q-badge" style="opacity:0.85;">✏️ Inline Live Editable</span>`}
            </div>
            <div class="q-actions">
              <button class="btn-solve-link" onclick="openInDedicatedGrapher(encodeURIComponent(document.getElementById('qinput-${effectiveNum}') ? document.getElementById('qinput-${effectiveNum}').value : '${encodeURIComponent(queryTarget)}'))">
                📈 Open in Grapher
              </button>
              <button class="btn-dyn-toggle" onclick="setOmniExample(document.getElementById('qinput-${effectiveNum}') ? document.getElementById('qinput-${effectiveNum}').value : decodeURIComponent('${encodeURIComponent(queryTarget)}'))">
                ⚡ Solve in Omni-Engine
              </button>
            </div>
          </div>

          ${problem ? `
            <div class="q-problem" id="qprob-${effectiveNum}" contenteditable="true" spellcheck="false" oninput="onProblemTextEdited('${effectiveNum}')" title="Click anywhere in this problem text to edit numbers or equations in real time!">
              ${probHtml}
            </div>
          ` : ''}

          <div class="inline-editor-bar">
            <span class="inline-editor-label">✏️ Live Edit Equation:</span>
            <input type="text" class="inline-live-input" id="qinput-${effectiveNum}" value="${safeAttrExpr}" placeholder="Type or edit equation/numbers here to recalculate Answer, Steps & Graph in real time..." oninput="updateQuestionCardRealtime('${effectiveNum}')">
            <button class="btn-inline-reset" id="qreset-${effectiveNum}" style="display:none;" onclick="resetQuestionCardRealtime('${effectiveNum}')">↺ Reset Original</button>
          </div>

          <div class="box-answer" id="qanswrap-${effectiveNum}" style="${answer ? '' : 'display:none;'}">
            <span class="box-badge badge-ans" id="qansbadge-${effectiveNum}">Verified Answer</span>
            <div class="ans-value" id="qansval-${effectiveNum}">${ansHtml}</div>
          </div>

          <div class="graph-card" id="qgraphwrap-${effectiveNum}" style="${graphEq ? '' : 'display:none;'}">
            <div class="graph-header">
              <span class="graph-title" id="qgraphtitle-${effectiveNum}">📊 Interactive Problem Graph: <code>${graphEq}</code></span>
              <div class="graph-controls">
                <button class="btn-ctrl" onclick="zoomActiveGraph('${canvasId}', 0.8)">− Zoom Out</button>
                <button class="btn-ctrl" onclick="resetActiveGraph('${canvasId}')">⟲ Reset</button>
                <button class="btn-ctrl" onclick="zoomActiveGraph('${canvasId}', 1.25)">+ Zoom In</button>
                <button class="btn-ctrl" onclick="openInDedicatedGrapher(encodeURIComponent(document.getElementById('qinput-${effectiveNum}') ? document.getElementById('qinput-${effectiveNum}').value : '${encodeURIComponent(graphEq)}'))">↗ Full Grapher</button>
              </div>
            </div>
            <canvas id="${canvasId}" class="inline-q-canvas" data-graph-eq="${encodeURIComponent(graphEq)}" width="720" height="340" style="width:100%; max-width:720px; height:auto; background:#070d19; border-radius:6px; cursor:crosshair; display:block; margin:0 auto;"></canvas>
          </div>

          ${rule ? `
            <div class="box-rule">
              <span class="box-badge badge-rule">The Rule / General Formula</span>
              <div>${formatMath(rule)}</div>
            </div>` : ''}

          <div class="box-work" id="qworkwrap-${effectiveNum}" style="${work ? '' : 'display:none;'}">
            <span class="box-badge badge-work" id="qworkbadge-${effectiveNum}">Step-by-Step Work</span>
            <div id="qworkval-${effectiveNum}">${workHtml}</div>
          </div>

          ${tip ? `
            <div class="box-tip">
              <span class="box-badge badge-tip">Watch Out / Tip</span>
              <div>${formatMath(tip)}</div>
            </div>` : ''}
        </div>
      `;
    }

    // ==========================================
    // Tab & Navigation Switching
    // ==========================================

    function switchMainTab(tab) {
      document.getElementById('tabDoc').style.display = tab === 'doc' ? 'block' : 'none';
      document.getElementById('tabSolver').style.display = tab === 'solver' ? 'block' : 'none';
      const tabGraphEl = document.getElementById('tabGraph');
      if (tabGraphEl) tabGraphEl.style.display = tab === 'graph' ? 'block' : 'none';
      document.getElementById('tabOmni').style.display = tab === 'omni' ? 'block' : 'none';

      document.getElementById('tabDocBtn').classList.toggle('active', tab === 'doc');
      document.getElementById('tabSolverBtn').classList.toggle('active', tab === 'solver');
      const tabGraphBtnEl = document.getElementById('tabGraphBtn');
      if (tabGraphBtnEl) tabGraphBtnEl.classList.toggle('active', tab === 'graph');
      document.getElementById('tabOmniBtn').classList.toggle('active', tab === 'omni');
      document.getElementById('tabOmniBtn').style.display = tab === 'omni' ? 'flex' : 'none';

      if (tab === 'graph') {
        setTimeout(plotCustomFunction, 40);
      } else if (tab === 'doc') {
        setTimeout(renderAllInlineGraphs, 40);
      }
    }

    function showSolver(type) {
      const types = [
        'synthetic', 'poly-zeros', 'rational', 'ineq', 'explog', 'conics', 'systems',
        'quadratic', 'quad-eq', 'abs', 'circle', 'radical', 'complex', 'projectile', 'dist-mid', 'poly-eval'
      ];
      types.forEach(t => {
        const el = document.getElementById(`solver-${t}`);
        if (el) el.style.display = (t === type) ? 'block' : 'none';
        const pill = document.getElementById(`pill-${t}`);
        if (pill) pill.classList.toggle('active', t === type);
      });
      if (type === 'synthetic') runSynthetic();
      if (type === 'poly-zeros') runPolyZeros();
      if (type === 'rational') runRationalSolver();
      if (type === 'ineq') runIneqSolver();
      if (type === 'explog') runExpLogSolver();
      if (type === 'conics') runConicsSolver();
      if (type === 'systems') runSystemsSolver();
      if (type === 'quadratic') runQuad();
      if (type === 'quad-eq') runQuadEq();
      if (type === 'abs') runAbs();
      if (type === 'circle') runCirc();
      if (type === 'radical') runRad();
      if (type === 'complex') runComplex();
      if (type === 'projectile') runProjectile();
      if (type === 'dist-mid') runDistMid();
      if (type === 'poly-eval') runPolyEval();
    }

    function launchSolver(type) {
      switchMainTab('solver');
      showSolver(type);
    }

    function launchSolverWithParams(type, params) {
      if (type === 'graph') {
        openInDedicatedGrapher((params && params.expr) || '');
        return;
      }
      switchMainTab('solver');
      showSolver(type);
      if (params) {
        if (type === 'synthetic' && params.coeffs) {
          document.getElementById('syn-coeffs').value = params.coeffs;
          if (params.c !== undefined) document.getElementById('syn-c').value = params.c;
          runSynthetic();
        } else if (type === 'poly-zeros' && params.expr) {
          document.getElementById('pzero-input').value = params.expr;
          runPolyZeros();
        } else if (type === 'rational') {
          if (params.num) document.getElementById('rat-num').value = params.num;
          if (params.den) document.getElementById('rat-den').value = params.den;
          runRationalSolver();
        } else if (type === 'ineq' && params.expr) {
          document.getElementById('ineq-input').value = params.expr;
          runIneqSolver();
        } else if (type === 'explog') {
          if (params.mode) document.getElementById('explog-mode').value = params.mode;
          if (params.a !== undefined) document.getElementById('explog-a').value = params.a;
          if (params.b !== undefined) document.getElementById('explog-b').value = params.b;
          if (params.h !== undefined) document.getElementById('explog-h').value = params.h;
          if (params.k !== undefined) document.getElementById('explog-k').value = params.k;
          if (params.rhs !== undefined) document.getElementById('explog-rhs').value = params.rhs;
          runExpLogSolver();
        } else if (type === 'conics') {
          if (params.type) document.getElementById('conic-type').value = params.type;
          if (params.h !== undefined) document.getElementById('conic-h').value = params.h;
          if (params.k !== undefined) document.getElementById('conic-k').value = params.k;
          if (params.a !== undefined) document.getElementById('conic-a').value = params.a;
          if (params.b !== undefined) document.getElementById('conic-b').value = params.b;
          runConicsSolver();
        } else if (type === 'systems' && params.sys) {
          document.getElementById('sys-input').value = params.sys;
          runSystemsSolver();
        } else if (type === 'quadratic') {
          if (params.a !== undefined) document.getElementById('quad-a').value = params.a;
          if (params.b !== undefined) document.getElementById('quad-b').value = params.b;
          if (params.c !== undefined) document.getElementById('quad-c').value = params.c;
          runQuad();
        } else if (type === 'abs') {
          if (params.a !== undefined) document.getElementById('abs-a').value = params.a;
          if (params.b !== undefined) document.getElementById('abs-b').value = params.b;
          if (params.op !== undefined) document.getElementById('abs-op').value = params.op;
          if (params.c !== undefined) document.getElementById('abs-c').value = params.c;
          runAbs();
        } else if (type === 'circle') {
          if (params.a !== undefined) document.getElementById('circ-a').value = params.a;
          if (params.b !== undefined) document.getElementById('circ-b').value = params.b;
          if (params.c !== undefined) document.getElementById('circ-c').value = params.c;
          if (params.d !== undefined) document.getElementById('circ-d').value = params.d;
          runCirc();
        } else if (type === 'radical') {
          if (params.n !== undefined) document.getElementById('rad-n').value = params.n;
          runRad();
        } else if (type === 'complex') {
          if (params.a1 !== undefined) document.getElementById('cplx-a1').value = params.a1;
          if (params.b1 !== undefined) document.getElementById('cplx-b1').value = params.b1;
          if (params.a2 !== undefined) document.getElementById('cplx-a2').value = params.a2;
          if (params.b2 !== undefined) document.getElementById('cplx-b2').value = params.b2;
          runComplex();
        }
      }
    }

    function loadFile(name) {
      currentFileName = name;
      document.querySelectorAll('.file-item').forEach(el => el.classList.remove('active'));
      const navEl = document.getElementById(`nav-${encodeURIComponent(name)}`);
      if (navEl) navEl.classList.add('active');
      const topSelect = document.getElementById('topAssignmentSelect');
      if (topSelect && topSelect.value !== name) {
        topSelect.value = name;
      }

      const content = answersData[name] || 'File not found.';
      docContainer.innerHTML = renderMarkdownToHtml(content);
      docContainer.scrollTop = 0;
      switchMainTab('doc');
      setTimeout(renderAllInlineGraphs, 40);
    }

    function buildSolverCanvasBlock(canvasId, title) {
      return `
        <div class="graph-card" style="margin-top:16px;">
          <div class="graph-header">
            <span class="graph-title">📊 ${title}</span>
            <div class="graph-controls">
              <button class="btn-ctrl" onclick="zoomActiveGraph('${canvasId}', 0.8)">− Zoom Out</button>
              <button class="btn-ctrl" onclick="resetActiveGraph('${canvasId}')">⟲ Reset</button>
              <button class="btn-ctrl" onclick="zoomActiveGraph('${canvasId}', 1.25)">+ Zoom In</button>
            </div>
          </div>
          <canvas id="${canvasId}" width="720" height="360" style="width:100%; max-width:720px; height:auto; background:#070d19; border-radius:6px; cursor:crosshair; display:block; margin:0 auto;"></canvas>
        </div>
      `;
    }

    // ==========================================
    // Interactive Solvers Implementation (Tab 2)
    // ==========================================

    function runSynthetic() {
      const raw = document.getElementById('syn-coeffs').value.trim();
      const c = parseFloat(document.getElementById('syn-c').value) || 0;
      if (!raw) return;
      const coeffs = raw.includes('x') ? parseAnyPolyCoeffs(raw) : raw.split(/\s+/).map(Number).filter(x => !isNaN(x));
      if (coeffs.length === 0) return;

      let multRow = [0];
      let resRow = [coeffs[0]];
      for (let i = 1; i < coeffs.length; i++) {
        let prod = resRow[resRow.length - 1] * c;
        multRow.push(prod);
        resRow.push(coeffs[i] + prod);
      }
      const quotientCoeffs = resRow.slice(0, -1);
      const rem = resRow[resRow.length - 1];
      let qStr = formatPolyCoeffs(quotientCoeffs);

      document.getElementById('syn-out').innerHTML = `
        <div class="tableau-wrap">
          <div class="tab-row">
            <span class="tab-cell tab-c-box">${c}</span>
            ${coeffs.map(x => `<span class="tab-cell">${x}</span>`).join('')}
          </div>
          <div class="tab-row">
            <span class="tab-cell tab-c-box">&nbsp;</span>
            ${multRow.map(x => `<span class="tab-cell" style="color:#38bdf8;">${x}</span>`).join('')}
          </div>
          <div class="tab-row">
            <span class="tab-cell tab-c-box">&nbsp;</span>
            ${resRow.map(x => `<span class="tab-cell tab-line" style="color:#34d399; font-weight:bold;">${x}</span>`).join('')}
          </div>
        </div>
        <div class="solver-out-box">
          <div class="out-label">Quotient & Remainder</div>
          <div class="out-val">q(x) = ${qStr} &nbsp;|&nbsp; Remainder = ${rem}</div>
          <ul class="out-steps">
            <li>Division Algorithm: <strong>P(x) = (x - ${c})(${qStr}) + (${rem})</strong></li>
            <li>Remainder Theorem: <strong>P(${c}) = ${rem}</strong></li>
            <li>Factor Theorem: Is ${c} a zero of P(x)? <strong>${rem === 0 ? 'YES (remainder is 0)' : 'NO (remainder is not 0)'}</strong></li>
          </ul>
          ${buildSolverCanvasBlock('synCanvas', `Polynomial P(x) = ${formatPolyCoeffs(coeffs)} & Point (${c}, ${rem})`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildPolynomialGraphData(coeffs, formatPolyCoeffs(coeffs));
        gd.points.push({ x: c, y: rem, type: 'vertex', color: '#fbbf24', label: `P(${c}) = ${rem}` });
        renderUniversalGraph('synCanvas', gd);
      }, 20);
    }

    function runPolyZeros() {
      const raw = (document.getElementById('pzero-input').value || '').trim();
      if (!raw) return;
      const coeffs = (raw.includes('x') || raw.includes('('))
        ? parseAnyPolyCoeffs(raw.replace(/^[fghpqr]\(x\)\s*=\s*/i, '').replace(/=\s*0$/, ''))
        : raw.split(/\s+/).map(Number).filter(x => !isNaN(x));
      if (coeffs.length < 2) return;

      const deg = coeffs.length - 1;
      const lead = coeffs[0];
      const constVal = coeffs[coeffs.length - 1];
      const pFacs = getFactorsJS(constVal);
      const qFacs = getFactorsJS(lead);
      const pqSet = new Set();
      pFacs.forEach(p => qFacs.forEach(q => pqSet.add(`±${fracStr(p, q)}`)));

      const roots = findRationalRootsJS(coeffs);
      const counts = {};
      roots.forEach(r => {
        const k = r.toFixed(4);
        counts[k] = (counts[k] || 0) + 1;
      });
      const zerosList = Object.keys(counts).map(k => {
        const r = parseFloat(k);
        const m = counts[k];
        return `x = ${Number(r.toFixed(3))} (Multiplicity ${m}: ${m % 2 !== 0 ? 'Crosses x-axis' : 'Touches & turns around'})`;
      });

      const proto = (deg % 2 === 0)
        ? (lead > 0 ? 'Rises left & rises right (↖ ↗)' : 'Falls left & falls right (↙ ↘)')
        : (lead > 0 ? 'Falls left & rises right (↙ ↗)' : 'Rises left & falls right (↖ ↘)');

      document.getElementById('pzero-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Polynomial Zeros, Multiplicity & End Behavior</div>
          <div class="out-val">${zerosList.join(' &nbsp;|&nbsp ') || 'No rational zeros found'}</div>
          <ul class="out-steps">
            <li>Expanded Form: <strong>f(x) = ${formatPolyCoeffs(coeffs)}</strong> (Degree n = ${deg}, Leading Coeff aₙ = ${lead})</li>
            <li>End Behavior Prototype: <strong>${proto}</strong> &nbsp;|&nbsp; Max Turning Points: <strong>${deg - 1}</strong></li>
            <li>Factors of constant p (${constVal}): ±{${pFacs.join(', ')}} &nbsp;|&nbsp; Factors of leading coeff q (${lead}): ±{${qFacs.join(', ')}}</li>
            <li>Possible Rational Zeros (p/q): <strong>${Array.from(pqSet).join(', ')}</strong></li>
            <li>y-intercept: <strong>(0, ${constVal})</strong></li>
          </ul>
          ${buildSolverCanvasBlock('pzeroCanvas', `Polynomial Graph: f(x) = ${formatPolyCoeffs(coeffs)}`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildPolynomialGraphData(coeffs, formatPolyCoeffs(coeffs));
        renderUniversalGraph('pzeroCanvas', gd);
      }, 20);
    }

    function runRationalSolver() {
      const numStr = (document.getElementById('rat-num').value || '1').trim();
      const denStr = (document.getElementById('rat-den').value || 'x').trim();
      const numCoeffs = parseAnyPolyCoeffs(numStr);
      const denCoeffs = parseAnyPolyCoeffs(denStr);
      const gd = buildRationalGraphData(numCoeffs, denCoeffs, `(${numStr})/(${denStr})`);

      const vertStr = gd.vertAsymptotes && gd.vertAsymptotes.length > 0 ? gd.vertAsymptotes.map(v => 'x = ' + v.label).join(', ') : 'None';
      const horizStr = gd.horizAsymptote ? gd.horizAsymptote.eq : 'None';
      const slantStr = gd.slantAsymptote ? gd.slantAsymptote.eq : 'None';
      const holesStr = gd.points.filter(p => p.type === 'hole').map(p => p.label).join(', ') || 'None';
      const xInts = gd.points.filter(p => p.y === 0 && p.type !== 'hole').map(p => p.label).join(', ') || 'None';
      const yInt = gd.points.find(p => p.x === 0 && p.type !== 'hole')?.label || 'None (undefined at x = 0)';
      const excl = findRationalRootsJS(denCoeffs).map(r => Number(r.toFixed(3)));
      const domStr = excl.length ? `{x | x ≠ ${Array.from(new Set(excl)).join(', ')}}` : '(-∞, ∞)';

      document.getElementById('rat-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Rational Function Complete Analysis</div>
          <div class="out-val">VA: ${vertStr} &nbsp;|&nbsp; HA: ${horizStr} &nbsp;|&nbsp; Slant: ${slantStr} &nbsp;|&nbsp; Holes: ${holesStr}</div>
          <ul class="out-steps">
            <li>Expanded Numerator P(x) = <strong>${formatPolyCoeffs(numCoeffs)}</strong> (deg ${numCoeffs.length - 1})</li>
            <li>Expanded Denominator Q(x) = <strong>${formatPolyCoeffs(denCoeffs)}</strong> (deg ${denCoeffs.length - 1})</li>
            <li>Domain: <strong>${domStr}</strong></li>
            <li>Removable Discontinuities (Holes): <strong>${holesStr}</strong></li>
            <li>Vertical Asymptote(s): <strong>${vertStr}</strong></li>
            <li>Horizontal Asymptote: <strong>${horizStr}</strong> &nbsp;|&nbsp; Slant (Oblique) Asymptote: <strong>${slantStr}</strong></li>
            <li>x-intercept(s): <strong>${xInts}</strong> &nbsp;|&nbsp; y-intercept: <strong>${yInt}</strong></li>
          </ul>
          ${buildSolverCanvasBlock('ratSolverCanvas', `Rational Function Graph: f(x) = (${numStr}) / (${denStr})`)}
        </div>
      `;
      setTimeout(() => {
        renderUniversalGraph('ratSolverCanvas', gd);
      }, 20);
    }

    function runIneqSolver() {
      const raw = (document.getElementById('ineq-input').value || '').trim();
      if (!raw) return;
      const parsed = parseEquationSyntax(raw);
      if (!parsed || (parsed.type !== 'poly_ineq' && parsed.type !== 'rat_ineq')) {
        document.getElementById('ineq-out').innerHTML = `<div class="solver-out-box"><div class="out-val" style="color:#f87171;">Enter a polynomial or rational inequality with &lt;, &lt;=, &gt;, or &gt;= (e.g. "(x - 2)/(x + 3) > 1" or "x^3 - 3x - 2 < 0").</div></div>`;
        return;
      }
      const numC = parsed.type === 'poly_ineq' ? parsed.coeffs : parsed.numCoeffs;
      const denC = parsed.type === 'poly_ineq' ? [1] : parsed.denCoeffs;
      const sc = solveSignChartInequalityJS(numC, denC, parsed.op);

      const tableRows = sc.chartRows.map(r => `
        <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
          <td style="padding:8px; font-family:monospace; color:#38bdf8;">${r.interval}</td>
          <td style="padding:8px; font-family:monospace;">x = ${r.testX}</td>
          <td style="padding:8px; font-family:monospace;">${r.val}</td>
          <td style="padding:8px; font-weight:700; color:${r.sign.startsWith('+') ? '#34d399' : '#f43f5e'};">${r.sign}</td>
          <td style="padding:8px; font-weight:700;">${r.satisfies ? '✅ YES (In Solution)' : '❌ NO'}</td>
        </tr>
      `).join('');

      document.getElementById('ineq-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Interval Notation Solution Set</div>
          <div class="out-val">${sc.intervalStr}</div>
          <ul class="out-steps">
            <li>Standardized Inequality (RHS = 0): <strong>${ parsed.type === 'poly_ineq' ? `${formatPolyCoeffs(numC)} ${parsed.op} 0` : `(${formatPolyCoeffs(numC)}) / (${formatPolyCoeffs(denC)}) ${parsed.op} 0` }</strong></li>
            <li>Zeros of Numerator: <strong>${sc.numRoots.length ? sc.numRoots.map(formatEndpoint).join(', ') : 'None'}</strong></li>
            ${parsed.type === 'rat_ineq' ? `<li>Undefined Poles of Denominator (Always Open Parentheses): <strong>${sc.denRoots.length ? sc.denRoots.map(formatEndpoint).join(', ') : 'None'}</strong></li>` : ''}
            ${sc.isolatedPoints && sc.isolatedPoints.length > 0 ? `<li>Isolated Boundary Solution(s): <strong>{${sc.isolatedPoints.map(formatEndpoint).join(', ')}}</strong></li>` : ''}
          </ul>
          <div style="margin-top:12px; overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem; text-align:left; background:rgba(0,0,0,0.25); border-radius:6px;">
              <thead>
                <tr style="border-bottom:2px solid var(--border); color:var(--text-muted);">
                  <th style="padding:8px;">Test Interval</th>
                  <th style="padding:8px;">Test Point</th>
                  <th style="padding:8px;">f(x) Value</th>
                  <th style="padding:8px;">Sign</th>
                  <th style="padding:8px;">Satisfies ${parsed.op} 0?</th>
                </tr>
              </thead>
              <tbody>${tableRows}</tbody>
            </table>
          </div>
          ${buildSolverCanvasBlock('ineqCanvas', `Function Sign Graph: ${raw}`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildGraphDataFromParsed(parsed, raw);
        if (gd) renderUniversalGraph('ineqCanvas', gd);
      }, 20);
    }

    function runExpLogSolver() {
      const mode = document.getElementById('explog-mode').value;
      const a = parseFloat(document.getElementById('explog-a').value) || 1;
      const b = parseFloat(document.getElementById('explog-b').value) || 2;
      const h = parseFloat(document.getElementById('explog-h').value) || 0;
      const k = parseFloat(document.getElementById('explog-k').value) || 0;
      const rhs = parseFloat(document.getElementById('explog-rhs').value) || 0;

      if (mode === 'exp') {
        const isolated = (rhs - k) / a;
        const hasSol = isolated > 0 && b > 0 && b !== 1;
        const solX = hasSol ? (Math.log(isolated) / Math.log(b) + h) : NaN;
        const yInt = a * Math.pow(b, -h) + k;
        document.getElementById('explog-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">Exponential Function & Equation Solution</div>
            <div class="out-val">HA: y = ${k} &nbsp;|&nbsp; Range: ${a > 0 ? `(${k}, ∞)` : `(-∞, ${k})`} &nbsp;|&nbsp; f(x) = ${rhs} ⇒ ${hasSol ? `x ≈ ${solX.toFixed(4)}` : 'No Real Solution'}</div>
            <ul class="out-steps">
              <li>Function: <strong>f(x) = ${a} · (${b})^(x - ${h}) + (${k})</strong></li>
              <li>Domain: <strong>(-∞, ∞)</strong> &nbsp;|&nbsp; Range: <strong>${a > 0 ? `(${k}, ∞)` : `(-∞, ${k})`}</strong> &nbsp;|&nbsp; Horizontal Asymptote: <strong>y = ${k}</strong></li>
              <li>Anchor Point (x = h): <strong>(${h}, ${(a + k).toFixed(3)})</strong> &nbsp;|&nbsp; y-intercept: <strong>(0, ${yInt.toFixed(3)})</strong></li>
              <li>Solving ${a}·(${b})^(x - ${h}) + (${k}) = ${rhs}: (${b})^(x - ${h}) = ${isolated.toFixed(4)} → ${hasSol ? `x = ${h} + ln(${isolated.toFixed(4)})/ln(${b}) = <strong>${solX.toFixed(4)}</strong>` : '<strong>No Real Solution (exponential cannot be ≤ 0)</strong>'}</li>
            </ul>
            ${buildSolverCanvasBlock('explogCanvas', `Exponential Graph: f(x) = ${a}·(${b})^(x - ${h}) + ${k}`)}
          </div>
        `;
        setTimeout(() => {
          const gd = buildGraphDataFromParsed({ type: 'exp_func', a, base: b, h, k, rhs, solX: hasSol ? solX : undefined }, '');
          renderUniversalGraph('explogCanvas', gd);
        }, 20);
      } else if (mode === 'log') {
        const safeB = (b > 0 && b !== 1) ? b : Math.E;
        const expVal = (rhs - k) / a;
        const solX = h + Math.pow(safeB, expVal);
        document.getElementById('explog-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">Logarithmic Function & Equation Solution</div>
            <div class="out-val">VA: x = ${h} &nbsp;|&nbsp; Domain: (${h}, ∞) &nbsp;|&nbsp; f(x) = ${rhs} ⇒ x = ${solX.toFixed(4)}</div>
            <ul class="out-steps">
              <li>Function: <strong>f(x) = ${a} · log_${safeB}(x - ${h}) + (${k})</strong></li>
              <li>Domain Restriction: x - ${h} &gt; 0 ⇒ <strong>(${h}, ∞)</strong> &nbsp;|&nbsp; Range: <strong>(-∞, ∞)</strong> &nbsp;|&nbsp; Vertical Asymptote: <strong>x = ${h}</strong></li>
              <li>Key Points: <strong>(${(h + 1).toFixed(2)}, ${k})</strong> and <strong>(${(h + safeB).toFixed(2)}, ${(a + k).toFixed(2)})</strong></li>
              <li>Solving f(x) = ${rhs}: log_${safeB}(x - ${h}) = ${expVal.toFixed(4)} ⇒ x = ${h} + (${safeB})^(${expVal.toFixed(4)}) = <strong>${solX.toFixed(4)}</strong></li>
            </ul>
            ${buildSolverCanvasBlock('explogCanvas', `Logarithmic Graph: f(x) = ${a}·log_${safeB}(x - ${h}) + ${k}`)}
          </div>
        `;
        setTimeout(() => {
          const gd = buildGraphDataFromParsed({ type: 'log_func', a, base: safeB, h, k, rhs, solX }, '');
          renderUniversalGraph('explogCanvas', gd);
        }, 20);
      } else {
        // Compound / Continuous Growth: P = a, r = b, n = h, t = k, target A = rhs
        const P = a, r = b, n = Math.max(1, h), t = k, targetA = rhs;
        const compA = P * Math.pow(1 + r / n, n * t);
        const contA = P * Math.exp(r * t);
        const doubleT = r !== 0 ? (Math.log(2) / r) : NaN;
        const timeToTarget = (targetA > 0 && P > 0 && r !== 0) ? (Math.log(targetA / P) / r) : NaN;
        document.getElementById('explog-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">Compound Interest, Continuous Growth & Doubling/Half-Life (Ch 4.6)</div>
            <div class="out-val">Periodic A(t) = $${compA.toFixed(2)} &nbsp;|&nbsp; Continuous Pe^(rt) = $${contA.toFixed(2)}</div>
            <ul class="out-steps">
              <li>Inputs: Principal P = ${P}, Rate r = ${r} (${(r*100).toFixed(2)}%), Compoundings/yr n = ${n}, Time t = ${t}</li>
              <li>Periodic Compound Formula A = P(1 + r/n)^(nt) = ${P}(1 + ${r}/${n})^(${n*t}) = <strong>${compA.toFixed(4)}</strong></li>
              <li>Continuous Growth Formula A = Pe^(rt) = ${P}·e^(${r}·${t}) = <strong>${contA.toFixed(4)}</strong></li>
              <li>Doubling / Half-Life Time Constant (ln(2)/|r|): <strong>${Math.abs(doubleT).toFixed(4)} time units</strong></li>
              ${!isNaN(timeToTarget) ? `<li>Time to reach target A = ${targetA} continuously: t = ln(${targetA}/${P}) / ${r} = <strong>${timeToTarget.toFixed(4)}</strong></li>` : ''}
            </ul>
            ${buildSolverCanvasBlock('explogCanvas', `Growth Curve A(t) = ${P}·e^(${r}t)`)}
          </div>
        `;
        setTimeout(() => {
          const fn = (x) => P * Math.exp(r * x);
          renderUniversalGraph('explogCanvas', {
            id: `fin_${P}_${r}_${t}`,
            type: 'function',
            fn,
            points: [{ x: 0, y: P, type: 'point', color: '#a855f7', label: `(0, ${P})` }, { x: t, y: contA, type: 'vertex', color: '#34d399', label: `(${t}, ${contA.toFixed(1)})` }],
            curveColor: '#38bdf8',
            label: `A(t) = ${P}e^(${r}t)`
          });
        }, 20);
      }
    }

    function runConicsSolver() {
      const cType = document.getElementById('conic-type').value;
      const h = parseFloat(document.getElementById('conic-h').value) || 0;
      const k = parseFloat(document.getElementById('conic-k').value) || 0;
      const a = Math.max(0.1, Math.abs(parseFloat(document.getElementById('conic-a').value) || 5));
      const b = Math.max(0.1, Math.abs(parseFloat(document.getElementById('conic-b').value) || 3));

      let parsed = null;
      if (cType === 'ellipse') {
        parsed = { type: 'ellipse', h, k, rx: a, ry: b };
      } else if (cType === 'hyp-h') {
        parsed = { type: 'hyperbola', h, k, a, b, transverse: 'horizontal' };
      } else {
        parsed = { type: 'hyperbola', h, k, a, b, transverse: 'vertical' };
      }

      const res = runToolOnParsed(parsed, '');
      const gd = buildGraphDataFromParsed(parsed, '');

      document.getElementById('conic-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">${res.title}</div>
          <div class="out-val">${res.outputVal}</div>
          <ul class="out-steps">
            ${res.steps.map(s => `<li>${s}</li>`).join('')}
          </ul>
          ${buildSolverCanvasBlock('conicCanvas', gd.label)}
        </div>
      `;
      setTimeout(() => {
        renderUniversalGraph('conicCanvas', gd);
      }, 20);
    }

    function runSystemsSolver() {
      const raw = (document.getElementById('sys-input').value || '').trim();
      if (!raw) return;
      const parsed = parseEquationSyntax(raw);
      if (parsed && parsed.type === 'system_2x2') {
        const res = runToolOnParsed(parsed, raw);
        document.getElementById('sys-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">2×2 System Solution</div>
            <div class="out-val">${res.outputVal}</div>
            <ul class="out-steps">
              ${res.steps.map(s => `<li>${s}</li>`).join('')}
            </ul>
            ${buildSolverCanvasBlock('sysCanvas', `System Intersection Graph: ${raw}`)}
          </div>
        `;
        setTimeout(() => {
          renderUniversalGraph('sysCanvas', parsed.graphData);
        }, 20);
        return;
      }

      // Nonlinear System fallback: e.g. "y = x^2 - 4, y = 2x - 1"
      const parts = raw.split(/[,;]/).map(p => p.trim()).filter(Boolean);
      if (parts.length === 2) {
        const fn1 = compileMathFunction(parts[0]);
        const fn2 = compileMathFunction(parts[1]);
        if (fn1 && fn2) {
          // Find numerical intersections in [-25, 25]
          const pts = [];
          let prevDiff = fn1(-25) - fn2(-25);
          for (let x = -24.95; x <= 25; x += 0.05) {
            const currDiff = fn1(x) - fn2(x);
            if (prevDiff * currDiff <= 0 && isFinite(prevDiff) && isFinite(currDiff)) {
              // Refine with bisection
              let lo = x - 0.05, hi = x;
              for (let iter = 0; iter < 25; iter++) {
                const mid = (lo + hi) / 2;
                if ((fn1(lo) - fn2(lo)) * (fn1(mid) - fn2(mid)) <= 0) hi = mid;
                else lo = mid;
              }
              const rx = (lo + hi) / 2;
              const ry = fn1(rx);
              if (!pts.some(p => Math.abs(p.x - rx) < 0.05)) {
                pts.push({ x: rx, y: ry, type: 'vertex', color: '#34d399', label: `(${Number(rx.toFixed(2))}, ${Number(ry.toFixed(2))})` });
              }
            }
            prevDiff = currDiff;
          }
          const solText = pts.length ? pts.map(p => p.label).join(' and ') : 'No Real Intersection';
          document.getElementById('sys-out').innerHTML = `
            <div class="solver-out-box">
              <div class="out-label">Nonlinear System Intersection Solutions (Ch 9.5)</div>
              <div class="out-val">${solText}</div>
              <ul class="out-steps">
                <li>Curve 1 (Blue): <strong>${parts[0]}</strong></li>
                <li>Curve 2 (Green): <strong>${parts[1]}</strong></li>
                <li>Real Intersection Point(s): <strong>${solText}</strong></li>
              </ul>
              ${buildSolverCanvasBlock('sysCanvas', `Nonlinear System Graph: ${parts[0]} & ${parts[1]}`)}
            </div>
          `;
          setTimeout(() => {
            renderUniversalGraph('sysCanvas', {
              id: `nonlin_${raw}`,
              type: 'function',
              fn: fn1,
              fn2: fn2,
              points: pts,
              curveColor: '#38bdf8',
              curve2Color: '#10b981',
              label: `${parts[0]} vs ${parts[1]}`
            });
          }, 20);
          return;
        }
      }
      document.getElementById('sys-out').innerHTML = `<div class="solver-out-box"><div class="out-val" style="color:#f87171;">Enter two equations separated by a comma (e.g. "2x + 3y = 7, x - y = 1" or "y = x^2 - 4, y = 2x - 1").</div></div>`;
    }

    function runQuad() {
      const a = parseFloat(document.getElementById('quad-a').value) || 1;
      const b = parseFloat(document.getElementById('quad-b').value) || 0;
      const c = parseFloat(document.getElementById('quad-c').value) || 0;

      const vx = -b / (2 * a);
      const vy = a * vx * vx + b * vx + c;
      const opens = a > 0 ? "Upward (Minimum at vertex)" : "Downward (Maximum at vertex)";
      const disc = b * b - 4 * a * c;

      let rootsStr = "None (Complex roots: " + (-b/(2*a)).toFixed(2) + " ± " + (Math.sqrt(Math.abs(disc))/(2*Math.abs(a))).toFixed(2) + "i)";
      if (disc > 0) {
        const r1 = (-b + Math.sqrt(disc)) / (2 * a);
        const r2 = (-b - Math.sqrt(disc)) / (2 * a);
        rootsStr = `x = ${r1.toFixed(3)}, x = ${r2.toFixed(3)}`;
      } else if (disc === 0) {
        rootsStr = `x = ${vx.toFixed(3)} (single intercept)`;
      }

      document.getElementById('quad-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Vertex & Axis of Symmetry</div>
          <div class="out-val">Vertex: (${vx.toFixed(2)}, ${vy.toFixed(2)}) &nbsp;|&nbsp; Axis: x = ${vx.toFixed(2)}</div>
          <ul class="out-steps">
            <li>Parabola opens: <strong>${opens}</strong></li>
            <li>Vertex Form: <strong>f(x) = ${a}(x - ${vx.toFixed(2)})² + (${vy.toFixed(2)})</strong></li>
            <li>y-intercept: <strong>(0, ${c})</strong></li>
            <li>Discriminant: b² - 4ac = <strong>${disc.toFixed(2)}</strong> (${disc > 0 ? '2 real x-intercepts' : disc === 0 ? '1 real x-intercept' : 'no real x-intercepts'})</li>
            <li>x-intercept(s): <strong>${rootsStr}</strong></li>
            <li>Domain: <strong>(-∞, ∞)</strong> &nbsp;|&nbsp; Range: <strong>${a > 0 ? `[${vy.toFixed(2)}, ∞)` : `(-∞, ${vy.toFixed(2)}]`}</strong></li>
          </ul>
          ${buildSolverCanvasBlock('quadSolverCanvas', `Parabola Graph: f(x) = ${a}x² + (${b})x + (${c})`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildGraphDataFromParsed({ type: 'quadratic', a, b, c }, '');
        renderUniversalGraph('quadSolverCanvas', gd);
      }, 20);
    }

    function runQuadEq() {
      const a = parseFloat(document.getElementById('qeq-a').value) || 1;
      const b = parseFloat(document.getElementById('qeq-b').value) || 0;
      const c = parseFloat(document.getElementById('qeq-c').value) || 0;

      const disc = b * b - 4 * a * c;
      let solStr = "";
      let steps = [];

      steps.push(`1. Quadratic Formula: x = [-b ± √(b² - 4ac)] / (2a)`);
      steps.push(`2. Identify coefficients: a = ${a}, b = ${b}, c = ${c}`);
      steps.push(`3. Discriminant Δ = (${b})² - 4(${a})(${c}) = ${b*b} - ${4*a*c} = ${disc}`);

      if (disc > 0) {
        const sq = Math.sqrt(disc);
        if (Number.isInteger(sq)) {
          const r1 = (-b + sq) / (2 * a);
          const r2 = (-b - sq) / (2 * a);
          solStr = `x = ${r1}, x = ${r2}`;
          steps.push(`4. Exact square root: √(${disc}) = ${sq}`);
          steps.push(`5. Two rational roots: x = (${-b} + ${sq})/${2*a} = ${r1}, x = (${-b} - ${sq})/${2*a} = ${r2}`);
        } else {
          const rad = simplifyRadical(disc);
          solStr = `x = [${-b} ± ${rad.str}] / ${2*a}`;
          steps.push(`4. Simplified radical: √(${disc}) = ${rad.str}`);
          steps.push(`5. Exact solutions: x = (${-b} ± ${rad.str}) / ${2*a}`);
        }
      } else if (disc === 0) {
        const r = -b / (2 * a);
        solStr = `x = ${r}`;
        steps.push(`4. Discriminant is zero: exactly one real double root x = -b/(2a) = ${r}`);
      } else {
        const rad = simplifyRadical(disc);
        solStr = `x = [${-b} ± ${rad.str}] / ${2*a}`;
        steps.push(`4. Negative discriminant yields complex roots with i = √(-1): √(${disc}) = ${rad.str}`);
        steps.push(`5. Exact complex conjugate solutions: x = (${-b} ± ${rad.str}) / ${2*a}`);
      }

      document.getElementById('qeq-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Exact Equation Solutions</div>
          <div class="out-val">${solStr}</div>
          <ul class="out-steps">
            ${steps.map(s => `<li>${s}</li>`).join('')}
          </ul>
          ${buildSolverCanvasBlock('qeqSolverCanvas', `Quadratic Curve y = ${a}x² + (${b})x + (${c})`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildGraphDataFromParsed({ type: 'quadratic', a, b, c }, '');
        renderUniversalGraph('qeqSolverCanvas', gd);
      }, 20);
    }

    function runAbs() {
      const a = parseFloat(document.getElementById('abs-a').value) || 1;
      const b = parseFloat(document.getElementById('abs-b').value) || 0;
      const op = document.getElementById('abs-op').value;
      const c = parseFloat(document.getElementById('abs-c').value) || 0;

      let ans = "";
      let steps = [];

      if (c < 0) {
        if (op === '<' || op === '<=') {
          ans = "No solution (∅)";
          steps.push("Absolute value cannot be negative. Solution set is ∅.");
        } else if (op === '=') {
          ans = "No solution (∅)";
          steps.push("Absolute value can never equal a negative number.");
        } else {
          ans = "All real numbers (-∞, ∞)";
          steps.push("Absolute value is always ≥ 0, which is always greater than any negative number.");
        }
      } else if (op === '=') {
        const x1 = (-c - b) / a;
        const x2 = (c - b) / a;
        ans = `{${x1.toFixed(3)}, ${x2.toFixed(3)}}`;
        steps.push(`Case 1: ${a}x + (${b}) = ${c} → x = ${x2.toFixed(3)}`);
        steps.push(`Case 2: ${a}x + (${b}) = -${c} → x = ${x1.toFixed(3)}`);
      } else if (op === '<' || op === '<=') {
        const left = (-c - b) / a;
        const right = (c - b) / a;
        const xMin = Math.min(left, right);
        const xMax = Math.max(left, right);
        const br1 = op === '<=' ? '[' : '(';
        const br2 = op === '<=' ? ']' : ')';
        ans = `${br1}${xMin.toFixed(3)}, ${xMax.toFixed(3)}${br2}`;
        steps.push(`Rewrite as three-part inequality: -${c} ${op} ${a}x + (${b}) ${op} ${c}`);
        steps.push(`Subtract ${b} from all three parts: ${-c - b} ${op} ${a}x ${op} ${c - b}`);
        steps.push(`Divide all parts by ${a}: ${xMin.toFixed(3)} ${op} x ${op} ${xMax.toFixed(3)}`);
      } else {
        const left = (-c - b) / a;
        const right = (c - b) / a;
        const xMin = Math.min(left, right);
        const xMax = Math.max(left, right);
        const br1 = op === '>=' ? ']' : ')';
        const br2 = op === '>=' ? '[' : '(';
        ans = `(-∞, ${xMin.toFixed(3)}${br1} ∪ ${br2}${xMax.toFixed(3)}, ∞)`;
        steps.push(`Rewrite as disjunction: ${a}x + (${b}) ${op} ${c}  OR  ${a}x + (${b}) ${op === '>' ? '<' : '<='} -${c}`);
        steps.push(`Solve branch 1: x ${op} ${xMax.toFixed(3)}`);
        steps.push(`Solve branch 2: x ${op === '>' ? '<' : '<='} ${xMin.toFixed(3)}`);
      }

      document.getElementById('abs-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Solution in Interval Notation</div>
          <div class="out-val">${ans}</div>
          <ul class="out-steps">
            ${steps.map(s => `<li>${s}</li>`).join('')}
          </ul>
          ${buildSolverCanvasBlock('absSolverCanvas', `Number Line Solution Set: |${a}x + (${b})| ${op} ${c}`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildGraphDataFromParsed({ type: 'abs', a: Math.abs(a), b: a < 0 ? -b : b, op, c }, '');
        renderUniversalGraph('absSolverCanvas', gd);
      }, 20);
    }

    function runCirc() {
      const a = parseFloat(document.getElementById('circ-a').value) || 1;
      const b = parseFloat(document.getElementById('circ-b').value) || 0;
      const c = parseFloat(document.getElementById('circ-c').value) || 0;
      const d = parseFloat(document.getElementById('circ-d').value) || 0;

      const h = -b / (2 * a);
      const k = -c / (2 * a);
      const rSq = (b * b + c * c - 4 * a * d) / (4 * a * a);

      if (rSq < 0) {
        document.getElementById('circ-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">Invalid Circle</div>
            <div class="out-val" style="color:#f87171;">r² = ${rSq.toFixed(2)} &lt; 0</div>
            <p>Completing the square gives a negative right-hand side. No real circle exists.</p>
          </div>
        `;
      } else {
        const r = Math.sqrt(rSq);
        document.getElementById('circ-out').innerHTML = `
          <div class="solver-out-box">
            <div class="out-label">Center & Radius</div>
            <div class="out-val">Center: (${h.toFixed(2)}, ${k.toFixed(2)}) &nbsp;|&nbsp; Radius: ${r.toFixed(2)}</div>
            <ul class="out-steps">
              <li>Standard Form: <strong>(x - ${h.toFixed(2)})² + (y - ${k.toFixed(2)})² = ${rSq.toFixed(2)}</strong></li>
              <li>Domain: <strong>[${(h - r).toFixed(2)}, ${(h + r).toFixed(2)}]</strong></li>
              <li>Range: <strong>[${(k - r).toFixed(2)}, ${(k + r).toFixed(2)}]</strong></li>
              <li>Cardinal Points: (${(h+r).toFixed(2)}, ${k.toFixed(2)}), (${(h-r).toFixed(2)}, ${k.toFixed(2)}), (${h.toFixed(2)}, ${(k+r).toFixed(2)}), (${h.toFixed(2)}, ${(k-r).toFixed(2)})</li>
            </ul>
            ${buildSolverCanvasBlock('circSolverCanvas', `Circle Graph: Center (${h.toFixed(2)}, ${k.toFixed(2)}), r = ${r.toFixed(2)}`)}
          </div>
        `;
        setTimeout(() => {
          const gd = buildGraphDataFromParsed({ type: 'circle_std', h, k, r, rSq }, '');
          renderUniversalGraph('circSolverCanvas', gd);
        }, 20);
      }
    }

    function runRad() {
      let n = parseInt(document.getElementById('rad-n').value) || 0;
      const sim = simplifyRadical(n);

      document.getElementById('rad-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Simplified Radical</div>
          <div class="out-val">${sim.str}</div>
          <ul class="out-steps">
            <li>Largest perfect square factor: <strong>${sim.outside * sim.outside}</strong></li>
            <li>Remaining inside factor: <strong>${sim.inside}</strong></li>
            ${sim.isImag ? '<li>Imaginary unit applied: i = √(-1)</li>' : ''}
            <li>Square Root Property solutions to x² = ${n}: <strong>x = ±${sim.str}</strong></li>
          </ul>
        </div>
      `;
    }

    function runComplex() {
      const a1 = parseFloat(document.getElementById('cplx-a1').value) || 0;
      const b1 = parseFloat(document.getElementById('cplx-b1').value) || 0;
      const a2 = parseFloat(document.getElementById('cplx-a2').value) || 0;
      const b2 = parseFloat(document.getElementById('cplx-b2').value) || 0;
      const pow = parseInt(document.getElementById('cplx-pow').value) || 0;

      const realMult = a1 * a2 - b1 * b2;
      const imagMult = a1 * b2 + a2 * b1;
      const imagStr = imagMult >= 0 ? `+ ${imagMult}i` : `- ${Math.abs(imagMult)}i`;

      const den = a2 * a2 + b2 * b2;
      let divStr = "Undefined (division by 0)";
      if (den !== 0) {
        const numReal = a1 * a2 + b1 * b2;
        const numImag = b1 * a2 - a1 * b2;
        divStr = `${fracStr(numReal, den)} ${numImag >= 0 ? '+ ' + fracStr(numImag, den) : '- ' + fracStr(Math.abs(numImag), den)}i`;
      }

      const rem = ((pow % 4) + 4) % 4;
      const valMap = { 0: '1', 1: 'i', 2: '-1', 3: '-i' };

      document.getElementById('cplx-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Product in Standard Form (a + bi)</div>
          <div class="out-val">${realMult} ${imagStr}</div>
          <ul class="out-steps">
            <li>FOIL Expansion: (${a1})(${a2}) + (${a1})(${b2}i) + (${b1}i)(${a2}) + (${b1}i)(${b2}i)</li>
            <li>Combine terms with i² = -1: (${a1*a2} - ${b1*b2}) + (${a1*b2 + a2*b1})i</li>
            <li>Conjugate Division (${a1}+${b1}i)/(${a2}+${b2}i): <strong>${divStr}</strong></li>
            <li>Power of i: i^${pow} = i^${rem} = <strong>${valMap[rem]}</strong> (since ${pow} mod 4 = ${rem})</li>
          </ul>
        </div>
      `;
    }

    function runProjectile() {
      const v0 = parseFloat(document.getElementById('proj-v0').value) || 0;
      const h0 = parseFloat(document.getElementById('proj-h0').value) || 0;

      const a = -16;
      const tPeak = -v0 / (2 * a);
      const hMax = a * tPeak * tPeak + v0 * tPeak + h0;

      const disc = v0 * v0 - 4 * a * h0;
      let tGround = 0;
      if (disc >= 0) {
        tGround = (-v0 - Math.sqrt(disc)) / (2 * a);
      }

      document.getElementById('proj-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Maximum Height & Flight Time</div>
          <div class="out-val">Peak Height: ${hMax.toFixed(2)} ft &nbsp;|&nbsp; Peak Time: ${tPeak.toFixed(2)} s</div>
          <ul class="out-steps">
            <li>Height equation: <strong>h(t) = -16t² + ${v0}t + ${h0}</strong></li>
            <li>Time to reach maximum height: t = -b/(2a) = -(${v0})/(2 · (-16)) = <strong>${tPeak.toFixed(2)} seconds</strong></li>
            <li>Maximum height: h(${tPeak.toFixed(2)}) = <strong>${hMax.toFixed(2)} feet</strong></li>
            <li>Total time until projectile hits the ground: <strong>${tGround.toFixed(2)} seconds</strong></li>
          </ul>
          ${buildSolverCanvasBlock('projCanvas', `Projectile Trajectory h(t) = -16t² + ${v0}t + ${h0}`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildGraphDataFromParsed({ type: 'quadratic', a: -16, b: v0, c: h0 }, '');
        renderUniversalGraph('projCanvas', gd);
      }, 20);
    }

    function runDistMid() {
      const x1 = parseFloat(document.getElementById('dm-x1').value) || 0;
      const y1 = parseFloat(document.getElementById('dm-y1').value) || 0;
      const x2 = parseFloat(document.getElementById('dm-x2').value) || 0;
      const y2 = parseFloat(document.getElementById('dm-y2').value) || 0;

      const midX = (x1 + x2) / 2;
      const midY = (y1 + y2) / 2;
      const dSq = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
      const rad = simplifyRadical(dSq);
      const dDec = Math.sqrt(dSq);

      document.getElementById('dm-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Exact Distance & Midpoint</div>
          <div class="out-val">Distance: ${rad.str} (≈ ${dDec.toFixed(3)}) &nbsp;|&nbsp; Midpoint: (${midX}, ${midY})</div>
          <ul class="out-steps">
            <li>Distance Formula: d = √[(${x2} - ${x1})² + (${y2} - ${y1})²] = √(${dSq})</li>
            <li>Simplified Radical Distance: <strong>${rad.str}</strong></li>
            <li>Midpoint Formula: M = ((${x1}+${x2})/2, (${y1}+${y2})/2) = <strong>(${midX}, ${midY})</strong></li>
          </ul>
        </div>
      `;
    }

    function runPolyEval() {
      const raw = document.getElementById('peval-coeffs').value.trim();
      const xVal = parseFloat(document.getElementById('peval-x').value) || 0;
      if (!raw) return;
      const coeffs = raw.includes('x') ? parseAnyPolyCoeffs(raw) : raw.split(/\s+/).map(Number).filter(x => !isNaN(x));
      if (coeffs.length === 0) return;

      let val = coeffs[0];
      for (let i = 1; i < coeffs.length; i++) {
        val = val * xVal + coeffs[i];
      }

      document.getElementById('peval-out').innerHTML = `
        <div class="solver-out-box">
          <div class="out-label">Polynomial Evaluation</div>
          <div class="out-val">P(${xVal}) = ${val}</div>
          <ul class="out-steps">
            <li>Coefficients: [${coeffs.join(', ')}]</li>
            <li>Remainder Theorem confirms dividing P(x) by (x - (${xVal})) yields remainder R = <strong>${val}</strong></li>
            <li>Is ${xVal} a zero? <strong>${val === 0 ? 'YES' : 'NO'}</strong></li>
          </ul>
          ${buildSolverCanvasBlock('pevalCanvas', `Polynomial P(x) = ${formatPolyCoeffs(coeffs)} at x = ${xVal}`)}
        </div>
      `;
      setTimeout(() => {
        const gd = buildPolynomialGraphData(coeffs, formatPolyCoeffs(coeffs));
        gd.points.push({ x: xVal, y: val, type: 'vertex', color: '#34d399', label: `P(${xVal}) = ${val}` });
        renderUniversalGraph('pevalCanvas', gd);
      }, 20);
    }

    // Math Formatting Engine
    function formatMath(text) {
      if (!text) return '';
      let s = text;
      s = s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      s = s.replace(/`([^`]+)`/g, '<code style="background:var(--code-bg); padding:2px 6px; border-radius:4px; color:#f472b6;">$1</code>');
      for (let i = 0; i < 4; i++) {
        s = s.replace(/\\sqrt\{([^{}]+)\}/g, '&radic;<span class="radicand">$1</span>');
        s = s.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '<span class="frac"><span class="num">$1</span><span class="den">$2</span></span>');
      }
      s = s.replace(/\\le/g, '&le;');
      s = s.replace(/\\ge/g, '&ge;');
      s = s.replace(/\\pm/g, '&plusmn;');
      s = s.replace(/\\neq/g, '&ne;');
      s = s.replace(/\\varnothing/g, '&empty;');
      s = s.replace(/\\cup/g, '&cup;');
      s = s.replace(/\\infty/g, '&infin;');
      s = s.replace(/\\cdot/g, '&sdot;');
      s = s.replace(/\\times/g, '&times;');
      s = s.replace(/\\pi/g, '&pi;');
      s = s.replace(/\^2/g, '<sup>2</sup>');
      s = s.replace(/\^3/g, '<sup>3</sup>');
      s = s.replace(/\^4/g, '<sup>4</sup>');
      s = s.replace(/\^5/g, '<sup>5</sup>');
      s = s.replace(/\^6/g, '<sup>6</sup>');
      s = s.replace(/\^([0-9a-zA-Z]+)/g, '<sup>$1</sup>');
      s = s.replace(/\$([^\$]+)\$/g, '<span class="math-sym">$1</span>');
      s = s.replace(/\n\s*\n/g, '<br><br>');
      return s;
    }

    function formatGeneralMarkdown(md) {
      let lines = md.split('\n');
      return lines.map(line => {
        if (line.startsWith('# ')) return `<h1>${formatMath(line.substring(2))}</h1>`;
        if (line.startsWith('## ')) return `<h2>${formatMath(line.substring(3))}</h2>`;
        if (line.startsWith('### ')) return `<h3>${formatMath(line.substring(4))}</h3>`;
        if (line.startsWith('---')) return `<hr style="border:none; border-top:1px solid var(--border); margin:20px 0;">`;
        if (line.startsWith('* ')) return `<li>${formatMath(line.substring(2))}</li>`;
        return `<p>${formatMath(line)}</p>`;
      }).join('');
    }

    // Startup Initialization
    initFileList();
    runSynthetic();
  </script>
</body>
</html>
"""

def generate_dashboard():
    # Rebuild SQLite database from all solved Markdown files in assignments/Answers/
    db_json_str = "{}"
    if build_database:
        try:
            build_database.init_database()
            build_database.populate_database()
            db_export = build_database.export_json_database()
            db_json_str = json.dumps(db_export)
        except Exception as e:
            print(f"Note: database build/export: {e}")

    answers = get_all_answers()
    json_str = json.dumps(answers)

    full_html = HTML_TEMPLATE.replace("###EMBEDDED_JSON###", json_str).replace("###EMBEDDED_DB_JSON###", db_json_str)
    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Successfully generated {DASHBOARD_FILE} with {len(answers)} answer sheets and complete database ({len(full_html)} bytes).")

if __name__ == "__main__":
    generate_dashboard()
