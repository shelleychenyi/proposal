# -*- coding: utf-8 -*-
"""Add THSR Taoyuan B1 (籃筐) pages into 版位照片集, stripping supplier branding/prices."""
import copy, os
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.oxml.ns import qn

BASE = os.path.dirname(os.path.abspath(__file__))
ALBUM = os.path.join(BASE, "..", "版位照片集.pptx")
HSR = os.path.join(BASE, "..", "高鐵", "【高鐵桃園站】0827騰訊」包區.pptx")
OUT = os.path.join(BASE, "..", "版位照片集_更新版.pptx")

tgt = Presentation(ALBUM)
src = Presentation(HSR)

# blank-ish layout in target
layout = min(tgt.slide_layouts, key=lambda l: len(l.placeholders))
print("using layout:", layout.name, len(layout.placeholders))

R_EMBED = qn("r:embed"); R_LINK = qn("r:link"); R_ID = qn("r:id")
from pptx.opc.package import Part

def copy_slide(src_slide):
    ns = tgt.slides.add_slide(layout)
    for shp in list(ns.shapes):
        shp._element.getparent().remove(shp._element)
    # map old rId -> new rId
    rmap = {}
    for rId, rel in src_slide.part.rels.items():
        if rel.reltype.endswith("/slideLayout") or rel.reltype.endswith("/notesSlide"):
            continue
        if rel.is_external:
            new_rId = ns.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        elif rel.reltype.endswith("/image"):
            from io import BytesIO
            _, new_rId = ns.part.get_or_add_image_part(BytesIO(rel.target_part.blob))
        else:
            raise ValueError("unexpected reltype: " + rel.reltype)
        rmap[rId] = new_rId
    spTree = ns.shapes._spTree
    for child in src_slide.shapes._spTree:
        tag = child.tag.split("}")[-1]
        if tag in ("nvGrpSpPr", "grpSpPr"):
            continue
        el = copy.deepcopy(child)
        for node in el.iter():
            for attr in (R_EMBED, R_LINK, R_ID):
                v = node.get(attr)
                if v and v in rmap:
                    node.set(attr, rmap[v])
        spTree.append(el)
    return ns

def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            for sub in walk(sh.shapes):
                yield sub

def shape_all_text(sh):
    out = []
    for s in walk([sh]) if sh.shape_type == 6 else [sh]:
        if s.has_text_frame:
            out.append(s.text_frame.text)
    return " ".join(out)

new_slides = [copy_slide(src.slides[i]) for i in (11, 12, 13)]

for i, ns in enumerate(new_slides):
    for sh in list(ns.shapes):
        txt = shape_all_text(sh)
        top = Emu(sh.top).inches if sh.top is not None else 0
        kill = False
        if "inspire activation" in txt or "創異促動" in txt:
            kill = True
        elif sh.shape_type == 14:  # placeholder page number
            kill = True
        elif "交通部>交通統計" in txt or "statis.motc.gov.tw" in txt:
            kill = True
        elif "NT$" in txt:
            kill = True
        elif "媒體費" in txt or "製作費" in txt:
            kill = True
        if kill:
            sh._element.getparent().remove(sh._element)
    # per-slide extras
    if i in (1, 2):
        for sh in list(ns.shapes):
            if sh.shape_type == 9:  # LINE dividers of removed price rows
                x = Emu(sh.left).inches; y = Emu(sh.top).inches; w = Emu(sh.width).inches
                if 8.5 < x < 9.0 and w > 3 and (2.5 < y < 2.9 or 3.4 < y < 3.9):
                    sh._element.getparent().remove(sh._element)
        for sh in ns.shapes:  # shrink right info card
            if sh.shape_type == 1 and abs(Emu(sh.left).inches - 8.50) < 0.05 and Emu(sh.height).inches > 4:
                sh.height = Inches(2.15)
    else:
        # fix supplier's station typo on the floor-plan page
        for sh in walk(ns.shapes):
            if sh.has_text_frame:
                for para in sh.text_frame.paragraphs:
                    for run in para.runs:
                        if "HSR Banqiao Station" in run.text:
                            run.text = run.text.replace("HSR Banqiao Station", "THSR Taoyuan Station")

# move the 3 appended slides to sit after slide 30 (機場捷運 section)
sldIdLst = tgt.slides._sldIdLst
ids = list(sldIdLst)
appended = ids[-3:]
for k, el in enumerate(appended):
    sldIdLst.remove(el)
    sldIdLst.insert(30 + k, el)

tgt.save(OUT)
print("saved", OUT, "slides:", len(tgt.slides))
