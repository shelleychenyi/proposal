# -*- coding: utf-8 -*-
"""列出範本裡每個錨點與目前文字，供撰寫 brief.json 時對照。

  python3 scripts/inspect_template.py [ja|zh] [--page N] [--md]
"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

HERE = Path(__file__).resolve().parent.parent
lang = "ja"
page = None
md = "--md" in sys.argv
for i, a in enumerate(sys.argv[1:], 1):
    if a in ("ja", "zh"):
        lang = a
    if a == "--page":
        page = int(sys.argv[i + 1])

prs = Presentation(str(HERE / "assets" / f"template_{lang}.pptx"))
if md:
    print(f"# 範本錨點對照表（template_{lang}.pptx）\n")
for pi, slide in enumerate(prs.slides, 1):
    if page and pi != page:
        continue
    rows = []
    for sh in slide.shapes:
        if not sh.name.startswith(("PD:", "T:")):
            continue
        txt = sh.text_frame.text.replace("\n", " ⏎ ") if sh.has_text_frame else ""
        kind = "圖表位" if ".chart." in sh.name else ("長條" if not sh.has_text_frame else "文字")
        rows.append((sh.name, kind, txt[:110]))
    if not rows:
        continue
    if md:
        print(f"\n## p{pi}\n")
        print("| 錨點 | 型別 | 範本原文 |")
        print("|---|---|---|")
        for n, k, t in rows:
            print(f"| `{n}` | {k} | {t.replace('|', '｜')} |")
    else:
        print(f"\n===== p{pi} =====")
        for n, k, t in rows:
            print(f"  {n:24s} [{k}] {t}")
