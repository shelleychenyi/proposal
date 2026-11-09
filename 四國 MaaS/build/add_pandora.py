# -*- coding: utf-8 -*-
"""現況分析章節擴充：Pandora 介紹・競合比較・高互動／交通／在地卡關原文・痛點放大。
直接改使用者手動調整過的簡報（不重跑 build_deck），另存 v2。
  python3 add_pandora.py ja|zh
"""
import os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

LANG = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if LANG == "ja":
    SRC = os.path.join(ROOT, "（提出）【XXX御中】四国MaaS 台湾向けインバウンド集客のご提案202611.pptx")
    OUT = os.path.join(ROOT, "【XXX御中】四国MaaS 台湾向けインバウンド集客のご提案202611_v2.pptx")
    d = Deck(SRC, font="Meiryo")
else:
    SRC = os.path.join(ROOT, "【繁中版】四國MaaS 台灣市場Inbound集客策略提案202611.pptx")
    OUT = os.path.join(ROOT, "【繁中版】四國MaaS 台灣市場Inbound集客策略提案202611_v2.pptx")
    d = Deck(SRC)
J = LANG == "ja"
def t(zh, ja):
    return ja if J else zh

S0 = list(d.prs.slides)          # 原始順序
d.page = 0
SRC_API = t("資料來源：Pandora Public API 實測（關鍵字一致、台灣・香港・澳門、2025/9/1〜2026/9/2）。「四國」已排除指歐洲四國等非日本四國的貼文。",
            "出典：Pandora Public API 実測（キーワード一致、台湾・香港・マカオ、2025年9月1日〜2026年9月2日）。「四國」は欧州四か国など日本の四国以外を指す投稿を除外。")

def title_shape(s):
    for sh in s.shapes:
        if sh.has_text_frame and sh.left < 914400 * 0.1 and sh.top < 914400 * 0.3 and sh.width > 914400 * 8:
            return sh

def set_text(sh, text):
    ps = sh.text_frame.paragraphs
    lines = text.split("\n")
    p0 = ps[0]
    for p in ps[1:]:
        p._p.getparent().remove(p._p)
    p0.runs[0].text = lines[0]
    for r in p0.runs[1:]:
        r.text = ""
    prev = p0._p
    for ln in lines[1:]:
        np_ = copy.deepcopy(p0._p)
        prev.addnext(np_)
        prev = np_
    for p, ln in zip(sh.text_frame.paragraphs, lines):
        p.runs[0].text = ln
        for r in p.runs[1:]:
            r.text = ""

def replace_text(s, old_start, new):
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith(old_start):
            set_text(sh, new)
            return True
    print("  !! not found:", old_start[:30])
    return False

def shot(s, path, x, y, w, h, cap, sub, color):
    """原文截圖卡：圖＋渠道色條＋說明"""
    d.rrect(s, x, y, w, h, WHITE, LINE, radius=0.03)
    d.pic(s, path, x + 0.08, y + 0.08, w - 0.16, h - 1.05)
    d.rect(s, x, y + h - 0.95, w, 0.05, color)
    d.tx(s, x + 0.1, y + h - 0.88, w - 0.2, 0.36, cap, 9.5, color, True, line=1.05)
    d.tx(s, x + 0.1, y + h - 0.5, w - 0.2, 0.46, sub, 8, INK, line=1.1)

CH = {"threads": ("tcj/s11_22.jpg", "111111"), "instagram": ("tcj/s11_23.png", "C13584"), "fb": ("tcj/s11_24.png", "1877F2"),
      "dcard": ("tcj/s11_25.jpg", "006AA6"), "ptt": ("tcj/s11_26.jpg", "2B2D7C")}

def badge(s, x, y, ch):
    p, c = CH[ch]
    d.pic(s, p, x, y, 0.32, 0.32)

