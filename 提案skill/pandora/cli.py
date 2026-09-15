# -*- coding: utf-8 -*-
"""Pandora → 提案範本 串接工具

  python3 cli.py check                     # 驗 key、看配額與權限（不耗配額）
  python3 cli.py fetch  -c config.json     # 呼叫 API，存原始資料與指標（每組關鍵字耗 1 次配額）
  python3 cli.py build  -c config.json     # 用已抓的指標回填範本，產出 pptx（不耗配額）
  python3 cli.py run    -c config.json     # fetch + build
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from metrics import DEFAULT_BANDS, aggregate, filter_posts          # noqa: E402
from pandora_client import PandoraClient, PandoraError              # noqa: E402

CACHE = HERE / "cache"
OUT = HERE / "out"


def load_cfg(path: Path) -> dict:
    cfg = json.loads(path.read_text(encoding="utf-8"))
    if not cfg.get("endDate"):
        cfg["endDate"] = date.today().isoformat()
    if not cfg.get("startDate"):
        end = datetime.fromisoformat(cfg["endDate"]).date()
        cfg["startDate"] = (end - timedelta(days=364)).isoformat()
    span = (datetime.fromisoformat(cfg["endDate"]).date()
            - datetime.fromisoformat(cfg["startDate"]).date()).days
    if span < 0 or span > 366:
        raise SystemExit(f"日期區間不合法（{span} 天）。startDate 到 endDate 最多 366 天。")
    return cfg


# ---------------- commands ----------------
def cmd_check(args) -> int:
    client = PandoraClient()
    s = client.schema()
    print("key 有效。")
    print("  scopes      :", ", ".join(s.get("scopes", [])))
    lim = s.get("limits", {})
    print(f"  每日查詢配額: {lim.get('dailyQuota')} 次／天（Asia/Taipei 午夜重置）")
    print(f"  日期區間上限: {lim.get('maxDateSpanDays')} 天   limit 上限: {lim.get('limitMax')}")
    if "scrape" in s:
        sc = s["scrape"]
        print(f"  爬取配額    : {sc.get('dailyLimit')} 次／天（與查詢配額分開計）")
    else:
        print("  爬取配額    : 未開通 scrape scope（本工具用不到）")
    return 0


def cmd_fetch(args) -> int:
    cfg = load_cfg(Path(args.config))
    client = PandoraClient(timeout=cfg.get("timeoutSec", 120))
    CACHE.mkdir(exist_ok=True)
    groups = cfg["groups"]
    print(f"期間 {cfg['startDate']} → {cfg['endDate']}　共 {len(groups)} 組查詢"
          f"（將耗用 {len(groups)} 次配額）")
    results = []
    for g in groups:
        print(f"  查詢「{g['label']}」… searchExpression={g['searchExpression']!r}", flush=True)
        try:
            body = client.query(
                g["searchExpression"], cfg["startDate"], cfg["endDate"],
                sources=cfg.get("sources"), geo_countries=cfg.get("geoCountries"),
                limit=cfg.get("limit", 50000))
        except PandoraError as exc:
            print(f"    失敗：{exc}", file=sys.stderr)
            if exc.code in ("quota_exceeded", "unauthorized", "forbidden"):
                return 2
            raise
        raw = body.get("posts", [])
        kept = filter_posts(
            raw,
            only_brand_relevant=cfg.get("onlyBrandRelevant", True),
            geo=set(cfg["geoFilter"]) if cfg.get("geoFilter") else None)
        m = aggregate(kept, bands=cfg.get("sentimentBands", DEFAULT_BANDS))
        q = body.get("meta", {}).get("quota", {})
        print(f"    回傳 {len(raw)} 筆 → 過濾後 {len(kept)} 筆｜總聲量 {m['totalVolume']:,}"
              f"｜耗時 {body['meta'].get('elapsedSec')}s｜配額剩餘 {q.get('remaining')}")
        if len(raw) >= cfg.get("limit", 50000):
            print("    ⚠ 回傳筆數已達 limit，可能被截斷；建議縮小日期範圍分批查詢。")
        (CACHE / f"raw_{g['id']}.json").write_text(
            json.dumps({"meta": body.get("meta"), "posts": raw}, ensure_ascii=False), encoding="utf-8")
        results.append({"id": g["id"], "label": g["label"], "metrics": m})
    payload = {"fetchedAt": datetime.now().isoformat(timespec="seconds"),
               "startDate": cfg["startDate"], "endDate": cfg["endDate"], "groups": results}
    (CACHE / "metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    print(f"已寫出 {CACHE/'metrics.json'}")
    return 0


def cmd_build(args) -> int:
    from fill_deck import fill
    cfg = load_cfg(Path(args.config))
    cache_file = CACHE / "metrics.json"
    if not cache_file.exists():
        print("找不到 cache/metrics.json，請先執行：python3 cli.py fetch", file=sys.stderr)
        return 2
    data = json.loads(cache_file.read_text(encoding="utf-8"))
    groups = data["groups"]
    merged = {"sentiment": groups[0]["metrics"]["sentiment"],
              "platforms": groups[0]["metrics"]["platforms"]}
    OUT.mkdir(exist_ok=True)
    made = []
    for lang, tpl in (cfg.get("templates") or {}).items():
        tpl_path = (HERE.parent / tpl).resolve()
        if not tpl_path.exists():
            print(f"找不到範本：{tpl_path}", file=sys.stderr)
            return 2
        uplift = cfg.get("kpi", {}).get("upliftPercent", 30)
        span = f"{data['startDate']}–{data['endDate']}"
        tokens = {"【yyyy/m/d–yyyy/m/d】": span, "【yyyy年m月d日–yyyy年m月d日】": span,
                  "【yyyy/m/d】": data["endDate"], "【30】": f"{uplift:g}"}
        for i, g in enumerate(groups[:2]):
            suffix = "AB"[i]
            tokens[f"【品牌名／關鍵字{suffix}】"] = g["label"]
            tokens[f"【ブランド名／キーワード{suffix}】"] = g["label"]
        tokens.update(cfg.get("tokens") or {})          # config 的設定優先
        c = dict(cfg, tokens=tokens, _merged=merged)
        out = OUT / f"{cfg.get('outputPrefix','提案')}_{lang}.pptx"
        fill(tpl_path, out, groups, c, lang=lang)
        made.append(out)
        print(f"已產出 {out}")
    if not made:
        print("config 沒有設定 templates。", file=sys.stderr)
        return 2
    return 0


def cmd_run(args) -> int:
    return cmd_fetch(args) or cmd_build(args)


def main() -> int:
    ap = argparse.ArgumentParser(description="Pandora → 提案範本 串接工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("check", cmd_check), ("fetch", cmd_fetch),
                     ("build", cmd_build), ("run", cmd_run)):
        p = sub.add_parser(name)
        if name != "check":
            p.add_argument("-c", "--config", default=str(HERE / "config.json"))
        p.set_defaults(func=fn)
    args = ap.parse_args()
    try:
        return args.func(args)
    except PandoraError as exc:
        print(f"錯誤 {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
