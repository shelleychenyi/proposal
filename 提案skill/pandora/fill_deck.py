# -*- coding: utf-8 -*-
"""把聚合後的指標寫回提案範本。

回填靠的是範本裡的具名圖形（PD:*），不是文字比對，所以改文案不會弄壞回填。
圖表用 PowerPoint 原生圖表插入，取代範本上的虛線佔位框。
"""
from __future__ import annotations

import copy
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Emu, Pt

INK = RGBColor(0x12, 0x20, 0x3F)
ACCENT = RGBColor(0xC0, 0x50, 0x4D)
MUTED = RGBColor(0x6B, 0x7A, 0x90)
SERIES_COLORS = [RGBColor(0x4A, 0x5F, 0xA5), RGBColor(0xC0, 0x50, 0x4D), RGBColor(0x85, 0x98, 0xC4),
                 RGBColor(0xBA, 0xC5, 0xDC), RGBColor(0x27, 0x26, 0x73), RGBColor(0x9A, 0xA9, 0xC0)]
SENTIMENT_COLORS = [RGBColor(0x27, 0x26, 0x73), RGBColor(0x4A, 0x5F, 0xA5), RGBColor(0xBA, 0xC5, 0xDC),
                    RGBColor(0xD9, 0x8B, 0x88), RGBColor(0xC0, 0x50, 0x4D)]

PLATFORM_LABEL = {"threads": "Threads", "instagram": "Instagram", "dcard": "Dcard",
                  "ptt": "PTT", "fb": "Facebook", "mobile01": "Mobile01"}


# ---------------- shape helpers ----------------
def index_shapes(prs) -> dict:
    return {sh.name: sh for slide in prs.slides for sh in slide.shapes if sh.name.startswith("PD:")}


def _slide_of(prs, shape):
    for slide in prs.slides:
        if shape._element in list(slide.shapes._spTree):
            return slide
    return None


def set_text(shape, lines) -> None:
    """保留原有字型／字級／顏色，只換文字內容。lines 可為 str 或 list[str]。"""
    if isinstance(lines, str):
        lines = [lines]
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    runs = p0.runs
    if not runs:
        return
    rPr = copy.deepcopy(runs[0]._r.get_or_add_rPr())
    _pPr = p0._p.find(_q("a:pPr"))
    pPr = copy.deepcopy(_pPr) if _pPr is not None else None

    txBody = tf._txBody
    for p in list(txBody.findall(_q("a:p"))):
        txBody.remove(p)
    for text in lines:
        p = txBody.makeelement(_q("a:p"), {})
        if pPr is not None:
            p.append(copy.deepcopy(pPr))
        r = txBody.makeelement(_q("a:r"), {})
        r.append(copy.deepcopy(rPr))
        tnode = txBody.makeelement(_q("a:t"), {})
        tnode.text = text
        r.append(tnode)
        p.append(r)
        txBody.append(p)


def _q(tag: str) -> str:
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    prefix, local = tag.split(":")
    return "{%s}%s" % (ns[prefix], local)


def set_bar_width(shape, inches: float) -> None:
    shape.width = Emu(int(inches * 914400))


# ---------------- charts ----------------
def _style_chart(chart, font_pt=7):
    chart.font.size = Pt(font_pt)
    chart.font.color.rgb = MUTED
    chart.has_title = False


def replace_with_line_chart(prs, shape, categories, values, name="聲量"):
    slide = _slide_of(prs, shape)
    left, top, width, height = shape.left, shape.top, shape.width, shape.height
    data = CategoryChartData()
    data.categories = categories
    data.add_series(name, values)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, left, top, width, height, data)
    chart = gf.chart
    _style_chart(chart)
    chart.has_legend = False
    ser = chart.plots[0].series[0]
    ser.format.line.color.rgb = SERIES_COLORS[0]
    ser.format.line.width = Pt(1.5)
    chart.value_axis.has_major_gridlines = True
    chart.value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xE6, 0xEB, 0xF2)
    chart.value_axis.major_gridlines.format.line.width = Pt(0.5)
    chart.category_axis.has_major_gridlines = False
    shape._element.getparent().remove(shape._element)
    return chart


