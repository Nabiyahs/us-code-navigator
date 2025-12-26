# US Code Navigator - 데이터 스키마 문서

## 개요

이 문서는 US Code Navigator 애플리케이션에서 사용하는 모든 JSON 데이터 파일의 구조와 관계를 설명합니다.

---

## 엔티티 관계 다이어그램 (ERD)

```
┌─────────────────┐       ┌─────────────────────┐       ┌─────────────────────┐
│   Discipline    │       │      CodeType       │       │    Jurisdiction     │
├─────────────────┤       ├─────────────────────┤       ├─────────────────────┤
│ DisciplineID(PK)│       │ CodeTypeID(PK)      │       │ JurisdictionID(PK)  │
│ DisciplineNameEN│       │ CodeTypeName        │       │ JurisdictionName    │
│ DisciplineNameKR│       │ Description         │       │ StateName           │
└────────┬────────┘       └──────────┬──────────┘       │ StateCode           │
         │                           │                  └─────────────────────┘
         │                           │
         │ N:1                       │ 1:N
         ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐
│ ModelCodeDiscipline │    │     ModelCode       │
├─────────────────────┤    ├─────────────────────┤
│ ModelCodeID(FK)─────┼────│ ModelCodeID(PK)     │
│ DisciplineID(FK)    │    │ CodeTypeID(FK)──────┼──────┘
│ ModelCodeName       │    │ ModelCodeName       │
└─────────────────────┘    │ DescriptionEN       │
         ▲                 │ DescriptionKR       │
         │                 └──────────┬──────────┘
         │                            │
         │                            │ 1:N
         │                            ▼
         │                 ┌─────────────────────┐
         │                 │  ModelCodeVersion   │
         │                 ├─────────────────────┤
         └─────────────────│ ModelCodeVersionID  │
                           │      (PK)           │
                           │ ModelCodeID(FK)─────┼──────┘
                           │ Year                │
                           │ Description         │
                           └──────────┬──────────┘
                                      │
                                      │ 1:N
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
         ┌─────────────────────┐             ┌─────────────────────┐
         │    CodeChapter      │             │   CodeAttachment    │
         ├─────────────────────┤             ├─────────────────────┤
         │ ChapterID(PK)       │             │ AttachmentID(PK)    │
         │ ModelCodeVersionID  │             │ ModelCodeVersionID  │
         │      (FK)           │             │      (FK)           │
         │ Chapter             │             │ Type (T/F)          │
         │ TitleEN             │             │ Number              │
         │ TitleKR             │             │ FileName            │
         │ ChapterComment      │             │ Chapter             │
         └──────────┬──────────┘             │ Section             │
                    │                        │ Subsection          │
                    │ 1:N                    │ AttachTitleEN       │
                    ▼                        │ AttachTitleKR       │
         ┌─────────────────────┐             │ AttachContentEN     │
         │    CodeContent      │             │ AttachContentKR     │
         ├─────────────────────┤             │ AttachComment       │
         │ (Implicit PK)       │             └─────────────────────┘
         │ ChapterID(FK)───────┼─────┘                ▲
         │ Subsection          │                      │
         │ OrderKey            │     AttachmentID     │
         │ Index               │  (세미콜론 구분 참조)  │
         │ SubIndex            │──────────────────────┘
         │ TitleEN             │
         │ TitleKR             │
         │ ContentEN           │
         │ ContentKR           │
         │ Comment             │
         │ Reference           │
         │ AttachmentID        │
         │ IndexTags[]         │
         │ SubindexPaths[]     │
         └─────────────────────┘
```

---

## 데이터 파일 상세

### 1. Discipline.json
**목적**: 법규의 분야/공종 분류

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `DisciplineID` | string (PK) | 분야 고유 ID | "D001" |
| `DisciplineNameEN` | string | 영문 분야명 | "Arch/Struct" |
| `DisciplineNameKR` | string | 한글 분야명 | "건축구조" |

**분야 목록**:
| ID | 영문명 | 한글명 |
|----|--------|--------|
| D001 | Arch/Struct | 건축구조 |
| D002 | MEP | MEP |
| D003 | Elec | 전기 |
| D004 | Fire (Elec) | 소방전기 |
| D005 | Fire (MEP) | 소방기계 |
| D006 | EHS | EHS |

---

