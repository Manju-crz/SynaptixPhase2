# 🚨 URGENT: Test Instructions for Filename Prefix Bug

## ⚡ Quick Fix Applied

I've added **enhanced debug logging** and **forced cache refresh** (v=3).

---

## 📋 Testing Steps

### Step 1: Restart Flask Server
```bash
# Press Ctrl+C to stop current server
# Then restart:
python .\custom_ui\app.py
```

### Step 2: **HARD REFRESH** Browser
**IMPORTANT:** You MUST do a hard refresh to clear the cache!

**Windows/Linux:**
- Press `Ctrl + Shift + R` (Chrome/Firefox)
- OR `Ctrl + F5`

**Mac:**
- Press `Cmd + Shift + R`

### Step 3: Open Browser Console
- Press `F12`
- Go to "Console" tab
- **Clear the console** (click the 🚫 icon)

### Step 4: Test with Custom Prefix

1. Go to "OpenAPI JSON Parser" tab
2. **Enter custom prefix:** `PetStore`
3. **DO NOT check the checkbox**
4. Click "Run JSON Parser"

### Step 5: Check Console Output

You should see these **THREE** debug lines in the browser console:

```
🔍 DEBUG: Checkbox checked: false
🔍 DEBUG: Input value: PetStore
🔍 DEBUG: Final filename prefix: PetStore
```

### Step 6: Check Flask Terminal

You should see these **TWO** debug lines in the Flask terminal:

```
📝 Received filename_prefix: 'PetStore'
📝 Request data: {'url': 'https://petstore.swagger.io/v2/swagger.json', 'filename_prefix': 'PetStore'}
```

### Step 7: Check Generated File

Look in `Rest_API_Data/` folder.

**Expected filename:** `PetStore_2026_08_25_XX_XX.xlsx`

---

## 🎯 What to Report

### If Browser Console Shows:
```
🔍 DEBUG: Checkbox checked: false
🔍 DEBUG: Input value: PetStore
🔍 DEBUG: Final filename prefix: PetStore
```

**AND Flask Terminal Shows:**
```
📝 Received filename_prefix: 'PetStore'
```

**BUT File is Still:**
```
OpenAPI_Data_2026_08_25_XX_XX.xlsx
```

**Then:** The issue is in the backend file creation logic.

---

### If Browser Console Shows:
```
🔍 DEBUG: Checkbox checked: false
🔍 DEBUG: Input value: PetStore
🔍 DEBUG: Final filename prefix: OpenAPI_Data  ❌ WRONG!
```

**Then:** The JavaScript logic is broken.

---

### If Browser Console Shows NOTHING

**Then:** The JavaScript file is still cached. Do a **HARD REFRESH**:
- `Ctrl + Shift + R` (Windows/Linux)
- `Cmd + Shift + R` (Mac)

---

## 🔍 Additional Debug Test

If the above doesn't show the debug logs, try this:

1. Open browser console (F12)
2. Type this command and press Enter:
   ```javascript
   document.getElementById('jsonFilePrefixInput').value
   ```
3. It should show: `"PetStore"` (or whatever you typed)

4. Then type:
   ```javascript
   document.getElementById('jsonDefaultFileNameCheckbox').checked
   ```
5. It should show: `false`

---

## ✅ Success Criteria

**Browser Console:**
```
🔍 DEBUG: Checkbox checked: false
🔍 DEBUG: Input value: PetStore
🔍 DEBUG: Final filename prefix: PetStore
Filename prefix: PetStore
Running OpenAPI JSON Parser for: https://petstore.swagger.io/v2/swagger.json
```

**Flask Terminal:**
```
📝 Received filename_prefix: 'PetStore'
📝 Request data: {'url': '...', 'filename_prefix': 'PetStore'}
✅ Excel file created: C:\...\Rest_API_Data\PetStore_2026_08_25_XX_XX.xlsx
```

**File Created:**
```
PetStore_2026_08_25_XX_XX.xlsx  ✅ CORRECT!
```

---

## 🚨 If Still Not Working

**Copy and send me:**

1. **Full browser console output** (screenshot or text)
2. **Full Flask terminal output** (from the POST request)
3. **Screenshot of the UI** showing:
   - The checkbox state
   - The input field with your text
   - The button

---

**Created:** August 25, 2026  
**Version:** v3 (cache-busting update)  
**Status:** Ready for testing
