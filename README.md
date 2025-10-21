# US Code Navigator

A professional, modern web application for searching, displaying, and comparing US building codes and standards (IBC, NFPA, etc.).

**Now with Real Data Integration!** This application includes actual code content from:
- IBC (International Building Code) 2021 & 2024
- NFPA 13 (Sprinkler Systems) 2025
- NFPA 14 (Standpipe Systems) 2024
- NFPA 20 (Fire Pumps) 2025
- NFPA 72 (Fire Alarm Systems)
- And more!

**Bilingual Support:** All content available in both English and Korean with easy language toggle.

**NEW! Enhanced Navigation:** Table of Contents panel, Bookmarks, History tracking, and more professional features.

## Features

### 1. **Home Page**
- **Advanced Search**: Quick access to filtered search with multiple criteria
- **Featured Codes**: Direct access to commonly used codes (IBC 2024, NFPA 13, NFPA 20, NFPA 72)
- **Global Search Bar**: Search across all codes from any page

### 2. **코드 (Code) Section** - Now with Enhanced Navigation!
- Dropdown navigation showing all available codes (dynamically populated from database)
- Click to view full code content with all sections and chapters
- **📑 Table of Contents Panel**:
  - Collapsible chapter/section tree view
  - Click any item to jump instantly
  - Reading progress indicator
  - Toggleable via button or FAB
- **⭐ Bookmarks System**:
  - Star any section for quick access
  - Bookmark manager with easy removal
  - Persistent across sessions
- **🕐 Recent History**:
  - Automatically tracks last 20 viewed sections
  - Time-ago display (e.g., "5 min ago")
  - Quick navigation to previous sections
- **🧭 Breadcrumb Navigation**:
  - Shows current location path
  - Each level clickable
  - Context-aware display
- **Section Toolbars**:
  - Bookmark button per section
  - Share link generation
  - Print button
- **Bilingual content**: Toggle between English and Korean
- **Smart Auto-Linking**: Automatic hyperlinks for Chapter and Section references
  - Internal links jump to referenced sections within the same code
  - External links search Google when section doesn't exist
  - Smooth scrolling with visual highlighting
- Easy navigation between different code standards
- Chapter comments and notes included where available

### 3. **검색 (Search) - Advanced Search**
Multiple filter options:
- **Code Type**: Filter by IBC, NFPA, IFC
- **Year**: Filter by publication year (2024, 2021, 2018, 2015)
- **Category**: Filter by category (Fire Protection, Building Construction, etc.)
- **Section Number**: Search specific sections (e.g., 903.3.1)
- **Keyword**: Search by keywords
- **Full Text Search**: Search within code content

Search results include:
- Highlighted search terms
- Code title and section information
- Content snippets
- Click-to-view functionality

### 4. **비교 (Compare) - Code Comparison**
- Select two codes to compare side-by-side
- Specify sections for detailed comparison
- Automatic diff highlighting:
  - **Green**: Content unique to first code
  - **Red**: Content unique to second code
  - **Yellow**: Modified content
- Visual side-by-side display

## Design Features

### Color Palette
- Primary Blue: #149CDC
- Dark Blue: #0C5484
- Charcoal: #2C4B5C
- Light Gray: #E3E9EF
- Medium Blue: #ACC9DB

### UI/UX Features
- Professional gradient header
- Sticky navigation sidebar
- Smooth transitions and animations
- Hover effects on interactive elements
- Responsive design for various screen sizes
- Modern card-based layouts
- Shadow effects for depth
- Rounded corners for modern aesthetic

## Included Code Standards

### IBC 2024 (International Building Code)
- Section 903.3.1: NFPA 13 Installation
- Section 1003.2: Ceiling Height

### NFPA 13 (Sprinkler Systems)
- Section 8.3.1: Sprinkler Spacing
- Section 10.1: Water Supply Requirements

### NFPA 20 (Fire Pumps)
- Section 4.8: Pump Room Requirements
- Section 4.14: Controllers

### NFPA 72 (Fire Alarm Systems)
- Section 17.4: Smoke Detector Spacing
- Section 23.8: Fire Alarm Control Units

## Data Structure & JSON Files

The application uses a relational data model with the following JSON files:

### Core Schema Files
- **`schema-meta.json`**: Complete database schema definition with tables, relationships, and foreign keys
- **`CodeType.json`**: Code type classifications (Model Code, Jurisdiction, etc.)
- **`ModelCode.json`**: Model code definitions (IBC, NFPA 13, NFPA 20, etc.)
- **`ModelCodeVersion.json`**: Version information for each code (year, edition)
- **`Discipline.json`**: Engineering disciplines (Arch/Struct, MEP, Electrical, Fire, EHS)

### Content Files
- **`CodeChapter.json`**: Chapter information for each code version (bilingual titles, comments)
- **`CodeContent.json`**: **Main content file (722KB)** - Full text of all code sections in English and Korean
- **`CodeAttachment.json`**: Attachments and supplementary materials
- **`Jurisdiction.json`**: US state jurisdictions
- **`ModelCodeDiscipline.json`**: Mapping between codes and disciplines

