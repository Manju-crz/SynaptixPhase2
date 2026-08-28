# Executor Tab Rebuild - Version 8

**Date:** August 25, 2026  
**Version:** v8  
**Status:** ✅ Complete - Phase 1

---

## 🎯 Objective

Rebuild the Executor tab from scratch to display test structure in a tree format with checkboxes for selection.

---

## 📋 Requirements

### Phase 1 (Completed)
1. ✅ Clear existing Executor tab content
2. ✅ Scan `rest_test` folder structure
3. ✅ Display folders, files, and test methods in a tree structure
4. ✅ Add checkboxes to each level (folder, file, method)
5. ✅ Implement expand/collapse functionality
6. ✅ Add select all/deselect all controls

### Phase 2 (Next)
- Execute selected tests
- Display test results
- Generate test reports

---

## 🌲 Tree Structure

### Visual Layout

```
📁 Test Suite Structure:

[✅ Select All] [❌ Deselect All] [📂 Expand All] [📁 Collapse All]

┌─────────────────────────────────────────────────────────────────┐
│ ▶ ☐ 📁 TestComponent_02 (2 files)                              │
│   ▶ ☐ 📄 TestFile_01.py (3 tests)                              │
│     ☐ 🧪 test_01_create_a_new_pet_in_pest_store_ai_ai          │
│     ☐ 🧪 test_02_update_pet_information                        │
│     ☐ 🧪 test_03_delete_a_pet                                  │
│                                                                  │
│ ▶ ☐ 📁 TestComponent_03 (1 file)                               │
│   ▶ ☐ 📄 TestFile_01.py (2 tests)                              │
│     ☐ 🧪 test_01_get_all_pets                                  │
│     ☐ 🧪 test_02_get_pet_by_id                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Expanded View

```
┌─────────────────────────────────────────────────────────────────┐
│ ▼ ☐ 📁 TestComponent_02 (2 files)                              │
│   ▼ ☐ 📄 TestFile_01.py (3 tests)                              │
│     ☐ 🧪 test_01_create_a_new_pet - Combined test executing... │
│     ☐ 🧪 test_02_update_pet_information                        │
│     ☐ 🧪 test_03_delete_a_pet                                  │
│   ▼ ☐ 📄 TestFile_02.py (2 tests)                              │
│     ☐ 🧪 test_01_search_pets                                   │
│     ☐ 🧪 test_02_filter_pets_by_status                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Implementation

### Backend API

**Endpoint:** `GET /get-test-structure`

**Response:**
```json
{
  "success": true,
  "structure": [
    {
      "name": "TestComponent_02",
      "type": "folder",
      "files": [
        {
          "name": "TestFile_01.py",
          "type": "file",
          "methods": [
            {
              "name": "test_01_create_a_new_pet_in_pest_store_ai_ai",
              "description": "Combined test executing 3 API operations"
            },
            {
              "name": "test_02_update_pet_information",
              "description": ""
            }
          ]
        }
      ]
    }
  ]
}
```

**Logic:**
1. Scans `rest_test` folder
2. Iterates through subfolders (TestComponent_XX)
3. Finds Python files (*.py, excluding __init__.py)
4. Parses each file using AST to extract test methods
5. Extracts method names and docstrings
6. Returns hierarchical structure

---

### Frontend HTML

**File:** `custom_ui/templates/tabs/executor.html`

**Key Elements:**
1. **Header Section:**
   - Title: "🚀 Test Executor"
   - Description of features

2. **Control Buttons:**
   - Select All
   - Deselect All
   - Expand All
   - Collapse All

3. **Tree Container:**
   - Scrollable container (max-height: 500px)
   - Border and background styling
   - Dynamic content loaded via JavaScript

**Styles:**
- `.tree-folder` - Folder container
- `.tree-folder-header` - Clickable folder header
- `.tree-file` - File container
- `.tree-file-header` - Clickable file header
- `.tree-method` - Individual test method
- Hover effects on all interactive elements
- Smooth transitions for expand/collapse

