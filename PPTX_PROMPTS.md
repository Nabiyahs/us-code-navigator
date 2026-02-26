# US CODE NAVIGATOR — PPTX 생성 프롬프트

> 아래 3개 프롬프트를 각각 별도로 사용하여 PPTX를 생성하세요.
> python-pptx를 사용하는 AI 도구(ChatGPT, Claude 등)에서 실행할 수 있습니다.

---

## 프롬프트 1: 기능 설명서 (GUIDE.pptx)

```
python-pptx로 아래 내용을 기반으로 PPTX 프레젠테이션을 생성해줘.

■ 파일명: GUIDE.pptx
■ 대상 독자: 설계 엔지니어 (비개발자)
■ 톤: 친절하고 직관적인 사용 안내서

■ 디자인 시스템 (모든 슬라이드 공통):
- 슬라이드 크기: 와이드스크린 (16:9)
- 배경색: 흰색 (#FFFFFF)
- 제목 텍스트: #24305E (짙은 남색), 볼드, 28pt
- 본문 텍스트: #333333, 16pt
- 강조 텍스트: #F76C6C (산호색), 볼드
- 하이라이트 배경: #F8E9A1 (연한 노랑)
- 액센트 라인/도형: #A8D0E6 (하늘색)
- 표 헤더 배경: #24305E, 텍스트 흰색
- 표 짝수행 배경: #EBF4FA (연한 하늘)
- 표 홀수행 배경: #FFFFFF
- 표 테두리: #A8D0E6
- 섹션 구분선: #374785 (밝은 남색), 2pt
- 폰트: 한글 "맑은 고딕", 영문 "Inter" 또는 "Calibri"
- 슬라이드 하단 우측에 페이지 번호 표시 (#374785, 10pt)
- 슬라이드 하단 좌측에 "US CODE NAVIGATOR" 워터마크 (#A8D0E6, 10pt)

■ 슬라이드 구성:

[슬라이드 1] 표지
- 중앙 상단: "US CODE NAVIGATOR" (40pt, #24305E, 볼드)
- 중앙: "기능 설명서" (32pt, #374785)
- 하단: "사용자를 위한 기능 안내 및 사용법" (16pt, #666666)
- 배경: 좌측에 #24305E 세로 띠 (너비 60px), 띠 위에 #A8D0E6 가는 선

[슬라이드 2] 목차
- 제목: "목차"
- 5개 항목을 번호와 함께 세로 나열:
  1. 서비스 개요
  2. 수록 코드 라이브러리
  3. 화면 구성
  4. 주요 기능 (5개)
  5. 주요 사용 시나리오 (4개)
- 각 항목 왼쪽에 #A8D0E6 원형 번호 아이콘

[슬라이드 3] 서비스 개요
- 제목: "1. 서비스 개요"
- 핵심 설명:
  "US CODE NAVIGATOR는 미국 건축 및 소방 관련 법규(Code)를 영한 이중언어로 열람, 검색, 비교할 수 있는 웹 기반 도구입니다."
- 3개 핵심 포인트를 아이콘 스타일 박스로:
  • 별도 설치 불필요 — 브라우저에서 index.html을 열면 즉시 사용 가능
  • 인터넷 연결 없이 로컬에서도 동작 (정적 파일 기반)
  • 반도체, 배터리, 데이터센터 등 하이테크 시설 설계 시 법규 참조용
- 하단에 DISCLAIMER 박스 (#F8E9A1 배경, #333333 텍스트, 12pt):
  "본 서비스에 수록된 코드 내용은 관련 법규 및 기준의 일부 발췌본이며, 이해를 돕기 위해 해설, 주석 및 참고 이미지를 포함하고 있습니다. 정확하고 전체적인 내용을 확인하기 위해서는 반드시 구매한 코드 원본을 열람 및 참고해주시기 바랍니다. — 하이테크 1본부"

[슬라이드 4] 수록 코드 라이브러리
- 제목: "2. 수록 코드 라이브러리 (15권)"
- 표: 공종 | 코드명 | 정식 명칭 | 에디션
  (아래 데이터를 표로)
  건축구조 | IBC | International Building Code (국제건축법규) | 2024
  소방기계 | NFPA 1 | Fire Code (화재 법규) | 2024
  소방기계 | NFPA 12 | Carbon Dioxide Extinguishing Systems (이산화탄소 소화설비) | 2025
  소방기계 | NFPA 13 | Sprinkler Systems (스프링클러 설비 설치기준) | 2025
  소방기계 | NFPA 14 | Standpipe & Hose Systems (연결송수관 및 호스시스템) | 2024
  소방기계 | NFPA 15 | Water Spray Fixed Systems (물분무 고정설비) | 2022
  소방기계 | NFPA 16 | Foam-Water Sprinkler Systems (포-물분무 시스템) | 2010
  소방기계 | NFPA 20 | Fire Pumps (소방용 고정펌프) | 2025
  소방기계 | NFPA 24 | Private Fire Service Mains (전용 소방배관) | 2025
  소방기계 | NFPA 92 | Smoke Control Systems (제연설비) | 2024
  소방기계 | NFPA 96 | Commercial Cooking (상업용 주방 환기 및 화재방호) | 2024
  소방기계 | NFPA 214 | Water-Cooling Towers (수냉식 냉각탑) | 2021
  소방기계 | NFPA 318 | Semiconductor Fabrication Facilities (반도체 제조시설 방호) | 2025
  소방전기 | NFPA 72 | Fire Alarm & Signaling Code (화재경보 및 신호설비) | 2025
- 하단에 "준비 중: NFPA 101, ADA, IMC, IPC, ASHRAE" (#374785, 이탤릭)

[슬라이드 5] 화면 구성
- 제목: "3. 화면 구성"
- 화면 레이아웃을 도형으로 시각화:
  ┌──────────────────────────────────────────────────────┐
  │  [상단 검색 바 - Quick Search]                          │
  ├──────────┬───────────────────────────────────────────┤
  │ 사이드바  │          메인 콘텐츠 영역                     │
  │          │    (홈 / 라이브러리 / 고급검색 / 코드비교)      │
  └──────────┴───────────────────────────────────────────┘
- 사이드바 영역: #24305E 배경
- 상단 바: #374785 배경
- 메인 콘텐츠: 흰색 배경
- 각 영역에 짧은 설명 캘아웃(callout) 추가

[슬라이드 6] 주요 기능 — 홈 화면 (책장 UI)
- 제목: "4-1. 홈 화면 (책장 UI)"
- 왼쪽 영역: 기능 설명 불릿 포인트
  • 수록 코드들이 실물 책 형태로 책장에 진열
  • 필터링: 전체/공종별/기관별/연도별
  • 책 클릭 → 팝업으로 개요, 적용 범위, 주요 참조사항 표시
  • "바로가기" 버튼 → 라이브러리 화면으로 직접 이동
  • 회색 표시 = 준비중 (데이터 미수록)

[슬라이드 7] 주요 기능 — 라이브러리
- 제목: "4-2. 라이브러리 (코드 본문 열람)"
- 왼쪽: Chapter 사이드바 설명
- 오른쪽: 본문 영역 설명
  • 영문 원문: 파란색 좌측 테두리 (#A8D0E6 색상 박스로 시각화)
  • 한국어 번역: 노란색 좌측 테두리 (#F8E9A1 색상 박스로 시각화)
  • NOTE: 빨간색 좌측 테두리 (#F76C6C 색상 박스로 시각화)
- 추가 기능: Index Tags, Figures & Tables, 섹션 복사/공유

[슬라이드 8] 주요 기능 — 검색 (Quick Search + 고급 검색)
- 제목: "4-3 / 4-4. 검색 기능"
- 2열 레이아웃:
  [좌측] Quick Search (상단 검색 바)
    • 모든 코드에서 영문/한글 검색
    • 정확 일치 / 부분 일치 구분 표시
    • 키워드 노란색 하이라이트
    • 결과 클릭 → 해당 코드 본문으로 이동
    • 첨부파일 내 텍스트도 검색 대상
  [우측] 고급 검색 (Advanced Search)
    • 키워드 + 공종별 필터 결합
    • 3개 카테고리: 건축구조, 소방기계, 소방전기
    • 개별 코드 선택/해제, Select All, Clear
    • 아코디언 형태 결과 (접기/펼치기)

[슬라이드 9] 주요 기능 — 코드 비교
- 제목: "4-5. 코드 비교 (Code Compare)"
- 핵심 설명: "같은 코드의 다른 에디션 또는 서로 다른 코드 간 Section 단위 비교"
- Code A / Code B 선택 방법 설명
- 비교 결과 시각적 구분을 실제 색상으로:
  • 수정됨: #F8E9A1 (노란색) 배경 박스
  • 삭제됨: #F76C6C (빨간색) 배경 + 취소선 텍스트
  • 추가됨: #90EE90 (초록색) 배경 박스
- 비교 요약 카운트: 추가(+), 수정(~), 삭제(-)

[슬라이드 10] 주요 사용 시나리오
- 제목: "5. 주요 사용 시나리오"
- 4개 시나리오를 2×2 그리드로 배치, 각각 #A8D0E6 테두리 라운드 박스:
  [A] 특정 코드 조항 확인
    홈 책장 → 책 클릭 → 바로가기 → Chapter 선택 → 본문 확인
  [B] 키워드로 관련 조항 찾기
    상단 검색 바 → 키워드 입력 → 결과 클릭 → 본문 이동
  [C] 에디션 간 변경사항 확인
    코드 비교 → Code A/B 선택 → Section 입력 → 비교 실행
  [D] 특정 공종의 코드만 모아보기
    홈 → 공종별 필터 → 해당 코드만 표시

[슬라이드 11] 마지막 — 감사 / 문의
- 중앙: "감사합니다" (36pt, #24305E)
- 하단: "문의: 하이테크 1본부" (#374785, 16pt)
```

