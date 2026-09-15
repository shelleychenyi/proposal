# -*- coding: utf-8 -*-
"""把 Pandora 報告（pptx / pdf / 圖片資料夾）的每一頁抽成圖片，供貼進提案簡報。

  python3 scripts/extract_report.py <報告檔> -o /tmp/案子/pandora [--dpi 160]

抽完務必用 Read 工具逐張看過，把數字讀出來——腳本不做 OCR，不會替你判讀。
"""
from __future__ import annotations

import argparse
import os
import shutil
import zipfile
from pathlib import Path

HINT = """
建議的裁切（Pandora 標準 6 頁報告）：
  p1 封面        → 取品牌名與「資料範圍」的日期
  p2 基本統計    → 總文章數／總按讚數／總留言數／平均按讚／平均留言／總聲量
  p3 平台與看板  → 左半＝平台分布圓餅（貼 PD:g1.chart.platform）
                   右半＝聲量看板排行（可貼 PD:chart.sentiment）
  p4 聲量趨勢    → 整張貼 PD:g1.chart.trend；讀出高峰月與空白月的數值
  p5 文章數      → 補充用，通常不貼
  p6 熱門文章    → 上半部貼 PD:chart.keyword；讀出 Top10 的主題傾向

裁切用 Pillow，例如只取左 40%：
  from PIL import Image
  im = Image.open("p3.png"); W, H = im.size
  im.crop((int(W*0.03), int(H*0.14), int(W*0.40), int(H*0.90))).save("platform.png")
"""


def from_pptx(src: Path, out: Path) -> list[Path]:
    made = []
    with zipfile.ZipFile(src) as z:
        names = sorted(n for n in z.namelist()
                       if n.startswith("ppt/media/") and not n.endswith("/"))
        for i, n in enumerate(names, 1):
            dst = out / f"p{i:02d}{Path(n).suffix}"
            with z.open(n) as s, open(dst, "wb") as d:
                shutil.copyfileobj(s, d)
            made.append(dst)
    return made


def from_pdf(src: Path, out: Path, dpi: int) -> list[Path]:
    import fitz
    made = []
    doc = fitz.open(src)
    for i, page in enumerate(doc, 1):
        dst = out / f"p{i:02d}.png"
        page.get_pixmap(dpi=dpi).save(dst)
        made.append(dst)
    return made


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dpi", type=int, default=160)
    a = ap.parse_args()

    src, out = Path(a.src).expanduser(), Path(a.out).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    if src.is_dir():
        made = []
        for f in sorted(src.iterdir()):
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                dst = out / f.name
                shutil.copy(f, dst)
                made.append(dst)
    elif src.suffix.lower() == ".pptx":
        made = from_pptx(src, out)
    elif src.suffix.lower() == ".pdf":
        made = from_pdf(src, out, a.dpi)
    else:
        print(f"不支援的格式：{src.suffix}")
        return 2

    print(f"抽出 {len(made)} 張到 {out}")
    for p in made:
        print("  ", p, f"({os.path.getsize(p)//1024} KB)")
    print(HINT)
    print("→ 下一步：用 Read 工具逐張看過，把數字抄進 brief.json。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
