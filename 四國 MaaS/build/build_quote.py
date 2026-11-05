# -*- coding: utf-8 -*-
"""四国MaaS 見積明細（Hakuba 12か月プラン明細の様式に準拠）"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "【インタセクト】XXX様_四国MaaS_台湾向け集客施策_3プランお見積り_202611.xlsx")

F = "Meiryo"
NAVY, HEAD, INK, GREY = "16243D", "22406B", "222222", "444444"
SOFT, OPT, GOLD, YEL = "F3F6FB", "E9F9EF", "F5B841", "FFFF00"
thin = Side(style="thin", color="D5DBE5")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

def font(sz=10, b=False, color=INK):
    return Font(name=F, size=sz, bold=b, color=color)

def fill(c):
    return PatternFill("solid", fgColor=c) if c else PatternFill()

def put(ws, ref, v, sz=10, b=False, color=INK, bg=None, fmt=None, wrap=True, h="left", border=True):
    c = ws[ref]
    if not (v is None and type(c).__name__ == "MergedCell"):
        c.value = v
    c.font = font(sz, b, color)
    if bg:
        c.fill = fill(bg)
    if fmt:
        c.number_format = fmt
    c.alignment = Alignment(wrap_text=wrap, vertical="center", horizontal=h)
    if border:
        c.border = BOX
    return c

def band(ws, row, text, sub=None, ncol=6):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncol)
    put(ws, f"A{row}", text, 14, True, "FFFFFF", NAVY, border=False)
    ws.row_dimensions[row].height = 30
    if sub:
        ws.merge_cells(start_row=row + 1, start_column=1, end_row=row + 1, end_column=ncol)
        put(ws, f"A{row+1}", sub, 10, False, "FFFFFF", NAVY, border=False)
        ws.row_dimensions[row + 1].height = 22

def header(ws, row, cols):
    for i, t in enumerate(cols):
        put(ws, f"{L(i+1)}{row}", t, 10, True, "FFFFFF", HEAD, h="center")
    ws.row_dimensions[row].height = 22

YEN = '#,##0;(#,##0);"-"'
INPUT = "0000FF"   # 青字＝入力値

wb = Workbook()

# =====================================================================
# Sheet 1：3プラン比較
# =====================================================================
ws = wb.active
ws.title = "3プラン比較"
for k, v in {"A": 32, "B": 58, "C": 7, "D": 12, "E": 8, "F": 13, "G": 8, "H": 13, "I": 8, "J": 13, "K": 30}.items():
    ws.column_dimensions[k].width = v
band(ws, 1, "XXX様　四国MaaS 台湾・繁体字圏向け集客施策　3プランのお見積り",
     "小：Threads口コミ／中：＋GEO・欣傳媒（読者体験ツアー）／大：フル展開｜金額はすべて日本円・税別｜2026年11月　インタセクト・コミュニケーションズ株式会社", ncol=11)

put(ws, "A4", "■ プラン別お見積り明細", 12, True, NAVY, border=False)
# 2段ヘッダー
for c, t in zip("ABCD", ["項目", "内容", "単位", "単価（円）"]):
    ws.merge_cells(f"{c}5:{c}6")
    put(ws, f"{c}5", t, 10, True, "FFFFFF", HEAD, h="center")
PLANS = [("E", "F", "小プラン｜Threads口コミ", "4A6FA5"), ("G", "H", "中プラン｜＋GEO・欣傳媒（推奨）", "C0504D"), ("I", "J", "大プラン｜フル展開", "16243D")]
for q, m, name, col in PLANS:
    ws.merge_cells(f"{q}5:{m}5")
    put(ws, f"{q}5", name, 10, True, "FFFFFF", col, h="center")
    put(ws, f"{m}5", None, 10, True, "FFFFFF", col)
    put(ws, f"{q}6", "数量", 9, True, "FFFFFF", col, h="center")
    put(ws, f"{m}6", "金額（円）", 9, True, "FFFFFF", col, h="center")
ws.merge_cells("K5:K6")
put(ws, "K5", "備考", 10, True, "FFFFFF", HEAD, h="center")
ws.row_dimensions[5].height = 24

items = [
    ("申請支援資料（台湾需要レポート）", "Pandora台湾需要レポート（四国全域）、観光推進KPI設計案、台湾プロモーション計画書（補助金申請書添付用）。2026年12月〜2027年1月", "式", 500000, (1, 1, 1), "仮単価：範囲確定後に確定"),
    ("Threads公式アカウント運用", "繁体字公式アカウント「四國 Easy Go（仮称）」の開設・運用。月6投稿以上（投稿カレンダー提出）、コメント返信30〜100件／月（DM対応は含まない）、画像制作10点以内／月、素材の繁体字再編集", "か月", 275000, (6, 10, 12), ""),
    ("Threads KOC 成果保証型", "フォロワー3,000+のKOCアカウント。1,500字以内の体験投稿＋コメント10件／本。1本あたり閲覧数10,000以上・エンゲージメント100以上・言及量1,000以上を保証。「合作」表記", "本", 249000, (8, 4, 6), ""),
    ("GEO（AI検索対策）", "1セット：ニュース記事6本（Yahoo奇摩ニュース／経済日報の掲載保証＋10〜15媒体への転載）＋SEO掲示板記事6本（Dcard／PTT／Mobile01）＋キーワード30組設計＋AI検索掲載3組保証。未達時は当該セット金額の30％を返金", "セット", 2400000, (0, 1, 2), "①交通・直行便 ②観光地・巡礼"),
    ("欣傳媒 旅行特集", "特集記事1本の企画・取材・制作・掲載、Yahoo等への記事配信、Facebook配信（広告費込み）", "本", 650000, (0, 1, 2), "中：ツアーレポート／大：＋直行便特集"),
    ("欣傳媒 読者体験ツアー 企画・運営", "読者約10名の募集（欣傳媒FB・IG投稿＋配信）、事前説明・LINE誘導、編集・撮影2名の同行取材、ショート動画制作、参加者アンケートの回収・集計", "回", 1200000, (0, 1, 1), "仮単価：欣傳媒の正式見積により確定"),
    ("旅行KOL（体験ツアー同行）", "バリアフリー・親子旅行／写真系のKOL。Instagramリール1本＋ストーリーズ2本、Threads投稿1本。「合作」表記", "名", 190000, (0, 2, 2), "人選は事前確認"),
    ("欣傳媒 ニュース風動画", "2〜3分のニュース風動画1本（企画・撮影・編集）、YouTube・SNS掲載", "本", 400000, (0, 0, 1), "仮単価：欣傳媒の正式見積により確定"),
    ("便連動広告 運用（Meta・Google）", "直行便の曜日・連休に合わせた友だち追加広告の設計・入稿・最適化、位置情報配信、月次レポート", "か月", 50000, (0, 0, 6), "媒体費は別途"),
    ("声量モニタリング（Pandora）", "施策前の基準値測定、月次レポート1本／月、LINE即時通知（キーワード4組・24時間監視）、ネガティブ投稿発生時の通報", "か月", 125000, (6, 10, 12), ""),
]
r0 = 7
for i, (a, b, u, p, qs, note) in enumerate(items):
    r = r0 + i
    bg = SOFT
    put(ws, f"A{r}", a, 10, True, INK, bg)
    put(ws, f"B{r}", b, 9, False, INK, bg)
    put(ws, f"C{r}", u, 10, False, INK, bg, h="center")
    put(ws, f"D{r}", p, 10, False, INPUT, bg, YEN, h="right")
    for (q, m, *_), n in zip(PLANS, qs):
        put(ws, f"{q}{r}", n, 10, False, INPUT, None, '#,##0;(#,##0);"-"', h="center")
        put(ws, f"{m}{r}", f"=D{r}*{q}{r}", 10, False, INK, None, YEN, h="right")
    put(ws, f"K{r}", note, 9, False, "C0504D" if "仮単価" in note else GREY, bg)
    ws.row_dimensions[r].height = 56
rl = r0 + len(items) - 1
rT = rl + 1
put(ws, f"A{rT}", "プラン合計（税別）", 11, True, NAVY, GOLD)
for c in "BCDK":
    put(ws, f"{c}{rT}", None, 11, True, NAVY, GOLD)
put(ws, f"B{rT}", "申請支援（2026年12月〜）＋施策期間（最長12か月、POC時期に合わせて調整）", 9, True, NAVY, GOLD)
for q, m, *_ in PLANS:
    put(ws, f"{q}{rT}", None, 11, True, NAVY, GOLD)
    put(ws, f"{m}{rT}", f"=SUM({m}{r0}:{m}{rl})", 11, True, NAVY, GOLD, YEN, h="right")
ws.row_dimensions[rT].height = 28
r = rT + 1
put(ws, f"A{r}", "プランの狙い", 10, True, INK, SOFT)
put(ws, f"B{r}", "共通：申請支援資料＋Pandoraで、台湾需要の根拠と効果測定を確保", 9, False, GREY, SOFT)
for c in "CD":
    put(ws, f"{c}{r}", None, 9, False, INK, SOFT)
aims = ["Threadsの公式アカウント＋KOC口コミで、POC前後の認知を集中的につくる",
        "口コミに加え、GEOで「行き方」の検索を押さえ、欣傳媒の読者体験ツアーでPOCの最初の乗客と記事をつくる",
        "GEO2セット・特集2本・動画・便連動広告まで、認知から予約・乗車までを通年で展開"]
for (q, m, *_), t_ in zip(PLANS, aims):
    ws.merge_cells(f"{q}{r}:{m}{r}")
    put(ws, f"{q}{r}", t_, 9, False, INK, None)
    put(ws, f"{m}{r}", None, 9)
put(ws, f"K{r}", None, 9, False, INK, SOFT)
ws.row_dimensions[r].height = 64
TOTROW = rT

# ---- 別途実費
r += 2
put(ws, f"A{r}", "■ 別途実費（上記合計に含まず）", 12, True, NAVY, border=False)
extras = [
    ("体験ツアーの旅費（中・大）", "参加者・KOL・欣傳媒スタッフの航空券（台北⇔四国）・宿泊・現地交通。負担方式は欣傳媒・雄獅と調整のうえ確定", "実費"),
    ("広告媒体費（大）", "Meta・Googleへの実投下額（便連動広告）", "実費"),
    ("POCサービスの乗車枠・施設チケット", "体験ツアー・KOC取材時の乗車枠・入館券など", "貴事業ご提供を想定"),
]
for a, b, n in extras:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, SOFT)
    ws.merge_cells(f"B{r}:J{r}")
    put(ws, f"B{r}", b, 9, False, INK, SOFT)
    put(ws, f"K{r}", n, 9, False, GREY, SOFT)
    ws.row_dimensions[r].height = 30

# ---- オプション
r += 2
put(ws, f"A{r}", "■ オプション（各プランに追加可能・単価）", 12, True, NAVY, border=False)
r += 1
for c, t_ in zip("ABCD", ["項目", "内容", "単位", "単価（円）"]):
    put(ws, f"{c}{r}", t_, 10, True, "FFFFFF", HEAD, h="center")
ws.merge_cells(f"E{r}:K{r}")
put(ws, f"E{r}", "備考", 10, True, "FFFFFF", HEAD, h="center")
opts = [
    ("LINE公式アカウント 初期構築（繁体字）", "アカウント開設・認証申請、プロフィール／あいさつメッセージ、リッチメニュー設計（6ボタン・デザイン込み）、自動応答・FAQ、クーポン設定、権限設定、運用研修1回", "式", 800000, "構築期間 約8週間"),
    ("LINE公式アカウント 運用代行", "繁体字配信 月4回（便の日程に合わせた出発前案内・到着通知・乗車後アンケート）、チャット一次対応（平日）、月次レポート", "か月", 200000, "LINE公式アカウントの月額プラン料金は別途"),
    ("繁体字ランディングページ制作（予約導線付き）", "企画・構成・繁体字コピー・デザイン・実装（PC／スマートフォン）、便連動の送迎検索、バリアフリー情報、テーマ別モデルコース、LINE連携、UTM計測設定", "式", 1500000, "予約・決済システムとの連携範囲により変動"),
    ("繁体字LP 保守・更新", "季節ごとのコンテンツ更新（年4回）、軽微な修正、サーバー・ドメイン管理", "か月", 80000, ""),
    ("新光三越「日本商品展」出展支援", "固定費（出展申込・条件交渉、ブース企画・装飾、LINE友だち追加・抽選企画、SNS告知、撤収・実績レポート）＋成功報酬：売上の20％", "回", 500000, "百貨店手数料（売上の16％）・ブース賃料・人件費は実費。詳細は「新光三越 出展費用」シート"),
]
for a, b, u, p, n in opts:
    r += 1
    put(ws, f"A{r}", a, 10, True, INK, OPT)
    put(ws, f"B{r}", b, 9, False, INK, OPT)
    put(ws, f"C{r}", u, 10, False, INK, OPT, h="center")
    put(ws, f"D{r}", p, 10, False, INPUT, OPT, YEN, h="right")
    ws.merge_cells(f"E{r}:K{r}")
    put(ws, f"E{r}", n, 9, False, GREY, OPT)
    ws.row_dimensions[r].height = 50

# ---- 備考
r += 2
put(ws, f"A{r}", "■ 保証項目・備考", 12, True, NAVY, border=False)
notes = [
    "・GEO保証：各セット30組のキーワードのうち3組が、AI検索結果（Google AI Overview・ChatGPT・Gemini）に有効に表示されることを保証。未達成の場合は当該セット金額の30％を返金。",
    "・Threads KOC保証：1本あたり閲覧数10,000以上・エンゲージメント（いいね＋コメント）100以上・言及量1,000以上。未達成の場合は保証値に達するまで無償で追加投稿。",
    "・すべてのKOC・KOL投稿は、台湾・公平交易委員会の規範に従い「合作」を表記。人選・原稿は実施前に貴事業へ確認。",
    "・「仮単価」の項目（申請支援資料・欣傳媒 読者体験ツアー・ニュース風動画）は、範囲の確定および欣傳媒の正式見積により金額を確定します。",
    "・実施スケジュールは、補助金の採択時期とPOC期間が決まり次第ご提示します。",
    "・金額はすべて日本円・税別（消費税は別途）。媒体費・旅費・LINE公式アカウント月額プラン料金は含まない。",
    "・青字は数量・単価の入力値です。変更すると各プランの金額・合計が自動で再計算されます。",
]
for n in notes:
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    put(ws, f"A{r}", n, 9, False, GREY, border=False)
ws.freeze_panes = "A7"
ws.sheet_view.zoomScale = 90

# =====================================================================
# Sheet 2：新光三越 出展費用
# =====================================================================
ws2 = wb.create_sheet("新光三越 出展費用")
for k, v in {"A": 34, "B": 30, "C": 18, "D": 18, "E": 18, "F": 44}.items():
    ws2.column_dimensions[k].width = v
band(ws2, 1, "XXX様　新光三越「日本商品展」出展支援　費用構成と試算", "金額はすべて日本円・税別｜売上は会期中の税別売上｜インタセクト・コミュニケーションズ株式会社", ncol=6)

put(ws2, "A4", "■ 前提条件（黄色セルを入力）", 12, True, NAVY, border=False)
header(ws2, 5, ["項目", "値", "", "", "", "備考"])
inputs = [
    ("想定売上（税別・円）", 5000000, YEN, "試算例。会期・会場・商品構成に応じて入力してください"),
    ("固定費（円）", 500000, YEN, "当社：出展申込・条件交渉、ブース企画・装飾、LINE抽選企画、SNS告知、撤収・実績レポート"),
    ("成功報酬率（当社）", 0.20, "0%", "売上に対して（ご指定条件）"),
    ("百貨店手数料率（ブース費）", 0.16, "0%", "売上に対して、新光三越へのお支払い（ご指定条件）"),
    ("ブース賃料（実費・円）", None, YEN, "実費精算。確定後に入力"),
    ("販売スタッフ・通訳（実費・円）", None, YEN, "実費精算。確定後に入力"),
]
for i, (a, v, fmt, n) in enumerate(inputs):
    rr = 6 + i
    put(ws2, f"A{rr}", a, 10, True, INK, SOFT)
    put(ws2, f"B{rr}", v, 10, False, INPUT, YEL, fmt, h="right")
    put(ws2, f"F{rr}", n, 9, False, GREY)
    ws2.row_dimensions[rr].height = 30
ws2["B6"].comment = Comment("試算例の値です。実際の想定売上に置き換えてください。", "Intasect")

put(ws2, "A13", "■ 費用の内訳", 12, True, NAVY, border=False)
header(ws2, 14, ["費用項目", "計算方法", "金額（円）", "お支払い先", "", "備考"])
lines = [
    ("① 固定費（企画・出展支援）", "固定", "=B7", "当社", "前払い（出展決定時）"),
    ("② 成功報酬", "売上 × 成功報酬率", "=B6*B8", "当社", "会期終了後、売上確定時に精算"),
    ("③ 百貨店手数料（ブース費）", "売上 × 百貨店手数料率", "=B6*B9", "新光三越", "売上から差し引き"),
    ("④ ブース賃料", "実費", "=B10", "新光三越ほか", "実費精算"),
    ("⑤ 販売スタッフ・通訳", "実費", "=B11", "人材手配先", "実費精算"),
]
for i, (a, m, f, who, n) in enumerate(lines):
    rr = 15 + i
    put(ws2, f"A{rr}", a, 10, True, INK, SOFT)
    put(ws2, f"B{rr}", m, 10, False, INK, SOFT)
    put(ws2, f"C{rr}", f, 10, False, INK, SOFT, YEN, h="right")
    put(ws2, f"D{rr}", who, 10, False, INK, SOFT, h="center")
    put(ws2, f"E{rr}", None, 10, False, INK, SOFT)
    put(ws2, f"F{rr}", n, 9, False, GREY, SOFT)
    ws2.row_dimensions[rr].height = 26
put(ws2, "A20", "費用合計（税別）", 11, True, NAVY, GOLD)
put(ws2, "B20", "①〜⑤", 11, True, NAVY, GOLD)
put(ws2, "C20", "=SUM(C15:C19)", 11, True, NAVY, GOLD, YEN, h="right")
for c in "DEF":
    put(ws2, f"{c}20", None, 11, True, NAVY, GOLD)
put(ws2, "A21", "うち当社へのお支払い（①＋②）", 10, True, INK)
put(ws2, "C21", "=C15+C16", 10, True, INK, fmt=YEN, h="right")
put(ws2, "A22", "売上に対する費用率", 10, True, INK)
put(ws2, "C22", '=IF(B6>0,C20/B6,0)', 10, True, INK, fmt="0.0%", h="right")
put(ws2, "A23", "売上 − 費用合計（商品原価・輸送費は含まず）", 10, True, INK)
put(ws2, "C23", "=B6-C20", 10, True, INK, fmt=YEN, h="right")

put(ws2, "A25", "■ 売上別の試算（④⑤実費は除く）", 12, True, NAVY, border=False)
header(ws2, 26, ["想定売上（税別）", "① 固定費", "② 成功報酬", "③ 百貨店手数料", "①〜③合計", "うち当社へのお支払い（①＋②）"])
for i, sales in enumerate([3000000, 5000000, 10000000, 20000000]):
    rr = 27 + i
    put(ws2, f"A{rr}", sales, 10, False, INPUT, None, YEN, h="right")
    put(ws2, f"B{rr}", "=$B$7", 10, fmt=YEN, h="right")
    put(ws2, f"C{rr}", f"=A{rr}*$B$8", 10, fmt=YEN, h="right")
    put(ws2, f"D{rr}", f"=A{rr}*$B$9", 10, fmt=YEN, h="right")
    put(ws2, f"E{rr}", f"=SUM(B{rr}:D{rr})", 10, True, fmt=YEN, h="right")
    put(ws2, f"F{rr}", f"=B{rr}+C{rr}", 10, True, fmt=YEN, h="right")

notes2 = [
    "・固定費50万円・成功報酬（売上の20％）・百貨店手数料（売上の16％）・ブース賃料と人件費の実費精算は、ご指定の条件にもとづく構成です。",
    "・商品の仕入れ・輸送費、会場までの交通・宿泊費は含みません。",
    "・会場・会期・ブース面積は、新光三越の年間計画と出展審査により確定します（推奨時期：2027年10〜11月の周年祭）。",
    "・黄色セル（青字）を変更すると、内訳と試算が自動で再計算されます。",
]
for i, n in enumerate(notes2):
    rr = 32 + i
    ws2.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=6)
    put(ws2, f"A{rr}", n, 9, False, GREY, border=False)

# =====================================================================
# Sheet 3：KPI目標（プラン別）
# =====================================================================
ws3 = wb.create_sheet("KPI目標")
for k, v in {"A": 24, "B": 24, "C": 24, "D": 24, "E": 24, "F": 28, "G": 20}.items():
    ws3.column_dimensions[k].width = v
band(ws3, 1, "XXX様　プラン別 KPI目標一覧", "保証＝契約に明記（未達時の措置あり）／目標値＝実績に基づく努力目標／承諾交付＝必ず納品する数量", ncol=7)
header(ws3, 4, ["施策", "KPI指標", "小プラン", "中プラン", "大プラン", "測定方法", "区分"])
TAG = {"保証": ("9C5700", "FDF3DC"), "目標値": ("22406B", "EEF2FA"), "承諾交付": ("048F3E", "E9F9EF")}
kpi = [
    ("申請支援", "申請書添付用資料", "1式", "1式", "1式", "納品物", "承諾交付"),
    ("声量（全体）", "「四國」の総言及量", "＋30％（472,744 → 614,567）", "＋30％（472,744 → 614,567）", "＋30％（472,744 → 614,567）", "Pandora", "保証"),
    ("", "月次レポート", "6本", "10本", "12本", "レポート提出", "承諾交付"),
    ("Threads公式アカウント", "運用期間・投稿数", "6か月・36本以上", "10か月・60本以上", "12か月・72本以上", "投稿カレンダー＋投稿リンク", "承諾交付"),
    ("", "フォロワー数", "3,000〜5,000人", "8,000〜10,000人", "10,000〜15,000人", "Threadsインサイト", "目標値"),
    ("", "平均エンゲージメント率", "4％以上", "4％以上", "4％以上", "Threadsインサイト", "目標値"),
    ("Threads KOC", "投稿数", "8本", "4本", "6本", "投稿リンク", "承諾交付"),
    ("", "閲覧数（1本あたり10,000以上）", "80,000以上", "40,000以上", "60,000以上", "プラットフォーム数値", "保証"),
    ("", "1本あたりエンゲージメント・言及量", "100以上・1,000以上", "100以上・1,000以上", "100以上・1,000以上", "スクリーンショット＋Pandora", "保証"),
    ("GEO", "ニュース・掲示板記事", "—", "ニュース6・掲示板6", "ニュース12・掲示板12", "掲載リンク一覧", "承諾交付"),
    ("", "キーワード設計", "—", "30組", "60組", "キーワード一覧", "承諾交付"),
    ("", "AI検索掲載", "—", "3組", "6組", "月次AI検索モニタリング", "保証（未達時30％返金）"),
    ("欣傳媒", "旅行特集", "—", "1本（ツアーレポート）", "2本", "掲載リンク＋配信レポート", "承諾交付"),
    ("", "読者体験ツアー", "—", "1回（読者約10名・KOL2名）", "1回（読者約10名・KOL2名）＋ニュース風動画1本", "参加者リスト・掲載リンク", "承諾交付"),
    ("", "参加者アンケート", "—", "参加者全員から回収", "参加者全員から回収", "アンケート集計", "承諾交付"),
    ("便連動広告", "運用・月次レポート", "—", "—", "6か月", "広告管理画面レポート", "承諾交付"),
]
for i, row in enumerate(kpi):
    rr = 5 + i
    put(ws3, f"A{rr}", row[0], 10, True, INK, SOFT)
    put(ws3, f"B{rr}", row[1], 10, True, INK)
    for j, c in enumerate("CDE"):
        put(ws3, f"{c}{rr}", row[2 + j], 9.5, False, INK, h="center")
    put(ws3, f"F{rr}", row[5], 9, False, INK)
    e = row[6]
    base = "保証" if e.startswith("保証") else e
    put(ws3, f"G{rr}", e, 9.5, True, TAG[base][0], TAG[base][1], h="center")
    ws3.row_dimensions[rr].height = 34
rr = 5 + len(kpi) + 1
for n in [
    "・「保証」：未達成時の対応を契約書に明記（GEO：AI検索掲載が未達のセットは金額の30％を返金／KOC：保証値に達するまで無償で追加投稿／声量：施策の追加実施で対応）。",
    "・「目標値」：同種アカウントの運用実績にもとづく目標。契約上の保証値ではなく、月次レポートで進捗を確認し施策を調整。",
    "・「承諾交付」：必ず納品する数量・成果物。投稿リンク・掲載リンク・スクリーンショットで交付を記録。",
    "・声量の基準値はPandora実測値（データ期間 2025/9/1〜2026/9/2、キーワード「四國」、台湾・香港・マカオ、総言及量472,744）。実施時は施策開始前日までの最新データを基準値とする。",
    "・POCの送迎利用人数・周遊率・満足度などの目標値は、予算とPOCの規模（台数・運行日・区間）が決まり次第、貴事業と共同で設定する。",
]:
    ws3.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=7)
    put(ws3, f"A{rr}", n, 9, False, GREY, border=False)
    rr += 1

for w in wb:
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.orientation = "landscape"
wb.calculation.fullCalcOnLoad = True
wb.save(OUT)
print("saved", OUT)
