# Pandora → 提案範本 串接

把 Pandora Public API 的實測聲量資料，自動算成指標並回填進提案範本，直接產出可交件的 pptx。

## 檔案

| 檔案 | 用途 |
|---|---|
| `cli.py` | 入口。`check` / `fetch` / `build` / `run` |
| `pandora_client.py` | API client（schema／query） |
| `metrics.py` | 把 posts[] 聚合成指標（聲量、情緒五級、平台分布、月度趨勢） |
| `fill_deck.py` | 依範本裡的具名圖形回填文字，並插入原生圖表 |
| `build_template.py` | 重新產生兩份空白範本（改版型時才需要動） |
| `config.json` | 目前這個案子的設定 |
| `config.example.json` | 新案子用的空白設定 |
| `.env` | `PANDORA_API_KEY=pk_...`（已在 .gitignore） |
| `cache/` | 原始貼文與算好的指標 |
| `out/` | 產出的 pptx |

## 使用

```bash
cd "提案 template/pandora"
python3 cli.py check                 # 驗 key、看配額與權限（不耗配額）
python3 cli.py fetch                 # 呼叫 API（每組關鍵字耗 1 次查詢配額）
python3 cli.py build                 # 用 cache 回填範本產出 pptx（不耗配額）
python3 cli.py run                   # fetch + build
```

新案子：複製 `config.example.json` 成 `config.json`，改 `groups`（最多 2 組，對應範本左右兩張卡）、
日期與 `kpi`，然後 `python3 cli.py run`。`startDate` / `endDate` 留空會自動抓「最近 365 天」。

## 自動回填的內容

| 頁 | 內容 |
|---|---|
| p.3 | 兩組的總聲量／貼文數／總按讚／總留言、月度聲量趨勢折線圖、平台分布環圈圖、三行重點條列 |
| p.4 | 情緒五級百分比與長條、情緒圓餅圖、正面比率（含已評分／未評分筆數）、各渠道聲量占比 |
| p.10 | 施策前聲量、施策後目標值與長條長度、＋N％ 大字、右側對照明細、曝光次數試算 |
| 全域 | 資料期間、專案名、＋N％、施策前基準日 |

`【】` 開頭且需要人判斷的欄位（洞察、受眾、切角、時程、貼文樣本）刻意不動，留給你寫。

## 回填是怎麼對上的

範本裡每個要放資料的圖形都有名字（`PD:g1.totalVolume`、`PD:sent.pct3`、`PD:kpi.g2.after`…，共 55 個），
程式是照名字找圖形，不是比對文字。所以**改文案、改字級、搬位置都不會弄壞回填**；
只有刪掉圖形或改掉名字才會失效（失效時該欄會維持範本原樣，不會報錯）。

在 PowerPoint 裡看圖形名稱：`常用 → 選取 → 選取範圍窗格`。

## 資料處理上的取捨（依 API 文件第 4 節建議）

- `sentiment` 為 `null` 是「未評分」，**排除**在情緒統計外，不當成 0 一起平均；未評分筆數會印在正面比率那行。
- `isConsist === false` 是「字面命中但語意不是在講該品牌」，預設過濾掉（`onlyBrandRelevant`）。
- 地區用請求端 `geoCountries: ["tw"]` 過濾；`geoCountry` 為 `null` 的舊資料伺服器端視同 `tw`。
- 平台占比用**聲量**口徑（不是篇數），與簡報上「聲量分布」的說法一致。
- 情緒五級切點預設 `[0.6, 0.2, -0.2, -0.6]`，可在 config 的 `sentimentBands` 調。

## 配額與注意事項

- 查詢是**先扣後查**，失敗、逾時、自己中斷都照扣，所以程式**刻意不做自動重試**；失敗會直接印錯誤讓你決定。
- 每組關鍵字 = 1 次配額。目前這把 key 是 1000 次／天，台北時間午夜重置。
- 單次查詢實測約 12–15 秒，client timeout 設 150 秒。
- `searchExpression` 含運算子時，精確過濾發生在 `limit` 之後，回傳筆數可能少於 `limit`。
  若 `fetch` 顯示「回傳筆數已達 limit」，代表可能被截斷，要縮小日期範圍分批查。
- 這把 key 只有 `posts` + `trends` scope，沒有 `scrape`，所以即時爬取端點用不了（本工具也沒用到）。

## 換 key

改 `.env` 裡的 `PANDORA_API_KEY`，或設同名環境變數（環境變數優先）。key 不會被寫進任何產出檔。
