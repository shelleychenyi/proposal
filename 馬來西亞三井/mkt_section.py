"""One More Thing: the marketing loop that sends people into the app (EN + ZH).
Rebuilt from LaLaport_Marketing_EN.pptx in the TurnCloud template; partner branding removed."""
from pptx.dml.color import RGBColor
from pptx.util import Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY, GOLD, GOLD_L = "#13294B", "#B8975A", "#E8D6AE"
RED, YEL, SOFT = "#E0283C", "#F6E27F", "#F3F1EC"
M = "assets/mkt/"


def add_marketing(d, lang, meta=None):
    T = (lambda en, zh: en) if lang == "en" else (lambda en, zh: zh)
    C = lambda s, x, y, w, h, t, sz, **k: d.tx(s, x, y, w, h, t, sz, align=PP_ALIGN.CENTER, **k)  # noqa: E731

    def num(s, x, y, n):
        d.round(s, x, y, 0.3, 0.3, "cyan", 0.5)
        C(s, x, y + 0.035, 0.3, 0.24, str(n), 10.5, color="white", bold=True)

    def chev(s, x, y):
        d.rect(s, x, y, 0.16, 0.34, "cyan", MSO_SHAPE.CHEVRON)

    def chip(s, x, y, w, text, col, h=0.3, size=9.5):
        d.round(s, x, y, w, h, "white", 0.5).line.color.rgb = RGBColor.from_string(col[1:])
        d.rect(s, x + 0.1, y + h / 2 - 0.05, 0.1, 0.1, col, MSO_SHAPE.OVAL)
        d.tx(s, x + 0.25, y, w - 0.3, h, text, size, bold=True, anchor=MSO_ANCHOR.MIDDLE)

    def gbar(s, x, y, w, h, c1="#1B2F78", c2="#2B7BC0"):
        r = d.rect(s, x, y, w, h, c1)
        r.fill.gradient()
        r.fill.gradient_angle = 0
        st = r.fill.gradient_stops
        st[0].color.rgb, st[1].color.rgb = RGBColor.from_string(c1[1:]), RGBColor.from_string(c2[1:])
        return r

    d.cur = "omt"  # no chapter number on these pages

    # ------------------------------------------------------------ cover
    s = d._new(bg="#0A1225")
    vx, vw = 13.333 - 7.5 * 806 / 720, 7.5 * 806 / 720  # Banaverse clip, left navy cropped off (AI tag burned in)
    d.movie(s, f"assets/video_r/omt_{lang}.mp4", f"assets/poster_r/omt_{lang}.jpg", vx, 0, vw, 7.5)
    if meta is not None:
        meta["video"].setdefault(d.n, []).append([f"omt_{lang}", vx, 0, vw, 7.5])
    d.tx(s, 0.9, 1.75, 4.6, 0.4, "ONE MORE THING", 14, color="accent", bold=True)
    d.tx(s, 0.85, 2.25, 4.8, 1.9, T("We don't just\nbuild the app.\nWe fill it.", "不只做 APP，\n還幫你\n把人送進來。"), 34, color="white",
         bold=True, spacing=1.1)
    d.tx(s, 0.9, 4.75, 4.0, 1.6, T("Pandora listens, Banana creates, Adriana buys the media. Nine channels, from Meta and TikTok to Xiaohongshu "
                                  "and VariFlight, all ending in the MSP app and its CRM.",
                                  "Pandora 聽、Banana 做、Adriana 投。從 Meta、TikTok 到小紅書、飛常準，9 個渠道，全部導回 MSP APP 與會員 CRM。"),
         12.5, color="gold", spacing=1.5)

    # ------------------------------------------------------------ 1 closed loop
    s = d.info(T("How it runs: one loop that sends people to LaLaport and back into the CRM",
                 "怎麼運作：一個把人送進 LaLaport、再回到 CRM 的閉環"),
               label="One More Thing | Flywheel",
               banner=T("Every round feeds the CRM, so the next round knows who to reach and what to say.",
                        "每跑一輪都回到 CRM，下一輪就更知道要找誰、說什麼。"),
               source=T("Data source: TurnCloud / Accucrazy product specs (Meta direct account, Google certified partner); 6,888 posts: Pandora, Malaysia, Nov 2025–Nov 2026; 5% → 20% illustrative.",
                        "資料來源：AI Agent 功能依騰雲／Accucrazy 產品規格；Accucrazy 為 Meta 直營代理、Google 認證夥伴。6,888 篇：Pandora 馬來西亞 IG＋Threads（2025/11–2026/11）。5%→20% 為 App 3.0 目標（示意）。"))
    # 1 data in
    d.round(s, 0.6, 1.2, 2.5, 4.55, SOFT, 0.05)
    num(s, 0.72, 1.32, 1)
    d.tx(s, 1.1, 1.33, 1.9, 0.3, T("Data in", "數據進來"), 12.5, bold=True)
    for i, (t, ds) in enumerate([(T("Website", "官網"), T("Visits, event-page clicks (pixel, GA4)", "瀏覽、活動頁點擊（pixel、GA4）")),
                                 (T("MSP App", "MSP APP"), T("Installs, receipts, parking, vouchers", "下載、發票、停車、券")),
                                 (T("Social & word of mouth", "社群與口碑"), T("IG, Threads, FB: 6,888 posts / 12 mo.", "IG、Threads、FB：一年 6,888 篇")),
                                 (T("Ad results", "廣告成效"), T("Every channel, by creative & audience", "各渠道、各素材、各受眾"))]):
        y = 1.78 + i * 0.98
        d.round(s, 0.72, y, 2.26, 0.86, "white", 0.1)
        d.tx(s, 0.85, y + 0.08, 2.05, 0.3, t, 11, bold=True, color=NAVY)
        d.tx(s, 0.85, y + 0.38, 2.05, 0.45, ds, 9, color="mid", spacing=1.1)
    chev(s, 3.17, 3.3)
    # 2 agents
    num(s, 3.42, 1.22, 2)
    d.tx(s, 3.8, 1.23, 5.8, 0.3, T("Three AI agents turn the data into reach", "三個 AI Agent 把數據變成觸及"), 12.5, bold=True)
    for i, (img, nm, role, l1, l2) in enumerate([
        ("pandora", "Pandora", T("LISTEN", "聆聽"), T("Reads every post and ad result, daily", "每天讀遍貼文與廣告成效"), T("Malay Threads asks, parking talk, monthly B.E.S.S.", "馬來語提問、停車聲量、每月 B.E.S.S.")),
        ("banana", "Banana", T("CREATE", "創意"), T("One idea → 30+ assets in 10 minutes", "一個點子 10 分鐘變 30+ 素材"), T("Drop-day visuals, Chinese guide carousels", "新品日主視覺、中文攻略輪播")),
        ("adriana", "Adriana", T("AMPLIFY", "投放"), T("Reads an ad account in 30 sec, reports itself", "30 秒讀懂廣告帳戶、自動報表"), T("Install ads on drop days & parking talk", "新品日、停車話題時投下載廣告"))]):
        x = 3.4 + i * 2.1
        d.round(s, x, 1.62, 1.98, 1.95, "white", 0.06).line.color.rgb = RGBColor.from_string("E3DFD7")
        d.cover_pic(s, M + f"{img}.jpg", x + 0.06, 1.68, 1.86, 0.66)
        d.tx(s, x + 0.12, 2.4, 1.0, 0.28, nm, 12, bold=True, color=NAVY)
        d.tx(s, x + 1.05, 2.43, 0.85, 0.24, role, 8.5, bold=True, color="cyan", align=PP_ALIGN.RIGHT)
        d.tx(s, x + 0.12, 2.7, 1.78, 0.4, l1, 9, spacing=1.1)
        d.tx(s, x + 0.12, 3.1, 1.78, 0.42, T("For LaLaport: ", "LaLaport：") + l2, 8.5, color="mid", spacing=1.1)
    # 3 out to market
    d.round(s, 3.4, 3.7, 6.18, 2.05, SOFT, 0.06)
    num(s, 3.52, 3.8, 3)
    d.tx(s, 3.9, 3.8, 3.0, 0.3, T("Out to market", "送到市場"), 12.5, bold=True)
    d.tx(s, 5.6, 3.84, 3.9, 0.26, T("9 CHANNELS WE BUY, RUN AND OPERATE", "我們投放、經營的 9 個渠道"), 9, bold=True, color="cyan",
         align=PP_ALIGN.RIGHT)
    paid = [("Meta · FB / IG", "#0866FF"), ("Google · Search", "#4285F4"), ("YouTube", "#FF0000"), ("TikTok", "#111111"),
            ("Threads", "#333333"), (T("ChatGPT · GEO", "ChatGPT・GEO"), "#10A37F"), (T("Xiaohongshu", "小紅書"), "#FF2442"),
            (T("VariFlight", "飛常準"), "#2F7BEA")]
    for i, (t, c) in enumerate(paid):
        chip(s, 3.55 + (i % 4) * 1.5, 4.22 + (i // 4) * 0.4, 1.42, t, c)
    d.tx(s, 3.55, 5.03, 3.0, 0.22, T("EARNED & OWNED", "口碑與自有"), 8.5, bold=True, color="mid")
    for i, (t, w) in enumerate([(T("Creators & KOC · BM / EN / CN", "KOL・KOC（馬來／英／中）"), 2.3),
                                (T("Threads replies", "Threads 回覆"), 1.45), (T("LaLa Buzz in app", "APP 內 LaLa Buzz"), 1.62)]):
        x = 3.55 + [0, 2.38, 3.91][i]
        chip(s, x, 5.28, w, t, GOLD)
    chev(s, 9.66, 3.3)
    # 4 convert
    d.round(s, 9.9, 1.2, 2.85, 2.38, SOFT, 0.06)
    num(s, 10.02, 1.32, 4)
    d.tx(s, 10.4, 1.33, 2.3, 0.3, T("Convert in the MSP App", "在 MSP APP 轉換"), 12, bold=True)
    for i, t in enumerate([T("Install from every post & ad (UTM · QR)", "貼文、廣告都導下載（UTM・QR）"),
                           T("Register plate: LaLa Park perks", "登錄車牌，拿 LaLa Park 優惠"),
                           T("Book LaLa Go, get the RM10 e-Voucher", "訂 LaLa Go，拿 RM10 e-Voucher"),
                           T("Submit receipts, enter the draw", "登錄發票、參加抽獎")]):
        y = 1.75 + i * 0.4
        d.tx(s, 10.02, y, 0.25, 0.3, "✓", 11, bold=True, color="cyan")
        d.tx(s, 10.27, y + 0.02, 2.4, 0.4, t, 9, spacing=1.05)
    d.round(s, 10.02, 3.36 - 0.06, 2.6, 0.24, "#DDEFF6", 0.3)
    d.tx(s, 10.05, 3.32, 2.55, 0.22, T("Members earning in-app 5% → 20%", "APP 內累點會員 5% → 20%"), 8.5, bold=True, color=NAVY,
         align=PP_ALIGN.CENTER)
    # 5 CRM
    d.round(s, 9.9, 3.7, 2.85, 2.05, NAVY, 0.06)
    num(s, 10.02, 3.82, 5)
    d.tx(s, 10.4, 3.83, 2.3, 0.3, T("CRM · member data", "CRM・會員數據"), 12, bold=True, color="white")
    d.tx(s, 10.02, 4.2, 2.65, 0.5, T("Every receipt, visit and tier in one member record", "每張發票、每次來店、等級，都在同一筆會員紀錄"),
         9, color="white", spacing=1.1)
    for i, t in enumerate([T("Fandom fans", "追星粉絲"), T("Malay weekend planners", "馬來週末族"), T("Chinese guide readers", "華語攻略族"),
                           T("Parking-minded drivers", "在意停車的車主"), T("China flyers via KLIA", "KLIA 中國旅客")]):
        x, y = 10.02 + (i % 2) * 1.35, 4.75 + (i // 2) * 0.33
        d.round(s, x, y, 1.28, 0.26, "#22406E", 0.5)
        C(s, x, y + 0.04, 1.28, 0.2, t, 7.5, color="white", bold=True)
    d.round(s, 0.6, 5.83, 12.15, 0.3, "#E2F4F9", 0.5)
    d.tx(s, 0.8, 5.86, 11.8, 0.24, T("↺  Back into the loop: member segments become Adriana's lookalike and retargeting audiences; what members buy and post sets Pandora's next brief.",
                                     "↺  回到閉環：會員分群回到 Adriana 做類似受眾與再行銷；會員買什麼、說什麼，決定 Pandora 下一輪的題目。"),
         9.5, bold=True, color=NAVY)

    # ------------------------------------------------------------ 2 channels
    s = d.info(T("9 doors we can open to send people to LaLaport", "我們能打開的 9 扇門，把人送進 LaLaport"),
               label="One More Thing | Channels",
               banner=T("One team, one budget, nine channels: locals, fans, Chinese-speaking travellers and China flyers.",
                        "一個團隊、一份預算、九個渠道：在地人、粉絲、華語旅客、中國航班旅客全都觸及。"),
               source=T("Data source: Facebook users, TikTok ad reach: DataReportal Digital 2026 Malaysia (via Elite Asia); ChatGPT: Marketing Magazine Malaysia; VariFlight: official; LaLaport: Pandora.",
                        "資料來源：Meta 受眾、TikTok 廣告觸及：DataReportal Digital 2026 Malaysia（Elite Asia 整理）；ChatGPT：Marketing Magazine Malaysia（2026）；飛常準：官方數據；LaLaport Threads／IG：Pandora（2025/11–2026/11）。"))
    ch = [("#0866FF", T("Meta · Facebook / Instagram", "Meta・Facebook／Instagram"), T("23.0M Facebook users in Malaysia", "馬來西亞 Facebook 2,300 萬人"),
           T("Drop-day launches and install ads; Reels for fandom tenants.", "新品日發佈＋下載廣告；粉絲型店鋪的 Reels。")),
          ("#4285F4", "Google · Search / Maps / PMax", T("Catch people the moment they search", "在對方搜尋的那一刻出現"),
           T("\"LaLaport parking\", \"bus to Singapore\" lead straight to the app.", "「LaLaport 停車」「去新加坡巴士」直接導進 APP。")),
          ("#FF0000", "YouTube", T("Big-screen video, before the weekend", "週末前的大螢幕影音"),
           T("Pudu heritage films, event recaps, 6-sec bumpers on Fridays.", "Pudu 歷史短片、活動回顧、週五 6 秒廣告。")),
          ("#111111", "TikTok", T("Ad reach = 86.8% of MY internet users", "廣告觸及＝大馬網民 86.8%"),
           T("Creator challenges at Rooftop Garden; Spark Ads boost the winners.", "屋頂花園創作者挑戰；Spark Ads 放大爆款。")),
          ("#333333", "Threads", T("Where young Malaysians plan the weekend", "大馬年輕人在這裡排週末"),
           T("33% of LaLaport Threads is in Malay: a \"Jom LaLaport\" post every Friday 6 pm.", "LaLaport 的 Threads 有 33% 是馬來語：每週五 6 點發「Jom LaLaport」。")),
          ("#10A37F", T("ChatGPT & AI search · GEO", "ChatGPT・AI 搜尋（GEO）"), T("About half of MY internet users use ChatGPT", "約一半大馬網民用 ChatGPT"),
           T("Make LaLaport the answer to \"where to go in KL this weekend\".", "讓「這週末 KL 去哪」的 AI 答案是 LaLaport。")),
          ("#FF2442", T("Xiaohongshu (RED)", "小紅書"), T("Where Chinese-speaking travellers plan", "華語旅客做功課的地方"),
           T("Guides and KOC notes for BBCC and MOP; search and feed ads.", "BBCC、MOP 攻略與 KOC 筆記；搜尋＋資訊流廣告。")),
          ("#2F7BEA", T("VariFlight", "飛常準 VariFlight"), T("45M+ monthly users tracking flights", "月活 4,500 萬+ 的航班 APP"),
           T("Reach China flyers landing at KLIA: MOP outlet + LaLa Go shuttle.", "鎖定降落 KLIA 的中國旅客：MOP Outlet＋LaLa Go 接駁。")),
          (GOLD, T("Creators & KOC · BM / EN / CN", "KOL・KOC（馬來／英／中）"), T("Micro-creators in three languages", "三語微型創作者"),
           T("Chinese guides average 2,915 likes, 3× the Instagram norm.", "繁中攻略平均 2,915 讚，是 IG 平均的 3 倍。"))]
    LOGOS = [["facebook", "instagram"], ["google"], ["youtube"], ["tiktok"], ["threads"], ["chatgpt"], ["red"], ["variflight"], ["koc"]]
    for i, (c, nm, reach, use) in enumerate(ch):
        x, y = 0.6 + (i % 3) * 4.08, 1.22 + (i // 3) * 1.6
        d.round(s, x, y, 3.95, 1.48, "white", 0.06).line.color.rgb = RGBColor.from_string("E3DFD7")
        d.rect(s, x, y + 0.12, 0.07, 1.24, c)
        lx = x + 0.25
        for lg in LOGOS[i]:
            if lg == "koc":
                d.round(s, lx, y + 0.1, 0.42, 0.42, GOLD, 0.5)
                C(s, lx, y + 0.21, 0.42, 0.2, "KOC", 8.5, color="white", bold=True)
            else:
                d.fit(s, M + f"logo/{lg}.png", lx, y + 0.1, 0.42, 0.42)
            lx += 0.48
        d.tx(s, lx + 0.04, y + 0.14, x + 3.85 - lx, 0.32, nm, 13 if i == 0 else 13.5, bold=True, color=NAVY)
        d.tx(s, x + 0.25, y + 0.6, 3.6, 0.3, reach, 11, bold=True, color=c if c not in ("#111111", "#333333") else "#3A3A3A")
        d.tx(s, x + 0.25, y + 0.92, 3.6, 0.55, use, 10, color="mid", spacing=1.15)
        if nm.startswith(("Xiao", "小紅", "Vari", "飛常")):
            d.round(s, x + 2.95, y + 0.19, 0.85, 0.24, RED, 0.5)
            C(s, x + 2.95, y + 0.22, 0.85, 0.2, T("CHINA", "中國渠道"), 8, color="white", bold=True)

    # ------------------------------------------------------------ 3 Xiaohongshu
    s = d.info(T("Xiaohongshu (RED): in the plan before Chinese-speaking travellers land",
                 "小紅書：在華語旅客做功課時，就把 LaLaport 排進行程"),
               label="One More Thing | Xiaohongshu",
               banner=T("Content + word of mouth + performance ads: RED reaches the travellers who are already planning KL.",
                        "內容＋口碑＋效果廣告：在小紅書接住正在規劃吉隆坡行程的旅客。"),
               source=T("Data source: Xiaohongshu ad products; Chinese-guide likes: Pandora post pool, Malaysia, Instagram, Nov 2025–Nov 2026.",
                        "資料來源：小紅書廣告產品；華語攻略讚數：Pandora 馬來西亞 Instagram（2025/11–2026/11）。"))
    d.round(s, 0.6, 1.22, 5.0, 2.55, "white", 0.05).line.color.rgb = RGBColor.from_string("FF2442")
    d.fit(s, M + "red_icon.png", 0.8, 1.38, 0.55, 0.55)
    d.tx(s, 1.5, 1.45, 4.0, 0.4, T("What RED can do", "小紅書能做什麼"), 15, bold=True, color="#FF2442")
    for i, (b, t) in enumerate([(T("Spark real UGC", "帶動真實 UGC"), T("Word-of-mouth notes that make people post their own", "口碑筆記，讓旅客自己也發文")),
                                (T("Awareness → visit", "認知 → 到店"), T("Feed ads, search-keyword ads, creator-boosted ads", "資訊流、搜尋關鍵字、達人加熱廣告")),
                                (T("Beyond posts", "不只發文"), T("Coupons, campaign spread, fan groups, surveys, ticketing", "優惠券、活動擴散、粉絲群、問卷、票券"))]):
        y = 2.08 + i * 0.55
        d.tx(s, 0.85, y, 1.5, 0.5, b, 11, bold=True, color=NAVY)
        d.tx(s, 2.4, y, 3.1, 0.5, t, 10.5, color="mid", spacing=1.1)
    d.round(s, 0.6, 3.92, 5.0, 2.15, NAVY, 0.05)
    d.tx(s, 0.85, 4.05, 4.6, 0.3, T("Why it fits LaLaport", "為什麼適合 LaLaport"), 13, bold=True, color=GOLD_L)
    for i, (big, t) in enumerate([("BBCC", T("Bukit Bintang: on every Chinese visitor's KL list", "武吉免登：華語旅客必排的 KL 景點")),
                                  ("MOP", T("KLIA Sepang: first and last stop of the trip", "KLIA 雪邦：旅程的第一站與最後一站")),
                                  ("3×", T("Chinese guides already earn 3× the likes on IG", "華語攻略在 IG 已拿到 3 倍讚數"))]):
        y = 4.45 + i * 0.52
        d.tx(s, 0.85, y, 1.1, 0.45, big, 17, bold=True, color="white")
        d.tx(s, 2.0, y + 0.07, 3.5, 0.45, t, 10.5, color="white")
    # flow
    C(s, 5.9, 1.25, 6.85, 0.35, T("Content + word of mouth + ads → the right users", "內容投稿＋口碑＋運用型廣告 → 觸及對的用戶"), 13, bold=True, color=NAVY)
    d.round(s, 6.0, 1.9, 2.55, 3.4, "#FDEEF0", 0.06)
    C(s, 6.0, 2.05, 2.55, 0.35, "Phase 1", 16, bold=True, color="#C8102E")
    C(s, 6.0, 2.42, 2.55, 0.3, T("Contents", "內容"), 13, bold=True, color=NAVY)
    C(s, 6.1, 2.9, 2.35, 1.0, T("LaLaport official RED account\nor\nour KL travel-info account\n(posts + ads)",
                               "LaLaport 官方帳號\n或\n我們經營的 KL 旅遊資訊帳號\n（投稿＋廣告）"), 10.5, color="ink", spacing=1.2)
    d.round(s, 6.15, 4.45, 2.25, 0.6, "white", 0.2).line.color.rgb = RGBColor.from_string("C8102E")
    C(s, 6.15, 4.5, 2.25, 0.5, T("Builds the brand's\nposition", "建立品牌定位"), 10, bold=True, color="#C8102E")
    for j, (y, a, b) in enumerate([(2.35, T("High-interest users", "高興趣用戶"), T("trend building", "培養趨勢")),
                                   (4.05, T("Precise audiences", "精準受眾"), T("quality notes surface", "優質筆記曝光"))]):
        d.rect(s, 8.75, y + 0.3, 0.75, 0.3, "#BFBFBF", MSO_SHAPE.RIGHT_ARROW)
        C(s, 8.6, y - 0.15, 1.05, 0.45, a, 8.5, color="#C8102E", bold=True)
        C(s, 8.6, y + 0.62, 1.05, 0.3, b, 8.5, color="#C8102E")
    d.round(s, 9.7, 1.75, 3.05, 3.7, "white", 0.05).line.color.rgb = RGBColor.from_string("C8102E")
    d.round(s, 9.7, 1.62, 1.25, 0.3, "#C8102E", 0.2)
    C(s, 9.7, 1.65, 1.25, 0.24, T("RECOMMENDED", "推薦"), 9, bold=True, color="white")
    for j, (y, ttl, sub, note) in enumerate([(2.05, T("Phase 2 · Word of mouth", "Phase 2・口碑"), "KOL & KOC",
                                               T("Travel, food and shopping creators", "旅遊、美食、購物類達人")),
                                              (3.75, T("Phase 2 · Performance ads", "Phase 2・效果廣告"), T("Run from our ad account", "由我們的廣告帳戶投放"),
                                               T("Search + feed, optimised weekly", "搜尋＋資訊流，每週優化"))]):
        d.round(s, 9.85, y, 2.75, 1.2, "#FDEEF0", 0.08)
        C(s, 9.85, y + 0.1, 2.75, 0.3, ttl, 12, bold=True, color=NAVY)
        C(s, 9.85, y + 0.45, 2.75, 0.3, sub, 11, bold=True, color="#C8102E")
        C(s, 9.85, y + 0.8, 2.75, 0.3, note, 9.5, color="mid")
    C(s, 9.7, 3.3, 3.05, 0.4, "or", 15, bold=True, color="#C8102E")
    C(s, 5.9, 5.55, 6.85, 0.35, T("For LaLaport: \"BBCC in a day\", \"MOP before your flight\", \"ACG Base map\" notes, each ending in the app QR.",
                                  "LaLaport 題目：「BBCC 一日攻略」「登機前逛 MOP」「ACG Base 地圖」，每篇都附 APP QR。"), 9.5, bold=True, color=NAVY)

    # ------------------------------------------------------------ 4 VariFlight
    s = d.info(T("VariFlight: meet China's flyers before they land at KLIA", "飛常準 VariFlight：在中國旅客降落 KLIA 前就遇見他們"),
               label="One More Thing | VariFlight",
               banner=T("The flight app 45M people open every month: reach them on arrival day, send them to MOP and BBCC.",
                        "每月 4,500 萬人打開的航班 APP：在降落當天觸及，把人送到 MOP 與 BBCC。"),
               source=T("Data source: VariFlight official figures (downloads, members, MAU, DAU). App screen for illustration.",
                        "資料來源：飛常準官方數據（下載、會員、月活、日活）。APP 畫面僅供示意。"))
    d.fit(s, M + "variflight_app.jpg", 0.7, 1.25, 2.4, 4.75)
    for i, (n, t) in enumerate([("300M+", T("total downloads", "累計下載")), ("100M+", T("registered members", "註冊會員")),
                                ("45M+", T("monthly active users", "月活躍用戶")), ("9M+", T("daily active users", "日活躍用戶"))]):
        y = 1.25 + i * 1.18
        d.tx(s, 3.4, y, 3.4, 0.75, n, 40, bold=True, color=RED, font=d.num_font)
        d.tx(s, 3.45, y + 0.72, 3.4, 0.3, t, 12, bold=True, color=NAVY)
    d.round(s, 7.05, 1.22, 5.7, 1.2, SOFT, 0.06)
    d.fit(s, M + "variflight_icon.png", 7.2, 1.35, 0.5, 0.5)
    d.tx(s, 7.85, 1.35, 4.8, 0.35, T("What it is", "這是什麼"), 13, bold=True, color=NAVY)
    d.tx(s, 7.85, 1.7, 4.8, 0.7, T("China's go-to real-time flight-status app: tracking, booking and tickets, built on data from airports, airlines and air traffic control.",
                                   "中國最普及的即時航班動態 APP：航班追蹤、訂票購票；資料來自機場、航空公司與空管，準確可信。"), 10, color="mid", spacing=1.15)
    d.tx(s, 7.05, 2.55, 5.7, 0.3, T("Its own segment model, ready to target", "自有的用戶分群，可直接鎖定"), 12, bold=True, color=NAVY)
    segs = [T("Business & first class", "商務／頭等艙"), T("Families flying with kids", "親子家庭"), T("Frequent international flyers", "高頻國際線旅客"),
            T("Seniors who travel well", "銀髮品質旅客"), T("Airline-industry users", "航空業相關用戶"), T("Price-sensitive travellers", "價格敏感族"),
            T("Members by tier", "會員等級分群"), T("Students & free travellers", "學生・自由行")]
    for i, t in enumerate(segs):
        x, y = 7.05 + (i % 2) * 2.88, 2.92 + (i // 2) * 0.4
        chip(s, x, y, 2.78, t, "#2F7BEA", h=0.32, size=9.5)
    d.round(s, 7.05, 4.6, 5.7, 1.45, NAVY, 0.06)
    d.tx(s, 7.3, 4.7, 5.3, 0.3, T("For LaLaport", "用在 LaLaport"), 12.5, bold=True, color=GOLD_L)
    d.tx(s, 7.3, 5.05, 5.3, 1.0, T("China → KLIA flyers see MOP KLIA Sepang on arrival day (\"20 min from your gate\"), then LaLa Go to BBCC "
                                   "with the RM10 e-Voucher. Departing flyers get a \"shop before you fly\" push.",
                                   "中國飛 KLIA 的旅客，降落當天看到 MOP KLIA 雪邦（「離登機門 20 分鐘」），再搭 LaLa Go 進 BBCC、拿 RM10 e-Voucher；回程旅客收到「登機前逛一圈」推播。"),
         10.5, color="white", spacing=1.2)

    # ------------------------------------------------------------ 5 method in one page
    s = d.info(T("How we read LaLaport: 4 numbers, 3 habits, 1 fix", "我們怎麼讀 LaLaport：4 個數字、3 個習慣、1 個要修的痛點"),
               label="One More Thing | B.E.S.S.",
               banner=T("Read the same four numbers every month, then aim each channel at what fans already do.",
                        "每月看同樣四個數字，讓每個渠道都對準粉絲本來就在做的事。"),
               source=T("Data source: Pandora post pool, Malaysia, Instagram + Threads, 14 Nov 2025–13 Nov 2026, N=6,888 posts mentioning LaLaport / BBCC; sentiment 3 May–31 Oct 2026.",
                        "資料來源：Pandora 馬來西亞 Instagram＋Threads，2025/11/14–2026/11/13，提及 LaLaport／BBCC 共 6,888 篇；情緒期間 2026/5/3–10/31。"))
    for i, (k, nm, n, t) in enumerate([("B", "Buzz", "39,550", T("posts + comments", "貼文＋留言")), ("E", "Engagement", "2.36M", T("likes", "讚")),
                                       ("S", "Search", "1,129", T("questions on Threads", "Threads 提問")),
                                       ("S", "Sentiment", "90.7%", T("positive · 1.2% negative", "正面・負面 1.2%"))]):
        x = 0.6 + i * 3.07
        d.round(s, x, 1.22, 2.95, 1.38, NAVY, 0.08)
        d.tx(s, x + 0.2, 1.3, 0.5, 0.5, k, 26, bold=True, color=GOLD)
        d.tx(s, x + 0.75, 1.42, 2.1, 0.3, nm, 12, bold=True, color=GOLD_L)
        d.tx(s, x + 0.2, 1.82, 2.6, 0.5, n, 26, bold=True, color="white", font=d.num_font)
        d.tx(s, x + 0.2, 2.27, 2.6, 0.28, t, 10, color="white")
    for i, (tag, found, do) in enumerate([
        (T("CHANNEL", "渠道"), T("Instagram holds 98% of likes. A third of Threads is in Malay and asks peak 6–9 pm. Chinese guides get 3× the likes.",
                                 "IG 拿下 98% 的讚；Threads 三分之一是馬來語、提問集中在晚上 6–9 點；華語攻略讚數 3 倍。"),
         T("Launch on Instagram, answer on Threads in Malay, guide in Chinese, land it before Friday 6 pm.", "IG 發佈、Threads 用馬來語回覆、中文寫攻略，週五 6 點前到位。")),
        (T("CONTENT", "內容"), T("Artist frames 1.47×, Malaysia firsts 1.56×; Pudu Prison stories get 6× the likes. Discount posts under-perform (0.87×).",
                                 "藝人相框 1.47 倍、大馬首發 1.56 倍；Pudu 監獄故事 6 倍讚；折扣文反而只有 0.87 倍。"),
         T("Own the drop calendar and tell the Pudu story officially.", "掌握新品日曆，官方說好 Pudu 的故事。")),
        (T("PAIN", "痛點"), T("Parking is the only negative score (−0.38). One joke reel about the fee: 34.6K likes.",
                              "停車是唯一負分（−0.38）；一支停車費梗片 3.46 萬讚。"),
         T("Make the app the fix: LaLa Park perks by tier become the install ad.", "讓 APP 成為解方：LaLa Park 分級停車就是下載廣告。"))]):
        x = 0.6 + i * 4.08
        d.round(s, x, 2.78, 3.95, 3.25, SOFT, 0.05)
        d.round(s, x + 0.2, 2.92, 1.2, 0.28, "cyan", 0.5)
        C(s, x + 0.2, 2.95, 1.2, 0.22, tag, 9, bold=True, color="white")
        d.tx(s, x + 0.2, 3.32, 3.55, 0.25, T("WHAT WE FOUND", "我們發現"), 8.5, bold=True, color="mid")
        d.tx(s, x + 0.2, 3.58, 3.55, 1.2, found, 11, spacing=1.2)
        d.round(s, x + 0.2, 4.85, 3.55, 1.05, "white", 0.08)
        d.tx(s, x + 0.35, 4.92, 3.3, 0.25, T("WHAT WE DO", "我們這樣做"), 8.5, bold=True, color=GOLD)
        d.tx(s, x + 0.35, 5.17, 3.3, 0.7, do, 11, bold=True, color=NAVY, spacing=1.15)

    # ------------------------------------------------------------ 6 case
    s = d.info(T("Case · Department store: three Threads posts made it a must-visit stop", "案例｜百貨：三篇 Threads，把百貨排進旅客的行程"),
               label="One More Thing | Case",
               banner=T("Topic → floor → product: word of mouth that ends with a reason to walk in.",
                        "話題 → 樓層 → 商品：每一篇口碑，最後都是一個走進來的理由。"),
               source=T("Data source: Accucrazy client records; Threads post data (Sep 2026). Department store in Okinawa, Japan, targeting Taiwanese travellers; client name withheld. KPI: contracted impressions 15K–100K.",
                        "資料來源：Accucrazy 執行紀錄；Threads 貼文數據（2026/9）。日本沖繩百貨，對象為台灣旅客；客戶名稱不公開。KPI：合約曝光 1.5–10 萬。"))
    steps = [("1", T("Make it a topic", "製造話題"), T("A \"no-plan traveller\" itinerary meme puts the store in the plan twice.", "「P 人行程」梗：朋友排的行程裡，百貨竟然出現兩天。"),
              "796K", T("views · 10K likes · 1,388 comments · 10K shares", "瀏覽・讚 1 萬・留言 1,388・分享 1 萬")),
             ("2", T("Make the floor concrete", "具體到樓層"), T("Rainy-day stop: the 2F select shop is \"the real Japanese lifestyle store\".", "雨天去處：2F 選物店是「真正的日系選物」。"),
              "11K", T("views · 324 likes", "瀏覽・讚 324")),
             ("3", T("Name the product", "指名到商品"), T("Must-buy brown sugar from 8 islands, and where to buy it: 2F.", "八島黑糖是沖繩必買，買的地方就在 2F。"),
              "39K", T("views · 1,094 likes · 873 shares", "瀏覽・讚 1,094・分享 873"))]
    for i, (n, ttl, d1, big, sub) in enumerate(steps):
        x = 0.6 + i * 2.95
        d.round(s, x, 1.22, 2.7, 3.15, "white", 0.06).line.color.rgb = RGBColor.from_string("E3DFD7")
        d.round(s, x + 0.2, 1.38, 0.42, 0.42, NAVY, 0.5)
        C(s, x + 0.2, 1.44, 0.42, 0.3, n, 13, bold=True, color="white")
        d.tx(s, x + 0.75, 1.42, 1.9, 0.35, ttl, 13, bold=True, color=NAVY)
        d.tx(s, x + 0.2, 1.95, 2.35, 1.0, d1, 10.5, spacing=1.2)
        d.tx(s, x + 0.2, 2.95, 2.4, 0.7, big, 34, bold=True, color=RED, font=d.num_font)
        d.tx(s, x + 0.2, 3.65, 2.35, 0.6, sub, 9.5, color="mid", spacing=1.15)
        if i < 2:
            chev(s, x + 2.74, 2.6)
    d.round(s, 0.6, 4.52, 8.6, 1.5, NAVY, 0.06)
    for i, (n, t) in enumerate([("846K", T("views in 1 month", "1 個月瀏覽")), ("~8×", T("the contracted KPI", "合約 KPI 上限")),
                                ("10K+", T("shares: saved as a \"must-go\" list", "分享：被收進「必去清單」"))]):
        x = 0.85 + i * 2.8
        d.tx(s, x, 4.65, 2.6, 0.7, n, 32, bold=True, color=GOLD_L, font=d.num_font)
        d.tx(s, x, 5.38, 2.6, 0.5, t, 10.5, color="white", spacing=1.1)
    d.round(s, 9.4, 1.22, 3.35, 4.8, SOFT, 0.06)
    d.tx(s, 9.6, 1.35, 3.0, 0.35, T("The same play at LaLaport", "放到 LaLaport"), 13, bold=True, color=NAVY)
    for i, (k, t) in enumerate([(T("Topic", "話題"), T("The Pudu story, a K-pop frame drop, Malaysia firsts", "Pudu 故事、K-pop 相框新品、大馬首發")),
                                (T("Floor", "樓層"), T("ACG Base, Rooftop Garden, the LTH bus hub", "ACG Base、屋頂花園、LTH 巴士轉運站")),
                                (T("Product", "商品"), T("Collab-café menus, limited merch, bus to Singapore", "聯名咖啡廳菜單、限定周邊、新加坡巴士")),
                                (T("App", "APP"), T("QR in every post: voucher, check-in, LaLa Park", "每篇都附 QR：券、打卡、LaLa Park"))]):
        y = 1.85 + i * 1.02
        d.round(s, 9.6, y, 0.85, 0.3, GOLD if i == 3 else NAVY, 0.5)
        C(s, 9.6, y + 0.04, 0.85, 0.22, k, 9, bold=True, color="white")
        d.tx(s, 9.6, y + 0.38, 3.0, 0.6, t, 10.5, spacing=1.15)

    # ------------------------------------------------------------ 7 results (wow)
    s = d.info(T("Results: what happened when department stores and retailers ran this loop", "成果：百貨與零售品牌跑過這套閉環之後"),
               label="One More Thing | Before → After",
               banner=T("Department stores and retailers saw the jump within a month. LaLaport is next.",
                        "百貨、零售品牌一個月內就看到跳升。下一個是 LaLaport。"),
               source=T("Data source: Accucrazy client records (names withheld), 2024–2026; before/after on the same conditions (Pandora, Threads, ad managers). Past results, not guarantees.",
                        "資料來源：Accucrazy 執行紀錄（客戶名稱不公開），2024–2026；同條件前後比較（Pandora、Threads、廣告後台）。皆為過往成果，非保證值。"))
    panels = [(T("Department store", "百貨公司"), T("Threads views vs KPI", "Threads 瀏覽 vs KPI"), "8", T("×", "倍"),
               [(100, 0), (796, 1)], [T("KPI", "KPI"), T("Actual", "實績")], T("846K views · 1 month", "1 個月 84.6 萬瀏覽")),
              (T("Discount retailer", "折扣零售"), T("Related posts per week", "每週相關貼文"), "+80", "%",
               [(54, 0), (82, 0), (120, 0), (126, 0), (144, 1), (196, 1), (169, 1), (178, 1)], [T("Before", "執行前"), T("After", "執行後")],
               T("28 days after launch", "執行後 28 天")),
              (T("Apparel retailer", "服飾品牌"), T("Monthly buzz", "月聲量"), "4.8", T("×", "倍"),
               [(1, 0), (4.8, 1)], [T("Month before", "前一個月"), T("Launch month", "啟動月")], T("Official Threads, month 1", "官方 Threads 第 1 個月")),
              (T("Convenience store chain", "連鎖超商"), T("Posts captured", "掌握到的貼文"), "12.4", T("×", "倍"),
               [(1, 0), (12.4, 1)], [T("Old tool", "舊工具"), "Pandora"], T("On Threads alone: 54×", "Threads 單平台：54 倍"))]
    for i, (ttl, metric, big, unit, bars, labels, band) in enumerate(panels):
        x = 0.6 + i * 3.07
        d.tx(s, x, 1.15, 2.95, 0.4, ttl, 15, bold=True, color=NAVY)
        d.rect(s, x, 1.58, 2.0, 0.3, "#1F6FB8")
        d.tx(s, x + 0.12, 1.6, 1.9, 0.26, metric, 10.5, bold=True, color="white")
        # chart frame
        cy0, cy1 = 2.95, 4.85
        d.rect(s, x, cy0, 0.012, cy1 - cy0, "#9A9A9A")
        for g in range(6):
            d.rect(s, x, cy0 + 0.12 + g * (cy1 - cy0 - 0.12) / 6, 2.95, 0.006, "#CFCFCF")
        d.rect(s, x, cy1, 2.95, 0.014, "#9A9A9A")
        vmax = max(v for v, _ in bars)
        n = len(bars)
        gap = 0.08 if n > 4 else 0.35
        bw = (2.75 - gap * (n - 1)) / n
        for j, (v, after) in enumerate(bars):
            bh = max(0.08, (cy1 - cy0 - 0.25) * v / vmax)
            bx = x + 0.12 + j * (bw + gap)
            if after:
                gbar(s, bx, cy1 - bh, bw, bh)
            else:
                d.rect(s, bx, cy1 - bh, bw, bh, "#BFD3EA")
        if n == 2:
            for j, lb in enumerate(labels):
                C(s, x + 0.12 + j * (bw + gap), cy1 + 0.03, bw, 0.22, lb, 8.5, color="mid")
        else:
            C(s, x + 0.12, cy1 + 0.03, 4 * bw + 3 * gap, 0.22, labels[0], 8.5, color="mid")
            C(s, x + 0.12 + 4 * (bw + gap), cy1 + 0.03, 4 * bw + 3 * gap, 0.22, labels[1], 8.5, color="mid")
        bt = d.tx(s, x - 0.02, 1.88, 2.95, 1.05, big, 54, bold=True, color=RED, font=d.num_font, anchor=MSO_ANCHOR.BOTTOM)
        r = bt.text_frame.paragraphs[0].add_run()
        r.text = unit
        r.font.size, r.font.bold = Pt(26), True
        r.font.color.rgb = RGBColor.from_string(NAVY[1:])
        d.rect(s, x, 5.15, 2.95, 0.4, YEL)
        C(s, x, 5.19, 2.95, 0.32, band, 11.5, bold=True, color=NAVY)
    d.round(s, 0.6, 5.68, 12.15, 0.4, SOFT, 0.5)
    d.tx(s, 0.85, 5.73, 11.7, 0.3, T("Also  ·  Department store (Taiwan): 70%+ of its AI Xmas campaign traffic came through its own app and site  ·  "
                                     "E-commerce: Double 11 ROAS 7.4×, orders 6.8×, sports-merch ROAS 2.5–5.0×",
                                     "其他  ·  台灣百貨：AI 聖誕活動 70%+ 流量來自自家 APP 與官網  ·  電商：雙 11 ROAS 7.4 倍、訂單 6.8 倍、運動周邊 ROAS 2.5–5.0 倍"),
         9, color="mid")
