# US Code Navigator - Feature Reference

## Key Functions Overview

### Navigation Functions

#### 1. `navigateToPage(page)`
Switches between main application pages.

**Parameters:**
- `page` (string): Page identifier ('home', 'code', 'search', 'compare')

**Usage:**
```javascript
navigateToPage('search'); // Navigate to search page
navigateToPage('home');   // Navigate to home page
```

**Behavior:**
- Hides all pages
- Shows selected page with fade-in animation
- Updates sidebar navigation active state
- Closes dropdown menu if open

---

#### 2. `viewCode(codeId)`
Displays full content of a selected code standard.

**Parameters:**
- `codeId` (string): Code identifier ('ibc', 'nfpa13', 'nfpa20', 'nfpa72')

**Usage:**
```javascript
viewCode('ibc');    // Display IBC 2024
viewCode('nfpa13'); // Display NFPA 13
```

**Behavior:**
- Loads code metadata (title, year, category)
- Renders all sections with formatted content
- Navigates to code page
- Updates dropdown selection state

---

#### 3. `toggleDropdown()`
Shows/hides the code dropdown menu.

**Usage:**
```javascript
toggleDropdown(); // Toggle dropdown visibility
```

**Behavior:**
- Toggles 'open' class on dropdown
- Rotates arrow icon
- Smooth height transition

---

### Search Functions

#### 4. `performGlobalSearch(query)`
Executes quick search from header search bar.

**Parameters:**
- `query` (string): Search term

**Usage:**
```javascript
performGlobalSearch('sprinkler'); // Search for 'sprinkler'
```

**Behavior:**
- Navigates to search page
- Populates full text search field
- Executes detailed search automatically

---

#### 5. `performAdvancedSearch()`
Executes search from home page with filters.

**Behavior:**
- Reads filter values from home page
- Navigates to search page
- Transfers filters to search page
- Executes detailed search

---

#### 6. `performDetailedSearch()`
Main search function with all filters.

**Filter Parameters:**
- `codeType`: Filter by code type (ibc, nfpa, ifc)
- `year`: Filter by publication year
- `category`: Filter by category
- `section`: Filter by section number
- `keyword`: Search in keywords and titles
- `fullText`: Search in content text

**Behavior:**
- Collects all filter values
- Calls `searchCodes()` algorithm
- Displays results with highlighting

---

#### 7. `searchCodes(filters)`
Core search algorithm.

**Parameters:**
- `filters` (object): Filter criteria

**Returns:**
- Array of matching results

**Algorithm:**
1. Iterate through all codes in database
2. Filter by code type and year
3. Search within sections
4. Apply section number filter
5. Apply keyword matching
6. Apply full text search
7. Return matched sections

---

#### 8. `displaySearchResults(results, searchTerm)`
Renders search results with highlighting.

**Parameters:**
- `results` (array): Search results from `searchCodes()`
- `searchTerm` (string): Term to highlight

**Behavior:**
- Shows result count
- Displays each result with:
  - Code title and section
  - Metadata (type, title)
  - Content snippet
  - Highlighted search terms
- Handles empty results

---

#### 9. `viewCodeSection(codeId, sectionNum)`
Navigates to specific code section from search results.

**Parameters:**
- `codeId` (string): Code identifier
- `sectionNum` (string): Section number

**Behavior:**
- Navigates to code page
- Scrolls to specific section
- Smooth scroll animation

---

### Comparison Functions

#### 10. `performComparison()`
Initiates code comparison.

**Behavior:**
- Reads selected codes and sections
- Validates selections
- Retrieves content from database
- Calls `displayComparison()`

---

#### 11. `displayComparison(title1, content1, title2, content2)`
Shows side-by-side comparison with diff highlighting.

**Parameters:**
- `title1` (string): First code title
- `content1` (string): First code content
- `title2` (string): Second code title
- `content2` (string): Second code content

**Behavior:**
- Splits content into lines
- Calls `highlightDifferences()` for each side
- Renders comparison panels
- Shows results section

---

#### 12. `highlightDifferences(linesA, linesB)`
Diff algorithm for highlighting changes.

**Parameters:**
- `linesA` (array): Lines from first code
- `linesB` (array): Lines from second code

**Returns:**
- HTML string with highlighted differences

**Highlighting:**
- Regular lines: No highlighting
- Modified lines: Yellow background (`diff-modified`)
- Unique lines: Green background (`diff-added`)

**Algorithm:**
1. Compare each line from A to B
2. If identical: normal display
3. If exists elsewhere: mark as modified
4. If unique: mark as added
5. Return formatted HTML

---

### Utility Functions

#### 13. `escapeRegExp(string)`
Escapes special regex characters.

**Parameters:**
- `string` (string): Text to escape

**Returns:**
- Escaped string safe for regex

**Usage:**
```javascript
escapeRegExp('test.string'); // Returns 'test\\.string'
```

---

#### 14. `escapeHtml(text)`
Escapes HTML special characters.

**Parameters:**
- `text` (string): Text to escape

**Returns:**
- HTML-safe string

**Usage:**
```javascript
escapeHtml('<script>alert("test")</script>');
// Returns: &lt;script&gt;alert("test")&lt;/script&gt;
```

---

## Data Structure

### Code Database Schema

