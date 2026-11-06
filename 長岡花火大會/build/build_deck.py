# -*- coding: utf-8 -*-
"""長岡花火｜台灣市場 Inbound 推廣施策提案（繁中版）v2
base：PASONA 提出版（Intasect 母片）。沿用封面・公司概要・服務概要・領域③・章節頁・媒體生態系・THANK YOU（文字改繁中），
其餘頁面依 PASONA 的章節結構重新繪製。報價不放簡報（另附 Excel）。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = os.path.join(os.path.dirname(ROOT), "Pasona", "（提出）【PASONA】2026インバウンド集客ソリューション（台湾メイン）(1).pptx")
import json
JA = "--ja" in sys.argv
if JA:
    OUT = os.path.join(ROOT, "【XXX御中】長岡花火 台湾向けインバウンド集客のご提案202611.pptx")
    _trp = os.path.join(HERE, "i18n_ja.json")
    d = Deck(BASE, font="Meiryo", tr=json.load(open(_trp, encoding="utf-8")) if os.path.exists(_trp) else {})
else:
    OUT = os.path.join(ROOT, "【繁中版】長岡花火 台灣市場Inbound推廣施策提案202611_V.2.pptx")
    d = Deck(BASE)
KEEP = [0, 1, 2, 3, 4, 5, 6, 8, 19]
d.keep_only(set(KEEP))
S = list(d.prs.slides)
cover, company, service, domain3, sec1, p11, media, sec2, thanks = S

NIGHT, GOLD_T, GOLD_L, PINK, BROWN = "0E1630", "B07D1E", "E8B84A", "EA336A", "623632"
TNAVY, LEAD = "272673", "1F2740"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
IMG = lambda n: os.path.join(HERE, "img", n)
PNG = lambda n: os.path.join(HERE, "png", n)
PD = lambda n: os.path.join(HERE, "pandora", n)
SRC_V = "資料來源：Pandora by The Pocket Company／Accucrazy「長岡花火大會」言及量レポート（2025/10/27〜2026/10/26・台灣＋香港）"
SRC_I = "資料來源：Pandora「長岡花火大會」インサイトレポート（2025/10/27〜2026/10/26）"
FONT_ZH = "Meiryo" if JA else "Microsoft JhengHei"

# ---------------------------------------------------------------- 沿用頁的繁中化
TR = {
    "会社概要": "公司概要", "サービス概要": "服務概要", "会社名": "公司名稱", "本社所在地": "總公司地址", "代表者": "代表人",
    "設立": "成立", "資本金": "資本額", "地域拠点": "國內據點", "海外拠点": "海外據點", "従業員数": "員工人數",
    "WEBサイト": "官方網站", "主要取引先": "主要客戶",
    "インタセクト・コミュニケ－ションズ株式会社": "Intasect Communications 株式會社",
    "東京都千代田区神田小川町三丁目1番地 B・Mビル2階～6階": "東京都千代田區神田小川町三丁目1番地 B・M大樓 2〜6 樓",
    "代表取締役社長　譚 玉峰 (Tan Yufeng)": "代表取締役社長　譚 玉峰（Tan Yufeng）",
    "9,856万円": "9,856 萬日圓", "大阪・姫路・札幌・京都、沖縄(グループ会社)": "大阪・姬路・札幌・京都、沖繩（集團公司）",
    "中国 (長春・太原・北京・上海・成都・広州)": "中國（長春・太原・北京・上海・成都・廣州）",
    "グループ全体 951名 (2025年1月末 現在)": "集團整體 951 名（2025年1月底）",
    "システム\n開発": "系統\n開發", "企業\nイノベーション": "企業\n創新", "　決済・\nインバウンド\n総合支援": "支付・\nInbound\n綜合支援",
    "Web\nマーケティング支援": "Web\n行銷支援", "SIサービス事業\n(System Integration)": "SI 服務事業\n(System Integration)",
    "ERPソリューション事業": "ERP 解決方案事業", "健康情報工学": "健康資訊工學", "マネージメント\n支援サービス": "管理\n支援服務",
    "BPM\n（ビジネスプロセス管理）": "BPM\n（業務流程管理）", "社外との取引文書や\n申請書の電子化": "對外交易文件與\n申請書電子化",
    "ウォークスルー型\n無人店舗ソリューション": "Walk-through 型\n無人店鋪解決方案", "eateat\n(モバイルオーダーサービス)": "eateat\n（行動點餐服務）",
    "アフィリエイト広告運用": "聯盟行銷廣告運用", "アフィリエイト以外の広告": "其他廣告運用",
    "WebAegis\n(広告表記チェック)": "WebAegis\n（廣告標示檢查）", "PicInSite\n(画像検索導入支援)": "PicInSite\n（圖像搜尋導入支援）",
    "PIA\n(SNSモニタリング)": "PIA\n（社群監測）", "SECOND BRAIN\n(EC店舗分析ツール)": "SECOND BRAIN\n（EC 店鋪分析工具）",
    "POP-TURN\n(離脱防止ツール)": "POP-TURN\n（防跳出工具）", "Passton\n(添削・共有・指示ツール)": "Passton\n（批改・共享・指示工具）",
    "クリエイティブ・映像制作\nライブ配信": "創意・影像製作\n直播", "海外販路拡大支援\n（越境EC/一般貿易）": "海外通路拓展支援\n（跨境 EC／一般貿易）",
    "百度\n(中国最大の検索サイト)": "百度\n（中國最大搜尋網站）", "海外SNS施策": "海外社群施策", "インフルエンサー施策": "網紅施策",
    "台湾市場サポート": "台灣市場支援", "馬蜂窩[マーフォンウォー]\n(旅行情報媒体)": "馬蜂窩\n（旅遊資訊媒體）",
    "集客支援と旅先提案": "集客支援與旅遊提案", "領域③「決済・インバウンド総合支援」": "領域③「支付・Inbound 綜合支援」",
    "広告型": "廣告型", "共感・声量特化型": "共感・聲量特化型", "EC連動型": "EC 連動型",
    "1-2.台湾市場の特徴を攻略するメディア・エコシステム": "1-2. 攻略台灣市場的媒體生態系",
    "1.台湾市場の特徴と現状分析": "1. 台灣市場的特徵與現況分析",
    "台湾市場向けインバウンド集客施策": "2. 台灣市場 Inbound 集客施策",
    "株式会社パソナグループ　御中": "XXX　敬啟",
    "インタセクト・コミュニケーションズ株式会社": "Intasect Communications 株式會社",
}


def _font(r):
    r.font.name = FONT_ZH
    rPr = r._r.get_or_add_rPr()
    el = rPr.find(f"{{{A}}}ea")
    if el is None:
        el = etree.SubElement(rPr, f"{{{A}}}ea")
    el.set("typeface", FONT_ZH)


def tr_tf(tf):
    full = tf.text.replace("\x0b", "\n")
    hit = TR.get(full) or TR.get(full.strip())
    if hit is not None:
        lines = hit.split("\n")
        for i, p in enumerate(tf.paragraphs):
            for j, r in enumerate(p.runs):
                r.text = lines[i] if (i < len(lines) and j == 0) else ""
                _font(r)
        return
    for p in tf.paragraphs:
        key = "".join(r.text for r in p.runs).replace("\x0b", "\n")
        hit = TR.get(key) or TR.get(key.strip())
        if hit and p.runs:
            p.runs[0].text = hit
            _font(p.runs[0])
            for r in p.runs[1:]:
                r.text = ""


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == 6:
            walk(sh.shapes)
        if sh.has_text_frame:
            tr_tf(sh.text_frame)
        if getattr(sh, "has_table", False) and sh.has_table:
            for row in sh.table.rows:
                for c in row.cells:
                    tr_tf(c.text_frame)
                    for p in c.text_frame.paragraphs:
                        for r in p.runs:
                            if "その他日本全国の自治体・DMO・観光協会等" in r.text:
                                r.text = r.text.replace("その他日本全国の自治体・DMO・観光協会等", "其他日本全國自治體・DMO・觀光協會等")


if JA:
    TR = {"台湾市場向けインバウンド集客施策": "台湾市場向けインバウンド集客施策", "株式会社パソナグループ　御中": "XXX　御中"}
for sl in (cover, company, service, domain3, sec1, media, sec2):
    walk(sl.shapes)

for sh in cover.shapes:
    if sh.has_text_frame and "インバウンドプロモーション" in sh.text_frame.text:
        runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
        runs[0].text = d.T("長岡花火｜台灣市場 Inbound 推廣施策提案")
        _font(runs[0])
        for r in runs[1:]:
            r.text = ""
d.tx(cover, 1.89, 4.15, 10.36, 0.45, "2026年11月", 16, "000000", True, align="c", font=FONT_ZH)
d.tx(cover, 1.89, 4.65, 10.36, 0.45, "一生一次的花火，讓更多台灣人知道、想去、去得成。", 13, TNAVY, True, align="c", font=FONT_ZH)

# ---------------------------------------------------------------- helpers
LAYOUT = d.prs.slide_layouts[1]  # タイトルとコンテンツ（confidential 帶）


def page(title, lead=None, src=None):
    s = d.prs.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    d.tx(s, 0.0, 0.13, 10.6, 0.49, title, 24, TNAVY, True, anchor="m", font=FONT_ZH)
    if lead:
        d.tx(s, 0.45, 0.72, 12.4, 0.62, lead, 13, LEAD, True, font=FONT_ZH, line=1.2)
    if src:
        d.tx(s, 0.45, 6.82, 12.4, 0.26, src, 7.5, GREY, font=FONT_ZH)
    return s


def ai(s, x, y, text="AI示意"):
    return d.label(s, x, y, 0.62, 0.2, text, "333333", size=7, bold=False, radius=0.15)


def photo(s, path, x, y, w, h, tag=True, mode="cover"):
    p = d.pic(s, path, x, y, w, h, mode=mode)
    if tag:
        ai(s, x + 0.08, y + 0.08)
    return p


def shot(s, path, x, y, w, h, mode="fit"):
    d.rect(s, x, y, w, h, WHITE, LINE, lw=0.75)
    return d.pic(s, path, x + 0.05, y + 0.05, w - 0.1, h - 0.1, mode=mode)


def grad_rect(s, x, y, w, h, color, a_from, a_to, angle=0):
    sh = d.rect(s, x, y, w, h, color)
    spPr = sh.fill._xPr
    for c in list(spPr):
        if c.tag == f"{{{A}}}solidFill":
            spPr.remove(c)
    xml = f'''<a:gradFill xmlns:a="{A}" rotWithShape="1"><a:gsLst>
<a:gs pos="0"><a:srgbClr val="{color}"><a:alpha val="{int(a_from*100000)}"/></a:srgbClr></a:gs>
<a:gs pos="100000"><a:srgbClr val="{color}"><a:alpha val="{int(a_to*100000)}"/></a:srgbClr></a:gs>
</a:gsLst><a:lin ang="{angle*60000}" scaled="0"/></a:gradFill>'''
    spPr.find(f"{{{A}}}prstGeom").addnext(etree.fromstring(xml))
    return sh


def head(s, x, y, w, text, color=TNAVY, size=12):
    d.rect(s, x, y + 0.05, 0.07, 0.26, color)
    d.tx(s, x + 0.15, y, w - 0.15, 0.36, text, size, color, True, anchor="m", font=FONT_ZH)


def card(s, x, y, w, h, title, body, color=TNAVY, size=9.5, tsize=12):
    d.rrect(s, x, y, w, h, WHITE, LINE, radius=0.05)
    d.rect(s, x, y, w, 0.06, color)
    d.tx(s, x + 0.15, y + 0.15, w - 0.3, 0.36, title, tsize, color, True, font=FONT_ZH)
    d.tx(s, x + 0.15, y + 0.55, w - 0.3, h - 0.65, body, size, INK, font=FONT_ZH, line=1.3)


def msgbar(s, text, y=6.3, h=0.46):
    d.rrect(s, 0.45, y, 12.45, h, TNAVY, None, radius=0.1)
    d.tx(s, 0.65, y, 12.1, h, text, 12, WHITE, True, anchor="m", font=FONT_ZH)


# ================================================================ 1-1 台灣消費者（沿用頁改寫）
s = p11
for sh in list(s.shapes):
    if sh.has_text_frame and "1-1." in sh.text_frame.text:
        rs = [r for p in sh.text_frame.paragraphs for r in p.runs]
        rs[0].text = d.T("1-1. 台灣消費者的行動特徵")
        _font(rs[0])
        for r in rs[1:]:
            r.text = ""
    elif sh.has_text_frame:
        sh._element.getparent().remove(sh._element)
d.tx(s, 0.45, 0.75, 7.6, 0.85, ["2025年訪日台灣旅客達 676萬3,400人，年增約 12％。", "月均 56 萬人以上造訪日本，台灣人出國目的地第 1 名是日本。"], 13, "000000", True, font=FONT_ZH, line=1.3)
d.tx(s, 0.45, 1.75, 7.6, 0.4, "【台灣獨有的市場特徵與消費者心理】", 13, "000000", True, font=FONT_ZH)
pts = [("先被感動，再出發", "不會因一支廣告就決定。IG Reels・Threads 上「過來人」的現場影片與體驗談，是旅行的起點。"),
       ("反覆比較、查證才安心", "部落客與論壇文化深植，會在 Threads・Dcard・PTT 反覆確認攻略，取得「確信」後才行動。"),
       ("自由行（FIT）為主流", "出發前就列好「在日本要看什麼、玩什麼」的清單。勝負在出發前 2〜6 個月就已決定。")]
for i, (t, b) in enumerate(pts):
    y = 2.25 + i * 1.12
    d.circle(s, 0.5, y + 0.03, 0.42, str(i + 1), TNAVY, 12)
    d.tx(s, 1.05, y, 6.9, 0.35, t, 13, TNAVY, True, font=FONT_ZH)
    d.tx(s, 1.05, y + 0.38, 6.9, 0.7, b, 10.5, INK, font=FONT_ZH, line=1.3)
d.rrect(s, 0.45, 5.6, 7.6, 1.1, "FDF3DC", None)
d.tx(s, 0.65, 5.65, 7.3, 1.0, [[("長岡花火也是同樣的路徑　", {"color": GOLD_T, "size": 11})],
                                "IG Reels 點燃嚮往 →「有沒有去過的朋朋分享攻略？」在 Threads 發問 → 抽選・報團・訂住宿。這條路徑上的每個接觸點，都是讓更多台灣人前往的機會。"],
     10, INK, True, font=FONT_ZH, line=1.3)
photo(s, IMG("phone_taipei.jpg"), 8.3, 0.95, 4.65, 5.75)
grad_rect(s, 8.3, 4.5, 4.65, 2.2, NIGHT, 0.0, 0.88, angle=90)
d.tx(s, 8.5, 5.45, 4.3, 1.2, "晚上 11 點，台北的沙發上，\n一支 Reels 決定了明年夏天。", 13, WHITE, True, font=FONT_ZH, line=1.3)

# ================================================================ 1-3 聲量分析①
p13 = s = page("1-3. 現況分析①｜長岡花火在台灣的聲量",
               "一年 2,669 篇、總聲量 477 萬。台灣人很愛長岡花火——但聲量的 74％ 集中在 8 月，其餘 11 個月幾乎沒有人談。",
               SRC_V)
head(s, 0.45, 1.45, 6.2, "過去一年的基本數據（2025/10/27〜2026/10/26）")
shot(s, PD("v_stats.png"), 0.45, 1.85, 6.2, 2.0)
head(s, 0.45, 4.0, 6.2, "平台分布：Threads 80.7％・Instagram 18.3％")
shot(s, PD("v_platform.png"), 0.45, 4.4, 4.3, 2.23)
d.pic(s, PD("qr_volume.png"), 4.95, 4.45, 0.82, 0.82)
d.tx(s, 5.8, 4.45, 0.95, 0.82, "聲量\n報告", 8.5, GREY, True, anchor="m", font=FONT_ZH)
d.pic(s, PD("qr_insight.png"), 4.95, 5.4, 0.82, 0.82)
d.tx(s, 5.8, 5.4, 0.95, 0.82, "洞察\n報告", 8.5, GREY, True, anchor="m", font=FONT_ZH)
d.tx(s, 4.9, 6.25, 1.9, 0.4, "可用 Google 翻譯閱讀", 7, GREY, font=FONT_ZH)
head(s, 6.95, 1.45, 6.0, "聲量趨勢（月別）")
shot(s, PD("v_trend.png"), 6.95, 1.85, 5.95, 2.95)
d.rrect(s, 6.95, 4.95, 5.95, 1.68, "EEF2FA", None)
d.tx(s, 7.1, 5.0, 5.7, 1.6, [[("讀法　", {"color": PINK, "size": 11})],
                              "・8月＝3,543,341（全年的 74.3％）：開催當下的感動分享",
                              "・1月＝27.5萬：「正三尺玉」影片只有 11 篇就引爆",
                              "・3〜7月：抽選・旅行團・交通攻略的討論持續成長",
                              "・10〜12月：幾乎為零——這段時間沒有人在講長岡"], 9.5, INK, True, font=FONT_ZH, line=1.3)
d.tx(s, 0.45, 6.66, 6.2, 0.18, "※ 聲量（Volume）＝貼文數・讚・留言等使用者反應的總和（10＋讚×3＋留言×5）", 6.5, GREY, font=FONT_ZH)

# ================================================================ 1-4 聲量分析②
p14 = s = page("1-4. 現況分析②｜台灣人怎麼談長岡花火（正面）",
               "正面評價 84.2％。「一生一次」「看到哭了」——聲量最高的貼文，全是 IG 上的現場感動影片。",
               SRC_I + "／" + SRC_V.replace("資料來源：", "") + "。貼文畫面截取自 Instagram 公開貼文。")
head(s, 0.45, 1.45, 3.9, "情緒分布：正面 84.2％")
shot(s, PD("n_senti.png"), 0.45, 1.85, 3.9, 2.15)
head(s, 0.45, 4.15, 3.9, "關鍵字：花火・鳳凰・三尺玉・感動")
shot(s, PD("n_tree.png"), 0.45, 4.55, 3.9, 2.2)
head(s, 4.55, 1.45, 5.6, "聲量 Top 貼文：IG 的感動影片", PINK)
igs = [("ig1.png", "聲量 53.9萬｜♡17.8萬"), ("ig2.png", "聲量 30.8萬｜♡10.2萬"), ("ig3.png", "聲量 25.3萬｜♡8.3萬"), ("ig4.png", "聲量 11.2萬｜♡3.7萬")]
for i, (f, cap) in enumerate(igs):
    x = 4.55 + (i % 2) * 2.83
    y = 1.85 + (i // 2) * 2.48
    d.rect(s, x, y, 2.73, 2.2, "111111", None)
    d.pic(s, os.path.join(HERE, "ig", f), x + 0.02, y + 0.02, 2.69, 2.16)
    d.label(s, x, y + 2.22, 2.73, 0.22, f"#{i+1}　" + cap, NIGHT, WHITE, 8, radius=0.1)
head(s, 10.35, 1.45, 2.6, "2 個發現", TNAVY)
finds = [("感動是最強的內容", "鳳凰・黃金雨・白菊・正三尺玉，加上戰災復興的故事。「傳給想一起去的人」讓影片持續擴散。"),
         ("IG 擴散、Threads 查證", "IG 只占 18.3％ 篇數，卻拿下 68％ 的互動；Threads 則是「怎麼搶票・怎麼去」的發問與攻略。")]
for i, (t, b) in enumerate(finds):
    y = 1.9 + i * 2.45
    d.rrect(s, 10.35, y, 2.6, 2.3, "F5F7FB", None)
    d.tx(s, 10.48, y + 0.1, 2.4, 0.6, f"{i+1}. " + t, 11, TNAVY, True, font=FONT_ZH, line=1.15)
    d.tx(s, 10.48, y + 0.75, 2.4, 1.5, b, 9, INK, font=FONT_ZH, line=1.35)

# ================================================================ 1-5 聲量分析③（負面）
p15 = s = page("1-5. 現況分析③｜熱情背後，沒有被回答的「不安」",
               "負面只占 8.8％，卻集中在「去不去得成」：搶不到票、訂不到房、散場回不去。87.9萬人看過的求救文、「這輩子再也不去」——官方不在場，不安就會擴散。",
               SRC_I + "（センチメント分析・キーワード分析）。貼文畫面截取自 Threads 公開貼文（瀏覽數為截取時點）。")
head(s, 0.45, 1.5, 4.6, "Pandora：負面評價的分析", RED)
shot(s, PD("n_neg.png"), 0.45, 1.9, 4.6, 1.62)
kw = [("車站", 135), ("飯店", 112), ("回程", 92), ("散場", 87), ("人潮", 76)]
d.tx(s, 0.45, 3.65, 4.6, 0.3, "反覆出現的不安關鍵字（篇數）", 10, RED, True, font=FONT_ZH)
for i, (k, n) in enumerate(kw):
    y = 4.0 + i * 0.4
    d.tx(s, 0.45, y, 0.7, 0.34, k, 10, INK, True, anchor="m", font=FONT_ZH)
    d.rect(s, 1.15, y + 0.07, 3.2 * n / 135, 0.22, RED)
    d.tx(s, 1.2 + 3.2 * n / 135, y, 0.6, 0.34, f"{n}篇", 9, RED, True, anchor="m", font=FONT_ZH)
d.rrect(s, 0.45, 6.05, 4.6, 0.7, "FBECEA", None)
d.tx(s, 0.6, 6.05, 4.35, 0.7, "負面 8.8％＝非常負面 0.7％＋負面 8.1％（全 2,669 篇）", 9.5, RED, True, anchor="m", font=FONT_ZH)
ths = [("th2.png", "87.9萬 瀏覽・732 則留言", "「有沒有人分享搶票跟住宿攻略？值得去嗎？」"),
       ("th1.png", "17.7萬 瀏覽", "「120多人擠不上末班新幹線，露宿體育館」「這輩子再也不去」"),
       ("th3.png", "7.0萬 瀏覽", "「一查飯店／入場券價格就直接放棄⋯」")]
for i, (f, v, q) in enumerate(ths):
    x = 5.25 + i * 2.58
    d.rect(s, x, 1.5, 2.48, 2.84, "101010", None)
    d.pic(s, os.path.join(HERE, "ig", f), x + 0.02, 1.52, 2.44, 2.8, mode="cover")
    d.label(s, x, 4.38, 2.48, 0.28, v, RED, WHITE, 8.5, radius=0.1)
    d.tx(s, x, 4.7, 2.48, 0.85, q, 9, INK, True, font=FONT_ZH, line=1.25)
d.rrect(s, 5.25, 5.6, 7.65, 1.15, TNAVY, None)
d.tx(s, 5.45, 5.6, 7.3, 1.15, [[("痛點　", {"color": GOLD_L, "size": 12})],
                                "這些問題現在由網友各自回答，官方的繁中聲音不在場。「想去卻沒去」的台灣人，就停在這裡——這正是官方帳號與 KOC 要接住的地方。"],
     10.5, WHITE, True, anchor="m", font=FONT_ZH, line=1.35)

# ================================================================ 2-0 提案概念
p20 = s = page("2-0. 提案概念｜讓更多台灣人知道、想去、去得成", None, "※ 圖為 AI 示意（Banaverse 生成）。")
photo(s, IMG("phoenix_pano.jpg"), 0.45, 0.85, 12.45, 2.9)
grad_rect(s, 0.45, 0.85, 7.5, 2.9, NIGHT, 0.88, 0.0)
d.tx(s, 0.8, 1.12, 7.0, 0.35, "KEY CONCEPT", 11, GOLD_L, True, font="Georgia")
d.tx(s, 0.8, 1.48, 7.2, 1.2, "一生一次的花火，\n從台灣人的手機開始。", 28, WHITE, True, font="Hiragino Mincho ProN", line=1.15)
d.tx(s, 0.8, 2.85, 6.8, 0.75, "把「看到哭了」的感動，送到還不認識長岡的台灣人手上；\n再用攻略與行程，把「想去」變成「去得成」。", 11, "E6E9F2", font=FONT_ZH, line=1.3)
pil = [("STEP 1", "讓更多人知道", "認知擴大", ["IG Reels・旅遊 KOC・在日台灣人 KOC", "雄獅×欣傳媒 專訪文章＋社群", "1月「正三尺玉」新年話題"], "2-4・2-6・2-7", PINK, "ta_yukata.jpg"),
       ("STEP 2", "讓人想去", "興趣・查證", ["Threads 繁中官方帳號", "Threads KOC 攻略文", "GEO（AI 搜尋）＋繁中官方指南"], "2-3・2-5", TNAVY, "ta_family.jpg"),
       ("STEP 3", "讓人去得成", "預約・行動", ["雄獅旅遊的觀覽席行程", "抽選前・訪日中的廣告", "季節別 Banner"], "2-6・2-8・2-9", GOLD_T, "bus.jpg")]
for i, (st, t, sub, items, ref, c, img) in enumerate(pil):
    x = 0.45 + i * 4.17
    d.rrect(s, x, 3.95, 4.05, 2.75, WHITE, c, lw=1.25, radius=0.05)
    photo(s, IMG(img), x + 0.12, 4.07, 1.3, 2.5, tag=False)
    d.label(s, x + 1.55, 4.1, 0.8, 0.26, st, c, WHITE, 8, radius=0.3)
    d.tx(s, x + 2.4, 4.06, 1.6, 0.32, sub, 9, GREY, True, font=FONT_ZH)
    d.tx(s, x + 1.55, 4.42, 2.45, 0.42, t, 15, c, True, font=FONT_ZH)
    for j, it in enumerate(items):
        d.tx(s, x + 1.55, 4.92 + j * 0.42, 2.45, 0.4, "・" + it, 9, INK, font=FONT_ZH, line=1.05)
    d.tx(s, x + 1.55, 6.3, 2.4, 0.3, "→ " + ref, 8, c, True, font=FONT_ZH)

# ================================================================ 2-1 全體像（漏斗）
p2f = s = page("2-1. 集客施策｜全體像",
               "認知（嚮往）→ 興趣・查證 → 預約・行動 → 分享・再訪。所有施策都導向繁中官方指南與雄獅行程，成效以 Pandora 聲量與 UTM 衡量。",
               "※ 施策組合依方案調整（詳見報價單）。")
layers = [("認知・嚮往", "IG Reels・旅遊 KOC ／ 雄獅×欣傳媒 專訪＋社群", "讓「還不知道長岡」的台灣人看見感動", PINK),
          ("興趣・查證", "Threads 官方帳號 ／ Threads KOC ／ GEO（AI 搜尋）", "「怎麼搶票・怎麼去」被問到時，答案是官方", TNAVY),
          ("預約・行動", "繁中官方指南 ／ 雄獅觀覽席行程 ／ 廣告", "抽選日程・席種・一日遊，把想去變成訂得到", GOLD_T),
          ("分享・再訪", "KOC・UGC 二次利用 ／ 白菊・長岡四季", "8月以外也被想起，接到下一年", "2E9E6A")]
for i, (t, a_, b_, c) in enumerate(layers):
    y = 1.5 + i * 1.08
    W = 8.4 - i * 1.25
    X = 0.45 + i * 0.625
    d.poly(s, [(X, y), (X + W, y), (X + W - 0.62, y + 0.98), (X + 0.62, y + 0.98)], c)
    d.tx(s, X + 0.6, y + 0.06, W - 1.2, 0.38, t, 14, WHITE, True, align="c", font=FONT_ZH)
    d.tx(s, X + 0.6, y + 0.46, W - 1.2, 0.48, a_, 9.5, WHITE, align="c", font=FONT_ZH)
    d.hline(s, X + W - 0.3, y + 0.49, 9.05, y + 0.49, "B8C4D6", 1, dash=True)
    d.rrect(s, 9.05, y + 0.12, 3.85, 0.76, WHITE, c, lw=1.25)
    d.tx(s, 9.18, y + 0.12, 3.6, 0.76, b_, 10, INK, True, anchor="m", font=FONT_ZH)
d.rrect(s, 0.45, 5.9, 12.45, 0.85, "EEF2FA", None)
d.tx(s, 0.65, 5.9, 2.2, 0.85, "Pandora\n月次監測", 12, TNAVY, True, anchor="m", font=FONT_ZH)
d.tx(s, 2.8, 5.9, 10.0, 0.85, "施策前基準值（總聲量 4,770,013）→ 月別聲量・正負面・話題。負面（轉賣・散場等）即時通知，官方帳號與 KOC 立即回應。", 10, INK, anchor="m", font=FONT_ZH, line=1.3)

# ================================================================ 2-2 KOC 的定義（沿用 Hakuba 金字塔頁的圖形）
import copy as _copy
from pptx import Presentation as _P
_HK = _P(os.path.join(os.path.dirname(ROOT), "白馬谷Hakuba Valley", "【株式会社岩岳リゾート御中】Hakuba Valley 台湾向けインバウンド集客のご提案202610.pptx" if JA else "【中文版】Hakuba Valley 繁體中文市場集客策略提案202610.pptx"))
pkoc = s = page("2-2. KOC 的定義｜台灣資訊發布者的結構",
                "在台灣，發文者的規模決定了觸及範圍與消費者的距離感。本提案的口碑施策全部以「KOC」執行——粉絲 10 萬以下、貼近旅客視角的發布者。",
                None)
for sh in _HK.slides[6].shapes:
    if sh.name in ("TextBox 1", "TextBox 2", "TextBox 63"):
        continue
    s.shapes._spTree.append(_copy.deepcopy(sh._element))
_T = {"TextBox 51": "微網紅・旅遊 KOC。以旅客的視角拍攝花火現場，擴大「想去」。→ 本提案：旅遊 KOC（花火當天同行）",
      "TextBox 55": "在日台灣人・一般旅客的 KOC。攻略與體驗談，是搜尋・比較時的依據。→ 本提案：Threads KOC・IG KOC",
      "TextBox 62": "※ 各層級區分為本公司實務上的參考標準。橘色為本提案定義的 KOC（粉絲 10 萬以下）。",
      "Rounded Rectangle 61": "本提案的 KOC\n粉絲 10萬以下"}
for sh in s.shapes:
    if sh.name in _T and sh.has_text_frame:
        lines = d.T(_T[sh.name]).split("\n")
        ps = sh.text_frame.paragraphs
        for i, pp in enumerate(ps):
            for j, r in enumerate(pp.runs):
                r.text = lines[i] if (i < len(lines) and j == 0) else ""
    if sh.name == "Rounded Rectangle 57":
        sh.top = int(3.86 * 914400)
        sh.height = int(2.46 * 914400)
    if sh.name in ("TextBox 51", "TextBox 55"):
        sh.width = int(4.55 * 914400)
        sh.height = int(0.75 * 914400)

# ================================================================ 2-1 聲量對策 Threads
p21 = s = page("2-3. 聲量對策｜Threads 繁中官方帳號 × Threads KOC",
               "台灣人實際「找資訊的地方」是 Threads。長岡花火的討論 80.7％ 在這裡——官方帳號說故事，KOC 寫攻略。",
               "資料來源：Similarweb・Meta 公開資料／" + SRC_V.replace("資料來源：", "") + "。畫面為示意。所有 KOC 貼文標示「合作」。")
card(s, 0.45, 1.45, 6.1, 2.4, "Threads 繁中官方帳號「長岡花火 繁中官方（暫稱）」",
     ["・台灣是 Threads 全球最大市場；長岡花火貼文 2,155 篇（80.7％）在 Threads",
      "・發信內容：白菊・鳳凰・正三尺玉的故事／抽選日程／席種與行程",
      "・每月 6 篇以上，抽選前（3〜6月）與 7〜8 月加碼；留言回覆 30〜100 則／月",
      "・成為台灣人「問長岡」的正式窗口，詳細資訊導向繁中官方指南"], TNAVY, 10.5)
card(s, 6.8, 1.45, 6.1, 2.4, "Threads KOC 成果保證型（粉絲 3,000＋）",
     ["・以「過來人」的語氣，回答台灣人真正在問的問題",
      "・5 個切角：①一生一次的理由 ②抽選・席種 ③住宿與交通 ④東京出發一日遊 ⑤花火以外的長岡",
      "・每篇保證：瀏覽 10,000＋／互動 100＋／聲量 1,000＋（未達成免費補發）",
      "・原稿事先經官方確認，一律標示「合作」"], PINK, 10.5)
d.pic(s, PNG("threads_official.png"), 0.6, 4.0, 1.38, 2.78)
photo(s, IMG("phoenix_pano.jpg"), 2.15, 4.0, 2.15, 1.32)
photo(s, IMG("shiragiku.jpg"), 2.15, 5.46, 2.15, 1.32, tag=False)
photo(s, IMG("sanjaku.jpg"), 4.4, 4.0, 2.15, 2.78, tag=False)
d.pic(s, PNG("threads_koc.png"), 6.95, 4.0, 1.38, 2.78)
photo(s, IMG("koc_film.jpg"), 8.5, 4.0, 2.15, 2.78)
photo(s, IMG("masu.jpg"), 10.75, 4.0, 2.15, 1.32, tag=False)
photo(s, IMG("winter_sake.jpg"), 10.75, 5.46, 2.15, 1.32, tag=False)

# ================================================================ 2-2 IG・KOC
p22 = s = page("2-4. 認知擴大｜Instagram Reels × 旅遊 KOC",
               "IG 只占 18.3％ 的篇數，卻拿下 68％ 的互動。「看到哭了」的 Reels，是把長岡帶給新的台灣人最快的方法。",
               SRC_V + "。IG KOC 觸及為參考值（粉絲 5,000〜10,000，單篇約 2,000〜5,000）。畫面為示意。")
d.pic(s, PNG("ig_reel.png"), 0.45, 1.45, 2.65, 5.32)
photo(s, IMG("ta_yukata.jpg"), 3.3, 1.45, 3.1, 2.55)
photo(s, IMG("koc_film.jpg"), 6.55, 1.45, 3.1, 2.55, tag=False)
d.tx(s, 3.3, 4.03, 3.1, 0.28, "浴衣・自拍・「傳給想一起去的人」", 8.5, TNAVY, True, align="c", font=FONT_ZH)
d.tx(s, 6.55, 4.03, 3.1, 0.28, "開場前的現場・「怎麼去、坐哪」", 8.5, TNAVY, True, align="c", font=FONT_ZH)
card(s, 3.3, 4.4, 3.1, 2.35, "旅遊 KOC（粉絲 1〜10萬）",
     ["・旅遊・攝影類 KOC", "・花火當天同行：Reels 1 本＋限時動態 2 本＋Threads 1 篇", "・觸及「還不知道長岡」的新族群"], PINK, 10)
card(s, 6.55, 4.4, 3.1, 2.35, "在日台灣人 IG KOC（粉絲 5,000〜1萬）",
     ["・粉絲 5,000〜10,000 的微型 KOC", "・8月當天＋冬・春的長岡（淡季也有內容）", "・素材授權給官方帳號・廣告二次利用"], TNAVY, 10)
d.rrect(s, 9.85, 1.45, 3.05, 5.3, NIGHT, None)
d.tx(s, 10.0, 1.55, 2.8, 0.32, "IG 的數字", 11, GOLD_L, True, font=FONT_ZH)
for i, (v, l) in enumerate([("489 篇", "IG 篇數（18.3％）"), ("105.6 萬", "IG 互動（讚＋留言）"), ("53.9 萬", "Top 貼文的聲量（IG Reels）")]):
    y = 1.98 + i * 1.05
    d.tx(s, 10.0, y, 2.8, 0.5, v, 22, WHITE, True, font="Meiryo")
    d.tx(s, 10.0, y + 0.52, 2.8, 0.3, l, 8.5, "C9D2E8", font=FONT_ZH)
d.hline(s, 10.0, 5.2, 12.75, 5.2, "3A4670", 1)
d.tx(s, 10.0, 5.3, 2.8, 1.35, "台灣人的固定句型：\n「傳給你想一起去的人」\n——嚮往，是靠分享擴散的。", 9.5, WHITE, True, font=FONT_ZH, line=1.35)

# ================================================================ 2-3 GEO
p23 = s = page("2-5. GEO 對策｜AI 搜尋 × 繁中官方指南",
               "台灣旅客越來越常用 ChatGPT・Google AI 查「長岡花火怎麼去」。新聞・論壇文章與繁中官方指南，讓 AI 回答時引用官方。",
               "※ 畫面為示意。GEO 保證：每套 30 組關鍵字中 3 組於 AI 搜尋結果有效顯示，未達成退還該套金額 30％。")
d.rrect(s, 0.45, 1.45, 6.2, 1.2, WHITE, TNAVY, lw=1.0)
d.tx(s, 0.6, 1.5, 5.95, 1.1, ["【AI 搜尋時代的新集客策略：GEO】", "・ChatGPT・Gemini・Google AI 概覽的使用快速增加", "・從「搜尋→看網站」變成「AI 直接給答案」——被 AI 引用的資訊才會被看見"], 9.5, INK, True, font=FONT_ZH, line=1.3)
d.pic(s, PNG("ai_search.png"), 0.45, 2.8, 6.2, 2.79)
kw = [("SET①", "認知・行程", "長岡花火 是什麼／日本三大花火／長岡花火 一日遊 東京出發／日本花火大會 推薦", PINK),
      ("SET②", "購票・交通", "長岡花火 門票 怎麼買／抽選 海外／旅行團 推薦／住宿 新潟／回程 新幹線", TNAVY)]
for i, (k, t, b, c) in enumerate(kw):
    y = 5.72 + i * 0.52
    d.label(s, 0.45, y + 0.06, 0.7, 0.3, k, c, WHITE, 8.5, radius=0.3)
    d.tx(s, 1.25, y, 1.2, 0.42, t, 10, c, True, anchor="m", font=FONT_ZH)
    d.tx(s, 2.4, y, 4.3, 0.42, b, 8, INK, anchor="m", font=FONT_ZH)
head(s, 6.9, 1.45, 6.0, "繁中官方指南（LP）＝AI 與 KOC 引用的「正確答案」")
d.pic(s, PNG("lp_pc.png"), 6.9, 1.9, 6.0, 3.46)
flow = [("新聞 6 本", "Yahoo奇摩新聞等保證刊登＋聯播"), ("論壇文 6 本", "Dcard・PTT・Mobile01"), ("KW 30 組", "依 Pandora 的提問設計"), ("AI 命中 3 組", "保證（未達退 30％）")]
for i, (t, b) in enumerate(flow):
    x = 6.9 + i * 1.52
    d.rrect(s, x, 5.5, 1.42, 1.25, "EEF2FA", None)
    d.tx(s, x + 0.08, 5.55, 1.3, 0.35, t, 10.5, TNAVY, True, font=FONT_ZH)
    d.tx(s, x + 0.08, 5.92, 1.3, 0.8, b, 8, INK, font=FONT_ZH, line=1.2)

# ================================================================ 2-6 雄獅×欣傳媒
p24 = s = page("2-6. 雄獅 × 欣傳媒｜專訪文章＋社群，把長岡帶給想去日本的讀者",
               "以雄獅集團旗下的旅遊媒體「欣傳媒」專訪長岡花火，並透過欣傳媒社群擴散。文章直接連結雄獅的觀覽席行程——從「知道」到「訂得到」一次完成。",
               "資料來源：欣傳媒「泛雄獅資源2026（日本線）」媒體資料（含 Similarweb・ahrefs）。數值為媒體資料記載值。畫面為示意（Banaverse 生成情境＋刊登示意），與實際刊登內容不同。")
d.pic(s, IMG("xin_device.jpg"), 0.45, 1.5, 7.55, 4.21, mode="cover")
ai(s, 0.55, 1.6)
d.tx(s, 0.45, 5.75, 7.55, 0.28, "① 欣傳媒專訪文章（網站）　② 欣傳媒 Facebook 推播", 8.5, TNAVY, True, align="c", font=FONT_ZH)
nums = [("27.5萬", "Facebook 粉絲"), ("145萬", "單月貼文觸及"), ("18萬＋", "IG 單月觸及"), ("129萬", "YouTube 最高觀看")]
for i, (v, l) in enumerate(nums):
    x = 8.2 + (i % 2) * 2.38
    y = 1.5 + (i // 2) * 0.98
    d.rrect(s, x, y, 2.28, 0.88, "F5F7FB", None)
    d.tx(s, x, y + 0.04, 2.28, 0.5, v, 18, PINK, True, align="c", font="Meiryo")
    d.tx(s, x, y + 0.53, 2.28, 0.3, l, 8.5, GREY, align="c", font=FONT_ZH)
card(s, 8.2, 3.5, 4.7, 2.25, "企劃內容",
     ["・專訪長岡花火的關係人：鳳凰・白菊・正三尺玉的故事",
      "・欣傳媒 FB・IG 推播（含廣告費），Yahoo・LINE TODAY 等轉載",
      "・文中連結雄獅「觀覽席保證行程」與繁中官方指南",
      "・雄獅門市・會員推播，線上線下同步"], TNAVY, 9.5)
flow = [("專訪刊登", "欣傳媒網站"), ("社群推播", "FB・IG"), ("新聞轉載", "Yahoo・LINE TODAY"), ("雄獅行程", "觀覽席保證")]
for i, (t, b_) in enumerate(flow):
    x = 0.45 + i * 3.13
    d.rrect(s, x, 6.08, 2.85, 0.68, PINK if i == 3 else TNAVY, None)
    d.tx(s, x, 6.08, 2.85, 0.68, [[(t + "　", {"size": 12}), (b_, {"size": 9, "bold": False})]], 11, WHITE, True, align="c", anchor="m", font=FONT_ZH)
    if i < 3:
        d.arrow(s, x + 2.88, 6.28, 0.22, 0.28, GOLD_L)

# ================================================================ 2-5 年間發信
p25 = s = page("2-7. 年間發信計畫｜不只 8 月，一整年都讓台灣人想起長岡",
               "1月的「正三尺玉」只有 11 篇就有 27.5 萬聲量——故事型內容在淡季也會擴散。依季節設計 4 個話題。",
               SRC_I + "（月次トレンド分析）。抽選日程依 2026 年實績推估，以官方公布為準。圖為AI示意。")
cal = [("1〜2月", "新年，從一顆正三尺玉開始", "直徑 650m 的大玉 × 新年開運話題。官方帳號與 KOC 同步發信，搶下「今年想看的花火」第一個位置。", "sanjaku.jpg", GOLD_T),
       ("3〜6月", "抽選前：今年一定要去", "抽選日程・海外報名方式・席種比較・旅行團。GEO 與 KOC 攻略文集中投放，接住「被 Reels 燒到」的人。", "ta_family.jpg", PINK),
       ("7〜8月", "現場：黃金雨與鳳凰", "KOC 的現場 Reels 與即時發信。在日本旅行中的台灣人，也能當天參加一日遊。", "kv_hero.jpg", TNAVY),
       ("9〜12月", "白菊與長岡的四季", "慰靈的「白菊」與復興的故事；酒藏・雪國・春櫻。8月以外也讓長岡被想起，接到下一年的抽選。", "winter_sake.jpg", "2E9E6A")]
for i, (m, t, b, img, c) in enumerate(cal):
    x = 0.45 + i * 3.13
    photo(s, IMG(img), x, 1.45, 3.0, 2.3, tag=(i == 0))
    d.label(s, x + 0.1, 3.4, 1.05, 0.28, m, c, WHITE, 9, radius=0.3)
    d.rect(s, x, 3.85, 3.0, 0.06, c)
    d.tx(s, x, 3.98, 3.0, 0.65, t, 13, c, True, font=FONT_ZH, line=1.15)
    d.tx(s, x, 4.65, 3.0, 1.5, b, 9.5, INK, font=FONT_ZH, line=1.35)
msgbar(s, "目標：全年聲量 ＋30％（4,770,013 → 6,201,017・保證）、8月以外的聲量 1.5 倍（目標值）", y=6.25)

# ================================================================ 2-6 廣告
p26 = s = page("2-8. Meta・Google 廣告｜抽選前的台灣 × 8月在日本的台灣人",
               "抽選前（3〜6月）在台灣觸及「對日本花火有興趣的人」；8月初，觸及正在東京旅行的繁中使用者，推薦當天的一日遊。",
               "※ 配信條件・預算為示意，依方案與媒體規範調整。廣告媒體費另計。圖為示意。")
d.rrect(s, 0.45, 1.45, 6.1, 4.0, WHITE, PINK, lw=1.25)
d.label(s, 0.6, 1.58, 1.6, 0.32, "① 抽選前｜台灣", PINK, WHITE, 9.5, radius=0.3)
d.pic(s, PNG("bn_newyear.png"), 0.6, 2.05, 2.3, 2.3)
d.pic(s, PNG("bn_kv.png"), 3.0, 2.05, 1.73, 2.3)
d.tx(s, 4.85, 2.05, 1.6, 2.3, [[("對象\n", {"color": PINK})], "台灣・日本旅遊／花火／祭典興趣", "", [("目的\n", {"color": PINK})], "Threads 追蹤・指南瀏覽・行程點擊"], 8.5, INK, True, font=FONT_ZH, line=1.25)
d.tx(s, 0.6, 4.45, 5.8, 0.95, "Meta（Facebook・Instagram・Threads）＋Google 搜尋廣告。抽選日程公布時與報名截止前加強。", 9.5, INK, True, font=FONT_ZH, line=1.3)
d.rrect(s, 6.8, 1.45, 6.1, 4.0, WHITE, TNAVY, lw=1.25)
d.label(s, 6.95, 1.58, 2.3, 0.32, "② 8月初｜在東京的台灣人", TNAVY, WHITE, 9.5, radius=0.3)
d.rrect(s, 6.95, 2.05, 2.6, 2.3, "EEF2FA", None)
d.circle(s, 7.15, 2.3, 0.9, "東京", TNAVY, 12)
d.arrow(s, 8.12, 2.6, 0.38, 0.3, PINK)
d.circle(s, 8.55, 2.3, 0.9, "長岡", PINK, 12)
d.tx(s, 6.95, 3.3, 2.6, 0.95, "上越新幹線 約1.5小時\n接駁巴士 當日往返", 9, TNAVY, True, align="c", font=FONT_ZH, line=1.3)
photo(s, IMG("bus.jpg"), 9.7, 2.05, 3.05, 2.3)
d.tx(s, 6.95, 4.45, 5.8, 0.95, "Google 位置配信：東京都內＋繁體中文使用者。推薦雄獅旅遊的當日往返・觀覽席行程。", 9.5, INK, True, font=FONT_ZH, line=1.3)
d.rrect(s, 0.45, 5.6, 12.45, 1.12, "F5F7FB", None)
d.tx(s, 0.65, 5.65, 12.1, 1.02, ["・訪日中的配信：在指定區域內的繁中使用者，以位置與語言精準觸及「人已經在日本」的台灣旅客",
                                   "・成效以 UTM 與 Pandora 衡量：廣告 → 欣傳媒專訪・繁中官方指南 → 雄獅行程頁"], 10, INK, font=FONT_ZH, line=1.4)

# ================================================================ 2-7 視覺提案
p27 = s = page("2-9. 視覺提案｜長岡花火・台灣版的 Key Visual",
               "研究官方主視覺・日本各地花火海報・台灣 OTA／KOC 的視覺後，決定台灣版的長相：黑夜×金、直書明朝、一定有「人」。",
               "研究對象：長岡花火官方主視覺（2026）・各地花火大會官方海報・KKday／Klook 商品頁・台灣 KOC 的 Reels 封面。所有畫面為示意（Banaverse 生成素材＋正式排版）。")
res = [("官方主視覺", "黑底×金色鳳凰、直書明朝、一句短文案", "品格・故事", TNAVY),
       ("各地花火海報", "浴衣人物背影、日期特大、深藍夜空", "祭典感・人物", BROWN),
       ("台灣 OTA・KOC", "金色水平線全景、「全攻略」大字、背影", "實用・真實感", PINK)]
for i, (t, b, k, c) in enumerate(res):
    y = 1.45 + i * 0.82
    d.rrect(s, 0.45, y, 4.4, 0.72, WHITE, c, lw=1.0)
    d.tx(s, 0.6, y + 0.04, 1.8, 0.3, t, 10, c, True, font=FONT_ZH)
    d.tx(s, 0.6, y + 0.36, 4.1, 0.32, b, 8.5, INK, font=FONT_ZH)
    d.label(s, 3.3, y + 0.07, 1.45, 0.24, k, c, WHITE, 7.5, radius=0.3)
d.tx(s, 0.45, 3.95, 4.4, 0.3, "→ 台灣版的設計原則", 11, TNAVY, True, font=FONT_ZH)
rules = ["黑夜 #0E1630 × 鳳凰金 #E8B84A 為主色", "官網桃紅 #EA336A 只用在 CTA", "故事用明朝體、資訊用黑體", "一定有台灣旅客的「人」", "一張圖只講一件事"]
for i, r in enumerate(rules):
    d.tx(s, 0.55, 4.3 + i * 0.4, 4.3, 0.38, f"{i+1}. " + r, 9.5, INK, font=FONT_ZH)
for i, cc in enumerate([NIGHT, GOLD_L, PINK, BROWN]):
    d.rect(s, 0.55 + i * 0.5, 6.35, 0.42, 0.3, cc)
d.pic(s, PNG("bn_kv.png"), 5.05, 1.45, 3.1, 4.13)
d.tx(s, 5.05, 5.62, 3.1, 0.28, "KV（直式海報・IG 4:5）", 8.5, TNAVY, True, align="c", font=FONT_ZH)
d.pic(s, PNG("bn_newyear.png"), 8.35, 1.45, 2.2, 2.2)
d.pic(s, PNG("bn_manner.png"), 10.7, 1.45, 2.2, 2.2)
d.tx(s, 8.35, 3.68, 2.2, 0.26, "1月 正三尺玉（1:1）", 8, TNAVY, True, align="c", font=FONT_ZH)
d.tx(s, 10.7, 3.68, 2.2, 0.26, "正規購票（1:1）", 8, TNAVY, True, align="c", font=FONT_ZH)
d.pic(s, PNG("bn_winter.png"), 8.35, 4.0, 4.55, 2.38)
d.tx(s, 8.35, 6.42, 4.55, 0.26, "長岡四季｜冬（廣告 1.91:1）", 8, TNAVY, True, align="c", font=FONT_ZH)

# ================================================================ 聲量分析導出的設計（PASONA 結尾頁）
pdes = s = page("聲量分析導出的台灣推廣設計",
                "以「一生一次」的感動為入口，讓還不認識長岡的台灣人知道、想去，並透過攻略與行程「去得成」。",
                SRC_V + "／" + SRC_I.replace("資料來源：", ""))
d.rrect(s, 0.45, 1.45, 2.7, 5.25, TNAVY, None, radius=0.08)
d.tx(s, 0.55, 1.6, 2.5, 0.65, "84.2%", 32, WHITE, True, align="c", font="Meiryo")
d.tx(s, 0.55, 2.25, 2.5, 0.3, "正面評價比率", 11, "D9EAF7", True, align="c", font=FONT_ZH)
d.tx(s, 0.7, 2.85, 2.25, 1.6, "好感度已經是滿分。\n\n下一個課題，是讓「更多台灣人」知道長岡花火。", 11, WHITE, True, font=FONT_ZH, line=1.3)
d.hline(s, 0.75, 4.75, 2.85, 4.75, "6F7FB8", 1)
d.tx(s, 0.7, 4.85, 2.3, 1.7, "IG Reels 擴散感動、Threads 回答問題、雄獅行程讓人去得成。", 9.5, WHITE, True, font=FONT_ZH, line=1.35)
d.tx(s, 3.45, 1.45, 5, 0.3, "目標族群｜3 個重點層", 12, "18275F", True, font=FONT_ZH)
tas = [("TA 1", "一生一次朝聖派", "20〜30代｜情侶・閨蜜。被 IG Reels「燒到」，浴衣・拍照", "ta_yukata.jpg"),
       ("TA 2", "攻略計畫派", "30〜40代｜家庭・小團體。比較席種・住宿，願意付費換安心", "ta_family.jpg"),
       ("TA 3", "日本旅遊回訪派", "30〜40代｜去過東京・大阪，想找「下一個日本」", "ta_photo.jpg")]
for i, (k, t, b, img) in enumerate(tas):
    x = 3.45 + i * 3.18
    d.rrect(s, x, 1.8, 3.05, 1.75, WHITE, LINE, radius=0.05)
    photo(s, IMG(img), x + 0.1, 1.9, 1.0, 1.55, tag=False)
    d.tx(s, x + 1.2, 1.9, 1.8, 0.25, k, 9, PINK, True, font=FONT_ZH)
    d.tx(s, x + 1.2, 2.15, 1.8, 0.32, t, 11, "18275F", True, font=FONT_ZH)
    d.tx(s, x + 1.2, 2.5, 1.8, 1.0, b, 8.5, "3F4752", font=FONT_ZH, line=1.25)
d.tx(s, 3.45, 3.7, 6, 0.3, "內容｜旅マエ → 旅ナカ → 旅アト", 12, "18275F", True, font=FONT_ZH)
rows = [("旅マエ", "讓人知道、想去", "正三尺玉的新年／鳳凰・白菊的故事／抽選日程／席種・行程比較／東京出發一日遊"),
        ("旅ナカ", "現場的感動即時傳出", "KOC 的現場 Reels／官方帳號的即時發信／在日台灣人的當日參加"),
        ("旅アト", "把感動翻譯成下一個人的理由", "UGC・心得文的二次利用／白菊與長岡四季／下一年的抽選提醒")]
for i, (k, t, b) in enumerate(rows):
    y = 4.05 + i * 0.85
    d.rrect(s, 3.45, y, 9.45, 0.75, "F5F7FB", None)
    d.tx(s, 3.65, y + 0.06, 0.95, 0.3, k, 12, "234B9B", True, font=FONT_ZH)
    d.tx(s, 4.6, y + 0.06, 3.5, 0.3, t, 12, "18275F", True, font=FONT_ZH)
    d.tx(s, 3.65, y + 0.38, 9.1, 0.35, b, 10, "3F4752", font=FONT_ZH)

# ================================================================ 時程
psch = s = page("實施時程（2026年12月〜2027年9月）",
                "抽選前（3〜6月）讓官方帳號・GEO・繁中指南就位；1月的正三尺玉話題起跑，8月現場，9月起接到下一年。",
                "※ 2027年的抽選日程依 2026 年實績（一般抽選 5/25〜6/8）推估，以官方公布為準。")
mm = ["12月", "1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月"]
GX, GW, GY = 2.75, 10.15, 1.5
cw = GW / 10
d.rect(s, GX, GY, cw, 0.3, NIGHT)
d.rect(s, GX + cw, GY, GW - cw, 0.3, NIGHT)
d.tx(s, GX, GY, cw, 0.3, "2026", 8, GOLD_L, True, align="c", anchor="m")
d.tx(s, GX + cw, GY, GW - cw, 0.3, "2027", 8, GOLD_L, True, align="c", anchor="m")
for i, m in enumerate(mm):
    d.rect(s, GX + i * cw, GY + 0.3, cw, 0.3, PINK if m in ("3月", "4月", "5月", "6月") else ("C0504D" if m == "8月" else TNAVY), "FFFFFF", lw=0.5)
    d.tx(s, GX + i * cw, GY + 0.3, cw, 0.3, m, 8.5, WHITE, True, align="c", anchor="m", font=FONT_ZH)
gant = [("Pandora 監測・月報", 0, 10, "8A93A6", "基準值測定 → 月報・即時通知"),
        ("Threads 官方帳號", 0, 10, TNAVY, "開設・故事 → 抽選資訊 → 現場 → 白菊・回顧"),
        ("Threads KOC", 1, 8, PINK, "①一生一次　②抽選・席種　③住宿・交通　④一日遊　⑤長岡四季"),
        ("IG KOC・旅遊 KOC", 1, 9, GOLD_T, "冬・春的長岡 ／ 8月 現場 Reels"),
        ("GEO（AI 搜尋）", 1, 4, "2E9E6A", "KW30・新聞6・論壇6"),
        ("繁中官方指南 LP", 1, 4, TEAL, "製作 → 3月上線"),
        ("雄獅×欣傳媒", 3, 8, "0F4C81", "專訪刊登・社群推播 → 觀覽席行程販售 → 現場"),
        ("Meta・Google 廣告", 3, 9, "C0504D", "抽選前（台灣）→ 8月初（在東京）"),
        ("KV・Banner", 0, 3, BROWN, "設計系統 → 季節 Banner")]
for i, (t, a, b, c, note) in enumerate(gant):
    y = GY + 0.68 + i * 0.44
    d.rect(s, 0.45, y, 12.45, 0.4, WHITE if i % 2 == 0 else "F5F7FB", None)
    d.tx(s, 0.5, y, 2.2, 0.4, t, 9, INK, True, anchor="m", font=FONT_ZH)
    d.rrect(s, GX + a * cw + 0.03, y + 0.06, (b - a) * cw - 0.06, 0.28, c, None, radius=0.3)
    d.tx(s, GX + a * cw + 0.1, y + 0.06, (b - a) * cw - 0.2, 0.28, note, 7.5, WHITE, True, anchor="m", font=FONT_ZH)
y = GY + 0.68 + len(gant) * 0.44 + 0.06
d.rect(s, 0.45, y, 12.45, 0.6, "FDECEF")
d.tx(s, 0.5, y, 2.2, 0.6, "主要時點", 9, PINK, True, anchor="m", font=FONT_ZH)
for i, t in [(1, "1/1 正三尺玉\n新年話題"), (3, "3月 繁中指南\n上線"), (5, "5〜6月\n一般抽選（推估）"), (8, "8/2・8/3\n長岡花火"), (9, "9月 成果\n總結報告")]:
    x = GX + i * cw + cw / 2
    d.tx(s, x - 0.8, y + 0.02, 1.6, 0.58, "◆ " + t, 7.5, PINK, True, align="c", line=1.0, font=FONT_ZH)

# ================================================================ 排序
order = [cover, company, service, domain3, sec1, p11, media, p13, p14, p15,
         sec2, p20, p2f, pkoc, p21, p22, p23, p24, p25, p26, p27, pdes, psch, thanks]
lst = d.prs.slides._sldIdLst
by_id = {}
for x in list(lst):
    by_id[d.prs.slides.get(int(x.get("id")))._element] = x
for x in list(lst):
    lst.remove(x)
for sl in order:
    lst.append(by_id[sl._element])
if JA and d.missing:
    json.dump(d.missing, open(os.path.join(HERE, "i18n_missing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("MISSING", len(d.missing))
d.save(OUT, animate=False)
print("saved", OUT, len(d.prs.slides))
