# File Rename Utility - Quick Reference

## 🎯 What Was Implemented

A complete file renaming system that allows users to rename test files from the UI, with the changes reflected on the actual file system.

## 📦 Files Created/Modified

### ✅ New Files
1. **`file_rename_util.py`** - Reusable utility for file renaming
2. **`test_file_rename.py`** - Comprehensive test suite
3. **`FILE_RENAME_INTEGRATION_GUIDE.md`** - Detailed integration guide
4. **`QUICK_REFERENCE.md`** - This file

### ✅ Modified Files
1. **`__init__.py`** - Exported new functions
2. **`app.py`** - Added `/rename-file` API endpoint
3. **`script.js`** - Updated `saveTestClassName()` to call backend API

## 🚀 Quick Usage

### From UI
1. Generate test code in any component tab
2. Click "Rename Test File" link
3. Enter new file name
4. Click ✓ to save
5. File is renamed on disk automatically!

### From Python Code
```python
from generator_altUtl import rename_file_in_folder

result = rename_file_in_folder(
    folder_name='TestComponent_01',
    existing_file_name='TestFile_01.py',
    new_file_name='CreatePetTest.py'
)

print(result['success'])  # True
print(result['message'])  # Success message
```

### From API
```bash
curl -X POST http://localhost:5000/rename-file \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "TestComponent_01",
    "existing_file_name": "TestFile_01",
    "new_file_name": "CreatePetTest"
  }'
```

## 🧪 Testing

### Run All Tests
```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2\generator_altUtl
python test_file_rename.py
```

### Test Options
1. **Run all tests** - Creates temporary test environment
2. **Test folder finding** - Read-only test on real project
3. **Run both** - Comprehensive testing

## 📋 Key Functions

### `rename_file_in_folder()`
Main function that renames files within a specified folder.

**Parameters:**
- `folder_name` - Folder to search for
- `existing_file_name` - Current file name
- `new_file_name` - New file name
- `project_root` (optional) - Project root directory
- `search_recursive` (optional) - Search recursively (default: True)

**Returns:** Dictionary with success status, message, and file paths

### `rename_file_with_extension_handling()`
Automatically preserves file extensions.

**Example:**
```python
rename_file_with_extension_handling(
    folder_name='TestComponent_01',
    existing_file_name='test.py',
    new_file_name='new_test'  # .py added automatically
)
```

## ✨ Features

- ✅ Recursive folder search
- ✅ Automatic .py extension handling
- ✅ File existence validation
- ✅ Target file conflict detection
- ✅ Comprehensive error handling
- ✅ Detailed logging
- ✅ UI integration with notifications
- ✅ Backend API endpoint
- ✅ Full test coverage

## 🔧 API Endpoint

**URL:** `/rename-file`  
**Method:** POST  
**Content-Type:** application/json

**Request:**
```json
{
  "folder_name": "TestComponent_01",
  "existing_file_name": "TestFile_01",
  "new_file_name": "CreatePetTest"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Successfully renamed...",
  "old_file_name": "TestFile_01.py",
  "new_file_name": "CreatePetTest.py",
  "old_file_path": "C:\\...\\TestFile_01.py",
  "new_file_path": "C:\\...\\CreatePetTest.py"
}
```

**Error Response (404/400/500):**
```json
{
  "success": false,
  "message": "Error description"
}
```

## 📝 Common Use Cases

### 1. Rename after generation
Generate test → Rename to descriptive name → Execute

### 2. Organize test files
Rename multiple files to follow naming convention

### 3. Fix naming mistakes
Quickly correct typos or improve clarity

## ⚠️ Important Notes

1. **Generate first** - Test code must be generated before renaming
2. **Unique names** - New file name must not already exist
3. **Valid names** - Use Python-compatible file names
4. **Extensions** - .py extension is added automatically if missing

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| Folder not found | Generate test code first |
| File not found | Check file exists in folder |
| File already exists | Choose different name |
| Folder name not set | Set folder name in component |

## 📚 Documentation

- **Integration Guide:** `FILE_RENAME_INTEGRATION_GUIDE.md`
- **Test Suite:** `test_file_rename.py`
- **Source Code:** `file_rename_util.py`

## 🎓 Example Workflow

```python
# 1. Import the utility
from generator_altUtl import rename_file_in_folder

# 2. Rename a file
result = rename_file_in_folder(
    folder_name='TestComponent_01',
    existing_file_name='TestFile_01.py',
    new_file_name='CreatePetTest.py'
)

# 3. Check result
if result['success']:
    print(f"✓ Renamed: {result['old_file_name']} → {result['new_file_name']}")
else:
    print(f"✗ Error: {result['message']}")
```

## 🔗 Related Utilities

- **`method_rename_util.py`** - Rename test methods within files
- **`file_rename_util.py`** - Rename entire test files (this utility)

---

**Created:** 2026-08-08  
**Version:** 1.0  
**Status:** ✅ Production Ready
