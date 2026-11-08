import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/shelley-deck/scripts"))
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN  # noqa: E402
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


def phone_demo(title, label, key, points, banner, photo=None, keys2=None, source=None):
    s = d.info(title, label=label, banner=banner, source=source)
    x = 0.9
    w = phone(s, key, x, 1.3, 4.55)
    x += w + 0.45
    for k in keys2 or []:
        w2 = phone(s, k, x, 1.3, 4.55)
        x += w2 + 0.45
    if photo:
        pw = 9.0 - x
        px, py, pw, ph = d.fit(s, photo, x, 1.3, pw, 4.55)
        d.ai_tag(s, px + 0.1, py + 0.1)
    d.tx(s, 9.35, 1.35, 3.4, 0.35, "畫面重點", 13, color="frame", bold=True)
    gap = min(1.15, 4.6 / max(1, len(points)))
    d.callouts(s, 9.35, 1.85, 3.4, points, gap=gap)
    return s


# ---------------------------------------------------------------- 封面
d.cover("MSP 會員 App\n3.0 改版提案。", "LaLa Quest｜每一次來，都在升級。", "2026.11",
        company="TURN CLOUD TECHNOLOGY SERVICE INC.", logos=[LALA, MOP], image=A + "mock_hero3.jpg")
d.toc([("現況與洞察", "機會"), ("標竿學習", "標竿"), ("App 3.0 全貌", "全貌"), ("會員分級", "分級"),
       ("遊戲化設計", "遊戲"), ("AI 功能", "AI"), ("口碑專區 LaLa Buzz", "口碑"), ("落地與 KPI", "落地")])

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

s = d.info("一頁看懂：把逛街，變成一場會升級的遊戲", label="Executive Summary",
           banner="不是再多一個優惠券入口，而是讓年輕人「想」打開 App：看得到等級、玩得到東西、問得到答案")
d.columns(s, [("洞察", "#8A94A6", "熱度很高，App 沒接住",
               "半年 3,696 篇、90.7% 正面\n年輕人為 ACG、K-pop、電影而來\n只有 5% 會員用 App 集點\n最痛的停車，App 早有解卻沒人知道"),
              ("解法", BLUE, "LaLa Quest：四件事",
               "Level Up：四級會員＋小怪獸角色\nPlay：簽到、任務、扭蛋\nAsk：AI 管家＋AI 發票集點\nBuzz：Pandora 好評＋Real Talk"),
              ("收益", ORANGE, "集點率 5% → 20%",
               "每張發票都回到 CRM\n偶爾來 → 每月來\n店家多一個導購入口\n兩館共用一個會員身份")])

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

s = d.info("洞察③　負評集中在停車與館內體驗：App 早有解，卻藏在 News 裡", label="Pandora 洞察報告｜App 現況",
           banner="把「免費停車」變成等級權益、把會員 QR 放上首頁：第一天就讓人感受到 App 的價值",
           source=PSRC + "；App 實機截圖 2026/11")
d.fit(s, PD + "i_negative.png", 0.6, 1.28, 6.1, 3.28, border=True)
d.tx(s, 0.75, 4.72, 5.9, 1.3, "Pandora 負評摘要：停車費太貴、停車場出入口封閉、\n館內訊號差導致 QR 付款困難。\n→ 3.0：停車時數跟著等級走（3H → 全日），首頁直接亮出會員 QR。",
     12, bold=True, spacing=1.55)
d.fit(s, A + "current_app.jpg", 7.0, 1.28, 5.75, 1.78, border=True)
d.ai_tag(s, 7.1, 1.36, "現行 App 實機畫面")
d.callouts(s, 7.0, 3.3, 5.75, [("首頁＝廣告牆", "Banner、News、Voucher 都在推，沒有「我」"),
                               ("免費停車藏在 News", "MSP Member Free 3H Parking 只是一則活動"),
                               ("一種會員、遊戲藏太深", "Regular Member；Spin & Win 在 Profile 第二層")], gap=0.9)

