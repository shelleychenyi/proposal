# -*- coding: utf-8 -*-
"""Pandora BQ Public Search API client.

重要：POST /api/public/query 是「先扣後查」，失敗也不退配額，因此這裡刻意不做自動重試。
GET /api/public/schema 不計配額，可以隨意呼叫。
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://pandora.thepocket.company"
DEFAULT_TIMEOUT = 120          # 文件 3.4：單次查詢約 13–15 秒，client timeout 建議 ≥60 秒


class PandoraError(RuntimeError):
    def __init__(self, code, message, status=None):
        super().__init__(f"{code}: {message}")
        self.code, self.message, self.status = code, message, status


def load_api_key(env_file: Path | None = None) -> str:
    """環境變數優先；否則讀同目錄的 .env。key 永遠不寫進程式碼或輸出檔。"""
    key = os.environ.get("PANDORA_API_KEY")
    if key:
        return key.strip()
    env_file = env_file or Path(__file__).with_name(".env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("PANDORA_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise PandoraError(
        "missing_key",
        "找不到 API key。請設定環境變數 PANDORA_API_KEY，或在 pandora/.env 寫入 PANDORA_API_KEY=pk_...",
    )


class PandoraClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL,
                 timeout: int = DEFAULT_TIMEOUT):
        self.api_key = api_key or load_api_key()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last_quota: dict | None = None

    # ---------- low level ----------
    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("x-api-key", self.api_key)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                self._note_quota(resp.headers)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            try:
                err = json.loads(raw)
            except ValueError:
                err = {"code": f"http_{exc.code}", "error": raw[:300]}
            self._note_quota(exc.headers)
            raise PandoraError(err.get("code", f"http_{exc.code}"),
                               err.get("error", ""), exc.code) from None
        except urllib.error.URLError as exc:
            raise PandoraError("network_error", str(exc.reason)) from None
        except TimeoutError:
            raise PandoraError(
                "timeout",
                f"超過 {self.timeout} 秒未回應。注意：查詢是先扣配額，這次仍已計入。",
            ) from None
        if not body.get("success"):
            raise PandoraError(body.get("code", "unknown"), body.get("error", ""))
        return body

    def _note_quota(self, headers) -> None:
        limit, remaining = headers.get("X-RateLimit-Limit"), headers.get("X-RateLimit-Remaining")
        if limit is not None:
            self.last_quota = {"limit": int(limit), "remaining": int(remaining or 0)}

    # ---------- endpoints ----------
    def schema(self) -> dict:
        """不計入配額。"""
        return self._request("GET", "/api/public/schema")

    def query(self, search_expression: str, start_date: str, end_date: str, *,
              sources: list[str] | None = None, geo_countries: list[str] | None = None,
              limit: int = 50000) -> dict:
        """計入配額 1 次（無論成功與否）。"""
        payload = {
            "table": "precise",
            "searchExpression": search_expression,
            "startDate": start_date,
            "endDate": end_date,
            "limit": limit,
            "format": "json",
        }
        if sources:
            payload["sources"] = sources
        if geo_countries:
            payload["geoCountries"] = geo_countries
        started = time.time()
        body = self._request("POST", "/api/public/query", payload)
        body.setdefault("meta", {})["elapsedSec"] = round(time.time() - started, 1)
        return body
