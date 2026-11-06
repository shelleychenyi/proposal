# -*- coding: utf-8 -*-
"""長岡花火｜台灣市場 Inbound 集客策略提案（繁中版）
base：Hakuba 中文版（Intasect 母片），沿用封面與 THANK YOU，其餘頁面重新繪製。
結構參考：PASONA（台灣市場→施策→聲量分析）＋四國MaaS（現況→概念→施策→KPI→時程）
圖片：Banaverse（Nano Banana Pro）生成，皆標「AI示意」。
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HAK = os.path.join(os.path.dirname(ROOT), "白馬谷Hakuba Valley")
BASE = os.path.join(HAK, "【中文版】Hakuba Valley 繁體中文市場集客策略提案202610.pptx")
OUT = os.path.join(ROOT, "【繁中版】長岡花火 台灣市場Inbound集客策略提案202611.pptx")
d = Deck(BASE)
n_orig = len(d.prs.slides)
d.keep_only({0, n_orig - 1})
cover, thanks = d.prs.slides[0], d.prs.slides[1]

# 長岡花火 palette（官網：可可棕 #623632・桃紅 #EA336A；主視覺：夜空藏青 × 鳳凰金）
NIGHT, GOLD_T, GOLD_L, PINK, BROWN, CREAM = "0E1630", "B07D1E", "E8B84A", "EA336A", "623632", "F7F3EE"
NIGHT2 = "1B2547"
SRC_V = "資料來源：Pandora by The Pocket Company／Accucrazy「長岡花火大會」言及量レポート（2025/10/27〜2026/10/26・台灣＋香港）"
SRC_I = "資料來源：Pandora「長岡花火大會」インサイトレポート（2025/10/27〜2026/10/26）"
IMG = lambda n: os.path.join(HERE, "img", n)
PNG = lambda n: os.path.join(HERE, "png", n)
E = 914400


def full_bg(s, path, crop_y=0.5, dark=0.0):
    """整頁滿版圖（cover）＋可選的暗化遮罩"""
    d.pic(s, path, 0, 0, 13.333, 7.5, mode="cover")
    if dark:
        sh = d.rect(s, 0, 0, 13.333, 7.5, "000000")
        _alpha(sh, dark)


def _alpha(sh, a):
    from lxml import etree
    sf = sh.fill._xPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill")
    clr = sf[0]
    el = etree.SubElement(clr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
    el.set("val", str(int(a * 100000)))


def grad_rect(s, x, y, w, h, color, a_from, a_to, angle=0):
    """左→右（angle=0）或上→下（angle=90）透明漸層矩形"""
    from lxml import etree
    sh = d.rect(s, x, y, w, h, color)
    spPr = sh.fill._xPr
    A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    for c in list(spPr):
        if c.tag in (f"{{{A}}}solidFill",):
            spPr.remove(c)
    xml = f'''<a:gradFill xmlns:a="{A}" rotWithShape="1"><a:gsLst>
<a:gs pos="0"><a:srgbClr val="{color}"><a:alpha val="{int(a_from*100000)}"/></a:srgbClr></a:gs>
<a:gs pos="100000"><a:srgbClr val="{color}"><a:alpha val="{int(a_to*100000)}"/></a:srgbClr></a:gs>
</a:gsLst><a:lin ang="{angle*60000}" scaled="0"/></a:gradFill>'''
    g = etree.fromstring(xml)
    prst = spPr.find(f"{{{A}}}prstGeom")
    prst.addnext(g)
    return sh


def blank():
    s = d.prs.slides.add_slide(d.prs.slide_layouts[6])
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    d.page += 1
    return s


def pageno(s, color="FFFFFF"):
    d.tx(s, 12.30, 7.10, 0.70, 0.25, str(d.page), 9, color, align="r", font="Meiryo")


def section(no, title, sub, img, pos="l"):
    s = blank()
    full_bg(s, img)
    grad_rect(s, 0, 0, 13.333, 7.5, NIGHT, 0.92, 0.15)
    d.tx(s, 0.8, 1.6, 3, 1.4, no, 88, GOLD_L, True, font="Georgia")
    d.hline(s, 0.85, 3.15, 2.6, 3.15, GOLD_L, 2)
    d.tx(s, 0.8, 3.35, 7.5, 0.9, title, 36, WHITE, True)
    d.tx(s, 0.82, 4.3, 6.8, 1.0, sub, 13, "D9DEEA")
    pageno(s)
    return s


def ai(s, x, y, text="AI示意"):
    return d.label(s, x, y, 0.62, 0.2, text, "333333", size=7, bold=False, radius=0.15)


def photo(s, path, x, y, w, h, tag=True, crop=None, mode="cover"):
    p = d.pic(s, path, x, y, w, h, mode=mode, crop=crop)
    if tag:
        ai(s, x + 0.08, y + 0.08)
    return p


def stat(s, x, y, w, h, val, lab, color=PINK, bg=SOFT, vs=22):
    d.rrect(s, x, y, w, h, bg, None, radius=0.06)
    d.tx(s, x, y + 0.08, w, h * 0.55, val, vs, color, True, align="c", anchor="m", font="Meiryo")
    d.tx(s, x + 0.05, y + h * 0.58, w - 0.1, h * 0.4, lab, 8.5, INK, align="c")


def bullets(s, x, y, w, items, size=9.5, gap=0.42, num_color=PINK, title_color=INK, h=0.4):
    """雄獅式「畫面重點」：圓形編號＋粗體標題＋說明"""
    for i, it in enumerate(items):
        t, b = it if isinstance(it, tuple) else (it, "")
        yy = y + i * gap
        d.circle(s, x, yy + 0.02, 0.3, str(i + 1), num_color, 9)
        d.tx(s, x + 0.4, yy - 0.02, w - 0.4, 0.26, t, size + 0.5, title_color, True)
        if b:
            d.tx(s, x + 0.4, yy + 0.24, w - 0.4, h, b, size - 1.5, GREY, line=1.1)


def bottom_bar(s, text, color=NIGHT, y=6.38):
    d.rrect(s, 0.45, y, 12.45, 0.44, color, None, radius=0.1)
    d.rect(s, 0.6, y + 0.15, 0.12, 0.14, GOLD_L)
    d.tx(s, 0.82, y, 12.0, 0.44, text, 11, WHITE, True, anchor="m")


# ================================================================ cover
for sh in cover.shapes:
    if sh.has_text_frame and "Hakuba" in sh.text_frame.text:
        tf = sh.text_frame
        bp = tf._txBody.bodyPr
        for c in list(bp):
            bp.remove(c)
        ps = tf.paragraphs
        ps[1].runs[0].text = "長岡花火｜台灣市場 Inbound 集客策略提案"
        ps[3].runs[0].text = "2026年11月"
        ps[3].runs[0].font.size = Pt(16)
        for i in (2, 0):
            ps[i]._p.getparent().remove(ps[i]._p)
    elif sh.has_text_frame and ("敬啟" in sh.text_frame.text or "御中" in sh.text_frame.text):
        r0 = sh.text_frame.paragraphs[0].runs
        r0[0].text = "XXX　敬啟"
        for r in r0[1:]:
            r.text = ""
d.tx(cover, 1.89, 4.6, 10.36, 0.45, "一生一次的花火，變成一整年的長岡。", 15, NAVY, True, align="c")

# ================================================================ p2 KV opener
s = blank()
d.rect(s, 0, 0, 13.333, 7.5, NIGHT)
d.pic(s, IMG("phoenix_pano.jpg"), 0, 3.0, 13.333, 4.5, mode="cover", crop=(0, 0.12, 0, 0))
grad_rect(s, 0, 3.0, 13.333, 1.3, NIGHT, 1.0, 0.0, angle=90)
d.tx(s, 0.8, 0.55, 11.5, 0.4, "NAGAOKA FIREWORKS × TAIWAN　2027", 12, GOLD_L, True, font="Georgia")
d.tx(s, 0.8, 0.95, 12, 1.0, "一生一次的花火，", 40, WHITE, True, font="Hiragino Mincho ProN")
d.tx(s, 0.8, 1.75, 12, 1.0, "變成一整年的長岡。", 40, WHITE, True, font="Hiragino Mincho ProN")
d.tx(s, 0.82, 2.75, 11.5, 0.4, "台灣人已經愛上長岡花火。下一步，是讓他們「用對的方式來」，並在 8 月以外也想起長岡。", 13, "E6E9F2")
ai(s, 12.5, 7.15)
pageno(s)

# ================================================================ p3 目次
s = blank()
d.tx(s, 0.0, 0.13, 10.7, 0.45, "目次", 24, NAVY, True, anchor="m")
photo(s, IMG("ta_yukata.jpg"), 8.3, 0.95, 4.6, 5.9)
grad_rect(s, 8.3, 4.6, 4.6, 2.25, NIGHT, 0.0, 0.85, angle=90)
d.tx(s, 8.55, 5.55, 4.2, 1.2, "「被 IG Reels 燒到🔥」\n——台灣人的長岡花火，從手機開始。", 12, WHITE, True, line=1.3)
toc = [("01", "現況分析", "台灣市場・長岡花火的聲量・卡關點"),
       ("02", "提案概念", "一生一次的花火，一整年的長岡"),
       ("03", "集客施策", "Threads・KOC・IG・GEO・繁中指南・安全啟發・淡季內容"),
       ("04", "視覺提案", "現行視覺研究 → KV・Banner 系列"),
       ("05", "KPI・方案・時程", "保證／目標值／承諾交付、3方案、2026/12〜2027/9")]
for i, (n, t, b) in enumerate(toc):
    y = 1.15 + i * 1.08
    d.tx(s, 0.8, y, 1.2, 0.8, n, 34, GOLD_T, True, font="Georgia", anchor="m")
    d.tx(s, 2.1, y + 0.05, 5.8, 0.45, t, 19, NAVY, True)
    d.tx(s, 2.1, y + 0.5, 5.8, 0.35, b, 11, GREY)
    d.hline(s, 2.1, y + 0.95, 7.8, y + 0.95, LINE, 1)
pageno(s, GREY)

# ================================================================ SECTION 01
section("01", "現況分析", "台灣市場的特性，與「長岡花火」在台灣被怎麼談論。\n聲量資料：Pandora（2025/10/27〜2026/10/26・2,669篇）", IMG("aerial.jpg"))

# ---------------------------------------------------------------- 1-1 台灣市場
s = d.new("1-1. 現況分析｜台灣旅客的3個前提",
          "2025年訪日台灣旅客676萬人（＋11.9％）。台灣人不會因一支廣告就出發——先被打動，再反覆查證，最後才訂票。長岡花火正好走完這三步。",
          "資料來源：JNTO訪日外客統計（2025年）／Similarweb・Meta公開資料／Pandora 長岡花火言及量・インサイトレポート")
photo(s, IMG("phone_taipei.jpg"), 0.45, 1.6, 5.2, 4.55)
grad_rect(s, 0.45, 4.6, 5.2, 1.55, NIGHT, 0.0, 0.9, angle=90)
d.tx(s, 0.65, 5.35, 4.9, 0.8, "晚上 11 點，在台北的沙發上，\n被一支 Reels 決定了明年夏天。", 12.5, WHITE, True, line=1.25)
pre = [("1", "先被「感動」打動", "IG Reels・Threads 的現場影片是起點。長岡花火的聲量 Top10 中，9 篇是「感動」與「嚮往」。", "Instagram ＝ 嚮往"),
       ("2", "再「反覆查證」", "搶票・交通・住宿，一定先問過去過的人。「請問有沒有去過的朋朋分享攻略」一篇就有 732 則留言。", "Threads・Dcard・PTT ＝ 查證"),
       ("3", "自由行（FIT），2〜6個月前決定", "長岡花火的「決定」集中在 3〜6 月的抽選期——遠早於 8 月的聲量高峰。", "勝負在出發前")]
for i, (n, t, b, tag) in enumerate(pre):
    y = 1.6 + i * 1.55
    d.rrect(s, 5.9, y, 7.0, 1.42, WHITE, LINE)
    d.tx(s, 6.05, y + 0.12, 0.7, 1.0, n, 40, GOLD_L, True, font="Georgia")
    d.tx(s, 6.8, y + 0.14, 4.0, 0.36, t, 13.5, NAVY, True)
    d.label(s, 10.75, y + 0.16, 2.0, 0.3, tag, PINK, WHITE, 8.5, radius=0.3)
    d.tx(s, 6.8, y + 0.55, 5.95, 0.8, b, 9.5, INK, line=1.25)
stat(s, 0.45, 6.25, 1.68, 0.6, "676萬人", "2025 訪日台灣旅客", PINK, SOFT, 14)
d.tx(s, 2.2, 6.25, 3.45, 0.6, "台灣人出國目的地第1名是日本。Threads 的台灣流量占全球第1。", 8.5, GREY, anchor="m")

# ---------------------------------------------------------------- 1-2 聲量全貌
s = d.new("1-2. 現況分析｜「長岡花火」在台灣的聲量全貌",
          "一年 2,669 篇、總聲量 477 萬。好感度極高，但聲量的 74％ 集中在 8 月一個月——平常的 11 個月，台灣人幾乎不談長岡。",
          SRC_V + "。聲量＝10＋讚×3＋留言×5。")
vals = [("2,669", "文章數"), ("1,509,071", "讚數"), ("43,222", "留言數"), ("565.4", "平均讚數"), ("16.2", "平均留言"), ("4,770,013", "總聲量")]
for i, (v, l) in enumerate(vals):
    x = 0.45 + i * 2.09
    stat(s, x, 1.6, 1.98, 0.95, v, l, NIGHT if i < 5 else WHITE, SOFT if i < 5 else NIGHT, 18)
    if i == 5:
        d.tx(s, x + 0.05, 1.6 + 0.95 * 0.58, 1.88, 0.38, l, 8.5, "C9D2E8", align="c")
# monthly bars
months = [("10", 0), ("11", 328), ("12", 528), ("1", 275147), ("2", 25219), ("3", 21176), ("4", 137034), ("5", 283410),
          ("6", 178541), ("7", 239519), ("8", 3543341), ("9", 61301), ("10", 4469)]
d.rrect(s, 0.45, 2.75, 7.6, 3.5, WHITE, LINE)
d.tx(s, 0.6, 2.82, 6, 0.3, "月別聲量（2025/10〜2026/10）", 10.5, NAVY, True)
CX, CY, CW, CH = 0.85, 3.3, 7.0, 2.35
mx = 3543341
for i, (m, v) in enumerate(months):
    bw = CW / 13 * 0.62
    x = CX + i * CW / 13
    hh = max(0.02, CH * (v / mx) ** 0.5)  # 平方根刻度
    col = PINK if m == "8" else (GOLD_L if v > 100000 else "C9D2E8")
    d.rect(s, x, CY + CH - hh, bw, hh, col)
    lab = f"{v/10000:.1f}萬" if v >= 10000 else f"{v:,}"
    d.tx(s, x - 0.25, CY + CH - hh - 0.25, bw + 0.5, 0.22, lab, 7, INK if m != "8" else PINK, m == "8", align="c")
    d.tx(s, x - 0.2, CY + CH + 0.03, bw + 0.4, 0.22, m + "月", 7.5, GREY, align="c")
d.hline(s, CX - 0.05, CY + CH, CX + CW, CY + CH, "B8C4D6", 1)
d.tx(s, 0.6, 5.95, 7.3, 0.28, "※ 縱軸為平方根刻度（8月數值過大，以利比較）。2026/8 = 3,543,341（全年的 74.3％）", 7.5, GREY)
# platform
d.rrect(s, 8.25, 2.75, 4.65, 3.5, WHITE, LINE)
d.tx(s, 8.4, 2.82, 4.4, 0.3, "平台分布：篇數 vs 互動", 10.5, NAVY, True)
plat = [("Threads", 2155, 495476, "000000"), ("Instagram", 489, 1056415, PINK), ("PTT・Dcard・FB", 25, 402, "8A93A6")]
for i, (p, a, e, c) in enumerate(plat):
    y = 3.3 + i * 0.88
    d.tx(s, 8.4, y, 1.6, 0.3, p, 9.5, INK, True)
    d.rect(s, 10.0, y + 0.04, 2.7 * a / 2669, 0.2, c)
    d.tx(s, 10.0 + 2.7 * a / 2669 + 0.05, y, 1.0, 0.28, f"{a/2669*100:.1f}%", 8, INK, True)
    d.rect(s, 10.0, y + 0.32, max(0.02, 2.7 * e / 1551893), 0.2, GOLD_L)
    d.tx(s, 10.0 + max(0.02, 2.7 * e / 1551893) + 0.05, y + 0.28, 1.2, 0.28, f"{e/1551893*100:.1f}%", 8, INK, True)
d.rect(s, 8.4, 5.98, 0.18, 0.12, "000000"); d.tx(s, 8.6, 5.9, 0.9, 0.25, "篇數", 7.5, GREY)
d.rect(s, 9.3, 5.98, 0.18, 0.12, GOLD_L); d.tx(s, 9.5, 5.9, 1.6, 0.25, "互動（讚＋留言）", 7.5, GREY)
d.tx(s, 8.4, 5.55, 4.4, 0.35, "Threads 篇數最多（80.7％）＝討論・發問；\nIG 互動最多（68.1％）＝感動的擴散。", 8, NAVY, True, line=1.1)
bottom_bar(s, "好感度是滿分，問題是「時間」：一年只有 8 月被看見。")

# ---------------------------------------------------------------- 1-3 時間空白
s = d.new("1-3. 現況分析｜聲量在8月爆發，但「決定」發生在1〜6月",
          "Pandora 的月次分析顯示：1月正三尺玉的影片引爆嚮往、3〜6月抽選與交通成為焦點、8月才是感動的分享。台灣人的旅程，比聲量高峰早了半年。",
          SRC_I + "（月次トレンド分析）")
phase = [("11〜12月", "回顧・白菊", "年末回顧中提到長岡；慰靈的「白菊」帶來情感共鳴", "328〜528", "C9D2E8", "shiragiku.jpg"),
         ("1〜2月", "嚮往被點燃", "1月「正三尺玉」影片爆紅：僅 11 篇卻有 27.5 萬聲量（單篇 25,013，全年最高）", "27.5萬", GOLD_L, "sanjaku.jpg"),
         ("3〜5月", "抽選・搶票", "抽選規則、海外販售、二重價格討論；落選後轉向旅行團", "2.1萬→28.3萬", PINK, "ta_family.jpg"),
         ("6〜7月", "交通・住宿攻略", "回程新幹線、住宿高漲、JR 周遊券；攻略文大量出現", "17.9萬→24.0萬", PINK, "masu.jpg"),
         ("8月", "感動・散場", "鳳凰・黃金雨的感動；同時長岡站的散場混雜成為話題", "354萬", NIGHT, "kv_hero.jpg"),
         ("9〜10月", "隔年預約", "回顧與「明年還要再來」；2027 旅行團開始招募", "6.1萬→0.4萬", "8A93A6", "bus.jpg")]
for i, (m, t, b, v, c, img) in enumerate(phase):
    x = 0.45 + i * 2.1
    photo(s, IMG(img), x, 1.6, 1.98, 1.25, tag=(i == 0))
    d.rect(s, x, 2.85, 1.98, 0.08, c)
    d.tx(s, x, 2.98, 1.98, 0.3, m, 11, c if c not in ("C9D2E8",) else GREY, True, font="Meiryo")
    d.tx(s, x, 3.28, 1.98, 0.32, t, 12.5, NAVY, True)
    d.tx(s, x, 3.62, 1.98, 1.1, b, 8.5, INK, line=1.2)
    d.rrect(s, x, 4.75, 1.98, 0.5, SOFT, None)
    d.tx(s, x, 4.75, 1.98, 0.5, [[("聲量 ", {"size": 7.5, "color": GREY}), (v, {"size": 11, "bold": True, "color": NAVY})]], 9, INK, align="c", anchor="m")
d.arrow(s, 0.45, 5.4, 12.45, 0.28, "E6E9F2")
d.tx(s, 0.6, 5.38, 12.2, 0.3, "旅マエ（決定）————————————————————————————　旅ナカ（體驗）　————　旅アト（再訪）", 8.5, GREY, True, anchor="m")
d.rrect(s, 0.45, 5.8, 12.45, 0.95, "FDECEF", None)
d.tx(s, 0.65, 5.85, 12.1, 0.85, [[("洞察　", {"color": PINK, "size": 11}), ("8 月的聲量是「結果」，不是「機會」。真正影響台灣人行動的是 1〜6 月——此時官方的繁中資訊幾乎不存在，KKday・Klook・KOL 代替官方回答了問題。", {})]], 10.5, INK, True, anchor="m", line=1.25)

# ---------------------------------------------------------------- 1-4 熱門貼文
s = d.new("1-4. 現況分析｜台灣人在談什麼——聲量 Top 貼文",
          "高聲量貼文分成兩種：IG 上「哭了・一生一次」的感動影片，以及 Threads 上「怎麼搶票・怎麼回去」的提問與攻略。前者製造嚮往，後者決定行動。",
          SRC_V + "。貼文內容為摘要。")
posts = [("IG", "2026/8/4", "2026長岡花火精華來了！看完就知道為什麼說是人生必看", "177,834", "1,126", "53.9萬", PINK, "感動"),
         ("IG", "2026/8/3", "4年前第一次看…今年終於拍到超美的復興 Phoenix 花火", "102,162", "319", "30.8萬", PINK, "感動"),
         ("IG", "2026/6/9", "千萬不要以為有座位票就安心了！住宿與交通才是大魔王", "33,811", "1,482", "10.9萬", GOLD_T, "攻略"),
         ("Threads", "2026/8/3", "平原綾香〈Jupiter〉一響，全場安靜。有去過的人，當下有哭嗎？", "33,032", "310", "10.1萬", NAVY, "感動・提問"),
         ("Threads", "2026/4/22", "有沒有去過的朋朋分享搶票跟行程住宿攻略？被IG Reels燒到🔥", "20,327", "732", "6.5萬", NAVY, "提問"),
         ("IG", "2026/8/13", "出發前研究了很多交通方式…東京當日來回的一日行程筆記", "15,148", "95", "4.6萬", GOLD_T, "攻略")]
for i, (pf, dt, t, lk, cm, vol, c, tag) in enumerate(posts):
    col, row = i % 3, i // 3
    x, y = 0.45 + col * 4.17, 1.6 + row * 2.05
    d.rrect(s, x, y, 4.05, 1.9, WHITE, LINE)
    d.label(s, x + 0.15, y + 0.15, 0.85, 0.26, pf, c, WHITE, 8.5, radius=0.3)
    d.label(s, x + 1.08, y + 0.15, 0.95, 0.26, tag, SOFT2, NAVY, 8, radius=0.3)
    d.tx(s, x + 2.1, y + 0.13, 1.8, 0.3, dt, 8, GREY, align="r")
    d.tx(s, x + 0.15, y + 0.5, 3.75, 0.75, "「" + t + "」", 10, INK, True, line=1.2)
    d.hline(s, x + 0.15, y + 1.32, x + 3.9, y + 1.32, LINE, 0.75)
    d.tx(s, x + 0.15, y + 1.38, 3.8, 0.42, [[("聲量 ", {"size": 8, "color": GREY}), (vol, {"size": 13, "bold": True, "color": c}),
                                             ("　♡ " + lk + "　💬 " + cm, {"size": 8.5, "color": GREY})]], 9, INK, anchor="m")
d.rrect(s, 0.45, 5.75, 6.15, 1.0, SOFT, None)
d.tx(s, 0.6, 5.8, 5.9, 0.9, [[("IG＝感動的擴散器　", {"color": PINK, "size": 10.5})], "489篇就拿下全體互動的68％。「傳給你想一起去的人」是固定句型——嚮往靠分享擴散。"], 9, INK, True, line=1.2)
d.rrect(s, 6.75, 5.75, 6.15, 1.0, SOFT, None)
d.tx(s, 6.9, 5.8, 5.9, 0.9, [[("Threads＝查證與發問的場所　", {"color": NAVY, "size": 10.5})], "2,155篇的主體是提問與攻略。留言最多的貼文，都是「怎麼買票・怎麼回去」。"], 9, INK, True, line=1.2)

# ---------------------------------------------------------------- 1-5 感動 vs 卡關
s = d.new("1-5. 現況分析｜「苦也值得」的感動，與一再出現的卡關",
          "Pandora 的情緒分析：體驗本身是滿分，負面幾乎都集中在「去程與回程」——搶票、住宿、散場。台灣人用「生存攻略」自力克服，官方並不在場。",
          SRC_I + "（センチメント分析・全体インサイト）")
photo(s, IMG("kv_hero.jpg"), 0.45, 1.6, 6.1, 2.0)
grad_rect(s, 0.45, 2.6, 6.1, 1.0, NIGHT, 0.0, 0.85, angle=90)
d.tx(s, 0.65, 3.12, 5.8, 0.45, "感動｜體驗價值", 15, WHITE, True)
pos = [("2km 的鳳凰・正三尺玉", "視覺與聲音的壓倒性規模，「起雞皮疙瘩」「眼淚停不下來」"),
       ("空襲追悼・震災復興的故事", "不只是煙火，而是和平與復興的祈願——深度共鳴"),
       ("一生一次的人生清單", "「再辛苦也值得」，看完後強烈想再訪、想推薦"),
       ("有料觀覽席的安心", "旅行社團體席・椅席等，能確保好位置被高度評價")]
for i, (t, b) in enumerate(pos):
    y = 3.75 + i * 0.66
    d.rect(s, 0.45, y, 0.08, 0.56, GOLD_L)
    d.tx(s, 0.65, y, 5.8, 0.28, t, 10.5, NAVY, True)
    d.tx(s, 0.65, y + 0.28, 5.8, 0.3, b, 8.5, GREY)
photo(s, IMG("station.jpg"), 6.8, 1.6, 6.1, 2.0)
grad_rect(s, 6.8, 2.6, 6.1, 1.0, "3A0E1A", 0.0, 0.85, angle=90)
d.tx(s, 7.0, 3.12, 5.8, 0.45, "卡關｜去程與回程", 15, WHITE, True)
neg = [("散場後的長岡站・新幹線", "月台極度擁擠、搭不上車、推擠與插隊；安全疑慮"),
       ("觀覽券抽選與轉賣", "連續落選、代理過量販售的取消、高價轉賣與詐騙疑慮"),
       ("住宿一房難求", "市內數月前客滿，被迫住新潟・越後湯沢・高崎或東京當日來回"),
       ("現場環境的資訊落差", "木板マス席久坐、酷暑、視線被遮——事前資訊不足")]
for i, (t, b) in enumerate(neg):
    y = 3.75 + i * 0.66
    d.rect(s, 6.8, y, 0.08, 0.56, PINK)
    d.tx(s, 7.0, y, 5.8, 0.28, t, 10.5, "8E1F3B", True)
    d.tx(s, 7.0, y + 0.28, 5.8, 0.3, b, 8.5, GREY)
bottom_bar(s, "負面不是對長岡的不滿，而是「資訊不足」的成本——這是官方繁中資訊可以直接解決的。", y=6.42)

# ---------------------------------------------------------------- 1-6 5個卡關點（地圖）
s = d.new("1-6. 現況分析｜台灣旅客在長岡花火的5個「卡關點」",
          "從抽選到回到飯店，台灣旅客在 5 個地方卡住。Pandora 的關鍵字分析中，「車站」「回程」「飯店」「散場」「人潮」都是高聲量話題。",
          SRC_I + "（キーワード分析：車站135篇・飯店112篇・回程92篇・散場87篇・人潮76篇）。航拍為AI示意，位置為概念示意。")
MX, MY, MW, MH = 3.55, 1.55, 6.25, 3.49
photo(s, IMG("aerial.jpg"), MX, MY, MW, MH)
grad_rect(s, MX, MY + MH - 1.0, MW, 1.0, NIGHT, 0.0, 0.6, angle=90)
pins = {1: (0.2, 0.84), 2: (0.82, 0.55), 3: (0.42, 0.62), 4: (0.74, 0.4), 5: (0.6, 0.18)}
cards = [(1, "抽選・購票", "「海外販售怎麼報名？」\n落選後只能找旅行團／轉賣", "繁中官方指南・GEO", 0.45, 1.55, "L"),
         (2, "住宿", "「飯店 112 篇」：市內客滿\n分散到新潟・越後湯沢・高崎", "住宿分散建議・回程班次", 0.45, 3.22, "L"),
         (3, "會場觀覽環境", "マス席久坐・酷暑・視線\n「要帶什麼？」的提問", "觀覽準備清單（KOC）", 0.45, 4.89, "L"),
         (4, "散場・長岡站", "「車站 135 篇」「散場 87 篇」\n月台擁擠、推擠、末班車", "散場路線・安全啟發", 9.95, 1.55, "R"),
         (5, "回程新幹線", "「回程 92 篇」：指定席秒殺\n自由席站一路、深夜到東京", "回程預約時程・接駁", 9.95, 3.22, "R")]
for n, t, b, sol, x, y, side in cards:
    with d.anim(s):
        px, py = pins[n]
        cx, cy = MX + px * MW, MY + py * MH
        d.hline(s, x + 2.95 if side == "L" else x, y + 0.75, cx, cy, "FFFFFF", 1.25)
        d.circle(s, cx - 0.17, cy - 0.17, 0.34, str(n), PINK, 10)
        d.rrect(s, x, y, 2.95, 1.52, WHITE, PINK, lw=1.25)
        d.circle(s, x + 0.12, y + 0.12, 0.4, str(n), PINK, 12)
        d.tx(s, x + 0.6, y + 0.1, 2.3, 0.42, t, 12, PINK, True, anchor="m")
        d.tx(s, x + 0.15, y + 0.56, 2.75, 0.52, b, 8.5, INK, line=1.1)
        d.label(s, x + 0.15, y + 1.12, 2.65, 0.3, "→ " + sol, NIGHT, WHITE, 8.5, radius=0.3)
with d.anim(s):
    d.rrect(s, 9.95, 4.89, 2.95, 1.52, SOFT2, None)
    d.tx(s, 10.1, 4.95, 2.7, 0.3, "共通前提", 10.5, NAVY, True)
    d.tx(s, 10.1, 5.27, 2.7, 1.1, "觀覽券每年完售（2026年6/17公告完售）。目的不是「多賣票」，而是讓來的人「準備好再來」。", 8.5, INK, line=1.2)
d.rrect(s, 3.55, 5.2, 6.25, 1.21, WHITE, LINE)
kw = [("車站", 135, 3382), ("飯店", 112, 3469), ("回程", 92, 2513), ("散場", 87, 1926), ("人潮", 76, 3043)]
d.tx(s, 3.7, 5.24, 6.0, 0.28, "卡關關鍵字（篇數｜平均聲量）", 9, NAVY, True)
for i, (k, n, v) in enumerate(kw):
    x = 3.7 + i * 1.2
    d.tx(s, x, 5.55, 1.15, 0.3, k, 10.5, PINK, True, align="c")
    d.tx(s, x, 5.85, 1.15, 0.45, f"{n}篇\n{v:,}", 8.5, INK, align="c", line=1.05)

# ---------------------------------------------------------------- 1-7 資訊中樞空缺
s = d.new("1-7. 現況分析｜回答台灣人問題的，不是官方",
          "台灣人的問題，現在由 KKday・Klook、在日台灣 KOL 與旅行團回答。官方的海外直接發信有限——轉賣、二重價格、散場安全等敏感議題，也只能任由網路解讀。",
          SRC_I + "（チャネルインサイト・月次トレンド 2026年5月）／長岡花火チケットセンター 官網（2026年）")
hubs = [("OTA（KKday・Klook）", "新幹線預購・當日往返接駁・觀覽席旅行團。混雜與回程的「解決方案」都在這裡被推薦。", "實質的資訊樞紐", GOLD_T),
        ("在日台灣人 KOL", "「住在東京10年的Lena」型的攻略・限時優惠。單篇 10.9 萬聲量、1,482 則留言。", "信任來自「過來人」", PINK),
        ("旅行團・包車", "「最懶人就是直接報團」。觀覽席＋住宿＋交通一體化的需求高，但團的品質爭議也存在。", "高價也願意付", NAVY)]
for i, (t, b, tag, c) in enumerate(hubs):
    y = 1.6 + i * 1.18
    d.rrect(s, 0.45, y, 6.4, 1.06, WHITE, LINE)
    d.rect(s, 0.45, y, 0.1, 1.06, c)
    d.tx(s, 0.7, y + 0.1, 3.8, 0.32, t, 12, c, True)
    d.label(s, 4.75, y + 0.12, 1.95, 0.28, tag, SOFT2, NAVY, 8, radius=0.3)
    d.tx(s, 0.7, y + 0.46, 6.0, 0.6, b, 9, INK, line=1.2)
d.rrect(s, 0.45, 5.2, 6.4, 1.55, "FDECEF", None)
d.tx(s, 0.65, 5.27, 6.0, 0.3, "官方不在場時，會發生什麼", 11, PINK, True)
d.tx(s, 0.65, 5.6, 6.1, 1.15, ["・海外票價的「二重價格」議論（2026年5月）被各自解讀",
                                  "・轉賣・過量販售・詐騙的疑慮，沒有可以引用的正確資訊",
                                  "・「沒有票也能在通道上看嗎？」——官方已禁止，但繁中沒有人說"], 9, INK, line=1.3)
photo(s, IMG("masu.jpg"), 7.1, 1.6, 5.8, 2.6)
d.rrect(s, 7.1, 4.35, 5.8, 2.4, NIGHT, None)
d.tx(s, 7.3, 4.45, 5.4, 0.35, "機會：成為「被引用的那個來源」", 13, GOLD_L, True)
d.tx(s, 7.3, 4.9, 5.45, 1.8, ["・Pandora：「官方對海外的直接發信與即時交通資訊有限，由有志者・KOL・OTA 代替」",
                                "・繁中的「官方說法」只要存在，就會被 OTA、KOL 與 AI 搜尋引用",
                                "・不必取代 OTA——讓 OTA 的商品頁也連回官方指南"], 9.5, WHITE, line=1.35)

# ================================================================ SECTION 02
section("02", "提案概念", "一生一次的花火，變成一整年的長岡。\n官方的繁中聲音，從「抽選前」開始陪伴台灣旅客。", IMG("kv_hero.jpg"))

# ---------------------------------------------------------------- IDEA
s = blank()
d.pic(s, IMG("shiragiku.jpg"), 0, 0, 7.4, 7.5, mode="cover")
ai(s, 0.15, 0.15)
d.rect(s, 7.4, 0, 5.933, 7.5, NIGHT)
d.tx(s, 7.9, 0.7, 4.8, 0.3, "IDEA", 11, GOLD_L, True, font="Georgia")
d.tx(s, 7.9, 1.05, 5.2, 1.6, "一生一次的花火，\n一整年的長岡。", 30, WHITE, True, font="Hiragino Mincho ProN", line=1.2)
d.tx(s, 7.9, 2.65, 4.9, 0.9, "8月2日・3日的兩個夜晚，是終點，不是全部。\n從「想去」到「再來」，官方的繁中聲音全程在場。", 11, "D9DEEA", line=1.4)
ide = [("被引用的官方", "Threads官方帳號＋繁中指南＋GEO：讓 OTA・KOL・AI 都引用同一份正確資訊"),
       ("準備好再來", "抽選・住宿・散場的攻略由官方先講：減少轉賣・混雜・失望"),
       ("8月以外也想起長岡", "白菊的故事、正三尺玉的新年、酒藏與春櫻：把聲量空白的 11 個月補起來")]
for i, (t, b) in enumerate(ide):
    y = 3.85 + i * 0.95
    d.circle(s, 7.9, y, 0.42, str(i + 1), PINK, 12)
    d.tx(s, 8.45, y - 0.04, 4.5, 0.32, t, 13, GOLD_L, True)
    d.tx(s, 8.45, y + 0.3, 4.5, 0.6, b, 9.5, WHITE, line=1.2)
pageno(s)

# ---------------------------------------------------------------- 2-1 Truth → Proposition
s = d.new("2-1. 提案概念｜從3個事實，導出3個對策",
          "每一個對策，都對應 Pandora 的一個數字。",
          SRC_V + "／" + SRC_I.replace("資料來源：", ""))
rows = [("事實①", "聲量 74％ 集中在 8 月，1〜6 月的「決定期」官方幾乎沒有繁中資訊",
         "2026/8＝3,543,341（全年 4,770,013）", "決定期的官方發信", "Threads 官方帳號＋繁中指南 LP＋GEO，在抽選前就成為答案"),
        ("事實②", "負面集中在搶票・住宿・散場；台灣人用「生存攻略」自力克服",
         "車站135篇・飯店112篇・回程92篇・散場87篇", "準備好再來", "KOC 攻略（官方監修）＋安全・正規購票啟發，把卡關變成清單"),
        ("事實③", "感動來自故事（白菊・鳳凰・正三尺玉），1月的正三尺玉僅 11 篇就有 27.5 萬聲量",
         "2026/1 單篇平均聲量 25,013（全年最高）", "故事讓淡季也被想起", "白菊・正三尺玉・長岡四季的內容與 IG UGC，填補 11 個月的空白")]
hdr = ["", "事實（Truth）", "Pandora 根據", "→ 對策（Proposition）", ""]
for j, (x, w) in enumerate([(0.45, 1.0), (1.5, 4.1), (5.65, 2.7), (8.4, 4.5)]):
    if j:
        d.label(s, x, 1.55, w, 0.38, ["", "事實（Truth）", "Pandora 根據", "對策（Proposition）"][j], NIGHT if j < 3 else PINK, WHITE, 10, radius=0.1)
for i, (k, t, ev, pt, pb) in enumerate(rows):
    y = 2.05 + i * 1.45
    d.circle(s, 0.6, y + 0.35, 0.65, str(i + 1), GOLD_L, 18, NIGHT)
    d.rrect(s, 1.5, y, 4.1, 1.32, WHITE, LINE)
    d.tx(s, 1.65, y + 0.1, 3.85, 1.15, t, 10.5, INK, True, anchor="m", line=1.25)
    d.rrect(s, 5.65, y, 2.25, 1.32, SOFT, None)
    d.tx(s, 5.72, y + 0.1, 2.1, 1.15, ev, 9.5, NAVY, True, anchor="m", align="c", line=1.2)
    d.arrow(s, 7.97, y + 0.5, 0.38, 0.32, PINK)
    d.rrect(s, 8.4, y, 4.5, 1.32, "FDECEF", None)
    d.tx(s, 8.55, y + 0.1, 4.25, 0.35, pt, 12.5, PINK, True)
    d.tx(s, 8.55, y + 0.5, 4.25, 0.8, pb, 9.5, INK, line=1.2)
bottom_bar(s, "Proposition｜官方的繁中聲音，從抽選前開始陪伴：準備好再來，8月以外也想起長岡。", y=6.45)

# ---------------------------------------------------------------- 2-2 TA
s = d.new("2-2. 目標族群｜從 Top 貼文反推的3種台灣旅客",
          "不是用年齡切，而是用「行為」切。每一群在不同的時間點、不同的平台做決定。",
          SRC_V + "（Top貼文・インサイトレポート ターゲット層）。人物為AI示意。")
tas = [("TA1", "一生一次朝聖派", "20〜30代・情侶／閨蜜", "ta_yukata.jpg",
        ["被 IG Reels「燒到」而心動", "浴衣・拍照・「傳給想一起去的人」", "第一次去，最怕搶不到票與散場"],
        "IG Reels ／ Threads", "①感動 ②準備清單", PINK),
       ("TA2", "攻略計畫派（J型）", "30〜40代・家庭／小團體", "ta_family.jpg",
        ["半年前就開始比較席種・住宿・回程", "「有沒有去過的朋朋分享攻略」型發問", "願意付費換安心（旅行團・接駁）"],
        "Threads ／ Dcard ／ AI搜尋", "③散場 ④住宿與回程", NAVY),
       ("TA3", "回訪深度派", "30〜40代・攝影／連續參加", "ta_photo.jpg",
        ["連續 2〜4 年參加、追求更好的位置", "對白菊・鳳凰的故事與歷史有共鳴", "也是長岡四季的潛在旅客"],
        "IG ／ Threads 攝影社群", "⑤故事・長岡四季", GOLD_T)]
for i, (k, n, a, img, bl, ch, ang, c) in enumerate(tas):
    x = 0.45 + i * 4.17
    photo(s, IMG(img), x, 1.6, 4.05, 2.15)
    d.label(s, x + 0.12, y := 1.6 + 1.75, 0.65, 0.28, k, c, WHITE, 9, radius=0.3)
    d.rrect(s, x, 3.8, 4.05, 2.95, WHITE, LINE)
    d.tx(s, x + 0.15, 3.88, 3.8, 0.38, n, 14, c, True)
    d.tx(s, x + 0.15, 4.25, 3.8, 0.28, a, 9, GREY)
    for j, b in enumerate(bl):
        d.tx(s, x + 0.15, 4.6 + j * 0.34, 3.8, 0.32, "・" + b, 9.5, INK)
    d.hline(s, x + 0.15, 5.68, x + 3.9, 5.68, LINE, 0.75)
    d.tx(s, x + 0.15, 5.74, 3.8, 0.3, [[("主要渠道　", {"color": GREY, "size": 8}), (ch, {"bold": True})]], 9, INK)
    d.tx(s, x + 0.15, 6.08, 3.8, 0.3, [[("對應切角　", {"color": GREY, "size": 8}), (ang, {"bold": True, "color": c})]], 9, INK)

# ---------------------------------------------------------------- 2-3 一年的旅程
s = d.new("2-3. 旅程設計｜把「8月的兩晚」攤成一整年",
          "旅マエ（決定）・旅ナカ（體驗）・旅アト（再訪）三階段，對應 Pandora 的月別話題。施策期間 2026年12月〜2027年9月。",
          SRC_I + "（月次トレンド分析）。抽選日程依2026年實績推估，以官方公布為準。")
stg = [("12〜2月", "嚮往", "正三尺玉的新年・白菊的故事", "sanjaku.jpg", "Threads官方開設／IG UGC 冬季／GEO 佈局", GOLD_T),
       ("3〜6月", "決定", "抽選・席種・住宿・回程", "ta_family.jpg", "繁中指南上線／KOC 攻略／抽選前廣告", PINK),
       ("7〜8月", "體驗", "準備清單・散場・回程", "bus.jpg", "安全啟發／即時通知／現場 UGC", NAVY),
       ("9月〜", "再訪", "回顧・2028 預約・長岡四季", "winter_sake.jpg", "白菊回顧／冬春長岡內容／月報總結", "2E9E6A")]
for i, (m, t, b, img, act, c) in enumerate(stg):
    x = 0.45 + i * 3.13
    photo(s, IMG(img), x, 1.6, 3.0, 1.75, tag=(i == 0))
    d.poly(s, [(x, 3.42), (x + 2.85, 3.42), (x + 3.0, 3.7), (x + 2.85, 3.98), (x, 3.98)], c)
    d.tx(s, x + 0.12, 3.42, 2.7, 0.56, [[(m + "　", {"size": 10}), (t, {"size": 15})]], 12, WHITE, True, anchor="m")
    d.tx(s, x, 4.1, 3.0, 0.35, b, 10.5, c, True)
    d.rrect(s, x, 4.5, 3.0, 1.1, SOFT, None)
    d.tx(s, x + 0.1, 4.55, 2.8, 1.0, [[("主要施策\n", {"size": 8, "color": GREY})], act], 9.5, INK, True, line=1.25)
d.rrect(s, 0.45, 5.78, 12.45, 0.97, NIGHT, None)
d.tx(s, 0.65, 5.83, 1.9, 0.87, "貫穿全年", 12, GOLD_L, True, anchor="m")
d.tx(s, 2.4, 5.83, 10.3, 0.87, "Pandora 月次監測（台灣・香港）＋LINE 即時通知：轉賣・詐騙・散場等負面話題一出現就通報，官方帳號 24 小時內以正確資訊回應。", 10, WHITE, anchor="m", line=1.3)

# ================================================================ SECTION 03
section("03", "集客施策", "Threads 官方帳號・KOC・IG UGC・GEO・繁中官方指南・\n安全與正規購票啟發・淡季內容", IMG("koc_film.jpg"))

# ---------------------------------------------------------------- 3-0 全體像
s = d.new("3. 集客施策｜全體像",
          "認知（嚮往）→ 查證（決定）→ 行動（準備）→ 再訪，所有施策都導向「繁中官方指南」。成效以 Pandora 聲量與 UTM 流量來源衡量。",
          "※ 施策組合依方案（P.33）調整。")
layers = [("認知・嚮往", "Threads 官方帳號 ／ IG UGC（在日台灣人 KOC）", "IG的感動擴散 × 官方的故事發信", 12.45, GOLD_L, NIGHT),
          ("查證・決定", "Threads KOC 攻略文 ／ GEO（AI搜尋・新聞・論壇）", "「怎麼買・怎麼回」被查到時，答案是官方", 10.6, PINK, WHITE),
          ("行動・準備", "繁中官方指南 LP ／ 安全・正規購票啟發", "抽選日程・席種・散場路線・住宿分散", 8.75, NAVY, WHITE),
          ("再訪・淡季", "白菊・正三尺玉・長岡四季內容", "8月以外的聲量", 6.9, "2E9E6A", WHITE)]
for i, (t, a, b, w, c, tc) in enumerate(layers):
    y = 1.6 + i * 1.02
    x = 0.45 + (12.45 - w) / 2 - 2.0
    xx = 0.45 + (8.4 - w * 0.62) / 2
    W = 8.4 - i * 1.25
    X = 0.45 + i * 0.625
    d.poly(s, [(X, y), (X + W, y), (X + W - 0.62, y + 0.92), (X + 0.62, y + 0.92)], c)
    d.tx(s, X + 0.6, y + 0.04, W - 1.2, 0.36, t, 13, tc, True, align="c")
    d.tx(s, X + 0.6, y + 0.42, W - 1.2, 0.45, a, 9.5, tc, align="c")
    d.hline(s, X + W - 0.3, y + 0.46, 9.05, y + 0.46, "B8C4D6", 1, dash=True)
    d.rrect(s, 9.05, y + 0.1, 3.85, 0.72, WHITE, c, lw=1.25)
    d.tx(s, 9.18, y + 0.1, 3.6, 0.72, b, 9.5, INK, True, anchor="m")
d.rrect(s, 0.45, 5.75, 12.45, 1.0, SOFT2, None)
d.tx(s, 0.65, 5.8, 2.2, 0.9, "Pandora\n月次監測", 12, NAVY, True, anchor="m")
d.tx(s, 2.8, 5.8, 10.0, 0.9, "施策前基準值（4,770,013）→ 月別聲量・平台・話題・負面即時通知。每月提交月報，下個月的貼文主題與 KOC 發布時機據此調整。", 10, INK, anchor="m", line=1.3)

# ---------------------------------------------------------------- 3-1 Threads 官方帳號
s = d.new("3-1. 集客施策｜Threads 繁中官方帳號「長岡花火 繁中官方（暫稱）」",
          "台灣是 Threads 全球最大市場，長岡花火的討論 80.7％ 在 Threads。開設繁中官方帳號，成為「抽選怎麼報名」「散場怎麼走」的正式窗口，也發信白菊與鳳凰的故事。",
          "資料來源：Similarweb・Meta 公開資料／" + SRC_V.replace("資料來源：", "") + "。畫面為示意。")
d.pic(s, PNG("threads_official.png"), 0.45, 1.55, 2.6, 5.25)
d.pic(s, PNG("threads_koc.png"), 3.2, 1.55, 2.6, 5.25)
why = [("80.7％", "長岡花火貼文中 Threads 的占比"), ("732則", "單篇「搶票攻略」提問的留言數"), ("世界第1", "台灣在 Threads 全球流量的占比")]
for i, (v, l) in enumerate(why):
    stat(s, 6.1 + i * 2.3, 1.6, 2.18, 1.1, v, l, PINK, SOFT, 20)
ops = [("角色", "繁中的「官方窗口」：抽選・席種・交通・散場的正確資訊；轉賣與詐騙出現時第一時間澄清"),
       ("內容比例", "攻略 4：故事 3：幕後 3（白菊・鳳凰的由來、花火師、長岡四季）。宣傳型 10 篇不超過 1 篇"),
       ("發文", "每月 6 篇以上，抽選前（4〜6月）與 7〜8月加碼；平日晚間、週四 20 時為主"),
       ("留言經營", "每月 30〜100 則回覆；發文後 3 小時內回覆，連結放在第 1 則留言"),
       ("導流", "所有詳細資訊導向繁中官方指南（UTM 計測）")]
for i, (t, b) in enumerate(ops):
    y = 2.9 + i * 0.7
    d.label(s, 6.1, y + 0.08, 1.35, 0.42, t, NIGHT, WHITE, 9.5, radius=0.15)
    d.tx(s, 7.6, y, 5.3, 0.62, b, 9.5, INK, anchor="m", line=1.2)

# ---------------------------------------------------------------- 3-2 KOC 5切角
s = d.new("3-2. 集客施策｜Threads KOC 成果保證型——5個切角",
          "切角全部來自 Pandora 中台灣人實際在問的問題。由在日台灣人等 KOC 以「過來人」的口吻撰寫，內容事先經官方確認，並一律標示「合作」。",
          SRC_I + "／ 所有 KOC 貼文依台灣公平交易委員會規範標示「合作」。")
ang = [("①", "一生一次的理由", "鳳凰・白菊・正三尺玉，「為什麼大家都哭了」", "認知喚起", "1〜2月", "kv_hero.jpg"),
       ("②", "抽選・席種攻略", "海外怎麼報名、マス席 vs イス席、落選後的正規選項", "比較檢討", "3〜5月", "masu.jpg"),
       ("③", "散場不卡關", "A・B 會場的離場時機、月台的禮儀、接駁的選擇", "避免失敗", "6〜7月", "station.jpg"),
       ("④", "住宿與回程", "新潟・越後湯沢・高崎住宿、回程新幹線何時訂", "理解保存", "5〜7月", "bus.jpg"),
       ("⑤", "花火以外的長岡", "隔天去哪：酒藏、米與酒、冬與春的長岡", "再訪喚起", "9月〜", "winter_sake.jpg")]
for i, (n, t, b, p, m, img) in enumerate(ang):
    y = 1.58 + i * 0.98
    photo(s, IMG(img), 0.45, y, 1.45, 0.88, tag=False)
    d.tx(s, 2.05, y + 0.02, 0.5, 0.45, n, 18, PINK, True)
    d.tx(s, 2.55, y + 0.04, 3.2, 0.36, t, 12.5, NAVY, True)
    d.tx(s, 2.55, y + 0.42, 4.6, 0.45, b, 9, INK)
    d.label(s, 6.0, y + 0.08, 1.05, 0.28, p, SOFT2, NAVY, 8, radius=0.3)
    d.tx(s, 6.0, y + 0.45, 1.05, 0.3, m, 9, GREY, True, align="c")
ai(s, 0.5, 1.63)
d.pic(s, PNG("threads_koc.png"), 7.35, 1.55, 2.55, 5.15)
d.rrect(s, 10.1, 1.6, 2.8, 5.1, NIGHT, None)
d.tx(s, 10.25, 1.7, 2.5, 0.3, "成果保證", 11, GOLD_L, True)
d.tx(s, 10.25, 2.05, 2.5, 1.7, [[("每篇保證\n", {"size": 8.5, "color": "C9D2E8"})], [("瀏覽 10,000+\n互動 100+\n聲量 1,000+", {"size": 14})]], 12, WHITE, True, line=1.25)
d.tx(s, 10.25, 3.75, 2.5, 0.6, "未達成時，免費補發至達標", 9, GOLD_L, True)
d.hline(s, 10.25, 4.4, 12.75, 4.4, "3A4670", 1)
d.tx(s, 10.25, 4.5, 2.5, 2.1, ["KOC 條件", "・粉絲 3,000+ 的台灣帳號", "・1,500 字以內＋置入回文 10 則", "・原稿事先送審", "・標示「合作」"], 8.5, WHITE, line=1.35)

# ---------------------------------------------------------------- 3-3 IG UGC
s = d.new("3-3. 集客施策｜IG UGC——在日台灣人 KOC 的現場與四季",
          "IG 只占 18.3％ 的篇數，卻拿下 68％ 的互動。請在日台灣人 KOC 在花火當天與冬・春的長岡拍攝 Reels，讓嚮往在 8 月以外也持續擴散。",
          SRC_V + "。IG UGC 觸及為參考值（粉絲5,000〜10,000，單篇觸及約2,000〜5,000）。畫面為示意。")
d.pic(s, PNG("ig_reel.png"), 0.45, 1.55, 2.6, 5.25)
photo(s, IMG("koc_film.jpg"), 3.25, 1.6, 5.0, 2.8)
d.tx(s, 3.25, 4.45, 5.0, 0.3, "花火當天：開場前的現場與「怎麼回去」", 9.5, NAVY, True)
photo(s, IMG("winter_sake.jpg"), 3.25, 4.85, 2.45, 1.55, tag=False)
photo(s, IMG("spring.jpg"), 5.8, 4.85, 2.45, 1.55, tag=False)
d.tx(s, 3.25, 6.42, 5.0, 0.3, "冬・春：酒藏與信濃川的櫻花（淡季內容）", 9.5, NAVY, True)
pts = [("在日台灣人 KOC", "粉絲 5,000〜10,000 的微型 KOC。招待體驗＋Feed／Reels＋限時動態"),
       ("拍攝主題", "8月：開場前・白菊的瞬間・散場的走法\n冬春：酒藏・米・櫻花・花火的城市日常"),
       ("固定句型", "「傳給你想一起去的人」——沿用台灣人自己的分享語法"),
       ("二次利用", "素材授權給官方帳號・繁中指南・廣告使用"),
       ("標示", "所有貼文標示「合作」，人選事先確認")]
bullets(s, 8.6, 1.7, 4.3, pts, 10, 0.98, PINK)

# ---------------------------------------------------------------- 3-4 GEO
s = d.new("3-4. 集客施策｜GEO（AI搜尋優化）——讓 AI 的答案引用官方",
          "台灣旅客越來越常用 ChatGPT・Google AI 概覽來查「長岡花火怎麼買票」。以新聞・論壇文章與繁中官方指南，讓 AI 回答時引用官方的正確資訊。",
          "※ AI 搜尋畫面為示意。GEO 保證：每套 30 組關鍵字中 3 組於 AI 搜尋結果有效顯示，未達成退還該套金額 30％。")
d.pic(s, PNG("ai_search.png"), 0.45, 1.6, 6.6, 2.97)
sets = [("SET①", "購票・觀覽席", ["長岡花火 門票 怎麼買", "長岡花火 抽選 海外", "長岡花火 マス席 椅席 差別", "長岡花火 旅行團 推薦"], PINK),
        ("SET②", "交通・散場・住宿", ["長岡花火 散場 長岡站", "長岡花火 回程 新幹線", "長岡花火 住宿 新潟 越後湯沢", "長岡花火 東京 一日遊"], NAVY)]
for i, (k, t, kws, c) in enumerate(sets):
    x = 7.3 + i * 2.85
    d.rrect(s, x, 1.6, 2.75, 3.0, WHITE, c, lw=1.25)
    d.label(s, x + 0.12, 1.72, 0.75, 0.28, k, c, WHITE, 8.5, radius=0.3)
    d.tx(s, x + 0.95, 1.7, 1.75, 0.32, t, 10.5, c, True)
    for j, kw in enumerate(kws):
        d.rrect(s, x + 0.12, 2.15 + j * 0.5, 2.5, 0.4, SOFT, None)
        d.tx(s, x + 0.15, 2.15 + j * 0.5, 2.45, 0.4, kw, 8.5, INK, anchor="m", align="c")
    d.tx(s, x + 0.12, 4.17, 2.5, 0.35, "＋共 30 組", 8, GREY, align="c")
flow = [("新聞 6 本", "Yahoo奇摩新聞等保證刊登＋10〜15 家聯播"), ("論壇文 6 本", "Dcard・PTT・Mobile01 的攻略文"),
        ("關鍵字 30 組", "依 Pandora 的提問設計"), ("AI 命中 3 組", "Google AI 概覽・ChatGPT・Gemini（保證）")]
for i, (t, b) in enumerate(flow):
    x = 0.45 + i * 3.13
    d.rrect(s, x, 4.8, 2.95, 1.0, SOFT2, None)
    d.tx(s, x + 0.12, 4.85, 2.7, 0.35, t, 12, NAVY, True)
    d.tx(s, x + 0.12, 5.22, 2.75, 0.55, b, 9, INK, line=1.15)
    if i < 3:
        d.arrow(s, x + 2.97, 5.18, 0.14, 0.24, PINK)
bottom_bar(s, "每套（3個月）：新聞6＋論壇6＋KW30＋AI命中保證3組。OTA・KOL 的文章也會被同一份官方資訊「校正」。", y=6.0)

# ---------------------------------------------------------------- 3-5 繁中官方指南 LP
s = d.new("3-5. 集客施策｜繁中官方指南（LP）——所有施策的終點",
          "抽選日程・席種・交通・散場・住宿・花火的故事・長岡四季，用一頁繁中說清楚。手機優先設計，「散場路線」可以存在手機裡帶去現場。",
          "※ 畫面為示意。網域・頁面構成與官方網站的連結方式另行協議。")
d.pic(s, PNG("lp_pc.png"), 0.45, 1.6, 8.0, 4.61)
d.pic(s, PNG("lp_phone.png"), 8.1, 2.3, 2.15, 4.35)
mods = [("抽選日程", "海外報名的期間與方式"), ("席種比較", "マス席・イス席・シート席"), ("散場路線", "A・B 會場別、可離線保存"),
        ("住宿・回程", "分散住宿與回程班次"), ("花火的故事", "白菊・鳳凰・正三尺玉"), ("長岡四季", "8月以外的長岡")]
for i, (t, b) in enumerate(mods):
    y = 1.6 + i * 0.78
    d.circle(s, 10.5, y + 0.08, 0.32, str(i + 1), PINK, 9)
    d.tx(s, 10.9, y + 0.02, 2.0, 0.3, t, 10.5, NAVY, True)
    d.tx(s, 10.9, y + 0.32, 2.0, 0.3, b, 8.5, GREY)
d.tx(s, 0.45, 6.3, 7.5, 0.45, "UTM 計測：Threads・KOC・IG・GEO・廣告各自的流入與停留，在月報中比較。", 9.5, NAVY, True, anchor="m")

# ---------------------------------------------------------------- 3-6 安全・正規購票
s = d.new("3-6. 集客施策｜安全・正規購票啟發「一起守護長岡的夜空」",
          "沒有觀覽券不能進入觀覽區、只在正規管道購票、散場依誘導分批移動——這些「官方規則」，用台灣人聽得進去的語氣，在抽選前與出發前分兩次傳遞。",
          "長岡花火チケットセンター 官網「for International Visitors」（無票者不得於觀覽區・通道觀賞）／Pandora ネガティブ分析。圖為示意。")
d.pic(s, PNG("bn_manner.png"), 0.45, 1.6, 4.25, 4.25)
photo(s, IMG("station.jpg"), 4.9, 1.6, 4.0, 2.05)
photo(s, IMG("bus.jpg"), 4.9, 3.8, 4.0, 2.05)
d.tx(s, 4.9, 5.9, 4.0, 0.3, "散場的「想像」先給——減少現場的不安與推擠", 9, NAVY, True, align="c")
tl = [("4〜6月（抽選前）", "正規購票", "海外報名方式／轉賣・代購・詐騙的注意／沒抽到時的正規選項"),
      ("7月（出發前）", "準備清單", "席種別的攜帶品（坐墊・防暑）／住宿分散／回程預約時程"),
      ("8月（當天）", "散場與安全", "A・B 會場別的離場時機／月台禮儀／LINE 即時通知與官方帳號的現場資訊"),
      ("負面發生時", "即時澄清", "Pandora 即時通知 → 官方帳號 24 小時內發布正確資訊")]
for i, (m, t, b) in enumerate(tl):
    y = 1.6 + i * 1.08
    d.rrect(s, 9.1, y, 3.8, 0.98, WHITE, PINK if i < 3 else NAVY, lw=1.0)
    d.tx(s, 9.22, y + 0.06, 3.6, 0.28, m, 8.5, GREY, True)
    d.tx(s, 9.22, y + 0.3, 3.6, 0.3, t, 12, PINK if i < 3 else NAVY, True)
    d.tx(s, 9.22, y + 0.6, 3.6, 0.38, b, 8, INK, line=1.05)
bottom_bar(s, "目的不是「多賣票」，而是讓來的人「準備好再來」——滿意度，就是下一年的口碑。", y=6.3)

# ---------------------------------------------------------------- 3-7 淡季內容
s = d.new("3-7. 集客施策｜淡季內容——補上聲量空白的11個月",
          "Pandora 顯示：故事型內容即使在淡季也會被大量分享（1月正三尺玉 11 篇＝27.5 萬聲量）。用4個主題，讓長岡在 8 月以外也被想起。",
          SRC_I + "（2026年1月・11〜12月）。圖為AI示意，實際素材以官方提供・實地拍攝為準。")
cont = [("sanjaku.jpg", "1月", "新年，從一顆正三尺玉開始", "直徑 650m 的大玉，搭上新年的「開運」話題。官方帳號與 IG KOC 同步發布。"),
        ("shiragiku.jpg", "8月1日前後", "白菊——慰靈的白色花火", "1945 年長岡空襲的追悼與和平祈願。用「安靜」的內容，傳遞長岡花火真正的意義。"),
        ("winter_sake.jpg", "12〜2月", "花火之外，長岡的冬天", "酒藏・雪國的米與酒。給回訪派與「明年想去」的人一個冬天的理由。"),
        ("spring.jpg", "4月", "信濃川的春天", "同一條河的另一個季節。抽選期的嚮往，與「順便去長岡」的行程提案。")]
for i, (img, m, t, b) in enumerate(cont):
    x = 0.45 + i * 3.13
    photo(s, IMG(img), x, 1.6, 3.0, 2.6)
    d.label(s, x + 0.1, 3.82, 1.2, 0.28, m, PINK, WHITE, 8.5, radius=0.3)
    d.tx(s, x, 4.3, 3.0, 0.65, t, 12.5, NAVY, True, line=1.15)
    d.tx(s, x, 4.95, 3.0, 1.25, b, 10, INK, line=1.3)
bottom_bar(s, "KPI：8月以外的聲量 1,226,672 → 目標 1.5 倍（目標值）。全年聲量 ＋30％ 為保證。", y=6.3)

# ================================================================ SECTION 04 視覺
section("04", "視覺提案", "先研究現行視覺的 Knowhow，再決定長岡花火在台灣的「長相」。\nKV・Banner 皆以 Banaverse 生成素材＋正式字體排版製作。", IMG("poster_gold.jpg"))

# ---------------------------------------------------------------- 4-1 視覺研究
s = d.new("4-1. 視覺提案｜現行視覺的研究：什麼讓人停下來",
          "比較官方主視覺、日本各地花火大會海報、台灣 OTA・KOL 的視覺。三者的共通點是「黑夜×金」與「人」；差別在於，台灣人需要「看得懂的下一步」。",
          "研究對象：長岡花火チケットセンター官網・2026年海報（ひらけ、未来／みんなで守る長岡花火）、各地花火大會官方海報、KKday・Klook 商品頁、台灣 KOL 的 Reels 封面（2026年11月調查）。")
refs = [("官方主視覺", "長岡花火（日本）", ["黑底×金色的鳳凰・大玉，畫面 7 成是花火", "直書明朝體「長岡花火」，大量留白", "一句短文案（ひらけ、未来）", "官網色：可可棕＋桃紅＋薄荷的花火 logo"], "莊嚴・故事・品格", NIGHT),
        ("各地花火大會海報", "山形・安倍川・岡崎 等", ["浴衣人物的背影＋仰望的構圖", "書法・直書大字＋日期特大", "深藍夜空的漸層，多彩花火", "「守護」系海報：白底・極簡・人物背影"], "祭典感・人物・在地", BROWN),
        ("台灣 OTA・KOL", "KKday・Klook・Reels 封面", ["橫幅的「金色水平線」全景", "大字標題：「門票／價錢／交通／全攻略」", "情侶・朋友的背影＋手機畫面", "人潮與車站的「真實狀況」截圖"], "實用・資訊・真實感", PINK)]
for i, (t, sub, bl, kw, c) in enumerate(refs):
    x = 0.45 + i * 4.17
    d.rrect(s, x, 1.6, 4.05, 3.3, WHITE, LINE)
    d.rect(s, x, 1.6, 4.05, 0.55, c)
    d.tx(s, x + 0.15, 1.6, 2.6, 0.55, t, 12.5, WHITE, True, anchor="m")
    d.tx(s, x + 2.4, 1.6, 1.55, 0.55, sub, 7.5, "E6E9F2", align="r", anchor="m")
    for j, b in enumerate(bl):
        d.tx(s, x + 0.15, 2.28 + j * 0.5, 3.8, 0.48, "・" + b, 9.5, INK, line=1.1)
    d.label(s, x + 0.15, 4.4, 3.75, 0.32, "關鍵：" + kw, SOFT2, c, 9, radius=0.3)
d.tx(s, 0.45, 5.05, 4, 0.3, "→ 長岡花火・台灣版的設計原則", 11, NAVY, True)
pr = [("黑夜×金為主", "鳳凰金 #E8B84A／夜空 #0E1630"), ("桃紅是行動色", "官網桃紅 #EA336A 只用在按鈕・CTA"),
      ("直書明朝＝故事", "標題用明朝體，攻略用黑體"), ("一定有「人」", "台灣旅客的背影・笑臉，讓人代入"), ("一張圖一個行動", "嚮往／準備／守護，三種模板")]
for i, (t, b) in enumerate(pr):
    x = 0.45 + i * 2.5
    d.rrect(s, x, 5.4, 2.38, 1.35, SOFT, None)
    d.tx(s, x + 0.1, 5.47, 2.2, 0.32, t, 11, PINK if i == 1 else NAVY, True)
    d.tx(s, x + 0.1, 5.82, 2.2, 0.85, b, 8.5, INK, line=1.2)
for i, cc in enumerate([NIGHT, GOLD_L, PINK, BROWN, CREAM]):
    d.rect(s, 10.95 + i * 0.38, 5.07, 0.34, 0.22, cc, LINE)

# ---------------------------------------------------------------- 4-2 KV・Banner
s = d.new("4-2. 視覺提案｜KV 與 Banner 系列——三種模板",
          "「嚮往」用官方的黑金與直書；「準備」用攻略型大字；「守護」用白底極簡。同一套色彩與字體，在 Threads・IG・LP・廣告中統一使用。",
          "※ 所有畫面為示意（Banaverse 生成素材）。正式版使用官方提供的照片・logo，文案與規則經官方確認後發布。")
d.pic(s, PNG("bn_kv.png"), 0.45, 1.6, 3.4, 4.53)
d.pic(s, PNG("bn_newyear.png"), 4.05, 1.6, 2.9, 2.9)
d.pic(s, PNG("bn_manner.png"), 7.1, 1.6, 2.9, 2.9)
d.tx(s, 0.45, 6.17, 3.4, 0.3, "嚮往｜KV（直式海報・IG 4:5）", 9, NAVY, True, align="c")
d.tx(s, 4.05, 4.55, 2.9, 0.3, "嚮往｜1月 正三尺玉（1:1）", 9, NAVY, True, align="c")
d.tx(s, 7.1, 4.55, 2.9, 0.3, "守護｜安全・正規購票（1:1）", 9, NAVY, True, align="c")
d.pic(s, PNG("lp_phone.png"), 4.05, 4.95, 0.0001, 0.0001) if False else None
d.rrect(s, 4.05, 4.95, 5.95, 1.5, SOFT, None)
bullets(s, 4.2, 5.05, 5.7, [("文案：一張圖只講一件事", "「一生一次，留給這片夜空。」「新年，從一顆正三尺玉開始。」"),
                            ("字體：明朝＝故事、黑體＝資訊", "日期・CTA 用黑體，讓人一眼看懂下一步")], 9.5, 0.68, GOLD_T)
d.rrect(s, 10.2, 1.6, 2.7, 4.85, NIGHT, None)
d.tx(s, 10.35, 1.7, 2.4, 0.3, "製作方式", 11, GOLD_L, True)
bullets(s, 10.35, 2.15, 2.45, [("Pandora", "抓出當月的話題"), ("Banaverse", "生成情境素材"), ("正式排版", "官方字體・logo"), ("多尺寸輸出", "9:16・4:5・1:1・LP")], 9.5, 0.98, PINK, WHITE)

# ---------------------------------------------------------------- 4-3 Banner 淡季・情境
s = d.new("4-3. 視覺提案｜淡季 Banner 與廣告的情境",
          "同一個設計系統，延伸到淡季內容與廣告。抽選前（4〜6月）的廣告以「準備」模板為主，冬季以「長岡四季」模板維持嚮往。",
          "※ 所有畫面為示意（Banaverse 生成素材）。廣告媒體費另計。")
d.pic(s, PNG("bn_winter.png"), 0.45, 1.6, 7.4, 3.87)
d.tx(s, 0.45, 5.52, 7.4, 0.3, "長岡四季｜冬（Meta 廣告 1.91:1・LP 橫幅）", 9, NAVY, True, align="c")
photo(s, IMG("ta_yukata.jpg"), 8.05, 1.6, 4.85, 1.85)
photo(s, IMG("phone_taipei.jpg"), 8.05, 3.6, 4.85, 1.85)
d.tx(s, 8.05, 5.52, 4.85, 0.3, "Reels 封面・廣告素材的情境（AI示意）", 9, NAVY, True, align="c")
rule = [("1月", "正三尺玉 新年", GOLD_T), ("4〜6月", "抽選前「準備」", PINK), ("7〜8月", "散場「守護」", NAVY), ("12〜2月", "長岡四季", "2E9E6A")]
for i, (m, t, c) in enumerate(rule):
    x = 0.45 + i * 3.13
    d.rrect(s, x, 5.95, 3.0, 0.8, WHITE, c, lw=1.25)
    d.tx(s, x + 0.12, 5.95, 0.95, 0.8, m, 10, c, True, anchor="m")
    d.tx(s, x + 1.05, 5.95, 1.9, 0.8, t, 10.5, INK, True, anchor="m")

# ================================================================ SECTION 05
section("05", "KPI・方案・時程", "保證・目標值・承諾交付分開標示。\n施策期間：2026年12月〜2027年9月（10個月）", IMG("sanjaku.jpg"))

# ---------------------------------------------------------------- 5-1 效果測定
s = d.new("5-1. 效果測定｜Pandora 月次監測與即時通知",
          "以施策前的 Pandora 實測值為基準，每月分析台灣・香港的反應。負面話題（轉賣・詐騙・散場混雜）由 LINE 即時通知，官方帳號 24 小時內回應。",
          "※ 畫面為示意。數值為說明用，非預測。")
d.pic(s, PNG("dashboard.png"), 0.45, 1.6, 7.6, 3.47)
mon = [("聲量・話題", "月別聲量、平台、熱門話題、正負面"), ("施策別成效", "官方帳號・KOC・IG・GEO 的聲量與 UTM 流量"),
       ("AI 搜尋", "GEO 關鍵字在 AI 搜尋的顯示狀況"), ("即時通知", "關鍵字 4 組・24 小時監測・LINE 通報"), ("下月建議", "發文主題・KOC 發布時機的調整")]
bullets(s, 8.35, 1.7, 4.5, mon, 10, 0.72, NAVY)
d.rrect(s, 0.45, 5.25, 7.6, 1.5, SOFT2, None)
d.tx(s, 0.6, 5.3, 7.3, 0.3, "施策前基準值（Pandora 實測）", 10.5, NAVY, True)
base = [("4,770,013", "全年總聲量"), ("1,226,672", "8月以外的聲量"), ("2,669", "文章數"), ("18.3％", "IG 篇數占比")]
for i, (v, l) in enumerate(base):
    stat(s, 0.6 + i * 1.83, 5.65, 1.73, 1.0, v, l, NAVY, WHITE, 15)

# ---------------------------------------------------------------- 5-2 KPI
s = d.new("5-2. KPI 設計｜保證・目標值・承諾交付",
          "KPI 分三類寫入契約。聲量以 Pandora 實測值為基準保證 ＋30％；官方帳號的粉絲數等為依實績設定的目標值。",
          "※ 施策前的數值為 2026/10/26 時點的 Pandora 實測值（2025/10/27〜2026/10/26）。實施時以施策開始前一日的最新資料為基準值。以下為「推薦方案」的數值。")
cols3 = [("保證", "未達成時有退費／補發條款", RED, "FBECEA",
          [("聲量（全年）＋30％", "4,770,013 → 6,201,017（Pandora・台灣＋香港）"),
           ("Threads KOC（每篇）", "瀏覽 10,000+／互動 100+／聲量 1,000+\n未達成時免費補發"),
           ("GEO AI 搜尋命中", "30 組關鍵字中 3 組於 AI 搜尋有效顯示\n未達成退還該套金額 30％")]),
         ("目標值", "依實績設定的努力目標（非契約值）", NAVY, "EEF2FA",
          [("Threads 官方帳號粉絲", "10個月 8,000〜10,000 人"),
           ("平均互動率", "4％ 以上"),
           ("8月以外的聲量", "1,226,672 → 1.5 倍（1,840,000）"),
           ("IG UGC 觸及（參考值）", "每名 2,000〜5,000")]),
         ("承諾交付", "一定交付的數量與成果物", TEAL, "E9F6F6",
          [("Threads 官方帳號", "10個月・60 篇以上・留言回覆 30〜100 則／月"),
           ("KOC・IG UGC", "Threads KOC 6 篇／IG UGC 6 名"),
           ("GEO・繁中指南", "新聞 6・論壇 6・KW 30 組／LP 1 式"),
           ("月報", "Pandora 月報 10 本＋KV・Banner 1 式")])]
for i, (t, sub, c, bg, items) in enumerate(cols3):
    x = 0.45 + i * 4.17
    d.rect(s, x, 1.6, 4.05, 0.62, c)
    d.tx(s, x + 0.15, 1.6, 1.4, 0.62, t, 16, WHITE, True, anchor="m")
    d.tx(s, x + 1.45, 1.6, 2.5, 0.62, sub, 8.5, WHITE, anchor="m")
    d.rect(s, x, 2.22, 4.05, 4.53, bg)
    for j, (a, b) in enumerate(items):
        y = 2.35 + j * (4.3 / len(items))
        d.tx(s, x + 0.15, y, 3.8, 0.3, a, 11, c, True)
        d.tx(s, x + 0.15, y + 0.33, 3.8, 0.7, b, 9, INK, line=1.2)

# ---------------------------------------------------------------- 5-3 3方案
s = d.new("5-3. 方案與報價｜3個方案（2026年12月〜2027年9月・10個月）",
          "推薦「中方案」：在抽選前的決定期，同時布局官方帳號・KOC・GEO・繁中指南。金額為日圓・未稅，詳細見報價單（Excel）。",
          "※ 金額為日圓・未稅。廣告媒體費・KOC 體驗的交通住宿・觀覽席等實費另計。KV・Banner 製作為暫定單價。")
plans = [("小方案", "口碑基礎", "¥4,996,000", ["Pandora 月報・即時通知 10個月", "Threads 官方帳號 10個月", "Threads KOC 4 篇"], "先建立官方的繁中窗口與口碑", "8A93A6"),
         ("中方案（推薦）", "官方窗口＋決定期", "¥9,064,000", ["小方案的全部（KOC 6 篇）", "IG UGC 在日台灣人 KOC 6 名", "GEO 1 套（購票・觀覽席）", "繁中官方指南 LP", "KV・Banner 系列"], "抽選前就成為「被引用的官方」", PINK),
         ("大方案", "全年展開", "¥13,040,000", ["中方案的全部", "GEO 2 套（＋交通・散場・住宿）", "Threads KOC 10 篇・IG UGC 10 名", "Meta／Threads 廣告運用 6個月"], "認知到再訪，全年不留空白", NIGHT)]
for i, (n, sub, pr, items, aim, c) in enumerate(plans):
    x = 0.45 + i * 4.17
    rec = i == 1
    d.rrect(s, x, 1.6 + (0 if rec else 0.15), 4.05, 5.15 - (0 if rec else 0.15), WHITE, c, lw=2.0 if rec else 1.0)
    d.rect(s, x, 1.6 + (0 if rec else 0.15), 4.05, 0.62, c)
    d.tx(s, x + 0.15, 1.6 + (0 if rec else 0.15), 3.8, 0.62, [[(n + "　", {"size": 14}), (sub, {"size": 9, "bold": False})]], 12, WHITE, True, anchor="m")
    d.tx(s, x, 2.4, 4.05, 0.6, pr, 24, c if c != "8A93A6" else NAVY, True, align="c", font="Meiryo")
    d.tx(s, x, 2.98, 4.05, 0.28, "10個月・未稅", 8.5, GREY, align="c")
    for j, it in enumerate(items):
        d.tx(s, x + 0.25, 3.4 + j * 0.47, 3.65, 0.4, "✔ " + it, 11, INK)
    d.rrect(s, x + 0.15, 5.85, 3.75, 0.72, SOFT, None)
    d.tx(s, x + 0.25, 5.85, 3.55, 0.72, aim, 9.5, NAVY, True, anchor="m", align="c")
d.label(s, 4.62 + 2.6, 1.42, 1.2, 0.32, "RECOMMEND", GOLD_L, NIGHT, 8.5, radius=0.4)

# ---------------------------------------------------------------- 5-4 時程
s = d.new("5-4. 實施時程（2026年12月〜2027年9月）",
          "抽選前（4〜6月）是決定期，所有施策在此前就位。8月當天以安全與散場為主，9月起轉為回顧與淡季內容。",
          "※ 2027年的抽選日程依2026年實績（一般抽選 5/25〜6/8）推估，以官方公布為準。")
mm = ["12月", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月"]
GX, GW, GY = 2.75, 10.15, 1.6
cw = GW / 10
d.rect(s, GX, GY, GW, 0.3, NIGHT)
d.tx(s, GX, GY, cw, 0.3, "2026", 8, GOLD_L, True, align="c", anchor="m")
d.tx(s, GX + cw, GY, GW - cw, 0.3, "2027", 8, GOLD_L, True, align="c", anchor="m")
for i, m in enumerate(mm):
    d.rect(s, GX + i * cw, GY + 0.3, cw, 0.3, PINK if m in ("4月", "5月", "6月") else ("C0504D" if m == "8月" else NIGHT2), "FFFFFF", lw=0.5)
    d.tx(s, GX + i * cw, GY + 0.3, cw, 0.3, m, 8.5, WHITE, True, align="c", anchor="m")
gant = [("Pandora 監測・月報", 0, 10, "8A93A6", "基準值測定 → 月報・即時通知"),
        ("Threads 官方帳號", 0, 10, NAVY, "開設・故事發信 → 攻略 → 現場資訊 → 回顧"),
        ("Threads KOC", 1, 8, PINK, "①感動　②抽選・席種　③散場　④住宿　⑤長岡四季"),
        ("IG UGC（在日台灣人）", 1, 9, GOLD_T, "冬・春の長岡 ／ 8月 花火當天"),
        ("GEO（AI搜尋）", 1, 4, "2E9E6A", "購票・觀覽席　KW30・新聞6・論壇6"),
        ("繁中官方指南 LP", 1, 4, TEAL, "製作 → 4月上線 → 抽選資訊更新"),
        ("KV・Banner", 0, 3, BROWN, "設計系統 → 季節別 Banner"),
        ("安全・正規購票啟發", 4, 9, "C0504D", "抽選前 → 出發前 → 當天")]
for i, (t, a, b, c, note) in enumerate(gant):
    y = GY + 0.68 + i * 0.45
    d.rect(s, 0.45, y, 12.45, 0.41, WHITE if i % 2 == 0 else SOFT, None)
    d.tx(s, 0.5, y, 2.2, 0.44, t, 9, INK, True, anchor="m")
    d.rrect(s, GX + a * cw + 0.03, y + 0.07, (b - a) * cw - 0.06, 0.3, c, None, radius=0.3)
    d.tx(s, GX + a * cw + 0.1, y + 0.07, (b - a) * cw - 0.2, 0.3, note, 7.5, WHITE, True, anchor="m")
y = GY + 0.68 + len(gant) * 0.45 + 0.08
d.rect(s, 0.45, y, 12.45, 0.62, "FDECEF")
d.tx(s, 0.5, y, 2.2, 0.62, "主要時點", 9, PINK, True, anchor="m")
mk = [(1, "1/1 正三尺玉\n新年"), (4, "4月 抽選資訊\n公布（推估）"), (5, "5〜6月\n一般抽選"), (8, "8/2・8/3\n長岡花火"), (9, "9月 成果\n總結報告")]
for i, t in mk:
    x = GX + i * cw + cw / 2
    d.tx(s, x - 0.75, y + 0.02, 1.5, 0.6, "◆ " + t, 7.5, PINK, True, align="c", line=1.0)

# ---------------------------------------------------------------- 5-5 下一步
s = d.new("5-5. 今後的進行方式",
          "12月確定方案與支援範圍，1月開設官方帳號並啟動正三尺玉的新年內容；4月抽選資訊公布前，繁中官方指南上線。",
          "")
d.rect(s, 0.45, 1.6, 6.1, 0.45, NAVY)
d.tx(s, 0.6, 1.6, 5.9, 0.45, "想向貴單位確認的事項", 11, WHITE, True, anchor="m")
qs = [("目的與優先順序", "安全・正規購票／淡季集客／整體聲量，哪一項最優先"),
      ("官方名義的範圍", "繁中官方帳號・指南能否以官方名義（或官方認可）營運"),
      ("素材的使用", "官方照片・影片・logo 的授權範圍"),
      ("與 OTA・旅行社的關係", "連結・共同企劃的可能性"),
      ("2027年的販售日程", "抽選與海外販售的預定（可公開時點）"),
      ("預算與期間", "方案選擇、施策期間")]
for i, (t, b) in enumerate(qs):
    y = 2.12 + i * 0.6
    d.rect(s, 0.45, y, 6.1, 0.56, WHITE if i % 2 == 0 else "F3F6FB", LINE)
    d.tx(s, 0.55, y, 0.35, 0.56, str(i + 1), 11, PINK, True, anchor="m")
    d.tx(s, 0.95, y, 2.0, 0.56, t, 9.5, INK, True, anchor="m")
    d.tx(s, 3.0, y, 3.5, 0.56, b, 8.5, INK, anchor="m")
d.rect(s, 6.8, 1.6, 6.1, 0.45, TEAL)
d.tx(s, 6.95, 1.6, 5.9, 0.45, "本公司的對應事項", 11, WHITE, True, anchor="m")
ours = [("12月上旬", "方案確定後，提交詳細時程與 KOC 人選"), ("12月", "Pandora 施策前基準值報告"),
        ("12〜1月", "Threads 官方帳號開設・KV 設計系統"), ("1月", "正三尺玉 新年內容・GEO 啟動"),
        ("1〜3月", "繁中官方指南 LP 製作（4月上線）"), ("4月〜", "抽選前攻略・安全啟發・月報")]
for i, (t, b) in enumerate(ours):
    y = 2.12 + i * 0.6
    d.rect(s, 6.8, y, 6.1, 0.56, WHITE if i % 2 == 0 else "F3F6FB", LINE)
    d.tx(s, 6.9, y, 1.2, 0.56, t, 9.5, TEAL, True, anchor="m")
    d.tx(s, 8.1, y, 4.8, 0.56, b, 9, INK, anchor="m")
photo(s, IMG("phoenix_pano.jpg"), 0.45, 5.85, 12.45, 0.9, tag=False)
grad_rect(s, 0.45, 5.85, 12.45, 0.9, NIGHT, 0.85, 0.35)
d.tx(s, 0.65, 5.85, 12.1, 0.9, [[("一生一次的花火，變成一整年的長岡。", {"size": 16}), ("　準備好再來，8月以外也想起長岡。", {"size": 11, "color": GOLD_L})]], 12, WHITE, True, align="c", anchor="m")

# ================================================================ finish
d.move_to_end(thanks)
for sh in thanks.shapes:
    if sh.has_text_frame and sh.text_frame.text.strip().isdigit():
        runs = sh.text_frame.paragraphs[0].runs
        if runs:
            runs[0].text = str(d.page + 1)
d.save(OUT, animate=True)
print("saved", OUT, "slides:", len(d.prs.slides))
