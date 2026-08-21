# File Rename CLI - Usage Guide

## 📋 Overview

Simple command-line tool to rename test files in `rest_test` folders without needing the UI.

## 🚀 Quick Start

### Method 1: Using Python Script Directly

```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2

python generator_altUtl\rename_file_cli.py <folder_name> <existing_file> <new_file>
```

### Method 2: Using Batch File (Windows)

```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2

rename_file.bat <folder_name> <existing_file> <new_file>
```

## 📝 Usage Examples

### Example 1: Basic Rename
```bash
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
```

**What it does:**
- Searches for folder `TestComponent_01` in the project
- Finds file `TestFile_01.py` (or `TestFile_01`)
- Renames it to `CreatePetTest.py`

### Example 2: With .py Extension
```bash
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01.py CreatePetTest.py
```

**Result:** Same as Example 1 (extensions are handled automatically)

### Example 3: Different Component
```bash
python generator_altUtl\rename_file_cli.py TestComponent_02 TestFile_03 UpdateUserTest
```

### Example 4: Using Batch File
```bash
rename_file.bat TestComponent_01 TestFile_01 DeletePetTest
```

## 📂 Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `folder_name` | Name of the folder containing the file | `TestComponent_01` |
| `existing_file` | Current file name (with or without .py) | `TestFile_01` or `TestFile_01.py` |
| `new_file` | New file name (with or without .py) | `CreatePetTest` or `CreatePetTest.py` |

## ✅ Success Output

```
======================================================================
FILE RENAME OPERATION
======================================================================

📁 Folder:        TestComponent_01
📄 Existing File: TestFile_01
✨ New File:      CreatePetTest

----------------------------------------------------------------------

🔍 Searching in:  C:\DATA\VS_Code_Notes\SynaptixPhase2

⏳ Processing...

======================================================================
✅ SUCCESS!
======================================================================

Successfully renamed 'TestFile_01.py' to 'CreatePetTest.py' in folder 'C:\...\rest_test\TestComponent_01'

📂 Old Path: C:\DATA\VS_Code_Notes\SynaptixPhase2\rest_test\TestComponent_01\TestFile_01.py
📂 New Path: C:\DATA\VS_Code_Notes\SynaptixPhase2\rest_test\TestComponent_01\CreatePetTest.py

======================================================================
```

## ❌ Error Examples

### Error 1: Folder Not Found
```
======================================================================
❌ FAILED!
======================================================================

Folder 'TestComponent_99' not found in project

======================================================================
```

**Solution:** Check the folder name or create the folder first by generating test code.

### Error 2: File Not Found
```
======================================================================
❌ FAILED!
======================================================================

File 'TestFile_99.py' not found in folder 'C:\...\rest_test\TestComponent_01'

======================================================================
```

**Solution:** Verify the file exists in the specified folder.

### Error 3: Target File Already Exists
```
======================================================================
❌ FAILED!
======================================================================

File 'CreatePetTest.py' already exists in folder 'C:\...\rest_test\TestComponent_01'

======================================================================
```

**Solution:** Choose a different name or delete the existing file.

### Error 4: Missing Arguments
```
❌ Error: Incorrect number of arguments!

======================================================================
FILE RENAME UTILITY - Command Line Interface
======================================================================

Usage:
  python rename_file_cli.py <folder_name> <existing_file> <new_file>
...
```

**Solution:** Provide all three required arguments.

## 🔍 How It Works

1. **Searches recursively** for the specified folder in the project
2. **Locates the file** in that folder
3. **Validates** that the file exists and target doesn't exist
4. **Renames** the physical file on disk
5. **Reports** success or failure with detailed messages

## 🎯 Common Workflows

### Workflow 1: Rename After Generation
```bash
# 1. Generate test code in UI (creates TestFile_01.py)
# 2. Rename using CLI
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest

# 3. File is now CreatePetTest.py
```

### Workflow 2: Batch Rename Multiple Files
```bash
# Rename multiple files in sequence
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_02 UpdatePetTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_03 DeletePetTest
```

### Workflow 3: Organize Test Files
```bash
# Rename files to follow a naming convention
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 Test_Pet_Create
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_02 Test_Pet_Update
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_03 Test_Pet_Delete
```

## 🛠️ Advanced Usage

### Check if File Exists Before Renaming
```bash
# PowerShell
if (Test-Path "rest_test\TestComponent_01\TestFile_01.py") {
    python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
} else {
    Write-Host "File not found!"
}
```

### Rename with Timestamp
```bash
# PowerShell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 "Test_$timestamp"
```

### Create Batch Rename Script
Create a file `batch_rename.bat`:
```batch
@echo off
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_02 UpdatePetTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_03 DeletePetTest
echo All files renamed!
pause
```

## 📊 Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success - File renamed successfully |
| `1` | Failure - Error occurred (see error message) |

### Using Exit Codes in Scripts
```batch
@echo off
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest
if %ERRORLEVEL% EQU 0 (
    echo Success!
) else (
    echo Failed!
)
```

## 🔧 Troubleshooting

### Issue: "No module named 'generator_altUtl'"
**Solution:** Run from the project root directory:
```bash
cd c:\DATA\VS_Code_Notes\SynaptixPhase2
python generator_altUtl\rename_file_cli.py ...
```

### Issue: "Permission denied"
**Solution:** 
1. Close any editors with the file open
2. Check file permissions
3. Run as administrator if needed

### Issue: Script doesn't find the folder
**Solution:**
1. Verify the folder exists in `rest_test/`
2. Check spelling of folder name
3. Generate test code first to create the folder

## 📖 Related Commands

### List Files in a Folder
```bash
# Windows
dir rest_test\TestComponent_01\*.py

# PowerShell
Get-ChildItem rest_test\TestComponent_01\*.py
```

### Check if File Exists
```bash
# PowerShell
Test-Path rest_test\TestComponent_01\TestFile_01.py
```

### View File Contents
```bash
# Windows
type rest_test\TestComponent_01\TestFile_01.py

# PowerShell
Get-Content rest_test\TestComponent_01\TestFile_01.py
```

## 💡 Tips

1. **Use tab completion** - Type partial names and press Tab
2. **No need for .py** - Extension is added automatically
3. **Case matters** - Folder and file names are case-sensitive on some systems
4. **Check first** - List files before renaming to verify names
5. **Backup** - Consider backing up important files before renaming

## 🎓 Examples for Your Project

Based on your current file `TestFile_01.py` in `TestComponent_01`:

```bash
# Rename to CreatePetTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 CreatePetTest

# Rename to PetStoreTest
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 PetStoreTest

# Rename to Test_Create_Pet
python generator_altUtl\rename_file_cli.py TestComponent_01 TestFile_01 Test_Create_Pet
```

---

**Quick Reference Card:**
```
┌─────────────────────────────────────────────────────────────┐
│  FILE RENAME CLI - QUICK REFERENCE                          │
├─────────────────────────────────────────────────────────────┤
│  Command:                                                    │
│    python generator_altUtl\rename_file_cli.py \             │
│      <folder> <old_file> <new_file>                         │
│                                                              │
│  Example:                                                    │
│    python generator_altUtl\rename_file_cli.py \             │
│      TestComponent_01 TestFile_01 CreatePetTest             │
│                                                              │
│  Shortcut (Windows):                                        │
│    rename_file.bat TestComponent_01 TestFile_01 NewName     │
└─────────────────────────────────────────────────────────────┘
```
