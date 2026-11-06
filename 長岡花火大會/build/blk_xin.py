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

