# -*- coding: utf-8 -*-
"""v.2 pricing workbook: restructure into ①..⑩ sheets matching the deck order."""
import copy
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

BASE = "/Users/shelleychen/Documents/提案/SMBC三井住友"
SRC = BASE + "/實體媒體_報價表.xlsx"
OUT = BASE + "/實體媒體_報價表_v.2.xlsx"

wb = openpyxl.load_workbook(SRC)

# circled billboard location numbers for ④ rows (deck p.22 order = sheet row order)
BILLBOARD_NUMS = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑪", "⑫"]

# (sheet name, [(source sheet, row numbers)], circled)
PLAN = [
    ("① 捷運聯播網", [("捷運 MRT", [9, 10, 11])], "①"),
    ("② 台北車站 站體數位", [("捷運 MRT", [12, 13, 14, 15, 16, 17])], "②"),
    ("③ 市區公車（松山機場線）", [("公車 BUS", [7, 6, 8, 9])], "③"),
    ("④ 戶外看板", [("戶外看板 BILLBOARD", list(range(2, 14)))], "④"),
    ("⑤ 機場捷運（桃捷）", [("捷運 MRT", [2, 3, 4, 5, 6, 7, 8])], "⑤"),
    ("⑥ 機場巴士", [("公車 BUS", [2, 3, 4, 5])], "⑥"),
    ("⑦ 計程車 車內螢幕", [("計程車 TAXI", [2, 3, 4])], "⑦"),
    ("⑧ 桃園機場 出境區", [("機場 AIRPORT", [2, 3, 4, 5, 6, 7, 8])], "⑧"),
    ("⑨ 桃園機場排班計程車椅套＋入境區", [("計程車 TAXI", [5, 6, 7]), ("機場 AIRPORT", list(range(9, 17)))], "⑨"),
    ("⑩ 台灣高鐵（桃園站・台北站）", [("高鐵", list(range(2, 19)))], "⑩"),
]

ref = wb["捷運 MRT"]
HEADERS = ["編號", "分類", "版位", "規格・數量・輪播條件", "CPM", "單價（円・税別）", "最小購買", "含於套餐", "備註"]
col_widths = [7, 16, 34, 53.6, 8, 22, 16, 12, 30]

hdr_style = ref["A1"]._style
GRAY = Font(name="Microsoft JhengHei", size=9, color="FF6B7A90")

for sheet_name, sources, mark in PLAN:
    ws = wb.create_sheet(sheet_name)
    for j, h in enumerate(HEADERS, 1):
        c = ws.cell(row=1, column=j, value=h)
        c._style = copy.copy(hdr_style)
    ws.row_dimensions[1].height = 26
    r_out = 2
    for src_name, rows in sources:
        src = wb[src_name]
        for r in rows:
            # 編號 cell styled like the 分類 cell of that source row
            c0 = ws.cell(row=r_out, column=1, value=mark)
            c0._style = copy.copy(src.cell(row=r, column=1)._style)
            c0.alignment = Alignment(horizontal="center", vertical="center")
            for j in range(1, 9):
                sc = src.cell(row=r, column=j)
                tc = ws.cell(row=r_out, column=j + 1, value=sc.value)
                tc._style = copy.copy(sc._style)
            ws.row_dimensions[r_out].height = 30
            r_out += 1
    # billboard rows: prefix location numbers to match deck p.22 / map pins
    if mark == "④":
        for k in range(len(BILLBOARD_NUMS)):
            cell = ws.cell(row=2 + k, column=3)
            cell.value = BILLBOARD_NUMS[k] + " " + str(cell.value)
    # HSR footer notes
    if mark == "⑩":
        for note in ["※ 高鐵版位之原始報價為新台幣（未稅）；本表依 1 TWD＝4.56 JPY 換算為日圓（税別），並進位至萬位。",
                     "※ 截稿送審台灣高鐵約 15 個工作日；台灣高鐵保有最終上刊與審稿權利。各版位可售狀態以下單前確認為準。"]:
            c = ws.cell(row=r_out + 1, column=1, value=note)
            c.font = GRAY
            ws.merge_cells(start_row=r_out + 1, start_column=1, end_row=r_out + 1, end_column=9)
            r_out += 1
    for j, w in enumerate(col_widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A2"

# 說明 sheet note about numbering
sm = wb["說明"]
sm["A12"] = "版位編號"
sm["B12"] = "① 至 ⑩ 對應提案簡報（0831 中文版）之版位編號與排列順序；④ 戶外看板內之 ①–⑫ 對應簡報據點位置圖"
sm["A12"].font = copy.copy(sm["A11"].font)
sm["B12"].font = copy.copy(sm["B11"].font)

# drop old category sheets
for name in ["計程車 TAXI", "捷運 MRT", "公車 BUS", "機場 AIRPORT", "戶外看板 BILLBOARD", "高鐵"]:
    del wb[name]

# order: 說明 first, then ①..⑩
wb.move_sheet("說明", offset=-wb.sheetnames.index("說明"))
wb.save(OUT)
print("saved", OUT)
print(wb.sheetnames)