### 2. CodeType.json
**목적**: 법규 유형 분류

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `CodeTypeID` | string (PK) | 법규 유형 ID | "CT001" |
| `CodeTypeName` | string | 유형명 | "Model Code" |
| `Description` | string | 설명 | "IBC, IFC, NEC 등" |

**유형 목록**:
| ID | 유형명 | 설명 |
|----|--------|------|
| CT001 | Model Code | IBC, IFC, NEC 등 |
| CT002 | Jurisdiction | 각 주별 법규 |
| CT003 | Other Jurisdictions | 기타 법규 |

---

### 3. Jurisdiction.json
**목적**: 미국 주(State) 정보

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `JurisdictionID` | string (PK) | 관할권 ID | "J001" |
| `JurisdictionName` | string | 관할권명 | "Georgia" |
| `StateName` | string | 주 이름 | "Georgia" |
| `StateCode` | string | 주 약칭 | "GA" |

---

### 4. ModelCode.json
**목적**: 모델 코드(법규) 기본 정보

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `ModelCodeID` | string (PK) | 법규 고유 ID | "MC001" |
| `CodeTypeID` | string (FK) | 법규 유형 참조 | "CT001" |
| `ModelCodeName` | string | 법규 약칭 | "IBC" |
| `DescriptionEN` | string | 영문 설명 | "International Building Code" |
| `DescriptionKR` | string | 한글 설명 | "국제건축법규" |

**주요 법규 목록**:
| ID | 약칭 | 설명 |
|----|------|------|
| MC001 | IBC | International Building Code |
| MC007 | NFPA 13 | 스프링클러 설비 설치 기준 |
| MC008 | NFPA 14 | 연결송수관 및 호스시스템 설치 기준 |
| MC010 | NFPA 72 | 화재경보 및 신호설비 법규 |
| MC024 | NFPA 101 | Life Safety Code |

---

### 5. ModelCodeVersion.json
**목적**: 법규의 연도별 버전 정보

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `ModelCodeVersionID` | string (PK) | 버전 고유 ID | "MCV002" |
| `ModelCodeID` | string (FK) | 법규 참조 | "MC001" |
| `Year` | number | 발행 연도 | 2024 |
| `Description` | string | 버전 설명 | "IBC 2024 Edition" |

**관계**: ModelCode(1) → ModelCodeVersion(N)

---

### 6. ModelCodeDiscipline.json
**목적**: 법규와 분야 간의 다대다(N:N) 관계 매핑

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `ModelCodeID` | string (FK) | 법규 참조 | "MC001" |
| `DisciplineID` | string (FK) | 분야 참조 | "D001" |
| `ModelCodeName` | string | 법규명 (중복) | "IBC" |

**관계**: ModelCode(N) ↔ Discipline(N)

---

### 7. CodeChapter.json
**목적**: 법규의 챕터(장) 정보

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `ChapterID` | string (PK) | 챕터 고유 ID | "CH001" |
| `ModelCodeVersionID` | string (FK) | 법규 버전 참조 | "MCV002" |
| `Chapter` | number | 챕터 번호 | 3 |
| `TitleEN` | string | 영문 제목 | "Occupancy Classification" |
| `TitleKR` | string | 한글 제목 | "용도 분류" |
| `ChapterComment` | string | 챕터 설명/해설 | "Chapter 3은..." |

**관계**: ModelCodeVersion(1) → CodeChapter(N)

---

### 8. CodeContent.json
**목적**: 법규의 실제 조문 내용

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `ChapterID` | string (FK) | 챕터 참조 | "CH003" |
| `Subsection` | string/number/null | 세부 조항 번호 | "1.1" 또는 1.1 |
| `OrderKey` | string | 정렬 키 | "0003.0307.001" |
| `Index` | string | 인덱스 (세미콜론 구분) | "CD;정의;구역" |
| `SubIndex` | string/null | 하위 인덱스 | null |
| `TitleEN` | string | 영문 제목 | "Area" |
| `TitleKR` | string | 한글 제목 | "면적, 구획" |
| `ContentEN` | string | 영문 조문 내용 | "The area included..." |
| `ContentKR` | string | 한글 조문 내용 | "외벽 또는..." |
| `Comment` | string/null | 해설/주석 | "ASTM D92..." |
| `Reference` | string/null | 참조 문서 | "ASTM D92" |
| `AttachmentID` | string/null | 첨부파일 ID (세미콜론 구분) | "D001;D002" |
| `IndexTags` | array | 인덱스 태그 배열 | ["CD", "정의"] |
| `SubindexPaths` | array | 하위 인덱스 경로 | [] |

