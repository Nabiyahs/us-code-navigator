# Image Link Review Report
**Repository**: us-code-navigator
**Date**: 2025-11-06
**Branch**: claude/review-image-links-011CUsWJwJH43jgN5y4hNGAn

## Executive Summary

검토 결과, **총 8개의 이미지 연결 문제**가 발견되었습니다:
- 3개의 attachment가 잘못된 파일명을 참조하여 이미지가 표시되지 않습니다
- 5개의 JPG 파일이 index.html에서 참조되지 않아 사용자가 볼 수 없습니다

## 1. 이미지 로딩 메커니즘

index.html은 다음과 같이 이미지를 로드합니다:

1. **데이터 구조**: `appData.CodeAttachment` 배열에 이미지 메타데이터 저장 (index.html:41509)
2. **로딩 함수**: `openImageModalById()` 함수가 AttachmentID로 이미지를 검색 (index.html:43549)
3. **파일명 변환**: 여러 파일명 패턴을 시도하여 이미지 로드 (index.html:43574-43595)
   - 원본 파일명
   - 첫 번째 점을 밑줄로 변환 (예: `[BE]403.5.1` → `[BE]403_5.1`)
   - 모든 점을 밑줄로 변환
4. **확장자 시도**: `.jpg`, `.JPG`, `.jpeg`, `.JPEG` 순서로 시도

## 2. 발견된 문제

### 2.1 파일명 불일치 문제 (3건)

다음 attachment들이 잘못된 파일명을 참조하여 **이미지가 표시되지 않습니다**:

#### ❌ D001: Table 307.1(1)
- **참조 파일명**: `IBC_3_307.1_T307.1(1)`
- **실제 파일**: `IBC_3_307.1.1_T1.jpg` 또는 `IBC_3_307.1.1_T2.jpg`
- **위치**: index.html:41515
- **영향**: "Maximum Allowable Quantity Per Control Area of Hazardous Materials Posing a Physical Hazard" 테이블이 표시되지 않음

#### ❌ D002: Table 307.1(2)
- **참조 파일명**: `IBC_3_307.1_T307.1(2)`
- **실제 파일**: `IBC_3_307.1.1_T1.jpg` 또는 `IBC_3_307.1.1_T2.jpg`
- **위치**: index.html:41530
- **영향**: "Maximum Allowable Quantity Per Control Area of Hazardous Materials Posing a Health Hazard" 테이블이 표시되지 않음

#### ❌ D003: Figure (Section 403)
- **참조 파일명**: `IBC_4_403_F`
- **실제 파일**: **파일이 존재하지 않음**
- **위치**: index.html:41545
- **영향**: "High-Rise Definition" 그림이 표시되지 않음

### 2.2 참조되지 않는 파일 문제 (5건)

다음 JPG 파일들이 저장소에 존재하지만 **index.html에서 참조되지 않습니다**:

#### 📄 IBC 관련 파일 (2건)
1. **IBC_3_307.1.1_T1.jpg**
   - D001이 참조해야 할 것으로 추정
   - Table 307.1(1) 이미지로 추정

2. **IBC_3_307.1.1_T2.jpg**
   - D002가 참조해야 할 것으로 추정
   - Table 307.1(2) 이미지로 추정

#### 📄 NFPA 13 관련 파일 (3건)
1. **NFPA 13_3_3.3.89_F.jpg**
   - NFPA 13 2025 Chapter 3, Section 3.3.89 관련
   - CodeAttachment에 정의되지 않음

2. **NFPA 13_16_16.12_F.jpg**
   - NFPA 13 2025 Chapter 16, Section 16.12 관련
   - CodeAttachment에 정의되지 않음

3. **NFPA 13_17_17.4_F.jpg**
   - NFPA 13 2025 Chapter 17, Section 17.4 관련
   - CodeAttachment에 정의되지 않음

### 2.3 정상 작동하는 이미지 (17건)