d.statement("IDEA", "LaLa Quest\n把逛街變成升級遊戲",
            "Every visit levels you up.\n"
            "Level Up：Rookie → Explorer → Senpai → Legend\n"
            "Play：簽到、任務、集章、扭蛋\n"
            "Ask：AI 管家＋AI 發票集點\n"
            "Buzz：Pandora 好評，一鍵帶你過去",
            image=A + ("idea_poster.jpg" if IDEA_VIDEO else "app/acg_event.jpg"), video=IDEA_VIDEO)
META["special"]["idea"] = d.n

# ---------------------------------------------------------------- 2 標竿
d.divider("標竿學習", "好的會員 App，讓人「想」打開，\n不是「要」打開", key="標竿")
s = d.info("六個標竿：每一個都把會員變成一種「身份」", label="Benchmark",
           banner="借來三件事：看得到的進度（Starbucks）、玩得到的收集（USJ／Shopee）、問得到的答案（Disney）",
           source="Data source: 各品牌官方 App 與公開資訊；Starbucks Rewards 2026/03 三級制（Restaurant Dive）")
d.table(s, ["品牌", "他們怎麼做", "LaLa Quest 借什麼"],
        [["MUJI Passport", "進店打卡也送 MUJI Miles，不買東西也能累積", "每日簽到 Streak、Check-in 任務"],
         ["Disney App", "AI 行程建議、排隊時能玩的小遊戲", "Ask LaLa 幫你排一天"],
         ["Universal Studios", "實體互動收集鑰匙，手機上看分數與收藏", "館內集章 Stamp Rally"],
         ["Starbucks Rewards", "Green／Gold／Reserve 三級，回饋 1x／1.2x／1.7x", "四級會員＋點數倍率"],
         ["Shopee", "Coins＋每日小遊戲，大馬人每天的習慣", "每日一抽 LaLa Capsule"],
         ["Sephora", "Beauty Insider 分級＋會員真實評價", "LaLa Buzz＋Real Talk"]],
        col_w=[1.6, 4.2, 3.2], size=13, row_h=0.62)

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
      "Ask LaLa「Plan my Saturday」幫你排一天；\n熱門餐廳排隊時間＋聯名咖啡預約；\n樓層地圖結合 Stamp Rally。",
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
      "Capsule、停車、聯名商品做成兌換階梯；\nAI 發票掃描後跳 +35 pts 動畫；\n升級時全螢幕 Level Up 慶祝。",
      "Starbucks 2026 改回三級制：等級＋階梯，是最被驗證的會員設計")
bench("Shopee：大馬人最熟悉的「每天打開」節奏", "Shopee MY", ["shopee_1.jpg", "shopee_4.jpg", "shopee_5.jpg"],
      [("檔期感超強", "11.11、Payday Sale，倒數與大字視覺"),
       ("ShopeeVIP 會員", "付費會員專屬免運、折扣與 Voucher"),
       ("直播＋大獎", "RM11 Million Vouchers、明星直播，製造話題")],
      "沿用大馬人熟悉的 Payday、11.11 節奏；\nMOP KLIA「Payday Reward」做成 Quest；\n每日 Capsule＝LaLa 版的 Shopee Coins。",
      "不用教育市場：大馬年輕人早就習慣「每天打開領東西」")
bench("Sephora：等級＝折扣，AI 幫你挑禮物", "Sephora", ["sephora_1.jpg", "sephora_4.jpg", "sephora_5.jpg"],
      [("等級直接對應折扣", "Insider 10%／VIB 15%／Rouge 20%，一張圖講完"),
       ("Wish List 分享", "收藏清單可以分享給朋友"),
       ("AI Beauty Chat", "用聊天問「200 美元內的禮物」，AI 直接推薦")],
      "Rookie → Legend 權益用一張圖講完；\nAsk LaLa 用聊天推薦店家與禮物；\nReal Talk＋Buzz 學 Sephora 的評價文化。",
      "Sephora 是「分級＋AI＋評價」三合一的最佳範本")

