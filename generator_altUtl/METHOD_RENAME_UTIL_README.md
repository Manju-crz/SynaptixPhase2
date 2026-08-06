# Method Rename Utility

## Overview
The `method_rename_util.py` provides reusable functions to rename test methods in generated test files within the `rest_test` folder structure.

## Location
`generator_altUtl/method_rename_util.py`

## Functions

### 1. `rename_method_in_file()`
Renames a test method in a generated test file.

**Parameters:**
- `subfolder_name` (str): The subfolder name (e.g., 'TestComponent_01')
- `file_name` (str): The file name without extension (e.g., 'TestClass_01')
- `old_method_name` (str): The current method name to be replaced
- `new_method_name` (str): The new method name
- `project_root` (str, optional): The project root directory. If None, auto-detects.

**Returns:**
Dictionary with keys:
- `success` (bool): Whether the operation succeeded
- `message` (str): Success or error message
- `old_method_name` (str): The original method name
- `new_method_name` (str): The new method name
- `file_path` (str): The path to the modified file

**Example:**
```python
from generator_altUtl.method_rename_util import rename_method_in_file

result = rename_method_in_file(
    subfolder_name='TestComponent_01',
    file_name='TestClass_01',
    old_method_name='test_01_create_pet_ai',
    new_method_name='test_01_create_pet_ai_updated'
)

if result['success']:
    print(f"Success: {result['message']}")
else:
    print(f"Error: {result['message']}")
```

### 2. `append_to_method_name()`
Appends text to an existing method name using a delimiter.

**Parameters:**
- `subfolder_name` (str): The subfolder name (e.g., 'TestComponent_01')
- `file_name` (str): The file name without extension (e.g., 'TestClass_01')
- `old_method_name` (str): The current method name
- `append_text` (str): The text to append to the method name
- `delimiter` (str, optional): The delimiter to use. Defaults to '_'.
- `project_root` (str, optional): The project root directory. If None, auto-detects.

**Returns:**
Same dictionary format as `rename_method_in_file()`

**Example:**
```python
from generator_altUtl.method_rename_util import append_to_method_name

result = append_to_method_name(
    subfolder_name='TestComponent_01',
    file_name='TestClass_01',
    old_method_name='test_01_create_pet_ai',
    append_text='updated'
)

print(f"New method name: {result['new_method_name']}")
# Output: test_01_create_pet_ai_updated
```

### 3. `validate_method_name()`
Validates that a method name follows Python naming conventions.

**Parameters:**
- `method_name` (str): The method name to validate

**Returns:**
Tuple: `(is_valid, error_message)`
- `is_valid` (bool): True if valid, False otherwise
- `error_message` (str): Error message if invalid, None if valid

**Example:**
```python
from generator_altUtl.method_rename_util import validate_method_name

is_valid, error = validate_method_name('test_01_valid_name')
print(f"Valid: {is_valid}")  # True

is_valid, error = validate_method_name('123_invalid')
print(f"Valid: {is_valid}, Error: {error}")
# Output: Valid: False, Error: Method name cannot start with a digit
```

## Usage in Flask Backend

The utility is integrated into the Flask backend (`custom_ui/app.py`) in the `/rename-method` route:

```python
from generator_altUtl.method_rename_util import append_to_method_name, validate_method_name

@app.route('/rename-method', methods=['POST'])
def rename_method():
    data = request.get_json()
    
    # Use the utility
    result = append_to_method_name(
        subfolder_name=data['folder_name'],
        file_name=data['file_name'],
        old_method_name=data['old_method_name'],
        append_text=data['append_text'],
        delimiter='_',
        project_root=PROJECT_ROOT
    )
    
    return jsonify(result)
```

## File Structure

The utility expects the following file structure:
```
project_root/
└── rest_test/
    └── TestComponent_01/
        └── TestClass_01.py
```

## Error Handling

The utility handles the following error cases:
- File not found
- Method not found in file
- Invalid method names (Python keywords, starting with digits, etc.)
- File read/write errors

All errors are logged and returned in the result dictionary with `success: False`.

## Logging

The utility uses Python's `logging` module. Enable logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Testing

Run the utility directly to see example usage:

```bash
python generator_altUtl/method_rename_util.py
```

This will run the examples in the `__main__` block and demonstrate all three functions.
