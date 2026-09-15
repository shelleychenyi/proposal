# -*- coding: utf-8 -*-
"""v.2 album: circled numbers + titles on every page, reorder to ①..⑩."""
import os, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

BASE = "/Users/shelleychen/Documents/提案/SMBC三井住友"
SRC = os.path.join(BASE, "8:28_版位照片集_無費用.pptx")
OUT = os.path.join(BASE, "8:28_版位照片集_無費用_v.2.pptx")

NAVY = RGBColor(0x12, 0x20, 0x3F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation(SRC)
slides = list(prs.slides)

def walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            for sub in walk(sh.shapes):
                yield sub
        elif sh.has_text_frame:
            yield sh

def set_font(run, size=None, bold=None, color=None, name="Microsoft JhengHei"):
    f = run.font
    if size: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if color is not None: f.color.rgb = color
    f.name = name
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", name)

# ---------- 1. menu-page titles & divider ranges (1-based original indices) ----------
MENU_TITLES = {
    3: ("捷運聯播網", "①　捷運聯播網"),
    7: ("台北捷運", "②　台北車站 站體數位"),
    14: ("公車", "③　市區公車（松山機場線）"),
    16: ("多元計程車", "⑦　計程車 車內螢幕"),
    21: ("戶外看板", "④　戶外看板"),
    38: ("機場排班計程車", "⑨　桃園機場 排班計程車椅套 ＋ 入境區"),
    41: ("機場捷運", "⑤　機場捷運（桃捷）"),
    48: ("機場巴士", "⑥　機場巴士"),
    51: ("航廈出境大廳", "⑧　桃園機場 出境區"),
    59: ("台灣高鐵 桃園站", "⑩　台灣高鐵 桃園站"),
    69: ("台灣高鐵 台北站", "⑩　台灣高鐵 台北站"),
}
DIVIDER_RANGES = {2: "　①–④", 37: "　⑤–⑦", 50: "　⑧–⑨", 58: "　⑩"}
DIVIDER_TEXTS = {"捷運與市區交通", "機場運輸系統", "機場航廈", "台灣高鐵"}

for idx, (old, new) in MENU_TITLES.items():
    s = slides[idx - 1]
    done = False
    for sh in walk(s.shapes):
        t = sh.text_frame.text.strip()
        top = Emu(sh.top).inches if sh.top is not None else 9
        if t == old and top < 1.7:
            para = sh.text_frame.paragraphs[0]
            if para.runs:
                para.runs[0].text = new
                for r in para.runs[1:]:
                    r._r.getparent().remove(r._r)
            done = True
            break
    if not done:
        print("!! title not found on slide", idx, old)

for idx, suffix in DIVIDER_RANGES.items():
    s = slides[idx - 1]
    done = False
    for sh in walk(s.shapes):
        t = sh.text_frame.text.strip()
        if t in DIVIDER_TEXTS:
            para = sh.text_frame.paragraphs[0]
            if para.runs:
                para.runs[-1].text = para.runs[-1].text + suffix
            done = True
            break
    if not done:
        print("!! divider not found on slide", idx)

# stray "01" chip on slide 7
s7 = slides[6]
for sh in list(walk(s7.shapes)):
    if sh.text_frame.text.strip() == "01" and Emu(sh.top).inches < 1.0:
        sh._element.getparent().remove(sh._element)

# ---------- 2. leftover price-string cleanup + stale caption ----------
PAIRS = [
    ("；單買合計 2,010,000／週", ""),
    ("；全案 CPM 最低", ""),
    ("，製作 356,000／次", ""),
    ("，製作 889,000／次", ""),
    ("；上稿費 7,520,000／次", ""),
    ("；製作費最低（205,000／次）", ""),
    ("｜免製作費", ""),
    ("尺寸・位置・對應動線（01–04）：", "尺寸・位置對應："),
]
for s in slides:
    for sh in walk(s.shapes):
        for para in sh.text_frame.paragraphs:
            for r in para.runs:
                for a, b in PAIRS:
                    if a in r.text:
                        r.text = r.text.replace(a, b)

# ---------- 3. photo-page labels ----------
PHOTO_LABELS = {
    "①　捷運聯播網": [4, 5, 6],
    "②　台北車站 站體數位": [8, 9, 10, 11, 12, 13],
    "③　市區公車（松山機場線）": [15],
    "⑦　計程車 車內螢幕": [17, 18, 19, 20],
    "④　戶外看板": list(range(22, 37)),
    "⑨　桃園機場 排班計程車椅套": [39, 40],
    "⑤　機場捷運（桃捷）": list(range(42, 48)),
    "⑥　機場巴士": [49],
    "⑧　桃園機場 出境區": list(range(52, 58)),
}
def add_chip(slide, text):
    w = 0.42 + 0.16 * len(text)
    sp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.18), Inches(0.13), Inches(w), Inches(0.36))
    try: sp.adjustments[0] = 0.5
    except Exception: pass
    sp.fill.solid(); sp.fill.fore_color.rgb = NAVY
    sp.line.color.rgb = WHITE; sp.line.width = Pt(1)
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = text
    set_font(run, size=12, bold=True, color=WHITE)

for label, idxs in PHOTO_LABELS.items():
    for idx in idxs:
        add_chip(slides[idx - 1], label)

# 高鐵 photo pages: prefix existing titles with ⑩
for idx in list(range(60, 69)) + list(range(70, 76)):
    s = slides[idx - 1]
    best = None
    for sh in walk(s.shapes):
        t = sh.text_frame.text.strip()
        if t.startswith(("桃園站", "台北站")) and len(t) > 4:
            best = sh
            break
    if best is None:
        print("!! hsr title not found on slide", idx)
        continue
    para = best.text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = "⑩　" + para.runs[0].text

# ---------- 4. reorder ----------
NEW_ORDER = ([1, 2, 3, 4, 5, 6] + list(range(7, 14)) + [14, 15] + list(range(21, 37))
             + [37] + list(range(41, 48)) + [48, 49] + list(range(16, 21))
             + [50] + list(range(51, 58)) + [38, 39, 40]
             + [58] + list(range(59, 69)) + list(range(69, 76)))
assert sorted(NEW_ORDER) == list(range(1, 76)), len(NEW_ORDER)
sldIdLst = prs.slides._sldIdLst
id_els = list(sldIdLst)
for el in id_els:
    sldIdLst.remove(el)
for pos in NEW_ORDER:
    sldIdLst.append(id_els[pos - 1])

prs.save(OUT)
print("saved", OUT, len(prs.slides))