# ---------------------------------------------------------------- 3 全貌
d.divider("App 3.0 全貌", "一個主色、四大支柱，\n更年輕也更有質感的 LaLaport", key="全貌")
phone_demo("首頁：一打開，就是我的會員卡、QR 和我的小怪獸", "Home", "home",
           [("會員卡＝QR＋等級", "結帳直接掃首頁 QR；卡上寫著 Explorer、1,884 pts"),
            ("我的小怪獸", "等級角色住在卡上，升級就換裝，想截圖分享"),
            ("進度與權益", "再 616 點升 Senpai；4H 免費停車、1.2x 點數一眼看到"),
            ("簽到＋快捷鍵", "5 天 Streak；Scan Receipt、Ask LaLa、Capsule、Parking")],
           "首頁從「商場在推什麼」換成「我是誰、我今天能拿到什麼」", photo=A + "mock_hijab_home.jpg")

s = d.info("LaLa Quest 四大支柱：升級、玩、問、口碑", label="App 架構",
           banner="四個支柱都導向同一件事：把每一次消費、每一次造訪，記回會員身上")
d.cover_pic(s, A + "world/sky.jpg", 0.54, 1.08, W - 1.08, 5.3)
ISL = [("levelup", "#1E9C9A", "Level Up 島", "四級會員：停車、倍率、扭蛋跟著升"),
       ("play", PINK, "Play 島", "簽到・Quest・集章・LaLa Capsule"),
       ("ask", BLUE, "Ask 島", "AI 發票掃描・Ask LaLa・For You"),
       ("buzz", ORANGE, "Buzz 島", "Pandora 好評＋Real Talk 真心話")]
for i, (k, col, name, desc) in enumerate(ISL):
    cx = 0.75 + i * 3.02
    yoff = [0.0, 0.35, 0.0, 0.35][i]
    d.fit(s, A + f"world/{k}_s.png", cx, 1.2 + yoff, 2.85, 2.95)
    d.round(s, cx + 0.2, 4.35 + yoff * 0.5, 2.45, 0.42, col, 0.5)
    d.tx(s, cx + 0.2, 4.41 + yoff * 0.5, 2.45, 0.3, name, 14, color="white", bold=True, align=PP_ALIGN.CENTER)
    d.round(s, cx + 0.05, 4.85 + yoff * 0.5, 2.75, 0.62, "white", 0.25)
    d.tx(s, cx + 0.15, 4.95 + yoff * 0.5, 2.55, 0.5, desc, 10.5, color="ink", bold=True, align=PP_ALIGN.CENTER)
d.ai_tag(s, 0.7, 1.2, "AI 示意圖｜網頁版可互動")
META["special"]["islands"] = d.n

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
mc = ["Jom! 2 quests waiting for you today.", "Ada! Here are 2 picks on L4", "Ask anything, lah…",
      "Done · Shiok!", "Squad up: bring 1 kawan", "Sedap gila · Worth it"]
for i, t in enumerate(mc):
    d.round(s, 9.0, 1.8 + i * 0.68, 3.7, 0.54, "soft", 0.3)
    d.tx(s, 9.2, 1.92 + i * 0.68, 3.4, 0.3, t, 11.5, bold=True)

# ---------------------------------------------------------------- 4 分級
d.divider("會員分級", "從 Regular Member，\n到 Rookie、Explorer、Senpai、Legend", key="分級")
s = d.info("四個等級，四個 LaLa：會員一路養大自己的角色", label="Tier Characters",
           banner="不叫金卡銀卡：每升一級，LaLa 換一套裝備、多一枚徽章，年輕人會想截圖分享",
           source="角色為 AI 示意設計，正式版可延伸成貼圖、扭蛋公仔與館內裝置")
