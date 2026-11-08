# 내 주변 박물관·미술관·문화재

내 위치(또는 입력한 주소) 주변의 박물관·미술관·문화재를 네이버 지도에 보여주고, 최적 방문 동선을 짜 주는 웹앱입니다.

## 데이터
- 박물관·미술관: 전국박물관미술관정보표준데이터 (`museums.json`, 원본은 `전국박물관미술관정보표준데이터.json`)
- 문화재: 국가유산청 Open API (키 불필요)
- 축제: 공공데이터포털 전국문화축제표준데이터 (`festivals.json`). 갱신: `DATA_GO_KR_KEY=인증키 python fetch_festivals.py` (인증키는 코드에 넣지 않고 환경변수로 전달)

데이터를 갱신하려면 새 원본 JSON을 넣고 `python convert_standard.py`를 실행합니다.

## 사용
1. [네이버 클라우드 플랫폼](https://console.ncloud.com)에서 Maps(Dynamic Map) Application을 만들고, **웹 서비스 URL에 배포 주소**(예: `https://<계정>.github.io`)를 등록합니다.
2. 앱을 처음 열면 Client ID 입력창이 나옵니다. 입력한 값은 사용자의 브라우저에만 저장되며 저장소에는 포함되지 않습니다.

로컬 실행: `python -m http.server 8000` 후 `http://localhost:8000` (이 주소도 웹 서비스 URL에 등록 필요)
