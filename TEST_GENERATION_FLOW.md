# Test Generation Flow - Updated Architecture

## Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (Generator Tab)                    │
│  - Excel File Selection                                                  │
│  - Base URL                                                              │
│  - Folder/File Name                                                      │
│  - Query with Instructions: "Create pet → Extract pet_id"               │
│  - AI Model Selection (OpenAI/DeepSeek/Groq)                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ Click "Generate Test Code"
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (/run-generator)                        │
│  1. Parse queries (split by semicolon)                                  │
│  2. Extract main actions (before → or ->)                               │
│  3. Semantic search for matching APIs (Sl_No)                           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              CODE GENERATOR (generator_util)                             │
│  - Read Excel data for each Sl_No                                       │
│  - Parse parameters (header, query, path, body)                         │
│  - Convert schemas to examples                                          │
│  - Generate pytest test method                                          │
│  - Create file: rest_test/{folder}/{file}.py                           │
│                                                                          │
│  OUTPUT: test_01_create_a_new_pet_in_pest_store()                      │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│           TEST METHOD READER (generator_aiUtil)                          │
│  - Parse file with AST                                                  │
│  - Extract generated method code                                        │
│  - Return method details (name, code, line count, step count)          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Instructions detected? │
                    │  (→ or -> in query)    │
                    └──────┬─────────┬───────┘
                           │ NO      │ YES
                           │         │
                           │         ▼
                           │    ┌─────────────────────────────────────────┐
                           │    │  PARAMETER EXTRACTOR (ext_util)         │
                           │    │  - Extract Excel data for each Sl_No    │
                           │    │  - Get operation details                │
                           │    │  - Get all parameters                   │
                           │    │  - Get request/response examples        │
                           │    └──────────────┬──────────────────────────┘
                           │                   │
                           │                   ▼
                           │    ┌─────────────────────────────────────────┐
                           │    │  AI CODE MODIFIER (generator_aiUtil)    │
                           │    │  1. Parse query instructions            │
                           │    │  2. Build AI prompt with:               │
                           │    │     - Original code                     │
                           │    │     - Excel data                        │
                           │    │     - Instructions                      │
                           │    │  3. Call AI model (OpenAI/DeepSeek/Groq)│
                           │    │  4. Get enhanced code                   │
                           │    │  5. **REPLACE** original method         │
                           │    │     ✓ Remove original method            │
                           │    │     ✓ Insert AI version at same spot   │
                           │    │     ✓ Rename with _ai suffix           │
                           │    └──────────────┬──────────────────────────┘
                           │                   │
                           │                   ▼
                           │         ┌─────────────────────┐
                           │         │  AI-Enhanced Method │
                           │         │  with _ai suffix    │
                           │         └─────────┬───────────┘
                           │                   │
                           └───────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CODE VALIDATOR                                      │
│  - Compile Python code                                                  │
│  - Check for syntax errors                                              │
│  - Return validation results                                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      RETURN TO UI                                        │
│  - Success/Failure status                                               │
│  - Generated code (BOTH methods for UI display):                        │
│    1. Original method (for reference/comparison)                        │
│    2. AI-enhanced method (actual file content)                          │
│  - File path                                                            │
│  - Validation results                                                   │
│  - Logs                                                                 │
│                                                                          │
│  NOTE: File contains only AI method, UI shows both                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Change: Replace vs Append

### OLD BEHAVIOR (Before Modification)
```python
# Generated file: test45.py
class TestGeneratedAPIs:
    
    def test_01_create_a_new_pet_in_pest_store(self):
        """Standard generated method"""
        # Basic code without data extraction
        pass
    
    def test_01_create_a_new_pet_in_pest_store_ai(self):
        """AI-enhanced method - APPENDED"""
        # Enhanced code with data extraction
        pass
```

### NEW BEHAVIOR (After Modification)
```python
# Generated file: test45.py (ACTUAL FILE CONTENT)
class TestGeneratedAPIs:
    
    def test_01_create_a_new_pet_in_pest_store_ai(self):
        """AI-enhanced method - REPLACED original"""
        # Enhanced code with data extraction
        pass

# UI Display (FOR REFERENCE ONLY - NOT IN FILE)
# Shows both methods:
# 1. test_01_create_a_new_pet_in_pest_store (original - for comparison)
# 2. test_01_create_a_new_pet_in_pest_store_ai (enhanced - actual file content)
```

## Method Replacement Logic

```
┌─────────────────────────────────────────────────────────────┐
│  replace_method_with_ai_version()                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Parse file with AST                                     │
│     ├─ Find original method by name                        │
│     ├─ Locate decorators (if any)                          │
│     └─ Get method boundaries (start/end lines)             │
│                                                             │
│  2. Prepare AI code                                         │
│     ├─ Rename method: add _ai suffix                       │
│     ├─ Indent properly for class                           │
│     └─ Preserve all decorators                             │
│                                                             │
│  3. Replace in file                                         │
│     ├─ Remove: lines[decorator_start:method_end]           │
│     ├─ Insert: AI-enhanced code at same position           │
│     └─ Write back to file                                  │
│                                                             │
│  4. Return result                                           │
│     └─ new_method_name, file_path, replaced=True           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow for Instructions

```
Query: "Create pet → Extract pet_id; Update pet → Use pet_id"
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│  Parse Instructions                                       │
│  ─────────────────────────────────────────────────────── │
│  Step 1:                                                  │
│    main_action: "Create pet"                              │
│    instructions: ["Extract pet_id"]                       │
│                                                           │
│  Step 2:                                                  │
│    main_action: "Update pet"                              │
│    instructions: ["Use pet_id"]                           │
└───────────────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│  Build AI Prompt                                          │
│  ─────────────────────────────────────────────────────── │
│  ORIGINAL CODE: [generated test method]                   │
│  EXCEL DATA: [API specs for each step]                   │
│  INSTRUCTIONS:                                            │
│    Step 1: Create pet                                     │
│      → Extract pet_id                                     │
│    Step 2: Update pet                                     │
│      → Use pet_id                                         │
│  REQUIREMENTS:                                            │
│    - Extract pet_id from response                         │
│    - Store in variable                                    │
│    - Use in next request                                  │
└───────────────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│  AI Model Response                                        │
│  ─────────────────────────────────────────────────────── │
│  def test_01_create_pet_ai(self):                         │
│      # Step 1: Create pet                                 │
│      response1 = requests.post(...)                       │
│      pet_id = response1.json()['id']  # EXTRACTED         │
│                                                           │
│      # Step 2: Update pet                                 │
│      url = f"{base_url}/pet/{pet_id}"  # USED            │
│      response2 = requests.put(url, ...)                   │
└───────────────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│  Replace Original Method                                  │
│  ─────────────────────────────────────────────────────── │
│  ✓ Original method removed from file                      │
│  ✓ AI-enhanced method inserted at same position           │
│  ✓ Only _ai method exists in final file                   │
└───────────────────────────────────────────────────────────┘
```

## Benefits of New Approach

1. **Single Source of Truth**: Only one method per test case in the file
2. **Automatic Enhancement**: No manual selection needed
3. **Cleaner Files**: Reduced code duplication in actual test files
4. **Better UX**: Users see the transformation in UI but execute only the enhanced version
5. **Maintains History**: Git shows the evolution from standard to AI-enhanced
6. **Educational Value**: UI shows both versions for learning and comparison
7. **No Confusion**: File contains only the working AI-enhanced version

## Backward Compatibility

The system still supports:
- Queries without instructions (no AI modification)
- Manual append mode (via `replace_original=False` parameter)
- Existing test files with multiple methods (only new methods are replaced)