TIERS = [("rookie", "#8F8A80", "ROOKIE", "LV1｜註冊即得", "1x 點數・3H 停車\n每日 1 抽"),
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

s = d.info("權益對照：不叫金卡銀卡，叫 Senpai", label="Tier Design",
           banner="用日系動漫語言命名，貼近 LaLaport 的日本 DNA，也是年輕人會想截圖分享的身份",
           source="門檻與權益為試算示意，正式數字依三井會員消費分布調整")
d.table(s, ["等級", "門檻（12 個月）", "點數倍率", "免費停車", "扭蛋", "代表權益"],
        [["Rookie　LV1", "註冊即得", "1x", "3 小時", "1 次／日", "每日簽到、生日禮"],
         ["Explorer　LV2", "RM 1,500 或 12 次造訪", "1.2x", "4 小時", "1 次／日", "生日月雙倍點、聯名咖啡優先訂位"],
         ["Senpai　LV3", "RM 5,000", "1.5x", "5 小時", "2 次／日", "Bon Odori・ACG 活動優先入場、限定扭蛋"],
         ["Legend　LV4", "RM 12,000", "2x", "全日", "3 次／日", "Legend Lounge、年度 Legend Night"]],
        col_w=[1.5, 2.2, 1.1, 1.1, 1.0, 3.6], size=13, row_h=0.7, hot_row=2)
d.tx(s, 0.75, 5.2, 12, 0.6, "★ 「次數」也能升級：Explorer 可用 12 次造訪達成 —— 學生、年輕上班族不用花大錢，常來就能升。",
     13.5, bold=True, color="frame")


phone_demo("等級頁：四張卡疊在一起，下一級永遠看得到", "Tier", "tiers",
           [("卡片疊疊樂", "四級會員卡像錢包一樣疊著，Legend 黑金卡最吸睛"),
            ("權益對照表", "倍率、停車、扭蛋、活動入場，一眼看懂"),
            ("三種升級方式", "消費掃發票、到館簽到、完成任務")],
           "讓會員知道「下一步在哪」，比給更多點數更有用",
           keys2=["levelup"])

# ---------------------------------------------------------------- 5 遊戲化
d.divider("遊戲化設計", "每天、每週、每季，\n都有一個回來的理由", key="遊戲")
s = d.info("三層迴圈：每天簽到、每週任務、每季祭典", label="Game Loop",
           banner="小獎勵天天給、大獎勵跟著檔期走：把 Bon Odori、ACG Matsuri 變成 App 裡的「季賽」")
d.flow(s, [("DAILY", "#1E9C9A", "簽到 Streak", "每天 +10 pts\n連續 7 天送扭蛋\n斷了可用點數補簽"),
           ("WEEKLY", BLUE, "Quest 任務", "Makan Quest：試 2 家新店\nSquad Quest：帶 1 個 kawan\n完成給 XP"),
           ("SEASONAL", PINK, "Matsuri Pass", "Bon Odori・ACG Matsuri・\nRaya・CNY・Deepavali\n館內集章 Stamp Rally"),
           ("COLLECT", ORANGE, "LaLa Capsule", "24 隻一系列\n稀有款可跟朋友交換\n集滿換實體公仔")])

phone_demo("Stamp Rally：把館內動線，變成一張尋寶地圖", "Quest", "quest",
           [("樓層地圖集章", "L4 Garden Dining、L2 ACG Base、L1 Doko Koko"),
            ("離你 40m", "定位提示下一站，帶動跨樓層人流"),
            ("集滿換限定", "5 章換 Matsuri 限定扭蛋＋300 XP")],
           "集章是日本商場最熟悉的玩法，搬進 App 就能量化每一層的人流",
           photo=A + "app/acg_event.jpg")

phone_demo("LaLa Capsule：每天一抽，抽到的是「想收集」的心", "Capsule", "capsule",
           [("每日免費一抽", "簽到送、等級越高次數越多"),
            ("24 隻一系列", "Durian-chan、Ramen-kun…原創角色，可做成實體公仔"),
            ("Trade with kawan", "重複的可以跟朋友交換，自帶社群擴散")],
           "扭蛋把「點數」變成「收藏」：數位收集，實體兌換，再回到館內",
           photo=A + "mock_friends_capsule.jpg")

# ---------------------------------------------------------------- 6 AI
d.divider("AI 功能", "拍發票、問管家、看推薦：\n三個 AI 各解一個麻煩", key="AI")
s = d.info("三個 AI 功能：讓集點從「麻煩」變成「順手」", label="AI Features",
           banner="5% 集點率的最大原因是麻煩：AI 把每一步縮短到一秒")
d.columns(s, [("AI Receipt Scan", ORANGE, "拍一張，1 秒入點",
               "AI 讀店名、金額、時間\n自動對應店家與任務\n防重複、防竄改"),
              ("Ask LaLa", BLUE, "你的 AI 逛街管家",
               "英文／馬來文／中文都能問\n找吃、找店、找停車出口\n幫你排一天行程"),
              ("For You", MINT, "每個人的首頁不一樣",
               "依等級、喜好、歷史推薦\nACG 粉看到聯名咖啡\n家庭客看到親子活動")])

phone_demo("AI 發票掃描：吃完拉麵，順手一拍就入點", "AI Receipt Scan", "scan",
           [("AI 即時辨識", "店名、金額、時間自動抓，1.2 秒完成"),
            ("等級倍率自動算", "Explorer 1.2x：RM28.90 → +35 pts"),
            ("順便推進任務", "Makan Quest 完成＋提示寫 Real Talk")],
           "拍發票是唯一不用改店家 POS 就能把 95% 消費記回來的方法",
           photo=A + "mock_ramen_scan.jpg")

phone_demo("Ask LaLa：像問朋友一樣問商場", "Ask LaLa", "ask",
           [("用馬來西亞英語聊", "「Jom makan! Any halal ramen under RM15?」"),
            ("答案帶你過去", "附 Buzz 評分、步行時間，按 Go 導航"),
            ("順便推任務", "提醒掃發票完成 Makan Quest")],
           "Ask LaLa 背後是 LLM＋館內店家資料＋Pandora 輿情：問得到，也走得到")

# ---------------------------------------------------------------- 7 口碑
d.divider("口碑專區 LaLa Buzz", "網路上的好評，搬進 App；\n館內的真心話，留在 App", key="口碑")
s = d.info("LaLa Buzz 的大腦是 Pandora：蒐集、判斷、摘要，每天自動更新", label="How it works｜Powered by Pandora",
           banner="不用店家自己寫廣告：Pandora 找出網友已經說過的好話，放到顧客做決定的那一刻")
d.flow(s, [("① 蒐集", "#13294B", "Pandora 輿情爬取", "每日爬 IG、Threads、\nFacebook 公開貼文\n依店家、活動自動歸類"),
           ("② 判斷", "#1E3A63", "Pandora AI 情緒判讀", "五級情緒分析\n判斷是否真的在講該店\n排除業配、無關貼文"),
           ("③ 呈現", "#B8975A", "Buzz Score＋AI 摘要", "「92% love it」好評比例\n大家愛什麼、熱門標籤\n一鍵導航、領券"),
           ("④ 回寫", "#8C6E3C", "Real Talk", "已購認證才能寫\n寫一篇 +20 pts\n回到 Pandora 一起分析")])

s = d.info("Pandora：同一套引擎，給商場看報告、給顧客看 LaLa Buzz", label="Our Product｜Pandora",
           banner="這些是 Pandora 為 LaLaport BBCC 跑出的真實報告畫面：LaLa Buzz 上線第一天就有資料可用",
           source=PSRC)
STEP = [("v_stats.png", "① 聲量蒐集", "3,696 篇貼文、510 萬聲量\n→ App 裡的「128 posts ▲32%」"),
        ("i_sentdist_c.png", "② 情緒判斷", "90.7% 正面、負評 1.2%\n→ App 裡的「92% love it」"),
        ("i_positive.png", "③ 好評摘要", "AI 讀完貼文寫重點\n→ App 裡的 AI 摘要與標籤")]
for i, (f, t, desc) in enumerate(STEP):
    x = 0.6 + i * 3.05
    d.round(s, x, 1.28, 2.85, 4.75, "soft", 0.06)
    d.tx(s, x + 0.15, 1.4, 2.6, 0.35, t, 14, color="frame", bold=True)
    d.fit(s, PD + f, x + 0.12, 1.85, 2.61, 2.1, border=True)
    d.tx(s, x + 0.15, 4.1, 2.6, 0.9, desc, 11.5, bold=True, spacing=1.5)
    if i < 2:
        d.rect(s, x + 2.88, 3.0, 0.14, 0.24, "grey", MSO_SHAPE.RIGHT_ARROW)
d.rect(s, 9.7, 3.0, 0.14, 0.24, ORANGE, MSO_SHAPE.RIGHT_ARROW)
phone(s, "brand", 10.05, 1.3, 4.0, video=False, tag=False)
d.tx(s, 9.85, 5.42, 2.3, 0.3, "LaLa Buzz 店家頁", 10, color="mid", bold=True, align=PP_ALIGN.CENTER)
d.fit(s, PD + "qr_insight.png", 12.2, 1.3, 0.8, 0.8, border=True)
d.tx(s, 12.07, 2.12, 1.05, 0.25, "看報告", 9, color="mid", bold=True, align=PP_ALIGN.CENTER)

s = d.info("Pandora 實測：馬來西亞網友，已經在幫店家寫好評", label="Pandora 實測",
           banner="這些是真實貼文：LaLa Buzz 上線第一天，就有內容可以放",
           source="Data source: Pandora 實測 2025/11/06–2026/11/05，馬來西亞地區；括號為提及篇數")
d.bars(s, [("ACG Base", 223), ("KLP48 劇場", 99), ("Doko Koko Café", 98), ("Pokémon", 71),
           ("Animate", 57), ("MINISO", 42), ("Akiba Ramen", 12)], 0.6, 1.35, 5.6, row_h=0.62, hot={2, 4, 6},
       name_w=1.7, size=11)
ugc(s, "akiba", 6.35, 1.25, 2.05, 4.85, "Akiba Ramen｜629 likes")
ugc(s, "dokokoko", 8.5, 1.25, 2.05, 4.85, "Doko Koko Café｜4,585 likes")
ugc(s, "kidscafe", 10.65, 1.25, 2.05, 4.85, "Ngam Ngam｜親子餐廳")

phone_demo("Buzz 首頁：大家最近在愛什麼，一頁看完", "LaLa Buzz", "buzz",
           [("Buzz of the Week", "本週聲量最高的店或活動"),
            ("分類切換", "Makan、ACG、Outlet、Family"),
            ("Buzz Score＋趨勢", "★4.8、128 篇、▲32%：好不好、紅不紅都看得到")],
           "顧客進館前先滑 Buzz，就知道今天要去哪一家", photo=A + "mock_hero3.jpg")

phone_demo("店家頁：AI 摘要＋網友原話，決定要不要過去", "LaLa Buzz", "brand",
           [("92% love it", "Pandora AI 判定的好評比例與篇數"),
            ("大家愛什麼", "Creamy paitan、Value for money…自動生成標籤"),
            ("Web Buzz／Real Talk", "網路原文附來源；館內已購者的真心話"),
            ("Take me there", "一鍵導航，或寫 Real Talk 拿 +20 pts")],
           "從「看到好評」到「走進店裡」，只差一個按鈕", keys2=["realtalk"])

s = d.info("真實性三道關：只放好評，但每一則都是真的", label="Trust & Safety",
           banner="好評專區不是洗評價：來源公開、已購認證、AI＋人工雙審")
d.columns(s, [("關卡 1", "#15325E", "來源公開", "Web Buzz 每一則都附\n原貼文連結與日期\n業配標記自動排除"),
              ("關卡 2", ORANGE, "已購認證", "Real Talk 必須先掃發票\nVerified purchase ✓\n一張發票只能寫一次"),
              ("關卡 3", MINT, "AI＋人工審核", "AI 先擋不當內容、個資\n商場小編每日複核\n店家可申請回覆")])

# ---------------------------------------------------------------- 8 落地
d.divider("落地與 KPI", "Activation、時程、分工、KPI", key="落地")
d.social_idea("A", "LaLaport BBCC × ACG", "ACG Season Pass：把 ACG Matsuri 變成 App 裡的季賽",
              "每季一張 Season Pass：集章、聯名咖啡任務、KLP48 劇場打卡；完成可換限定扭蛋與活動優先入場。"
              "（AI 示意圖）", A + "app/acg_event.jpg")
d.social_idea("B", "MOP KLIA Sepang × 旅客", "Transit Quest：轉機前 3 小時，在 Outlet 升一級",
              "接 Batik Air 合作與 Tourist Privilege Pass：旅客下載即升 Explorer 試用 30 天、"
              "KLIA 轉乘專屬任務與退稅提醒，讓一次性的旅客也留下會員資料。（AI 示意圖）", A + "klia_outlet.jpg")

s = d.info("先上最痛的三件事，再把遊戲一層層加上去", label="時程",
           banner="Phase 0 先解決「集點麻煩」，Phase 1 再讓人「想玩」")
d.timeline(s, 1.8, ["2027/01", "2027/04", "2027/07", "2027/10", "2028/01"],
           [("P0｜分級＋AI 發票＋Buzz 唯讀", 0, 0.33),
            ("P1｜Quest・Capsule・Ask LaLa", 0.25, 0.6),
            ("P2｜Matsuri Pass・Real Talk", 0.5, 0.85),
            ("P3｜KLIA Transit・For You", 0.72, 1.0)])
d.table(s, ["", "三井 Mitsui Shopping Park", "騰雲 TurnCloud"],
        [["內容", "等級權益、活動檔期、店家合作", "UI/UX 設計、Prototype、文案在地化"],
         ["系統", "既有 App／會員資料提供", "分級引擎、AI 發票、Ask LaLa、遊戲模組"],
         ["數據", "門檻與權益決策", "Pandora 口碑爬取、Buzz Score、CRM 儀表板"]],
        y=3.85, col_w=[1.0, 4.0, 4.0], size=12.5, row_h=0.5)

s = d.info("KPI：一年內，把集點率從 5% 拉到 20%", label="KPI",
           banner="每一層都看得到數字：Phase 0 的數據，就是 Phase 1 權益調整的依據",
           source="目標值為試算示意，正式目標依三井現有會員數與 App 數據校正")
d.table(s, ["指標", "現況", "Phase 0（3 個月）", "上線 12 個月（示意）"],
        [["App 集點會員比例", "5%", "10%", "20%"],
         ["MAU／會員數", "—", "20%", "35%"],
         ["每月發票登錄筆數", "—", "20,000", "60,000"],
         ["平均月造訪次數", "—", "+0.2 次", "+0.6 次"],
         ["Real Talk 分享則數／月", "0", "500", "3,000"],
         ["Explorer 以上會員占比", "—", "15%", "30%"]],
        col_w=[3.0, 1.6, 2.4, 2.6], size=14, row_h=0.6, hot_row=0)

d.closing("每一次來，都在升級。",
          "Next Step\n① 11 月：確認四級門檻與權益方向\n② 12 月：Prototype 使用者測試（20 位 18–34 歲會員）\n"
          "③ 2027/01：Phase 0 開發啟動（分級＋AI 發票＋Buzz）",
          logos=[TC])
d.save("MSP_App3.0_LaLaQuest_提案.pptx")
import json
json.dump(META, open("web_meta.json", "w"))
