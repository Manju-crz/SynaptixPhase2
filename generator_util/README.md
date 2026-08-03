# generator_util

Utility package for generating pytest test files from Excel-based API metadata.

## Files

- `__init__.py` - Package export for `CodeGenerator`
- `code_generator_util.py` - Core generator implementation
- `example_code_generator_usage.py` - Example usage script
- `README.md` - Package documentation

## Usage

```python
from generator_util import CodeGenerator

generator = CodeGenerator(
    excel_path=r"C:\BLK\Developer\Synaptix\Rest_API_Data\Swagger_Data.xlsx",
    base_url="https://api.example.com"
)
result = generator.generate_test_file(
    sl_nos=[1, 2],
    queries=["Get pets", "Create pet"],
    folder_name="generated_tests",
    filename="test_pet_workflow"
)
print(result)
```

## Notes

- Generated test files are placed in the provided `folder_name`.
- `filename` should be provided without the `.py` extension.
