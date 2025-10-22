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

        cards_html.append(card_html)

    return '\n'.join(cards_html)

def escape_js_string(s):
    """JavaScript 문자열을 이스케이프합니다."""
    if not s:
        return ''
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')

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
        if latest_version.get('Year'):
            year = int(latest_version['Year'])
            display_name = f"{code_name.split(':')[0].strip()} {year}"
        else:
            display_name = code_name.split(':')[0].strip()

        submenu_html = f'''
        <div class="submenu-item pl-12 py-2 text-sm text-white hover:bg-[#374785] cursor-pointer transition-all rounded-r-lg"
             data-code-id="{model_code_id}"
             data-version-id="{latest_version['ModelCodeVersionID']}"
             onclick="loadCodeFromSidebar('{latest_version['ModelCodeVersionID']}', '{model_code_id}')">
            <span>{display_name}</span>
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
        # 라이브러리 메뉴 항목 찾기
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

    # 라이브러리 섹션의 하드코딩된 챕터 리스트와 콘텐츠를 실제 데이터로 교체
    print("Replacing library section content with actual data...")
    library_section = soup.find('div', id='librarySection')
    if library_section:
        # 챕터 리스트를 비우고 초기 메시지 추가
        chapter_list = library_section.find('div', id='chapterList')
        if chapter_list:
            chapter_list.clear()
            placeholder = soup.new_tag('p', **{'class': 'text-gray-500 text-sm p-4'})
            placeholder.string = 'Select a code from the library to view chapters'
            chapter_list.append(placeholder)
            print("✓ Chapter list cleared, ready for dynamic loading")

        # 콘텐츠 영역을 비우고 초기 메시지 추가
        content_area = library_section.find('div', id='contentArea')
        if content_area:
            content_area.clear()
            welcome_html = '''
            <div class="bg-white rounded-lg shadow-sm p-8 text-center">
                <div class="max-w-2xl mx-auto">
                    <svg class="w-24 h-24 mx-auto mb-6 text-[#A8D0E6]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                    <h2 class="text-3xl font-bold text-[#24305E] mb-4">Welcome to US Code Navigator</h2>
                    <p class="text-gray-600 text-lg mb-6">Select a code from the home page library to browse chapters and content</p>
                    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded text-left">
                        <p class="text-sm text-gray-700"><strong>Available Codes:</strong></p>
                        <ul class="text-sm text-gray-700 mt-2 space-y-1">
                            <li>• IBC 2024 - International Building Code</li>
                            <li>• NFPA 13 2025 - Sprinkler Systems</li>
                            <li>• NFPA 14 2024 - Standpipe Systems</li>
                            <li>• NFPA 20 2025 - Fire Pumps</li>
                        </ul>
                    </div>
                </div>
            </div>
            '''
            welcome_soup = BeautifulSoup(welcome_html, 'lxml')
            for child in welcome_soup.find('div').children:
                content_area.append(child)
            print("✓ Content area cleared and welcome message added")

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

    // Load chapters
    loadChapters(versionId, codeId);
}}

// Search function
function performTopSearch() {{
    const query = document.getElementById('topSearchInput').value.trim();
    if (!query) return;

    // Switch to search section
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    document.getElementById('searchSection').classList.add('active');

    // Update sidebar
    document.querySelectorAll('.sidebar-item').forEach(item => item.classList.remove('active'));
    document.querySelector('.sidebar-item[data-section="search"]').classList.add('active');

    // Set search input
    document.getElementById('keywordInput').value = query;

    // Perform search (to be implemented)
    alert('Search functionality: ' + query);
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

            // Switch to library section
            document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
            document.getElementById('librarySection').classList.add('active');

            // Update sidebar
            document.querySelectorAll('.sidebar-item').forEach(item => item.classList.remove('active'));
            document.querySelector('.sidebar-item[data-section="library"]').classList.add('active');

            // Load chapters
            loadChapters(versionId, codeId);
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

    // Auto-load first available code on page load (optional - only if on library section)
    const currentSection = document.querySelector('.section-content.active');
    if (currentSection && currentSection.id === 'librarySection') {{
        const firstActiveCard = document.querySelector('.code-card[data-version-id]');
        if (firstActiveCard) {{
            const versionId = firstActiveCard.dataset.versionId;
            const codeId = firstActiveCard.dataset.codeId;
            loadChapters(versionId, codeId);
        }}
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
