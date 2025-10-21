# US Code Navigator

A professional, modern web application for searching, displaying, and comparing US building codes and standards (IBC, NFPA, etc.).

## Features

### 1. **Home Page**
- **Advanced Search**: Quick access to filtered search with multiple criteria
- **Featured Codes**: Direct access to commonly used codes (IBC 2024, NFPA 13, NFPA 20, NFPA 72)
- **Global Search Bar**: Search across all codes from any page

### 2. **코드 (Code) Section**
- Dropdown navigation showing all available codes
- Click to view full code content with all sections
- Organized by sections with formatted text display
- Easy navigation between different code standards

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

## Technical Implementation

### Structure
- **Single HTML File**: Easy deployment to Confluence or any web platform
- **Embedded CSS**: No external stylesheets required
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Works on desktop and mobile devices

### Key Functions

#### Navigation
- `navigateToPage(page)`: Switch between main pages
- `viewCode(codeId)`: Display specific code content
- `toggleDropdown()`: Show/hide code dropdown menu

#### Search
- `performGlobalSearch(query)`: Quick search from header
- `performAdvancedSearch()`: Filter-based search
- `searchCodes(filters)`: Search algorithm with multiple filters
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
