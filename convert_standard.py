"""전국박물관미술관정보표준데이터.json -> museums.json (앱용 경량 파일)

표준데이터에는 박물관/미술관 구분 필드가 없고 '박물관미술관구분'은 설립 주체(국립/공립/사립/대학)이다.
따라서 시설명으로 미술관 여부를 판정하고, 설립 주체를 체크박스 유형으로 쓴다.
사용: python convert_standard.py
"""
import json, re
from pathlib import Path

here = Path(__file__).parent
d = json.load(open(here / "전국박물관미술관정보표준데이터.json", encoding="utf-8-sig"))
fields = [f["id"] for f in d["fields"]]
ART = re.compile(r"미술|아트|갤러리|화랑|\bart\b|gallery", re.I)

def fee(r):
    v = [r["어른관람료"], r["청소년관람료"], r["어린이관람료"]]
    if all(x in ("0", "", None) for x in v) and not r["관람료기타정보"]:
        return "무료"
    s = f'성인 {int(v[0]):,}원' if (v[0] or "").isdigit() and int(v[0]) else ""
    return s or r["관람료기타정보"][:30]

def hours(r):
    a, b = r["평일관람시작시각"], r["평일관람종료시각"]
    return f"{a}~{b}" if a and b else ""

out, bad = [], 0
for r in d["records"]:
    r = r if isinstance(r, dict) else dict(zip(fields, r))
    try:
        lat, lon = float(r["위도"]), float(r["경도"])
    except (ValueError, TypeError):
        bad += 1; continue
    if not (33 < lat < 39 and 124 < lon < 132):
        bad += 1; continue
    name = r["시설명"].strip()
    info = " · ".join(x for x in [hours(r), ("휴관 " + r["휴관정보"]) if r["휴관정보"] else "", fee(r)] if x)
    out.append([
        name, round(lat, 6), round(lon, 6), "art" if ART.search(name) else "museum",
        (r["소재지도로명주소"] or r["소재지지번주소"]).strip(),
        r["운영기관전화번호"].strip() or r["관리기관전화번호"].strip(),
        r["박물관미술관구분"].strip() or "기타",
        r["운영기관명"].strip(),
        r["운영홈페이지"].strip(),
        info,
    ])
(here / "museums.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(out)}곳 저장 (제외 {bad}), 미술관 {sum(1 for o in out if o[3]=='art')}")
