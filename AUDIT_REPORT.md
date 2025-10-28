# Code Audit Report: Search Input Enter Key Failure

## Critical Issues Found

### 1. **MISSING FORM ELEMENT** ❌
**Location:** Line 520-535
**Problem:** The `#topSearchInput` is NOT wrapped in a `<form>` tag.
**Impact:** Browsers do NOT treat Enter key as "submit" when input is not inside a form.
**Evidence:**
```html
<input id="topSearchInput" ... />  <!-- No <form> parent -->
```

### 2. **IME COMPOSITION NOT HANDLED** ❌
**Location:** Line 43373-43380
**Problem:** No check for `event.isComposing` in keypress handler.
**Impact:** Asian language input (Korean, Japanese, Chinese) with IME may fail or fire prematurely.
**Evidence:**
```javascript
topSearchInput.addEventListener('keypress', function(e) {
    // Missing: if (e.isComposing) return;
    if (e.key === 'Enter') ...
});
```

### 3. **WRONG EVENT TYPE** ⚠️
**Location:** Line 43373
**Problem:** Using `keypress` which is deprecated; should use `keydown`.
**Impact:** Some browsers may not fire keypress reliably.

### 4. **SECTION VISIBILITY LOGIC** ✅ (Working)
**Location:** Line 42497-42498
**Status:** CORRECT - properly toggles `.active` class
**CSS:** Lines 112-117 correctly show/hide with display:none/block

### 5. **EVENT LISTENER TIMING** ✅ (Working)
**Location:** Line 43297
**Status:** CORRECT - wrapped in `DOMContentLoaded`

## Root Cause Analysis

The Enter key doesn't work because:
1. **No form submit event** - Input not in form, so Enter doesn't trigger submit
2. **Deprecated keypress** - Should use keydown instead
3. **IME interference** - No isComposing check causes issues with Korean input
4. **Missing debug instrumentation** - Can't diagnose runtime issues

## Recommended Fix

1. Wrap input in `<form>` tag
2. Use `form.addEventListener('submit')` as primary handler
3. Add `input.addEventListener('keydown')` with `isComposing` check as backup
4. Add minimal console.debug() for diagnostics
5. Verify computed visibility before/after render
