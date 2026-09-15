# -*- coding: utf-8 -*-
"""Transform the SMCC Visa deck: reorder, strip pricing, add route maps."""
import copy, os, re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "..", "【SMCC様】_Visaタッチについて（中文版）(2).pptx")
OUT = os.path.join(BASE, "..", "【SMCC様】_Visaタッチについて（中文版）(3)_提案版.pptx")

prs = Presentation(SRC)

NAVY = RGBColor(0x12, 0x20, 0x3F)
GRAY = RGBColor(0x6B, 0x7A, 0x90)
INACT = RGBColor(0xC9, 0xD2, 0xDE)
INACT_T = RGBColor(0x9A, 0xA3, 0xB0)
PANEL_BG = RGBColor(0xF7, 0xF9, 0xFC)
PANEL_LN = RGBColor(0xD6, 0xDD, 0xE8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

COLORS = {  # 動線 accent per page
    "blue": RGBColor(0x3E, 0x7C, 0xB1),
    "teal": RGBColor(0x1C, 0x72, 0x93),
    "orange": RGBColor(0xFF, 0x5A, 0x3C),
    "green": RGBColor(0x3F, 0x5D, 0x45),
}

def part_name(slide):
    return slide.part.partname.rsplit("/", 1)[-1]

def slide_by_part(name):
    for s in prs.slides:
        if part_name(s) == name:
            return s
    raise KeyError(name)

# ---------- 1. structure: move slide14 after slide11 ----------
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
el14 = ids[13]
sldIdLst.remove(el14)
sldIdLst.insert(11, el14)

# ---------- 2. delete package/quote slides 56,57,62,63,67 ----------
R_ID = qn("r:id")
drop_names = {"slide56.xml", "slide57.xml", "slide62.xml", "slide63.xml", "slide67.xml"}
for sldId in list(sldIdLst):
    rId = sldId.get(R_ID)
    part = prs.part.rels[rId].target_part
    if part.partname.rsplit("/", 1)[-1] in drop_names:
        prs.part.drop_rel(rId)
        sldIdLst.remove(sldId)
print("slides after delete:", len(prs.slides))

# ---------- helpers ----------
def shape_text(sh):
    return sh.text_frame.text if sh.has_text_frame else ""

def del_shape(sh):
    sh._element.getparent().remove(sh._element)

def iter_text_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == 6:  # group
            for sub in iter_text_shapes(sh.shapes):
                yield sub
        elif sh.has_text_frame:
            yield sh

def replace_in_runs(slide, pairs):
    for sh in iter_text_shapes(slide.shapes):
        for para in sh.text_frame.paragraphs:
            for run in para.runs:
                for a, b in pairs:
                    if a in run.text:
                        run.text = run.text.replace(a, b)

def rewrite_shape_text(sh, new_text):
    tf = sh.text_frame
    first = tf.paragraphs[0]
    runs = first.runs
    if runs:
        runs[0].text = new_text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        first.text = new_text
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)

def delete_paragraphs(slide, texts):
    for sh in iter_text_shapes(slide.shapes):
        for para in list(sh.text_frame.paragraphs):
            t = "".join(r.text for r in para.runs).strip()
            if t in texts:
                para._p.getparent().remove(para._p)

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

def add_label(shapes, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT, wrap=True):
    tb = shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        para = p if i == 0 else tf.add_paragraph()
        para.alignment = align
        run = para.add_run()
        run.text = ln
        set_font(run, size=size, bold=bold, color=color)
    return tb

def add_line(shapes, x1, y1, x2, y2, color, width_pt, dash=None, arrow=False):
    ln = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = color
    ln.line.width = Pt(width_pt)
    lnEl = ln.line._get_or_add_ln()
    if dash:
        d = lnEl.makeelement(qn("a:prstDash"), {"val": dash})
        lnEl.append(d)
    cap = lnEl.set("cap", "rnd")
    if arrow:
        te = lnEl.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"})
        lnEl.append(te)
    return ln

def add_polyline(shapes, pts, color, width_pt, dash=None, arrow=False):
    for i in range(len(pts) - 1):
        add_line(shapes, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], color, width_pt,
                 dash=dash, arrow=(arrow and i == len(pts) - 2))

