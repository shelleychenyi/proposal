import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from shelley_deck import Deck, W, H, _alpha  # noqa: E402

os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = "assets/"
LALA = A + "logo/logo@3x_org.png"
MOP = A + "logo/logo@3x_org_mitsui.png"
TC = "brand/turncloud.png"
BLUE, ORANGE, MINT, PINK, CORAL = "#2B67B0", "#F39A1E", "#22C2A0", "#FF6FA3", "#FF6F61"
IDEA_VIDEO = A + "video/idea_bg.mp4" if os.path.exists(A + "video/idea_bg.mp4") else None

META = {"video": {}, "special": {}}
d = Deck(theme={"frame": BLUE, "accent": ORANGE}, footer_logos=[TC])


def phone(s, key, x, y, h, video=True, tag=True):
    """手機框＋Prototype 錄影（poster = 截圖）。回傳寬度。"""
    w = h * 390 / 844
    d.round(s, x - 0.07, y - 0.07, w + 0.14, h + 0.14, "#0E1A33", 0.12)
    poster = A + f"poster_r/{key}.jpg"
    vid = A + f"video_r/{key}.mp4" if video else None
    d.movie(s, vid, poster, x, y, w, h)
    if video:
        META["video"].setdefault(d.n, []).append([key, x, y, w, h])
    if tag:
        d.ai_tag(s, x + 0.08, y + h + 0.14, "Prototype 錄影" if video else "UI 示意")
    return w


def ugc(s, key, x, y, w, h, cap=None):
    """真實社群貼文截圖（IG 嵌入頁）。"""
    px, py, pw, ph = d.fit(s, A + f"ugc/{key}_c.png", x, y, w, h - (0.3 if cap else 0), border=True)
    if cap:
        d.tx(s, x, py + ph + 0.06, w, 0.25, cap, 9, color="grey", align=PP_ALIGN.CENTER)
    return px, py, pw, ph


def bench(title, brand, shots, good, borrow, banner):
    s = d.info(title, label="Benchmark｜" + brand, banner=banner,
               source="Data source: App Store 官方截圖（2026/11）")
    for i, f in enumerate(shots):
        d.fit(s, A + f"bench/{f}", 0.6 + i * 2.32, 1.3, 2.2, 4.75, border=True)
    d.tx(s, 7.75, 1.3, 5.0, 0.35, "好在哪裡", 13, color="frame", bold=True)
    d.callouts(s, 7.75, 1.75, 5.0, good, gap=0.92)
    yb = 1.75 + 0.92 * len(good) + 0.05
    d.rect(s, 7.75, yb, 5.0, 0.02, "line")
    d.tx(s, 7.75, yb + 0.15, 5.0, 0.35, "LaLa Quest 借鏡", 13, color=ORANGE, bold=True)
    d.tx(s, 7.75, yb + 0.55, 5.0, 1.3, borrow, 12.5, bold=True, spacing=1.55)
    return s


def phone_demo(title, label, key, points, banner, photo=None, keys2=None, source=None, clip=None):
    s = d.info(title, label=label, banner=banner, source=source)
    x = 0.9
    w = phone(s, key, x, 1.3, 4.55)
    x += w + 0.45
    for k in keys2 or []:
        w2 = phone(s, k, x, 1.3, 4.55)
        x += w2 + 0.45
    if clip:  # AI 示意影片（16:9），置中於右側區塊
        pw = 9.0 - x
        ph = pw * 9 / 16
        py = 1.3 + (4.55 - ph) / 2
        d.movie(s, A + f"video_r/{clip}.mp4", A + f"poster_r/{clip}.jpg", x, py, pw, ph)
        META["video"].setdefault(d.n, []).append([clip, x, py, pw, ph])
        d.ai_tag(s, x, py + ph + 0.12, "AI 示意影片")
    elif photo:
        pw = 9.0 - x
        px, py, pw, ph = d.fit(s, photo, x, 1.3, pw, 4.55)
        d.ai_tag(s, px + 0.1, py + 0.1)
    d.tx(s, 9.35, 1.35, 3.4, 0.35, "畫面重點", 13, color="frame", bold=True)
    gap = min(1.15, 4.6 / max(1, len(points)))
    d.callouts(s, 9.35, 1.85, 3.4, points, gap=gap)
    return s


NAVY, GOLD2 = "#13294B", "#8C6E3C"


def core_map(s, y=1.3):
    """核心＋加購架構：三個加購模組插在同一個核心上。"""
    adds = [("PLAY 遊戲包", PINK, "簽到 Streak・Quest 任務\nStamp Rally・LaLa Capsule\nMatsuri Pass"),
            ("AI 智慧包", BLUE, "AI 發票掃描（1 秒）\nAsk LaLa 管家\nFor You 個人化推薦"),
            ("BUZZ 口碑包", ORANGE, "Pandora LaLa Buzz\nBuzz Score＋AI 摘要\nReal Talk 真心話")]
    d.tx(s, 0.72, y, 8, 0.3, "加購 ADD-ONS｜提升體驗・準備好再開", 12, color=GOLD2, bold=True)
    for i, (t, col, body) in enumerate(adds):
        x = 0.72 + i * 3.98
        d.round(s, x, y + 0.38, 3.78, 1.55, "soft", 0.08)
        d.rect(s, x, y + 0.38, 0.09, 1.55, col)
        d.tx(s, x + 0.3, y + 0.5, 3.3, 0.35, t, 15, color=col, bold=True)
        d.tx(s, x + 0.3, y + 0.88, 3.4, 1.0, body, 11.5, bold=True, spacing=1.4)
        d.rect(s, x + 1.79, y + 2.0, 0.2, 0.28, "grey", MSO_SHAPE.DOWN_ARROW)
    cy = y + 2.38
    d.round(s, 0.72, cy, W - 1.44, 2.05, NAVY, 0.06)
    d.tx(s, 1.0, cy + 0.14, 9, 0.35, "核心 CORE｜LaLa Quest 基本版・帶來人流與註冊", 13, color="#E8D6AE", bold=True)
    cores = [("會員身份＋四級", "首頁 QR・Rookie → Legend"),
             ("LaLa Park 車牌停車", "車牌＝會員・等級送時數\n點數折抵剩餘停車費"),
             ("LaLa Go 巴士", "LTH 購票・時刻表\n乘車提醒・KLIA 接駁"),
             ("點數＋e-Voucher", "發票登錄・票券錢包\n乘車券與店家優惠")]
    for i, (t, body) in enumerate(cores):
        x = 1.0 + i * 2.95
        d.round(s, x, cy + 0.6, 2.75, 1.25, "#1E3A63", 0.08)
        d.tx(s, x + 0.18, cy + 0.7, 2.5, 0.35, t, 13.5, color="white", bold=True)
        d.tx(s, x + 0.18, cy + 1.07, 2.5, 0.75, body, 10.5, color="#C9D3E0", spacing=1.35)



