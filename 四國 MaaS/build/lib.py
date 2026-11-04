# -*- coding: utf-8 -*-
"""Intasect 版型小工具：沿用 Hakuba 中文版的母片與字級。"""
import copy, os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY, INK, RED, TEAL, GREY = "272673", "12203F", "C0504D", "299294", "6B7A90"
SOFT, SOFT2, LINE, WHITE = "F5F7FB", "EAF0F8", "DDE3EC", "FFFFFF"
BLUE, GREEN, ORANGE, GOLD, PALE_G = "2A7BBF", "06C755", "E8572A", "F2A541", "E8F6EE"
FONT = "Microsoft JhengHei"


def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self, base):
        self.prs = Presentation(base)
        self.groups = {}
        self._cur = None
        self.page = 1

    # ---------- slide management ----------
    def keep_only(self, keep_idx):
        sldIdLst = self.prs.slides._sldIdLst
        ids = list(sldIdLst)
        for i, sid in enumerate(ids):
            if i not in keep_idx:
                self.prs.part.drop_rel(sid.rId)
                sldIdLst.remove(sid)
        from pptx.opc.packuri import PackURI
        for i, sl in enumerate(self.prs.slides, 1):
            sl.part.partname = PackURI(f"/ppt/slides/slide{i}.xml")

    def move_to_end(self, slide):
        lst = self.prs.slides._sldIdLst
        for sid in list(lst):
            if self.prs.slides.get(int(sid.get("id"))) is slide:
                lst.remove(sid)
                lst.append(sid)

    def new(self, title, lead, source=None):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        self.page += 1
        self.tx(s, 0.0, 0.13, 10.7, 0.45, title, 24, NAVY, True, anchor="m")
        self.tx(s, 0.45, 0.80, 12.45, 0.62, lead, 12.5, INK, True)
        self.tx(s, 12.30, 7.10, 0.70, 0.25, str(self.page), 9, GREY, align="r", font="Meiryo")
        if source:
            self.tx(s, 0.45, 6.90, 11.7, 0.26, source, 7.5, GREY)
        return s

    # ---------- primitives ----------
    def _track(self, s, shp):
        if self._cur is not None:
            self._cur.append(shp.shape_id)
        return shp

    def tx(self, s, x, y, w, h, text, size=10, color=INK, bold=False, align="l",
           anchor="t", font=FONT, line=1.15, margin=0.04):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        for side in ("left", "right", "top", "bottom"):
            setattr(tf, f"margin_{side}", Inches(margin))
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        paras = text if isinstance(text, list) else str(text).split("\n")
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            para.line_spacing = line
            runs = p if isinstance(p, tuple) or isinstance(p, list) else [(p, {})]
            if isinstance(p, tuple):
                runs = [p]
            for seg in runs:
                if isinstance(seg, str):
                    seg = (seg, {})
                t, o = seg
                r = para.add_run()
                r.text = t
                f = r.font
                f.name = font
                f.size = Pt(o.get("size", size))
                f.bold = o.get("bold", bold)
                f.color.rgb = rgb(o.get("color", color))
                rPr = r._r.get_or_add_rPr()
                for tag in ("a:ea", "a:cs"):
                    el = rPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}" + tag.split(":")[1])
                    if el is None:
                        el = etree.SubElement(rPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}" + tag.split(":")[1])
                    el.set("typeface", font)
        return self._track(s, tb)

    def rect(self, s, x, y, w, h, fill=SOFT, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None, lw=0.75):
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill:
            sh.fill.solid()
            sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line)
            sh.line.width = Pt(lw)
        else:
            sh.line.fill.background()
        sh.shadow.inherit = False
        if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = radius
        if sh.has_text_frame:
            sh.text_frame.text = ""
        return self._track(s, sh)

    def rrect(self, s, x, y, w, h, fill=SOFT, line=None, radius=0.08, lw=0.75):
        return self.rect(s, x, y, w, h, fill, line, MSO_SHAPE.ROUNDED_RECTANGLE, radius, lw)

    def label(self, s, x, y, w, h, text, fill, color=WHITE, size=10, bold=True, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
              radius=0.2, align="c", font=FONT):
        sh = self.rect(s, x, y, w, h, fill, None, shape, radius if shape == MSO_SHAPE.ROUNDED_RECTANGLE else None)
        tf = sh.text_frame
        tf.word_wrap = True
        for side in ("left", "right", "top", "bottom"):
            setattr(tf, f"margin_{side}", Inches(0.03))
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        lines = text.split("\n")
        for i, t in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER}[align]
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.name = font
            r.font.color.rgb = rgb(color)
            rPr = r._r.get_or_add_rPr()
            ea = etree.SubElement(rPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}ea")
            ea.set("typeface", font)
        return sh

    def circle(self, s, x, y, d, text, fill, size=10, color=WHITE):
        return self.label(s, x, y, d, d, text, fill, color, size, shape=MSO_SHAPE.OVAL, font="Meiryo")

    def arrow(self, s, x, y, w, h, fill="B8C4D6", shape=MSO_SHAPE.RIGHT_ARROW):
        return self.rect(s, x, y, w, h, fill, None, shape)

    def hline(self, s, x1, y1, x2, y2, color=LINE, width=1.25, dash=False):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color)
        ln.line.width = Pt(width)
        if dash:
            from pptx.enum.dml import MSO_LINE
            ln.line.dash_style = MSO_LINE.DASH
        return self._track(s, ln)

    def pic(self, s, path, x, y, w, h, mode="fit", crop=None):
        """fit：等比放進框內置中；cover：裁切填滿框。"""
        path = os.path.join(HERE, path) if not os.path.isabs(path) else path
        im = Image.open(path)
        iw, ih = im.size
        if crop:
            l, t, r, b = crop
            iw2, ih2 = iw * (1 - l - r), ih * (1 - t - b)
        else:
            l = t = r = b = 0
            iw2, ih2 = iw, ih
        ar = iw2 / ih2
        if mode == "fit":
            if w / h > ar:
                nw, nh = h * ar, h
            else:
                nw, nh = w, w / ar
            p = s.shapes.add_picture(path, Inches(x + (w - nw) / 2), Inches(y + (h - nh) / 2), Inches(nw), Inches(nh))
            if crop:
                p.crop_left, p.crop_top, p.crop_right, p.crop_bottom = l, t, r, b
        else:
            p = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
            box = w / h
            if ar > box:  # too wide -> crop sides
                extra = (1 - box / ar) * (1 - l - r)
                p.crop_left, p.crop_right = l + extra / 2, r + extra / 2
                p.crop_top, p.crop_bottom = t, b
            else:
                extra = (1 - ar / box) * (1 - t - b)
                p.crop_top, p.crop_bottom = t + extra / 2, b + extra / 2
                p.crop_left, p.crop_right = l, r
        return self._track(s, p)

    def poly(self, s, pts, fill):
        E = 914400
        fb = s.shapes.build_freeform(int(pts[0][0] * E), int(pts[0][1] * E), scale=1.0)
        fb.add_line_segments([(int(x * E), int(y * E)) for x, y in pts[1:]], close=True)
        sh = fb.convert_to_shape()
        sh.fill.solid()
        sh.fill.fore_color.rgb = rgb(fill)
        sh.line.fill.background()
        sh.shadow.inherit = False
        return self._track(s, sh)

    def ai_tag(self, s, x, y, text="AI示意"):
        return self.label(s, x, y, 0.62, 0.2, text, "555555", size=7, bold=False, radius=0.15)

    # ---------- animation ----------
    def anim(self, s):
        """with d.anim(s): 期間加入的圖形成為一組；組依序淡入。"""
        deck = self

        class _G:
            def __enter__(self_):
                deck._cur = []
                return self_

            def __exit__(self_, *a):
                deck.groups.setdefault(id(s), (s, []))[1].append(deck._cur)
                deck._cur = None
        return _G()

    def apply_animations(self, step=0.45, dur=450):
        P = "http://schemas.openxmlformats.org/presentationml/2006/main"
        for s, groups in self.groups.values():
            groups = [g for g in groups if g]
            if not groups:
                continue
            nid = [3]

            def cid():
                nid[0] += 1
                return nid[0]

            inner = []
            delay = 0
            for gi, g in enumerate(groups):
                effects = []
                for k, spid in enumerate(g):
                    node = "afterEffect" if (k == 0) else "withEffect"
                    if gi == 0 and k == 0:
                        node = "afterEffect"
                    effects.append(f'''<p:par><p:cTn id="{cid()}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{cid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{cid()}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par>''')
                inner.append(f'''<p:par><p:cTn id="{cid()}" fill="hold"><p:stCondLst><p:cond delay="{int(delay)}"/></p:stCondLst><p:childTnLst>{''.join(effects)}</p:childTnLst></p:cTn></p:par>''')
                delay += step * 1000
            bld = "".join(f'<p:bldP spid="{spid}" grpId="0" animBg="1"/>' for g in groups for spid in g)
            xml = f'''<p:timing xmlns:p="{P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>
{''.join(inner)}
</p:childTnLst></p:cTn></p:par>
</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>
</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'''
            el = etree.fromstring(xml)
            sld = s._element
            old = sld.find(f"{{{P}}}timing")
            if old is not None:
                sld.remove(old)
            # timing must come after clrMapOvr / transition
            ext = sld.find(f"{{{P}}}extLst")
            if ext is not None:
                ext.addprevious(el)
            else:
                sld.append(el)

    def save(self, path, animate=True):
        if animate:
            self.apply_animations()
        self.prs.save(path)
