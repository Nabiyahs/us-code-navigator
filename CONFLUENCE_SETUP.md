# Confluence Setup Guide

## Quick Setup for Confluence WIKI

Follow these steps to add the US Code Navigator to your Confluence page.

## Method 1: HTML Macro (Recommended)

### Step 1: Create or Edit Confluence Page
1. Navigate to your Confluence space
2. Create a new page or edit an existing one
3. Give it a title (e.g., "US Code Navigator")

### Step 2: Insert HTML Macro
1. In the editor, type `/html` or click Insert > Other Macros
2. Search for "HTML" macro
3. Select "HTML Include" or "HTML" macro

### Step 3: Paste Code
1. Open `us-code-navigator.html` in a text editor
2. Copy the entire contents (Ctrl+A, Ctrl+C)
3. Paste into the HTML macro editor
4. Click "Insert" or "Save"

### Step 4: Publish
1. Save and publish your Confluence page
2. The US Code Navigator should now be fully functional

## Method 2: Iframe Embed

If your Confluence instance doesn't support HTML macro:

### Step 1: Upload to Web Server
1. Upload `us-code-navigator.html` to an accessible web server
2. Note the full URL (e.g., `https://yourserver.com/us-code-navigator.html`)

### Step 2: Use Iframe Macro
1. In Confluence editor, type `/iframe`
2. Enter the URL of your uploaded file
3. Set dimensions:
   - Width: 100%
   - Height: 800px (or adjust as needed)
4. Save and publish

## Method 3: Attachment + Link

If neither macro works:

### Step 1: Attach File
1. Edit your Confluence page
2. Click the attachment icon (paperclip)
3. Upload `us-code-navigator.html`

### Step 2: Create Link
1. Add text: "Click here to open US Code Navigator"
2. Link to the attachment
3. Set link to open in new window/tab

### Step 3: User Access
Users click the link to open the navigator in a new window

## Troubleshooting

### HTML Macro Not Available
- **Solution**: Contact your Confluence admin to enable HTML macros
- **Alternative**: Use Method 2 (Iframe) or Method 3 (Attachment)

### Styling Not Working
- **Issue**: Confluence may strip some CSS
- **Solution**: Use Iframe method to preserve all styling

### Content Not Displaying
- **Issue**: JavaScript may be blocked
- **Solution**: Check Confluence security settings or use external hosting

### Height Too Small
- **Issue**: Content cut off or requires scrolling
- **Solution**: Adjust iframe height or HTML macro height parameter
  ```
  Recommended heights:
  - Minimum: 600px
  - Optimal: 800px
  - Full page: 1200px
  ```

## Customization for Confluence

### Adjust Width for Confluence Layout

If the navigator is too wide for your Confluence page:

1. Find this CSS section in the HTML file:
```css
.main-container {
    display: flex;
    min-height: calc(100vh - 140px);
}
```

2. Add max-width:
```css
.main-container {
    display: flex;
    min-height: calc(100vh - 140px);
    max-width: 1400px;
    margin: 0 auto;
}
```

### Remove Header for Embedded View

If you want to remove the header when embedded in Confluence:

1. Find the header section:
```html
<header class="header">
    ...
</header>
```

2. Add `style="display: none;"`:
```html
<header class="header" style="display: none;">
    ...
</header>
```

### Adjust Colors to Match Confluence Theme

To match your Confluence theme colors:

1. Find the `:root` CSS variables section
2. Replace with your theme colors:
```css
:root {
    --primary-blue: #YOUR_COLOR_1;
    --dark-blue: #YOUR_COLOR_2;
    --charcoal: #YOUR_COLOR_3;
    --light-gray: #YOUR_COLOR_4;
    --medium-blue: #YOUR_COLOR_5;
}
```

## Permissions

### Required Permissions
- **Page Edit**: To add/edit the HTML macro
- **Attachment Upload**: If using attachment method
- **Macro Usage**: HTML or Iframe macro permissions

### Recommended Permissions
- **Page View**: All users who need to access the navigator
- **Space Admin**: For initial setup and troubleshooting

## Best Practices

### 1. Create Dedicated Page
- Don't embed in existing content pages
- Create a standalone "US Code Navigator" page
- Add to space sidebar for easy access

### 2. Add to Favorites
- Pin the page to space shortcuts
- Add to personal favorites
- Create quick link in space overview

### 3. User Training
- Add brief instructions at top of page
- Create quick reference guide
- Include contact info for support

### 4. Regular Updates
- Update code database quarterly
- Add new code standards as needed
- Document changes in page comments

## Integration Tips

### Link from Other Pages
Create quick links to the navigator from related pages:

```
For code requirements, see [US Code Navigator](/display/SPACE/US+Code+Navigator)
```

### Add to Space Sidebar
1. Go to Space Settings
2. Choose "Sidebar"
3. Add link to US Code Navigator page

### Create Page Labels
Add labels for easy finding:
- `code-reference`
- `building-codes`
- `nfpa-standards`
- `ibc-reference`

## Maintenance

### Monthly Checks
- Verify all links work
- Test search functionality
- Confirm comparisons display correctly

### Quarterly Updates
- Add new code sections
- Update existing content
- Review user feedback

### Annual Review
- Update to latest code versions
- Add new code standards
- Refresh UI if needed

## Support Resources

### Common Questions

**Q: Can I add more codes?**
A: Yes! Edit the `codeDatabase` object in the JavaScript section.

**Q: Can I export search results?**
A: Currently no, but this can be added. See README for enhancement ideas.

**Q: Does it work on mobile?**
A: Yes, the design is responsive and works on tablets and smartphones.

**Q: Can multiple users access simultaneously?**
A: Yes, it's client-side only, so unlimited concurrent users.

### Getting Help

1. Check the README.md for detailed documentation
2. Review the inline code comments
3. Contact your Confluence admin for macro issues
4. Test in a sandbox page before production deployment

## Success Checklist

- [ ] HTML file uploaded/pasted correctly
- [ ] Page displays without errors
- [ ] All four navigation items work (Home, 코드, 검색, 비교)
- [ ] Search functionality works
- [ ] Code comparison works
- [ ] Styling appears correct
- [ ] Responsive on mobile devices
- [ ] Page added to space navigation
- [ ] Users can access the page
- [ ] Documentation provided to users

---

**Ready to go!** Your US Code Navigator should now be fully functional in Confluence.