def add_dot(shapes, x, y, d, fill, line_color=None):
    sp = shapes.add_shape(MSO_SHAPE.OVAL, Inches(x - d/2), Inches(y - d/2), Inches(d), Inches(d))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color; sp.line.width = Pt(1.2)
    sp.shadow.inherit = False
    return sp

def add_node(shapes, x, y, w, h, text, active, accent, size=8):
    sp = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    try: sp.adjustments[0] = 0.35
    except Exception: pass
    sp.fill.solid()
    sp.fill.fore_color.rgb = accent if active else WHITE
    sp.line.color.rgb = accent if active else INACT
    sp.line.width = Pt(1.4 if active else 1)
    sp.shadow.inherit = False
    tf = sp.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = text
    set_font(run, size=size, bold=active, color=(WHITE if active else INACT_T))
    return sp

# ---------- journey map ----------
PX, PY, PW, PH = 8.35, 1.90, 4.37, 5.05

def journey_panel(slide, accent, highlights, labels):
    """highlights: set of element keys to light up; labels: list of (x,y,w,text,anchor?) rel coords."""
    shapes = slide.shapes
    bg = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(PX), Inches(PY), Inches(PW), Inches(PH))
    try: bg.adjustments[0] = 0.03
    except Exception: pass
    bg.fill.solid(); bg.fill.fore_color.rgb = PANEL_BG
    bg.line.color.rgb = PANEL_LN; bg.line.width = Pt(1)
    bg.shadow.inherit = False

    def A(rx, ry):  # rel->abs
        return PX + rx, PY + ry

    # header
    add_label(shapes, PX + 0.18, PY + 0.10, 2.2, 0.25, "動線位置圖", 11, NAVY, bold=True)
    lg = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(PX + PW - 2.03), Inches(PY + 0.11), Inches(0.36), Inches(0.09))
    lg.fill.solid(); lg.fill.fore_color.rgb = accent; lg.line.fill.background(); lg.shadow.inherit = False
    try: lg.adjustments[0] = 0.5
    except Exception: pass
    add_label(shapes, PX + PW - 1.62, PY + 0.085, 0.72, 0.2, "本頁版位", 8, NAVY, bold=True)
    lg2 = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(PX + PW - 0.94), Inches(PY + 0.11), Inches(0.24), Inches(0.09))
    lg2.fill.solid(); lg2.fill.fore_color.rgb = INACT; lg2.line.fill.background(); lg2.shadow.inherit = False
    try: lg2.adjustments[0] = 0.5
    except Exception: pass
    add_label(shapes, PX + PW - 0.66, PY + 0.085, 0.6, 0.2, "其他動線", 8, INACT_T)

    def C(key):
        return accent if key in highlights else INACT
    def W_(key, on=2.6, off=1.6):
        return on if key in highlights else off

    # --- edges (draw inactive first, then active on top) ---
    def draw(key):
        act = key in highlights
        c = C(key); w = W_(key)
        if key == "hsr":
            add_polyline(shapes, [A(2.62, 2.62), A(1.95, 3.72), A(2.02, 4.32), A(2.32, 4.66), A(2.56, 4.90)], c, w)
        elif key == "airport_mrt":
            add_polyline(shapes, [A(2.45, 2.32), A(1.95, 2.55), A(1.30, 2.88)], c, w)
            add_polyline(shapes, [A(1.30, 3.12), A(1.55, 3.68)], c, w)
        elif key == "wenhu":
            add_polyline(shapes, [A(3.20, 1.58), A(3.50, 1.05)], c, w * 0.7)
        elif key == "mrt_city":
            for src, pt in [(A(2.80, 2.14), A(3.16, 1.64)), (A(2.55, 2.12), A(2.32, 1.68)), (A(3.18, 2.40), A(3.60, 2.52))]:
                add_line(shapes, *src, *pt, c, w * 0.7)
        elif key == "bus_dunhua":
            add_line(shapes, *A(3.30, 1.08), *A(3.08, 2.02), c, w * 0.8)
            add_line(shapes, *A(2.80, 1.64), *A(3.70, 1.48), c, w * 0.8)
        elif key == "bus_945":
            add_polyline(shapes, [A(1.92, 2.52), A(2.30, 1.50), A(3.00, 0.88)], c, w * 0.8, dash="dash")
        elif key == "bus_airport":
            add_polyline(shapes, [A(2.38, 2.50), A(1.72, 2.78), A(1.42, 3.02)], c, w, dash="dash")
        elif key == "taxi_out":
            add_polyline(shapes, [A(3.02, 1.72), A(2.02, 2.20), A(1.52, 2.72)], c, w, dash="sysDot")
        elif key == "taxi_return":
            add_polyline(shapes, [A(1.10, 3.22), A(2.35, 3.30), A(3.42, 2.25), A(3.42, 1.85)], c, w, dash="dash", arrow=True)

    order = ["wenhu", "mrt_city", "bus_dunhua", "bus_945", "bus_airport", "taxi_out", "taxi_return", "hsr", "airport_mrt"]
    order = [k for k in order if k in highlights or k not in ("taxi_out", "taxi_return")]
    for k in [k for k in order if k not in highlights] + [k for k in order if k in highlights]:
        draw(k)

    # --- station dots on lines ---
    for rx, ry, key in [(1.95, 2.55, "airport_mrt"), (2.02, 4.32, "hsr"), (2.32, 4.66, "hsr"), (2.56, 4.90, "hsr"), (3.20, 1.60, "mrt_city")]:
        add_dot(shapes, *A(rx, ry), 0.07, WHITE, line_color=C(key))
    # dot labels
    add_label(shapes, *A(1.55, 2.28), 0.8, 0.16, "林口", 7.5, NAVY if ("airport_mrt" in highlights or "bus_945" in highlights) else INACT_T)
    add_label(shapes, *A(2.14, 4.24), 0.8, 0.16, "台中", 7.5, NAVY if "hsr" in highlights else INACT_T)
    add_label(shapes, *A(2.44, 4.56), 0.8, 0.16, "台南", 7.5, NAVY if "hsr" in highlights else INACT_T)
    add_label(shapes, *A(2.68, 4.82), 1.0, 0.16, "高雄 左營", 7.5, NAVY if "hsr" in highlights else INACT_T)
    add_label(shapes, *A(2.98, 0.98), 1.3, 0.16, "敦化・民生商圈", 7.5,
              NAVY if ("bus_dunhua" in highlights or "mrt_city" in highlights or "taxi_out" in highlights) else INACT_T)

    # --- nodes ---
    add_node(shapes, *A(2.90, 0.42), 1.28, 0.36, "松山機場 TSA", any(k in highlights for k in ("bus_945", "wenhu")), accent, size=8)
    add_node(shapes, *A(2.12, 2.10), 1.10, 0.36, "台北車站", "tps" in highlights or "mrt_city" in highlights or "airport_mrt" in highlights, accent, size=8)
    add_node(shapes, *A(0.52, 2.72), 1.30, 0.44, "桃園機場 T1・T2", "tpe" in highlights, accent, size=8)
    add_node(shapes, *A(1.02, 3.66), 1.42, 0.36, "高鐵桃園站 A18", "a18" in highlights, accent, size=8)

    # --- callout labels ---
    for (rx, ry, w, text) in labels:
        add_label(shapes, *A(rx, ry), w, 0.5, text, 8, accent, bold=True)

    # line names (small, always)
    add_label(shapes, *A(0.62, 4.55), 1.4, 0.16, "高鐵（西部走廊）", 7.5, NAVY if "hsr" in highlights else INACT_T)

