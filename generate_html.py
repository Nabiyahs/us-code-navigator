#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US Code Navigator HTML Generator with Schema-based Data Integration
이 스크립트는 schema-meta.json을 기반으로 데이터 계층 구조를 파악하고
reference.txt의 HTML 구조를 유지하면서 JSON 데이터를 통합합니다.
"""

import json
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict

# 파일 경로
BASE_DIR = Path("/home/user/us-code-navigator")
REFERENCE_FILE = BASE_DIR / "reference.txt"
SCHEMA_FILE = BASE_DIR / "schema-meta.json"
OUTPUT_FILE = BASE_DIR / "index.html"

# JSON 파일들
JSON_FILES = {
    'CodeType': 'CodeType.json',
    'ModelCode': 'ModelCode.json',
    'ModelCodeVersion': 'ModelCodeVersion.json',
    'Discipline': 'Discipline.json',
    'ModelCodeDiscipline': 'ModelCodeDiscipline.json',
    'CodeChapter': 'CodeChapter.json',
    'Jurisdiction': 'Jurisdiction.json',
    'CodeContent': 'CodeContent.json',
    'CodeAttachment': 'CodeAttachment.json'
}

class DataHierarchy:
    """스키마를 기반으로 데이터 계층 구조를 관리하는 클래스"""

    def __init__(self, schema, data):
        self.schema = schema
        self.data = data
        self.relationships = self._parse_relationships()
        self.indexes = self._build_indexes()

    def _parse_relationships(self):
        """스키마에서 관계를 파싱합니다."""
        relationships = defaultdict(list)

        for table_name, table_info in self.schema['tables'].items():
            for fk in table_info.get('fks', []):
                ref_table = fk['ref']['table']
                relationships[table_name].append({
                    'columns': fk['columns'],
                    'ref_table': ref_table,
                    'ref_columns': fk['ref']['columns']
                })

        return relationships

    def _build_indexes(self):
        """빠른 조회를 위한 인덱스를 생성합니다."""
        indexes = {}

        # 각 테이블의 PK 인덱스 생성
        for table_name, records in self.data.items():
            if table_name not in self.schema['tables']:
                continue

            pk_columns = self.schema['tables'][table_name]['pk']
            indexes[table_name] = {}

            for record in records:
                # PK 값으로 인덱스 생성
                if len(pk_columns) == 1:
                    key = record.get(pk_columns[0])
                    if key:
                        indexes[table_name][key] = record
                else:
                    # 복합 키
                    key = tuple(record.get(col) for col in pk_columns)
                    indexes[table_name][key] = record

        return indexes

    def get_related(self, table_name, record, ref_table):
        """관련된 레코드를 가져옵니다."""
        relationships = self.relationships.get(table_name, [])

        for rel in relationships:
            if rel['ref_table'] == ref_table:
                # FK 값으로 참조 레코드 찾기
                if len(rel['ref_columns']) == 1:
                    key = record.get(rel['columns'][0])
                    return self.indexes.get(ref_table, {}).get(key)
                else:
                    # 복합 키
                    key = tuple(record.get(col) for col in rel['columns'])
                    return self.indexes.get(ref_table, {}).get(key)

        return None

    def get_children(self, table_name, record):
        """자식 레코드들을 가져옵니다."""
        pk_columns = self.schema['tables'][table_name]['pk']
        pk_value = record.get(pk_columns[0]) if len(pk_columns) == 1 else tuple(record.get(col) for col in pk_columns)

        children = {}

        # 모든 테이블을 순회하며 현재 레코드를 참조하는 것을 찾음
        for child_table, child_rels in self.relationships.items():
            for rel in child_rels:
                if rel['ref_table'] == table_name:
                    # 이 테이블이 현재 레코드를 참조함
                    matching_records = []
                    for child_record in self.data.get(child_table, []):
                        if len(rel['columns']) == 1:
                            if child_record.get(rel['columns'][0]) == pk_value:
                                matching_records.append(child_record)
                        else:
                            child_key = tuple(child_record.get(col) for col in rel['columns'])
                            if child_key == pk_value:
                                matching_records.append(child_record)

                    if matching_records:
                        if child_table not in children:
                            children[child_table] = []
                        children[child_table].extend(matching_records)

        return children

def load_json_data():
    """모든 JSON 파일을 로드합니다."""
    data = {}
    for key, filename in JSON_FILES.items():
        file_path = BASE_DIR / filename
        print(f"Loading {filename}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data[key] = json.load(f)
    return data

def load_schema():
    """스키마 파일을 로드합니다."""
    print(f"Loading schema from {SCHEMA_FILE}...")
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_html():
    """reference.txt HTML 파일을 로드합니다."""
    print(f"Loading {REFERENCE_FILE}...")
    with open(REFERENCE_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

def get_icon_svg(code_name):
    """코드 이름에 맞는 아이콘 SVG를 반환합니다."""
    icons = {
        'IBC': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                    <path d="M9 22v-4h6v4"></path>
                    <path d="M8 6h.01"></path>
                    <path d="M16 6h.01"></path>
                    <path d="M12 6h.01"></path>
                    <path d="M12 10h.01"></path>
                    <path d="M12 14h.01"></path>
                    <path d="M16 10h.01"></path>
                    <path d="M16 14h.01"></path>
                    <path d="M8 10h.01"></path>
                    <path d="M8 14h.01"></path>
                  </svg>''',
        'NFPA 13': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"></path>
                    <path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"></path>
                  </svg>''',
        'NFPA 14': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="m2 22 1-1h3l9-9"></path>
                    <path d="M3 21v-3l9-9"></path>
                    <path d="m15 6 3.4-3.4a2.1 2.1 0 1 1 3 3L18 9l.4.4a2.1 2.1 0 1 1-3 3l-3.8-3.8a2.1 2.1 0 1 1 3-3l.4.4Z"></path>
                  </svg>''',
        'NFPA 20': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="m12 14 4-4"></path>
                    <path d="M3.34 19a10 10 0 1 1 17.32 0"></path>
                  </svg>''',
        'NFPA 72': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M6 8a6 6 0 0112 0c0 7 3 9 3 9H3s3-2 3-9"></path>
                    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path>
                  </svg>''',
        'ADA': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <circle cx="16" cy="4" r="1"></circle>
                    <path d="m18 19 1-7-6 1"></path>
                    <path d="M5 8 3-3 5.5 3-2.36 3.5"></path>
                    <path d="M4.24 14.5a5 5 0 0 0 6.88 6"></path>
                    <path d="M13.76 17.5a5 5 0 0 0-6.88-6"></path>
                  </svg>''',
        'IMC': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"></path>
                    <path d="M9.6 4.6A2 2 0 1 1 11 8H2"></path>
                    <path d="M12.6 19.4A2 2 0 1 0 14 16H2"></path>
                  </svg>''',
        'IPC': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                  </svg>''',
        'NEC': '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                  </svg>'''
    }

    # 코드 이름에서 시작 부분 매칭
    for key in icons:
        if code_name.startswith(key):
            return icons[key]

    # 기본 아이콘
    return '''<svg class="w-6 h-6 text-[#24305E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>'''

def create_library_cards(hierarchy):
    """스키마 기반으로 라이브러리 카드를 생성합니다."""
    cards_html = []

    # 데이터가 있는 코드와 없는 코드를 분리
    codes_with_data = []
    codes_without_data = []

    # ModelCode와 관련 데이터를 조인
    for model_code in hierarchy.data['ModelCode']:
        model_code_id = model_code['ModelCodeID']
        code_name = model_code['ModelCodeName']
        description = model_code['Description']

        # ModelCodeDiscipline을 통해 Discipline 찾기
        discipline_name = '기타'
        badge_color = '#A8D0E6'
        badge_text = '건축·구조'

        for mcd in hierarchy.data['ModelCodeDiscipline']:
            if mcd['ModelCodeID'] == model_code_id:
                discipline = hierarchy.get_related('ModelCodeDiscipline', mcd, 'Discipline')
                if discipline:
                    discipline_name = discipline['DisciplineNameKR']
                    if '소방' in discipline_name or '안전' in discipline_name:
                        badge_color = '#F76C6C'
                        badge_text = '소방'
                    break

        # 최신 버전 찾기
        versions = [v for v in hierarchy.data['ModelCodeVersion'] if v['ModelCodeID'] == model_code_id]
        latest_version = max(versions, key=lambda v: v.get('Year') or 0) if versions else None

        # 버전 텍스트
        if latest_version and latest_version.get('Year'):
            year = int(latest_version['Year']) if latest_version['Year'] else ''
            version_text = f"{code_name.split(':')[0].strip()} {year}" if year else code_name
        else:
            version_text = code_name.split(':')[0].strip()

        # 아이콘
        icon_svg = get_icon_svg(code_name)

        # 활성화 여부 (챕터가 있는 코드만 활성화)
        chapters = hierarchy.get_children('ModelCodeVersion', latest_version) if latest_version else {}
        is_active = 'CodeChapter' in chapters and len(chapters['CodeChapter']) > 0

        opacity_class = '' if is_active else 'opacity-50'
        cursor_class = 'cursor-pointer' if is_active else 'cursor-not-allowed'
        data_attrs = f'data-code-id="{model_code_id}" data-version-id="{latest_version["ModelCodeVersionID"]}"' if is_active and latest_version else ''

        card_html = f'''
              <div class="code-card bg-white p-4 rounded-lg border-2 border-gray-200 {cursor_class} relative {opacity_class}" data-nav="library" {data_attrs}>
                <span class="absolute top-3 right-3 text-xs font-medium text-[{badge_color}] bg-[{badge_color}] bg-opacity-20 px-2 py-1 rounded">{badge_text}</span>
                <div class="w-12 h-12 bg-[#F8E9A1] rounded-lg flex items-center justify-center mb-3">
                  {icon_svg}
                </div>
                <h3 class="text-lg font-bold text-[#24305E] mb-1">{version_text}</h3>
                <p class="text-gray-600 text-xs">{description}</p>
              </div>'''

        # 데이터 유무에 따라 분류
        if is_active:
            codes_with_data.append(card_html)
        else:
            codes_without_data.append(card_html)

    # 데이터가 있는 코드를 먼저, 그 다음 없는 코드 순서로 배치
    return '\n'.join(codes_with_data + codes_without_data)

def escape_js_string(s):
    """JavaScript 문자열을 이스케이프합니다."""
    if not s:
        return ''
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

def create_all_library_content(hierarchy):
    """라이브러리 섹션의 모든 코드 콘텐츠를 생성합니다."""
    all_codes_content = []
    first_code_id = None

    for model_code in hierarchy.data['ModelCode']:
        model_code_id = model_code['ModelCodeID']

        # 최신 버전 찾기
        versions = [v for v in hierarchy.data['ModelCodeVersion'] if v['ModelCodeID'] == model_code_id]
        latest_version = max(versions, key=lambda v: v.get('Year') or 0) if versions else None

        if not latest_version:
            continue

        # 챕터가 있는지 확인
        chapters = hierarchy.get_children('ModelCodeVersion', latest_version)
        if 'CodeChapter' not in chapters or len(chapters['CodeChapter']) == 0:
            continue

        # 첫 번째 활성 코드 찾음!
        chapter_list = sorted(chapters['CodeChapter'], key=lambda x: x['Chapter'])

        # 챕터 리스트 HTML 생성 (섹션 포함)
        chapters_html = []
        for i, ch in enumerate(chapter_list):
            active_class = 'active bg-[#F8E9A1]' if i == 0 else ''
            chapter_id = ch['ChapterID']
            chapter_num = ch['Chapter']

            # 이 챕터의 섹션 목록 가져오기
            chapter_contents = [c for c in hierarchy.data['CodeContent'] if c.get('ChapterID') == chapter_id]
            sections = {}
            for content in chapter_contents:
                section = content.get('Section') or 'General'
                if section not in sections:
                    sections[section] = content.get('TitleEN', '')

            # 섹션 HTML 생성
            sections_html = []
            def section_sort_key(x):
                import re
                if x == 'General':
                    return (0, 'General')
                match = re.search(r'\d+', str(x))
                if match:
                    return (int(match.group()), str(x))
                return (999999, str(x))

            for section_num in sorted(sections.keys(), key=section_sort_key):
                section_title = sections[section_num]
                sections_html.append(f'''
                  <div class="section-item px-4 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded cursor-pointer"
                       onclick="scrollToSection('{chapter_id}', '{section_num}')">
                    Section {section_num}{': ' + section_title if section_title else ''}
                  </div>''')

            # 챕터 그룹 (챕터 + 섹션)
            expanded_class = 'max-h-96' if i == 0 else 'max-h-0'
            icon_rotation = 'rotate-180' if i == 0 else ''
            title_kr = ch.get('TitleKR', '')
            chapters_html.append(f'''
              <div class="chapter-group">
                <div class="chapter-item {active_class} px-4 py-3 rounded-lg cursor-pointer flex items-center justify-between"
                     data-chapter-id="{chapter_id}"
                     onclick="toggleChapterSidebar('{chapter_id}')">
                  <div>
                    <div class="font-semibold text-[#24305E] text-sm">Chapter {chapter_num}</div>
                    <div class="text-xs text-gray-600 mt-1">{ch['TitleEN'] or ''}</div>
                    {f'<div class="text-sm text-gray-500 mt-0.5">{title_kr}</div>' if title_kr else ''}
                  </div>
                  <svg class="w-4 h-4 text-[#24305E] transition-transform {icon_rotation}" id="chevron-{chapter_id}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                  </svg>
                </div>
                <div class="sections-list overflow-hidden transition-all duration-300 {expanded_class}" id="sections-{chapter_id}">
                  {''.join(sections_html)}
                </div>
              </div>''')

        # 모든 챕터의 콘텐츠 생성
        content_html = []
        for chapter in chapter_list:
            chapter_id = chapter['ChapterID']
            chapter_num = chapter['Chapter']

            # 이 챕터의 콘텐츠 가져오기
            contents = [c for c in hierarchy.data['CodeContent'] if c.get('ChapterID') == chapter_id]

            # Helper function to parse section/subsection for sorting
            def parse_section_key(value):
                if not value:
                    return (0,)
                # Handle both "1,1" and "2.1.1" formats
                value_str = str(value).replace(',', '.')
                try:
                    parts = [float(p) for p in value_str.split('.')]
                    return tuple(parts)
                except:
                    return (0,)

            contents.sort(key=lambda x: (
                parse_section_key(x.get('Section')),
                parse_section_key(x.get('Subsection'))
            ))

            if not contents:
                continue

            # 챕터 시작
            content_html.append(f'''
            <div class="bg-white rounded-lg shadow-sm p-8 mb-6" id="chapter-{chapter_id}">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-[#24305E] mb-2">Chapter {chapter_num}: {chapter['TitleEN'] or ''}</h2>
                    {f'<p class="text-base text-gray-600">{chapter["TitleKR"]}</p>' if chapter.get('TitleKR') else ''}
                </div>
                {f'<div class="mb-6 p-4 bg-blue-50 border-l-4 border-blue-400 rounded"><p class="text-base text-gray-700 whitespace-pre-line">{chapter["ChapterComment"]}</p></div>' if chapter.get('ChapterComment') else ''}
            ''')

            # 섹션별로 그룹화
            sections = {}
            for content in contents:
                section = content.get('Section') or 'General'
                if section not in sections:
                    sections[section] = []
                sections[section].append(content)

            # 각 섹션 출력
            def get_section_sort_key(section_str):
                import re
                if section_str == 'General':
                    return (0, 'General')
                # Extract numeric part from formats like "[F]414", "[BS]403", or plain "123"
                match = re.search(r'\d+', str(section_str))
                if match:
                    return (int(match.group()), str(section_str))
                return (999999, str(section_str))  # Put unparseable sections at the end

            for section_num in sorted(sections.keys(), key=get_section_sort_key):
                section_contents = sections[section_num]
                first_content = section_contents[0]

                # Display only "General" for General sections, not "Section General"
                section_title = section_num if section_num == 'General' else f'Section {section_num}'
                title_suffix = f' - {first_content["TitleEN"]}' if first_content.get('TitleEN') else ''

                content_html.append(f'''
                <div class="content-section mb-8" id="section-{chapter_id}-{section_num}">
                    <h3 class="text-xl font-semibold text-[#374785] mb-3">{section_title}{title_suffix}</h3>
                    {f'<p class="text-lg text-gray-600 mb-4">{first_content["TitleKR"]}</p>' if first_content.get('TitleKR') else ''}
                    <div class="space-y-4">''')

                # 각 subsection
                for content in section_contents:
                    subsection = f".{content['Subsection']}" if content.get('Subsection') else ''
                    section_number = f"{section_num}{subsection}"

                    # Attachments
                    attachments = [att for att in hierarchy.data['CodeAttachment']
                                   if att.get('ModelCodeVersionID') == latest_version['ModelCodeVersionID']
                                   and att.get('Chapter') == str(chapter_num)
                                   and att.get('Section') == str(section_num)
                                   and att.get('Subsection') == content.get('Subsection')]

                    attachment_html = ''
                    if attachments:
                        att_items = []
                        for att in attachments:
                            icon = 'M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z' if att['Type'].lower() == 'table' else 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'
                            att_items.append(f'''
                            <div class="border border-gray-300 rounded p-2 hover:border-[#A8D0E6] transition-colors cursor-pointer flex-shrink-0" style="min-width: 120px;">
                                <div class="bg-gray-100 h-16 rounded flex items-center justify-center mb-1">
                                    <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon}"></path>
                                    </svg>
                                </div>
                                <p class="text-xs font-medium text-gray-700 text-center">{att['Type']} {att.get('Number') or ''}</p>
                            </div>''')
                        attachment_html = f'''
                        <div class="mt-3 pt-3 border-t border-gray-200">
                            <div class="figures-scroll">
                                {''.join(att_items)}
                            </div>
                        </div>'''

                    # 코드 정보와 위치 생성
                    code_base = model_code['ModelCodeName'].split(':')[0].strip()
                    year = int(latest_version['Year']) if latest_version.get('Year') else ''
                    location_text = f"{code_base} {year}: Chapter {chapter_num} - {section_number}"

                    content_html.append(f'''
                    <div class="bg-gray-50 p-4 rounded-lg relative" id="section-{section_number.replace('.', '-')}">
                        <div class="absolute top-3 right-3 flex items-center gap-1">
                            <button class="p-1.5 hover:bg-gray-200 rounded transition-colors" title="Copy link" onclick="copyLink('{section_number}')">
                                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                                </svg>
                            </button>
                        </div>
                        <div class="flex items-center gap-2 mb-3 flex-wrap">
                            <span class="text-xs bg-[#A8D0E6] text-[#24305E] font-semibold px-2 py-0.5 rounded">{location_text}</span>
                        </div>
                        <div class="flex items-center gap-2 mb-2">
                            <h4 class="font-semibold text-[#24305E]">{section_number}{' ' + content['TitleEN'] if content.get('TitleEN') else ''}</h4>
                        </div>
                        {f'<p class="text-base text-gray-600 mb-2">{content["TitleKR"]}</p>' if content.get('TitleKR') else ''}
                        {f'<p class="text-gray-700 leading-relaxed mb-2">{content["ContentEN"]}</p>' if content.get('ContentEN') else ''}
                        {f'<p class="text-gray-600 text-base leading-relaxed mb-3">{content["ContentKR"]}</p>' if content.get('ContentKR') else ''}
                        {f'<div class="mt-3 pt-3 border-t border-gray-200 bg-[#FEE9EC] bg-opacity-30 p-3 rounded-lg"><label class="text-xs font-semibold text-[#F76C6C] mb-1 block">Note</label><div class="w-full text-base p-2 bg-white border border-[#F76C6C] border-opacity-20 rounded text-gray-700 whitespace-pre-line">{content["Comment"]}</div></div>' if content.get('Comment') else ''}
                        {attachment_html}
                    </div>''')

                content_html.append('</div></div>')

            content_html.append('</div>')

        # 코드 정보 저장
        code_data = {
            'code_id': model_code_id,
            'version_id': latest_version['ModelCodeVersionID'],
            'code_name': model_code['ModelCodeName'],
            'code_title': f"{model_code['ModelCodeName'].split(':')[0].strip()} {int(latest_version['Year'])}",
            'code_subtitle': model_code['Description'],
            'chapters_html': '\n'.join(chapters_html),
            'content_html': '\n'.join(content_html)
        }
        all_codes_content.append(code_data)

        # 첫 번째 코드 ID 저장
        if first_code_id is None:
            first_code_id = model_code_id

    # 모든 코드 데이터와 첫 번째 코드 ID 반환
    return {
        'codes': all_codes_content,
        'first_code_id': first_code_id
    }

def create_sidebar_library_submenu(hierarchy):
    """사이드바 라이브러리 하위메뉴를 생성합니다."""
    submenu_items = []

    # 데이터가 있는 코드만 필터링
    for model_code in hierarchy.data['ModelCode']:
        model_code_id = model_code['ModelCodeID']
        code_name = model_code['ModelCodeName']

        # 최신 버전 찾기
        versions = [v for v in hierarchy.data['ModelCodeVersion'] if v['ModelCodeID'] == model_code_id]
        latest_version = max(versions, key=lambda v: v.get('Year') or 0) if versions else None

        if not latest_version:
            continue

        # 챕터가 있는지 확인
        chapters = hierarchy.get_children('ModelCodeVersion', latest_version)
        if 'CodeChapter' not in chapters or len(chapters['CodeChapter']) == 0:
            continue

        # 버전 텍스트
        code_base = code_name.split(':')[0].strip()
        if latest_version.get('Year'):
            year = int(latest_version['Year'])
            display_name = f"{code_base} {year}"
        else:
            display_name = code_base

        # Icon SVG 가져오기 (sidebar용으로 크기 조정)
        icon_svg_full = get_icon_svg(code_base)
        # w-6 h-6을 w-4 h-4로 변경하고, text-[#24305E]를 제거 (현재 색상 상속)
        icon_svg = icon_svg_full.replace('w-6 h-6', 'w-4 h-4 mr-2').replace('text-[#24305E]', '')

        submenu_html = f'''
        <div class="submenu-item flex items-center pl-14 pr-6 py-2 text-sm text-gray-300 hover:text-white hover:bg-[#374785] rounded cursor-pointer transition-colors"
             data-section="library"
             data-code-id="{model_code_id}"
             data-version-id="{latest_version['ModelCodeVersionID']}"
             onclick="loadCodeFromSidebar('{latest_version['ModelCodeVersionID']}', '{model_code_id}')">
            {icon_svg}
            {display_name}
        </div>'''

        submenu_items.append(submenu_html)

    return '\n'.join(submenu_items)

def generate_html(hierarchy):
    """최종 HTML을 생성합니다."""
    print("Parsing reference HTML...")
    html_content = load_html()
    soup = BeautifulSoup(html_content, 'lxml')

    # 사이드바의 라이브러리 메뉴에 접기/펴기 아이콘과 하위메뉴 추가
    print("Adding collapsible submenu to sidebar library...")
    sidebar = soup.find('aside', class_='fixed')
    if sidebar:
        # 기존 librarySubmenu를 찾아서 내용 교체
        library_submenu = sidebar.find('div', id='librarySubmenu')
        if library_submenu:
            # 기존 내용 제거
            library_submenu.clear()

            # 새로운 submenu 항목들 추가
            submenu_items_html = create_sidebar_library_submenu(hierarchy)
            submenu_soup = BeautifulSoup(submenu_items_html, 'lxml')

            # body 안의 모든 요소들을 librarySubmenu에 추가
            body = submenu_soup.find('body')
            if body:
                for element in body.children:
                    if element.name:  # 텍스트 노드가 아닌 경우만
                        library_submenu.append(element)

            print("✓ Sidebar library submenu updated with database!")
        else:
            # librarySubmenu가 없으면 생성 (기존 로직)
            library_item = None
            for item in sidebar.find_all('div', class_='sidebar-item'):
                if item.get('data-section') == 'library':
                    library_item = item
                    break

            if library_item:
                # 기존 라이브러리 항목에 chevron 아이콘 추가
                library_item['onclick'] = 'toggleLibrarySubmenu(event)'
                library_item['class'] = library_item.get('class', []) + ['relative']

                # SVG 아이콘 뒤에 chevron 추가
                chevron_html = '''
                <svg class="w-4 h-4 ml-auto transition-transform" id="libraryChevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
                '''
                chevron_soup = BeautifulSoup(chevron_html, 'lxml')
                library_item.append(chevron_soup.find('svg'))

                # 하위메뉴 생성
                submenu_html = f'''
                <div class="library-submenu overflow-hidden transition-all duration-300" style="max-height: 0;" id="librarySubmenu">
                    {create_sidebar_library_submenu(hierarchy)}
                </div>
                '''
                submenu_soup = BeautifulSoup(submenu_html, 'lxml')

                # 라이브러리 항목 다음에 하위메뉴 삽입
                library_item.insert_after(submenu_soup.find('div'))
                print("✓ Sidebar library submenu added!")

    # Make top search bar header sticky with proper z-index
    print("Ensuring top search bar is sticky with proper z-index...")
    main_header = soup.find('header', class_='bg-white')
    if main_header and 'sticky' in main_header.get('class', []):
        header_classes = main_header.get('class', [])
        # Remove old z-index if present
        header_classes = [c for c in header_classes if not c.startswith('z-')]
        # Add z-20 to ensure it's above other sticky elements
        if 'z-20' not in header_classes:
            header_classes.append('z-20')
        main_header['class'] = header_classes
        print("✓ Top search bar header updated with z-20!")

    # Libraries 섹션의 코드 카드들을 교체
    print("Generating library cards from schema hierarchy...")
    h2_elements = soup.find_all('h2', string=lambda text: text and 'Libraries' in text)
    if h2_elements:
        for h2 in h2_elements:
            parent_section = h2.find_parent('section')
            if parent_section:
                grid_div = parent_section.find('div', class_='grid')
                if grid_div:
                    library_cards_html = create_library_cards(hierarchy)
                    new_grid = BeautifulSoup(f'<div class="grid grid-cols-4 gap-4">{library_cards_html}</div>', 'lxml')
                    grid_div.replace_with(new_grid.find('div'))
                    print("✓ Library cards updated with hierarchical data!")

    # 라이브러리 섹션에 실제 데이터 삽입
    print("Generating initial library content with actual database...")
    all_content = create_all_library_content(hierarchy)

    library_section = soup.find('div', id='librarySection')
    if library_section and all_content and all_content['codes']:
        # 첫 번째 코드로 초기화
        first_code = all_content['codes'][0]

        # 헤더 업데이트
        code_title = library_section.find('h1', id='codeTitle')
        code_subtitle = library_section.find('p', id='codeSubtitle')
        if code_title:
            code_title.string = first_code['code_title']
        if code_subtitle:
            code_subtitle.string = first_code['code_subtitle']

        # 라이브러리 헤더를 sticky로 만들기
        library_header = library_section.find('header')
        if library_header:
            header_classes = library_header.get('class', [])
            if 'sticky' not in header_classes:
                header_classes.extend(['sticky', 'top-0', 'z-10'])
                library_header['class'] = header_classes

        # 챕터 리스트 컨테이너 찾기
        aside = library_section.find('aside', class_='w-80')
        chapters_container = None
        if aside:
            # Make aside sticky with correct top offset (header height)
            aside['class'] = aside.get('class', [])
            if 'sticky' not in aside['class']:
                aside['class'].append('sticky')
            # aside should stick below the header
            aside['style'] = 'top: 88px; max-height: calc(100vh - 88px);'

            chapters_heading = aside.find('h2', string='Chapters')
            if chapters_heading:
                chapters_container = chapters_heading.find_next('div', class_='space-y-2')

        # flex container에 높이 제한 추가 (header의 바로 다음 형제 요소)
        if library_header:
            flex_container = library_header.find_next_sibling('div', class_='flex')
            if flex_container:
                flex_container['style'] = 'height: calc(100vh - 88px); overflow: hidden;'

                # content area의 부모 div에 overflow 추가
                content_parent = flex_container.find('div', class_='flex-1')
                if content_parent:
                    content_parent['class'] = content_parent.get('class', [])
                    if 'overflow-y-auto' not in content_parent['class']:
                        content_parent['class'].append('overflow-y-auto')

        # 콘텐츠 영역 찾기
        content_area = library_section.find('div', id='contentArea')

        # 모든 코드의 챕터 리스트와 콘텐츠 생성
        if chapters_container and content_area:
            chapters_container.clear()
            content_area.clear()

            for i, code_data in enumerate(all_content['codes']):
                is_first = (i == 0)
                # 첫 번째는 명시적으로 display: block, 나머지는 display: none
                display_style = 'display: block;' if is_first else 'display: none;'

                # 챕터 리스트 추가
                chapter_wrapper = soup.new_tag('div',
                                               id=f"chapters-{code_data['code_id']}",
                                               style=display_style,
                                               **{'class': 'code-chapters'})
                chapters_soup = BeautifulSoup(code_data['chapters_html'], 'lxml')
                body = chapters_soup.find('body')
                if body:
                    for element in body.find_all('div', class_='chapter-group', recursive=False):
                        chapter_wrapper.append(element)
                chapters_container.append(chapter_wrapper)

                # 콘텐츠 추가
                content_wrapper = soup.new_tag('div',
                                               id=f"content-{code_data['code_id']}",
                                               style=display_style,
                                               **{'class': 'code-content'})
                content_soup = BeautifulSoup(code_data['content_html'], 'lxml')
                body = content_soup.find('body')
                if body:
                    for element in body.find_all('div', class_='bg-white', recursive=False):
                        content_wrapper.append(element)
                content_area.append(content_wrapper)

            print(f"✓ Library populated with {len(all_content['codes'])} codes")

    # Restructure Advanced Search section
    print("Restructuring advanced search layout...")
    search_section = soup.find('div', id='searchSection')
    if search_section:
        # Find the keyword search div and remove it
        keyword_div = search_section.find('div', class_='mb-6')
        if keyword_div and keyword_div.find('input', id='keywordInput'):
            keyword_div.decompose()
            print("✓ Removed initial keyword search input")

        # Find the filter collapsible header and remove it, keep filterSection expanded
        collapsible_header = search_section.find('div', class_='collapsible-header')
        if collapsible_header:
            collapsible_header.decompose()
            print("✓ Removed collapsible filter header")

        # Update filterSection to be always expanded without border-t
        filter_section_parent = search_section.find('div', class_='border-t')
        if filter_section_parent:
            # Remove border-t and pt-4 classes
            parent_classes = filter_section_parent.get('class', [])
            parent_classes = [c for c in parent_classes if c not in ['border-t', 'pt-4']]
            filter_section_parent['class'] = parent_classes

        filter_section = search_section.find('div', id='filterSection')
        if filter_section:
            # Ensure it's always expanded
            filter_classes = filter_section.get('class', [])
            if 'expanded' not in filter_classes:
                filter_classes.append('expanded')
            filter_section['class'] = filter_classes
            print("✓ Filter section set to always expanded")

        print("✓ Advanced search layout restructured")

    # JavaScript 데이터 및 기능 삽입
    print("Injecting JavaScript with schema-based data hierarchy...")
    script_tag = soup.new_tag('script')

    # JSON 데이터를 안전하게 JavaScript에 삽입
    json_data = json.dumps(hierarchy.data, ensure_ascii=False, indent=2)

    script_tag.string = f'''
// === Data Layer ===
const appData = {json_data};

// === Schema-based Data Access Functions ===
function getModelCodeVersions(modelCodeId) {{
    return appData.ModelCodeVersion.filter(v => v.ModelCodeID === modelCodeId);
}}

function getChapters(versionId) {{
    return appData.CodeChapter.filter(ch => ch.ModelCodeVersionID === versionId)
        .sort((a, b) => a.Chapter - b.Chapter);
}}

function getContents(chapterId) {{
    return appData.CodeContent.filter(c => c.ChapterID === chapterId)
        .sort((a, b) => {{
            const aSection = parseFloat(a.Section) || 0;
            const bSection = parseFloat(b.Section) || 0;
            if (aSection !== bSection) return aSection - bSection;

            const aSubsection = parseFloat(a.Subsection) || 0;
            const bSubsection = parseFloat(b.Subsection) || 0;
            return aSubsection - bSubsection;
        }});
}}

function getAttachments(versionId, chapter, section, subsection) {{
    return appData.CodeAttachment.filter(att =>
        att.ModelCodeVersionID === versionId &&
        att.Chapter === String(chapter) &&
        att.Section === String(section) &&
        att.Subsection === subsection
    );
}}

function getModelCode(modelCodeId) {{
    return appData.ModelCode.find(mc => mc.ModelCodeID === modelCodeId);
}}

function getDiscipline(modelCodeId) {{
    const mcd = appData.ModelCodeDiscipline.find(mcd => mcd.ModelCodeID === modelCodeId);
    if (mcd) {{
        return appData.Discipline.find(d => d.DisciplineID === mcd.DisciplineID);
    }}
    return null;
}}

// === UI Functions ===
function loadChapters(versionId, codeId) {{
    const chapters = getChapters(versionId);
    const chapterList = document.getElementById('chapterList');

    if (!chapters || chapters.length === 0) {{
        chapterList.innerHTML = '<p class="text-gray-500 text-sm p-4">No chapters available</p>';
        return;
    }}

    // 챕터 리스트 생성
    chapterList.innerHTML = chapters.map((ch, i) => `
        <div class="chapter-item ${{i === 0 ? 'active bg-[#F8E9A1]' : ''}} px-4 py-3 rounded-lg cursor-pointer"
             data-chapter="${{ch.Chapter}}" data-chapter-id="${{ch.ChapterID}}" onclick="loadChapterContent('${{ch.ChapterID}}', '${{versionId}}')">
            <div class="font-semibold text-[#24305E] text-sm">Chapter ${{ch.Chapter}}</div>
            <div class="text-xs text-gray-600 mt-1">${{ch.TitleEN || ''}}</div>
        </div>
    `).join('');

    // 코드 제목 업데이트
    const modelCode = getModelCode(codeId);
    const version = appData.ModelCodeVersion.find(v => v.ModelCodeVersionID === versionId);

    if (modelCode) {{
        const codeName = modelCode.ModelCodeName.split(':')[0].trim();
        const year = version && version.Year ? ' ' + Math.floor(version.Year) : '';
        document.getElementById('codeTitle').textContent = codeName + year;
        document.getElementById('codeSubtitle').textContent = modelCode.Description || '';
    }}

    // 첫 번째 챕터 로드
    if (chapters.length > 0) {{
        loadChapterContent(chapters[0].ChapterID, versionId);
    }}
}}

function loadChapterContent(chapterId, versionId) {{
    const chapter = appData.CodeChapter.find(ch => ch.ChapterID === chapterId);
    if (!chapter) return;

    // 챕터 활성화 표시
    document.querySelectorAll('.chapter-item').forEach(item => {{
        item.classList.remove('active', 'bg-[#F8E9A1]');
    }});
    const activeItem = document.querySelector(`[data-chapter-id="${{chapterId}}"]`);
    if (activeItem) {{
        activeItem.classList.add('active', 'bg-[#F8E9A1]');
    }}

    // 콘텐츠 로드
    const contents = getContents(chapterId);
    const contentArea = document.getElementById('contentArea');

    if (!contents || contents.length === 0) {{
        contentArea.innerHTML = `
            <div class="bg-white rounded-lg shadow-sm p-8">
                <h2 class="text-2xl font-bold text-[#24305E] mb-2">Chapter ${{chapter.Chapter}}: ${{chapter.TitleEN || ''}}</h2>
                ${{chapter.TitleKR ? `<p class="text-sm text-gray-600">${{chapter.TitleKR}}</p>` : ''}}
                ${{chapter.ChapterComment ? `
                <div class="mt-4 p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                    <p class="text-sm text-gray-700 whitespace-pre-line">${{chapter.ChapterComment}}</p>
                </div>` : ''}}
                <p class="text-gray-500 mt-6">No content available for this chapter.</p>
            </div>
        `;
        return;
    }}

    // 섹션별로 그룹화
    const sections = {{}};
    contents.forEach(content => {{
        const section = content.Section || 'General';
        if (!sections[section]) sections[section] = [];
        sections[section].push(content);
    }});

    // HTML 생성
    let html = `
        <div class="bg-white rounded-lg shadow-sm p-8 mb-6">
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-[#24305E] mb-2">Chapter ${{chapter.Chapter}}: ${{chapter.TitleEN || ''}}</h2>
                ${{chapter.TitleKR ? `<p class="text-sm text-gray-600">${{chapter.TitleKR}}</p>` : ''}}
            </div>
            ${{chapter.ChapterComment ? `
            <div class="mb-6 p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                <p class="text-sm text-gray-700 whitespace-pre-line">${{chapter.ChapterComment}}</p>
            </div>` : ''}}
    `;

    // 각 섹션 출력
    Object.keys(sections).sort((a, b) => parseFloat(a) - parseFloat(b)).forEach(sectionNum => {{
        const sectionContents = sections[sectionNum];
        const firstContent = sectionContents[0];

        html += `
            <div class="content-section mb-8">
                <h3 class="text-xl font-semibold text-[#374785] mb-3">Section ${{sectionNum}}${{firstContent.TitleEN ? ' - ' + firstContent.TitleEN : ''}}</h3>
                ${{firstContent.TitleKR ? `<p class="text-sm text-gray-500 mb-4">${{firstContent.TitleKR}}</p>` : ''}}
                <div class="space-y-4">
        `;

        // 각 subsection 출력
        sectionContents.forEach(content => {{
            const subsection = content.Subsection ? `.${{content.Subsection}}` : '';
            const sectionNumber = `${{sectionNum}}${{subsection}}`;

            // Attachments 찾기
            const attachments = getAttachments(versionId, content.Chapter, sectionNum, content.Subsection);

            html += `
                <div class="bg-gray-50 p-4 rounded-lg relative" id="section-${{sectionNumber.replace('.', '-')}}">
                    <div class="absolute top-3 right-3 flex items-center gap-1">
                        <button class="p-1.5 hover:bg-gray-200 rounded transition-colors" title="Copy link" onclick="copyLink('${{sectionNumber}}')">
                            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                            </svg>
                        </button>
                        <button class="p-1.5 hover:bg-gray-200 rounded transition-colors" title="Copy content" onclick="copyContent('${{sectionNumber}}')">
                            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                        </button>
                    </div>
                    <div class="flex items-center gap-2 mb-2">
                        <h4 class="font-semibold text-[#24305E]">${{sectionNumber}}${{content.TitleEN ? ' ' + content.TitleEN : ''}}</h4>
                    </div>
                    ${{content.ContentEN ? `<p class="text-gray-700 leading-relaxed mb-2">${{content.ContentEN}}</p>` : ''}}
                    ${{content.ContentKR ? `<p class="text-gray-600 text-sm leading-relaxed mb-3">${{content.ContentKR}}</p>` : ''}}
                    ${{content.Comment ? `
                    <div class="mt-3 pt-3 border-t border-gray-200 bg-[#FEE9EC] bg-opacity-30 p-3 rounded-lg">
                        <label class="text-xs font-semibold text-[#F76C6C] mb-1 block">Note</label>
                        <div class="w-full text-sm p-2 bg-white border border-[#F76C6C] border-opacity-20 rounded text-gray-700 whitespace-pre-line">
                            ${{content.Comment}}
                        </div>
                    </div>` : ''}}
                    ${{attachments.length > 0 ? `
                    <div class="mt-3 pt-3 border-t border-gray-200">
                        <div class="figures-scroll">
                            ${{attachments.map(att => `
                            <div class="border border-gray-300 rounded p-2 hover:border-[#A8D0E6] transition-colors cursor-pointer flex-shrink-0" style="min-width: 120px;" onclick="openAttachmentModal('${{att.AttachmentID}}')">
                                <div class="bg-gray-100 h-16 rounded flex items-center justify-center mb-1">
                                    <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${{att.Type.toLowerCase() === 'table' ? 'M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z' : 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'}}"></path>
                                    </svg>
                                </div>
                                <p class="text-xs font-medium text-gray-700 text-center">${{att.Type}} ${{att.Number || ''}}</p>
                            </div>
                            `).join('')}}
                        </div>
                    </div>` : ''}}
                </div>
            `;
        }});

        html += '</div></div>';
    }});

    html += '</div>';
    contentArea.innerHTML = html;
}}

// Attachment modal function
function openAttachmentModal(attachmentId) {{
    const attachment = appData.CodeAttachment.find(a => a.AttachmentID === attachmentId);
    if (!attachment) return;

    alert(`${{attachment.Type}} ${{attachment.Number || ''}}\\n${{attachment.AttachTitleEN || ''}}\\n${{attachment.AttachContentEN || 'Content not available'}}`);
}}

// Copy functions
function copyLink(sectionNumber) {{
    const url = window.location.href.split('#')[0] + '#section-' + sectionNumber.replace('.', '-');
    navigator.clipboard.writeText(url).then(() => {{
        alert('Link copied to clipboard!');
    }});
}}

function copyContent(sectionNumber) {{
    const element = document.getElementById('section-' + sectionNumber.replace('.', '-'));
    if (element) {{
        const text = element.innerText;
        navigator.clipboard.writeText(text).then(() => {{
            alert('Content copied to clipboard!');
        }});
    }}
}}

// Scroll to chapter function for pre-rendered content with header offset
function scrollToChapter(chapterId) {{
    const chapterElement = document.getElementById('chapter-' + chapterId);
    if (chapterElement) {{
        // Get the scrollable content container
        const contentContainer = document.querySelector('#librarySection .flex-1.overflow-y-auto');

        if (contentContainer) {{
            // Scroll within the content container
            const containerTop = contentContainer.scrollTop;
            const elementTop = chapterElement.offsetTop;

            contentContainer.scrollTo({{
                top: elementTop - 20, // 20px padding from top
                behavior: 'smooth'
            }});
        }} else {{
            // Fallback to window scroll if container not found
            const header = document.querySelector('#librarySection header');
            const headerHeight = header ? header.offsetHeight : 80;
            const elementPosition = chapterElement.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - headerHeight - 20;

            window.scrollTo({{
                top: offsetPosition,
                behavior: 'smooth'
            }});
        }}

        // Update active chapter in sidebar
        document.querySelectorAll('.chapter-item').forEach(item => {{
            item.classList.remove('active', 'bg-[#F8E9A1]');
        }});
        const activeItem = document.querySelector(`[data-chapter-id="${{chapterId}}"]`);
        if (activeItem) {{
            activeItem.classList.add('active', 'bg-[#F8E9A1]');
        }}
    }}
}}

// Toggle chapter sidebar sections
function toggleChapterSidebar(chapterId) {{
    const sectionsDiv = document.getElementById('sections-' + chapterId);
    const chevron = document.getElementById('chevron-' + chapterId);

    if (sectionsDiv && chevron) {{
        if (sectionsDiv.classList.contains('max-h-0')) {{
            sectionsDiv.classList.remove('max-h-0');
            sectionsDiv.classList.add('max-h-96');
            chevron.classList.add('rotate-180');
        }} else {{
            sectionsDiv.classList.remove('max-h-96');
            sectionsDiv.classList.add('max-h-0');
            chevron.classList.remove('rotate-180');
        }}
    }}

    // Also scroll to chapter
    scrollToChapter(chapterId);
}}

// Scroll to section with header offset
function scrollToSection(chapterId, sectionNum) {{
    const sectionElement = document.getElementById('section-' + chapterId + '-' + sectionNum);
    if (sectionElement) {{
        // Get the scrollable content container
        const contentContainer = document.querySelector('#librarySection .flex-1.overflow-y-auto');

        if (contentContainer) {{
            // Scroll within the content container
            const elementTop = sectionElement.offsetTop;

            contentContainer.scrollTo({{
                top: elementTop - 20, // 20px padding from top
                behavior: 'smooth'
            }});
        }} else {{
            // Fallback to window scroll if container not found
            const header = document.querySelector('#librarySection header');
            const headerHeight = header ? header.offsetHeight : 80;
            const elementPosition = sectionElement.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - headerHeight - 20;

            window.scrollTo({{
                top: offsetPosition,
                behavior: 'smooth'
            }});
        }}
    }}
}}

// Sidebar library submenu functions
function toggleLibrarySubmenu(event) {{
    event.stopPropagation();
    const submenu = document.getElementById('librarySubmenu');
    const chevron = document.getElementById('libraryChevron');

    if (submenu.style.maxHeight === '0px' || submenu.style.maxHeight === '') {{
        // 펼치기
        submenu.style.maxHeight = submenu.scrollHeight + 'px';
        chevron.style.transform = 'rotate(180deg)';
    }} else {{
        // 접기
        submenu.style.maxHeight = '0px';
        chevron.style.transform = 'rotate(0deg)';
    }}
}}

function loadCodeFromSidebar(versionId, codeId) {{
    switchToLibraryCode(codeId, versionId);
}}

function switchToLibraryCode(codeId, versionId) {{
    console.log('Switching to code:', codeId, 'version:', versionId);

    // Switch to library section
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    document.getElementById('librarySection').classList.add('active');

    // Update sidebar active state
    document.querySelectorAll('.sidebar-item').forEach(item => {{
        if (item.dataset.section === 'library') {{
            item.classList.add('active');
        }} else {{
            item.classList.remove('active');
        }}
    }});

    // Highlight selected submenu item
    document.querySelectorAll('.submenu-item').forEach(item => {{
        if (item.dataset.versionId === versionId) {{
            item.style.backgroundColor = '#374785';
        }} else {{
            item.style.backgroundColor = '';
        }}
    }});

    // Hide all code chapters and content
    document.querySelectorAll('.code-chapters').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.code-content').forEach(el => el.style.display = 'none');

    // Show selected code chapters and content
    const selectedChapters = document.getElementById('chapters-' + codeId);
    const selectedContent = document.getElementById('content-' + codeId);

    console.log('Chapters element:', selectedChapters);
    console.log('Content element:', selectedContent);

    if (selectedChapters) {{
        selectedChapters.style.display = 'block';
    }} else {{
        console.error('Chapters not found for codeId:', codeId);
    }}

    if (selectedContent) {{
        selectedContent.style.display = 'block';
    }} else {{
        console.error('Content not found for codeId:', codeId);
    }}

    // Update header with code info
    const modelCode = appData.ModelCode.find(mc => mc.ModelCodeID === codeId);
    const version = appData.ModelCodeVersion.find(v => v.ModelCodeVersionID === versionId);

    if (modelCode && version) {{
        const codeName = modelCode.ModelCodeName.split(':')[0].trim();
        const year = version.Year ? ' ' + Math.floor(version.Year) : '';
        document.getElementById('codeTitle').textContent = codeName + year;
        document.getElementById('codeSubtitle').textContent = modelCode.Description || '';
    }}

    // Reset scroll to top - both window and content container
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
    const contentContainer = document.querySelector('#librarySection .flex-1.overflow-y-auto');
    if (contentContainer) {{
        contentContainer.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
}}

// Search function for top search bar
function performTopSearch() {{
    const query = document.getElementById('topSearchInput').value.trim();
    if (!query) return;

    // Switch to search section
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    document.getElementById('searchSection').classList.add('active');

    // Update sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => item.classList.remove('active'));
    document.querySelector('.sidebar-item[data-section="search"]').classList.add('active');

    // Perform search across all codes with the keyword
    const modelCodeIds = new Set(['MC001', 'MC007', 'MC008', 'MC009']);
    const exactMatches = [];
    const partialMatches = [];
    const keyword = query.toLowerCase();

    appData.CodeContent.forEach(content => {{
        if (!modelCodeIds.has(content.ModelCodeID)) return;

        const titleEN = (content.TitleEN || '').toLowerCase();
        const titleKR = (content.TitleKR || '').toLowerCase();
        const contentEN = (content.ContentEN || '').toLowerCase();
        const contentKR = (content.ContentKR || '').toLowerCase();

        // Check if any field contains the keyword
        if (titleEN.includes(keyword) || titleKR.includes(keyword) ||
            contentEN.includes(keyword) || contentKR.includes(keyword)) {{

            // Get code info
            const modelCode = appData.ModelCode.find(mc => mc.ModelCodeID === content.ModelCodeID);
            const version = appData.ModelCodeVersion.find(v => v.ModelCodeVersionID === content.ModelCodeVersionID);
            const chapter = appData.CodeChapter.find(ch => ch.ChapterID === content.ChapterID);

            if (modelCode && version && chapter) {{
                const result = {{
                    code: modelCode.ModelCodeName.split(':')[0].trim(),
                    year: version.Year ? Math.floor(version.Year) : '',
                    chapter: chapter.Chapter,
                    chapterTitle: chapter.TitleEN || '',
                    section: content.Section || 'General',
                    subsection: content.Subsection || '',
                    titleEN: content.TitleEN || '',
                    titleKR: content.TitleKR || '',
                    contentEN: content.ContentEN || '',
                    contentKR: content.ContentKR || '',
                    codeId: content.ModelCodeID,
                    versionId: content.ModelCodeVersionID,
                    chapterId: content.ChapterID
                }};

                // Check for exact match
                const wordBoundaryRegex = new RegExp('\\\\b' + keyword.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + '\\\\b', 'i');
                const isExactMatch = wordBoundaryRegex.test(titleEN) || wordBoundaryRegex.test(titleKR) ||
                                   wordBoundaryRegex.test(contentEN) || wordBoundaryRegex.test(contentKR);

                if (isExactMatch) {{
                    exactMatches.push(result);
                }} else {{
                    partialMatches.push(result);
                }}
            }}
        }}
    }});

    // Display results
    displaySearchResults(exactMatches, partialMatches, [], keyword);

    // Clear the top search input
    document.getElementById('topSearchInput').value = '';
}}

function performSearch() {{
    // Get keyword from dynamic search input if it exists, otherwise use empty string
    const keywordInput = document.getElementById('dynamicKeywordInput');
    const keyword = keywordInput ? keywordInput.value.trim().toLowerCase() : '';

    const selectedArchCategories = Array.from(document.querySelectorAll('input[name="archCategory"]:checked')).map(cb => cb.value);
    const selectedFireCategories = Array.from(document.querySelectorAll('input[name="fireCategory"]:checked')).map(cb => cb.value);

    // Check if at least one filter is selected
    if (selectedArchCategories.length === 0 && selectedFireCategories.length === 0) {{
        alert('최소 하나의 필터를 선택해주세요');
        return;
    }}

    console.log('Searching for:', keyword || '(no keyword)');
    console.log('Arch categories:', selectedArchCategories);
    console.log('Fire categories:', selectedFireCategories);

    // Filter by selected codes
    let searchResults = [];
    let modelCodeIds = new Set();

    // Add codes based on selected categories
    if (selectedArchCategories.length > 0) {{
        selectedArchCategories.forEach(cat => {{
            if (cat === 'IBC') modelCodeIds.add('MC001');
        }});
    }}
    if (selectedFireCategories.length > 0) {{
        selectedFireCategories.forEach(cat => {{
            if (cat === 'NFPA13') modelCodeIds.add('MC007');
            if (cat === 'NFPA14') modelCodeIds.add('MC008');
            if (cat === 'NFPA20') modelCodeIds.add('MC009');
        }});
    }}

    // If no categories selected, search all
    if (modelCodeIds.size === 0) {{
        modelCodeIds = new Set(['MC001', 'MC007', 'MC008', 'MC009']);
    }}

    // Search in CodeContent - separate exact and partial matches
    const exactMatches = [];
    const partialMatches = [];
    const allFilteredResults = [];

    appData.CodeContent.forEach(content => {{
        if (!modelCodeIds.has(content.ModelCodeID)) return;

        // Get code info first
        const modelCode = appData.ModelCode.find(mc => mc.ModelCodeID === content.ModelCodeID);
        const version = appData.ModelCodeVersion.find(v => v.ModelCodeVersionID === content.ModelCodeVersionID);
        const chapter = appData.CodeChapter.find(ch => ch.ChapterID === content.ChapterID);

        if (modelCode && version && chapter) {{
            const result = {{
                code: modelCode.ModelCodeName.split(':')[0].trim(),
                year: version.Year ? Math.floor(version.Year) : '',
                chapter: chapter.Chapter,
                chapterTitle: chapter.TitleEN || '',
                section: content.Section || 'General',
                subsection: content.Subsection || '',
                titleEN: content.TitleEN || '',
                titleKR: content.TitleKR || '',
                contentEN: content.ContentEN || '',
                contentKR: content.ContentKR || '',
                codeId: content.ModelCodeID,
                versionId: content.ModelCodeVersionID,
                chapterId: content.ChapterID
            }};

            // If keyword is provided, filter by keyword
            if (keyword) {{
                const titleEN = (content.TitleEN || '').toLowerCase();
                const titleKR = (content.TitleKR || '').toLowerCase();
                const contentEN = (content.ContentEN || '').toLowerCase();
                const contentKR = (content.ContentKR || '').toLowerCase();

                // Check if any field contains the keyword
                if (titleEN.includes(keyword) || titleKR.includes(keyword) ||
                    contentEN.includes(keyword) || contentKR.includes(keyword)) {{

                    // Check for exact match (keyword as whole word)
                    const wordBoundaryRegex = new RegExp('\\\\b' + keyword.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + '\\\\b', 'i');
                    const isExactMatch = wordBoundaryRegex.test(titleEN) || wordBoundaryRegex.test(titleKR) ||
                                       wordBoundaryRegex.test(contentEN) || wordBoundaryRegex.test(contentKR);

                    if (isExactMatch) {{
                        exactMatches.push(result);
                    }} else {{
                        partialMatches.push(result);
                    }}
                }}
            }} else {{
                // No keyword - just filter by category
                allFilteredResults.push(result);
            }}
        }}
    }});

    // Display results with exact matches first
    displaySearchResults(exactMatches, partialMatches, allFilteredResults, keyword);
}}

// Helper function to highlight keyword in text - with different colors for exact vs partial
function highlightKeyword(text, keyword, isExactMatch) {{
    if (!text || !keyword) return text;

    // Escape special regex characters in keyword
    const escapeRegex = (str) => str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
    const escapedKeyword = escapeRegex(keyword);

    // Create regex for case-insensitive matching
    const regex = new RegExp(`(${{escapedKeyword}})`, 'gi');

    // Different highlight colors: exact match = yellow, partial match = light blue
    const highlightClass = isExactMatch ? 'bg-yellow-200 font-semibold' : 'bg-blue-200 font-medium';

    // Replace matches with highlighted spans
    return text.replace(regex, `<mark class="${{highlightClass}}">$1</mark>`);
}}

function displaySearchResults(exactMatches, partialMatches, allFilteredResults, keyword) {{
    const resultsList = document.getElementById('resultsList');
    const resultsSection = document.getElementById('resultsSection');

    const totalResults = exactMatches.length + partialMatches.length + allFilteredResults.length;

    if (totalResults === 0) {{
        resultsList.innerHTML = '<p class="text-gray-500 text-center py-8">검색 결과가 없습니다</p>';
        // Hide keyword search input when no results
        const existingKeywordSearch = document.getElementById('dynamicKeywordSearch');
        if (existingKeywordSearch) existingKeywordSearch.style.display = 'none';
        return;
    }}

    // Add dynamic keyword search input if results exist
    let keywordSearchHTML = document.getElementById('dynamicKeywordSearch');
    if (!keywordSearchHTML) {{
        // Create the keyword search input section
        keywordSearchHTML = document.createElement('div');
        keywordSearchHTML.id = 'dynamicKeywordSearch';
        keywordSearchHTML.className = 'mb-4 p-4 bg-gray-50 rounded-lg';
        keywordSearchHTML.innerHTML = `
            <label class="block text-sm font-semibold text-[#24305E] mb-2">결과 내 키워드 검색</label>
            <div class="relative max-w-xl">
                <input
                    type="text"
                    id="dynamicKeywordInput"
                    placeholder="검색 결과 중에서 키워드 검색..."
                    class="w-full px-4 py-3 pr-20 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-[#A8D0E6] transition-colors"
                >
                <button
                    class="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 bg-[#F76C6C] hover:bg-[#e55a5a] rounded transition-colors"
                    onclick="performSearch()"
                >
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                    </svg>
                </button>
            </div>
        `;
        // Insert before resultsList
        resultsList.parentNode.insertBefore(keywordSearchHTML, resultsList);

        // Add enter key support for dynamic keyword input
        setTimeout(() => {{
            const input = document.getElementById('dynamicKeywordInput');
            if (input) {{
                input.addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') performSearch();
                }});
            }}
        }}, 100);
    }} else {{
        keywordSearchHTML.style.display = 'block';
    }}

    let html = '<div class="space-y-4">';

    // Display exact matches first
    if (exactMatches.length > 0) {{
        html += '<div class="mb-6"><h3 class="text-lg font-semibold text-[#24305E] mb-3 flex items-center"><svg class="w-5 h-5 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>정확히 일치하는 결과 (${{exactMatches.length}})</h3>';

        exactMatches.forEach((result, index) => {{
            const sectionNum = result.section + (result.subsection ? '.' + result.subsection : '');

            // Highlight keyword in all text fields - exact match color
            const highlightedTitleEN = highlightKeyword(result.titleEN, keyword, true);
            const highlightedTitleKR = highlightKeyword(result.titleKR, keyword, true);
            const highlightedContentEN = highlightKeyword(result.contentEN, keyword, true);
            const highlightedContentKR = highlightKeyword(result.contentKR, keyword, true);

            html += `
                <div class="bg-white rounded-lg border-2 border-green-200 p-4 hover:border-[#A8D0E6] transition-colors cursor-pointer"
                     onclick="openSearchResultModal(${{JSON.stringify(result).replace(/"/g, '&quot;')}})">
                    <div class="flex items-start justify-between mb-2">
                        <div>
                            <span class="text-xs font-medium text-[#A8D0E6] bg-[#A8D0E6] bg-opacity-20 px-2 py-1 rounded">
                                ${{result.code}} ${{result.year}}
                            </span>
                            <span class="text-xs text-gray-500 ml-2">Chapter ${{result.chapter}}: ${{result.chapterTitle}}</span>
                        </div>
                        <span class="text-sm font-semibold text-[#24305E]">Section ${{sectionNum}}</span>
                    </div>
                    <h4 class="font-semibold text-[#24305E] mb-1">${{highlightedTitleEN}}</h4>
                    <p class="text-sm text-gray-600 mb-2">${{highlightedTitleKR}}</p>
                    <p class="text-sm text-gray-700 line-clamp-2">${{highlightedContentEN}}</p>
                    <p class="text-xs text-gray-500 line-clamp-1 mt-1">${{highlightedContentKR}}</p>
                </div>
            `;
        }});
        html += '</div>';
    }}

    // Display partial matches
    if (partialMatches.length > 0) {{
        html += '<div class="mb-6"><h3 class="text-lg font-semibold text-[#24305E] mb-3 flex items-center"><svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path></svg>관련 검색 결과 (${{partialMatches.length}})</h3>';

        partialMatches.forEach((result, index) => {{
            const sectionNum = result.section + (result.subsection ? '.' + result.subsection : '');

            // Highlight keyword in all text fields - partial match color
            const highlightedTitleEN = highlightKeyword(result.titleEN, keyword, false);
            const highlightedTitleKR = highlightKeyword(result.titleKR, keyword, false);
            const highlightedContentEN = highlightKeyword(result.contentEN, keyword, false);
            const highlightedContentKR = highlightKeyword(result.contentKR, keyword, false);

            html += `
                <div class="bg-white rounded-lg border border-gray-200 p-4 hover:border-[#A8D0E6] transition-colors cursor-pointer"
                     onclick="openSearchResultModal(${{JSON.stringify(result).replace(/"/g, '&quot;')}})">
                    <div class="flex items-start justify-between mb-2">
                        <div>
                            <span class="text-xs font-medium text-[#A8D0E6] bg-[#A8D0E6] bg-opacity-20 px-2 py-1 rounded">
                                ${{result.code}} ${{result.year}}
                            </span>
                            <span class="text-xs text-gray-500 ml-2">Chapter ${{result.chapter}}: ${{result.chapterTitle}}</span>
                        </div>
                        <span class="text-sm font-semibold text-[#24305E]">Section ${{sectionNum}}</span>
                    </div>
                    <h4 class="font-semibold text-[#24305E] mb-1">${{highlightedTitleEN}}</h4>
                    <p class="text-sm text-gray-600 mb-2">${{highlightedTitleKR}}</p>
                    <p class="text-sm text-gray-700 line-clamp-2">${{highlightedContentEN}}</p>
                    <p class="text-xs text-gray-500 line-clamp-1 mt-1">${{highlightedContentKR}}</p>
                </div>
            `;
        }});
        html += '</div>';
    }}

    // Display filtered results (no keyword)
    if (allFilteredResults.length > 0) {{
        html += '<div class="mb-6"><h3 class="text-lg font-semibold text-[#24305E] mb-3 flex items-center"><svg class="w-5 h-5 mr-2 text-gray-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clip-rule="evenodd"></path></svg>필터 검색 결과 (${{allFilteredResults.length}})</h3>';

        allFilteredResults.forEach((result, index) => {{
            const sectionNum = result.section + (result.subsection ? '.' + result.subsection : '');

            html += `
                <div class="bg-white rounded-lg border border-gray-200 p-4 hover:border-[#A8D0E6] transition-colors cursor-pointer"
                     onclick="openSearchResultModal(${{JSON.stringify(result).replace(/"/g, '&quot;')}})">
                    <div class="flex items-start justify-between mb-2">
                        <div>
                            <span class="text-xs font-medium text-[#A8D0E6] bg-[#A8D0E6] bg-opacity-20 px-2 py-1 rounded">
                                ${{result.code}} ${{result.year}}
                            </span>
                            <span class="text-xs text-gray-500 ml-2">Chapter ${{result.chapter}}: ${{result.chapterTitle}}</span>
                        </div>
                        <span class="text-sm font-semibold text-[#24305E]">Section ${{sectionNum}}</span>
                    </div>
                    <h4 class="font-semibold text-[#24305E] mb-1">${{result.titleEN}}</h4>
                    <p class="text-sm text-gray-600 mb-2">${{result.titleKR}}</p>
                    <p class="text-sm text-gray-700 line-clamp-2">${{result.contentEN}}</p>
                    <p class="text-xs text-gray-500 line-clamp-1 mt-1">${{result.contentKR}}</p>
                </div>
            `;
        }});
        html += '</div>';
    }}

    html += '</div>';

    resultsList.innerHTML = html;
}}

// Open search result in modal popup
function openSearchResultModal(result) {{
    // Create modal if it doesn't exist
    let modal = document.getElementById('searchResultModal');
    if (!modal) {{
        modal = document.createElement('div');
        modal.id = 'searchResultModal';
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center hidden';
        modal.innerHTML = `
            <div class="bg-white rounded-lg shadow-2xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-hidden">
                <div class="flex items-center justify-between p-6 border-b border-gray-200">
                    <div class="flex-1">
                        <h2 id="modalTitle" class="text-2xl font-bold text-[#24305E]"></h2>
                        <p id="modalLocation" class="text-sm text-gray-500 mt-1"></p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button
                            onclick="navigateToLibraryFromModal()"
                            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                            title="라이브러리에서 보기"
                        >
                            <svg class="w-6 h-6 text-[#F76C6C]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                            </svg>
                        </button>
                        <button
                            onclick="closeSearchResultModal()"
                            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                            <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                </div>
                <div id="modalContent" class="p-6 overflow-y-auto max-h-[calc(90vh-100px)]"></div>
            </div>
        `;
        document.body.appendChild(modal);

        // Close modal when clicking outside
        modal.addEventListener('click', function(e) {{
            if (e.target === modal) {{
                closeSearchResultModal();
            }}
        }});
    }}

    // Store current result for navigation
    window.currentModalResult = result;

    // Populate modal with result data
    const sectionNum = result.section + (result.subsection ? '.' + result.subsection : '');
    document.getElementById('modalTitle').textContent = sectionNum + (result.titleEN ? ' ' + result.titleEN : '');
    document.getElementById('modalLocation').textContent = `${{result.code}} ${{result.year}} - Chapter ${{result.chapter}}: ${{result.chapterTitle}}`;

    let contentHTML = '';
    if (result.titleKR) {{
        contentHTML += `<p class="text-lg text-gray-700 font-semibold mb-4">${{result.titleKR}}</p>`;
    }}
    if (result.contentEN) {{
        contentHTML += `<div class="mb-4"><h3 class="text-sm font-semibold text-gray-500 uppercase mb-2">English</h3><p class="text-gray-800 leading-relaxed whitespace-pre-wrap">${{result.contentEN}}</p></div>`;
    }}
    if (result.contentKR) {{
        contentHTML += `<div class="mb-4"><h3 class="text-sm font-semibold text-gray-500 uppercase mb-2">한국어</h3><p class="text-gray-700 leading-relaxed whitespace-pre-wrap">${{result.contentKR}}</p></div>`;
    }}

    document.getElementById('modalContent').innerHTML = contentHTML;

    // Show modal
    modal.classList.remove('hidden');
}}

function closeSearchResultModal() {{
    const modal = document.getElementById('searchResultModal');
    if (modal) {{
        modal.classList.add('hidden');
    }}
}}

function navigateToLibraryFromModal() {{
    if (window.currentModalResult) {{
        const result = window.currentModalResult;
        closeSearchResultModal();

        // Switch to library and load the code
        switchToLibraryCode(result.codeId, result.versionId);

        // Scroll to the section after a short delay
        setTimeout(() => {{
            scrollToSection(result.chapterId, result.section);
        }}, 500);
    }}
}}

function openSearchResult(codeId, versionId, chapterId, section) {{
    // Switch to library and load the code
    switchToLibraryCode(codeId, versionId);

    // Scroll to the section after a short delay
    setTimeout(() => {{
        scrollToSection(chapterId, section);
    }}, 500);
}}

function clearSearchInput() {{
    document.getElementById('topSearchInput').value = '';
}}

// === Page Initialization ===
document.addEventListener('DOMContentLoaded', function() {{
    console.log('US Code Navigator initialized with schema-based hierarchy');
    console.log('Loaded data:', appData);

    // Library card click handlers
    document.querySelectorAll('.code-card[data-version-id]').forEach(card => {{
        card.addEventListener('click', function() {{
            const versionId = this.dataset.versionId;
            const codeId = this.dataset.codeId;

            // Switch to library code
            switchToLibraryCode(codeId, versionId);
        }});
    }});

    // Sidebar navigation
    document.querySelectorAll('.sidebar-item').forEach(item => {{
        item.addEventListener('click', function() {{
            const section = this.dataset.section;

            // Update active state
            document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            // Show corresponding section
            document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
            document.getElementById(section + 'Section').classList.add('active');
        }});
    }});

    // Feature card navigation
    document.querySelectorAll('.feature-card[data-nav]').forEach(card => {{
        card.addEventListener('click', function() {{
            const section = this.dataset.nav;
            document.querySelector(`.sidebar-item[data-section="${{section}}"]`).click();
        }});
    }});

    // Search button click handler
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {{
        searchBtn.addEventListener('click', performSearch);
    }}

    // Reset button for advanced search
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {{
        resetBtn.addEventListener('click', function() {{
            document.getElementById('keywordInput').value = '';
            document.querySelectorAll('input[name="archCategory"]:checked').forEach(cb => cb.checked = false);
            document.querySelectorAll('input[name="fireCategory"]:checked').forEach(cb => cb.checked = false);
            document.getElementById('selectAllArch').checked = false;
            document.getElementById('selectAllFire').checked = false;
            document.getElementById('resultsList').innerHTML = '';
        }});
    }}

    // Enter key in search inputs
    const keywordInput = document.getElementById('keywordInput');
    if (keywordInput) {{
        keywordInput.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') performSearch();
        }});
    }}

    const topSearchInput = document.getElementById('topSearchInput');
    if (topSearchInput) {{
        topSearchInput.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') performTopSearch();
        }});
    }}
}});
    '''

    # script를 body 끝에 추가
    body_tag = soup.find('body')
    if body_tag:
        body_tag.append(script_tag)

    return str(soup)

def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("US Code Navigator - Schema-based HTML Generator")
    print("=" * 70)

    # 스키마 로드
    schema = load_schema()

    # JSON 데이터 로드
    data = load_json_data()

    # 데이터 계층 구조 생성
    print("\nBuilding data hierarchy from schema...")
    hierarchy = DataHierarchy(schema, data)
    print(f"✓ Data hierarchy built with {len(hierarchy.relationships)} table relationships")

    # HTML 생성
    print("\nGenerating HTML...")
    final_html = generate_html(hierarchy)

    # HTML 파일 저장
    print(f"\nWriting HTML to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("=" * 70)
    print(f"✓ Success! HTML file generated: {OUTPUT_FILE}")
    print(f"✓ All JSON data integrated with schema-based relationships")
    print("=" * 70)

if __name__ == "__main__":
    main()
