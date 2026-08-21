# File Rename Utility - Integration Guide

## Overview
The file rename utility allows users to rename test files directly from the UI. When a user renames a file in any component tab, the actual physical file on disk is renamed.

## Components

### 1. Backend API (`app.py`)
**Route:** `/rename-file`
**Method:** POST

**Request Payload:**
```json
{
  "folder_name": "TestComponent_01",
  "existing_file_name": "TestFile_01",
  "new_file_name": "TestFile_Updated"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully renamed 'TestFile_01.py' to 'TestFile_Updated.py' in folder '...'",
  "old_file_name": "TestFile_01.py",
  "new_file_name": "TestFile_Updated.py",
  "old_file_path": "C:\\...\\rest_test\\TestComponent_01\\TestFile_01.py",
  "new_file_path": "C:\\...\\rest_test\\TestComponent_01\\TestFile_Updated.py"
}
```

### 2. Utility Function (`file_rename_util.py`)
**Function:** `rename_file_in_folder(folder_name, existing_file_name, new_file_name, project_root=None, search_recursive=True)`

**Features:**
- ✅ Recursively searches for the folder in the project
- ✅ Validates file existence before renaming
- ✅ Checks if target file already exists
- ✅ Automatic extension handling (.py)
- ✅ Comprehensive error handling
- ✅ Detailed logging

### 3. Frontend Integration (`script.js`)
**Function:** `saveTestClassName(id, event)`

**Flow:**
1. User clicks "Rename Test File" link in component tab
2. Input field appears with current file name
3. User enters new file name and clicks ✓ (save button)
4. JavaScript extracts:
   - Component number and class number from element ID
   - Folder name from component's folder input field
   - Existing file name (derived from class number)
5. Calls `/rename-file` API endpoint
6. Shows success/error notification
7. Updates UI with new file name

## User Workflow

### Step 1: Generate Test Code
1. Navigate to the Generator tab
2. Create a test component (e.g., "TestComponent_01")
3. Add a test class (e.g., "TestFile_01")
4. Generate test code
   - This creates the actual file: `rest_test/TestComponent_01/TestFile_01.py`

### Step 2: Rename Test File
1. Click the "Rename Test File" link next to the test class name
2. Enter the new file name (e.g., "CreatePetTest")
3. Click the ✓ button to save
4. The system will:
   - Rename the physical file on disk
   - Update the UI to show the new name
   - Show a success notification

### Step 3: Verify
The file `rest_test/TestComponent_01/TestFile_01.py` is now renamed to `rest_test/TestComponent_01/CreatePetTest.py`

## Error Handling

### Common Errors

1. **Folder not found**
   - Error: "Folder 'TestComponent_01' not found in project"
   - Solution: Ensure test code has been generated first

2. **File not found**
   - Error: "File 'TestFile_01.py' not found in folder '...'"
   - Solution: Verify the file exists in the specified folder

3. **Target file already exists**
   - Error: "File 'CreatePetTest.py' already exists in folder '...'"
   - Solution: Choose a different name or delete the existing file

4. **Folder name not set**
   - Error: "Folder name is not set. Please generate test code first."
   - Solution: Generate test code before attempting to rename

## API Testing

### Using cURL
```bash
curl -X POST http://localhost:5000/rename-file \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "TestComponent_01",
    "existing_file_name": "TestFile_01",
    "new_file_name": "CreatePetTest"
  }'
```

### Using Python
```python
import requests

response = requests.post(
    'http://localhost:5000/rename-file',
    json={
        'folder_name': 'TestComponent_01',
        'existing_file_name': 'TestFile_01',
        'new_file_name': 'CreatePetTest'
    }
)

print(response.json())
```

## Code Examples

### Direct Utility Usage
```python
from generator_altUtl import rename_file_in_folder

# Rename a test file
result = rename_file_in_folder(
    folder_name='TestComponent_01',
    existing_file_name='TestFile_01.py',
    new_file_name='CreatePetTest.py'
)

if result['success']:
    print(f"✓ {result['message']}")
    print(f"  Old: {result['old_file_path']}")
    print(f"  New: {result['new_file_path']}")
else:
    print(f"✗ {result['message']}")
```

### With Extension Handling
```python
from generator_altUtl import rename_file_with_extension_handling

# Automatically preserves .py extension
result = rename_file_with_extension_handling(
    folder_name='TestComponent_01',
    existing_file_name='TestFile_01.py',
    new_file_name='CreatePetTest'  # .py will be added automatically
)

print(result['new_file_name'])  # Output: CreatePetTest.py
```

## Best Practices

1. **Always generate test code first** before attempting to rename
2. **Use descriptive names** that reflect the test's purpose (e.g., "CreatePetTest", "UpdateUserTest")
3. **Avoid special characters** in file names (stick to letters, numbers, underscores)
4. **Check for existing files** before renaming to avoid conflicts
5. **Use the UI** for renaming rather than manual file system operations

## Troubleshooting

### Issue: "Folder name is not set"
**Cause:** The component's folder input field is empty
**Solution:** 
1. Check if "Use component name as folder" checkbox is checked
2. If not, manually enter a folder name
3. Generate test code to create the folder

### Issue: File rename succeeds but UI doesn't update
**Cause:** JavaScript error or notification system not loaded
**Solution:**
1. Check browser console for errors
2. Refresh the page
3. Verify the file was actually renamed on disk

### Issue: Permission denied error
**Cause:** File is open in another program or insufficient permissions
**Solution:**
1. Close any editors with the file open
2. Check file permissions
3. Run the application with appropriate permissions

## Related Files

- **Backend:** `c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui\app.py` (line 597-652)
- **Utility:** `c:\DATA\VS_Code_Notes\SynaptixPhase2\generator_altUtl\file_rename_util.py`
- **Frontend:** `c:\DATA\VS_Code_Notes\SynaptixPhase2\custom_ui\static\script.js` (line 349-438)
- **Tests:** `c:\DATA\VS_Code_Notes\SynaptixPhase2\generator_altUtl\test_file_rename.py`

## Future Enhancements

- [ ] Batch rename multiple files
- [ ] Rename with pattern matching (e.g., TestFile_* → Test_*)
- [ ] Undo/redo rename operations
- [ ] Rename history tracking
- [ ] Validation for Python naming conventions
- [ ] Auto-update import statements in other files
