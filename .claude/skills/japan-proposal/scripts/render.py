# -*- coding: utf-8 -*-
"""把簡報轉成逐頁 PNG，供目視檢查。

  python3 scripts/render.py <deck.pptx> -o /tmp/案子/shots [--dpi 110]

macOS 用 PowerPoint 匯出 PDF（不需安裝 LibreOffice），再用 PyMuPDF 轉圖。
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

APPLESCRIPT = '''with timeout of 600 seconds
    tell application "Microsoft PowerPoint"
        close every presentation saving no
        open POSIX file "{src}"
        set d to active presentation
        save d in POSIX file "{pdf}" as save as PDF
        close d saving no
    end tell
end timeout'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args()

    src = Path(a.deck).resolve()
    out = Path(a.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / (src.stem + ".pdf")
    if pdf.exists():
        pdf.unlink()

    r = subprocess.run(["osascript", "-e", APPLESCRIPT.format(src=src, pdf=pdf)],
                       capture_output=True, text=True)
    if not pdf.exists():
        msg = r.stderr.strip()
        print("PowerPoint 匯出失敗：", msg, file=sys.stderr)
        if "-9074" in msg or "-128" in msg:
            print("→ PowerPoint 可能有對話框卡住，或檔案仍被開啟。"
                  "請切到 PowerPoint 關掉視窗後重跑。", file=sys.stderr)
        soffice = shutil.which("soffice")
        if soffice:
            print("→ 改用 LibreOffice 匯出…", file=sys.stderr)
            subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                            "--outdir", str(out), str(src)], capture_output=True)
        if not pdf.exists():
            return 2

    import fitz
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=a.dpi).save(out / f"s{i:02d}.png")
    print(f"已輸出 {len(doc)} 頁到 {out}")
    for i in range(1, len(doc) + 1):
        print("  ", out / f"s{i:02d}.png")
    print("→ 下一步：用 Read 工具逐頁看過，檢查溢出／重疊／空白區塊。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