new = {}
# ================================================================ Pandora 介紹
s = d.new(t("1-3. 現況分析｜Pandora（AI社群聆聽）的調查範圍", "1-3. 現状分析｜Pandora（AIソーシャルリスニング）の調査範囲"),
          t("本提案的現況分析全部來自本公司的AI社群聆聽工具「Pandora」。橫跨亞洲11個國家・地區、5大社群平台，每天收集並分析在地的真實聲音。",
            "本提案の現状分析は、すべて当社のAIソーシャルリスニングツール「Pandora」によるものです。アジアを中心に11の国・地域、5大SNSから、現地のリアルな声を毎日収集・分析しています。"),
          t("資料來源：Pandora 系統規格（2026年11月）。國旗・平台標誌為各國家地區與服務的識別用途。",
            "出典：Pandora システム仕様（2026年11月時点）。国旗・ロゴは各国・地域およびサービスの識別目的で掲載しています。"))
d.rrect(s, 0.45, 1.6, 3.55, 5.15, SOFT, None, radius=0.04)
d.pic(s, "tcj/s11_8.jpg", 0.75, 1.8, 1.25, 1.25, mode="cover")
d.tx(s, 2.1, 1.9, 1.8, 0.4, "Pandora", 17, NAVY, True, font="Meiryo")
d.tx(s, 2.1, 2.32, 1.85, 0.6, t("AI社群聆聽\n輿論分析專家", "AIソーシャル\nリスニング"), 9.5, BLUE, True, line=1.1)
d.tx(s, 0.7, 3.25, 3.1, 0.3, t("Pandora 能做什麼", "Pandoraでできること"), 10.5, NAVY, True)
caps = [t("聲量・情緒（正負面）的趨勢分析", "声量・センチメントの推移分析"),
        t("話題關鍵字・競合地區比較", "話題キーワード・競合エリア比較"),
        t("高互動・負評貼文的自動抽出", "高反響・ネガティブ投稿の自動抽出"),
        t("施策前後的效果驗證（基準值比較）", "施策前後の効果検証（基準値比較）")]
for i, c in enumerate(caps):
    y = 3.62 + i * 0.6
    d.rrect(s, 0.7, y, 3.05, 0.5, WHITE, None)
    d.circle(s, 0.78, y + 0.1, 0.3, str(i + 1), RED, 9)
    d.tx(s, 1.15, y, 2.55, 0.5, c, 8.5, INK, True, anchor="m")
# 數字
stats = [("11", t("國家・地區", "国・地域")), ("5", t("大社群平台", "大SNS")), ("7", t("種語言", "言語")), (t("每天", "毎日"), t("自動收集・更新", "自動収集・更新"))]
for i, (v, l) in enumerate(stats):
    x = 4.2 + i * 2.2
    d.rrect(s, x, 1.6, 2.1, 1.0, NAVY, None)
    d.tx(s, x, 1.62, 2.1, 0.55, v, 24 if len(v) < 3 else 18, WHITE, True, align="c", anchor="m", font="Meiryo")
    d.tx(s, x, 2.15, 2.1, 0.38, l, 9, "C9D2E3", True, align="c")
# 國家
d.tx(s, 4.2, 2.8, 8.7, 0.3, t("監測國家・地區（貼文地區標籤）", "モニタリング対象の国・地域（投稿の地域タグ）"), 10.5, NAVY, True)
FL = [("tw", "台灣", "台湾"), ("hk", "香港", "香港"), ("mo", "澳門", "マカオ"), ("jp", "日本", "日本"), ("kr", "韓國", "韓国"), ("cn", "中國", "中国"),
      ("th", "泰國", "タイ"), ("vn", "越南", "ベトナム"), ("my", "馬來西亞", "マレーシア"), ("sg", "新加坡", "シンガポール"), ("us", "美國", "米国")]
