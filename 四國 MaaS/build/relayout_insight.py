# -*- coding: utf-8 -*-
"""1-5 頁：改為台港澳、歸納 4 個 insight（結論在上、Pandora 洞察報告截圖在下）。  python3 relayout_insight.py zh|ja"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

LANG = sys.argv[1]
J = LANG == "ja"
def t(zh, ja):
    return ja if J else zh
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "【XXX御中】四国MaaS 台湾向けインバウンド集客のご提案202611_v2.pptx" if J else
                 "【繁中版】四國MaaS 台灣市場Inbound集客策略提案202611_v2.pptx")
d = Deck(F, font="Meiryo" if J else None)
E = 914400

def is_title(sh):
    return sh.has_text_frame and sh.left < E * 0.1 and sh.top < E * 0.3 and sh.width > E * 8

s = next(sl for sl in d.prs.slides if any(is_title(sh) and sh.text_frame.text.startswith("1-5.") for sh in sl.shapes))

def set_text(sh, text):
    ps = sh.text_frame.paragraphs
    ps[0].runs[0].text = text
    for r in ps[0].runs[1:]:
        r.text = ""
    for p in ps[1:]:
        p._p.getparent().remove(p._p)

# 只留標題・引言・頁碼・出處，其餘清掉
for sh in list(s.shapes):
    y, x = sh.top / E, sh.left / E
    if is_title(sh):
        set_text(sh, t("1-5. 現況分析｜台港澳旅客怎麼談四國", "1-5. 現状分析｜台湾・香港・マカオの旅行者は四国をどう語っているか"))
    elif sh.has_text_frame and abs(y - 0.8) < 0.05:
        set_text(sh, t("台港澳旅客喜歡的是四國的絕景、遍路與美食；讓人卻步的是移動與天候。而「交通工具」本身，也能成為吸引人的話題。",
                       "台湾・香港・マカオの旅行者が好むのは、四国の絶景・遍路・グルメ。足を止めるのは移動と天候です。そして「乗り物」そのものも、人を惹きつける話題になります。"))
    elif sh.has_text_frame and abs(y - 6.9) < 0.05:
        set_text(sh, t("資料來源：Pandora（AI社群聆聽）洞察報告「四國」（資料期間 2025/9/1〜2026/9/2，台灣・香港・澳門）。",
                       "出典：Pandora by The Pocket Company／Accucrazy「四國」インサイトレポート（データ期間：2025年9月1日〜2026年9月2日、台湾・香港・マカオ）"))
    elif sh.has_text_frame and x > 12.2 and y > 7.0:
        pass
    else:
        sh._element.getparent().remove(sh._element)

INS = [
    ("1", RED, t("話題集中在少數景點", "話題は一部の観光地に集中"),
     t("小豆島・高松・金刀比羅宮等點狀景點最常被提到，串連四國的「周遊路線」幾乎沒人談。",
       "小豆島・高松・金刀比羅宮など「点」の観光地が中心。四国をつなぐ「周遊ルート」はほとんど語られていません。")),
    ("2", "1E7B47", t("嚮往來自絕景・遍路・美食", "憧れは絶景・遍路・グルメから"),
     t("正面評價集中在瀨戶內海絕景、遍路的自我對話、讚岐烏龍麵與鰹魚。想去的理由已經足夠。",
       "ポジティブ評価は瀬戸内の絶景、遍路での自分との対話、讃岐うどん・鰹に集中。行きたい理由は十分です。")),
    ("3", RED, t("負面只有「移動」與「天候」", "ネガティブは「移動」と「天候」だけ"),
     t("夏季酷暑下的長距離移動、颱風・梅雨造成的交通混亂。不滿的對象不是四國，而是「怎麼移動」。",
       "猛暑の中の長距離移動、台風・梅雨による交通の乱れ。不満の対象は四国そのものではなく「移動手段」です。")),
    ("4", NAVY, t("交通工具本身就能成為話題", "乗り物そのものが話題になる"),
     t("觀光列車「伊予灘ものがたり」被列為正面評價。e-Palette等POC車輛，也能成為吸引人的內容。",
       "観光列車「伊予灘ものがたり」がポジティブ評価に。e-PaletteなどPOCの車両も、人を惹きつけるコンテンツになります。")),
]
CW, CH_, CY = 3.05, 1.3, 1.5
for i, (n, c, ttl, body) in enumerate(INS):
    x = 0.45 + i * 3.15
    with d.anim(s):
        d.rrect(s, x, CY, CW, CH_, WHITE, LINE)
        d.rect(s, x, CY + 0.1, 0.06, CH_ - 0.2, c)
        d.circle(s, x + 0.15, CY + 0.1, 0.36, n, c, 10)
        d.tx(s, x + 0.58, CY + 0.07, CW - 0.65, 0.44, ttl, 10, c, True, anchor="m", line=1.0)
        d.tx(s, x + 0.15, CY + 0.55, CW - 0.25, 0.72, body, 8, INK, line=1.2)
d.rect(s, 0.45, 2.95, 12.5, 0.02, "D5DBE5")
d.tx(s, 0.45, 3.02, 6.2, 0.28, t("佐證①　關鍵字分析（綠：正面／黃：中立）", "根拠①　キーワード分析（緑：ポジティブ／黄：中立）"), 9.5, NAVY, True)
d.pic(s, "pandora/n_tree.png", 0.45, 3.32, 6.1, 3.0)
d.tx(s, 0.45, 6.38, 6.1, 0.4, t("面積越大＝提到越多。景點名稱為主，幾乎沒有「路線」「交通」的關鍵字。",
                                "面積が大きいほど言及が多い。観光地名が中心で、「ルート」「交通」のキーワードはほぼありません。"), 8, GREY)
d.tx(s, 6.75, 3.02, 6.2, 0.28, t("佐證②③④　情緒分析（正面・負面的主要論點）", "根拠②③④　センチメント分析（ポジティブ・ネガティブの主な論点）"), 9.5, NAVY, True)
d.pic(s, "pandora/n_pn.png", 6.75, 3.32, 6.2, 3.45)
# 截圖上的編號（右上）
pw = 3.45 * 1290 / 795          # n_pn 實際寬
px = 6.75 + (6.2 - pw) / 2
for n, x, y, c in (("1", 6.2, 3.36, RED), ("2", px + pw - 0.75, 3.5, "1E7B47"), ("4", px + pw - 0.38, 3.5, NAVY), ("3", px + pw - 0.38, 5.05, RED)):
    d.circle(s, x, y, 0.32, n, c, 9)
d.save(F)
print("saved", F)
