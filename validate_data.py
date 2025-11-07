#!/usr/bin/env python3
"""
데이터 일관성 검증 스크립트
새 데이터를 추가한 후 이 스크립트를 실행하여 문제를 조기에 발견할 수 있습니다.
"""

import json
import os

def validate_attachments():
    """CodeAttachment.json 검증"""
    print("=" * 70)
    print("CodeAttachment.json 검증")
    print("=" * 70)

    with open('CodeAttachment.json') as f:
        attachments = json.load(f)

    errors = []
    warnings = []

    for i, att in enumerate(attachments):
        att_id = att.get('AttachmentID') or f"index_{i}"

        # 필수 필드 검사
        if not att.get('AttachmentID'):
            errors.append(f"{att_id}: AttachmentID 누락")
        if not att.get('ModelCodeVersionID'):
            errors.append(f"{att_id}: ModelCodeVersionID 누락")
        if not att.get('FileName'):
            warnings.append(f"{att_id}: FileName 누락 (빈 레코드?)")
            continue

        # 데이터 타입 검사
        chapter = att.get('Chapter')
        if chapter is not None:
            if isinstance(chapter, float) and chapter == int(chapter):
                warnings.append(f"{att_id}: Chapter가 float({chapter})입니다. int({int(chapter)})로 변경 권장")

        # 파일 존재 확인
        filename = att['FileName']
        found = False
        for ext in ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG']:
            if os.path.exists(f"public/{filename}{ext}"):
                found = True
                if ext != '.jpg':
                    warnings.append(f"{att_id}: 파일 확장자 {ext}입니다. .jpg로 통일 권장")
                break

        if not found:
            errors.append(f"{att_id}: 파일 '{filename}.*'을 public/ 폴더에서 찾을 수 없음")

    # 결과 출력
    print(f"\n총 {len(attachments)}개 레코드 검사")

    if errors:
        print(f"\n❌ 오류 ({len(errors)}개):")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... 외 {len(errors) - 10}개")

    if warnings:
        print(f"\n⚠️  경고 ({len(warnings)}개):")
        for warn in warnings[:10]:
            print(f"  - {warn}")
        if len(warnings) > 10:
            print(f"  ... 외 {len(warnings) - 10}개")

    if not errors and not warnings:
        print("\n✅ 모든 검사 통과!")

    return len(errors) == 0

def validate_images():
    """public/ 폴더의 이미지 파일 검증"""
    print("\n" + "=" * 70)
    print("이미지 파일 검증")
    print("=" * 70)

    if not os.path.exists('public'):
        print("❌ public/ 폴더가 없습니다")
        return False

    images = []
    for root, dirs, files in os.walk('public'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                images.append(file)

    print(f"\n총 {len(images)}개 이미지 파일")

    # 확장자 통계
    extensions = {}
    for img in images:
        ext = os.path.splitext(img)[1]
        extensions[ext] = extensions.get(ext, 0) + 1

    print("\n확장자 분포:")
    for ext, count in sorted(extensions.items()):
        status = "✅" if ext == '.jpg' else "⚠️"
        print(f"  {status} {ext}: {count}개")

    if len(extensions) > 1:
        print("\n⚠️  권장: 모든 확장자를 .jpg로 통일")
    else:
        print("\n✅ 확장자가 통일되어 있습니다")

    return True

def main():
    print("\n🔍 데이터 일관성 검증 시작\n")

    valid_attachments = validate_attachments()
    valid_images = validate_images()

    print("\n" + "=" * 70)
    print("검증 완료")
    print("=" * 70)

    if valid_attachments and valid_images:
        print("✅ 모든 검증 통과!")
        return 0
    else:
        print("❌ 일부 검증 실패. 위 메시지를 확인하세요.")
        return 1

if __name__ == '__main__':
    exit(main())
