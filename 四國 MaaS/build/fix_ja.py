# -*- coding: utf-8 -*-
"""使用者手動調整過頁序的日文版：拿掉儀表板、重編標題與頁碼、封面改 XXX御中。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "【インタセクト】四国MaaS 台湾市場インバウンド集客施策のご提案202611_日本語版.pptx")
OUT = os.path.join(ROOT, "【XXX御中】四国MaaS 台湾向けインバウンド集客のご提案202611.pptx")
d = Deck(SRC, font="Meiryo")
S = d.prs.slides

def set_text(sh, text):
    tf = sh.text_frame
    ps = tf.paragraphs
    runs = ps[0].runs
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""
    for p in ps[1:]:
        p._p.getparent().remove(p._p)

def title_of(s):
    for sh in s.shapes:
        if sh.has_text_frame and sh.left < 914400 * 0.1 and sh.top < 914400 * 0.3 and sh.width > 914400 * 8:
            return sh

TITLES = {
    "1. 現状整理": "1. 現状分析｜四国MaaSの3つのPOCと台湾客の位置づけ",
    "1-2. 課題整理": "1-2. 現状分析｜台湾旅行者が四国でつまずく5つの課題",
    "1-3. タイミング": "1-3. 現状分析｜台湾⇔四国の直行便と今後のタイミング",
    "1-4. 現状分析": "1-4. 現状分析｜「四国」に関する口コミ分析",
    "1-5. 現状分析": "1-5. 現状分析｜台湾旅行者の関心とセンチメント",
    "2-2. コンセプト": "2. 提案コンセプト｜便連動のMaaS「着いたら、すぐ乗れる」",
    "2. 提案概要": "2-2. 提案概要",
    "3. 全体像": "3. 目指す乗車・再訪までの全体像",
    "3-2. 台湾旅行者の1日": "3-2. 全体像｜台湾旅行者の1日の旅程",
    "3-3. 補助金申請との対応": "3-3. 全体像｜補助金申請（観光推進）との対応",
    "4. 集客施策": "4. 集客施策｜施策ごとの役割",
    "4-1. 集客施策｜口コミ施策①": "4-1. 集客施策｜口コミ施策①（Threads KOC）",
    "4-1. 集客施策｜口コミ施策②": "4-1. 集客施策｜口コミ施策②（Threads公式アカウント運用）",
    "4-2. 集客施策": "4-2. 集客施策｜GEO（AI検索対策）",
    "4-3. 集客施策｜雄獅・欣傳媒①": "4-3. 集客施策｜欣傳媒①　媒体の特徴と雄獅グループの資源",
    "4-3. 集客施策｜雄獅・欣傳媒②": "4-3. 集客施策｜欣傳媒②　読者体験ツアーの企画",
    "4-3. 集客施策｜雄獅・欣傳媒③": "4-3. 集客施策｜欣傳媒③　実施フローと掲載イメージ",
    "4-4. 集客施策": "4-4. 集客施策｜便連動広告（Meta・Google）",
    "4-5. リアル接点": "4-5. リアル接点｜新光三越「日本商品展」出展支援",
    "5-1. 予約導線": "5-1. 予約導線｜繁体字ランディングページ（便連動の送迎予約）",
    "5-2. LINE公式アカウント": "5-2. LINE公式アカウント｜台湾で予約・乗車まで完結する理由",
    "5-3. LINE運用フロー": "5-3. LINE公式アカウント｜運用フローとPOC後の引き継ぎ",
    "6. 効果測定": "6. 効果測定｜月次モニタリング",
    "7. KPI設計": "7. KPI設計｜保証・目標値・提供内容",
    "8. 実施スケジュール": "8. 実施スケジュール（2026年12月〜2028年3月）",
    "9. 今後の進め方": "9. 今後の進め方",
}

# ---- cover
for sh in S[0].shapes:
    if not sh.has_text_frame:
        continue
    t = sh.text_frame.text
    if "四国MaaS｜" in t:
        sh.text_frame.paragraphs[0].runs[0].text = "四国MaaS｜繁体字圏向け集客施策のご提案"
    elif "ご関係者各位" in t or "御中" in t:
        set_text(sh, "XXX　御中")

# ---- titles & page numbers
for idx, s in enumerate(S, 1):
    if idx in (1, len(S)):
        continue
    t = title_of(s)
    if t is not None:
        cur = t.text_frame.text
        key = max((k for k in TITLES if cur.startswith(k)), key=len, default=None)
        if key:
            set_text(t, TITLES[key])
        else:
            print("NO TITLE MATCH", idx, cur)
    for sh in s.shapes:
        if sh.has_text_frame and sh.left > 914400 * 12.2 and sh.top > 914400 * 7.0 and sh.text_frame.text.strip().isdigit():
            set_text(sh, str(idx))

# ---- dashboard slide
for s in S:
    t = title_of(s)
    if t is None or not t.text_frame.text.startswith("6. 効果測定"):
        continue
    for sh in list(s.shapes):
        x, y = sh.left / 914400, sh.top / 914400
        if sh.shape_type == 13 and x < 1 and y > 1.4:      # dashboard picture
            sh._element.getparent().remove(sh._element)
        elif sh.has_text_frame and x < 1 and 5.6 < y < 6.1:  # old Pandora caption
            sh._element.getparent().remove(sh._element)
        elif sh.has_text_frame and abs(y - 0.8) < 0.05:
            set_text(sh, "Pandoraで台湾・香港・マカオの反応を毎月分析します。施策の効果と旅行者の疑問を共通の指標で把握し、翌月の施策に反映します。")
        elif sh.has_text_frame and abs(y - 6.9) < 0.05:
            set_text(sh, "※ POC利用データの取得範囲は、運行システムとの連携方法により確定します。")
    # left panel (native)
    d.rrect(s, 0.45, 1.6, 8.1, 5.15, SOFT, None, radius=0.04)
    d.circle(s, 0.65, 1.78, 0.62, "AI", NAVY, 14)
    d.tx(s, 1.4, 1.78, 6.9, 0.35, "Pandora", 15, NAVY, True)
    d.tx(s, 1.4, 2.12, 6.9, 0.3, "AIソーシャルリスニングツール", 9.5, GREY)
    d.tx(s, 0.7, 2.6, 3.7, 0.3, "モニタリング対象", 10.5, RED, True)
    d.tx(s, 0.7, 2.95, 3.75, 2.2,
         ["・四国MaaSのサービス名・POC実施地周辺の観光地",
          "・四国遍路・ジョン万次郎など季節の話題",
          "・ほかの訪日先（関西・九州など）との比較",
          "・ネガティブ意見と懸念（交通・バリアフリー・費用）"], 9, INK, line=1.4)
    d.tx(s, 0.7, 4.55, 3.7, 0.3, "データソース（台湾・香港・マカオ）", 10.5, RED, True)
    for i, c in enumerate(["Threads", "Instagram", "Facebook", "Dcard", "PTT", "ニュース", "YouTube"]):
        d.label(s, 0.7 + (i % 4) * 0.93, 4.92 + (i // 4) * 0.4, 0.86, 0.32, c, WHITE, NAVY, 8.5, radius=0.3)
    d.tx(s, 0.7, 5.8, 3.75, 0.8, "現状分析（P.5）と同じキーワード・地域設定を基準に、継続して追跡します。", 8.5, GREY, line=1.25)
    d.tx(s, 4.65, 2.6, 3.8, 0.3, "Pandoraレポート（P.5の実測画面）", 9, NAVY, True)
    d.pic(s, "pandora/v_stats.png", 4.65, 2.95, 3.75, 1.2)
    d.pic(s, "pandora/v_trend.png", 4.65, 4.25, 3.75, 1.65)
    d.tx(s, 4.65, 5.95, 3.75, 0.6, "基準値（施策前）と同じ形式で、声量・反応・推移を毎月比較します。", 8.5, GREY, line=1.25)

d.prs.save(OUT)
print("saved", OUT)