# ---------- 3. menu slide edits ----------
MENU = {
    "slide15.xml": "blue", "slide21.xml": "blue", "slide26.xml": "blue",
    "slide29.xml": "blue", "slide30.xml": "teal", "slide39.xml": "teal",
    "slide42.xml": "teal", "slide48.xml": "orange", "slide55.xml": "green",
}

for name in MENU:
    s = slide_by_part(name)
    for sh in list(s.shapes):
        if not sh.has_text_frame:
            continue
        l = Emu(sh.left).inches
        w = Emu(sh.width).inches
        if 8.0 <= l <= 12.0:
            del_shape(sh)
        elif 6.4 < l < 6.7 and w > 5:      # right-aligned section notes -> shift left
            sh.left = Inches(8.15 - w)
        elif l < 1.0 and w > 11:            # full-width dividers / footnotes -> stop at 8.15
            sh.width = Inches(8.15 - l)
    # non-text dividers (autoshapes/lines with tiny height)
    for sh in list(s.shapes):
        if sh.has_text_frame:
            continue
        try:
            l = Emu(sh.left).inches; w = Emu(sh.width).inches; h = Emu(sh.height).inches
        except Exception:
            continue
        if l < 1.0 and w > 11 and h < 0.06:
            sh.width = Inches(8.15 - l)