# ---------------------------------------------------------------- v4 helpers: What's New + scenario demo
SC_NAVY, SC_GOLD, SC_GOLD_L = "#13294B", "#B8975A", "#E8D6AE"
PAGES, PAGE_REFS = {}, []


def whats_new(title, label, banner, head, rows):
    """Before → After table that doubles as a feature directory (p.N filled in at the end)."""
    s = d.info(title, label=label, banner=banner)
    X = [(0.6, 1.75), (2.4, 3.3), (6.1, 4.75), (10.95, 1.15), (12.2, 0.6)]
    y0 = 1.25
    d.rect(s, 0.6, y0, 12.15, 0.36, SC_NAVY)
    for i, (x, w) in enumerate(X):
        d.tx(s, x + (0.12 if i < 3 else 0), y0 + 0.08, w, 0.25, head[i], 10.5, color=SC_GOLD_L if i == 2 else "white",
             bold=True, align=PP_ALIGN.LEFT if i < 3 else PP_ALIGN.CENTER)
    rh = 0.535
    for r, (feat, before, after, pkg, key) in enumerate(rows):
        y = y0 + 0.42 + r * rh
        new = "NEW" in pkg
        if r % 2 == 0:
            d.rect(s, 0.6, y, 12.15, rh, "soft")
        if new:
            d.rect(s, 0.6, y, 0.07, rh, SC_GOLD)
        d.tx(s, 0.72, y, 1.65, rh, feat, 12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        d.tx(s, 2.52, y, 3.15, rh, before, 10, color="grey", anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
        d.rect(s, 5.78, y + rh / 2 - 0.09, 0.2, 0.18, SC_GOLD, MSO_SHAPE.RIGHT_ARROW)
        d.tx(s, 6.22, y, 4.65, rh, after, 11, bold=True, color=SC_NAVY, anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)
        core = pkg.startswith(("Core", "核心"))
        d.round(s, 11.0, y + 0.11, 1.05, rh - 0.22, SC_NAVY if core else SC_GOLD, 0.5)
        d.tx(s, 11.0, y + 0.11, 1.05, rh - 0.22, pkg, 8.5, color="white", bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        tb = d.tx(s, 12.2, y, 0.6, rh, "p.", 11, color="frame", bold=True, align=PP_ALIGN.CENTER,
                  anchor=MSO_ANCHOR.MIDDLE)
        PAGE_REFS.append((tb, key))
    return s


def scene(title, label, banner, photo, phones, beats, stats=None, chip=None, source=None):
    """Scenario demo: scene photo + story strip (time-stamped beats) + prototype recordings (+ big stats)."""
    s = d.info(title, label=label, banner=banner, source=source)
    pw_phone = 4.55 * 390 / 844
    phones_w = len(phones) * pw_phone + (len(phones) - 1) * 0.3
    stats_w = 3.2 if stats else 0
    pw = 12.15 - 0.4 - phones_w - (stats_w + 0.4 if stats else 0)
    d.cover_pic(s, photo, 0.6, 1.3, pw, 2.95)
    d.ai_tag(s, 0.7, 1.38)
    if chip:
        d.tag(s, 0.6, 3.83, chip, col=SC_GOLD, size=10.5, h=0.42)
    d.round(s, 0.6, 4.33, pw, 1.55, SC_NAVY, 0.06)
    cw = (pw - 0.2) / len(beats)
    for i, (t, line) in enumerate(beats):
        x = 0.7 + i * cw
        d.tx(s, x + 0.15, 4.45, cw - 0.3, 0.3, t, 11.5, color=SC_GOLD_L, bold=True)
        d.tx(s, x + 0.15, 4.78, cw - 0.3, 1.05, line, 10.5, color="white", spacing=1.25)
        if i:
            d.rect(s, x, 4.5, 0.012, 1.2, "#3A5378")
    x = 0.6 + pw + 0.4
    for k in phones:
        phone(s, k, x, 1.3, 4.55)
        x += pw_phone + 0.3
    if stats:
        x += 0.1
        hh = (4.6 - 0.15 * (len(stats) - 1)) / len(stats)
        for i, (big, lab) in enumerate(stats):
            y = 1.3 + i * (hh + 0.15)
            d.round(s, x, y, stats_w, hh, "soft", 0.08)
            d.rect(s, x, y, 0.07, hh, SC_GOLD)
            d.tx(s, x + 0.3, y + 0.18, stats_w - 0.4, 0.6, big, 26, color=SC_NAVY, bold=True)
            d.tx(s, x + 0.3, y + 0.85, stats_w - 0.4, 0.6, lab, 11, color="mid", bold=True, spacing=1.2)
    return s


def fill_page_refs():
    for tb, key in PAGE_REFS:
        tb.text_frame.paragraphs[0].runs[0].text = "p.%d" % PAGES[key]


# ---------------------------------------------------------------- 封面
d.cover("MSP 會員 App\n3.0 改版提案。", "LaLa Quest｜每一次來，都在升級。", "2026.11",
        company="TURN CLOUD TECHNOLOGY SERVICE INC.", logos=[LALA, MOP], image=A + "mock_hero3.jpg")
d.toc([("現況與洞察", "機會"), ("標竿學習", "標竿"), ("App 3.0 全貌", "全貌"), ("核心｜會員分級", "分級"),
       ("核心｜LaLa Park 停車", "停車"), ("核心｜LaLa Go 巴士", "巴士"), ("加購｜遊戲包", "遊戲"),
       ("加購｜AI 智慧包", "AI"), ("加購｜口碑包 LaLa Buzz", "口碑"), ("落地與 KPI", "落地")])

# ---------------------------------------------------------------- 1 現況與洞察
PD = A + "pandora/"
PSRC = "Data source: Pandora 輿情報告「Lalaport&BBCC」2026/5/3–2026/10/31，N=3,696（Instagram、Threads）；掃 QR 看完整報告"


def qr_pair(s, x, y, size=1.05, gap=0.35, label=True):
    """兩份 Pandora 報告 QR。"""
    for i, (k, nm) in enumerate([("volume", "聲量報告"), ("insight", "洞察報告")]):
        xx = x + i * (size + gap)
        d.fit(s, PD + f"qr_{k}.png", xx, y, size, size, border=True)
        if label:
            d.tx(s, xx - 0.15, y + size + 0.04, size + 0.3, 0.25, "Pandora " + nm, 9, color="mid", bold=True,
                 align=PP_ALIGN.CENTER)


d.divider("現況與洞察", "大家很愛 LaLaport，\n只是 App 沒接住這份熱度", key="機會")

s = d.info("一頁看懂：核心功能把人帶進來，加購功能讓人留下來", label="Executive Summary",
           banner="核心先上：停車、巴士、等級，讓每一位來館的人第一天就有理由註冊")
d.columns(s, [("洞察", "#8A94A6", "有熱度，缺導客工具",
               "半年 3,696 篇、90.7% 正面\n最大負評：停車\nLTH＋KLIA 帶來大量旅客\n只有 5% 會員用 App 集點"),
              ("解法", BLUE, "一個核心＋三個加購",
               "核心：四級會員、車牌停車\n核心：LaLa Go 巴士購票\n核心：點數＋e-Voucher\n加購：遊戲・AI・口碑"),
              ("收益", ORANGE, "更多來客、更多會員",
               "每一個車牌＝一位會員\n每一張車票＝一筆館內消費\n集點率 5% → 20%\n各館共用一個會員身份")])

s = d.info("洞察①　大家很愛 LaLaport：半年 3,696 篇、九成正面", label="Pandora 聲量報告",
           banner="聲量和好感都在，缺的是一個把這份熱度「記回會員身上」的 App", source=PSRC)
d.fit(s, PD + "v_stats.png", 0.6, 1.28, 6.3, 2.0, border=True)
d.fit(s, PD + "i_sentdist.png", 0.6, 3.38, 6.3, 2.7, border=True)
d.tx(s, 7.35, 1.3, 5.4, 0.3, "Pandora 告訴我們", 13, color="frame", bold=True)
for i, (big, lab, desc) in enumerate([("90.7%", "正面情緒", "Very Positive 28.1%＋Positive 62.6%，負評僅 1.2%"),
                                      ("510 萬", "總聲量", "165 萬讚、2 萬則留言，8 月單月破 120 萬"),
                                      ("5%", "用 App 集點的會員", "熱度在社群，不在 App 裡（客戶提供）")]):
    y = 1.75 + i * 0.95
    d.tx(s, 7.35, y, 1.9, 0.6, big, 28, color=ORANGE if i == 2 else "frame", bold=True)
    d.tx(s, 9.3, y + 0.02, 3.5, 0.3, lab, 13, bold=True)
    d.tx(s, 9.3, y + 0.33, 3.5, 0.5, desc, 10.5, color="mid")
d.rect(s, 7.35, 4.65, 5.4, 0.02, "line")
d.tx(s, 7.35, 4.8, 2.2, 1.0, "掃描看\n完整 Pandora\n報告 →", 12.5, bold=True, color="frame", spacing=1.35)
qr_pair(s, 9.35, 4.75, size=1.0, gap=0.4)

s = d.info("洞察②　年輕人為 ACG、K-pop、電影而來", label="Pandora 洞察報告",
           banner="App 的遊戲化與角色設計，就是對著這群人：ACG Base、Photoism、GSC 粉絲場、Bon Odori",
           source=PSRC)
d.fit(s, PD + "i_keyword.png", 0.6, 1.28, 6.2, 3.08, border=True)
d.callouts(s, 0.75, 4.55, 6.0, [("ACG 主場", "ACG Base、Ani-One POP、Doko Koko 聯名咖啡、Anime Fest"),
                                ("K-pop＋電影", "Photoism 偶像相框、GSC Chiikawa／蠟筆小新粉絲場")], gap=0.72)
d.fit(s, PD + "i_positive.png", 7.05, 1.28, 5.7, 3.08, border=True)
d.tx(s, 7.05, 4.5, 4.3, 1.4, "Pandora AI 好評摘要：\n「LaLaport BBCC 是吉隆坡的潮流文化據點」——\n這群人習慣收集、打卡、追限定，正是遊戲化會員的最佳用戶。",
     12, bold=True, spacing=1.5)
d.fit(s, PD + "qr_insight.png", 11.65, 4.5, 0.95, 0.95, border=True)
d.tx(s, 11.42, 5.47, 1.4, 0.25, "洞察報告", 9, color="mid", bold=True, align=PP_ALIGN.CENTER)

s = d.info("洞察③　最大負評是停車：App 早有解，卻藏在 News 裡", label="Pandora 洞察報告｜App 現況",
           banner="大馬商場早已用車牌辨識停車：把 LPR 綁上會員，停車就變成註冊的理由",
           source=PSRC + "；App 實機截圖 2026/11")
d.fit(s, PD + "i_negative.png", 0.6, 1.28, 6.1, 3.28, border=True)
d.tx(s, 0.75, 4.72, 5.9, 1.3, "Pandora 負評摘要：停車費太貴、停車場出入口封閉、\n館內訊號差導致 QR 付款困難。\n→ 3.0：註冊車牌，攝影機自動辨識；免費時數跟著等級走（3H → 全日），剩下用點數折抵。",
     12, bold=True, spacing=1.55)
d.fit(s, A + "current_app.jpg", 7.0, 1.28, 5.75, 1.78, border=True)
d.ai_tag(s, 7.1, 1.36, "現行 App 實機畫面")
d.callouts(s, 7.0, 3.3, 5.75, [("首頁＝廣告牆", "Banner、News、Voucher 都在推，沒有「我」"),
                               ("免費停車藏在 News", "MSP Member Free 3H Parking 只是一則活動"),
                               ("紙本停車券，沒綁車牌", "停車跟會員身份、點數完全沒有連動")], gap=0.9)

s = d.info("洞察④　旅客本來就在館內經過：LaLaport 有 LTH 巴士站、MOP 緊鄰機場", label="桌面調查｜交通",
           banner="等車的時間就是逛街的時間：在 App 賣票、附上 e-Voucher、提醒上車",
           source="Data source: busonlineticket.com LaLaport Transportation Hub 頁面（2026/11）；railtravelstation.com MOP KLIA Sepang 接駁資訊；班次以業者公告為準")
d.num_cards(s, [("8", "LTH 巴士業者", "LaLaport BBCC LG1 East Atrium\n吉隆坡 ⇄ 新加坡、新山\n約 06:30–23:45 發車"),
                ("~10 分", "MOP ⇄ KLIA 免費接駁", "KLIA T1 約 10 分、klia2 約 20 分\n轉機旅客、候機觀光客"),
                ("0", "目前與商場的連動", "車票在第三方網站購買\n沒有會員、沒有優惠券\n也沒有「先逛再上車」的提醒")], y=1.35, h=2.55)
d.fit(s, A + "app/lth_bay.jpg", 0.72, 4.05, 3.2, 2.0)
d.ai_tag(s, 0.82, 4.12)
d.callouts(s, 4.2, 4.1, 8.4, [("旅客都會提早到", "跨境巴士要求提早報到：30–90 分鐘的空檔可以被填滿"),
                              ("他們需要提醒，不是廣告", "「30 分鐘後上車，RM10 優惠券還沒用」把等待變成消費")], gap=0.95)

d.statement("IDEA", "LaLa Quest\n停車、搭車、升級",
            "Every visit levels you up.\n"
            "核心：四級會員・車牌停車・LaLa Go 巴士・e-Voucher\n"
            "遊戲包：簽到、任務、集章、扭蛋\n"
            "AI 智慧包：1 秒發票掃描＋Ask LaLa\n"
            "口碑包：Pandora 好評，一鍵帶你過去",
            image=A + ("idea_poster.jpg" if IDEA_VIDEO else "app/acg_event.jpg"), video=IDEA_VIDEO)
META["special"]["idea"] = d.n

# ---------------------------------------------------------------- 2 標竿
d.divider("標竿學習", "好的會員 App，讓人「想」打開，\n不是「要」打開", key="標竿")
s = d.info("八個標竿：實用功能把人帶進來，身份感把人留下來", label="Benchmark",
           banner="借來的事：車牌停車（1 Utama、Sunway）、看得到的進度（Starbucks）、玩得到的收集（USJ／Shopee）",
           source="Data source: 各品牌官方 App 與公開資訊；1 Utama ONECARD LPR 頁面（2026/11）；Starbucks Rewards 2026/03 三級制（Restaurant Dive）")
d.table(s, ["品牌", "他們怎麼做", "LaLa Quest 借什麼"],
        [["1 Utama ONECARD", "App 綁定最多 2 個車牌，LPR 開閘、電子錢包扣款", "核心：LaLa Park 車牌登入"],
         ["Sunway Smart Parking", "車牌辨識無票進出，在 App 內付費", "核心：出場自動付款"],
         ["MUJI Passport", "進店打卡也送 MUJI Miles，不買東西也能累積", "遊戲包：每日簽到"],
         ["Disney App", "AI 行程建議、排隊時能玩的小遊戲", "AI 包：Ask LaLa 排一天"],
         ["Universal Studios", "實體互動收集鑰匙，手機上看分數與收藏", "遊戲包：館內集章"],
         ["Starbucks Rewards", "Green／Gold／Reserve 三級，回饋 1x／1.2x／1.7x", "核心：四級會員＋倍率"],
         ["Shopee", "Coins＋每日小遊戲，大馬人每天的習慣", "遊戲包：每日一抽扭蛋"],
         ["Sephora", "Beauty Insider 分級＋會員真實評價", "口碑包：Buzz＋Real Talk"]],
        col_w=[2.1, 4.6, 2.9], size=12.5, row_h=0.52)

bench("MUJI：會員卡就是首頁，點數規則一句話講完", "MUJI", ["muji_2.jpg", "muji_3.jpg", "muji_5.jpg"],
      [("打開就是會員條碼", "首頁第一屏＝會員卡＋點數，結帳不用找"),
       ("規則極簡", "「100 円＝1 點，1 點＝1 円」，一句話就懂"),
       ("會員週＝節慶", "「無印良品週間」全會員 10% off，固定檔期養成習慣")],
      "首頁會員卡＋點數放第一屏；\n點數規則寫成一句馬來西亞英語；\n把 Bon Odori、Raya 做成「Member Week」。",
      "MUJI 證明：會員卡放首頁、規則越簡單，使用率越高")
bench("Disney：App 幫你排好一天，等待時間也變成資訊", "Disney", ["disney_3.jpg", "disney_4.jpg", "disney_5.jpg"],
      [("即時等待時間", "每個設施排多久、下一場表演幾點，一眼看到"),
       ("My Plans 行程", "把預約、餐廳、表演排成自己的一天"),
       ("互動地圖", "地圖上直接點設施、餐廳、廁所")],
      "LaLa Go 行程卡：發車時間、月台、倒數；\nAI 包：「Plan my Saturday」幫你排一天；\n熱門餐廳排隊時間。",
      "Disney 把「逛」變成「我的行程」：LaLa Quest 用 AI 做到同一件事")
bench("USJ：地圖是主角，整理券讓人提前規劃", "Universal Studios Japan", ["usj_3.jpg", "usj_4.jpg", "usj_5.jpg"],
      [("等待時間排行", "依分鐘數排序，最快能玩的放最上面"),
       ("全園地圖導覽", "設施直接標在插畫地圖上"),
       ("e 整理券／抽選", "熱門區域用 App 抽入場，製造期待感")],
      "ACG Matsuri、KLP48 劇場、聯名咖啡：\n用 App 抽「優先入場券」；\nSenpai 以上等級中籤率加倍。",
      "USJ 的整理券證明：限量＋抽選，會讓人每天打開 App")
bench("Starbucks：獎勵階梯清楚，掃碼那一刻有驚喜", "Starbucks Rewards", ["starbucks_2.jpg", "starbucks_3.jpg", "starbucks_5.jpg"],
      [("點數兌換階梯", "25★、100★、200★…每一階換什麼一目了然"),
       ("掃碼即付即集", "付款＝集點，一個動作完成"),
       ("Yay! 回饋動畫", "結帳後跳出慶祝畫面，強化成就感")],
      "停車時數、乘車券、聯名商品做成兌換階梯；\n點數折抵停車費＝看得到的價值；\n升級時全螢幕 Level Up 慶祝。",
      "Starbucks 2026 改回三級制：等級＋階梯，是最被驗證的會員設計")
bench("Shopee：大馬人最熟悉的「每天打開」節奏", "Shopee MY", ["shopee_1.jpg", "shopee_4.jpg", "shopee_5.jpg"],
      [("檔期感超強", "11.11、Payday Sale，倒數與大字視覺"),
       ("ShopeeVIP 會員", "付費會員專屬免運、折扣與 Voucher"),
       ("直播＋大獎", "RM11 Million Vouchers、明星直播，製造話題")],
      "沿用大馬人熟悉的 Payday、11.11 節奏；\nMOP KLIA「Payday Reward」e-Voucher；\n遊戲包：每日 Capsule＝LaLa 版 Coins。",
      "不用教育市場：大馬年輕人早就習慣「每天打開領東西」")
bench("Sephora：等級＝折扣，AI 幫你挑禮物", "Sephora", ["sephora_1.jpg", "sephora_4.jpg", "sephora_5.jpg"],
      [("等級直接對應折扣", "Insider 10%／VIB 15%／Rouge 20%，一張圖講完"),
       ("Wish List 分享", "收藏清單可以分享給朋友"),
       ("AI Beauty Chat", "用聊天問「200 美元內的禮物」，AI 直接推薦")],
      "Rookie → Legend 權益用一張圖講完；\nAI 包：Ask LaLa 用聊天推薦；\n口碑包學 Sephora 的評價文化。",
      "Sephora 的升級路徑：先有分級，再疊上 AI 與評價")

# ---------------------------------------------------------------- 3 全貌
d.divider("App 3.0 全貌", "核心把人帶進來，\n加購讓人留下來", key="全貌")
whats_new("App 3.0 更新一覽：8 項升級，其中 5 項是全新功能", "What's New｜Before → After",
          "從「推播商場消息的 App」，變成「幫我停車、幫我訂車、陪我升級的 App」",
          ["功能", "Before・現在的 App", "After・App 3.0", "方案", "Demo"],
          [("首頁", "Banner、News 一直推，沒有「我」", "我的會員卡、我的車、我的行程，一頁看完", "核心", "home"),
           ("會員", "權益看不清楚，沒有升級的動力", "4 個等級＋角色，每次來館權益都長大", "核心", "tiers"),
           ("停車", "紙本票卡；免費 3H 藏在 News 裡", "LaLa Park：車牌即會員、依等級免費停、點數折抵、閘門自動開", "核心・NEW", "park"),
           ("巴士・接駁", "在第三方網站買票，跟商場無關", "LaLa Go：App 買票＋RM10 券＋上車提醒；MOP 機場接駁", "核心・NEW", "go"),
           ("點數・券", "只有 5% 會員在 App 集點", "點數可抵停車、巴士；店家券＋行程券都在同一個錢包", "核心", "coremap"),
           ("遊戲", "—", "每日簽到、任務、Stamp Rally、LaLa Capsule", "加購・NEW", "play"),
           ("AI", "—", "1 秒發票掃描、Ask LaLa 管家、For You 推薦", "加購・NEW", "ai"),
           ("口碑", "好評散在 IG、Threads，App 裡看不到", "LaLa Buzz：Pandora Buzz Score＋Real Talk 真心話", "加購・NEW", "buzz")])
phone_demo("首頁：我的會員卡、我的車、我的行程，一頁看完", "Home", "home",
           [("會員卡＝QR＋等級", "結帳一打開 App，店員直接掃首頁 QR（右：情境影片）"),
            ("我的車，即時", "LPR 辨識 WXY 1234 停在 P2：免費時數剩 2h 31m"),
            ("我的行程", "15:30 往新加坡、Bay 3、還有 RM10 優惠券可用"),
            ("核心快捷鍵", "停車、巴士票、優惠券、登錄發票")],
           "首頁從「商場在推什麼」換成「我是誰、我今天能拿到什麼」", clip="checkout")
PAGES["home"] = d.n

s = d.info("核心＋加購：先上能帶來人流的功能，好玩的之後再插上", label="產品架構",
           banner="核心是基本授權、第一階段上線；每個加購模組都可單獨開通，不用重做 App")
core_map(s)
META["special"]["coremap"] = d.n
PAGES["coremap"] = d.n

s = d.info("為什麼這樣分：核心功能每一個都帶來一次來館，加購讓來館更深", label="模組邏輯",
           banner="判斷原則：能把一台車、一班巴士、一張發票帶進館的，就是核心")
d.table(s, ["模組", "方案", "怎麼帶來人流", "主要 KPI"],
        [["會員身份＋四級", "核心", "每來一次權益就長大一點", "Explorer 以上占比"],
         ["LaLa Park 車牌停車", "核心", "免費停車只給註冊車牌的會員", "註冊車牌數"],
         ["LaLa Go 巴士", "核心", "賣 LTH 車票＋附 e-Voucher 先消費", "售票數、券使用率"],
         ["點數＋e-Voucher", "核心", "店家優惠、乘車優惠券", "優惠券兌換數"],
         ["遊戲包 Play", "加購", "簽到、任務、集章、扭蛋", "週活躍"],
         ["AI 智慧包", "加購", "1 秒發票掃描、Ask LaLa、For You", "每月發票數"],
         ["口碑包 Buzz", "加購", "Pandora 好評＋Real Talk", "Buzz → 導航點擊"]],
        col_w=[2.6, 1.2, 3.9, 2.4], size=13, row_h=0.58)

s = d.info("視覺：一個主色、一抹香檳金，站得住精品品牌旁邊", label="Design System",
           banner="向官網的乾淨留白看齊：午夜藍做主色、香檳金只用在等級與重點，告別五顏六色的「App 感」")
sw = [("#13294B", "Midnight Navy", "#13294B", "唯一主色・卡片・導覽"), ("#B8975A", "Champagne Gold", "#B8975A", "等級・重點・點數"),
      ("#F6F3EE", "Ivory", "#F6F3EE", "背景・大量留白"), ("#E6E0D6", "Pearl", "#E6E0D6", "線條・分隔"),
      ("#1A1F2B", "Ink", "#1A1F2B", "文字")]
for i, (c, n, hx, use) in enumerate(sw):
    x = 0.7 + i * 1.62
    d.round(s, x, 1.4, 1.45, 1.1, c, 0.12)
    d.tx(s, x, 2.6, 1.5, 0.3, n, 11.5, bold=True)
    d.tx(s, x, 2.88, 1.5, 0.3, hx + "\n" + use, 10, color="mid", spacing=1.3)
d.logo(s, LALA, 0.7, 3.85, 0.55)
d.logo(s, MOP, 3.3, 3.88, 0.5)
d.tx(s, 0.7, 4.65, 7.5, 1.2, "字型：Cormorant Garamond（標題，精品襯線）＋ Plus Jakarta Sans（內文，易讀、支援馬來文）\n線性 icon 取代 emoji；金色只出現在等級、點數與 QR 邊框",
     12.5, color="mid", spacing=1.6)
d.tx(s, 9.0, 1.35, 3.7, 0.35, "Microcopy：馬來西亞英語", 13, color="frame", bold=True)
mc = ["Jom! Your car is parked, 2h 31m free.", "30 min to boarding, still got RM10 lah", "Ask anything, lah…",
      "Done · Shiok!", "Squad up: bring 1 kawan", "Drive safe, see you again!"]
for i, t in enumerate(mc):
    d.round(s, 9.0, 1.8 + i * 0.68, 3.7, 0.54, "soft", 0.3)
    d.tx(s, 9.2, 1.92 + i * 0.68, 3.4, 0.3, t, 11.5, bold=True)

# ---------------------------------------------------------------- 4 分級
d.divider("會員分級", "核心①｜從 Regular Member，\n到 Rookie、Explorer、Senpai、Legend", key="分級")
s = d.info("四個等級，四個 LaLa：會員一路養大自己的角色", label="核心｜Tier Characters",
           banner="不叫金卡銀卡：每升一級，LaLa 換一套裝備、停車多一小時、多一枚徽章",
           source="角色為 AI 示意設計，正式版可延伸成貼圖、扭蛋公仔與館內裝置")
TIERS = [("rookie", "#8F8A80", "ROOKIE", "LV1｜註冊即得", "1x 點數・3H 停車\n乘車 e-Voucher"),
         ("explorer", "#13294B", "EXPLORER", "LV2｜RM1,500 或 12 次造訪", "1.2x 點數・4H 停車\n生日月雙倍點"),
         ("senpai", "#B8975A", "SENPAI", "LV3｜RM5,000", "1.5x 點數・5H 停車\n活動優先入場"),
         ("legend", "#0B1A30", "LEGEND", "LV4｜RM12,000", "2x 點數・全日停車\nLegend Lounge")]
for i, (k, col, nm, th, perk) in enumerate(TIERS):
    x = 0.72 + i * 3.02
    d.round(s, x, 1.25, 2.8, 4.75, "soft", 0.08)
    d.rect(s, x, 1.25, 2.8, 0.09, col)
    d.fit(s, A + f"world/char_{k}_s.png", x + 0.25, 1.45, 2.3, 2.25)
    d.tx(s, x, 3.8, 2.8, 0.45, nm, 22, color=col, bold=True, align=PP_ALIGN.CENTER, font="Arial Black")
    d.tx(s, x, 4.32, 2.8, 0.3, th, 11.5, color="mid", bold=True, align=PP_ALIGN.CENTER)
    d.tx(s, x + 0.2, 4.8, 2.4, 0.9, perk, 13, bold=True, align=PP_ALIGN.CENTER, spacing=1.5)
    if i < 3:
        d.rect(s, x + 2.84, 3.4, 0.14, 0.24, "grey", MSO_SHAPE.RIGHT_ARROW)
d.ai_tag(s, 0.82, 1.38)
META["special"]["tiers"] = d.n
PAGES["tiers"] = d.n

s = d.info("權益對照：停車時數、乘車點數跟著等級長大", label="核心｜Tier Design",
           banner="停車是每個人都懂的權益：「升級」直接變成每次來省下的時數",
           source="門檻與權益為試算示意，正式數字依三井會員消費與停車場數據調整")
d.table(s, ["等級", "門檻（12 個月）", "點數倍率", "免費停車（LPR）", "乘車點數", "代表權益"],
        [["Rookie　LV1", "註冊即得", "1x", "3 小時", "1x", "乘車 e-Voucher、生日禮"],
         ["Explorer　LV2", "RM 1,500 或 12 次造訪", "1.2x", "4 小時", "1.2x", "生日月雙倍點、可綁第 2 台車"],
         ["Senpai　LV3", "RM 5,000", "1.5x", "5 小時", "1.5x", "Bon Odori・ACG 活動優先入場"],
         ["Legend　LV4", "RM 12,000", "2x", "全日", "2x", "Legend Lounge、專屬車位、Legend Night"]],
        col_w=[1.5, 2.2, 1.0, 1.6, 1.1, 3.1], size=13, row_h=0.7, hot_row=2)
d.tx(s, 0.75, 5.2, 12, 0.6, "★ 「次數」也能升級：Explorer 可用 12 次造訪達成。加購遊戲包後，各級另享每日扭蛋 1／1／2／3 次。",
     13.5, bold=True, color="frame")

phone_demo("等級頁：四張卡疊在一起，下一級永遠看得到", "核心｜Tier", "tiers",
           [("卡片疊疊樂", "四級會員卡像錢包一樣疊著，Legend 黑金卡最吸睛"),
            ("權益對照表", "倍率、車牌停車時數、乘車點數、活動入場"),
            ("升級那一刻", "全螢幕慶祝：停車 4H → 5H 解鎖")],
           "讓會員知道「下一步在哪」，比給更多點數更有用",
           keys2=["levelup"])

# ---------------------------------------------------------------- 5 LaLa Park（核心）
d.divider("LaLa Park", "核心②｜車牌註冊一次，\n閘門就認得你是會員", key="停車")
scene("LaLa Park：開進來、逛一下午、開出去，閘門自己打開", "核心｜LaLa Park・情境 Demo",
      "每個開車來的人都有理由註冊，每一次來館都被記錄下來",
      A + "app/lpr_gate.jpg", ["parking"],
      [("週六 2:14 PM", "開進停車場，鏡頭辨識 WXY 1234：「免費 4H 開始計時」"),
       ("5:12 PM", "逛街、吃飯、看電影，App 隨時看得到剩餘免費時間"),
       ("出場", "扣掉 4H 免費，800 點付清餘額，閘門自動打開，不用票卡")],
      stats=[("0 張票卡", "車牌就是會員卡"), ("3H → 全天", "免費停車時數跟著等級長大"),
             ("100 點 = RM1", "點數直接折抵停車費")],
      source="停車時數、費率與點數比例皆為示意；與三井 LPR 停車系統以 API 串接")
PAGES["park"] = d.n

# ---------------------------------------------------------------- 6 LaLa Go（核心）
d.divider("LaLa Go", "核心③｜在 App 買巴士票，\n等車的時間留在館內逛", key="巴士")
scene("LaLa Go：App 訂巴士票、多拿 RM10 券，時間到了提醒你上車", "核心｜LaLa Go・情境 Demo",
      "等車時間變成逛街時間：每位乘客手上都帶著一張券經過店門口",
      A + "app/lth_bay.jpg", ["bus", "busticket"],
      [("1:30 PM", "App 訂 3:30 往新加坡的巴士，加送 RM10 e-Voucher"),
       ("3:00 PM", "推播：「30 分鐘後上車，RM10 還沒用！」買杯珍奶剛好"),
       ("3:20 PM", "Bay 3 掃 QR 上車，點數在行程結束後入帳")],
      chip="MOP：機場免費接駁時刻＋趕飛機提醒",
      source="業者、票價與時刻皆為示意；票務以業者訂票 API 串接（LTH 為 busonlineticket.com 體系）")
PAGES["go"] = d.n

# ---------------------------------------------------------------- 7 遊戲包（加購）
d.divider("遊戲包", "加購 A｜每天、每週、每季，\n都有一個回來的理由", key="遊戲")
s = d.info("遊戲包：每天簽到、每週任務、每季祭典", label="加購｜Play Pack",
           banner="選配加購：等核心累積會員後，配合 ACG Matsuri、Bon Odori 檔期開通")
d.flow(s, [("DAILY", "#1E9C9A", "簽到 Streak", "每天 +10 pts\n連續 7 天送扭蛋\n斷了可用點數補簽"),
           ("WEEKLY", BLUE, "Quest 任務", "Makan Quest：試 2 家新店\nSquad Quest：帶 1 個 kawan\n完成給 XP"),
           ("SEASONAL", PINK, "Matsuri Pass", "Bon Odori・ACG Matsuri・\nRaya・CNY・Deepavali\n館內集章 Stamp Rally"),
           ("COLLECT", ORANGE, "LaLa Capsule", "24 隻一系列\n稀有款可跟朋友交換\n集滿換實體公仔")])

phone_demo("Stamp Rally：把館內動線，變成一張尋寶地圖", "加購｜遊戲包・Quest", "quest",
           [("樓層地圖集章", "L4 Garden Dining、L2 ACG Base、L1 Doko Koko"),
            ("離你 40m", "定位提示下一站，帶動跨樓層人流"),
            ("集滿換限定", "5 章換 Matsuri 限定扭蛋＋300 XP")],
           "集章是日本商場最熟悉的玩法，搬進 App 就能量化每一層的人流",
           photo=A + "app/acg_event.jpg")
PAGES["play"] = d.n

phone_demo("LaLa Capsule：每天一抽，抽到的是「想收集」的心", "加購｜遊戲包・Capsule", "capsule",
           [("每日免費一抽", "簽到送、等級越高次數越多"),
            ("24 隻一系列", "Durian-chan、Ramen-kun…原創角色，可做成實體公仔"),
            ("Trade with kawan", "重複的可以跟朋友交換，自帶社群擴散")],
           "扭蛋把「點數」變成「收藏」：數位收集，實體兌換，再回到館內",
           photo=A + "mock_friends_capsule.jpg")

# ---------------------------------------------------------------- 8 AI（加購）
d.divider("AI 智慧包", "加購 B｜拍發票、問管家、看推薦：\n三個 AI 各解一個麻煩", key="AI")
s = d.info("AI 智慧包：讓集點從「麻煩」變成「順手」", label="加購｜AI Pack",
           banner="核心已能上傳發票登錄；AI 包讓它 1 秒完成，再加上一位 AI 管家")
d.columns(s, [("AI Receipt Scan", ORANGE, "拍一張，1 秒入點",
               "AI 讀店名、金額、時間\n1.2 秒（核心：上傳、24h 審核）\n防重複、防竄改"),
              ("Ask LaLa", BLUE, "你的 AI 逛街管家",
               "英文／馬來文／中文都能問\n找吃、找店、找停車出口\n幫你排一天行程"),
              ("For You", MINT, "每個人的首頁不一樣",
               "依等級、喜好、歷史推薦\nACG 粉看到聯名咖啡\n旅客看到乘車優惠")])

phone_demo("AI 發票掃描：吃完拉麵，順手一拍就入點", "加購｜AI Receipt Scan", "scan",
           [("AI 即時辨識", "店名、金額、時間自動抓，1.2 秒完成"),
            ("等級倍率自動算", "Explorer 1.2x：RM28.90 → +35 pts"),
            ("順便推進任務", "加購遊戲包時：Makan Quest 完成")],
           "拍發票是唯一不用改店家 POS 就能把 95% 消費記回來的方法",
           photo=A + "mock_ramen_scan.jpg")
PAGES["ai"] = d.n

phone_demo("Ask LaLa：像問朋友一樣問商場", "加購｜Ask LaLa", "ask",
           [("用馬來西亞英語聊", "「Jom makan! Any halal ramen under RM15?」"),
            ("答案帶你過去", "附 Buzz 評分、步行時間，按 Go 導航"),
            ("認得你的車和行程", "問「最近的出口？」直接用 LaLa Park 資料")],
           "Ask LaLa 背後是 LLM＋館內店家資料＋核心停車與巴士資料：問得到，也走得到")

# ---------------------------------------------------------------- 9 口碑包（加購）
d.divider("口碑包 LaLa Buzz", "加購 C｜網路上的好評，搬進 App；\n館內的真心話，留在 App", key="口碑")
scene("LaLa Buzz：看大家最近在愛什麼，一鍵走過去", "加購｜LaLa Buzz・情境 Demo",
      "Pandora 驅動：網友的真心好評變成來館理由，Real Talk 把熱度留在 App",
      A + "app/ramen.jpg", ["buzz", "brand"],
      [("週五晚上", "滑 Buzz：Akiba Ramen ★4.8・92% 好評・本週 ▲32%"),
       ("週六中午", "按「帶我去」：L4 走路 2 分鐘，濃厚白湯果然好吃"),
       ("吃完", "拍發票、寫一則 Real Talk，+20 點")],
      chip="Powered by Pandora・3,696 則真實貼文",
      source="資料來源：Pandora 社群聆聽，LaLaport BBCC，2026/5/3–10/31，N=3,696（Instagram、Threads）")
PAGES["buzz"] = d.n

# ---------------------------------------------------------------- 10 落地
d.divider("落地與 KPI", "核心先上、加購隨時開：\nActivation、時程、分工、KPI", key="落地")
d.social_idea("A", "MOP KLIA Sepang × 旅客", "Transit Quest：在 Outlet 轉機一次，成為一輩子的會員",
              "LaLa Go 顯示 KLIA 免費接駁，時間到提醒旅客出發趕飛機。下載即送 Explorer 試用 30 天＋RM10 e-Voucher＋"
              "Tourist Privilege Pass，讓一次性的旅客也留下會員資料。（AI 示意圖）", A + "klia_outlet.jpg")
d.social_idea("B", "LaLaport BBCC × ACG（加購遊戲包）", "ACG Season Pass：把 ACG Matsuri 變成 App 裡的季賽",
              "開通遊戲包後：集章、聯名咖啡任務、KLP48 劇場打卡。Matsuri 週末開車來的會員停車多送 1H；"
              "完成可換限定扭蛋。（AI 示意圖）", A + "app/acg_event.jpg")

s = d.info("先上線核心，再依檔期一個個插上加購模組", label="時程",
           banner="Phase 0 全部是核心：分級、車牌停車、LaLa Go 一起上線；加購依需求開通")
d.timeline(s, 1.8, ["2027/01", "2027/04", "2027/07", "2027/10", "2028/01"],
           [("P0 核心｜分級・停車・巴士・優惠券", 0, 0.4),
            ("加購｜口碑包（Pandora）", 0.3, 0.6),
            ("加購｜AI 智慧包（發票・Ask LaLa）", 0.45, 0.8),
            ("加購｜遊戲包（任務・扭蛋・祭典）", 0.6, 1.0)])
d.table(s, ["", "三井 Mitsui Shopping Park", "騰雲 TurnCloud"],
        [["內容", "等級權益、停車規則、店家優惠券", "UI/UX 設計、Prototype、文案在地化"],
         ["系統", "App、會員資料、停車場 LPR 與巴士業者窗口", "分級引擎、LPR／巴士 API 串接、加購模組"],
         ["數據", "門檻、停車與優惠券預算", "Pandora 口碑爬取、CRM 儀表板"]],
        y=3.85, col_w=[1.0, 4.0, 4.0], size=12.5, row_h=0.5)

s = d.info("KPI：核心拉來客與註冊，加購拉黏著度", label="KPI",
           banner="每一層都看得到數字：Phase 0 的核心數據，決定先開哪一個加購模組",
           source="目標值為試算示意，正式目標依三井會員數、停車場與 App 數據校正")
d.table(s, ["指標", "方案", "現況", "Phase 0（3 個月）", "12 個月（示意）"],
        [["註冊車牌數（LaLa Park）", "核心", "—", "15,000", "60,000"],
         ["App 售出巴士票（LaLa Go）", "核心", "0", "3,000／月", "10,000／月"],
         ["乘車 e-Voucher 使用率", "核心", "0", "40%", "55%"],
         ["App 集點會員比例", "核心", "5%", "10%", "20%"],
         ["平均月造訪次數", "核心", "—", "+0.2 次", "+0.6 次"],
         ["MAU／會員數", "加購", "—", "20%", "35%"],
         ["Real Talk 分享則數／月", "加購", "0", "—", "3,000"]],
        col_w=[3.4, 1.2, 1.2, 2.1, 2.2], size=13, row_h=0.56, hot_row=0)

d.closing("每一次來，都在升級。",
          "Next Step\n① 11 月：確認核心範圍與等級權益（含停車時數）\n② 12 月：停車場 LPR＋巴士業者 API 工作坊；20 位會員 Prototype 測試\n"
          "③ 2027/01：Phase 0 核心開發啟動",
          logos=[TC])
fill_page_refs()
d.save("MSP_App3.0_LaLaQuest_提案.pptx")
import json
META["n"] = d.n
json.dump(META, open("web_meta.json", "w"))
