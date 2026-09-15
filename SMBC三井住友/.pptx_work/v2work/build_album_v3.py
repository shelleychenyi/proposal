# -*- coding: utf-8 -*-
"""v.3 album: 高鐵 -> ⑧ (moved before 機場航廈), 出境區 -> ⑨, 椅套 -> ⑩ (drop 入境區 in title)."""
import os
from pptx import Presentation
from pptx.util import Inches, Emu

BASE = "/Users/shelleychen/Documents/提案/SMBC三井住友"
SRC = os.path.join(BASE, "8:28_版位照片集_無費用_v.2.pptx")
OUT = os.path.join(BASE, "8:28_版位照片集_無費用_v.3.pptx")

prs = Presentation(SRC)
slides = list(prs.slides)

def walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            for sub in walk(sh.shapes):
                yield sub
        elif sh.has_text_frame:
            yield sh

def para_text(para):
    return "".join(r.text for r in para.runs)

def rewrite_para(para, new_text):
    if not para.runs:
        return
    para.runs[0].text = new_text
    for r in para.runs[1:]:
        r._r.getparent().remove(r._r)

# order matters: 高鐵 ⑩->⑧ first, then 出境 ⑧->⑨, then 椅套 ⑨->⑩
STEPS = [
    {
        "⑩　台灣高鐵 桃園站": "⑧　台灣高鐵 桃園站",
        "⑩　台灣高鐵 台北站": "⑧　台灣高鐵 台北站",
        "台灣高鐵　⑩": "台灣高鐵　⑧",
    },
    "HSR_PREFIX",   # ⑩　桃園站... / ⑩　台北站... photo titles -> ⑧
    {
        "⑧　桃園機場 出境區": "⑨　桃園機場 出境區",
        "機場航廈　⑧–⑨": "機場航廈　⑨–⑩",
    },
    {
        "⑨　桃園機場 排班計程車椅套 ＋ 入境區": "⑩　桃園機場 排班計程車（椅套）",
        "⑨　桃園機場 排班計程車椅套": "⑩　桃園機場 排班計程車（椅套）",
    },
]
for step in STEPS:
    for s in slides:
        for sh in walk(s.shapes):
            for para in sh.text_frame.paragraphs:
                t = para_text(para).strip()
                if step == "HSR_PREFIX":
                    if t.startswith("⑩　桃園站") or t.startswith("⑩　台北站"):
                        para.runs[0].text = para.runs[0].text.replace("⑩　", "⑧　", 1)
                elif t in step:
                    rewrite_para(para, step[t])

# resize navy chips to fit new text (chips: h~0.36, top~0.13, left~0.18)
for s in slides:
    for sh in s.shapes:
        if not sh.has_text_frame or sh.top is None:
            continue
        if abs(Emu(sh.top).inches - 0.13) < 0.03 and abs(Emu(sh.left).inches - 0.18) < 0.03 and Emu(sh.height).inches < 0.5:
            t = sh.text_frame.text.strip()
            if t and t[0] in "①②③④⑤⑥⑦⑧⑨⑩":
                sh.width = Inches(0.42 + 0.16 * len(t))

# reorder: [1..46] + [58..75] + [47..57]  (1-based v.2 positions)
NEW_ORDER = list(range(1, 47)) + list(range(58, 76)) + list(range(47, 58))
assert sorted(NEW_ORDER) == list(range(1, 76))
sldIdLst = prs.slides._sldIdLst
id_els = list(sldIdLst)
for el in id_els:
    sldIdLst.remove(el)
for pos in NEW_ORDER:
    sldIdLst.append(id_els[pos - 1])

prs.save(OUT)
print("saved", OUT, len(prs.slides))