다음 attachment들은 **정상적으로 작동**합니다:
- ✓ D004: IBC_4_[BE]403.5.1_F
- ✓ D005: IBC_4_[F]414.2_F
- ✓ D006: IBC_4_[F]414.2.2_T1
- ✓ D007: IBC_4_[F]414.2.2_F
- ✓ D008: IBC_4_[F]414.5.1_T
- ✓ D009: IBC_4_[F]415.6.5_T
- ✓ D010: IBC_4_[F]415.11.1.1_T
- ✓ D011: IBC_5_503.1.2_F1
- ✓ D012: IBC_5_503.1.2_F2
- ✓ D013: IBC_5_504.3_T
- ✓ D014: IBC_5_504.4_T
- ✓ D015: IBC_5_506.2_T
- ✓ D016: IBC_5_506.3.2_F
- ✓ D017: IBC_5_506.3.3_T
- ✓ D018: IBC_5_508.4_T
- ✓ D019: IBC_5_509.1_T
- ✓ D020: IBC_5_510.2_F

## 3. Display 문제

### 3.1 사용자가 볼 수 없는 이미지

다음 이미지들을 클릭하면 **이미지가 로드되지 않습니다**:
1. Table 307.1(1) - 위험물질 물리적 위험 최대 허용량
2. Table 307.1(2) - 위험물질 건강 위험 최대 허용량
3. Figure (Section 403) - 고층 건물 정의

### 3.2 접근할 수 없는 이미지

다음 이미지들은 index.html에서 **전혀 참조되지 않아** 사용자가 접근할 방법이 없습니다:
1. IBC_3_307.1.1_T1.jpg
2. IBC_3_307.1.1_T2.jpg
3. NFPA 13_3_3.3.89_F.jpg
4. NFPA 13_16_16.12_F.jpg
5. NFPA 13_17_17.4_F.jpg

## 4. 권장 수정 사항

### 4.1 긴급 수정 (Critical)

**index.html 파일 수정** (라인 41515, 41530):

```javascript
// D001 수정
"FileName": "IBC_3_307.1_T307.1(1)"  // 현재
→ "FileName": "IBC_3_307.1.1_T1"     // 수정 필요

// D002 수정
"FileName": "IBC_3_307.1_T307.1(2)"  // 현재
→ "FileName": "IBC_3_307.1.1_T2"     // 수정 필요
```

### 4.2 D003 처리

다음 중 하나를 선택:
- **옵션 A**: `IBC_4_403_F.jpg` 파일을 저장소에 추가
- **옵션 B**: D003 attachment를 index.html에서 제거

### 4.3 NFPA 13 이미지 통합

NFPA 13 관련 이미지들을 index.html의 CodeAttachment 배열에 추가:

```javascript
{
  "AttachmentID": "D021",
  "ModelCodeVersionID": "MCV003",  // NFPA 13 2025
  "Type": "F",
  "Number": null,
  "FileName": "NFPA 13_3_3.3.89_F",
  "Chapter": 3,
  "Section": 3,
  "Subsection": 3.89,
  "AttachTitleEN": "...",
  "AttachTitleKR": "...",
  "AttachContentEN": null,
  "AttachContentKR": null,
  "AttachComment": null
},
{
  "AttachmentID": "D022",
  "ModelCodeVersionID": "MCV003",
  "Type": "F",
  "Number": null,
  "FileName": "NFPA 13_16_16.12_F",
  "Chapter": 16,
  "Section": 16,
  "Subsection": 12,
  ...
},
{
  "AttachmentID": "D023",
  "ModelCodeVersionID": "MCV003",
  "Type": "F",
  "Number": null,
  "FileName": "NFPA 13_17_17.4_F",
  "Chapter": 17,
  "Section": 17,
  "Subsection": 4,
  ...
}
```

## 5. 통계

| 항목 | 개수 |
|------|------|
| 전체 JPG 파일 | 22 |
| CodeAttachment 참조 | 20 |
| 정상 작동 | 17 |
| 파일명 불일치 | 3 |
| 참조되지 않는 파일 | 5 |
| **총 문제 건수** | **8** |

## 6. 결론

index.html의 이미지 연결에 여러 문제가 발견되었습니다. 특히 Section 307.1의 중요한 테이블 이미지 2개가 표시되지 않고, NFPA 13 관련 이미지 3개가 전혀 사용되지 않고 있습니다. 위의 권장 수정 사항을 적용하여 모든 이미지가 정상적으로 표시되도록 해야 합니다.