# spec-text price fragments
GLOBAL_PAIRS = [
    ("，製作 356,000／次", ""),
    ("，製作 889,000／次", ""),
    ("；上稿費 7,520,000／次", ""),
    ("；製作費最低（205,000／次）", ""),
    ("；單買合計 2,010,000／週", ""),
    ("；全案 CPM 最低", ""),
    ("｜免製作費", ""),
    ("燈箱 5,340,000／6,700,000；壁貼 8,760,000／區", "T2 入境動線 燈箱與壁貼版位"),
    ("松山機場 出境區（需另行報價）", "松山機場 出境區"),
    ("竹方案 年間排期", "建議年間排期"),
    ("SCHEDULE ・竹", "SCHEDULE"),
]
for s in prs.slides:
    replace_in_runs(s, GLOBAL_PAIRS)

# footnotes
s26 = slide_by_part("slide26.xml")
for sh in s26.shapes:
    if sh.has_text_frame and shape_text(sh).strip() == "26" and Emu(sh.top).inches < 6.5:
        sh.top = Inches(7.02)
for sh in list(s26.shapes):
    if sh.has_text_frame and shape_text(sh).startswith("※ CPM 為本案推估值"):
        del_shape(sh)
s29 = slide_by_part("slide29.xml")
for sh in s29.shapes:
    if sh.has_text_frame and shape_text(sh).startswith("※ 戶外看板之 CPM"):
        rewrite_shape_text(sh, "※ 熱門版面通常需提前 3–6 個月鎖檔。")
s55 = slide_by_part("slide55.xml")
for sh in s55.shapes:
    if sh.has_text_frame and shape_text(sh).startswith("※ 椅套 CPM"):
        rewrite_shape_text(sh, "※ 入境區版位之受眾為入境旅客，與出境區母體不同。")

# 目錄 bullets
s2 = slide_by_part("slide2.xml")
delete_paragraphs(s2, {
    "・單價、CPM、建議刊登檔次與刊登期間",
    "・建議版位的單價級距",
    "・內容與素材製作單價",
    "・各媒體類別中高性價比的推薦組合",
    "・年度預算配置總表與明細",
})

# ---------- 4. p29 row numbering + OSM maps ----------
NUMS = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪⑫"]
rows = []
for sh in s29.shapes:
    if sh.has_text_frame and abs(Emu(sh.left).inches - 0.62) < 0.05 and abs(Emu(sh.width).inches - 3.28) < 0.1:
        t = shape_text(sh)
        if t and (t.startswith("桃園") or t.startswith("台北") or t.startswith("新北") or t.startswith("新竹") or t.startswith("台中") or t.startswith("台南")):
            rows.append((Emu(sh.top).inches, sh))
rows.sort()
print("p29 rows found:", len(rows))
for i, (y, sh) in enumerate(rows):
    para = sh.text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = NUMS[i] + " " + para.runs[0].text