---

## 프롬프트 2: 관리 가이드 (ADMIN_GUIDE.pptx)

```
python-pptx로 아래 내용을 기반으로 PPTX 프레젠테이션을 생성해줘.

■ 파일명: ADMIN_GUIDE.pptx
■ 대상 독자: 시스템 관리자, 데이터 담당자, 개발자
■ 톤: 기술적이고 정확한 관리/운영 문서

■ 디자인 시스템 (모든 슬라이드 공통):
- 슬라이드 크기: 와이드스크린 (16:9)
- 배경색: 흰색 (#FFFFFF)
- 제목 텍스트: #24305E (짙은 남색), 볼드, 28pt
- 본문 텍스트: #333333, 16pt
- 강조 텍스트: #F76C6C (산호색), 볼드
- 하이라이트 배경: #F8E9A1 (연한 노랑)
- 액센트 라인/도형: #A8D0E6 (하늘색)
- 표 헤더 배경: #24305E, 텍스트 흰색
- 표 짝수행 배경: #EBF4FA (연한 하늘)
- 표 홀수행 배경: #FFFFFF
- 표 테두리: #A8D0E6
- 코드 블록 배경: #F5F5F5, 텍스트 #333333, 폰트 "Consolas" 또는 "D2Coding", 12pt
- 섹션 구분선: #374785, 2pt
- 폰트: 한글 "맑은 고딕", 영문 "Inter" 또는 "Calibri"
- 슬라이드 하단 우측에 페이지 번호 (#374785, 10pt)
- 슬라이드 하단 좌측에 "US CODE NAVIGATOR — Admin Guide" 워터마크 (#A8D0E6, 10pt)

■ 슬라이드 구성:

[슬라이드 1] 표지
- 중앙 상단: "US CODE NAVIGATOR" (40pt, #24305E, 볼드)
- 중앙: "관리 가이드" (32pt, #374785)
- 하단: "시스템 관리자 및 데이터 담당자를 위한 아키텍처, 데이터 구조, 유지보수 안내" (14pt, #666666)
- 배경: 좌측에 #24305E 세로 띠 (너비 60px), 띠 위에 #F76C6C 가는 선 (GUIDE.pptx와 구분)

[슬라이드 2] 목차
- 제목: "목차"
- 7개 항목:
  1. 시스템 아키텍처
  2. 기술 스택
  3. index.html 내부 구조
  4. 데이터 구조 (ERD)
  5. 데이터 파이프라인 (Excel → JSON)
  6. 유지보수 — 데이터 추가/수정
  7. 유지보수 — UI 커스터마이징
- 각 항목 왼쪽에 #A8D0E6 원형 번호 아이콘

[슬라이드 3] 시스템 아키텍처
- 제목: "1. 시스템 아키텍처 — 서버리스 구조"
- 핵심 포인트 (아이콘 + 텍스트):
  • index.html 1개 파일 (~7,600줄)에 HTML + CSS + JS 모두 포함
  • 데이터: data/ 폴더의 9개 JSON 파일에서 fetch()로 로드
  • 이미지: image/ 폴더의 266개 JPG 파일
  • 백엔드 서버/DB 불필요 → GitHub Pages, 사내 파일서버에서 바로 호스팅

[슬라이드 4] 파일 구조
- 제목: "1-1. 파일 구조"
- 트리 구조를 도형으로 시각화:
  us-code-navigator/
  ├── index.html (단일 HTML 앱, 7,612줄)
  ├── data/ (JSON 9개)
  │   ├── Discipline.json (6건)
  │   ├── CodeType.json (3건)
  │   ├── Jurisdiction.json (3건)
  │   ├── ModelCode.json (24건)
  │   ├── ModelCodeVersion.json (20건)
  │   ├── ModelCodeDiscipline.json (24건)
  │   ├── CodeChapter.json (73건)
  │   ├── CodeContent.json (1,712건)
  │   └── CodeAttachment.json (264건)
  ├── image/ (266개 JPG)
  ├── GUIDE.md
  ├── PRESENTATION_CONTENT.md
  └── DATA_SCHEMA.md
- 각 폴더를 색상 구분: data/ → #A8D0E6, image/ → #F8E9A1, 문서 → #EBF4FA

[슬라이드 5] 기술 스택
- 제목: "2. 기술 스택"
- 표:
  구분 | 기술 | 설명
  프론트엔드 | Vanilla JavaScript | 프레임워크 없이 순수 JS
  스타일링 | Tailwind CSS (CDN) | 유틸리티 기반 CSS + 커스텀
  폰트 | Google Fonts (Inter) | 산세리프 UI 폰트
  데이터 | JSON (9개 파일) | fetch() API로 비동기 로딩
  이미지 | JPG (266개 파일) | Figure/Table 이미지
  데이터 변환 | Python (pandas) | Excel → JSON 자동 변환
  호스팅 | 정적 파일 | 서버 불필요
- 하단에 반응형 브레이크포인트 표:
  1280px+ (XL) | 1536px+ (2XL) | 1920px+ (3XL) | 2560px+ (4XL)

[슬라이드 6] index.html 내부 구조 — 레이아웃
- 제목: "3. index.html 내부 구조"
- HTML 레이아웃을 도형으로 시각화:
  <aside> 사이드바 (#24305E 배경) | <main> 메인 영역
                                  |  <header> 검색바 (#374785 배경)
                                  |  4개 섹션 (한 번에 하나만 active):
                                  |    #homeSection
                                  |    #librarySection
                                  |    #searchSection
                                  |    #compareSection

[슬라이드 7] JavaScript 핵심 로직 — 데이터 로딩
- 제목: "3-1. JS 핵심 로직 — 데이터 로딩"
- 코드 블록 스타일로:
  loadAppData() → fetch('data/*.json') × 9 → appData 저장
               → mapChapterIDsToContent()
               → initAdvancedSearchFilters()

[슬라이드 8] JavaScript 핵심 로직 — 법규 열람 함수 체인
- 제목: "3-2. JS 핵심 로직 — 법규 열람 함수 체인"
- 함수 호출 흐름을 플로차트 도형으로:
  사용자 클릭 → loadCodeFromSidebar(versionId, codeId)
    → showSection('library')
    → loadChapters(versionId, codeId)
      → getChapters(versionId)
      → loadAllChaptersContent()
        → getContents(chapterId)
        → buildContentViewModel()
        → getAttachmentsByIds()
        → HTML 렌더링

[슬라이드 9] JavaScript 핵심 로직 — 이미지 표시
- 제목: "3-3. JS 핵심 로직 — 이미지 표시"
- 이미지 참조 흐름을 화살표 도형으로:
  CodeContent.AttachmentID ("D001;D002")
    → split(';')
    → CodeAttachment 매칭
    → FileName + '.jpg'
    → <img src="image/{encodedFileName}">
    → onerror: .jpg → .JPG → 폴백 아이콘
    → 클릭: openAttachmentModal()

[슬라이드 10] 데이터 구조 — ERD 전체
- 제목: "4. 데이터 구조 — ERD"
- 전체 ERD를 도형(사각형 + 화살표)으로 시각화:
  상단: Discipline(#A8D0E6) — CodeType(#A8D0E6) — Jurisdiction(#A8D0E6)
  중단: ModelCodeDiscipline — ModelCode — ModelCodeVersion
  하단: CodeChapter — CodeContent — CodeAttachment
  관계선: 1:N, N:N 표시
- 마스터 테이블: #A8D0E6 배경
- 관계 테이블: #F8E9A1 배경
- 본문/첨부: #FFFFFF 배경, #24305E 테두리

[슬라이드 11] 데이터 구조 — 파일별 레코드 수
- 제목: "4-1. 데이터 파일 통계"
- 표:
  JSON 파일 | 레코드 수 | 분류 | 설명
  Discipline.json | 6 | 마스터 | 공종 분류
  CodeType.json | 3 | 마스터 | 법규 유형
  Jurisdiction.json | 3 | 마스터 | 관할 지역
  ModelCode.json | 24 | 마스터 | 법규 기본 정보
  ModelCodeVersion.json | 20 | 마스터 | 법규 버전
  ModelCodeDiscipline.json | 24 | 관계 | N:N 매핑
  CodeChapter.json | 73 | 구조 | 챕터 정보
  CodeContent.json | 1,712 | 본문 | 조문 내용
  CodeAttachment.json | 264 | 첨부 | Figure/Table

[슬라이드 12] 데이터 구조 — OrderKey & 이미지 파일명
- 제목: "4-2. OrderKey 구조 & 이미지 파일명 규칙"
- 2열 레이아웃:
  [좌측] OrderKey:
    형식: CCCC.SSSS.III (챕터.섹션.아이템)
    예시: 0003.0307.001 → Chapter 3, Section 307, Item 1
    특수 접두사: [F]=소방, [BE]=건축기본, [BS]=건축구조
  [우측] 이미지 파일명:
    형식: {법규}_{챕터}_{섹션}_{유형}({번호}).jpg
    예시: IBC_3_307.1.1_T(1).jpg
    유형: T=Table, F=Figure

[슬라이드 13] 데이터 파이프라인
- 제목: "5. 데이터 파이프라인 (Excel → JSON)"
- 플로차트 도형:
  [Excel 파일 (.xlsx)] → Python (pandas/openpyxl) → [JSON 파일 (9개)] → index.html fetch() → 화면 렌더링
- 변환 처리 사항 불릿:
  • Excel 시트별 별도 JSON 생성
  • ID 체계 자동 생성 (C001, C002, ...)
  • Index → IndexTags 배열 파싱
  • SubIndex → SubindexPaths 배열 변환
  • 빈 셀 → JSON null

[슬라이드 14] 유지보수 — 새 법규 추가 절차
- 제목: "6. 유지보수 — 데이터 추가/수정"
- 5-Step 흐름을 수평 화살표로:
  Step 1: Excel 원본 업데이트
  Step 2: Python → JSON 변환
  Step 3: 마스터 데이터 업데이트
  Step 4: image/ 폴더에 JPG 추가
  Step 5: index.html 사이드바 업데이트 (선택)
- 하단에 수정 파일 매핑 표:
  추가 대상 | 수정 파일 | 필수 필드
  새 법규 | ModelCode.json | ModelCodeID, CodeTypeID, ...
  새 버전 | ModelCodeVersion.json | ModelCodeVersionID, ...
  새 챕터 | CodeChapter.json | ChapterID, ...
  새 조문 | CodeContent.json | ChapterID, OrderKey, ...
  새 이미지 | CodeAttachment.json | AttachmentID, FileName, ...

[슬라이드 15] 유지보수 — UI 커스터마이징
- 제목: "7. 유지보수 — UI 커스터마이징"
- 컬러 팔레트 시각화 (실제 색상 사각형 + 코드):
  #24305E 사이드바 배경 (짙은 남색)
  #374785 사이드바 호버 (밝은 남색)
  #A8D0E6 액센트/하이라이트 (하늘색)
  #F76C6C 강조/경고 (산호색)
  #F8E9A1 키워드 태그 (연한 노랑)
- CSS 수정 위치: <style> 태그 (1~1650줄)
- 사이드바 법규 목록: <nav> librarySubmenu (1680~1760줄)

[슬라이드 16] 주요 조인 관계 코드
- 제목: "참고: 주요 조인(Join) 관계"
- 3개 코드 블록:
  [법규 목록] Discipline → ModelCodeDiscipline → ModelCode → Version
  [조문 내용] Version → CodeChapter → CodeContent (.sort by OrderKey)
  [첨부파일] Content.AttachmentID.split(';') → CodeAttachment → FileName + '.jpg'

[슬라이드 17] 마지막 — 감사 / 문의
- 중앙: "감사합니다" (36pt, #24305E)
- 하단: "관리 문의: 하이테크 1본부" (#374785, 16pt)
```

