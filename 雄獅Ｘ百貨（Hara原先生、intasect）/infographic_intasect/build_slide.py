"""單頁 infographic：Intasect B 端企業網絡 × 騰雲 T-Space ASP × 雄獅（雙向導流）"""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402
from shelley_deck import Deck, text_w  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
A = lambda n: os.path.join(HERE, "assets", n)  # noqa: E731

RED, CYAN, GOLD = "#C8102E", "#1DB7D3", "#FFC000"
d = Deck(theme={"frame": RED}, footer_logos=["brand/accucrazy-dark.png"])

s = d.info("合作示意圖：透過 Intasect，雄獅一次接上日本自治體與百貨的流量",
           label="合作架構", numbered=False,
           banner="日本客人從企業官網走進雄獅，台灣客人從雄獅走進日本地方——中心都是騰雲 T-Space",
           source="客戶名單出處：Intasect 事業紹介資料（2026/10）主要取引先・IntaPay 導入實例；intasect.com 導入事例；"
                  "PR TIMES（2025/02 白馬谷 IntaPay、IntaEvent）；長岡花火、淡路島 Pasona 為 Intasect 提供之合作對象")


def arrow(x, y, w, h, col, left=False):
    a = d.rect(s, x, y, w, h, col, MSO_SHAPE.LEFT_ARROW if left else MSO_SHAPE.RIGHT_ARROW)
    return a


