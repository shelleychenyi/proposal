# -*- coding: utf-8 -*-
"""依 brief.json 產出提案簡報。

  python3 scripts/build_deck.py brief.json

brief.json：
{
  "template": "ja",                       // ja | zh
  "output": "/絕對路徑/【インタセクト】○○様_….pptx",
  "fills":  { "T:p3.2": "一行文字", "PD:g1.bullets": ["・第一行", "・第二行"] },
  "images": { "PD:g1.chart.trend": "/path/to/pandora_trend.png" },
  "bars":   { "PD:sent.bar1": 1.9 },      // 單位：英吋
  "hide":   ["T:p6.31"],                   // 不使用的欄位直接移除
  "hideRegion": [{"page": 3, "box": [6.7, 2.1, 6.1, 4.6]}]   // 整區移除（左,上,寬,高；英吋）
}

原則：只換文字內容，字型／字級／顏色／位置全部沿用範本。
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Emu

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"


def q(tag: str) -> str:
    return "{%s}%s" % (NS_A, tag.split(":")[1])


def index_shapes(prs) -> dict:
    out = {}
    for slide in prs.slides:
        for sh in slide.shapes:
            if sh.name.startswith(("PD:", "T:")):
                out[sh.name] = (slide, sh)
    return out


def set_text(shape, lines) -> None:
    """保留原字型／字級／顏色，只換文字。lines 為 str 或 list[str]。"""
    if isinstance(lines, str):
        lines = [lines]
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if not p0.runs:
        return
    rPr = copy.deepcopy(p0.runs[0]._r.get_or_add_rPr())
    _pPr = p0._p.find(q("a:pPr"))
    pPr = copy.deepcopy(_pPr) if _pPr is not None else None
    txBody = tf._txBody
    for p in list(txBody.findall(q("a:p"))):
        txBody.remove(p)
    for text in lines:
        p = txBody.makeelement(q("a:p"), {})
        if pPr is not None:
            p.append(copy.deepcopy(pPr))
        r = txBody.makeelement(q("a:r"), {})
        r.append(copy.deepcopy(rPr))
        node = txBody.makeelement(q("a:t"), {})
        node.text = text
        r.append(node)
        p.append(r)
        txBody.append(p)


def place_image(slide, shape, img_path: Path) -> None:
    """把圖片等比縮放後置中放進佔位框，並移除佔位框本身。"""
    box_l, box_t, box_w, box_h = shape.left, shape.top, shape.width, shape.height
    with Image.open(img_path) as im:
        iw, ih = im.size
    scale = min(box_w / iw, box_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    left = box_l + (box_w - w) // 2
    top = box_t + (box_h - h) // 2
    slide.shapes.add_picture(str(img_path), Emu(left), Emu(top), Emu(w), Emu(h))
    shape._element.getparent().remove(shape._element)


def main() -> int:
    brief_path = Path(sys.argv[1]).resolve()
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    here = Path(__file__).resolve().parent.parent
    tpl = here / "assets" / f"template_{brief.get('template', 'ja')}.pptx"
    if not tpl.exists():
        print(f"找不到範本 {tpl}", file=sys.stderr)
        return 2

    prs = Presentation(str(tpl))
    S = index_shapes(prs)
    unknown, done = [], 0

    for anchor in brief.get("hide", []):
        if anchor in S:
            _, sh = S[anchor]
            sh._element.getparent().remove(sh._element)
            done += 1
        else:
            unknown.append(anchor)

    for reg in (brief.get("hideRegion") or []):
        page, (bx, by, bw, bh) = reg["page"], reg["box"]
        slide = prs.slides[page - 1]
        for sh in list(slide.shapes):
            if sh.left is None:
                continue
            l, t = Emu(sh.left).inches, Emu(sh.top).inches
            if bx <= l <= bx + bw and by <= t <= by + bh:
                sh._element.getparent().remove(sh._element)
                done += 1

    for anchor, value in (brief.get("fills") or {}).items():
        if anchor not in S:
            unknown.append(anchor)
            continue
        _, sh = S[anchor]
        if not sh.has_text_frame:
            unknown.append(anchor + "（非文字圖形）")
            continue
        set_text(sh, value)
        done += 1

    for anchor, width in (brief.get("bars") or {}).items():
        if anchor not in S:
            unknown.append(anchor)
            continue
        S[anchor][1].width = Emu(int(float(width) * 914400))
        done += 1

    for anchor, img in (brief.get("images") or {}).items():
        if anchor not in S:
            unknown.append(anchor)
            continue
        path = Path(img)
        if not path.is_absolute():
            path = (brief_path.parent / path).resolve()
        if not path.exists():
            print(f"找不到圖片：{path}", file=sys.stderr)
            return 2
        slide, sh = S[anchor]
        place_image(slide, sh, path)
        done += 1

    out = Path(brief["output"]).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))

    # ---- 收尾檢查：還沒填掉的佔位符 ----
    leftovers = []
    check = Presentation(str(out))
    for pi, slide in enumerate(check.slides, 1):
        for sh in slide.shapes:
            if sh.has_text_frame and "【" in sh.text_frame.text:
                leftovers.append((pi, sh.name, sh.text_frame.text.replace("\n", " ")[:70]))

    print(f"已套用 {done} 項，輸出 {out}")
    if unknown:
        print("\n⚠ 下列錨點不存在（請用 inspect_template.py 對照）：", file=sys.stderr)
        for a in unknown:
            print("   ", a, file=sys.stderr)
    if leftovers:
        print(f"\n⚠ 有 {len(leftovers)} 處仍含【】，請確認是未填的佔位符還是日文原本的括號用法：")
        for pi, name, txt in leftovers:
            print(f"   p{pi} {name}: {txt}")
    else:
        print("✓ 沒有殘留的【】佔位符")
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())