---

## 프롬프트 3: 데이터 스키마 (DATA_SCHEMA.pptx)

```
python-pptx로 아래 내용을 기반으로 PPTX 프레젠테이션을 생성해줘.

■ 파일명: DATA_SCHEMA.pptx
■ 대상 독자: 데이터 담당자, 개발자
■ 톤: 정확하고 체계적인 기술 레퍼런스

■ 디자인 시스템 (모든 슬라이드 공통):
- 슬라이드 크기: 와이드스크린 (16:9)
- 배경색: 흰색 (#FFFFFF)
- 제목 텍스트: #24305E (짙은 남색), 볼드, 28pt
- 본문 텍스트: #333333, 16pt
- 강조 텍스트: #F76C6C (산호색), 볼드
- 하이라이트 배경: #F8E9A1 (연한 노랑)
- 액센트 라인/도형: #A8D0E6 (하늘색)
- 표 헤더 배경: #24305E, 텍스트 흰색
- 표 짝수행 배경: #EBF4FA (연한 하늘)
- 표 홀수행 배경: #FFFFFF
- 표 테두리: #A8D0E6
- PK 필드: 볼드 + #F76C6C 색상
- FK 필드: 이탤릭 + #374785 색상
- 코드 블록 배경: #F5F5F5, 폰트 "Consolas" 또는 "D2Coding", 12pt
- 폰트: 한글 "맑은 고딕", 영문 "Inter" 또는 "Calibri"
- 슬라이드 하단 우측에 페이지 번호 (#374785, 10pt)
- 슬라이드 하단 좌측에 "US CODE NAVIGATOR — Data Schema" 워터마크 (#A8D0E6, 10pt)

■ 슬라이드 구성:

[슬라이드 1] 표지
- 중앙 상단: "US CODE NAVIGATOR" (40pt, #24305E, 볼드)
- 중앙: "데이터 스키마" (32pt, #374785)
- 하단: "9개 JSON 데이터 파일의 구조, 필드, 관계 상세 문서" (14pt, #666666)
- 배경: 좌측에 #24305E 세로 띠 (너비 60px), 띠 위에 #A8D0E6 가는 선

[슬라이드 2] 목차
- 제목: "목차"
- 항목:
  1. ERD (전체 엔티티 관계도)
  2~4. 마스터 테이블 — Discipline / CodeType / Jurisdiction
  5~6. 법규 정보 — ModelCode / ModelCodeVersion
  7. 관계 테이블 — ModelCodeDiscipline
  8. 구조 테이블 — CodeChapter
  9. 본문 테이블 — CodeContent (핵심)
  10. 첨부 테이블 — CodeAttachment
  11. 데이터 흐름 & 조인 관계
  12. 데이터 통계

[슬라이드 3] ERD 전체
- 제목: "1. 엔티티 관계 다이어그램 (ERD)"
- 전체 ERD를 도형으로 시각화 (관리 가이드 슬라이드 10과 동일 구조):
  상단 3개: Discipline, CodeType, Jurisdiction (#A8D0E6 배경)
  중단: ModelCodeDiscipline (#F8E9A1), ModelCode, ModelCodeVersion
  하단: CodeChapter, CodeContent, CodeAttachment
  관계선: 실선 화살표, 1:N / N:N 레이블 표시
- PK/FK 필드를 각 박스 내에 나열

[슬라이드 4] Discipline.json
- 제목: "2. Discipline.json — 공종/분야 분류"
- 스키마 표:
  필드명 | 타입 | 설명 | 예시
  DisciplineID | string (PK) | 분야 고유 ID | "D001"
  DisciplineNameEN | string | 영문 분야명 | "Arch/Struct"
  DisciplineNameKR | string | 한글 분야명 | "건축구조"
- 전체 데이터 표:
  ID | 영문명 | 한글명
  D001 | Arch/Struct | 건축구조
  D002 | MEP | MEP
  D003 | Elec | 전기
  D004 | Fire (Elec) | 소방전기
  D005 | Fire (MEP) | 소방기계
  D006 | EHS | EHS

[슬라이드 5] CodeType.json + Jurisdiction.json
- 제목: "3. CodeType.json & Jurisdiction.json"
- 2열 레이아웃:
  [좌측] CodeType (법규 유형):
    CT001 | Model Code | IBC, IFC, NEC 등
    CT002 | Jurisdiction | 각 주별 법규
    CT003 | Other Jurisdictions | 기타 법규
  [우측] Jurisdiction (관할 지역):
    J001 | Georgia | GA
    J002 | Texas | TX
    J003 | Ohio | OH

[슬라이드 6] ModelCode.json
- 제목: "4. ModelCode.json — 법규 기본 정보"
- 스키마 표:
  필드명 | 타입 | 설명 | 예시
  ModelCodeID | string (PK) | 법규 고유 ID | "MC001"
  CodeTypeID | string (FK) | 법규 유형 참조 | "CT001"
  ModelCodeName | string | 법규 약칭 | "IBC"
  DescriptionEN | string | 영문 설명 | "International Building Code"
  DescriptionKR | string | 한글 설명 | "국제건축법규"
- 주요 법규 목록 (MC001~MC024 중 주요 5건)

[슬라이드 7] ModelCodeVersion.json + ModelCodeDiscipline.json
- 제목: "5. ModelCodeVersion & ModelCodeDiscipline"
- 2열 레이아웃:
  [좌측] ModelCodeVersion (버전):
    스키마: ModelCodeVersionID(PK), ModelCodeID(FK), Year, Description
    관계: ModelCode(1) → Version(N)
  [우측] ModelCodeDiscipline (법규↔공종):
    스키마: ModelCodeID(FK), DisciplineID(FK), ModelCodeName
    관계: ModelCode(N) ↔ Discipline(N)

[슬라이드 8] CodeChapter.json
- 제목: "6. CodeChapter.json — 챕터 정보"
- 스키마 표:
  필드명 | 타입 | 설명 | 예시
  ChapterID | string (PK) | 챕터 고유 ID | "CH001"
  ModelCodeVersionID | string (FK) | 법규 버전 참조 | "MCV002"
  Chapter | number | 챕터 번호 | 3
  TitleEN | string | 영문 제목 | "Occupancy Classification"
  TitleKR | string | 한글 제목 | "용도 분류"
  ChapterComment | string | 챕터 해설 | "Chapter 3은..."
- 관계: ModelCodeVersion(1) → CodeChapter(N)

[슬라이드 9] CodeContent.json — 스키마
- 제목: "7. CodeContent.json — 조문 본문 (핵심)"
- 제목 옆에 (#F76C6C 배경 뱃지: "핵심 테이블")
- 스키마 표:
  필드명 | 타입 | 설명 | 예시
  ChapterID | string (FK) | 챕터 참조 | "CH003"
  Subsection | string/number/null | 세부 조항 번호 | "1.1"
  OrderKey | string | 정렬 키 | "0003.0307.001"
  Index | string | 인덱스 (세미콜론 구분) | "CD;정의;구역"
  SubIndex | string/null | 하위 인덱스 | null
  TitleEN | string | 영문 제목 | "Area"
  TitleKR | string | 한글 제목 | "면적, 구획"
  ContentEN | string | 영문 본문 | "The area included..."
  ContentKR | string | 한글 본문 | "외벽 또는..."
  Comment | string/null | 해설/주석 | "ASTM D92..."
  Reference | string/null | 참조 문서 | "ASTM D92"
  AttachmentID | string/null | 첨부파일 ID (;구분) | "D001;D002"
  IndexTags | array | 인덱스 태그 배열 | ["CD","정의"]
  SubindexPaths | array | 하위 인덱스 경로 | []

[슬라이드 10] CodeContent — OrderKey 상세
- 제목: "7-1. OrderKey 구조 (정렬의 핵심)"
- OrderKey 구조를 도형으로 분해:
  CCCC . SSSS . III
   ↓      ↓     ↓
  챕터   섹션   아이템
  (0003) (0307) (001) → Chapter 3, Section 307, Item 1
- 특수 접두사 예시:
  [F] = 소방 → 0009.[F]0903.001
  [BE] = 건축기본
  [BS] = 건축구조
- 정렬 방식: normalizeForSort() → localeCompare()

[슬라이드 11] CodeAttachment.json
- 제목: "8. CodeAttachment.json — 첨부파일 (Figure/Table)"
- 스키마 표:
  필드명 | 타입 | 설명 | 예시
  AttachmentID | string (PK) | 고유 ID | "D001"
  ModelCodeVersionID | string (FK) | 법규 버전 참조 | "MCV002"
  Type | string | 유형 (T/F) | "T"
  Number | string/null | 번호 | "(1)"
  FileName | string | 파일명(확장자 제외) | "IBC_3_307.1.1_T(1)"
  Chapter | number | 챕터 번호 | 3
  Section | number/string | 섹션 번호 | 307
  Subsection | number/null | 하위 섹션 | 1.1
  AttachTitleEN | string/null | 영문 제목 | "MAXIMUM ALLOWABLE..."
  AttachTitleKR | string/null | 한글 제목 | "제어 구역에서..."
  AttachContentEN | string/null | 영문 설명 | "For SI: 1 cubic..."
  AttachContentKR | string/null | 한글 설명 | "NL = Not Limited..."
  AttachComment | string/null | 주석 | "[관련 조항]..."
- 파일명 분해: {법규}_{챕터}_{섹션}_{유형}({번호}).jpg

[슬라이드 12] 데이터 흐름 & 조인 관계
- 제목: "9. 데이터 흐름 & 조인 관계"
- 사용자 선택 흐름을 세로 플로차트로:
  1. Discipline 선택
  2. ModelCodeDiscipline → ModelCode 필터링
  3. ModelCode → ModelCodeVersion 선택
  4. CodeChapter 목록 표시
  5. CodeContent 조문 표시
  6. CodeAttachment 이미지/표 표시
- 하단에 3개 조인 코드 블록 (코드 블록 스타일):
  [법규 목록] filter → map → find
  [조문 내용] filter → sort by OrderKey
  [첨부파일] split(';') → filter → FileName + '.jpg'

[슬라이드 13] 데이터 통계 요약
- 제목: "10. 데이터 통계"
- 표:
  파일명 | 레코드 수 | 분류 | 설명
  (9개 파일 전체)
- 총계: 총 2,129건 레코드, 266개 이미지 파일
- 파이 차트 또는 바 차트: 레코드 분포 (CodeContent 1,712건이 전체의 80%)

[슬라이드 14] 마지막 — 감사 / 문의
- 중앙: "감사합니다" (36pt, #24305E)
- 하단: "데이터 스키마 문의: 하이테크 1본부" (#374785, 16pt)
```

---

## 공통 참고사항

- 세 PPTX 모두 동일한 컬러 팔레트(#24305E, #374785, #A8D0E6, #F76C6C, #F8E9A1)를 사용하되, 표지의 액센트 선 색상으로 문서를 구분합니다:
  - GUIDE.pptx → #A8D0E6 (하늘색)
  - ADMIN_GUIDE.pptx → #F76C6C (산호색)
  - DATA_SCHEMA.pptx → #F8E9A1 (연한 노랑)
- 모든 표의 스타일, 폰트, 색상 코드를 통일하여 시리즈 문서 느낌을 유지합니다.