for i, (c, zh, ja) in enumerate(FL):
    x = 4.2 + (i % 6) * 1.46
    y = 3.18 + (i // 6) * 0.98
    hot = c in ("tw", "hk", "mo")
    d.rrect(s, x, y, 1.38, 0.88, "FBECEA" if hot else WHITE, RED if hot else LINE, lw=1.25 if hot else 0.75)
    d.pic(s, f"flags/{c}.png", x + 0.39, y + 0.08, 0.6, 0.4)
    d.tx(s, x, y + 0.5, 1.38, 0.32, ja if J else zh, 8.5, RED if hot else INK, hot, align="c")
d.tx(s, 11.5, 4.2, 1.45, 0.8, t("紅框＝本提案的\n分析對象\n（台港澳）", "赤枠＝本提案の\n分析対象\n（台湾・香港・マカオ）"), 7.5, RED, True, line=1.1)
# 平台
d.tx(s, 4.2, 5.25, 8.7, 0.3, t("資料來源平台", "データソース（SNS・掲示板）"), 10.5, NAVY, True)
PL = [("threads", "Threads", t("台灣是全球最大市場", "台湾が世界最大の市場")), ("instagram", "Instagram", t("旅遊照片・Reels", "旅行写真・リール")),
      ("fb", "Facebook", t("社團・粉專", "グループ・ページ")), ("dcard", "Dcard", t("年輕族群論壇", "若年層の掲示板")), ("ptt", "PTT", t("台灣最大論壇", "台湾最大の掲示板"))]
for i, (k, n, sub) in enumerate(PL):
    x = 4.2 + i * 1.75
    d.rrect(s, x, 5.6, 1.66, 1.15, WHITE, LINE)
    p, c = CH[k]
    if k in ("dcard", "ptt"):
        d.pic(s, p, x + 0.18, 5.68, 1.3, 0.45)
    else:
        d.pic(s, p, x + 0.6, 5.68, 0.46, 0.46)
    d.tx(s, x, 6.15, 1.66, 0.28, n, 9, INK, True, align="c")
    d.tx(s, x, 6.42, 1.66, 0.28, sub, 7.5, GREY, align="c")
new["intro"] = s

# ================================================================ 競合比較
s = d.new(t("1-6. 現況分析｜四國的聲量只有北海道的1/7", "1-6. 現状分析｜競合エリアとの声量比較"),
          t("直飛航線已有3條，但在台灣社群上，四國的聲量只有北海道的1/7、沖繩的1/13。旅客在「比較」階段就已經把四國刷掉了。",
            "直行便が3路線あるにもかかわらず、台湾SNS上の四国の声量は北海道の1/7、沖縄の1/13。旅行者の「比較検討」の段階で、四国は候補から外れています。"),
          SRC_API)
B = [(t("沖繩", "沖縄"), 39194865, 41116), (t("北海道", "北海道"), 22167646, 18566), (t("九州", "九州"), 5947279, 5348),
     (t("四國", "四国"), 3063464, 3666), (t("北陸", "北陸"), 399124, 635)]
d.tx(s, 0.45, 1.55, 7.6, 0.3, t("台灣・港澳社群聲量（近12個月）", "台湾・香港・マカオのSNS声量（直近12か月）"), 10.5, NAVY, True)
mx = B[0][1]
for i, (n, v, c) in enumerate(B):
    y = 1.98 + i * 0.86
    hot = n in ("四國", "四国")
    with d.anim(s):
        d.tx(s, 0.45, y, 1.1, 0.62, n, 13, RED if hot else INK, True, anchor="m")
        w = max(0.08, 5.0 * v / mx)
        d.rect(s, 1.6, y + 0.08, w, 0.46, RED if hot else "B8C4D6")
        d.tx(s, 1.7 + w, y, 2.6, 0.62, [[(f"{v/10000:,.0f}" + t("萬", "万"), {"size": 13, "bold": True, "color": RED if hot else INK})],
                                         [(t(f"貼文 {c:,} 則", f"投稿 {c:,}件"), {"size": 8, "color": GREY})]], 13, INK, True, anchor="m", line=1.0)
big = [("1/13", t("沖繩", "沖縄")), ("1/7", t("北海道", "北海道")), ("1/2", t("九州", "九州"))]
for i, (v, n) in enumerate(big):
    x = 8.3 + i * 1.57
    with d.anim(s):
        d.rrect(s, x, 1.6, 1.5, 1.55, "FBECEA", None)
        d.tx(s, x, 1.65, 1.5, 0.3, t("對比", "対") + n, 9, GREY, True, align="c")
        d.tx(s, x, 1.95, 1.5, 0.75, v, 30, RED, True, align="c", anchor="m", font="Meiryo")
        d.tx(s, x, 2.72, 1.5, 0.35, t("四國的聲量", "四国の声量"), 8.5, INK, True, align="c")
d.rrect(s, 8.3, 3.35, 4.65, 2.35, WHITE, LINE)
d.tx(s, 8.45, 3.42, 4.4, 0.3, t("這代表什麼", "この差が意味すること"), 10.5, NAVY, True)
d.tx(s, 8.45, 3.75, 4.4, 1.9,
     [t("・台灣旅客做功課時，看到的幾乎都是北海道・沖繩・九州", "・台湾旅行者が下調べで目にするのは、ほぼ北海道・沖縄・九州"),
      t("・九州的聲量也有四國的約2倍", "・九州でさえ、四国の約2倍の声量がある"),
      t("・航線與景點都有，缺的是「被看見」與「去得了」的資訊", "・路線も観光地もある。足りないのは「見つかる」「行ける」情報")], 9, INK, line=1.45)
d.rrect(s, 0.45, 6.05, 12.5, 0.7, NAVY, None)
d.tx(s, 0.65, 6.05, 12.1, 0.7, t("好感度很高，卻在「比較」階段落選——這正是現在需要投資的理由。聲量＋30％，才只是追上的第一步。",
                                  "好感度は高いのに、「比較」の段階で選ばれていない。これが今、投資が必要な理由です。声量＋30％は、追いつくための第一歩にすぎません。"),
     10.5, WHITE, True, anchor="m")
new["bench"] = s

# ================================================================ 高互動（嚮往）
s = d.new(t("1-7. 現況分析｜高互動貼文：嚮往的力量已經足夠", "1-7. 現状分析｜反響の大きい投稿（憧れ）"),
          t("聲量前段班的貼文，動輒數萬個讚。台灣旅客對四國的「嚮往」已經被證明——問題是，這些貼文幾乎沒有告訴大家「怎麼去」。",
            "声量上位の投稿は、数万いいねに達します。台湾旅行者の四国への「憧れ」はすでに証明済み。問題は、これらの投稿が「どう行くか」をほとんど伝えていないことです。"),
          t("資料來源：Pandora Public API（台灣・香港・澳門、2025/9/1〜2026/9/2）聲量排名上位貼文。畫面為各貼文的公開頁面截圖（2026年11月9日擷取，數值為擷取當下）。",
            "出典：Pandora Public API（台湾・香港・マカオ、2025年9月1日〜2026年9月2日）の声量上位投稿。画面は各投稿の公開ページのスクリーンショット（2026年11月9日取得、数値は取得時点）。"))
hi = [("posts/ig_saryu_c.png", t("Instagram｜聲量第1名", "Instagram｜声量1位"), t("香川的貓島「佐柳島」。4萬人按讚，但交通只寫了一句「搭船50分鐘」", "香川の猫島「佐柳島」。4万いいねでも、交通は「船で50分」の一文のみ")),
      ("posts/ig_deep_c.png", t("Instagram｜留言數最多", "Instagram｜コメント数最多"), t("「四國很值得深度旅行」。數千則留言都在要行程", "「四国は深く旅する価値がある」。数千件のコメントが行程を求める")),
      ("posts/ig_henro_c.png", t("Instagram｜遍路系第1名", "Instagram｜遍路系1位"), t("走了1,800公里的遍路紀錄。精神性共鳴極高", "1,800kmを歩いた遍路の記録。精神性への共感が極めて高い"))]
for i, (p, cap, sub) in enumerate(hi):
    with d.anim(s):
        shot(s, p, 0.45 + i * 3.0, 1.55, 2.85, 5.2, cap, sub, "C13584")
d.rrect(s, 9.55, 1.55, 3.4, 5.2, "FBECEA", None)
d.tx(s, 9.7, 1.65, 3.1, 0.35, t("看見的落差", "見えてきたギャップ"), 11, RED, True)
gap = [(t("數萬", "数万"), t("上位貼文的按讚數", "上位投稿のいいね数")),
       ("21.5%", t("提到交通的貼文比例", "交通に触れた投稿の比率")),
       ("8.5%", t("可以查證的論壇占比", "確認できる掲示板の比率"))]
for i, (v, l) in enumerate(gap):
    y = 2.1 + i * 1.12
    d.tx(s, 9.7, y, 3.1, 0.6, v, 26, RED, True, font="Meiryo")
    d.tx(s, 9.7, y + 0.6, 3.1, 0.35, l, 8.5, INK, True)
d.tx(s, 9.7, 5.5, 3.1, 1.2, t("「想去」的情緒很滿，但「怎麼去」的資訊是空白。嚮往沒有被轉換成行程。",
                              "「行きたい」気持ちは満ちているのに、「どう行くか」は空白。憧れが旅程に変わっていません。"), 9.5, RED, True, line=1.3)
new["high"] = s

# ================================================================ 交通の壁
s = d.new(t("1-8. 現況分析｜交通貼文：近4成以租車為前提", "1-8. 現状分析｜交通に関する投稿分析"),
          t("四國相關貼文每5則就有1則在談交通，其中近4成以「租車・自駕」為前提。對不開車的台灣旅客來說，四國至今仍是「去不了的地方」。",
            "四国関連の投稿の5件に1件が交通に触れ、そのうち約4割が「レンタカー・自駕」を前提にしています。運転しない台湾旅行者にとって、四国はいまだ「行けない場所」です。"),
          SRC_API + t("畫面為公開貼文截圖（2026年11月9日擷取）。", "画面は公開投稿のスクリーンショット（2026年11月9日取得）。"))
nums = [("21.5%", t("四國相關貼文中\n提到交通的比例", "四国関連投稿のうち\n交通に触れた比率"), t("3,666則中789則", "3,666件中789件")),
        ("38.4%", t("交通貼文中\n以租車・自駕為前提", "交通投稿のうち\nレンタカー・自駕前提"), t("789則中303則", "789件中303件")),
        (t("唯一", "唯一"), t("日本沒有新幹線的\n地區（高互動貼文）", "新幹線がない地域\n（反響の大きい投稿）"), t("IG・2,382讚", "IG・2,382いいね"))]
for i, (v, l, n) in enumerate(nums):
    y = 1.6 + i * 1.72
    with d.anim(s):
        d.rrect(s, 0.45, y, 3.0, 1.6, NAVY if i < 2 else "1A2550", None)
        d.tx(s, 0.6, y + 0.05, 2.7, 0.65, v, 28, "FFD166", True, font="Meiryo")
        d.tx(s, 0.6, y + 0.72, 2.7, 0.55, l, 9, WHITE, True, line=1.1)
        d.tx(s, 0.6, y + 1.25, 2.7, 0.3, n, 7.5, "C9D2E3")
posts = [("posts/th_mani_c.png", "threads", t("Threads｜1,300讚・103留言", "Threads｜1,300いいね・103コメント"), t("「九州、北海道、四國沒車很難行動」", "「九州・北海道・四国は車がないと動きにくい」")),
         ("posts/th_sassy_c.png", "threads", t("Threads｜旅遊帳號的提問", "Threads｜旅行アカウントの質問"), t("「沒有車的話會不會不方便？」", "「車がないと不便ですか？」")),
         ("posts/ptt_shodo_c.png", "ptt", t("PTT 日本旅遊板｜37則推文", "PTT 日本旅行板｜37件の返信"), t("「公車班次很少，你會花很多時間在等」", "「バスは本数が少なく、待つ時間が長い」"))]
for i, (p, ch, cap, sub) in enumerate(posts):
    x = 3.65 + i * 3.1
    with d.anim(s):
        shot(s, p, x, 1.6, 2.98, 5.15, cap, sub, CH[ch][1])
        badge(s, x + 2.55, 1.68, ch)
new["trans"] = s

# ================================================================ 在地卡關原文
s = d.new(t("1-9. 現況分析｜在地的「卡關」原文", "1-9. 現状分析｜現地でのつまずきの声"),
          t("已經去了的旅客，在現場一樣卡住：接駁只有假日、包車司機失聯、785階的石階。反響越大的抱怨，越會勸退下一批旅客。",
            "実際に訪れた旅行者も、現地でつまずいています。送迎は休日のみ、貸切バスの運転手と連絡不通、785段の石段。反響の大きい不満ほど、次の旅行者を遠ざけます。"),
          t("資料來源：Pandora Public API 抽出的負面・不便相關貼文（2025/9/1〜2026/9/2）。畫面為公開貼文截圖（2026年11月9日擷取，數值為擷取當下）。",
            "出典：Pandora Public API で抽出したネガティブ・不便に関する投稿（2025年9月1日〜2026年9月2日）。画面は公開投稿のスクリーンショット（2026年11月9日取得、数値は取得時点）。"))
neg = [("posts/th_edzr_c.png", "threads", t("Threads｜1.07萬讚", "Threads｜1.07万いいね"), t("「看了站牌才知道只有週末假日有接駁」", "「バス停を見て初めて、送迎が土日祝のみと知った」")),
       ("posts/th_jamie_c.png", "threads", t("Threads｜962讚・76留言", "Threads｜962いいね・76コメント"), t("「司機直接失聯，25人等了將近一小時」", "「運転手と連絡が取れず、25人が1時間近く待った」")),
       ("posts/ig_kotohira_c.png", "instagram", t("Instagram｜金刀比羅宮", "Instagram｜金刀比羅宮"), t("「本宮785階、奧社1,368階，腿抖也要上」", "「本宮785段・奥社1,368段、足が震えても登る」"))]
for i, (p, ch, cap, sub) in enumerate(neg):
    x = 0.45 + i * 3.1
    with d.anim(s):
        shot(s, p, x, 1.55, 2.98, 5.2, cap, sub, CH[ch][1])
        badge(s, x + 2.55, 1.63, ch)
d.rrect(s, 9.8, 1.55, 3.15, 5.2, NAVY, None)
d.tx(s, 9.95, 1.65, 2.9, 0.35, t("不改善會怎樣", "放置した場合"), 11, "FFD166", True)
risk = [(t("負評被擴散", "不満が拡散"), t("1則抱怨＝1萬人看到的「四國很難去」", "1件の不満＝1万人に届く「四国は行きにくい」")),
        (t("比較時被刷掉", "比較で落選"), t("北海道・沖繩的資訊量是四國的7〜13倍", "北海道・沖縄の情報量は四国の7〜13倍")),
        (t("POC沒人搭", "POCに乗る人がいない"), t("交通沒被看見，新的服務也不會被使用", "交通が知られなければ、新サービスも使われない"))]
for i, (k, v) in enumerate(risk):
    y = 2.15 + i * 1.45
    d.tx(s, 9.95, y, 2.9, 0.35, f"{i+1}. {k}", 10.5, WHITE, True)
    d.tx(s, 9.95, y + 0.38, 2.9, 0.95, v, 8.5, "C9D2E3", line=1.25)
new["neg"] = s

# ================================================================ 既有頁的修改
OLD = {"pov": S0[1], "timing": S0[3], "voice": S0[4], "insight": S0[5], "pain": S0[2]}
# 口碑分析頁：痛點化
s = OLD["voice"]
if J:
    replace_text(s, "四国は繁体字圏で好意的評価が", "好意的評価93.9％は「憧れ」の数字にすぎません。投稿は年間668件、1日2件未満。移動への不安が、憧れを行動に変える前に止めています。")
    replace_text(s, "① 好意的評価", "① 好意的93.9％、でも投稿は1日2件未満")
    replace_text(s, "非常にポジティブ73.2％", "年間668件。訪日台湾人676万人に対し、四国の体験を語る投稿は極めて少数です。")
    replace_text(s, "② つまずきは", "② ネガティブの中身はすべて「移動」")
    replace_text(s, "③ 声量の波が", "③ 年の半分は「空白期」")
    replace_text(s, "ピーク（2026年4月", "ピーク（4月・7月）の約6.6〜6.8万に対し、11月・3月は2万未満。旅行の検討期に情報が途切れます。")
    replace_text(s, "④ 「確認型」", "④ 調べても答えが見つからない")
else:
    replace_text(s, "四國在繁中圈的好感度高達", "好感度93.9%只是「嚮往」的數字。實際貼文一年只有668則、一天不到2則。移動的不安，讓嚮往停在「想去」。")
    replace_text(s, "① 好感度93.9", "① 好感度93.9%，但一天不到2則貼文")
    replace_text(s, "非常正面73.2", "全年只有668則。相對於676萬訪日台灣旅客，分享四國體驗的人極少。")
    replace_text(s, "② 卡關的是", "② 負面意見全部指向「移動」")
    replace_text(s, "③ 聲量起伏大", "③ 一年有一半是「空白期」")
    replace_text(s, "高峰（2026年4月", "高峰（4月・7月）約6.6〜6.8萬，11月・3月不到2萬。旅客做功課的時期，資訊斷掉了。")
    replace_text(s, "④ 「查證型」", "④ 想查也查不到答案")
# 痛點地圖：放大
s = OLD["pain"]
if J:
    replace_text(s, "「行きたい」から", "Pandoraのデータが示すのは、5つの「行けない理由」です。いずれも、POCのサービスと繁体字の集客で解消できます。")
    replace_text(s, "「行きたいが、行き方がわからない」", "上位投稿は数万いいねでも\n確認できる掲示板は8.5％のみ")
    replace_text(s, "空港から観光地への直通公共交通がなく", "交通投稿の約4割がレンタカー前提\n「送迎は土日祝のみ」の不満")
    replace_text(s, "高齢の家族や車いす利用者は", "「785段、足が震えても登る」\n坂・階段が反響を集める")
    replace_text(s, "1台では効果が限られ", "声量は北海道の1/7・沖縄の1/13\n需要がまだ集まっていない")
else:
    replace_text(s, "從「想去」到「玩得盡興」", "Pandora的數據指出5個「去不了的理由」。每一個，都能用POC的服務與繁中集客解開。")
    replace_text(s, "「想去，但不知道怎麼去」", "上位貼文數萬讚\n可查證的論壇只有8.5%")
    replace_text(s, "機場到景點沒有直達公共交通", "交通貼文近4成以租車為前提\n「接駁只有假日」的抱怨")
    replace_text(s, "帶長輩・輪椅族不敢去", "「785階，腿抖也要上」\n爬坡・石階最受關注")
    replace_text(s, "1台效果有限", "聲量只有北海道1/7・沖繩1/13\n需求還沒被集中起來")

# ================================================================ 重新排序
P = d.prs.slides
lst = P._sldIdLst
ids = {id(sl): sid for sid, sl in zip(list(lst), list(P))}
def sid(sl):
    for x, s_ in zip(list(lst), list(P)):
        if s_ is sl:
            return x
order = [S0[0], OLD["pov"], OLD["timing"], new["intro"], OLD["voice"], OLD["insight"], new["bench"], new["high"], new["trans"], new["neg"], OLD["pain"]] + S0[6:]
els = [sid(sl) for sl in order]
for e in list(lst):
    lst.remove(e)
for e in els:
    lst.append(e)

# 標題重編
TT = {
    id(OLD["timing"]): t("1-2. 時機｜台灣與四國的距離，正在快速縮短", "1-2. 現状分析｜台湾⇔四国の直行便と今後のタイミング"),
    id(OLD["voice"]): t("1-4. 現況分析｜「四國」台灣社群聲量分析", "1-4. 現状分析｜「四国」に関する口コミ分析"),
    id(OLD["insight"]): t("1-5. 現況分析｜台灣旅客怎麼談四國", "1-5. 現状分析｜台湾旅行者の関心とセンチメント"),
    id(OLD["pain"]): t("1-10. 課題整理｜Pandora數據指出的5個「卡關點」", "1-10. 現状分析｜Pandoraデータから見える5つの課題"),
}
for i, sl in enumerate(P, 1):
    if id(sl) in TT:
        set_text(title_shape(sl), TT[id(sl)])
    if i in (1, len(P)):
        continue
    for sh in sl.shapes:
        if sh.has_text_frame and sh.left > 914400 * 12.2 and sh.top > 914400 * 7.0 and sh.text_frame.text.strip().isdigit():
            set_text(sh, str(i))
# 內文頁碼參照（P.5 → 新位置）
for sl in P:
    for sh in sl.shapes:
        if sh.has_text_frame and "P.5" in sh.text_frame.text:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    r.text = r.text.replace("P.5", "P.5")
d.save(OUT)
print("saved", OUT, len(P))