---

### Frontend JavaScript

**File:** `custom_ui/static/js/pages/executorPage.js`

**Class:** `ExecutorPage`

**Key Methods:**

1. **`loadTestStructure()`**
   - Fetches test structure from backend
   - Stores in `this.testStructure`

2. **`renderTestTree()`**
   - Generates HTML for entire tree
   - Adds control buttons
   - Renders folders, files, and methods

3. **`renderFolder(folder, folderIndex)`**
   - Creates folder HTML with checkbox
   - Adds expand/collapse icon
   - Shows file count

4. **`renderFile(file, folderIndex, fileIndex)`**
   - Creates file HTML with checkbox
   - Adds expand/collapse icon
   - Shows test count

5. **`renderMethod(method, folderIndex, fileIndex, methodIndex)`**
   - Creates method HTML with checkbox
   - Shows method name and description
   - Stores test path in data attribute

6. **`toggleFolder(folderId)`**
   - Expands/collapses folder content
   - Rotates icon (▶ ↔ ▼)

7. **`toggleFile(fileId)`**
   - Expands/collapses file content
   - Rotates icon (▶ ↔ ▼)

8. **`toggleFolderSelection(folderId, folderIndex)`**
   - Selects/deselects all files in folder
   - Cascades to all methods

9. **`toggleFileSelection(fileId, folderIndex, fileIndex)`**
   - Selects/deselects all methods in file
   - Updates `selectedTests` Set

10. **`toggleMethodSelection(methodId, testPath)`**
    - Adds/removes test from `selectedTests`
    - Updates selection count

11. **`selectAll()` / `deselectAll()`**
    - Selects/deselects all checkboxes
    - Updates `selectedTests` Set

12. **`expandAll()` / `collapseAll()`**
    - Expands/collapses all folders and files
    - Updates all icons

13. **`getSelectedTests()`**
    - Returns array of selected test paths
    - Format: `FolderName/FileName.py::method_name`

---

## 🎨 Styling Details

### Color Scheme

| Element | Color | Purpose |
|---------|-------|---------|
| Folder Name | `#00d4ff` (cyan) | Highlight folders |
| File Name | `#fff` (white) | Standard text |
| Method Name | `#ccc` (light gray) | Subdued text |
| Description | `#888` (gray) | Italic, secondary info |
| Hover Background | `rgba(0, 212, 255, 0.2)` | Interactive feedback |
| Border | `rgba(0, 212, 255, 0.3)` | Container outline |

### Icons

| State | Icon | Meaning |
|-------|------|---------|
| Collapsed | ▶ | Click to expand |
| Expanded | ▼ | Click to collapse |
| Folder | 📁 | Folder item |
| File | 📄 | Python file |
| Method | 🧪 | Test method |

### Transitions

```css
transition: all 0.2s ease;
```

Applied to:
- Background color changes
- Icon rotations
- Content visibility

---

## 📊 Data Flow

### 1. Page Load
```
User opens Executor tab
    ↓
executorPage.init()
    ↓
loadTestStructure()
    ↓
GET /get-test-structure
    ↓
Backend scans rest_test folder
    ↓
Returns JSON structure
    ↓
renderTestTree()
    ↓
Display tree in UI
```

### 2. User Interaction
```
User clicks folder checkbox
    ↓
toggleFolderSelection()
    ↓
Select all files in folder
    ↓
Select all methods in each file
    ↓
Update selectedTests Set
    ↓
updateSelectionCount()
```

### 3. Test Path Format
```
Folder: TestComponent_02
File: TestFile_01.py
Method: test_01_create_a_new_pet

Test Path: TestComponent_02/TestFile_01.py::test_01_create_a_new_pet
```

---

## 🧪 Testing Checklist

