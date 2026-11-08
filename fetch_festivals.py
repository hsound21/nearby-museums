"""공공데이터포털 '전국문화축제표준데이터' API -> festivals.json (앱용 경량 파일)

인증키는 코드에 넣지 않고 환경변수로 받는다.
  Windows PowerShell:  $env:DATA_GO_KR_KEY="인증키"; python fetch_festivals.py
  bash:                DATA_GO_KR_KEY=인증키 python fetch_festivals.py
좌표가 없는 축제는 지도에 표시할 수 없어 제외하고, 종료된 지 오래된 축제(기본 1년 초과)도 제외한다.
"""
import json, os, sys, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

KEY = os.environ.get("DATA_GO_KR_KEY")
if not KEY:
    sys.exit("환경변수 DATA_GO_KR_KEY 가 필요합니다.")

BASE = "https://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api"
items, page = [], 1
while True:
    q = urllib.parse.urlencode({"serviceKey": KEY, "pageNo": page, "numOfRows": 1000, "type": "json"}, safe="")
    with urllib.request.urlopen(f"{BASE}?{q}", timeout=60) as r:
        d = json.load(r)
    if "response" in d:
        d = d["response"]
    body = d["body"]
    got = body["items"]
    got = got["item"] if isinstance(got, dict) else got
    items += got or []
    if page * 1000 >= int(body["totalCount"]):
        break
    page += 1

cutoff = (date.today() - timedelta(days=365)).isoformat()
out, skip = [], {"nocoord": 0, "old": 0, "nodate": 0}
for x in items:
    try:
        lat, lon = float(x["latitude"]), float(x["longitude"])
    except (ValueError, TypeError, KeyError):
        skip["nocoord"] += 1
        continue
    if not (33 < lat < 39 and 124 < lon < 132):
        skip["nocoord"] += 1
        continue
    s = (x.get("fstvlStartDate") or "").strip()
    e = (x.get("fstvlEndDate") or "").strip() or s
    if not s:
        skip["nodate"] += 1
        continue
    if e < cutoff:
        skip["old"] += 1
        continue
    out.append([
        x["fstvlNm"].strip(), round(lat, 6), round(lon, 6), s, e,
        (x.get("opar") or "").strip(),
        (x.get("rdnmadr") or x.get("lnmadr") or "").strip(),
        (x.get("phoneNumber") or "").strip(),
        (x.get("homepageUrl") or "").strip(),
        (x.get("fstvlCo") or "").strip()[:200],
        (x.get("mnnstNm") or x.get("auspcInsttNm") or "").strip(),
    ])

out.sort(key=lambda r: r[3])
Path(__file__).with_name("festivals.json").write_text(
    json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"전체 {len(items)}건 중 {len(out)}건 저장, 제외: {skip}")