```javascript
{
    codeId: {
        id: string,           // Unique identifier
        title: string,        // Full display title
        year: string,         // Publication year
        category: string,     // Main category
        sections: {
            sectionNumber: {
                title: string,     // Section title
                content: string,   // Full text content
                type: string,      // Section type/category
                keywords: array    // Searchable keywords
            }
        }
    }
}
```

### Example Entry

```javascript
ibc: {
    id: 'ibc',
    title: 'International Building Code (IBC) 2024',
    year: '2024',
    category: 'Building Construction',
    sections: {
        '903.3.1': {
            title: 'NFPA 13 Installation',
            content: '903.3.1 NFPA 13 Installation\n\n...',
            type: 'Fire Protection',
            keywords: ['sprinkler', 'NFPA 13', 'installation']
        }
    }
}
```

---

## Event Handlers

### Navigation Click Events
```javascript
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        const page = this.dataset.page;
        if (page === 'code') {
            toggleDropdown();
        } else {
            navigateToPage(page);
        }
    });
});
```

### Dropdown Click Events
```javascript
document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', function() {
        const code = this.dataset.code;
        viewCode(code);
    });
});
```

### Global Search Enter Key
```javascript
document.getElementById('globalSearch').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performGlobalSearch(this.value);
    }
});
```

---

## CSS Classes

### State Classes
- `.active` - Currently selected/displayed item
- `.open` - Expanded dropdown or section
- `.hidden` - Display none

### Navigation Classes
- `.nav-item` - Sidebar navigation item
- `.nav-item.has-dropdown` - Nav item with dropdown
- `.dropdown-menu` - Dropdown container
- `.dropdown-item` - Dropdown menu item

### Content Classes
- `.page` - Main content page container
- `.code-section` - Individual code section
- `.code-text` - Formatted code content
- `.search-results` - Search results container
- `.result-item` - Individual search result

### Comparison Classes
- `.diff-added` - Green highlighting (unique content)
- `.diff-removed` - Red highlighting (removed content)
- `.diff-modified` - Yellow highlighting (modified content)
- `.comparison-panel` - Comparison side panel

### UI Component Classes
- `.code-card` - Featured code card
- `.filter-group` - Filter form group
- `.filter-select` - Filter dropdown
- `.filter-input` - Filter text input
- `.search-button` - Primary action button

---

## Customization Guide

### Adding New Codes

1. **Add to Database:**
```javascript
codeDatabase.newcode = {
    id: 'newcode',
    title: 'New Code Title',
    year: '2024',
    category: 'Category',
    sections: {
        '1.1': {
            title: 'Section Title',
            content: 'Content here...',
            type: 'Type',
            keywords: ['keyword1', 'keyword2']
        }
    }
};
```

2. **Add to Dropdown:**
```html
<div class="dropdown-item" data-code="newcode">New Code</div>
```

3. **Add to Featured (Optional):**
```html
<div class="code-card" onclick="viewCode('newcode')">
    <h3>New Code</h3>
    <p>Description</p>
    <span class="code-badge">Category</span>
</div>
```

### Modifying Colors

Update CSS variables:
```css
:root {
    --primary-blue: #149CDC;
    --dark-blue: #0C5484;
    --charcoal: #2C4B5C;
    --light-gray: #E3E9EF;
    --medium-blue: #ACC9DB;
}
```

### Adding New Filters

1. **Add HTML Input:**
```html
<div class="filter-group">
    <label class="filter-label">New Filter</label>
    <select class="filter-select" id="newFilter">
        <option value="">All</option>
        <option value="value1">Option 1</option>
    </select>
</div>
```

2. **Update Search Function:**
```javascript
function performDetailedSearch() {
    const filters = {
        // ... existing filters
        newFilter: document.getElementById('newFilter').value
    };
    // ... rest of function
}
```

3. **Add to Search Algorithm:**
```javascript
function searchCodes(filters) {
    // ... existing code
    if (filters.newFilter) {
        // Apply new filter logic
    }
    // ... rest of function
}
```

---

## Performance Tips

1. **Lazy Loading**: Current implementation loads all data upfront. For larger databases, implement lazy loading of sections.

2. **Search Optimization**: For very large code databases, consider:
   - Indexing keywords
   - Debouncing search input
   - Implementing pagination

3. **Caching**: Browser automatically caches the single HTML file.

4. **Animation Performance**: CSS transitions use GPU-accelerated properties (transform, opacity).

---

## Accessibility Features

- Semantic HTML structure
- Keyboard navigation support
- Focus states on interactive elements
- ARIA labels (can be enhanced further)
- Readable font sizes
- High contrast color scheme

---

## Browser API Usage

- **DOM Manipulation**: `querySelector`, `querySelectorAll`, `classList`
- **Events**: `addEventListener` for click and keyboard events
- **Storage**: None (stateless application)
- **Animation**: CSS transitions and `@keyframes`
- **Layout**: Flexbox and CSS Grid

---

## Testing Checklist

- [ ] All navigation links work
- [ ] Dropdown opens/closes correctly
- [ ] Code content displays properly
- [ ] Search finds relevant results
- [ ] Search highlighting works
- [ ] Filters apply correctly
- [ ] Comparison shows differences
- [ ] Responsive on mobile
- [ ] Works in all major browsers
- [ ] No console errors

---

**For detailed implementation examples, see the inline comments in `us-code-navigator.html`**
