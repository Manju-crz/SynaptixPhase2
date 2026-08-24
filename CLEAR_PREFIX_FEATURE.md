# Clear Custom Prefix Feature

**Enhancement:** Added "Clear Custom Prefix" link to both OpenAPI Parser and Swagger Scraper tabs.

---

## ✨ New Feature

### Visual Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [Enter prefix]  Clear Custom Prefix  [▶️ Run]│
│  ↑ Checkbox               ↑ Input (250px) ↑ Link (disabled)    ↑ Button│
└─────────────────────────────────────────────────────────────────────┘
```

### Components

1. **Checkbox:** "Set Default File Name"
2. **Input Field:** Max-width 250px (reduced from full width)
3. **Clear Link:** "Clear Custom Prefix" (NEW!)
4. **Button:** "Run JSON Parser" / "Run UI Scraper"

---

## 🎯 Feature Behavior

### State 1: Initial (No Input)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [                ]  Clear Custom Prefix  [🔒 Run]│
│  ✅ Enabled               ✅ Enabled         🔒 Disabled (grayed)  🔒 Disabled│
└─────────────────────────────────────────────────────────────────────┘
```

**Clear Link State:**
- Opacity: 0.5 (grayed out)
- Pointer Events: none (not clickable)
- Cursor: default

---

### State 2: User Enters Text

```
USER TYPES "PetStore"
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [PetStore        ]  Clear Custom Prefix  [✅ Run]│
│  🔒 Disabled              ✅ Enabled         ✅ ENABLED (clickable) ✅ Enabled│
└─────────────────────────────────────────────────────────────────────┘
```

**Clear Link State:**
- Opacity: 1 (fully visible)
- Pointer Events: auto (clickable)
- Cursor: pointer
- Color: #00d4ff (cyan blue)
- Text Decoration: underline

---

### State 3: User Clicks "Clear Custom Prefix"

```
USER CLICKS "Clear Custom Prefix"
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [                ]  Clear Custom Prefix  [🔒 Run]│
│  ✅ Enabled (re-enabled!) ✅ Enabled         🔒 Disabled (grayed)  🔒 Disabled│
└─────────────────────────────────────────────────────────────────────┘
```

**What Happens:**
1. Input field is cleared (value = "")
2. Checkbox is re-enabled
3. Clear link is disabled again
4. Button is disabled
5. User can now check the checkbox if desired

---

### State 4: Checkbox Checked

```
USER CHECKS CHECKBOX
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│  ☑ Set Default File Name  [                ]  Clear Custom Prefix  [✅ Run]│
│  ✅ Enabled               🔒 Disabled        🔒 Disabled (grayed)  ✅ Enabled│
└─────────────────────────────────────────────────────────────────────┘
```

**Clear Link State:**
- Opacity: 0.5 (grayed out)
- Pointer Events: none (not clickable)
- Reason: No custom text to clear

---

## 🔄 Complete User Flow

### Scenario A: Enter Text → Clear → Check Checkbox

```
Step 1: Initial State
        ☐ Set Default File Name  [        ]  Clear (disabled)  [🔒 Run]

Step 2: User types "MyAPI"
        ☐ Set Default File Name  [MyAPI   ]  Clear (enabled)   [✅ Run]
        ↑ Disabled

Step 3: User clicks "Clear Custom Prefix"
        ☐ Set Default File Name  [        ]  Clear (disabled)  [🔒 Run]
        ↑ Re-enabled!

Step 4: User checks checkbox
        ☑ Set Default File Name  [        ]  Clear (disabled)  [✅ Run]
        
Step 5: User submits
        → File: OpenAPI_Data_2026_08_25_XX_XX.xlsx
```

---

### Scenario B: Enter Text → Submit (No Clear)

```
Step 1: Initial State
        ☐ Set Default File Name  [        ]  Clear (disabled)  [🔒 Run]

Step 2: User types "PetStore"
        ☐ Set Default File Name  [PetStore]  Clear (enabled)   [✅ Run]

Step 3: User submits (without clearing)
        → File: PetStore_2026_08_25_XX_XX.xlsx
```

---

### Scenario C: Enter Text → Clear → Enter Different Text

```
Step 1: User types "OldName"
        ☐ Set Default File Name  [OldName ]  Clear (enabled)   [✅ Run]

Step 2: User clicks "Clear Custom Prefix"
        ☐ Set Default File Name  [        ]  Clear (disabled)  [🔒 Run]

Step 3: User types "NewName"
        ☐ Set Default File Name  [NewName ]  Clear (enabled)   [✅ Run]

Step 4: User submits
        → File: NewName_2026_08_25_XX_XX.xlsx
```

---

## 💻 Implementation Details

### HTML Changes

**OpenAPI Parser Tab:**
```html
<input
    type="text"
    id="jsonFilePrefixInput"
    placeholder="Enter file name prefix"
    value=""
    oninput="updateJsonParserControls()"
    style="max-width: 250px;"  <!-- Changed from flex: 1 -->
>
<a id="jsonClearPrefixLink" 
   onclick="clearJsonPrefix()" 
   style="color: #00d4ff; cursor: pointer; text-decoration: underline; 
          font-size: 0.9rem; opacity: 0.5; pointer-events: none;">
    Clear Custom Prefix
</a>
```

**Swagger Scraper Tab:**
```html
<input
    type="text"
    id="swaggerFilePrefixInput"
    placeholder="Enter file name prefix"
    value=""
    oninput="updateSwaggerScraperControls()"
    style="max-width: 250px;"  <!-- Changed from flex: 1 -->
>
<a id="swaggerClearPrefixLink" 
   onclick="clearSwaggerPrefix()" 
   style="color: #00d4ff; cursor: pointer; text-decoration: underline; 
          font-size: 0.9rem; opacity: 0.5; pointer-events: none;">
    Clear Custom Prefix
</a>
```