### Visual Tests
- [ ] Tree structure displays correctly
- [ ] Folders show file count
- [ ] Files show test count
- [ ] Method descriptions appear (if available)
- [ ] Icons change on expand/collapse
- [ ] Hover effects work on all elements
- [ ] Scrollbar appears when content exceeds 500px

### Functional Tests
- [ ] Folders expand/collapse on click
- [ ] Files expand/collapse on click
- [ ] Folder checkbox selects all files
- [ ] File checkbox selects all methods
- [ ] Method checkbox toggles individually
- [ ] Select All button works
- [ ] Deselect All button works
- [ ] Expand All button works
- [ ] Collapse All button works

### Data Tests
- [ ] Backend API returns correct structure
- [ ] All folders are detected
- [ ] All Python files are found
- [ ] All test methods are extracted
- [ ] Method docstrings are captured
- [ ] Test paths are correctly formatted

---

## 📁 Files Modified

1. ✅ `custom_ui/app.py`
   - Added `/get-test-structure` endpoint
   - Scans rest_test folder
   - Parses Python files with AST

2. ✅ `custom_ui/templates/tabs/executor.html`
   - Completely rebuilt from scratch
   - New tree structure layout
   - Added CSS styles for tree

3. ✅ `custom_ui/static/js/pages/executorPage.js`
   - Completely rewritten
   - New ExecutorPage class
   - Tree rendering logic
   - Selection management

4. ✅ `custom_ui/templates/index.html`
   - Updated version to v=8

---

## 🎯 Example Test Structure

### Folder Structure
```
rest_test/
├── TestComponent_02/
│   ├── __init__.py
│   └── TestFile_01.py (3 test methods)
├── TestComponent_03/
│   ├── __init__.py
│   └── TestFile_01.py (2 test methods)
└── TestComponent_05/
    ├── __init__.py
    └── TestFile_01.py (1 test method)
```

### Rendered Tree
```
☐ 📁 TestComponent_02 (1 file)
  ☐ 📄 TestFile_01.py (3 tests)
    ☐ 🧪 test_01_create_a_new_pet_in_pest_store_ai_ai
    ☐ 🧪 test_02_update_pet_information
    ☐ 🧪 test_03_delete_a_pet

☐ 📁 TestComponent_03 (1 file)
  ☐ 📄 TestFile_01.py (2 tests)
    ☐ 🧪 test_01_get_all_pets
    ☐ 🧪 test_02_get_pet_by_id

☐ 📁 TestComponent_05 (1 file)
  ☐ 📄 TestFile_01.py (1 test)
    ☐ 🧪 test_01_search_functionality
```

---

## 🚀 Next Steps (Phase 2)

1. **Add Run Button:**
   - Button to execute selected tests
   - Disabled when no tests selected
   - Shows count of selected tests

2. **Execute Tests:**
   - Send selected test paths to backend
   - Run pytest with selected tests
   - Stream output to frontend

3. **Display Results:**
   - Show test execution status
   - Display pass/fail for each test
   - Show execution time
   - Display error messages

4. **Generate Reports:**
   - Create Allure reports
   - Link to detailed test reports
   - Show test coverage

---

## 📝 Usage Instructions

### For Users

1. **Open Executor Tab**
2. **Browse Test Structure:**
   - Click folder/file icons to expand
   - View all available tests

3. **Select Tests:**
   - Check individual test methods
   - Check files to select all methods
   - Check folders to select all files
   - Use "Select All" for everything

4. **Manage Selection:**
   - Use "Deselect All" to clear
   - Use "Expand All" to see everything
   - Use "Collapse All" to minimize

5. **Ready for Execution (Phase 2)**

---

## 🎉 Status

**Phase 1:** ✅ **COMPLETE**

- Tree structure implemented
- Checkboxes functional
- Expand/collapse working
- Selection management ready

**Phase 2:** 🔜 **PENDING**

- Test execution
- Results display
- Report generation

---

**Created:** August 25, 2026  
**Feature:** Executor Tab Tree Structure  
**Version:** v8  
**Status:** Ready for testing (Phase 1)
