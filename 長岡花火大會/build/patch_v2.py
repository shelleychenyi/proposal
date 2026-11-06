p='build_deck.py'; s=open(p).read()
def rep(a,b):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b,1)
rep('OUT = os.path.join(ROOT, "【繁中版】長岡花火 台灣市場Inbound推廣施策提案202611.pptx")','OUT = os.path.join(ROOT, "【繁中版】長岡花火 台灣市場Inbound推廣施策提案202611_V.2.pptx")')
a=s.index("# ================================================================ 1-4 聲量分析②")
b=s.index("# ================================================================ 2-0 提案概念")
s=s[:a]+open('blk_14.py').read()+s[b:]
rep('["IG Reels・旅遊 KOL・在日台灣人 KOC", "欣傳媒 旅遊特集", "1月「正三尺玉」新年話題"], "2-2・2-4・2-5"','["IG Reels・旅遊 KOC・在日台灣人 KOC", "雄獅×欣傳媒 專訪文章＋社群", "1月「正三尺玉」新年話題"], "2-4・2-6・2-7"')
rep('["Threads 繁中官方帳號", "Threads KOC 攻略文", "GEO（AI 搜尋）＋繁中官方指南"], "2-1・2-3"','["Threads 繁中官方帳號", "Threads KOC 攻略文", "GEO（AI 搜尋）＋繁中官方指南"], "2-3・2-5"')
rep('["旅行社・OTA 的觀覽席行程", "抽選前・訪日中的廣告", "季節別 Banner"], "2-4・2-6・2-7"','["雄獅旅遊的觀覽席行程", "抽選前・訪日中的廣告", "季節別 Banner"], "2-6・2-8・2-9"')
a=s.index("# ================================================================ 2-1 聲量對策 Threads")
s=s[:a]+open('blk_fun.py').read()+s[a:]
rep('page("2-1. 聲量對策｜Threads 繁中官方帳號 × KOC",','page("2-3. 聲量對策｜Threads 繁中官方帳號 × Threads KOC",')
rep('"Threads KOC 成果保證型（在日台灣人・旅遊 KOC）"','"Threads KOC 成果保證型（粉絲 3,000＋）"')
rep('page("2-2. 認知擴大｜Instagram Reels × 旅遊 KOL",','page("2-4. 認知擴大｜Instagram Reels × 旅遊 KOC",')
rep('"旅遊 KOL（同行拍攝）",\n     ["・旅遊・攝影類 KOL",','"旅遊 KOC（粉絲 1〜10萬）",\n     ["・旅遊・攝影類 KOC",')
rep('"在日台灣人 KOC（IG UGC）"','"在日台灣人 IG KOC（粉絲 5,000〜1萬）"')
rep('page("2-3. GEO 對策｜','page("2-5. GEO 對策｜')
rep('page("2-5. 年間發信計畫｜','page("2-7. 年間發信計畫｜')
rep('page("2-6. Meta・Google 廣告｜','page("2-8. Meta・Google 廣告｜')
rep('page("2-7. 視覺提案｜','page("2-9. 視覺提案｜')
rep('推薦 OTA 的當日往返接駁・觀覽席行程','推薦雄獅旅遊的當日往返・觀覽席行程')
rep('廣告 → 繁中官方指南 → 旅行社・OTA 行程頁','廣告 → 欣傳媒專訪・繁中官方指南 → 雄獅行程頁')
rep('("欣傳媒 特集・旅行社", 3, 8, "0F4C81", "特集 → 觀覽席行程販售 → 現場")','("雄獅×欣傳媒", 3, 8, "0F4C81", "專訪刊登・社群推播 → 觀覽席行程販售 → 現場")')
rep('IG Reels 擴散感動、Threads 回答問題、旅行社行程讓人去得成。','IG Reels 擴散感動、Threads 回答問題、雄獅行程讓人去得成。')
a=s.index("# ================================================================ 2-4 旅行社・OTA・媒體")
b=s.index("# ================================================================ 2-5 年間發信")
s=s[:a]+open('blk_xin.py').read()+s[b:]
s=s.replace("KOL・KOC","KOC").replace("旅遊 KOL","旅遊 KOC").replace("KOL","KOC")
rep('''order = [cover, company, service, domain3, sec1, p11, media, p13, p14,
         sec2, p20, p21, p22, p23, p24, p25, p26, p27, pdes, psch, thanks]''','''order = [cover, company, service, domain3, sec1, p11, media, p13, p14, p15,
         sec2, p20, p2f, pkoc, p21, p22, p23, p24, p25, p26, p27, pdes, psch, thanks]''')
open(p,'w').write(s); print("patched")