def replace_with_pie_chart(prs, shape, categories, values, *, doughnut=True, colors=None,
                           legend=True):
    slide = _slide_of(prs, shape)
    left, top, width, height = shape.left, shape.top, shape.width, shape.height
    data = CategoryChartData()
    data.categories = categories
    data.add_series("share", values)
    ctype = XL_CHART_TYPE.DOUGHNUT if doughnut else XL_CHART_TYPE.PIE
    gf = slide.shapes.add_chart(ctype, left, top, width, height, data)
    chart = gf.chart
    _style_chart(chart, 6)
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
    pal = colors or SERIES_COLORS
    points = chart.plots[0].series[0].points
    for i, point in enumerate(points):
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = pal[i % len(pal)]
        point.format.line.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        point.format.line.width = Pt(0.75)
    shape._element.getparent().remove(shape._element)
    return chart


# ---------------- main fill ----------------
def _fmt(n) -> str:
    return f"{int(round(n)):,}"


def _pct(x) -> str:
    return f"{x * 100:.1f}％"


def fill(template_path: Path, out_path: Path, groups, cfg, lang="zh") -> Path:
    """groups: [{'label':..., 'metrics': {...}}, ...]（最多 2 組，對應範本的左右兩張卡）"""
    prs = Presentation(str(template_path))
    S = index_shapes(prs)
    ja = lang == "ja"
    unit = "件"

    for gi, g in enumerate(groups[:2], 1):
        m = g["metrics"]
        if f"PD:g{gi}.label" in S:
            set_text(S[f"PD:g{gi}.label"], g["label"])
        for key in ("totalVolume", "postCount", "likes", "comments"):
            if f"PD:g{gi}.{key}" in S:
                set_text(S[f"PD:g{gi}.{key}"], _fmt(m[key]))

        # 月度趨勢折線圖
        anchor = S.get(f"PD:g{gi}.chart.trend")
        if anchor is not None and m["trend"]:
            replace_with_line_chart(
                prs, anchor,
                [t["month"][2:] for t in m["trend"]],
                [t["volume"] for t in m["trend"]],
                name="声量" if ja else "聲量")

        # 平台分布環圈圖
        anchor = S.get(f"PD:g{gi}.chart.platform")
        if anchor is not None and m["platforms"]:
            top = m["platforms"][:5]
            replace_with_pie_chart(
                prs, anchor,
                [PLATFORM_LABEL.get(p["source"], p["source"]) for p in top],
                [p["volumeShare"] for p in top])

        # 重點條列
        if f"PD:g{gi}.bullets" in S:
            peak, plats = m["peakMonth"], m["platforms"][:3]
            share = "、".join(f"{PLATFORM_LABEL.get(p['source'], p['source'])} {_pct(p['volumeShare'])}"
                             for p in plats)
            if ja:
                lines = [
                    f"・声量ピークは {peak['month']}（{_fmt(peak['volume'])}）" if peak else "・—",
                    f"・言及の内訳は {share}",
                    f"・直近期間の投稿数は {_fmt(m['postCount'])}件、総いいね {_fmt(m['likes'])}・"
                    f"総コメント {_fmt(m['comments'])}",
                ]
            else:
                lines = [
                    f"・聲量高峰為 {peak['month']}（{_fmt(peak['volume'])}）" if peak else "・—",
                    f"・平台占比為 {share}",
                    f"・期間內貼文數 {_fmt(m['postCount'])} 篇，總按讚 {_fmt(m['likes'])}、"
                    f"總留言 {_fmt(m['comments'])}",
                ]
            set_text(S[f"PD:g{gi}.bullets"], lines)

    # ---- 情緒分布（以第一組為準，或全部合併，由 cfg 決定） ----
    sm = (cfg.get("sentimentSource") or "g1")
    base = groups[0]["metrics"] if sm == "g1" else cfg["_merged"]
    sent = base["sentiment"]
    from metrics import BAND_KEYS
    max_share = max(sent["share"].values()) or 1.0
    for i, k in enumerate(BAND_KEYS, 1):
        if f"PD:sent.pct{i}" in S:
            set_text(S[f"PD:sent.pct{i}"], _pct(sent["share"][k]))
        if f"PD:sent.bar{i}" in S:
            set_bar_width(S[f"PD:sent.bar{i}"], 0.06 + 1.84 * (sent["share"][k] / max_share))
    if "PD:sent.positiveRate" in S:
        set_text(S["PD:sent.positiveRate"],
                 (f"ポジティブ比率（非常に good ＋ good）＝ {_pct(sent['positiveRate'])}／基準値"
                  f"（評価済 {_fmt(sent['scoredCount'])}件・未評価 {_fmt(sent['unscoredCount'])}件は除外）")
                 if ja else
                 (f"正面比率（非常正面＋正面）＝ {_pct(sent['positiveRate'])}／基準線"
                  f"（已評分 {_fmt(sent['scoredCount'])} 篇；未評分 {_fmt(sent['unscoredCount'])} 篇已排除）"))
    anchor = S.get("PD:chart.sentiment")
    if anchor is not None and sent["scoredCount"]:
        labels = (["非常に good", "good", "中立", "bad", "非常に bad"] if ja
                  else ["非常正面", "正面", "中性", "負面", "非常負面"])
        replace_with_pie_chart(prs, anchor, labels, [sent["share"][k] for k in BAND_KEYS],
                               doughnut=False, colors=SENTIMENT_COLORS)

    # ---- 渠道分布 ----
    plats = base["platforms"][:5]
    for i in range(1, 6):
        nm, pc = S.get(f"PD:chan.name{i}"), S.get(f"PD:chan.pct{i}")
        if i <= len(plats):
            p = plats[i - 1]
            if nm is not None:
                set_text(nm, PLATFORM_LABEL.get(p["source"], p["source"]))
            if pc is not None:
                set_text(pc, _pct(p["volumeShare"]))
        else:
            if nm is not None:
                set_text(nm, "—")
            if pc is not None:
                set_text(pc, "—")

    # ---- KPI 頁 ----
    uplift = float(cfg.get("kpi", {}).get("upliftPercent", 30))
    factor = 1 + uplift / 100
    detail = []
    for gi, g in enumerate(groups[:2], 1):
        before = g["metrics"]["totalVolume"]
        after = int(round(before * factor))
        if f"PD:kpi.g{gi}.label" in S:
            set_text(S[f"PD:kpi.g{gi}.label"], g["label"])
        if f"PD:kpi.g{gi}.before" in S:
            set_text(S[f"PD:kpi.g{gi}.before"], f"{_fmt(before)}{unit}")
        if f"PD:kpi.g{gi}.after" in S:
            set_text(S[f"PD:kpi.g{gi}.after"], f"{_fmt(after)}{unit}（＋{uplift:g}％）")
        if f"PD:kpi.g{gi}.barAfter" in S:
            set_bar_width(S[f"PD:kpi.g{gi}.barAfter"], min(3.75, 2.84 * factor))
        detail.append(f"{g['label']}　{_fmt(before)}{unit} → {_fmt(after)}{unit}"
                      f"（＋{_fmt(after - before)}{unit}）")
    if "PD:kpi.uplift" in S:
        set_text(S["PD:kpi.uplift"], f"＋{uplift:g}％")
    if "PD:kpi.detail" in S:
        set_text(S["PD:kpi.detail"], detail)

    kpi = cfg.get("kpi", {})
    imp, posts_n = kpi.get("impressionsPerPost"), kpi.get("postCount")
    if imp and posts_n and "PD:kpi.impressions" in S:
        lo, hi = int(imp[0]) * int(posts_n), int(imp[1]) * int(posts_n)
        set_text(S["PD:kpi.impressions"], f"{_fmt(lo)} 〜 {_fmt(hi)} " + ("回" if ja else "次"))
        if "PD:kpi.impressionsNote" in S:
            set_text(S["PD:kpi.impressionsNote"],
                     f"投稿表示回数の想定（1投稿あたり{_fmt(imp[0])}〜{_fmt(imp[1])}回 × {_fmt(posts_n)}投稿）"
                     if ja else
                     f"投稿曝光次數之想定（每則 {_fmt(imp[0])}〜{_fmt(imp[1])} 次 × {_fmt(posts_n)} 則投稿）")
    reg = kpi.get("registrations")
    if reg and "PD:kpi.registrations" in S:
        set_text(S["PD:kpi.registrations"], f"{_fmt(reg[0])} 〜 {_fmt(reg[1])} 人")

    # ---- 全域字串替換（日期區間、專案名等） ----
    for token, value in (cfg.get("tokens") or {}).items():
        _replace_token(prs, token, value)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    return out_path


def _replace_token(prs, token, value):
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if token in run.text:
                        run.text = run.text.replace(token, value)
