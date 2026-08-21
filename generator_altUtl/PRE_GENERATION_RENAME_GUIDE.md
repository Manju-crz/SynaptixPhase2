# Pre-Generation File Rename - Complete Guide

## 🎯 Feature Overview

You can now **rename test files BEFORE they are created**! The system intelligently handles three scenarios:

1. **Rename before file exists** - Updates UI only, file created with new name
2. **Rename after file exists** - Renames physical file on disk
3. **Rename when folder doesn't exist** - Updates UI only, file created with new name

## 📋 Workflow Scenarios

### Scenario 1: Rename Before Generation (NEW!)

**Steps:**
1. Add new Test Component (e.g., TestComponent_01)
2. Add new Test Class (shows as "TestFile_01")
3. **Click "Rename Test File"** → Enter "CreatePetTest"
4. **Click ✓** → UI updates to "CreatePetTest"
5. **Generate test code** → Creates `CreatePetTest.py` (not TestFile_01.py!)

**What Happens:**
```
User Action: Rename TestFile_01 → CreatePetTest
System Check: Does folder exist? NO
System Action: Update UI only (data-file-name="CreatePetTest")
Notification: "File name set to 'CreatePetTest'. File will be created with this name when you generate code."

User Action: Generate Test Code
System Check: What file name to use?
System Action: Read data-file-name → "CreatePetTest"
Result: Creates rest_test/TestComponent_01/CreatePetTest.py ✅
```

### Scenario 2: Rename After Generation (Existing)

**Steps:**
1. Generate test code → Creates `TestFile_01.py`
2. **Click "Rename Test File"** → Enter "UpdatePetTest"
3. **Click ✓** → Physical file renamed on disk

**What Happens:**
```
User Action: Rename TestFile_01 → UpdatePetTest
System Check: Does folder exist? YES
System Action: Call backend API to rename physical file
Backend: Renames TestFile_01.py → UpdatePetTest.py
Frontend: Updates UI (data-file-name="UpdatePetTest")
Notification: "File renamed successfully: TestFile_01.py → UpdatePetTest.py"

User Action: Execute Test
System Action: Read data-file-name → "UpdatePetTest"
Result: Executes rest_test/TestComponent_01/UpdatePetTest.py ✅
```

### Scenario 3: Rename When File Not Found

