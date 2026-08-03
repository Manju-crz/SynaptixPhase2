# Test Method Reader Readme

## Overview

The Test Method Reader Utility extracts and reads test methods from generated pytest files.

## Features

- Extract all test methods from a file
- Read individual test method code and details
- Count test steps and lines
- Support for complex test methods

## Usage

```python
from generator_aiUtil.test_method_reader_util import TestMethodReader

reader = TestMethodReader("test_file.py")
all_methods = reader.get_all_test_methods()

for method_name in all_methods:
    result = reader.read_test_method(method_name)
    print(result['code'])
```

## Returns

Dictionary containing:
- `success`: Boolean
- `code`: The method code
- `line_count`: Number of lines in method
- `step_count`: Number of test steps
