#!/usr/bin/env python3
"""Fetch public logistics/OSINT sources into raw_corpus/fetched."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "raw_corpus" / "fetched"
OUT.mkdir(parents=True, exist_ok=True)

URLS = [
    # GAO sealift / mobility
    "https://www.gao.gov/assets/gao-17-503.pdf",
    "https://www.gao.gov/assets/gao-23-106121.pdf",
    "https://www.gao.gov/assets/gao-21-154.pdf",
    "https://www.gao.gov/assets/gao-18-78.pdf",
    "https://www.gao.gov/assets/gao-15-480.pdf",
    "https://www.gao.gov/assets/gao-22-105829.pdf",
    "https://www.gao.gov/assets/gao-19-414.pdf",
    "https://www.gao.gov/assets/gao-17-84.pdf",
    "https://www.gao.gov/assets/gao-13-710.pdf",
    "https://www.gao.gov/assets/gao-24-106583.pdf",
    # FAS CRS mirrors
    "https://sgp.fas.org/crs/natsec/IF10275.pdf",
    "https://sgp.fas.org/crs/weapons/R46810.pdf",
    "https://sgp.fas.org/crs/natsec/R47096.pdf",
    "https://sgp.fas.org/crs/row/R46810.pdf",
    "https://sgp.fas.org/crs/natsec/IF11719.pdf",
    "https://sgp.fas.org/crs/misc/R42740.pdf",
    "https://sgp.fas.org/crs/natsec/RL33153.pdf",
    "https://sgp.fas.org/crs/weapons/RS20557.pdf",
    # DOT / FMCSA / FHWA pages
    "https://www.fmcsa.dot.gov/oversize-overweight-load-permits",
    "https://www.fmcsa.dot.gov/regulations/hazardous-materials",
    "https://ops.fhwa.dot.gov/freight/infrastructure/nat_freight_stats/",
    "https://www.bts.gov/browse-statistical-products-and-data/freight-facts-and-figures/freight-facts-figures",
    "https://dot.ca.gov/programs/traffic-operations/transportation-permits",
    "https://dot.ca.gov/-/media/dot-media/programs/traffic-operations/documents/transportation-permits/permit-policy-a11y.pdf",
    # Ports
    "https://www.portoflosangeles.org/business/tariffs",
    "https://polb.com/business/tariffs/",
    "https://www.portoflosangeles.org/business/supply-chain",
    "https://polb.com/port-info/facts-at-a-glance/",
    # CBP / DDTC public
    "https://www.cbp.gov/trade/basic-import-export",
    "https://www.cbp.gov/trade/basic-import-export/export-documents",
    "https://www.pmddtc.state.gov/ddtc_public",
    "https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M",
    "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-393",
    "https://www.ecfr.gov/current/title-33/chapter-I",
    # MARAD / sealift public pages
    "https://www.maritime.dot.gov/national-defense-reserve-fleet/ndrf/maritime-administration%E2%80%99s-national-defense-reserve-fleet",
    "https://www.maritime.dot.gov/ports/office-ship-operations/ready-reserve-force-rrf",
    "https://www.maritime.dot.gov/about-us",
    # USTRANSCOM public
    "https://www.ustranscom.mil/",
    "https://www.ustranscom.mil/cmd/aboutustc.cfm",
    # Army pubs (may 404; try)
    "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN17424_ATP%204-13%20FINAL%20WEB.pdf",
    "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN31843-ATP_4-16-000-WEB-1.pdf",
    "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/atp4_12.pdf",
    # DTIC / RAND open
    "https://apps.dtic.mil/sti/pdfs/ADA550445.pdf",
    "https://apps.dtic.mil/sti/pdfs/AD1019084.pdf",
    "https://www.rand.org/pubs/research_reports/RRA1678-1.html",
    "https://www.rand.org/pubs/research_reports/RR419.html",
    # CSIS / open analysis pages
    "https://www.csis.org/analysis/first-battle-next-war-wargaming-chinese-invasion-taiwan",
    "https://www.csis.org/analysis/commanding-seas-survey-chinas-military",
    # IMO public
    "https://www.imo.org/en/OurWork/Safety/Pages/Cargoes.aspx",
    "https://www.imo.org/en/OurWork/Safety/Pages/CSS-Code.aspx",
    # Taiwan MOTC / port English pages
    "https://www.motc.gov.tw/en/",
    "https://www.twport.com.tw/en/",
    "https://www.khb.gov.tw/en/",
    # AAR / rail public
    "https://www.aar.org/issue/freight-rail-safety/",
    "https://www.aar.org/wp-content/uploads/2020/08/AAR-Railroads-Move-America-Fact-Sheet.pdf",
    "https://railroads.dot.gov/",
    "https://railroads.dot.gov/rail-network-development/freight-rail-overview",
    # More GAO/govinfo
    "https://www.govinfo.gov/app/details/GOVPUB-TD-PURL-LPS10391",
    "https://www.transportation.gov/mission/administrations/intelligence-security-emergency-response/defense-transportation",
]

UA = {"User-Agent": "AI-Harness-Bootcamp-CorpusBuilder/1.0 (educational courseware)"}
CTX = ssl.create_default_context()


def fetch(url: str) -> dict:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, context=CTX, timeout=40) as resp:
            data = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            final = resp.geturl()
        ext = ".bin"
        lower = url.lower()
        if "pdf" in ctype or lower.endswith(".pdf"):
            ext = ".pdf"
        elif "html" in ctype or "text" in ctype or lower.endswith("/") or lower.endswith(".html"):
            ext = ".html"
        elif "json" in ctype:
            ext = ".json"
        h = hashlib.sha256(url.encode()).hexdigest()[:12]
        name = re.sub(r"[^a-zA-Z0-9]+", "_", url.split("//", 1)[-1])[:80].strip("_")
        path = OUT / f"{name}_{h}{ext}"
        path.write_bytes(data)
        text_path = None
        if ext in {".html", ".txt"}:
            text = data.decode("utf-8", errors="replace")
            text2 = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
            text2 = re.sub(r"(?is)<style.*?>.*?</style>", " ", text2)
            text2 = re.sub(r"(?s)<[^>]+>", " ", text2)
            text2 = re.sub(r"\s+", " ", text2).strip()
            text_path = path.with_suffix(".txt")
            text_path.write_text(text2[:200000], encoding="utf-8")
        return {
            "url": url,
            "ok": True,
            "path": str(path.relative_to(ROOT / "raw_corpus")),
            "bytes": len(data),
            "ctype": ctype,
            "final": final,
            "text": str(text_path.relative_to(ROOT / "raw_corpus")) if text_path else None,
        }
    except Exception as exc:  # noqa: BLE001
        return {"url": url, "ok": False, "error": str(exc)}


def main() -> int:
    # dedupe preserving order
    seen = set()
    urls = []
    for u in URLS:
        if u not in seen:
            seen.add(u)
            urls.append(u)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futs = [pool.submit(fetch, u) for u in urls]
        for fut in concurrent.futures.as_completed(futs):
            row = fut.result()
            results.append(row)
            status = "OK" if row.get("ok") else "FAIL"
            detail = row.get("bytes", row.get("error", ""))
            print(status, row.get("url", "")[:72], detail)
    (OUT / "_fetch_log.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    ok = sum(1 for r in results if r.get("ok"))
    print(f"DONE_FETCH {ok}/{len(results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
