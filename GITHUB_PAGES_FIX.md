# GitHub Pages 404 에러 해결 가이드

## 🔍 문제 확인

✅ **index.html은 저장소 루트에 정상적으로 있습니다!**
- 경로: `/index.html`
- public/ 폴더: `/public/` (이미지 20개)
- 모든 파일이 올바른 위치

## ❌ 404 에러 원인

**GitHub Pages 설정이 잘못되어 있습니다!**

현재 상태 (추정):
```
GitHub Pages Source: main 브랜치 / docs 폴더
                                    ^^^^
                                 잘못된 설정!
```

저장소 구조:
```
/  (루트)
├── index.html          ✅ 단일 페이지 앱 (이걸 봐야 함!)
├── public/
│   └── *.jpg (20개)
└── docs/               ⚠️ MkDocs 문서 (index.html 없음)
    └── *.md
```

## 🔧 해결 방법

### ⭐ 방법 1: GitHub Pages 설정 변경 (필수!)

**단계별 가이드:**

1. **GitHub 저장소 페이지 접속**
   ```
   https://github.com/Nabiyahs/us-code-navigator
   ```

2. **Settings 탭 클릭**

3. **왼쪽 메뉴에서 'Pages' 클릭**

4. **Build and deployment 섹션 찾기**

5. **설정 변경:**
   ```
   Source: Deploy from a branch

   Branch: main              ✅ (이미 맞음)
   Folder: /(root)          ⚠️ 이걸로 변경! (현재는 /docs일 것)
          ^^^^^^
          중요!
   ```

6. **Save 버튼 클릭**

7. **1-2분 대기 (자동 재배포)**

### 방법 2: .nojekyll 파일 머지 (선택)

GitHub에서 PR 생성 후 머지:
```
https://github.com/Nabiyahs/us-code-navigator/pull/new/claude/fix-github-pages-011CUsdyrj6DGmK1tTZBgapD
```

`.nojekyll` 파일은 Jekyll 처리를 비활성화합니다.

## 💡 권장 사항

**두 가지 방법을 모두 실행하세요:**
1. ✅ PR 머지 (.nojekyll 추가)
2. ✅ GitHub Pages 설정 변경 (docs → root)

## 🎯 결과 확인

설정 변경 후:
1. GitHub Pages 페이지에서 "Your site is published at ..." 메시지 확인
2. 해당 URL 클릭
3. index.html이 정상적으로 로드되는지 확인
4. 브라우저 개발자 도구 → Console에서 404 에러 없는지 확인
5. 이미지가 모두 표시되는지 확인

## 📸 스크린샷 참고 위치

GitHub Pages 설정 화면:
```
Settings → Pages → Build and deployment
├── Source: Deploy from a branch
└── Branch: [main] [/(root)] [Save]
                     ^^^^^^^
                   이걸로 변경!
```

## ❓ 문제가 계속되면

1. 브라우저 캐시 삭제 (Ctrl+Shift+R)
2. 프라이빗 브라우징으로 테스트
3. GitHub Actions 탭에서 Pages build and deployment 워크플로우 확인
4. 오류 로그 확인

---

**작성 일시**: 2025-11-07
**작성자**: Claude