**OrderKey 구조**:
- 형식: `CCCC.SSSS.III` (챕터.섹션.아이템)
- 예시: `0003.0307.001` → Chapter 3, Section 307, Item 1
- 특수 접두사: `[F]`, `[BE]`, `[BS]` 등 (소방, 건축기본, 건축구조 관련)

**관계**: CodeChapter(1) → CodeContent(N)

---

### 9. CodeAttachment.json
**목적**: 법규 관련 첨부파일(그림, 표) 정보

| 필드명 | 타입 | 설명 | 예시 |
|--------|------|------|------|
| `AttachmentID` | string (PK) | 첨부파일 고유 ID | "D001" |
| `ModelCodeVersionID` | string (FK) | 법규 버전 참조 | "MCV002" |
| `Type` | string | 유형 (T=Table, F=Figure) | "T" |
| `Number` | string/null | 번호 | "(1)" |
| `FileName` | string | 파일명 (확장자 제외) | "IBC_3_307.1.1_T(1)" |
| `Chapter` | number | 챕터 번호 | 3 |
| `Section` | number/string | 섹션 번호 | 307 또는 "[F]414" |
| `Subsection` | number/null | 하위 섹션 번호 | 1.1 |
| `AttachTitleEN` | string/null | 영문 제목 | "MAXIMUM ALLOWABLE..." |
| `AttachTitleKR` | string/null | 한글 제목 | "제어 구역에서..." |
| `AttachContentEN` | string/null | 영문 설명 | "For SI: 1 cubic..." |
| `AttachContentKR` | string/null | 한글 설명 | "NL = Not Limited..." |
| `AttachComment` | string/null | 주석/해설 | "[관련 조항]..." |

**파일명 규칙**: `{법규}_{챕터}_{섹션}_{유형}({번호})`
- 예: `IBC_3_307.1.1_T(1)` → IBC Chapter 3, Section 307.1.1, Table (1)

**이미지 파일 위치**: `image/` 폴더 (확장자: .jpg, .JPG, .jpeg, .png)

---

## 데이터 흐름

```
사용자 선택 흐름:

1. [Discipline 선택]
        ↓
2. [ModelCodeDiscipline → ModelCode 필터링]
        ↓
3. [ModelCode → ModelCodeVersion 선택]
        ↓
4. [CodeChapter 목록 표시]
        ↓
5. [CodeContent 조문 표시]
        ↓
6. [CodeAttachment 이미지/표 표시]
```

---

## 주요 조인(Join) 관계

### 법규 목록 조회
```javascript
// Discipline → ModelCodeDiscipline → ModelCode → ModelCodeVersion
const codes = ModelCodeDiscipline
    .filter(mcd => mcd.DisciplineID === selectedDiscipline)
    .map(mcd => ModelCode.find(mc => mc.ModelCodeID === mcd.ModelCodeID))
    .map(mc => ({
        ...mc,
        versions: ModelCodeVersion.filter(v => v.ModelCodeID === mc.ModelCodeID)
    }));
```

### 조문 내용 조회
```javascript
// ModelCodeVersion → CodeChapter → CodeContent
const chapters = CodeChapter.filter(ch => ch.ModelCodeVersionID === versionId);
const contents = CodeContent.filter(c => c.ChapterID === chapterId);
```

### 첨부파일 조회
```javascript
// CodeContent.AttachmentID → CodeAttachment
const attachmentIds = content.AttachmentID.split(';');
const attachments = CodeAttachment.filter(a => attachmentIds.includes(a.AttachmentID));
```

---

## 데이터 통계

| 파일명 | 레코드 수 | 설명 |
|--------|-----------|------|
| Discipline.json | 6 | 분야 분류 |
| CodeType.json | 3 | 법규 유형 |
| Jurisdiction.json | 3 | 관할 지역 |
| ModelCode.json | 24 | 법규 종류 |
| ModelCodeVersion.json | 20 | 법규 버전 |
| ModelCodeDiscipline.json | 24 | 법규-분야 매핑 |
| CodeChapter.json | ~50+ | 챕터 정보 |
| CodeContent.json | ~1000+ | 조문 내용 |
| CodeAttachment.json | ~200+ | 첨부파일 |

---

## 버전 정보

- 문서 생성일: 2025-12-26
- 데이터 버전: IBC 2024, NFPA 2024-2025