### Data Integration
All JSON data is **embedded directly into the HTML file** for Confluence compatibility. The application:
1. Loads all JSON data on startup (~900KB total)
2. Builds a searchable code database with proper relationships
3. Dynamically populates dropdowns, featured codes, and navigation
4. Supports bilingual content switching
5. Enables fast client-side search and filtering

## Technical Implementation

### Structure
- **Single HTML File**: Easy deployment to Confluence or any web platform
- **Embedded CSS**: No external stylesheets required
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Works on desktop and mobile devices

### Key Functions

#### Data Processing
- `buildCodeDatabase()`: Builds searchable database from JSON data with proper relationships
- `toggleLanguage()`: Switches between English and Korean content
- `getText(section, field)`: Gets text in current language

#### Navigation
- `navigateToPage(page)`: Switch between main pages
- `viewCode(codeId)`: Display specific code content with bilingual support and auto-linking
- `toggleDropdown()`: Show/hide code dropdown menu
- `scrollToSection(sectionKey)`: Smooth scroll to referenced section with highlight animation

#### Auto-Linking
- `autoLinkReferences(text, code, sectionKey)`: Automatically creates links for Chapter/Section references
- Supports internal navigation and external Google searches
- Pattern matching for "Chapter X" and "Section X.X.X" formats

#### Bookmarks & History
- `toggleBookmark(codeId, sectionKey, title)`: Add/remove bookmark for a section
- `isBookmarked(codeId, sectionKey)`: Check if section is bookmarked
- `addToHistory(codeId, sectionKey, title)`: Track viewed sections
- `updateBookmarksUI()`: Refresh bookmarks panel display
- `updateHistoryUI()`: Refresh history panel display
- `navigateToBookmark(codeId, sectionKey)`: Jump to bookmarked section

#### Table of Contents
- `buildTOC(code)`: Generate interactive TOC from code structure
- `toggleTOC()`: Show/hide TOC panel
- `toggleTOCChapter(element)`: Expand/collapse chapter sections
- `updateScrollProgress()`: Track and display reading progress

#### Breadcrumb
- `updateBreadcrumb(codeId, sectionKey)`: Update navigation path display

#### Data Persistence
- `AppStorage.get(key, defaultValue)`: Retrieve from LocalStorage
- `AppStorage.set(key, value)`: Save to LocalStorage
- `AppStorage.remove(key)`: Delete from LocalStorage

#### Search
- `performGlobalSearch(query)`: Quick search from header
- `performAdvancedSearch()`: Filter-based search
- `searchCodes(filters)`: Search algorithm supporting bilingual content
- `displaySearchResults(results, searchTerm)`: Render search results with highlighting

#### Comparison
- `performComparison()`: Compare two selected codes
- `displayComparison()`: Show side-by-side comparison
- `highlightDifferences()`: Diff algorithm for highlighting changes

### Data Structure
```javascript
codeDatabase = {
    codeId: {
        id: 'unique-id',
        title: 'Full Code Title',
        year: 'Publication Year',
        category: 'Code Category',
        sections: {
            'sectionNumber': {
                title: 'Section Title',
                content: 'Full section text',
                type: 'Section Type',
                keywords: ['keyword1', 'keyword2']
            }
        }
    }
}
```

## Usage Instructions

### For Confluence WIKI

1. **Upload Method**:
   - Open Confluence page editor
   - Insert > Other Macros > HTML
   - Paste the entire content of `us-code-navigator.html`
   - Save and publish

2. **As Attachment**:
   - Attach `us-code-navigator.html` to Confluence page
   - Create link to open in new window
   - Users can download and open locally

### For Web Server

1. Upload `us-code-navigator.html` to your web server
2. Access via direct URL
3. No additional setup required

### Adding New Codes

To add new code standards, edit the `codeDatabase` object:

```javascript
codeDatabase.newcode = {
    id: 'newcode',
    title: 'New Code Title',
    year: '2024',
    category: 'Category Name',
    sections: {
        '1.1': {
            title: 'Section Title',
            content: 'Section content here...',
            type: 'Section Type',
            keywords: ['keyword1', 'keyword2']
        }
    }
};
```

Then add to dropdown menu:
```html
<div class="dropdown-item" data-code="newcode">New Code</div>
```

And featured codes (optional):
```html
<div class="code-card" onclick="viewCode('newcode')">
    <h3>New Code</h3>
    <p>Description</p>
    <span class="code-badge">Category</span>
</div>
```

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- IE11: Not supported (uses modern CSS features)

## Performance

- Lightweight: Single file, ~50KB
- Fast loading: No external dependencies
- Efficient search: Client-side filtering
- Smooth animations: CSS transitions

## Future Enhancements

Potential additions:
- Export search results to PDF/Excel
- Bookmark favorite sections
- Print-friendly version
- Dark mode toggle
- More code standards (IFC, IMC, IECC, etc.)
- Version comparison (e.g., IBC 2024 vs IBC 2021)
- User annotations and notes
- Share links to specific sections

## Support

For issues or questions:
- Check the inline code comments
- Review the data structure examples
- Ensure browser compatibility

## License

This project is designed for internal use. Ensure compliance with code publisher licensing when using actual code content.

## Credits

Developed for professional code navigation and comparison.
Color scheme designed for optimal readability and professional appearance.