**Steps:**
1. Generate test code → Creates `TestFile_01.py`
2. **Manually delete** `TestFile_01.py` from disk
3. **Click "Rename Test File"** → Enter "DeletePetTest"
4. **Click ✓** → UI updates (file doesn't exist to rename)

**What Happens:**
```
User Action: Rename TestFile_01 → DeletePetTest
System Check: Does folder exist? YES
System Action: Call backend API to rename physical file
Backend: File not found error
Frontend: Detects "not found" in error message
Frontend Action: Update UI only (data-file-name="DeletePetTest")
Notification: "File name updated to 'DeletePetTest'. File will be created with this name when you generate code."

User Action: Generate Test Code
System Action: Read data-file-name → "DeletePetTest"
Result: Creates rest_test/TestComponent_01/DeletePetTest.py ✅
```

## 🔍 Decision Logic

```javascript
// Pseudo-code for rename logic
function saveTestClassName(id, newName) {
    // Get folder name
    const folderName = getFolderName();
    
    if (!folderName || folderName === '') {
        // Case 1: No folder set yet
        updateUIOnly(newName);
        showNotification("File will be created with this name");
    } else {
        // Case 2: Folder exists, try to rename physical file
        const result = callBackendRenameAPI(folderName, oldName, newName);
        
        if (result.success) {
            // Physical file renamed
            updateUIOnly(newName);
            showNotification("File renamed successfully");
        } else if (result.message.includes('not found')) {
            // File doesn't exist yet
            updateUIOnly(newName);
            showNotification("File will be created with this name");
        } else {
            // Other error
            showError(result.message);
        }
    }
}
```

## 📊 Comparison Table

| Scenario | Folder Exists? | File Exists? | Backend Called? | Physical Rename? | UI Updated? | File Created As |
|----------|---------------|--------------|-----------------|------------------|-------------|-----------------|
| **Before Generation** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes | New name |
| **After Generation** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | N/A (renamed) |
| **File Deleted** | ✅ Yes | ❌ No | ✅ Yes (fails) | ❌ No | ✅ Yes | New name |

## 🎯 Key Benefits

### 1. **Flexibility**
- Rename anytime - before or after file creation
- No need to generate first, then rename

### 2. **Better Workflow**
```
Old Workflow:
1. Generate → TestFile_01.py created
2. Rename → TestFile_01.py → CreatePetTest.py
3. Execute → Uses CreatePetTest.py

New Workflow:
1. Rename → UI shows CreatePetTest
2. Generate → CreatePetTest.py created directly
3. Execute → Uses CreatePetTest.py
```

### 3. **Intelligent Handling**
- Automatically detects if file exists
- Calls backend only when needed
- Gracefully handles all edge cases

## 🧪 Testing Guide

### Test 1: Rename Before Generation
```
1. Open UI → http://localhost:5000
2. Go to Generator tab
3. Add Test Component
4. Add Test Class (shows "TestFile_01")
5. Click "Rename Test File"
6. Enter: "CreatePetTest"
7. Click ✓
8. Expected: Blue notification "File name set to 'CreatePetTest'..."
9. Generate test code
10. Expected: Creates CreatePetTest.py (not TestFile_01.py)
11. Check disk: rest_test/TestComponent_01/CreatePetTest.py exists ✅
```

### Test 2: Rename After Generation
```
1. Generate test code (creates TestFile_01.py)
2. Click "Rename Test File"
3. Enter: "UpdatePetTest"
4. Click ✓
5. Expected: Green notification "File renamed successfully..."
6. Check disk: UpdatePetTest.py exists, TestFile_01.py deleted ✅
```

### Test 3: Rename Multiple Times Before Generation
```
1. Add Test Class (shows "TestFile_01")
2. Rename to "CreatePetTest" → UI updates
3. Rename to "PetStoreTest" → UI updates
4. Rename to "FinalTestName" → UI updates
5. Generate test code
6. Expected: Creates FinalTestName.py ✅
```

### Test 4: Rename, Generate, Rename Again
```
1. Rename to "CreatePetTest" (before generation)
2. Generate → Creates CreatePetTest.py
3. Rename to "UpdatePetTest" (after generation)
4. Expected: Physical file renamed on disk ✅
```

## 💡 Console Logging

The system logs different messages based on the scenario:

### Before Generation
```
Folder name not set - updating UI only (file will be created with new name)
Updated data-file-name to: CreatePetTest (UI only - no folder set yet)
```

### After Generation (Success)
```
Updated data-file-name to: UpdatePetTest (file renamed on disk)
```

### File Not Found
```
File not found on disk - updating UI only (file will be created with new name)
Updated data-file-name to: DeletePetTest (UI only - file doesn't exist yet)
```

## 🎨 Notification Types

### Info (Blue) - UI Only Update
```
"File name set to 'CreatePetTest'. File will be created with this name when you generate code."
```
**When:** File doesn't exist yet

### Success (Green) - Physical Rename
```
"File renamed successfully: TestFile_01.py → CreatePetTest.py"
```
**When:** Physical file renamed on disk

### Error (Red) - Rename Failed
```
"Failed to rename file: [error message]"
```
**When:** Unexpected error (not "file not found")

## 🔧 Technical Details

### Data Attribute Storage
```html
<!-- Initial state -->
<div class="test-class-section" data-file-name="TestFile_01">

<!-- After rename (before generation) -->
<div class="test-class-section" data-file-name="CreatePetTest">
```

### Generate Function Reads Attribute
```javascript
// In runGenerator()
const fileName = testClassSection.getAttribute('data-file-name');
// Returns: "CreatePetTest" (not "TestFile_01")

// Sends to backend
body: JSON.stringify({
    file_name: "CreatePetTest"  // Uses renamed name!
})
```

### Backend Creates File
```python
# In run_generator route
file_name = data.get('file_name')  # "CreatePetTest"
# Creates: rest_test/TestComponent_01/CreatePetTest.py
```

## ✅ Validation

### What Gets Validated
- ✅ New name is not empty
- ✅ Component number and class number are valid
- ✅ Folder name input exists (for backend call)

### What Doesn't Fail
- ✅ File doesn't exist yet (UI update only)
- ✅ Folder doesn't exist yet (UI update only)
- ✅ Multiple renames before generation (last one wins)

## 🚀 Production Ready

This feature is **fully tested and production-ready**!

### Checklist
- [x] Rename before file exists
- [x] Rename after file exists
- [x] Rename when file not found
- [x] Rename when folder not set
- [x] Multiple renames before generation
- [x] UI updates correctly
- [x] Data attribute updates correctly
- [x] Generate uses renamed name
- [x] Execute uses renamed name
- [x] Proper notifications
- [x] Console logging
- [x] Error handling

## 📝 Summary

**Old Behavior:** Could only rename after file was created

**New Behavior:** Can rename anytime - before or after creation

**Key Innovation:** Intelligent detection of file existence + graceful fallback to UI-only updates

**Result:** More flexible, intuitive workflow! ✅

---

**Status:** ✅ COMPLETE
**Date:** 2026-08-08
**Version:** 2.0
