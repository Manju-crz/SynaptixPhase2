# Debug Guide - Filename Prefix Issue

## 🐛 Issue Reported

**Problem:** Custom filename prefix is not being used. File is created with default name instead.

**Example:**
- User enters: `PetStore`
- Expected file: `PetStore_2026_08_25_02_26.xlsx`
- Actual file: `OpenAPI_Data_2026_08_25_02_26.xlsx` ❌

---

## 🔍 Debug Logging Added

I've added debug logging to help identify where the issue is occurring.

### Frontend (JavaScript)
**Files Modified:**
- `custom_ui/static/js/pages/openapiParserPage.js`
- `custom_ui/static/js/pages/swaggerScraperPage.js`

**Added:**
```javascript
console.log('Filename prefix:', filenamePrefix);
```

### Backend (Flask)
**File Modified:**
- `custom_ui/app.py`

**Added:**
```python
logger.info(f"📝 Received filename_prefix: '{filename_prefix}'")
logger.info(f"📝 Request data: {data}")
```

---

## 🧪 Testing Steps

### Step 1: Restart Flask Server
```bash
# Stop current server (Ctrl+C)
# Start fresh
python .\custom_ui\app.py
```

### Step 2: Open Browser Console
1. Open browser (http://localhost:5000)
2. Press F12 to open Developer Tools
3. Go to "Console" tab
4. Keep it open

### Step 3: Test OpenAPI Parser with Custom Prefix

1. Go to "OpenAPI JSON Parser" tab
2. Enter custom prefix: `PetStore`
3. Enter URL: `https://petstore.swagger.io/v2/swagger.json`
4. Click "Run JSON Parser"

**Check Browser Console:**
```
Running OpenAPI JSON Parser for: https://petstore.swagger.io/v2/swagger.json
Filename prefix: PetStore  <-- Should show your custom prefix
```

**Check Flask Terminal:**
```
📝 Received filename_prefix: 'PetStore'  <-- Should show your custom prefix
📝 Request data: {'url': 'https://petstore.swagger.io/v2/swagger.json', 'filename_prefix': 'PetStore'}
```

### Step 4: Check Generated File
Look in `Rest_API_Data/` folder for the newest file.

**Expected:** `PetStore_2026_08_25_XX_XX.xlsx`

---

## 🔎 What to Look For

### Scenario A: Prefix Shows Correctly in Logs, But File is Wrong
**Browser Console shows:** `Filename prefix: PetStore`  
**Flask Terminal shows:** `📝 Received filename_prefix: 'PetStore'`  
**File created:** `OpenAPI_Data_2026_08_25_02_26.xlsx`

**This means:** The issue is in the `create_excel_with_data()` function or `run_openapi_json_parser()` function.

**Action:** Check `ext_util/xl_util.py` and `custom_ui/test_runner.py`

---

### Scenario B: Prefix Shows as Default in Logs
**Browser Console shows:** `Filename prefix: OpenAPI_Data`  
**Flask Terminal shows:** `📝 Received filename_prefix: 'OpenAPI_Data'`

**This means:** The JavaScript is not reading the input field correctly.

**Action:** Check the `updateJsonParserControls()` function and input field ID.

---

### Scenario C: Prefix Not in Request Data
**Flask Terminal shows:** `📝 Request data: {'url': '...'}` (no filename_prefix)

**This means:** The JavaScript is not sending the parameter.

**Action:** Check the `fetch()` call in JavaScript.

---

## 🔧 Possible Root Causes

### 1. Input Field ID Mismatch
**Check:**
```html
<!-- HTML -->
<input type="text" id="jsonFilePrefixInput" ...>

<!-- JavaScript -->
document.getElementById('jsonFilePrefixInput')?.value.trim()
```

**Verify:** IDs match exactly (case-sensitive)

---

### 2. Control Logic Issue
**Check:**
```javascript
const filenamePrefix = document.getElementById('jsonDefaultFileNameCheckbox')?.checked
    ? 'OpenAPI_Data'
    : (document.getElementById('jsonFilePrefixInput')?.value.trim() || 'OpenAPI_Data');
```

**Verify:** 
- If checkbox is checked → should use 'OpenAPI_Data'
- If input has text → should use input value
- If both empty → should use 'OpenAPI_Data'

---

### 3. Backend Parameter Name Mismatch
**Check:**
```python
# Flask
filename_prefix = data.get('filename_prefix', 'OpenAPI_Data')

# JavaScript
body: JSON.stringify({ url: url, filename_prefix: filenamePrefix })
```

**Verify:** Parameter name is exactly `filename_prefix` in both places

---

### 4. Excel Utility Issue
**Check:**
```python
# ext_util/xl_util.py
def create_excel_with_data(folder_path: str, filename_prefix: str, ...):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"{filename_prefix}_{timestamp}"  # Should use the prefix
```

**Verify:** The prefix is being used in the filename construction

---

## 📊 Expected Debug Output

### Successful Custom Prefix Flow

**Browser Console:**
```
Running OpenAPI JSON Parser for: https://petstore.swagger.io/v2/swagger.json
Filename prefix: PetStore
```

**Flask Terminal:**
```
02:50:00 | INFO | 📝 Received filename_prefix: 'PetStore'
02:50:00 | INFO | 📝 Request data: {'url': 'https://petstore.swagger.io/v2/swagger.json', 'filename_prefix': 'PetStore'}
02:50:00 | INFO | Fetching OpenAPI spec from URL: https://petstore.swagger.io/v2/swagger.json
02:50:02 | INFO | ✅ Successfully fetched OpenAPI spec from URL
02:50:02 | INFO | Base URL: https://petstore.swagger.io/v2
02:50:02 | INFO | Found 3 tags
02:50:02 | INFO | ✅ Extracted 20 operations
02:50:02 | INFO | ✅ Excel file created: C:\...\Rest_API_Data\PetStore_2026_08_25_02_50.xlsx
```

**File Created:**
```
PetStore_2026_08_25_02_50.xlsx  ✅ CORRECT
```

---

### Successful Default Prefix Flow (Checkbox Checked)

**Browser Console:**
```
Running OpenAPI JSON Parser for: https://petstore.swagger.io/v2/swagger.json
Filename prefix: OpenAPI_Data
```

**Flask Terminal:**
```
02:55:00 | INFO | 📝 Received filename_prefix: 'OpenAPI_Data'
02:55:00 | INFO | 📝 Request data: {'url': 'https://petstore.swagger.io/v2/swagger.json', 'filename_prefix': 'OpenAPI_Data'}
...
02:55:02 | INFO | ✅ Excel file created: C:\...\Rest_API_Data\OpenAPI_Data_2026_08_25_02_55.xlsx
```

**File Created:**
```
OpenAPI_Data_2026_08_25_02_55.xlsx  ✅ CORRECT
```

---

## 🎯 Next Steps

1. **Restart the Flask server** to load the new debug logging
2. **Open browser console** (F12)
3. **Test with custom prefix** "PetStore"
4. **Copy all console output** (both browser and Flask terminal)
5. **Share the logs** so we can identify exactly where the issue is

---

## 📝 Quick Test Checklist

- [ ] Flask server restarted
- [ ] Browser console open (F12)
- [ ] Entered custom prefix: "PetStore"
- [ ] Clicked "Run JSON Parser"
- [ ] Checked browser console for: `Filename prefix: PetStore`
- [ ] Checked Flask terminal for: `📝 Received filename_prefix: 'PetStore'`
- [ ] Checked generated file name in Rest_API_Data/
- [ ] Copied all logs (browser + Flask)

---

**Created:** August 25, 2026  
**Purpose:** Debug filename prefix issue  
**Status:** Awaiting test results with debug logging
