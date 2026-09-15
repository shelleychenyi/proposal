# -*- coding: utf-8 -*-
"""v.3 deck: insert ⑧ 高鐵桃園站 page, renumber ⑧⑨⑩, drop 入境區, reorder schedule rows."""
import copy, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn

BASE = "/Users/shelleychen/Documents/提案/SMBC三井住友"
SRC = os.path.join(BASE, "8:28-v.2_編集中【SMCC様】_Visaタッチについて0831_中文版 copy_v.2.pptx")
OUT = os.path.join(BASE, "8:28-v.2_編集中【SMCC様】_Visaタッチについて0831_中文版 copy_v.3.pptx")

TEAL = RGBColor(0x1C, 0x72, 0x93)
INACT = RGBColor(0xC9, 0xD2, 0xDE)
INACT_T = RGBColor(0x9A, 0xA3, 0xB0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation(SRC)

def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            for sub in walk(sh.shapes):
                yield sub

def para_text(para):
    return "".join(r.text for r in para.runs)

def rewrite_para(para, new_text):
    if not para.runs:
        return
    para.runs[0].text = new_text
    for r in para.runs[1:]:
        r._r.getparent().remove(r._r)

def rewrite_shape(sh, new_text):
    tf = sh.text_frame
    rewrite_para(tf.paragraphs[0], new_text)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)

# ---------- 1. global renumbering (exact paragraph matches) ----------
EXACT = {
    "⑧　桃園機場 出境區": "⑨　桃園機場 出境區",
    "⑧-Ⅰ　桃園機場 出境區": "⑨-Ⅰ　桃園機場 出境區",
    "⑧　松山機場 出境區": "⑨　松山機場 出境區",
    "⑧　桃機 T1 出境查驗大廳 燈箱": "⑨　桃機 T1 出境查驗大廳 燈箱",
    "⑨　桃機排班計程車 椅套": "⑩　桃機排班計程車 椅套",
    "⑩　台灣高鐵（桃園站・台北站）": "⑧　台灣高鐵（桃園站・台北站）",
    "⑨　桃園機場 排班計程車椅套 ＋ 入境區": "⑩　桃園機場 排班計程車（椅套）",
    "⑨-Ⅰ　桃園機場 排班計程車（椅套）": "⑩-Ⅰ　桃園機場 排班計程車（椅套）",
    "高鐵旅客來源地（廣告 ⑤–⑦ 的上游）": "高鐵旅客來源地（廣告 ⑤–⑧ 的上游）",
    "機場捷運・機場巴士・計程車": "機場捷運・機場巴士・計程車・高鐵",
    "⑩高鐵": "⑧高鐵",
    "大台北・桃園（據點 ①–⑦）": "大台北・桃園（據點 ❶–❼）",
    "全台西部走廊（據點 ⑧–⑫）": "全台西部走廊（據點 ❽–⓬）",
}
for idx, slide in enumerate(prs.slides, 1):
    if idx <= 15:
        continue
    for sh in walk(slide.shapes):
        if not sh.has_text_frame:
            continue
        for para in sh.text_frame.paragraphs:
            t = para_text(para).strip()
            if t in EXACT:
                rewrite_para(para, EXACT[t])
            elif t.startswith("⑧") and "桃園高鐵站" in t:
                rewrite_para(para, "⑧　高鐵桃園站")

# ---------- 2. p29 (椅套): delete 入境區 section ----------
s29 = prs.slides[28]
for sh in list(walk(s29.shapes)):
    if sh.top is None:
        continue
    x = Emu(sh.left).inches; y = Emu(sh.top).inches
    kill = False
    if x < 8.3 and y >= 3.45:
        kill = True
    if sh.has_text_frame and sh.text_frame.text.strip() == "入境區 燈箱・數位":
        kill = True
    if kill:
        sh._element.getparent().remove(sh._element)

# ---------- 3. clone p28 -> new ⑧ 高鐵桃園站 page ----------
src_slide = prs.slides[27]
layout = src_slide.slide_layout
new_slide = prs.slides.add_slide(layout)
for shp in list(new_slide.shapes):
    shp._element.getparent().remove(shp._element)
spTree = new_slide.shapes._spTree
for child in src_slide.shapes._spTree:
    tag = child.tag.split("}")[-1]
    if tag in ("nvGrpSpPr", "grpSpPr"):
        continue
    spTree.append(copy.deepcopy(child))

def by_id(slide, sid):
    for sh in walk(slide.shapes):
        if sh.shape_id == sid:
            return sh
    return None

ns = new_slide
# stray page number
pg = by_id(ns, 2)
if pg is not None:
    pg._element.getparent().remove(pg._element)
