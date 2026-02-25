@echo off
echo =============================
echo Excel → JSON 변환 실행
echo =============================

REM Excel 파일 이름 설정
set EXCEL_FILE=data-us-code-navigator.xlsx

REM JSON 출력 폴더
set OUTPUT_DIR=json_out

REM JSON 들여쓰기(Pretty 출력) 사용할 경우: 빈 값 유지
set INDENT_FLAG=

REM JSON 용량을 최소화하고 싶다면 아래 주석 제거
REM set INDENT_FLAG=--no-indent

echo 실행 중...
python excel_to_json.py --input "%EXCEL_FILE%" --outdir "%OUTPUT_DIR%" %INDENT_FLAG%

echo.
echo 변환 완료! 출력 폴더: %OUTPUT_DIR%
pause