---

### JavaScript Changes

**OpenAPI Parser (`openapiParserPage.js`):**
```javascript
function updateJsonParserControls() {
    const input = document.getElementById('jsonFilePrefixInput');
    const checkbox = document.getElementById('jsonDefaultFileNameCheckbox');
    const button = document.getElementById('runJsonParserBtn');
    const clearLink = document.getElementById('jsonClearPrefixLink');
    
    if (checkbox.checked) {
        input.disabled = true;
        button.disabled = false;
        clearLink.style.opacity = '0.5';
        clearLink.style.pointerEvents = 'none';
    } else if (input.value.trim() !== '') {
        checkbox.disabled = true;
        button.disabled = false;
        clearLink.style.opacity = '1';          // ✅ Enable link
        clearLink.style.pointerEvents = 'auto'; // ✅ Make clickable
    } else {
        checkbox.disabled = false;
        input.disabled = false;
        button.disabled = true;
        clearLink.style.opacity = '0.5';
        clearLink.style.pointerEvents = 'none';
    }
}

function clearJsonPrefix() {
    const input = document.getElementById('jsonFilePrefixInput');
    if (input) {
        input.value = '';                    // Clear the input
        updateJsonParserControls();          // Update all controls
    }
}
```

**Swagger Scraper (`swaggerScraperPage.js`):**
```javascript
function updateSwaggerScraperControls() {
    // Same logic as OpenAPI Parser
    // ...
}

function clearSwaggerPrefix() {
    const input = document.getElementById('swaggerFilePrefixInput');
    if (input) {
        input.value = '';
        updateSwaggerScraperControls();
    }
}
```

---

## 🎨 Visual States Matrix

| Checkbox | Input Value | Clear Link | Button | Description |
|----------|-------------|------------|--------|-------------|
| ☐ Unchecked | Empty | 🔒 Disabled | 🔒 Disabled | Initial state |
| ☐ Unchecked | "PetStore" | ✅ Enabled | ✅ Enabled | Custom prefix entered |
| ☑ Checked | Empty | 🔒 Disabled | ✅ Enabled | Default filename |
| 🔒 Disabled | "PetStore" | ✅ Enabled | ✅ Enabled | Custom prefix (checkbox disabled) |

---

## 🧪 Testing Checklist

### OpenAPI Parser Tab

- [ ] Initial state: Clear link is grayed out (not clickable)
- [ ] Enter text "PetStore": Clear link becomes blue and clickable
- [ ] Click "Clear Custom Prefix": Input is cleared
- [ ] After clearing: Checkbox is re-enabled
- [ ] After clearing: Clear link is grayed out again
- [ ] After clearing: Button is disabled
- [ ] Check checkbox: Clear link stays grayed out
- [ ] Input field width is 250px (not full width)

### Swagger Scraper Tab

- [ ] Initial state: Clear link is grayed out (not clickable)
- [ ] Enter text "MySwagger": Clear link becomes blue and clickable
- [ ] Click "Clear Custom Prefix": Input is cleared
- [ ] After clearing: Checkbox is re-enabled
- [ ] After clearing: Clear link is grayed out again
- [ ] After clearing: Button is disabled
- [ ] Check checkbox: Clear link stays grayed out
- [ ] Input field width is 250px (not full width)

---

## 📊 Before vs After

### Before (No Clear Link)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [Enter file name prefix (full width)]  [▶️ Run]│
└─────────────────────────────────────────────────────────────────────┘
```

**Problem:** 
- Input field too wide
- No easy way to clear entered text
- User had to manually delete text to re-enable checkbox

---

### After (With Clear Link)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ☐ Set Default File Name  [Enter prefix (250px)]  Clear Custom Prefix  [▶️ Run]│
└─────────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ Input field is more compact (250px max-width)
- ✅ Clear link provides one-click text clearing
- ✅ Clear link is only enabled when needed
- ✅ Better UX for reverting to default filename
- ✅ Visual feedback (grayed out when disabled, blue when enabled)

---

## 🎯 User Benefits

1. **Quick Reset:** One click to clear custom prefix instead of manual deletion
2. **Visual Feedback:** Link changes color to show when it's available
3. **Better Layout:** Input field no longer stretches across the page
4. **Intuitive:** Link only appears clickable when there's text to clear
5. **Smooth Workflow:** Easy to switch between custom and default filenames

---

## 📝 Files Modified

1. ✅ `custom_ui/templates/tabs/openapi_parser.html`
   - Added clear link
   - Reduced input width to 250px

2. ✅ `custom_ui/templates/tabs/swagger_scraper.html`
   - Added clear link
   - Reduced input width to 250px

3. ✅ `custom_ui/static/js/pages/openapiParserPage.js`
   - Updated `updateJsonParserControls()` to manage clear link
   - Added `clearJsonPrefix()` function

4. ✅ `custom_ui/static/js/pages/swaggerScraperPage.js`
   - Updated `updateSwaggerScraperControls()` to manage clear link
   - Added `clearSwaggerPrefix()` function

5. ✅ `custom_ui/templates/index.html`
   - Updated version to v=5 for cache refresh

---

## 🚀 Ready to Test

**Version:** v5  
**Status:** ✅ COMPLETE

**Test Steps:**
1. Restart Flask server
2. Hard refresh browser (Ctrl + Shift + R)
3. Test the clear link functionality
4. Verify input field is narrower (250px)
5. Verify link enables/disables correctly

---

**Created:** August 25, 2026  
**Feature:** Clear Custom Prefix Link  
**Status:** Ready for testing