rewrite_shape(by_id(ns, 6), "⑧　高鐵桃園站")
rewrite_shape(by_id(ns, 7), "全台高鐵出國旅客到站必經。年進出站 1,961 萬人次、站內平均停留 20–60 分鐘——下高鐵即在 A18 轉乘機場捷運前往桃園機場")
rewrite_shape(by_id(ns, 14), "⑧-Ⅰ　高鐵桃園站（B1 候車大廳・1F 大廳）")
rewrite_shape(by_id(ns, 15), "65% 以上為高收入・高學歷・高消費力族群")
ROWS = [
    ("包區 案一：籃筐 9 面（整區買斷）", "進出月台層手扶梯正對牆面 9 面；W298×H147 cm／面"),
    ("包區 案二：籃筐 7 面", "進出月台層手扶梯正對牆面 7 面；W298×H147 cm／面"),
    ("籃筐 牆面 單面（TA-L3-64〜67 等）", "W298×H147 cm／面；進出月台層手扶梯正前方，視覺唯一焦點"),
    ("B1 燈箱（L4-52／53・L4-62／63 等）", "W386×H177 cm／面；進出南北月台手扶梯處與洗手間・商店旁"),
    ("1F PIDS Banner（6・7 號出口）", "W753×H169 cm；出口轉乘機場捷運 A18 → 桃園機場必經動線"),
    ("1F PIDS Banner（2・3 號出口）", "W753×H169 cm；桃園在地接送・商務出口動線"),
    ("1F 往 B1 手扶梯 牆面", "W3620.5×H227 cm；往 B1 候車大廳手扶梯・樓梯處搭車動線"),
]
row_ids = [(17, 18), (23, 24), (29, 30), (35, 36), (41, 42), (47, 48)]
for (lid, sid), (label, spec) in zip(row_ids, ROWS[:6]):
    rewrite_shape(by_id(ns, lid), label)
    rewrite_shape(by_id(ns, sid), spec)
# row 7: clone label/spec/divider from row 6 and shift down
PITCH = 0.28
for sid in (47, 48, 52):
    src_sh = by_id(ns, sid)
    el = copy.deepcopy(src_sh._element)
    spTree.append(el)
new_shapes = list(walk(ns.shapes))[-3:]
for k, sh in enumerate(new_shapes):
    sh.top = Emu(sh.top) + Inches(PITCH)
    cNvPr = sh._element.find(".//" + qn("p:cNvPr"))
    if cNvPr is not None:
        cNvPr.set("id", str(200 + k))
rewrite_shape(new_shapes[0], ROWS[6][0])
rewrite_shape(new_shapes[1], ROWS[6][1])

def set_node_style(sh, active):
    sh.fill.solid()
    sh.fill.fore_color.rgb = TEAL if active else WHITE
    sh.line.color.rgb = TEAL if active else INACT
    sh.line.width = Pt(1.4 if active else 1)
    for para in sh.text_frame.paragraphs:
        for r in para.runs:
            r.font.bold = active
            r.font.color.rgb = WHITE if active else INACT_T

set_node_style(by_id(ns, 88), False)   # 桃園機場 node -> gray
set_node_style(by_id(ns, 89), True)    # 高鐵桃園站 A18 -> lit
cal = by_id(ns, 90)
cal.left = Inches(8.55); cal.top = Inches(6.02); cal.width = Inches(2.0)
tf = cal.text_frame
rewrite_para(tf.paragraphs[0], "B1 候車大廳 籃筐包區・燈箱")
if len(tf.paragraphs) > 1:
    rewrite_para(tf.paragraphs[1], "1F PIDS（轉乘機捷必經）")
for para in tf.paragraphs:
    for r in para.runs:
        r.font.color.rgb = TEAL
        r.font.bold = True
chip = by_id(ns, 55)
chip.fill.solid(); chip.fill.fore_color.rgb = TEAL

# move new slide to position 28 (0-based 27)
sldIdLst = prs.slides._sldIdLst
el = list(sldIdLst)[-1]
sldIdLst.remove(el)
sldIdLst.insert(27, el)

# ---------- 4. reorder schedule rows (pages now 33 & 34 after insert) ----------
def shift_bands(slide, bands):
    for sh in list(walk(slide.shapes)):
        if sh.top is None:
            continue
        y = Emu(sh.top).inches
        for lo, hi, delta in bands:
            if lo <= y < hi:
                sh.top = Emu(sh.top) + Inches(delta)
                break

# p.33 (投放時機, 0-based 32)
shift_bands(prs.slides[32], [
    (5.32, 5.65, 0.33), (5.65, 5.98, 0.33), (5.98, 6.31, 0.33), (6.31, 6.64, -0.99),
])
# p.34 (年間排期, 0-based 33)
shift_bands(prs.slides[33], [
    (4.595, 4.935, 0.34), (4.935, 5.275, 0.34), (5.275, 5.615, -0.68),
])

prs.save(OUT)
print("saved", OUT, len(prs.slides))