def pill(x, y, text, fill, fg="white", size=9, h=0.25, bold=False, line=None):
    w = text_w(text, 0.155 * size / 11.2, 0.085 * size / 11.2) + 0.14
    if line:
        r = d.round(s, x, y, w, h, "white", 0.5)
        r.line.color.rgb = d.col(line)
        r.line.width = Pt(0.75)
    else:
        d.round(s, x, y, w, h, fill, 0.5)
    d.tx(s, x, y, w, h, text, size, color=fg, bold=bold, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return w


def chips(x, y, w, items, gap=0.05, row_gap=0.05, **kw):
    """自動換行的 chip 群；items 可為 str 或 (str, featured)。回傳結束 y。"""
    cx, cy = x, y
    h = kw.get("h", 0.25)
    for it in items:
        t, feat = (it, False) if isinstance(it, str) else it
        size = kw.get("fsize", 9.5) if feat else kw.get("size", 8.5)
        iw = text_w(t, 0.155 * size / 11.2, 0.085 * size / 11.2) + 0.14
        if cx + iw > x + w + 0.01:
            cx, cy = x, cy + h + row_gap
        if feat:
            pill(cx, cy, t, RED, size=size, h=h, bold=True)
        else:
            pill(cx, cy, t, None, fg="ink", size=size, h=h, line="#CFC8CA")
        cx += iw + gap
    return cy + h


# ---------------------------------------------------------------- 版面座標
LX, LW = 0.6, 2.5            # 左：雄獅
HX, HW = 4.2, 2.1            # 中：T-Space
RX = 7.4                     # 右：Intasect
RW = 12.73 - RX
G1, G2 = (LX + LW, HX), (HX + HW, RX)
TOP, Y0, Y1 = 1.18, 1.55, 6.1

d.tx(s, LX, TOP, LW, 0.3, "雄獅集團", 13, color=RED, bold=True)
d.tx(s, HX, TOP, HW, 0.3, "騰雲", 13, color="navy", bold=True, align=PP_ALIGN.CENTER)
d.tx(s, RX, TOP, RW, 0.3, "Intasect B 端企業網絡", 13, color=RED, bold=True)


# ---------------------------------------------------------------- 左：雄獅兩張卡
def lion_card(y, title, sub, img, who):
    d.round(s, LX, y, LW, 2.15, CYAN, 0.08)
    d.tx(s, LX + 0.14, y + 0.15, 1.6, 0.6, title, 12.5, color="white", bold=True, spacing=1.1)
    d.tx(s, LX + 0.14, y + 0.85, 1.55, 1.2, sub, 9, color="white", spacing=1.25)
    d.fit(s, img, LX + LW - 0.95, y + 0.1, 0.88, 1.95)
    pill(LX + 0.14, y + 1.78, who, "navy", size=8.5, h=0.24, bold=True)


lion_card(Y0, "國際版 App\nLionTrip", "下載 App、成為\n雄獅國際會員，\n購買雄獅日本行程", A("app_intl.jpg"), "日本客人")
lion_card(Y1 - 2.15, "台灣官網・App\n雄獅旅遊", "開設對應團，\n帶台灣客人造訪\n自治體・購買票券", A("app_tw.jpg"), "台灣客人")

# ---------------------------------------------------------------- 中：T-Space ASP
HY, HH = Y0, Y1 - Y0
d.round(s, HX, HY, HW, HH, GOLD, 0.08)
d.tx(s, HX, HY + 0.18, HW, 0.3, "雙向交流的中心", 9.5, color="navy", bold=True, align=PP_ALIGN.CENTER)
d.tx(s, HX, HY + 0.45, HW, 0.75, "騰雲 T-Space\nASP 平台", 16.5, color="navy", bold=True,
     align=PP_ALIGN.CENTER, spacing=1.05)
d.rect(s, HX + 0.3, HY + 1.3, HW - 0.6, 0.012, "navy")


def lp(y, head, body, col):
    d.round(s, HX + 0.15, y, HW - 0.3, 0.95, "white", 0.1)
    d.rect(s, HX + 0.15, y, 0.07, 0.95, col)
    d.tx(s, HX + 0.32, y + 0.08, HW - 0.5, 0.25, head, 10, color=col, bold=True)
    d.tx(s, HX + 0.32, y + 0.36, HW - 0.5, 0.55, body, 8.5, color="ink", spacing=1.2)


lp(HY + 1.45, "Landing Page ①", "引導下載雄獅國際版 App\n／瀏覽雄獅日本行程", RED)
lp(HY + 2.5, "導購頁 ②", "自治體行程報名\n／Intasect 票券購買", CYAN)
d.tx(s, HX + 0.1, HY + 3.6, HW - 0.2, 0.9, "點擊追蹤・成效報表\n導客結算・分潤", 9.5, color="navy",
     bold=True, align=PP_ALIGN.CENTER, spacing=1.3)

# ---------------------------------------------------------------- 箭頭＋步驟說明
AY1, AY2 = 2.35, 4.95


def lane(gap, y, col, left, top, bottom):
    x0, x1 = gap[0] + 0.07, gap[1] - 0.07
    arrow(x0, y, x1 - x0, 0.34, col, left=left)
    d.tx(s, gap[0], y - 0.6, gap[1] - gap[0], 0.53, top, 8.5, color=col, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, spacing=1.1)
    d.tx(s, gap[0], y + 0.42, gap[1] - gap[0], 0.5, bottom, 8.5, color="mid", align=PP_ALIGN.CENTER, spacing=1.1)


# 方向 ①（紅）：Intasect 企業官網 → T-Space LP → 雄獅國際版 App
lane(G2, AY1, RED, True, "① 企業官網\n放雄獅 Banner", "點擊後\n進入 LP")
lane(G1, AY1, RED, True, "LP 導流\n下載 App", "或看雄獅\n日本行程")
# 方向 ②（青）：雄獅台灣官網 → T-Space → 自治體行程／Intasect 票券
lane(G1, AY2, CYAN, False, "② 開對應團\n導入 T-Space", "台灣客人\n報名行程")
lane(G2, AY2, CYAN, False, "造訪自治體\n購買票券", "Intasect\n販售票券")

# ---------------------------------------------------------------- 右：Intasect 企業網絡
d.round(s, RX, Y0, RW, HH, "soft", 0.04)
IX, IW = RX + 0.14, RW - 0.28

stats = [("4萬+", "IntaPay\n導入店舖"), ("2,500億", "年流通額\n（日圓）"), ("951名", "集團\n員工")]
sw = (IW - 0.16) / 3
for i, (n, l) in enumerate(stats):
    x = IX + i * (sw + 0.08)
    d.round(s, x, Y0 + 0.1, sw, 0.42, "white", 0.15)
    d.tx(s, x + 0.12, Y0 + 0.13, 0.95, 0.36, n, 14, color=RED, bold=True, anchor=MSO_ANCHOR.MIDDLE,
         font=d.num_font)
    d.tx(s, x + sw - 0.82, Y0 + 0.13, 0.75, 0.36, l, 7.5, color="mid", anchor=MSO_ANCHOR.MIDDLE, spacing=1.05)


def group(y, head, items, **kw):
    d.rect(s, IX, y + 0.04, 0.05, 0.16, RED)
    d.tx(s, IX + 0.12, y, IW, 0.24, head, 9.5, bold=True)
    return chips(IX, y + 0.27, IW, items, **kw) + 0.09


y = Y0 + 0.62
y = group(y, "地方自治體・DMO・觀光地（重點）", [
    ("富良野市｜智慧城市", True), ("四國｜香川・高知", True), ("長岡花火大會", True),
    ("白馬谷｜白馬村・小谷村・大町市", True), ("淡路島 Pasona", True),
    "京都府", "三鷹市", "平取町", "美瑛町觀光協會", "占冠村", "小樽堺町通商店街", "有馬溫泉",
    "河口湖旅館協同組合", "福井縣立恐龍博物館", "舊福岡縣公會堂", "祇園祭 函谷鉾",
    "海洋博美ら海花火大會", "岩岳度假村", "和島夢來考房",
], h=0.23, fsize=9, size=8)
y = group(y, "百貨・零售", [
    ("阪急阪神百貨店", True), ("高島屋", True), ("近鐵百貨店", True), ("Ryubo 琉球百貨", True),
    "唐吉訶德（PPIH）",
], h=0.23, fsize=9, size=8)
y = group(y, "交通・航空・休閒", [
    "JR 東日本", "JR 西日本", "JR 九州", "JR 東日本 View Tourism", "JR 東日本企劃", "Toki Air",
    "富士急行", "東方樂園（Oriental Land）", "東京晴空塔", "計程車 12,000 台",
], h=0.22, size=7.5)
y = group(y, "金融・企業", [
    "三井住友 FG", "SBI", "Sony 銀行", "Sony Payment Services", "Aplus", "野村總研", "Toyota",
], h=0.22, size=7.5)
print("right panel content ends at", round(y, 2), "(limit", Y1, ")")

d.save(os.path.join(HERE, "Intasect合作示意_infographic.pptx"))
