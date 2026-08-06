# Method Rename Utility - Test Guide

## Overview
This guide explains how to test the method rename utility using the provided test script.

## Test Script Location
`generator_altUtl/test_method_rename.py`

## How to Run

### Option 1: Interactive Menu
```bash
python generator_altUtl/test_method_rename.py
```

This will show a menu with the following options:
1. **Test validate_method_name()** - Tests the validation function
2. **List existing test methods** - Shows all methods in TestClass_01.py
3. **Interactive test** - Manually enter details to test renaming
4. **Automated test** - Quick test with predefined values
5. **Run all tests** - Runs tests 1 and 2
0. **Exit**

### Option 2: Direct Test
You can also run specific tests directly:

```python
cd generator_altUtl && python -c "from test_method_rename import test_list_existing_methods; test_list_existing_methods()"
```

## Test Scenarios

### Test 1: Validate Method Name
Tests various method names to ensure validation works correctly:
- ✅ Valid names: `test_01_valid_name`, `test_create_pet_ai`
- ❌ Invalid names: `123_invalid`, empty string, Python keywords

### Test 2: List Existing Methods
Lists all test methods currently in `rest_test/TestComponent_01/TestClass_01.py`

Example output:
```
✅ Found 6 test methods:
  1. test_01_create_a_new_pet_in_pest_store_ai
  2. test_02_create_a_new_pet_in_pest_store_ai
  3. test_03_create_a_new_pet_in_pest_store_ai
  4. test_04_create_a_new_pet_in_pest_store_ai
  5. test_05_create_a_new_pet_in_pest_store_ai
  6. test_06_create_a_new_pet_in_pest_store_ai
```

### Test 3: Interactive Test
Prompts you to enter:
- Subfolder name (default: TestComponent_01)
- File name (default: TestClass_01)
- Method name to rename (from the list shown)
- Text to append (e.g., 'updated', 'v2', 'modified')

Then shows a summary and asks for confirmation before renaming.

### Test 4: Automated Test
Automatically renames the last method in the list by appending `_test_automated`.

## Example Usage

### Example 1: Rename a specific method
```bash
python test_method_rename.py
# Choose option 3 (Interactive test)
# Enter:
#   Subfolder: TestComponent_01
#   File: TestClass_01
#   Method: test_06_create_a_new_pet_in_pest_store_ai
#   Append: updated
# Result: test_06_create_a_new_pet_in_pest_store_ai_updated
```

### Example 2: Quick validation test
```bash
python test_method_rename.py
# Choose option 1 (Test validate_method_name)
# See results for various test cases
```

## Expected Output

### Success Case
```
================================================================================
✅ SUCCESS!
================================================================================
  Message:          Successfully renamed 'test_06_..._ai' to 'test_06_..._ai_updated'
  Old method name:  test_06_create_a_new_pet_in_pest_store_ai
  New method name:  test_06_create_a_new_pet_in_pest_store_ai_updated
  File path:        C:\DATA\...\rest_test\TestComponent_01\TestClass_01.py

💡 You can verify the change by opening the test file.
================================================================================
```

### Failure Case
```
================================================================================
❌ FAILED!
================================================================================
  Error:            Method 'test_99_nonexistent' not found in file
  File path:        C:\DATA\...\rest_test\TestComponent_01\TestClass_01.py
================================================================================
```

## Troubleshooting

### Issue: "Test file not found"
**Solution:** Make sure you have generated at least one test method using the UI first.

### Issue: "Method not found in file"
**Solution:** 
1. Run option 2 to list all existing methods
2. Copy the exact method name from the list
3. Make sure there are no extra spaces

### Issue: "Method name cannot start with a digit"
**Solution:** The append text should not start with a digit. Use descriptive text like 'updated', 'v2', 'modified', etc.

### Issue: Import error
**Solution:** Make sure you're running the script from the project root directory:
```bash
cd C:\DATA\VS_Code_Notes\SynaptixPhase2
python test_method_rename.py
```

## Verifying the Rename

After a successful rename, you can verify by:

1. **Opening the test file:**
   ```bash
   code rest_test/TestComponent_01/TestClass_01.py
   ```

2. **Searching for the new method name:**
   - Press Ctrl+F
   - Search for the new method name
   - Verify it exists and the old name is gone

3. **Running the test:**
   ```bash
   pytest rest_test/TestComponent_01/TestClass_01.py::TestGeneratedAPIs::test_06_create_a_new_pet_in_pest_store_ai_updated -v
   ```

## Notes

- ⚠️ **This modifies actual test files!** Make sure you have backups or version control.
- The script uses the same utility that the Flask backend uses, so if it works here, it should work in the UI.
- All operations are logged with timestamps for debugging.
- You can run the tests multiple times - each rename creates a new method name.

## Quick Commands

```bash
# List all methods
cd generator_altUtl && python -c "from test_method_rename import test_list_existing_methods; test_list_existing_methods()"

# Test validation
cd generator_altUtl && python -c "from test_method_rename import test_validate_method_name; test_validate_method_name()"

# Run full interactive test
python generator_altUtl/test_method_rename.py
```
