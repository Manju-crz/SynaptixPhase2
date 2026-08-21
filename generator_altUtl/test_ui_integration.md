# UI File Rename - Integration Test Guide

## ✅ File Rename Utility is Ready!

The file rename utility now works both from:
1. **Command Line** - Direct file renaming via CLI
2. **Web UI** - Rename files from component tabs

## 🧪 Testing Steps

### Test 1: Command Line (Already Working ✅)

```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2

# Rename CreatePetTest.py back to TestFile_01.py
python generator_altUtl\rename_file_cli.py TestComponent_01 CreatePetTest TestFile_01
```

**Expected Result:**
```
✅ SUCCESS!
Successfully renamed 'CreatePetTest.py' to 'TestFile_01.py'
```

### Test 2: Web UI Integration

#### Step 1: Start Flask Server
```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui
python app.py
```

**Wait for:**
```
* Running on http://127.0.0.1:5000
```

#### Step 2: Open Browser
Navigate to: `http://localhost:5000`

#### Step 3: Test File Rename from UI

1. **Go to Generator Tab**
2. **Find your component** (TestComponent_01)
3. **Locate the test class** (TestFile_01)
4. **Click "Rename Test File"** link
5. **Enter new name:** `CreatePetTest`
6. **Click ✓ (save button)**

**Expected Result:**
- ✅ Success notification appears
- ✅ File name updates in UI to "CreatePetTest"
- ✅ Physical file renamed on disk: `rest_test/TestComponent_01/CreatePetTest.py`

### Test 3: Verify File on Disk

```bash
# Check if file was renamed
dir rest_test\TestComponent_01\*.py
```

**Expected Output:**
```
CreatePetTest.py
```

## 🔧 Troubleshooting UI Integration

### Issue: "Unexpected token '<'"

**Cause:** Flask server not running or needs restart

**Solution:**
1. Stop Flask (Ctrl+C)
2. Restart: `python custom_ui/app.py`
3. Refresh browser (Ctrl+F5)
4. Try rename again

### Issue: "Folder name is not set"

**Cause:** Test code not generated yet

**Solution:**
1. Generate test code first
2. This creates the folder and sets the folder name
3. Then try renaming

### Issue: File not found

**Cause:** File doesn't exist or wrong name

**Solution:**
1. Check file exists: `dir rest_test\TestComponent_01\*.py`
2. Verify folder name matches
3. Use exact file name (case-sensitive)

## 📋 Complete Workflow Test

### Scenario: Rename a test file from UI

**Setup:**
```bash
# 1. Ensure file exists
dir rest_test\TestComponent_01\TestFile_01.py

# 2. Start Flask server
cd custom_ui
python app.py
```

**Test in Browser:**
1. Open `http://localhost:5000`
2. Go to Generator tab
3. Find TestComponent_01 → TestFile_01
4. Click "Rename Test File"
5. Enter: `CreatePetTest`
6. Click ✓

**Verify:**
```bash
# Check file was renamed
dir rest_test\TestComponent_01\CreatePetTest.py
```

**Expected:** File exists with new name ✅

## 🎯 Key Features Now Working

✅ **Automatic .py extension handling**
- Input: `TestFile_01` → Finds: `TestFile_01.py`
- Input: `CreatePetTest` → Creates: `CreatePetTest.py`

✅ **Recursive folder search**
- Searches entire project for folder
- No need to specify full path

✅ **Error handling**
- File not found
- Folder not found
- Target file already exists
- Clear error messages

✅ **UI notifications**
- Success: Green notification with file paths
- Error: Red notification with error message

✅ **Both CLI and UI work**
- CLI: Direct command-line usage
- UI: Browser-based renaming

## 📝 Usage Summary

### Command Line
```bash
python generator_altUtl\rename_file_cli.py <folder> <old_file> <new_file>
```

### Web UI
1. Navigate to component tab
2. Click "Rename Test File"
3. Enter new name
4. Click ✓

### API Endpoint
```bash
curl -X POST http://localhost:5000/rename-file \
  -H "Content-Type: application/json" \
  -d '{"folder_name":"TestComponent_01","existing_file_name":"TestFile_01","new_file_name":"CreatePetTest"}'
```

## ✨ What's Updated

### Files Modified:
1. ✅ `generator_altUtl/file_rename_util.py` - Auto .py extension handling
2. ✅ `custom_ui/app.py` - Removed manual extension handling
3. ✅ `custom_ui/static/script.js` - Better error handling

### Features Added:
1. ✅ Automatic extension detection
2. ✅ Extension preservation
3. ✅ Better error messages
4. ✅ CLI tool for testing
5. ✅ Complete documentation

## 🚀 Ready to Use!

The file rename utility is now fully integrated and ready for production use!

**Test it now:**
1. Start Flask server
2. Open browser to http://localhost:5000
3. Rename a file from the UI
4. Success! 🎉
