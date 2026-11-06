s=open('build_quote_zh_src.py').read()
s=s.replace('F = "Microsoft JhengHei"','F = "Meiryo"')
s=s.replace('OUT = os.path.join(ROOT, "【繁中版】Intasect_長岡花火_台灣市場集客施策_3方案報價明細_202612-202709_V.2.xlsx")','OUT = os.path.join(ROOT, "【インタセクト】XXX様_長岡花火_台湾向け集客施策_3プランお見積り_202611.xlsx")')
import json
R=json.load(open('quote_ja_pairs.json'))
for a,b in R:
    assert a in s, a[:50]; s=s.replace(a,b)
a=s.index("kpi = [\n"); b=s.index("]\n",a)+2
s=s[:a]+open('quote_ja_kpi.txt').read()+s[b:]
a=s.index('for n in ["・「保證」'); b=s.index(']:\n',a)
s=s[:a]+open('quote_ja_notes.txt').read()+s[b:]
open('build_quote_ja.py','w').write(s)
print('ok')
