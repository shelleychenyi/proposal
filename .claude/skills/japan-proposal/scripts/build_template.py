# -*- coding: utf-8 -*-
"""Intasect 提案範本 — 繁中版／日本語版。視覺全部沿用「最終版-SMCC向け…」的母片與版型。"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches as I, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

LANG = sys.argv[1]                      # 'zh' | 'ja'
def t(zh, ja): return zh if LANG == 'zh' else ja

# ---------- design tokens ----------
INK    = RGBColor(0x12, 0x20, 0x3F)
DARKI  = RGBColor(0x0B, 0x18, 0x38)
TITLE  = RGBColor(0x27, 0x26, 0x73)
MUTED  = RGBColor(0x6B, 0x7A, 0x90)
MUTED2 = RGBColor(0x55, 0x65, 0x82)
CARD   = RGBColor(0xF4, 0xF7, 0xFB)
BORDER = RGBColor(0xD6, 0xDD, 0xE8)
BARGRY = RGBColor(0xBA, 0xC5, 0xDC)
ACCENT = RGBColor(0xC0, 0x50, 0x4D)
RED    = RGBColor(0xFF, 0x00, 0x00)
ORANGE = RGBColor(0xFF, 0x5A, 0x3C)
ORTXT  = RGBColor(0xFF, 0x4F, 0x36)
BLUEBR = RGBColor(0x4A, 0x5F, 0xA5)
BLUETX = RGBColor(0x4C, 0x60, 0xAA)
BLUEMD = RGBColor(0x85, 0x98, 0xC4)
BLUETM = RGBColor(0x78, 0x8C, 0xB4)
HOLIBG = RGBColor(0xFF, 0xF3, 0xF0)
AXIS   = RGBColor(0x9A, 0xA9, 0xC0)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
POSTBG = RGBColor(0x14, 0x14, 0x14)
LAT = "Meiryo"
EA  = "Microsoft JhengHei" if LANG == 'zh' else "メイリオ"

def _font(run, sz, bold=False, color=INK, latin=LAT, ea=None):
    ea = ea or EA
    f = run.font; f.size = Pt(sz); f.bold = bold; f.color.rgb = color; f.name = latin
    rPr = run._r.get_or_add_rPr()
    for tag, tf in (('a:ea', ea), ('a:cs', latin)):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {}); rPr.append(el)
        el.set('typeface', tf)

def _nm(shape, name):
    if name: shape.name = name
    return shape

def tb(sl, x, y, w, h, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    s = sl.shapes.add_textbox(I(x), I(y), I(w), I(h))
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    tf.paragraphs[0].alignment = align
    return s

def put(sl, x, y, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=0, lnspc=None, name=None):
    s = tb(sl, x, y, w, h, align, anchor); tf = s.text_frame
    for i, ln in enumerate(lines):
        txt, sz, b, c = ln[:4]
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if space and i: p.space_before = Pt(space)
        if lnspc: p.line_spacing = lnspc
        r = p.add_run(); r.text = txt; _font(r, sz, b, c)
    return _nm(s, name)

def runs(sl, x, y, w, h, chunks, sz, lnspc=1.5, space=0):
    """chunks: list of paragraphs; each paragraph = list of (text, bold, color)"""
    s = tb(sl, x, y, w, h); tf = s.text_frame
    for i, chunk in enumerate(chunks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = lnspc
        if space and i: p.space_before = Pt(space)
        for txt, b, c in chunk:
            r = p.add_run(); r.text = txt; _font(r, sz, b, c)
    return s

def rect(sl, x, y, w, h, fill=CARD, line=BORDER, lw=0.75, rounded=False, adj=None, name=None):
    shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                              I(x), I(y), I(w), I(h))
    if rounded and adj is not None: shp.adjustments[0] = adj
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    shp.text_frame.word_wrap = True
    return _nm(shp, name)

def line(sl, x1, y1, x2, y2, color=BORDER, lw=0.75):
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, I(x1), I(y1), I(x2), I(y2))
    c.line.color.rgb = color; c.line.width = Pt(lw)
    return c

def chip(sl, x, y, w, h, text, fill=INK, color=WHITE, sz=8.5, adj=0.5, name=None):
    r = rect(sl, x, y, w, h, fill=fill, line=None, rounded=True, adj=adj)
    tfr = r.text_frame
    tfr.margin_left = tfr.margin_right = tfr.margin_top = tfr.margin_bottom = 0
    tfr.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tfr.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = text; _font(run, sz, True, color)
    return _nm(r, name)

def ph_img(sl, x, y, w, h, label, name=None):
    r = rect(sl, x, y, w, h, fill=WHITE, line=BORDER); r.line.dash_style = 4
    tfr = r.text_frame; tfr.margin_left = tfr.margin_right = I(0.06)
    tfr.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tfr.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = label; _font(run, 8, False, MUTED)
    return _nm(r, name)

def title(sl, num, text):
    s = tb(sl, 0.0, 0.133, 7.44, 0.446); s.text_frame.margin_left = I(0.1)
    p = s.text_frame.paragraphs[0]
    for seg in (f"{num}.", text):
        r = p.add_run(); r.text = seg
        _font(r, 24, True, TITLE, latin="メイリオ", ea="メイリオ")

def lead(sl, text, y=1.02, h=0.55, x=0.62, w=12.09):
    put(sl, x, y, w, h, [(text, 14, True, INK)], lnspc=1.25)

def footer(sl, src, page, note=None):
    if note: put(sl, 0.62, 6.36, 12.10, 0.28, [(note, 8, False, MUTED)])
    put(sl, 0.62, 6.94, 11.72, 0.30, [(s, 8, False, MUTED) for s in src], lnspc=1.2)
    put(sl, 12.05, 7.09, 0.66, 0.15, [(str(page), 9, False, MUTED)], align=PP_ALIGN.RIGHT)

def bullets(sl, x, y, w, h, items, sz=8.5, color=INK, space=2.5, name=None):
    return put(sl, x, y, w, h, [("・" + s, sz, False, color) for s in items],
               space=space, lnspc=1.25, name=name)

# ---------- 以最終版為底：保留封面(1)與封底(10)，其餘重建 ----------
BASE_DECK = Path(__file__).resolve().parent.parent / "assets" / "base_deck.pptx"
OUT_DIR = Path(__file__).resolve().parent.parent / "assets"
prs = Presentation(str(BASE_DECK))
ids = list(prs.slides._sldIdLst)
for sid in ids[1:9]:
    prs.part.drop_rel(sid.get(qn('r:id'))); prs.slides._sldIdLst.remove(sid)
cover_id, back_id = list(prs.slides._sldIdLst)
# 封底原本佔用 slide10.xml，先讓出編號，避免新增投影片時 partname 撞名
from pptx.opc.packuri import PackURI
prs.slides[1].part.partname = PackURI('/ppt/slides/slide2.xml')

# --- 封面文字改為佔位 ---
cover = prs.slides[0]
for sh in cover.shapes:
    if not sh.has_text_frame: continue
    txt = sh.text_frame.text
    if "御中" in txt:
        sh.text_frame.clear()
        p = sh.text_frame.paragraphs[0]
        r = p.add_run(); r.text = t("【客戶名】　敬呈", "【クライアント名】　御中")
        _font(r, 20, False, RGBColor(0x3A, 0x42, 0x56), latin="メイリオ", ea="メイリオ")
    elif "キャッシュバック" in txt or "ご提案" in txt:
        sh.text_frame.clear()
        for i, ln in enumerate([t("【提案主標題：一行寫完本次施策的主張】",
                                  "【提案メインタイトル：施策の主張を一行で】"),
                                t("台灣市場　【平台】口碑施策提案",
                                  "台湾市場向け　【プラットフォーム】口コミ施策のご提案")]):
            p = sh.text_frame.paragraphs[0] if i == 0 else sh.text_frame.add_paragraph()
            r = p.add_run(); r.text = ln
            _font(r, 24, True, RGBColor(0x00, 0x00, 0x00), latin="メイリオ", ea="メイリオ")

BLANK = prs.slide_masters[0].slide_layouts[6]
def new():
    sl = prs.slides.add_slide(BLANK)
    for shp in list(sl.shapes): shp._element.getparent().remove(shp._element)
    return sl

SRC_PAN = [t("資料來源：Pandora by The Pocket Company／Accucrazy「【專案名】聲量報告」（資料期間：【yyyy/m/d–yyyy/m/d】）",
             "出典：Pandora by The Pocket Company／Accucrazy「【案件名】声量レポート」（データ期間：【yyyy年m月d日–yyyy年m月d日】）"),
           t("※ 總聲量為加權彙總按讚・留言等互動之 Pandora 獨自指標（10＋按讚×3＋留言×5）。上方圖表由 Pandora API 實測資料產生。",
             "※ 総声量は、いいね・コメント等の反応を加重集計したPandora独自指標です（10＋いいね×3＋コメント×5）。上記グラフはPandora APIの実測データから生成しています。")]

# ================= P1｜台灣消費者的行動特徵（最終版 p.2 版型） =================
sl = new()
title(sl, 1, t(" 台灣消費者的行動特徵", "台湾消費者の行動特徴"))
runs(sl, 1.09, 0.99, 10.16, 0.91, [[
    (t("【yyyy】年赴日的【市場】旅客達【—】萬人，成長率約【—】％。",
       "【yyyy】年日本を訪れた【市場】人旅行者数は【—】万人に達し、成長率は約【—】％。"), False, INK)],
    [(t("平均每月超過【—】萬人造訪日本。", "平均毎月【—】万人以上が日本を訪れている。"), False, INK)]], 18)
runs(sl, 1.09, 2.05, 10.61, 3.11, [
    [(t("【台灣獨有的市場特徵與消費者心理】", "【台湾独自の市場特徴と消費者心理】"), False, INK)],
    [("・", True, INK),
     (t("部落客、論壇文化", "ブロガー、掲示板文化"), True, RED),
     (t("已深植消費者心理的台灣，消費者不會因單一廣告就衝動購買。",
        "が深く消費者心理に浸透している台湾では、消費者は単一の広告で衝動買いをしない。"), False, INK)],
    [(t("・不分線上線下，會徹底篩選", "・オンライン・オフラインを問わず、"), False, INK),
     (t("口碑與體驗談", "口コミや体験談"), True, RED),
     (t("，直到取得「確信」才會購買。", "を徹底的に取捨選択し、「確信」が得られた時点でようやく購入に至る。"), False, INK)],
    [(t("・旅行型態以個人旅行（FIT）為主流。許多旅客在出發前就已列好「該在日本買什麼」清單。勝負在訪日前就已決定。",
        "・旅行スタイルとしては個人旅行（FIT）が主流。事前に「日本で買うべきもの」リストを作成してから来日する旅行者も多い。勝負は訪日前に決まる。"), False, INK)],
    [(t("・【依專案補充：品類特有的資訊蒐集行為・決策關鍵】",
        "・【案件ごとに追記：カテゴリ特有の情報収集行動・意思決定の決め手】"), False, INK)]], 18, lnspc=1.35, space=10)
put(sl, 0.62, 6.94, 11.72, 0.30,
    [(t("資料來源：【日本政府觀光局（JNTO）「訪日外客數」／各市場官方統計 等】",
        "出典：【日本政府観光局（JNTO）「訪日外客数」／各市場公式統計 等】"), 8, False, MUTED)])
put(sl, 12.05, 7.09, 0.66, 0.15, [("1", 9, False, MUTED)], align=PP_ALIGN.RIGHT)

# ================= P2｜Pandora 台灣市場報告：聲量現況 =================
sl = new()
title(sl, 2, t(" Pandora 台灣市場報告", "Pandora 台湾市場レポート"))
lead(sl, t("「【品牌名／關鍵字A】」、「【品牌名／關鍵字B】」近 12 個月在台灣社群的聲量現況。以 Pandora 實測數據"
           "確認現有的口碑接點規模，作為本次施策的基準線。",
           "「【ブランド名／キーワードA】」、「【ブランド名／キーワードB】」の直近12か月の声量を見ると、"
           "口コミ接点の規模はまだ限られています。Pandoraの実測データで現状を可視化し、本施策の基準値とします。"),
     y=1.00, h=0.71)
for gi, (bx, bname, cc) in enumerate([(0.62, t("【品牌名】＋【關鍵字A】", "【ブランド名】＋【キーワードA】"), INK),
                                      (6.76, t("【品牌名】＋【關鍵字B】", "【ブランド名】＋【キーワードB】"), ACCENT)], 1):
    rect(sl, bx, 2.20, 5.95, 4.41, fill=WHITE, line=BORDER, rounded=True, adj=0.03)
    chip(sl, bx + 0.18, 2.33, 1.86, 0.27, bname, fill=cc, name=f"PD:g{gi}.label")
    put(sl, bx + 3.75, 2.37, 1.99, 0.20,
        [(t("近 12 個月聲量數據", "直近12か月 声量データ"), 8, False, MUTED)], align=PP_ALIGN.RIGHT)
    for j, (lb, mk) in enumerate(zip([t("總聲量", "総声量"), t("貼文數", "投稿数"),
                                      t("總按讚", "総いいね"), t("總留言", "総コメント")],
                                     ["totalVolume", "postCount", "likes", "comments"])):
        sx = bx + 0.18 + j * 1.42
        rect(sl, sx, 2.69, 1.33, 0.70, fill=WHITE, line=BORDER)
        put(sl, sx, 2.76, 1.33, 0.33, [("—", 17, True, INK)], align=PP_ALIGN.CENTER,
            name=f"PD:g{gi}.{mk}")
        put(sl, sx, 3.13, 1.33, 0.18, [(lb, 8, False, MUTED)], align=PP_ALIGN.CENTER)
    ph_img(sl, bx + 0.18, 3.49, 3.77, 1.86,
           t("貼上 Pandora「聲量趨勢分析」圖表", "Pandora「声量推移」グラフを貼り付け"),
           name=f"PD:g{gi}.chart.trend")
    ph_img(sl, bx + 4.07, 3.49, 1.59, 1.81,
           t("貼上「平台分布」圖表", "「プラットフォーム分布」を貼り付け"),
           name=f"PD:g{gi}.chart.platform")
    put(sl, bx + 0.18, 5.39, 3.77, 0.16, [(t("聲量趨勢（月次）", "声量推移（月次）"), 8, True, MUTED)], align=PP_ALIGN.CENTER)
    put(sl, bx + 4.07, 5.39, 1.59, 0.16, [(t("平台分布", "プラットフォーム分布"), 8, True, MUTED)], align=PP_ALIGN.CENTER)
    bullets(sl, bx + 0.18, 5.66, 5.59, 0.80, [
        t("【高峰月份與成因：哪一則貼文／哪一檔活動帶動聲量】", "【急増した月とその要因：どの投稿・どの施策が話題化したか】"),
        t("【平台占比：Threads —％、Instagram —％、其他 —％】", "【言及の内訳：Threads —％、Instagram —％、その他 —％】"),
        t("【近 12 個月貼文數僅 — 篇，口碑接點仍相當有限】", "【直近12か月の投稿数はわずか—件。口コミによる消費者接点はまだ限定的】")],
        name=f"PD:g{gi}.bullets")
footer(sl, SRC_PAN, 2)

# ================= P3｜Pandora：情緒・關鍵字・渠道 =================
sl = new()
title(sl, 2, t(" Pandora 台灣市場報告", "Pandora 台湾市場レポート"))
lead(sl, t("台灣消費者對「【品牌名】」的印象結構。情緒五級分布、關鍵字地圖與渠道分布，決定口碑文章「該說什麼」的切入點。",
           "台湾の生活者が「【ブランド名】」をどう捉えているか。感情5段階の分布、キーワードマップ、"
           "チャネル別分布から、口コミで「何を語るか」の切り口を決めます。"), y=1.00, h=0.55)
CW, GAP = 3.87, 0.24
cx = [0.62, 0.62 + CW + GAP, 0.62 + 2 * (CW + GAP)]
rect(sl, cx[0], 1.85, CW, 4.35, fill=CARD, line=BORDER, rounded=True, adj=0.03)
put(sl, cx[0] + 0.18, 2.02, CW - 0.36, 0.20, [(t("情緒分布（五級）", "感情分布（5段階）"), 10.5, True, INK)])
for j, (lb, bw) in enumerate([(t("非常正面", "非常に good"), 1.05), (t("正面", "good"), 1.90),
                              (t("中性", "中立"), 1.45), (t("負面", "bad"), 0.62),
                              (t("非常負面", "非常に bad"), 0.30)]):
    y = 2.38 + j * 0.36
    put(sl, cx[0] + 0.18, y, 0.90, 0.20, [(lb, 8, True, MUTED)])
    rect(sl, cx[0] + 1.02, y + 0.02, bw, 0.16, fill=BARGRY, line=None, name=f"PD:sent.bar{j+1}")
    put(sl, cx[0] + 3.02, y - 0.01, 0.67, 0.22, [("—％", 9.5, True, INK)], align=PP_ALIGN.RIGHT,
        name=f"PD:sent.pct{j+1}")
ph_img(sl, cx[0] + 0.18, 4.30, CW - 0.36, 1.32, t("貼上 Pandora「情緒分布」圓餅圖", "Pandora「感情分布」円グラフを貼り付け"), name="PD:chart.sentiment")
put(sl, cx[0] + 0.18, 5.72, CW - 0.36, 0.34,
    [(t("正面比率（非常正面＋正面）＝ —％／基準線", "ポジティブ比率（非常に good ＋ good）＝ —％／基準値"), 7.5, False, MUTED)],
    lnspc=1.2, name="PD:sent.positiveRate")

rect(sl, cx[1], 1.85, CW, 4.35, fill=CARD, line=BORDER, rounded=True, adj=0.03)
put(sl, cx[1] + 0.18, 2.02, CW - 0.36, 0.20, [(t("關鍵字分析（矩形圖）", "キーワード分析（ツリーマップ）"), 10.5, True, INK)])
ph_img(sl, cx[1] + 0.18, 2.38, CW - 0.36, 1.86,
       t("貼上 Pandora「關鍵字分析（矩形圖）」圖表", "Pandora「キーワード分析」を貼り付け"), name="PD:chart.keyword")
for j, (lb, col) in enumerate([(t("中性・資訊脈絡", "中立・情報文脈"), MUTED),
                               (t("正面脈絡", "ポジティブ文脈"), INK),
                               (t("負面脈絡", "ネガティブ文脈"), ACCENT)]):
    y = 4.36 + j * 0.60
    put(sl, cx[1] + 0.18, y, CW - 0.36, 0.18, [(lb, 8.5, True, col)])
    put(sl, cx[1] + 0.18, y + 0.20, CW - 0.36, 0.34,
        [(t("【該情緒下最常出現的關鍵字群】", "【当該文脈で頻出するキーワード群】"), 8, False, MUTED)], lnspc=1.2)

rect(sl, cx[2], 1.85, CW, 4.35, fill=CARD, line=BORDER, rounded=True, adj=0.03)
put(sl, cx[2] + 0.18, 2.02, CW - 0.36, 0.20, [(t("各渠道聲量分布", "チャネル別 声量分布"), 10.5, True, INK)])
for j, lb in enumerate(["Threads", "Instagram", "Dcard", "PTT", "Facebook"]):
    y = 2.38 + j * 0.32
    put(sl, cx[2] + 0.18, y, 1.30, 0.20, [(lb, 8.5, False, INK)], name=f"PD:chan.name{j+1}")
    put(sl, cx[2] + 2.85, y - 0.01, 0.84, 0.22, [("—％", 9.5, True, INK)], align=PP_ALIGN.RIGHT,
        name=f"PD:chan.pct{j+1}")
put(sl, cx[2] + 0.18, 4.12, CW - 0.36, 0.20, [(t("解讀觀點", "読み解きの視点"), 10.5, True, ACCENT)])
bullets(sl, cx[2] + 0.18, 4.42, CW - 0.36, 1.60, [
    t("聲量高峰與【新品／促銷／檔期／訪日旺季】的連動關係", "声量のピークが【新商品・販促・キャンペーン・訪日繁忙期】と、どう連動しているか"),
    t("品牌被談論的場域（論壇 vs 個人帳號），決定要增加的貼文類型", "語られている場（掲示板 vs 個人アカウント）を把握し、増やすべき投稿タイプを決める"),
    t("從高互動貼文萃取打中台灣消費者的「說法」", "反応の高い投稿から、台湾の生活者に刺さる「型」を抽出する")], sz=8, space=4)
footer(sl, [SRC_PAN[0], t("※ 情緒判定與關鍵字分群為 Pandora 之自動分析結果，僅供掌握結構之用。",
                          "※ 感情判定・キーワード分類はPandoraの自動分析結果です。構造把握を目的とした参考値です。")], 3)

# ================= P4｜企劃案概要（最終版 p.5 版型） =================
sl = new()
title(sl, 3, t(" 提案｜洞察・受眾・策略", "企画案概要"))
lead(sl, t("【以一句話說明本次施策的核心命題：因為○○，所以要在○○階段建立口碑接點，把認知一路接到【登錄／到店／購買】】。",
           "【一文で施策の主張を：○○だからこそ、○○の段階で口コミ接点をつくり、認知から【登録・来店・購入】までつなげます。】"),
     y=1.06, h=0.30)
cards = [(t("① 為何需要（洞察）", "① なぜ必要か"),
          t("【消費者行為上的關鍵卡點】", "【生活者行動における最大のボトルネック】"),
          t("→【從 Pandora 數據看到的事實，一句話收斂】", "→【Pandoraデータから見えた事実を一行で】")),
         (t("② 傳達給誰（受眾）", "② 誰に届けるか"),
          t("【主力客層：地區・年齡・行為特徵】", "【主力ターゲット：地域・年齢・行動特性】"),
          t("→【他們在哪裡蒐集資訊、用什麼標準做決定】", "→【どこで情報を集め、何を基準に判断する層か】")),
         (t("③ 如何驅動（策略）", "③ どう動かすか"),
          t("【主戰場平台＋從認知到行動的路徑】", "【主戦場のプラットフォーム＋認知から行動までの導線】"),
          t("→【旅前／旅中／旅後，各階段要做的事】", "→【旅マエ・旅ナカ・旅アトで、それぞれ何をするか】"))]
for j, (h1, h2, h3) in enumerate(cards):
    x = 0.62 + j * 4.09
    rect(sl, x, 1.72, 3.91, 2.48, fill=WHITE, line=BORDER, rounded=True, adj=0.04)
    put(sl, x + 0.26, 1.92, 3.40, 0.24, [(h1, 11, True, ACCENT)])
    put(sl, x + 0.26, 2.24, 3.40, 0.55, [(h2, 12, True, INK)], lnspc=1.3)
    put(sl, x + 0.26, 2.95, 3.42, 0.60, [(h3, 9, False, INK)], lnspc=1.35)
    put(sl, x + 0.26, 3.62, 3.42, 0.18, [(t("根據", "根拠"), 8, True, ACCENT)])
    put(sl, x + 0.26, 3.84, 3.42, 0.34,
        [(t("【引用哪一頁的 Pandora 數據／市場資料佐證】", "【どのページのPandoraデータ・市場データを根拠とするか】"), 8.5, False, MUTED)], lnspc=1.25)
metrics = [(t("投稿期間", "投稿期間"), t("【m/d – m/d】", "【m/d – m/d】"), t("全【—】週（【平台】投稿）", "全【—】週（【プラットフォーム】投稿）")),
           (t("集中期間", "集中期間"), t("全體約【—】成", "全体の約【—】割"), t("【m/d〜m/d、m/d〜m/d】重點配分", "【m/d〜m/d、m/d〜m/d】に重点配分")),
           (t("目標", "目標"), t("口碑接點擴大確認", "口コミ接点の拡大を確認"), t("（聲量＋【30】％保證）", "（声量＋【30】％保証）")),
           (t("想定【登錄／到店】數", "想定【登録・来店】者数"), t("【—〜—】人", "【—〜—】人"), t("口碑導流之【登錄／到店】試算", "口コミ経由の【登録・来店】者数（試算）"))]
for j, (a, b, c) in enumerate(metrics):
    x = 0.62 + j * 3.07
    rect(sl, x, 4.61, 2.87, 1.12, fill=CARD, line=BORDER, rounded=True, adj=0.06)
    put(sl, x + 0.18, 4.73, 2.51, 0.22, [(a, 10.5, True, ACCENT)])
    put(sl, x + 0.18, 4.99, 2.51, 0.28, [(b, 12, True, INK)])
    put(sl, x + 0.18, 5.33, 2.60, 0.32, [(c, 8, False, MUTED)], lnspc=1.2)
put(sl, 0.62, 5.99, 12.09, 0.40, [(t(
    "投稿期間為【yyyy 年 m 月 d 日（—）〜 m 月 d 日（—）】共【—】週。計【—〜—】則投稿，其中約【—】成集中投放於"
    "【訪日前／檔期前】資訊蒐集最活躍的【m/d〜m/d、m/d〜m/d】。",
    "投稿期間は【yyyy年m月d日（—）〜m月d日（—）】の全【—】週間。計【—〜—】投稿を想定し、そのうち約【—】割を、"
    "【訪日前・商戦期前】の情報収集が活発になる【m/d〜m/d、m/d〜m/d】に集中投下します。"), 9, False, INK)], lnspc=1.3)
footer(sl, [t("資料來源：【JNTO 訪日外客數／行政院人事行政總處行事曆／客戶提供之活動資訊 等】",
              "出典：【日本政府観光局（JNTO）「訪日外客数」／台湾行政院人事行政総処「政府行政機関カレンダー」／貴社ご提供資料 等】"),
            t("※ 目標值中僅「聲量＋30％」為保證值，其餘為施策設計上之參考值。",
              "※ 目標値のうち「声量＋30％」のみ保証値です。その他は施策設計上の参考値として設定しています。")], 4)

# ================= P5｜受眾設計 =================
sl = new()
title(sl, 3, t(" 提案｜受眾設計", "企画案概要｜ターゲット設計"))
lead(sl, t("針對上述策略，設計【4】個受眾層。素材共用，只更換切入點與訴求語言。",
           "上記の戦略に対し、【4】つのターゲット層を設計します。クリエイティブは共用し、切り口と訴求のみを変えます。"),
     y=1.04, h=0.24)
tas = [("TA 1", t("【核心客層】", "【コア層】"), t("【年齡・性別】", "【年齢・性別】"),
        t("【PTT／Threads／YouTube】", "【PTT／Threads／YouTube】"),
        t("【對品類本身有高度興趣，想比較規格與價格】", "【カテゴリ自体への関心が高く、スペック・価格を比較したい】")),
       ("TA 2", t("【日本旅遊愛好者】", "【日本旅行好き】"), t("【25–45 歲・訪日常客】", "【25–45歳・訪日リピーター】"),
        t("【Dcard 旅遊板／IG／Threads】", "【Dcard旅行板／Instagram／Threads】"),
        t("【想在行程中加入一項「體驗・購買」】", "【旅程に「体験・買い物」を一つ加えたい】")),
       ("TA 3", t("【收藏＆送禮族】", "【コレクション＆ギフト層】"), t("【25–45 歲・重視品質】", "【25–45歳・品質重視】"),
        t("【Instagram／Facebook】", "【Instagram／Facebook】"),
        t("【限定感與官方性，「只有這裡買得到」】", "【限定感と公式性。「ここでしか買えない」】")),
       ("TA 4", t("【輕度・家庭客層】", "【ライト・ファミリー層】"), t("【30–50 歲】", "【30–50歳】"),
        t("【Facebook 社團／新聞】", "【Facebookグループ／ニュース】"),
        t("【不熟悉也能輕鬆享受的體驗】", "【詳しくなくても楽しめる体験】"))]
for j, (tag, name, demo, place, motive) in enumerate(tas):
    x = 0.62 + j * 3.07
    rect(sl, x, 1.72, 2.87, 3.62, fill=WHITE, line=BORDER, rounded=True, adj=0.04)
    chip(sl, x + 0.18, 1.90, 0.62, 0.24, tag, fill=INK, sz=8)
    put(sl, x + 0.18, 2.28, 2.51, 0.28, [(name, 12, True, INK)])
    put(sl, x + 0.18, 2.64, 2.51, 0.20, [(demo, 9, False, MUTED)])
    put(sl, x + 0.18, 3.02, 2.51, 0.18, [(t("主要場域", "主な接触チャネル"), 8, True, ACCENT)])
    put(sl, x + 0.18, 3.24, 2.51, 0.42, [(place, 8.5, False, INK)], lnspc=1.25)
    put(sl, x + 0.18, 3.80, 2.51, 0.18, [(t("購買動機", "購買動機"), 8, True, ACCENT)])
    put(sl, x + 0.18, 4.02, 2.51, 0.60, [(motive, 8.5, False, INK)], lnspc=1.25)
    put(sl, x + 0.18, 4.76, 2.51, 0.18, [(t("對應切角", "対応する切り口"), 8, True, ACCENT)])
    put(sl, x + 0.18, 4.98, 2.51, 0.30, [(t("【切角①〜⑤中對應的編號】", "【切り口①〜⑤のうち該当する番号】"), 8.5, False, INK)], lnspc=1.25)
rect(sl, 0.62, 5.58, 12.09, 0.72, fill=CARD, line=BORDER, rounded=True, adj=0.12)
put(sl, 0.84, 5.72, 11.65, 0.20, [(t("受眾共通的行為前提", "ターゲットに共通する行動前提"), 10.5, True, ACCENT)])
put(sl, 0.84, 5.96, 11.65, 0.22, [(t(
    "【台灣消費者不會因單一廣告衝動購買；會在論壇・SNS 反覆比對口碑與體驗談，取得「確信」後才行動。因此勝負在【訪日前／檔期前】就已決定。】",
    "【台湾の生活者は単一の広告で衝動買いをせず、掲示板・SNSで口コミと体験談を徹底的に比較し、「確信」を得てから行動する。"
    "だからこそ勝負は【訪日前・商戦期前】に決まる。】"), 9, False, INK)])
footer(sl, [t("資料來源：Pandora by The Pocket Company／Accucrazy 聲量報告、【JNTO 訪日外客數 等】",
              "出典：Pandora by The Pocket Company／Accucrazy 声量レポート、【日本政府観光局（JNTO）「訪日外客数」 等】")], 5)

# ================= P6｜實施時程（最終版 p.6 版型） =================
sl = new()
title(sl, 4, t(" 實施時程", "実施スケジュール"))
lead(sl, t("投稿整體約【—】成重點配分於兩個連假前，在【訪日前】資訊蒐集最活躍的時機，有效促進活動認知與事前登錄。"
           "連假前為「促進登錄的口碑」，連假中切換為「實際使用的口碑」，以一連串的投稿設計串起資訊蒐集到店頭利用。",
           "投稿全体の約【—】割を2つの連休前に重点配分し、訪日前の情報収集が活発になるタイミングで、キャンペーン認知と事前登録を"
           "効率的に促進します。連休前は「登録を促す口コミ」、連休中は「実際に使った口コミ」へと役割を切り替え、"
           "情報収集から店頭利用までを一連の投稿設計でつなげます。"), y=0.98, h=0.71)
rect(sl, 0.62, 1.93, 12.09, 0.34, fill=CARD, line=BORDER)
put(sl, 0.84, 2.02, 11.65, 0.18, [(t(
    "活動期間　【yyyy/m/d（—）〜 m/d（—）】　｜　投稿期間　【m/d（—）〜 m/d（—）】　全【—】週・合計【—】則投稿",
    "キャンペーン期間　【yyyy/m/d（—）〜m/d（—）】　｜　投稿期間　【m/d（—）〜m/d（—）】　全【—】週・合計【—】投稿"), 10.5, True, INK)])
# 週刻度
line(sl, 0.62, 3.00, 12.71, 3.00, BORDER, 0.75)
ticks = [0.62, 1.63, 2.64, 3.64, 5.16, 6.16, 7.50, 8.68, 9.69, 10.70, 11.70]
for j, tx in enumerate(ticks):
    line(sl, tx, 2.92, tx, 3.00, MUTED, 0.75)
    lx = tx if j == 0 else tx - 0.31
    lab = t("第1週 m/d", "第1週 m/d") if j == 0 else "m/d"
    put(sl, lx, 2.71, 0.61, 0.17, [(lab, 7, True, INK)], align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
put(sl, 11.94, 2.71, 0.77, 0.17, [(t("m/d 結束", "m/d 終了"), 7, True, MUTED)])
# 連假底色與 chip
for hx in (4.23, 6.88):
    rect(sl, hx, 3.06, 0.92, 1.54, fill=HOLIBG, line=None)
    chip(sl, hx + 0.01, 3.10, 0.90, 0.22, t("【連假】", "【連休】"), fill=ORANGE, sz=7, adj=0.2)
# 投稿量長條
for bx, by, bw, bh, bc in [(0.64, 3.24, 3.57, 1.36, ORANGE), (4.25, 3.44, 0.88, 1.16, BLUEBR),
                           (5.17, 3.15, 1.69, 1.45, ORANGE), (6.90, 3.44, 0.88, 1.16, BLUEBR),
                           (7.82, 3.79, 1.84, 0.81, BLUEMD), (9.70, 4.29, 2.99, 0.31, BARGRY)]:
    rect(sl, bx, by, bw, bh, fill=bc, line=None, rounded=True, adj=0.06)
line(sl, 0.62, 4.60, 12.71, 4.60, AXIS, 1.0)
# 三條資訊帶
for by in (4.49, 4.92, 5.35):
    rect(sl, 0.63, by, 12.09, 0.34, fill=CARD, line=BORDER)
put(sl, 0.64, 4.55, 1.20, 0.20, [(t("投稿期間：", "投稿期間："), 10.5, False, DARKI)])
put(sl, 0.64, 4.99, 1.32, 0.18, [(t("投稿角色：", "投稿役割："), 10.5, False, DARKI)])
put(sl, 0.64, 5.42, 1.26, 0.18, [(t("主要目的：", "主な目的："), 10.5, False, DARKI)])
cols = [(0.62, 3.61, t("重點投放", "重点投下"), ORTXT, t("促進登錄", "登録促進"),
         [t("登錄方式・對象門市・條件理解", "登録方法・対象店舗・条件理解")]),
        (4.23, 0.92, t("連假中", "連休中"), BLUETX, t("實體驗", "実体験"),
         [t("現地消費", "現地決済"), t("購物體驗", "買い物体験")]),
        (5.15, 1.73, t("重點投放", "重点投下"), ORTXT, t("再訴求", "再訴求"),
         [t("第2波連假前", "第2波の連休前に"), t("再訴求登錄", "登録を再訴求")]),
        (6.88, 0.92, t("連假中", "連休中"), BLUETX, t("店頭想起", "店頭想起"),
         [t("喚起店頭使用", "店頭利用の想起")]),
        (7.80, 1.88, t("持續投放", "継続投下"), BLUETM, t("信賴形成", "信頼形成"),
         [t("成果實證・信賴形成", "還元実証・信頼形成")]),
        (9.68, 3.03, t("終盤投放", "終盤投下"), BLUETM, t("推一把", "利用後押し"),
         [t("季節需求・結束前提醒", "季節需要・終了前リマインド")])]
for x, w, role, rc, aim, desc in cols:
    dw = max(w, 1.30); dx = x + w / 2 - dw / 2
    put(sl, dx, 4.58, dw, 0.18, [("【m/d–m/d】", 10.5, False, INK)], align=PP_ALIGN.CENTER)
    put(sl, dx, 5.01, dw, 0.18, [(role, 10.5, False, rc)], align=PP_ALIGN.CENTER)
    put(sl, dx, 5.43, dw, 0.18, [(aim, 10.5, False, DARKI)], align=PP_ALIGN.CENTER)
    put(sl, x, 5.87, w, 0.34, [(ln, 9, False, MUTED2) for ln in desc], align=PP_ALIGN.CENTER, lnspc=1.15)
put(sl, 0.65, 6.35, 11.48, 0.18, [(t("※ 投稿角色僅表示各時期的主要目的。具體則數配分將依開始後的反應調整。",
                                     "※ 投稿役割は時期ごとの主な目的を示すものです。具体的な本数配分は、開始後の反応を見ながら調整します。"), 8, False, MUTED2)])
footer(sl, [t("資料來源：【行政院人事行政總處「政府行政機關行事曆」（連假期間）】",
              "出典：【台湾行政院人事行政総処「政府行政機関カレンダー」（連休期間）】"),
            t("【日本政府觀光局（JNTO）「訪日外客數」／【市場】於【月份】為當月歷史新高】",
              "【日本政府観光局（JNTO）「訪日外客数」／【市場】は【該当月】として過去最高を記録】")], 6)

# ================= P7｜口碑切角：切角總覽 =================
sl = new()
title(sl, 5, t(" 口碑切角設計", "コンテンツ設計"))
lead(sl, t("配合【旅前・旅中・旅後】各階段，以【5】種投稿切角設計口碑內容。",
           "旅マエ・旅ナカ・旅アトの各段階に合わせ、【5】つの投稿タイプで口コミ内容を設計します。"), y=1.04, h=0.24)
angles = [("①", t("【旅前・攻略系】", "【旅マエ攻略系】"), t("【理解・收藏】", "【登録理解・保存】"),
           [t("【登錄／購買手順】", "【事前登録・購入手順】"), t("【對象門市／期間／上限】", "【対象店舗／期間／上限】"),
            t("【出發前檢查清單】", "【出発前チェック】"), t("【納入旅行計畫】", "【旅行計画への組み込み】")]),
          ("②", t("【旅前・優惠情報系】", "【旅マエお得情報系】"), t("【認知喚起・擴散】", "【認知喚起・拡散】"),
           [t("【核心優惠的認知】", "【還元内容の認知】"), t("【有無登錄的差別】", "【登録有無による差】"),
            t("【不知道就虧了的重點】", "【知らないと損するポイント】"), t("【容易分享給朋友的小知識】", "【友人に共有しやすい豆知識】")]),
          ("③", t("【旅中・實體驗系】", "【旅ナカ決済実体験系】"), t("【現地使用・想起】", "【現地利用・決済想起】"),
           [t("【購買品／收據】", "【購入品／レシート】"), t("【店頭使用場景】", "【店頭での決済シーン】"),
            t("【指定通路的體驗】", "【対象加盟店での利用体験】"), t("【旅行中的即時投稿】", "【旅行中のリアルタイム投稿】")]),
          ("④", t("【旅中・省錢檢證系】", "【旅ナカ節約検証系】"), t("【理解・比較檢討】", "【節約理解・比較検討】"),
           [t("【免稅＋回饋的實際計算】", "【免税＋還元の実計算】"), t("【多門市的搭配使用】", "【複数店舗での使い分け】"),
            t("【購物計畫最佳化】", "【買い物計画の最適化】"), t("【上限運用的具體例】", "【上限活用の具体例】")]),
          ("⑤", t("【旅後・成果實證系】", "【旅アト還元実証系】"), t("【確認・信賴形成】", "【還元確認・信頼形成】"),
           [t("【回饋入帳確認】", "【キャッシュバック入金確認】"), t("【使用後評價】", "【利用後レビュー】"),
            t("【給下一位旅客的建議】", "【次回旅行者へのアドバイス】"), t("【回饋時程的分享】", "【還元タイミングの共有】")])]
for j, (num, name, goal, items) in enumerate(angles):
    x = 0.62 + j * 2.4475
    rect(sl, x, 1.71, 2.30, 3.54, fill=WHITE, line=BORDER, rounded=True, adj=0.05)
    chip(sl, x + 0.16, 1.85, 0.26, 0.26, num, fill=INK, sz=9, adj=0.18)
    put(sl, x + 0.50, 1.87, 1.72, 0.24, [(name, 10, True, INK)])
    put(sl, x + 0.16, 2.19, 1.98, 0.18, [(goal, 8, True, ACCENT)])
    put(sl, x + 0.16, 2.53, 1.98, 0.18, [(t("內容構成", "内容構成"), 9, True, INK)])
    bullets(sl, x + 0.16, 2.86, 2.00, 1.70, items, sz=8, space=3)
    rect(sl, x + 0.16, 4.77, 1.98, 0.44, fill=CARD, line=BORDER, rounded=True, adj=0.14)
    put(sl, x + 0.16, 4.92, 1.98, 0.18, [(t("投稿預定：【m/d–m/d】", "投稿予定：【m/d–m/d】"), 8, True, INK)], align=PP_ALIGN.CENTER)
put(sl, 0.62, 5.45, 1.90, 0.34, [(t("投稿時機", "投稿タイミング"), 8, True, MUTED),
                                 (t("（與時程頁連動）", "（実施スケジュールに連動）"), 7.5, False, MUTED)])
segs = [("【m/d–m/d】", 3.55, ORANGE), (t("【連假】", "【連休】"), 1.00, BLUEBR), ("【m/d–m/d】", 2.00, ORANGE),
        (t("【連假】", "【連休】"), 1.00, BLUEBR), ("【m/d–m/d】", 1.60, BLUEMD), ("【m/d–m/d】", 1.05, BARGRY)]
xx = 2.60
for lb, w, col in segs:
    rect(sl, xx, 5.45, w, 0.30, fill=col, line=None, rounded=True, adj=0.4)
    put(sl, xx, 5.51, w, 0.18, [(lb, 7.5, True, INK if col is BARGRY else WHITE)], align=PP_ALIGN.CENTER)
    xx += w + 0.06
put(sl, 0.62, 5.90, 1.90, 0.20, [(t("內容構成", "コンテンツ構成"), 8, True, MUTED)])
xx = 2.60
for lb, w, _ in segs:
    rect(sl, xx, 5.86, w, 0.30, fill=WHITE, line=BORDER, rounded=True, adj=0.4)
    put(sl, xx, 5.92, w, 0.18, [(t("【切角編號】", "【切り口番号】"), 7.5, False, INK)], align=PP_ALIGN.CENTER)
    xx += w + 0.06
put(sl, 0.62, 6.30, 12.09, 0.22, [(t(
    "【一句話收斂：旅前建立理解，旅中可視化使用場景與省錢效果，旅後把成果轉為信賴材料。】",
    "【一行で：旅マエで理解をつくり、旅ナカで利用シーンと節約効果を可視化し、旅アトで実績を信頼材料に転換します。】"), 10, True, INK)])
footer(sl, [t("資料來源：【活動利用規約／客戶提供資訊】、Accucrazy「【參考案例名】」企劃資料（切角設計原型）",
              "出典：【キャンペーン利用規約／貴社ご提供資料】、Accucrazy「【参考案件名】」企画資料（切り口設計の原型）"),
            t("※ 投稿角色僅表示各時期的主要目的，實際則數配分將依開始後的反應調整。",
              "※ 投稿役割は時期ごとの主な目的を示すものです。具体的な本数配分は、開始後の反応を見ながら調整します。")], 7)

# ================= P8｜口碑切角：單一切角範例 =================
sl = new()
title(sl, 5, t(" 口碑切角設計", "投稿サンプル"))
put(sl, 0.64, 0.93, 8.60, 0.34, [(t("【切角①・旅前攻略系】｜【一句話說明這個切角要讓讀者理解什麼】",
                                    "【切り口①・旅マエ攻略系】｜【この切り口で何を伝えるかを一行で】"), 14, True, INK)])
put(sl, 0.52, 1.51, 3.60, 0.22, [(t("實際的【平台】貼文示意", "実際の【プラットフォーム】投稿イメージ"), 10.5, True, ACCENT)])
rect(sl, 0.39, 1.78, 4.13, 4.35, fill=POSTBG, line=None, rounded=True, adj=0.04)
av = sl.shapes.add_shape(MSO_SHAPE.OVAL, I(0.84), I(2.20), I(0.34), I(0.34))
av.fill.solid(); av.fill.fore_color.rgb = RGBColor(0x3A, 0x4A, 0x42); av.line.fill.background(); av.shadow.inherit = False
put(sl, 1.25, 2.24, 1.60, 0.18, [(t("【帳號名稱】", "【アカウント名】"), 9, True, WHITE)])
put(sl, 2.95, 2.24, 1.20, 0.18, [(t("【— 小時】", "【—時間】"), 8, False, RGBColor(0x9A, 0x9A, 0x9A))], align=PP_ALIGN.RIGHT)
post_zh = ["【第一句：情境鋪陳，例如最近在排行程】", "【第二句：發現了什麼優惠／商品】", "【第三句：具體條件——通路、比例、期間】", "",
           "【第四句：關鍵限制，例如要先登錄才算】", "【第五句：真實感的個人反應】", "",
           "【第六句：為什麼這兩家本來就會逛】", "【最後一句：拋問句引導留言】"]
post_ja = ["【1行目：シチュエーション。例）旅行の計画を立てていて】", "【2行目：何を見つけたか（キャンペーン・商品）】",
           "【3行目：具体条件——対象店舗・還元率・期間】", "",
           "【4行目：重要な制約。例）事前登録が必要】", "【5行目：リアルな個人の反応】", "",
           "【6行目：もともとよく行く店である理由】", "【最終行：問いかけでコメントを促す】"]
put(sl, 1.25, 2.63, 2.92, 2.82, [(s, 9, False, WHITE) for s in (post_zh if LANG == 'zh' else post_ja)], lnspc=1.3)
put(sl, 1.22, 5.58, 2.90, 0.22, [("♡  【—】        ◯  【—】        ↻        ➤", 10, False, RGBColor(0xCC, 0xCC, 0xCC))])
rect(sl, 4.87, 1.78, 3.82, 4.35, fill=CARD, line=BORDER, rounded=True, adj=0.04)
chip(sl, 5.10, 2.20, 1.42, 0.28, t("【譯文・摘要】", "【日本語訳（要約）】"), fill=INK, sz=8.5, adj=0.2)
tr_zh = ["【段落一：把貼文的情境與發現，改寫成給客戶端閱讀的摘要。】", "【段落二：具體條件——對象通路、回饋比例、期間。】",
         "【段落三：關鍵限制與提醒——事前登錄、上限、先到先得。】", "【段落四：收斂到行動——出發前先完成登錄。】"]
tr_ja = ["【第1段落：投稿のシチュエーションと発見を、要約して記載。】", "【第2段落：具体条件——対象加盟店・還元率・期間。】",
         "【第3段落：重要な制約——事前登録、上限、先着。】", "【第4段落：行動に収斂——出発前に登録しておく。】"]
put(sl, 5.12, 2.61, 3.32, 1.90, [(s, 8.5, False, INK) for s in (tr_zh if LANG == 'zh' else tr_ja)], space=5, lnspc=1.35)
put(sl, 5.12, 4.74, 3.20, 0.18, [(t("1 則貼文傳達的主要資訊", "1投稿で伝える主なキャンペーン情報"), 9, True, INK)])
for j in range(6):
    y = 4.98 + j * 0.17
    put(sl, 5.12, y, 0.18, 0.14, [("✓", 8, True, ACCENT)])
    put(sl, 5.35, y, 3.05, 0.14, [(t(f"【要傳達的資訊 {j+1}】", f"【伝えるべき情報 {j+1}】"), 8, False, INK)])
rect(sl, 8.82, 1.78, 4.05, 1.93, fill=WHITE, line=BORDER, rounded=True, adj=0.06)
put(sl, 8.96, 1.94, 3.77, 0.18, [(t("留言區的溝通設計", "コメント欄でのコミュニケーション設計"), 10, True, ACCENT)])
qa = [(t("「【共感・參加回報型留言】」", "「【共感・参加報告型のコメント】」"),
       t("【以共感留言為起點，擴大貼文的互動。】", "【共感・参加報告のコメントを起点に、投稿への反応を広げる。】")),
      (t("「【提問型留言】」", "「【質問型のコメント】」"),
       t("【針對操作方式的提問，導引至【官方頁面】。】", "【登録方法に関する質問には、【公式ページ】を案内する。】")),
      (t("「【惋惜型留言】」", "「【惜しかった型のコメント】」"),
       t("【從「不知道」「下次要用」的反應，接到下一次需求。】", "【「知らなかった」「次回は使いたい」という反応から、次の需要につなげる。】"))]
for j, (q, a) in enumerate(qa):
    y = 2.25 + j * 0.42
    put(sl, 9.02, y, 3.65, 0.17, [(q, 8.5, True, INK)])
    put(sl, 9.02, y + 0.20, 3.65, 0.20, [(a, 8, False, MUTED)])
rect(sl, 8.82, 3.88, 4.05, 1.05, fill=WHITE, line=BORDER, rounded=True, adj=0.10)
put(sl, 8.96, 3.98, 3.77, 0.18, [(t("貼文圖片的方向性", "投稿画像の方向性"), 10, True, ACCENT)])
bullets(sl, 9.02, 4.26, 3.65, 0.56, [
    t("【店頭・收據・購買商品等，能傳達真實體驗的照片】", "【店頭・レシート・購入商品など、実際の体験が伝わる写真を使用】"),
    t("【避免過度演出與修圖，維持自然的口碑感】", "【過度な演出や加工を避け、自然な口コミ投稿として見せる】")], sz=8, space=3)
rect(sl, 8.82, 5.07, 4.05, 1.06, fill=WHITE, line=BORDER, rounded=True, adj=0.10)
put(sl, 8.96, 5.17, 3.77, 0.18, [(t("效果指標", "効果指標"), 10, True, ACCENT)])
bullets(sl, 9.02, 5.45, 3.65, 0.56, [
    t("【收藏數／留言數／曝光次數／與操作方式相關的提問】", "【保存数／コメント数／投稿表示回数／登録方法に関する質問・反応を確認】"),
    t("【分析反應好的切角，最佳化後續投稿內容與配分】", "【反応の高い切り口を分析し、以降の投稿内容・本数配分を最適化】")], sz=8, space=3)
footer(sl, [t("資料來源：【活動利用規約（對象通路・期間・事前登錄・回饋上限）】、Accucrazy「【參考案例名】」企劃資料",
              "出典：【キャンペーン利用規約（対象加盟店・期間・事前登録・還元上限）】、Accucrazy「【参考案件名】」企画資料")], 8,
       note=t("※ 投稿依生活者本人的實際體驗撰寫，並適當標示廣告・PR，依貴司及各平台規範運營。",
              "※ 投稿は生活者本人の実体験に基づいて作成し、広告・PR表記を適切に行ったうえで、貴社および各プラットフォームの規定に沿って運用します。"))

# ================= P9｜KPI 設計・目標值 =================
sl = new()
title(sl, 6, t(" KPI 設計・目標值", "効果指標・目標値"))
lead(sl, t("以【平台】上的口碑接點為起點，目標為從活動認知帶動【事前登錄／到店使用】的行動喚起。"
           "效果檢證分兩段確認：顯示口碑接點擴大的「聲量・曝光」，以及最終行動的「【登錄／到店】數」。",
           "【プラットフォーム】上の口コミ接点を起点に、キャンペーン認知から【事前登録・店頭利用】への行動喚起を目指します。"
           "効果検証では、口コミ接点の拡大を示す「声量・表示回数」と、最終行動となる「【登録・来店】者数」を段階的に確認します。"),
     y=1.09, h=0.55)
rect(sl, 0.62, 2.22, 12.09, 2.65, fill=CARD, line=BORDER, rounded=True, adj=0.03)
put(sl, 0.84, 2.43, 7.66, 0.18, [(t("① 口碑接點：聲量【30】％ UP（保證）", "① 口コミ接点：声量【30】％UP（保証）"), 10.5, True, INK)])
for gi, (bname, y0) in enumerate([(t("【品牌 × 關鍵字A】", "【ブランド × キーワードA】"), 2.74),
                                  (t("【品牌 × 關鍵字B】", "【ブランド × キーワードB】"), 3.67)], 1):
    chip(sl, 0.84, y0, 1.64, 0.26, bname, fill=INK, sz=8.5, name=f"PD:kpi.g{gi}.label")
    put(sl, 0.84, y0 + 0.33, 0.66, 0.22, [(t("施策前", "施策前"), 8, True, MUTED)])
    rect(sl, 1.55, y0 + 0.33, 2.84, 0.22, fill=BARGRY, line=None, name=f"PD:kpi.g{gi}.barBefore")
    put(sl, 4.49, y0 + 0.31, 2.19, 0.26, [(t("【—】件", "【—】件"), 11, True, INK)], name=f"PD:kpi.g{gi}.before")
    put(sl, 0.84, y0 + 0.62, 0.66, 0.22, [(t("施策後", "施策後"), 8, True, MUTED)])
    rect(sl, 1.55, y0 + 0.62, 3.70, 0.22, fill=ACCENT, line=None, name=f"PD:kpi.g{gi}.barAfter")
    put(sl, 5.35, y0 + 0.63, 2.40, 0.22, [(t("【—】件（＋【30】％）", "【—】件（＋【30】％）"), 11, True, ACCENT)],
        name=f"PD:kpi.g{gi}.after")
put(sl, 0.84, 4.59, 7.66, 0.20, [(t("※ 施策前數值為【yyyy/m/d】時點之資料。實施時以施策開始前一日的最新數據作為基準值。",
                                    "※ 施策前の数値は【yyyy/m/d】時点のデータです。実施時は、施策開始前日までの最新データを基準値とします。"), 7.5, False, MUTED)])
rect(sl, 8.75, 2.42, 3.74, 2.25, fill=WHITE, line=BORDER, rounded=True, adj=0.05)
put(sl, 8.75, 2.68, 3.74, 1.01, [("＋30％", 54, True, ACCENT)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, name="PD:kpi.uplift")
put(sl, 8.75, 3.78, 3.74, 0.26, [(t("口碑接點的擴大確認", "口コミ接点の拡大を確認"), 12, True, INK)], align=PP_ALIGN.CENTER)
put(sl, 8.75, 4.10, 3.74, 0.42, [(t("【關鍵字A】　【—】件 → 【—】件（＋【—】件）", "【キーワードA】　【—】件 → 【—】件（＋【—】件）"), 8.5, False, MUTED),
                                 (t("【關鍵字B】　【—】件 → 【—】件（＋【—】件）", "【キーワードB】　【—】件 → 【—】件（＋【—】件）"), 8.5, False, MUTED)],
    align=PP_ALIGN.CENTER, lnspc=1.25, name="PD:kpi.detail")
for j, (h1, big, sub) in enumerate([
        (t("② 資訊接觸", "② 情報接触"), t("【—】 〜 【—】 次", "【—】 〜 【—】 回"),
         t("投稿曝光次數之想定（每則【—〜—】次 × 【—】則投稿）", "投稿表示回数の想定（1投稿あたり【—〜—】回 × 【—】投稿）")),
        (t("③ 想定【登錄／到店】數（參考值）", "③ 想定【登録・来店】者数（参考値）"), t("【—】 〜 【—】 人", "【—】 〜 【—】 人"),
         t("依貴司計測數據檢證成效", "貴社計測データに基づき効果を検証"))]):
    x = 0.62 + j * 6.14
    rect(sl, x, 5.03, 5.95, 1.20, fill=CARD, line=BORDER, rounded=True, adj=0.10)
    put(sl, x + 0.22, 5.19, 5.51, 0.18, [(h1, 10.5, True, ACCENT)])
    mk = ["impressions", "registrations"][j]
    put(sl, x + 0.22, 5.46, 5.51, 0.40, [(big, 22, True, INK)], name=f"PD:kpi.{mk}")
    put(sl, x + 0.22, 5.97, 5.51, 0.18, [(sub, 8, False, MUTED)], name=f"PD:kpi.{mk}Note")
footer(sl, [SRC_PAN[0], t("※ 僅「聲量＋30％」為保證值。曝光次數・【登錄／到店】數為施策設計上之參考值，將依實施後的反應與實績最佳化投稿內容與配分。",
                          "※ 声量＋30％は保証値です。表示回数・【登録・来店】者数は施策設計上の参考値として設定し、実施後の反応・実績を踏まえて投稿内容・配分を最適化します。")], 9)

# ---------- 封底移到最後 ----------
lst = prs.slides._sldIdLst
lst.remove(back_id); lst.append(back_id)

# ---------- 自動為所有文字圖形編錨點 T:p{頁}.{序} ----------
def _autoname(presentation):
    for pi, slide in enumerate(presentation.slides, 1):
        k = 0
        for shp in slide.shapes:
            if not shp.has_text_frame or not shp.text_frame.text.strip():
                continue
            if shp.name.startswith("PD:"):
                continue
            k += 1
            shp.name = f"T:p{pi}.{k}"

_autoname(prs)
out = OUT_DIR / ("template_zh.pptx" if LANG == 'zh' else "template_ja.pptx")
prs.save(str(out))
print("saved", out)
