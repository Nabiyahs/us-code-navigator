# Auto-Linking Feature Guide

## Overview

The US Code Navigator now includes **intelligent auto-linking** for Chapter and Section references within code content. This feature automatically creates clickable links whenever "Chapter X" or "Section X.X.X" appears in the code text.

## How It Works

### Automatic Detection

The system uses advanced pattern matching to find references:

**Chapter References:**
- `Chapter 3`
- `Chapter 10`
- `Chapter 902`

**Section References:**
- `Section 903.3.1`
- `Section 10`
- `Section 4.8.2.1`

### Link Behavior

#### 1. Internal Links (Section Exists)
When the referenced chapter or section **exists** in the current code:
- Creates an **internal anchor link**
- Clicking scrolls smoothly to that section
- Section briefly highlights with blue background
- Styled with solid underline
- Example: `Chapter 3` → jumps to Chapter 3 in same document

#### 2. External Links (Section Not Found)
When the referenced chapter or section **does NOT exist** in the current code:
- Creates a **Google search link**
- Opens in new tab
- Search query: "[Code Name] [chapter/section] [number]"
- Includes 🔍 icon for visual indication
- Styled with dashed underline
- Example: `Section 404.5` → searches "IBC 2024 section 404.5" on Google

## Visual Design

### Internal Links
```
Chapter 3
─────────  (solid blue underline)
```
- **Color**: Primary blue (#149CDC)
- **Hover**: Light blue background
- **Underline**: Solid
- **Cursor**: Pointer

### External Links
```
🔍 Section 404.5
─ ─ ─ ─ ─ ─ ─ ─  (dashed underline)
```
- **Color**: Dark blue (#0C5484)
- **Hover**: Light background
- **Underline**: Dashed
- **Icon**: 🔍 magnifying glass
- **Target**: Opens in new tab

## Examples

### Example 1: IBC 2024 - Fire Barrier Definition

**Original Text:**
```
A fire-resistance-rated wall assembly of materials designed
to restrict the spread of fire in accordance with Chapter 7.
```

**After Auto-Linking:**
```
A fire-resistance-rated wall assembly of materials designed
to restrict the spread of fire in accordance with [Chapter 7].
                                                     ^^^^^^^^
                                              (clickable link)
```

If Chapter 7 exists → Internal link to Chapter 7 section
If Chapter 7 doesn't exist → Google search for "IBC 2024 chapter 7"

### Example 2: NFPA 13 - Cross References

**Original Text:**
```
Where required by this code, automatic sprinkler systems shall
be installed in accordance with Section 903.3.1.1, 903.3.1.2
or 903.3.1.3.
```

**After Auto-Linking:**
```
Where required by this code, automatic sprinkler systems shall
be installed in accordance with [Section 903.3.1.1], [903.3.1.2]
or [903.3.1.3].
```

Each section number becomes a clickable link.

### Example 3: Mixed References

**Original Text:**
```
The means of egress shall comply with Chapter 10. Exception:
Buildings equipped throughout with an automatic sprinkler
system in accordance with Section 903.3.1.1.
```

**Result:**
- `Chapter 10` → Internal/External link
- `Section 903.3.1.1` → Internal/External link

## Technical Implementation

### Pattern Matching

**Chapter Regex:**
```javascript
/\b(Chapter)\s+(\d+)\b/gi
```
- Matches "Chapter" followed by one or more digits
- Case insensitive
- Word boundaries prevent partial matches

**Section Regex:**
```javascript
/\b(Section)\s+(\d+(?:\.\d+)*(?:\.\d+)?(?:\.\d+)?)\b/gi
```
- Matches "Section" followed by numbers with optional decimals
- Supports formats like: 903, 903.3, 903.3.1, 903.3.1.1
- Case insensitive

### Link Generation Algorithm

1. **Scan text** for all Chapter and Section patterns
2. **For each match:**
   - Extract the reference number
   - Search current code's sections database
   - If found → Create internal anchor link with `scrollToSection()`
   - If not found → Create Google search link
3. **Replace text** with HTML link tags
4. **Preserve context** (apply before HTML escaping)

### Section Matching Logic

**For Chapters:**
```javascript
// Find chapter without section number
sections.find(section =>
  section.chapter === chapterNum && !section.section
)
```

**For Sections:**
```javascript
// Find exact section match
sections.find(section =>
  section.section === sectionNum
)
```

## JavaScript Functions

### `autoLinkReferences(text, code, currentSectionKey)`

**Parameters:**
- `text`: Raw text content to process
- `code`: Current code object with sections
- `currentSectionKey`: Current section (to avoid self-linking)

**Returns:**
- HTML string with embedded links

**Process:**
1. Find all matches using regex
2. Determine if internal or external
3. Generate appropriate link HTML
4. Replace in text (reverse order to preserve indices)

### `scrollToSection(sectionKey)`

**Parameters:**
- `sectionKey`: Unique identifier for section (e.g., "ch3_s903.3.1")

**Behavior:**
1. Find element by ID
2. Smooth scroll to element
3. Apply temporary highlight (blue background)
4. Remove highlight after 2 seconds

## Google Search Format

When creating external links, the search query format is:

```
https://www.google.com/search?q=[Code Title] [type] [number]
```

**Examples:**
- IBC 2024 + Chapter 7 → `IBC 2024 chapter 7`
- NFPA 13 2025 + Section 8.3.1 → `NFPA 13 2025 section 8.3.1`

## CSS Styling

```css
.code-reference {
    color: var(--primary-blue);
    text-decoration: none;
    font-weight: 600;
    border-bottom: 2px solid var(--medium-blue);
    transition: all 0.3s ease;
    padding: 0 0.2rem;
}

.code-reference.internal-link:hover {
    background-color: rgba(20, 156, 220, 0.1);
    border-bottom-color: var(--primary-blue);
}

.code-reference.external-link {
    color: var(--dark-blue);
    border-bottom-style: dashed;
}
```

## User Experience

### Smooth Scrolling
- Internal links use `scroll-behavior: smooth`
- Scroll margin ensures section isn't hidden behind header
- Animated highlighting draws attention to target section

### Visual Feedback
- Hover effects indicate clickability
- Different styles for internal vs external links
- Icon (🔍) clearly marks external searches
- Tooltip shows destination on hover

### Accessibility
- Links include `title` attributes
- External links include `rel="noopener noreferrer"` for security
- External links open in new tab (`target="_blank"`)
- Semantic HTML with proper anchor tags

## Limitations & Edge Cases

### Not Matched:
- "Chapter" without number: ❌ "See Chapter"
- Lowercase: ❌ "chapter 3" (can be added if needed)
- Other formats: ❌ "Ch. 3", "Sec. 903"
- Inside code blocks: ✓ Still matched (intentional)

### Prevented:
- Self-linking: Sections don't link to themselves
- Duplicate processing: Each reference processed once
- HTML injection: All user content properly escaped

## Future Enhancements

Potential improvements:
1. **Support alternate formats**: "Ch.", "Sec.", "§"
2. **Table/Figure references**: "Table 903.2", "Figure 4.1"
3. **Cross-code linking**: Link between different codes
4. **Smart suggestions**: "Did you mean Section 903.3.1.1?"
5. **Link preview**: Hover tooltip showing section title
6. **Bookmarks**: Save frequently accessed sections

## Testing

### Test Cases:

1. ✅ Internal link to existing chapter
2. ✅ Internal link to existing section
3. ✅ External link when chapter not found
4. ✅ External link when section not found
5. ✅ Multiple references in same paragraph
6. ✅ Nested section numbers (903.3.1.1)
7. ✅ Smooth scroll behavior
8. ✅ Highlight animation
9. ✅ Google search opens in new tab
10. ✅ Proper URL encoding

## Conclusion

The auto-linking feature significantly enhances the usability of the US Code Navigator by:
- **Reducing navigation time**: Jump directly to referenced sections
- **Improving research**: Quick Google searches for missing content
- **Enhancing readability**: Visual indication of cross-references
- **Maintaining context**: Smooth scrolling keeps users oriented

This intelligent system adapts to the available content, providing the most helpful action for each reference.