shp29 = s29.shapes
bg = shp29.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(PX), Inches(PY), Inches(PW), Inches(PH))
try: bg.adjustments[0] = 0.03
except Exception: pass
bg.fill.solid(); bg.fill.fore_color.rgb = PANEL_BG
bg.line.color.rgb = PANEL_LN; bg.line.width = Pt(1); bg.shadow.inherit = False
add_label(shp29, PX + 0.18, PY + 0.08, 2.4, 0.25, "戶外看板 據點位置圖", 11, NAVY, bold=True)
# legend
lx = PX + 0.18
for col, txt, wchip in [(COLORS["orange"], "Ⅰ 桃園動線", 0.95), (NAVY, "Ⅱ 台北・新北", 1.05), (COLORS["teal"], "Ⅲ 新竹・中南部", 1.2)]:
    dotc = shp29.add_shape(MSO_SHAPE.OVAL, Inches(lx), Inches(PY + 0.40), Inches(0.10), Inches(0.10))
    dotc.fill.solid(); dotc.fill.fore_color.rgb = col; dotc.line.fill.background(); dotc.shadow.inherit = False
    add_label(shp29, lx + 0.14, PY + 0.365, wchip, 0.18, txt, 8, NAVY)
    lx += 0.14 + wchip + 0.08
MW = 4.05
mx = PX + (PW - MW) / 2
nh = MW * 874 / 1427.0
sh_h = MW * 621 / 1477.0
pic1 = shp29.add_picture(os.path.join(BASE, "map_north.png"), Inches(mx), Inches(PY + 0.62), width=Inches(MW))
pic1.line.color.rgb = PANEL_LN; pic1.line.width = Pt(0.75)
add_label(shp29, mx + 0.08, PY + 0.68, 2.4, 0.2, "大台北・桃園（據點 ①–⑦）", 8, NAVY, bold=True)
y2 = PY + 0.62 + nh + 0.10
pic2 = shp29.add_picture(os.path.join(BASE, "map_south.png"), Inches(mx), Inches(y2), width=Inches(MW))
pic2.line.color.rgb = PANEL_LN; pic2.line.width = Pt(0.75)
add_label(shp29, mx + 0.08, y2 + 0.06, 2.6, 0.2, "全台西部走廊（據點 ⑧–⑫）", 8, NAVY, bold=True)
print("p29 maps bottom:", y2 + sh_h, "(panel bottom", PY + PH, ")")

# ---------- 5. journey panels ----------
PAGES = {
    "slide15.xml": dict(hl={"mrt_city", "airport_mrt", "tps"}, labels=[
        (2.30, 1.18, 1.9, "北捷月台電視 572 台\n＋導購屏 45 座"),
        (0.30, 2.02, 1.7, "桃捷月台電視 184 台\n（全線 21 站）"),
    ]),
    "slide21.xml": dict(hl={"tps"}, labels=[
        (2.02, 1.55, 2.1, "台北車站 站體數位\n大型 LED・75 吋柱體・拼接"),
    ]),
    "slide26.xml": dict(hl={"bus_dunhua", "bus_945"}, labels=[
        (2.30, 2.62, 2.0, "敦化・民生幹線 車內海報\n（262／278／617 等）"),
        (1.30, 1.26, 1.3, "945 松山機場線\n車體滿版"),
    ]),
    "slide30.xml": dict(hl={"airport_mrt", "a18", "tps"}, labels=[
        (0.28, 1.95, 1.8, "專車海報・車廂創意\n（整列・全線往返）"),
        (0.60, 4.12, 2.2, "A18 玻璃牆面（高鐵轉乘動線）"),
    ]),
    "slide39.xml": dict(hl={"bus_airport", "tpe"}, labels=[
        (0.30, 3.28, 2.2, "機場巴士 1819＋1840\n・1960 系 車體滿版"),
    ]),
    "slide42.xml": dict(hl={"taxi_out", "tpe"}, labels=[
        (1.95, 1.95, 2.0, "多元計程車 車內螢幕\n（去程・市區 → 桃機）"),
    ]),
    "slide48.xml": dict(hl={"tpe"}, labels=[
        (0.30, 3.30, 2.2, "桃機 T1／T2 出境大廳\n燈箱・數位看板"),
    ]),
    "slide55.xml": dict(hl={"taxi_return", "tpe"}, labels=[
        (1.60, 3.42, 2.4, "排班計程車 椅套 670 台\n（回程・車程 40–60 分）"),
        (0.30, 3.30, 1.6, "入境區 燈箱・數位"),
    ]),
}
for name, cfg in PAGES.items():
    s = slide_by_part(name)
    journey_panel(s, COLORS[MENU[name]], cfg["hl"], cfg["labels"])

prs.save(OUT)
print("saved", OUT)
