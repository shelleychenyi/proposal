# -*- coding: utf-8 -*-
"""把 Pandora 的 posts[] 聚合成簡報要用的指標。

依文件第 4 節的使用建議：
  * sentiment 為 null 代表「未評分」，做情緒統計時必須排除，不可當 0 平均。
  * geoCountry 為 null 是未標記的舊資料，做台灣聲量統計時併入 tw。
  * isConsist=false 是字面命中但語意不相關，預設過濾掉。
"""
from __future__ import annotations

from collections import Counter, defaultdict

# 情緒五級切點（由正到負）；-1.0 ~ 1.0
DEFAULT_BANDS = [0.6, 0.2, -0.2, -0.6]
BAND_KEYS = ["veryPositive", "positive", "neutral", "negative", "veryNegative"]


def band_of(score: float, bands=DEFAULT_BANDS) -> str:
    hi, pos, neg, lo = bands
    if score >= hi:
        return "veryPositive"
    if score >= pos:
        return "positive"
    if score > neg:
        return "neutral"
    if score > lo:
        return "negative"
    return "veryNegative"


def filter_posts(posts, *, only_brand_relevant=True, geo=None, treat_null_geo_as_tw=True):
    out = []
    for p in posts:
        if only_brand_relevant and p.get("isConsist") is False:
            continue
        if geo:
            g = p.get("geoCountry")
            if g is None and treat_null_geo_as_tw:
                g = "tw"
            if g not in geo:
                continue
        out.append(p)
    return out


def aggregate(posts, *, bands=DEFAULT_BANDS) -> dict:
    total_volume = sum(int(p.get("volume") or 0) for p in posts)
    likes = sum(int(p.get("likes") or 0) for p in posts)
    comments = sum(int(p.get("comments") or 0) for p in posts)

    # --- 情緒：排除 null ---
    scored = [p for p in posts if isinstance(p.get("sentiment"), (int, float))]
    band_counts = Counter(band_of(float(p["sentiment"]), bands) for p in scored)
    n_scored = len(scored)
    sentiment = {
        "scoredCount": n_scored,
        "unscoredCount": len(posts) - n_scored,
        "counts": {k: band_counts.get(k, 0) for k in BAND_KEYS},
        "share": {k: (band_counts.get(k, 0) / n_scored if n_scored else 0.0) for k in BAND_KEYS},
        "meanScore": (sum(float(p["sentiment"]) for p in scored) / n_scored) if n_scored else None,
    }
    sentiment["positiveRate"] = sentiment["share"]["veryPositive"] + sentiment["share"]["positive"]

    # --- 平台分布：以聲量與篇數兩種口徑 ---
    by_src_vol, by_src_cnt = defaultdict(int), Counter()
    for p in posts:
        src = (p.get("source") or "unknown").lower()
        by_src_vol[src] += int(p.get("volume") or 0)
        by_src_cnt[src] += 1
    platforms = sorted(
        ({"source": s, "volume": v, "posts": by_src_cnt[s],
          "volumeShare": (v / total_volume if total_volume else 0.0)}
         for s, v in by_src_vol.items()),
        key=lambda d: -d["volume"])

    # --- 月度趨勢 ---
    by_month = defaultdict(lambda: {"volume": 0, "posts": 0})
    for p in posts:
        stamp = (p.get("pageCreatedAt") or "")[:7]          # YYYY-MM
        if len(stamp) == 7:
            by_month[stamp]["volume"] += int(p.get("volume") or 0)
            by_month[stamp]["posts"] += 1
    trend = [{"month": m, **v} for m, v in sorted(by_month.items())]
    peak = max(trend, key=lambda d: d["volume"]) if trend else None

    top = sorted(posts, key=lambda p: -(int(p.get("volume") or 0)))[:10]
    return {
        "totalVolume": total_volume,
        "postCount": len(posts),
        "likes": likes,
        "comments": comments,
        "sentiment": sentiment,
        "platforms": platforms,
        "trend": trend,
        "peakMonth": peak,
        "topPosts": [{k: p.get(k) for k in
                      ("postId", "url", "title", "source", "author",
                       "likes", "comments", "volume", "sentiment", "pageCreatedAt")}
                     for p in top],
    }
