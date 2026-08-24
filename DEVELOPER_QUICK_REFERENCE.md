# SynaptixPhase2 - Developer Quick Reference

**Quick reference for developers working on SynaptixPhase2**

---

## 📁 Project Structure Quick Map

```
SynaptixPhase2/
├── custom_ui/              # 🌐 Web UI (Flask + JavaScript)
│   ├── app.py              # Flask routes (21 routes)
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, assets
│       └── js/pages/       # Page controllers (5 files)
│
├── executor_util/          # 🚀 API execution engine
├── generator_util/         # ⚡ Test code generation
├── generator_aiUtil/       # 🤖 AI code enhancement
├── generator_altUtl/       # 🔧 File/method/class management
├── nlp/                    # 🔍 Semantic search (NLP)
├── loader/                 # 📂 Test loader & prompt manager
├── openapi_json/           # 📄 OpenAPI parser
├── swagger/                # 🌐 Swagger scraper
├── rest_util/              # 🌍 REST client
└── ext_util/               # 📊 Excel & parameter utilities
```

---

## 🔑 Key Files Reference

| File | Purpose | Key Functions/Routes |
|------|---------|---------------------|
| `custom_ui/app.py` | Flask backend | 21 routes (see below) |
| `generator_util/code_generator_util.py` | Test code generation | `generate_test_file()` |
| `generator_aiUtil/ai_code_modifier_util.py` | AI enhancement | `modify_generated_code_with_ai()` |
| `nlp/semantic_search_util.py` | Semantic search | `get_best_match_sl_no()` |
| `executor_util/executor_util.py` | API execution | `execute_api_call()` |
| `loader/test_loader.py` | Load existing tests | `load_existing_tests()` |
| `loader/prompt_manager.py` | Manage prompts | `save_prompts()`, `load_prompts()` |

---

## 🛣️ Flask Routes Quick Reference

### Core Routes
```python
GET  /                          # Main UI page
GET  /get-excel-files           # List Excel files
```

### Swagger/OpenAPI Routes
```python
POST /run-test                  # Swagger UI scraper
POST /run-json-parser           # OpenAPI JSON parser
```

### Executor Routes
```python
POST /run-executor              # Execute API calls
```

### Generator Routes
```python
POST /run-generator             # Generate test code
POST /execute-generated-test    # Execute single test
POST /execute-class-tests       # Execute class tests
GET  /check-test-status/<id>    # Check test status
POST /show-allure-report        # Generate Allure report
POST /clear-execution-results   # Clear results
GET  /allure-report/<filename>  # Serve report files
```

### Test Management Routes
```python
GET  /load-existing-tests       # Load test structure
POST /update-prompt             # Update method prompt
POST /rename-method             # Rename test method
POST /delete-method             # Delete test method
POST /rename-file               # Rename test file
POST /delete-file               # Delete test file
POST /rename-class              # Rename test class
POST /rename-component          # Rename component
POST /delete-component          # Delete component
```

---

## 🎯 Common Development Tasks

### 1. Add a New Flask Route

**File:** `custom_ui/app.py`

```python
@app.route('/your-new-route', methods=['POST'])
def your_new_route():
    """Your route description"""
    data = request.get_json()
    
    # Your logic here
    
    return jsonify({
        'success': True,
        'message': 'Success message',
        'data': {}
    })
```

### 2. Add a New Frontend Page

**Files to create/modify:**
1. `custom_ui/templates/tabs/your_tab.html` - HTML template
2. `custom_ui/static/js/pages/yourPage.js` - JavaScript controller
3. `custom_ui/templates/index.html` - Add tab navigation

**Example JavaScript Page Controller:**
```javascript
class YourPage {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add event listeners
    }

    async yourMethod() {
        try {
            const response = await fetch('/your-route', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            });
            const data = await response.json();
            
            if (data.success) {
                notification.success(data.message);
            } else {
                notification.error(data.message);
            }
        } catch (error) {
            notification.error('Error: ' + error.message);
        }
    }
}

// Initialize
const yourPage = new YourPage();
```

### 3. Add a New Utility Module

**Example structure:**
```python
# your_util/your_utility.py

import logging

logger = logging.getLogger(__name__)

class YourUtility:
    """Your utility description"""
    
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        logger.info(f"Initialized YourUtility")
    
    def your_method(self):
        """Your method description"""
        try:
            # Your logic
            logger.info("Success message")
            return {'success': True, 'data': {}}
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {'success': False, 'error': str(e)}
```

### 4. Modify AI Code Generation

**File:** `generator_aiUtil/ai_code_modifier_util.py`

**Key function:** `modify_generated_code_with_ai()`

**To add a new AI provider:**
1. Add API key to `.env`
2. Add provider logic in `ai_code_modifier_util.py`
3. Update UI dropdown in `configurationPage.js`

### 5. Modify Semantic Search

**File:** `nlp/semantic_search_util.py`

**To change search columns:**
```python
search_columns = [
    'Component',
    'Operation_Summary',
    'Operation_Path',
    # Add more columns
]
search_engine = SemanticSearchEngine(
    excel_path, 
    search_columns=search_columns
)
```

---

## 🔧 Utility Functions Quick Reference

### File Management (generator_altUtl/)

```python
# Rename file
from generator_altUtl.file_rename_util import rename_file_in_folder
result = rename_file_in_folder(
    folder_name='TestComponent_01',
    existing_file_name='TestFile_01',
    new_file_name='TestFile_02'
)

# Delete file
from generator_altUtl.file_delete_util import delete_test_file
result = delete_test_file(
    subfolder_name='TestComponent_01',
    file_name='TestFile_01'
)

# Delete component
from generator_altUtl.file_delete_util import delete_component
result = delete_component(
    subfolder_name='TestComponent_01'
)
```

### Method Management (generator_altUtl/)

```python
# Rename method
from generator_altUtl.method_rename_util import rename_method_in_file
result = rename_method_in_file(
    subfolder_name='TestComponent_01',
    file_name='TestFile_01',
    old_method_name='test_01_old_name',
    new_method_name='test_01_new_name'
)

# Remove method
from generator_altUtl.method_remove_util import remove_method_from_file
result = remove_method_from_file(
    subfolder_name='TestComponent_01',
    file_name='TestFile_01',
    method_name='test_01_to_remove'
)
```

### Class Management (generator_altUtl/)

```python
# Rename class
from generator_altUtl.class_rename_util import rename_class_in_file
result = rename_class_in_file(
    subfolder_name='TestComponent_01',
    file_name='TestFile_01',
    old_class_name='OldClassName',
    new_class_name='NewClassName'
)
```

### Prompt Management (loader/)

```python
# Save prompts
from loader.prompt_manager import save_prompts
save_prompts(
    project_root='/path/to/project',
    component='TestComponent_01',
    file_name='TestFile_01',
    prompts={
        'test_01_method': 'Create pet → Extract pet_id'
    }
)

# Load prompts
from loader.prompt_manager import load_prompts
prompts = load_prompts(
    project_root='/path/to/project',
    component='TestComponent_01',
    file_name='TestFile_01'
)
```

### Excel Operations (ext_util/)

```python
# Extract parameters
from ext_util.parameter_extractor_util import ParameterExtractor
extractor = ParameterExtractor(excel_path)
params = extractor.extract_parameters(sl_no=2)

# params contains:
# - operation_method, operation_path, operation_summary
# - header_parameters, query_parameters, path_parameters
# - form_data_parameters, example_value_json, response_model_json
```

### Semantic Search (nlp/)

```python
# Search for API
from nlp.semantic_search_util import SemanticSearchEngine
search_engine = SemanticSearchEngine(excel_path)
sl_no = search_engine.get_best_match_sl_no("Create a new pet")
```

### Code Generation (generator_util/)

```python
# Generate test code
from generator_util.code_generator_util import CodeGenerator
generator = CodeGenerator(excel_path, base_url)
result = generator.generate_test_file(
    sl_nos=[2, 3, 8],
    queries=['Create pet', 'Update pet', 'Delete pet'],
    folder_name='TestComponent_01',
    filename='TestFile_01'
)
```

### AI Code Modification (generator_aiUtil/)

```python
# Modify code with AI
from generator_aiUtil.ai_code_modifier_util import modify_generated_code_with_ai
result = modify_generated_code_with_ai(
    file_path='/path/to/test_file.py',
    method_name='test_01_method',
    original_code='...',
    excel_data=[...],
    queries=['Create pet → Extract pet_id'],
    ai_provider='openai',
    replace_original=True
)
```

---

## 📊 Data Structures

### Excel Row Structure
```python
{
    'Sl_No': 2,
    'Component': 'pet',
    'Component_SmallDescription': 'Everything about your Pets',
    'Operation_Method': 'POST',
    'Operation_Path': '/pet',
    'Operation_Summary': 'Add a new pet to the store',
    'Operation_SecondarySummary': 'Add a new pet',
    'header_parameters': '{}',
    'query_parameters': '{}',
    'path_parameters': '{}',
    'form_data_parameters': '{}',
    'example_value_json': '{"name": "doggie", "status": "available"}',
    'response_model_json': '{"id": 0, "name": "string", ...}'
}
```

### Prompt Sidecar Structure
```json
{
  "methods": {
    "test_01_create_pet": "Create a new pet → Extract pet_id",
    "test_02_update_pet": "Update pet → Use pet_id"
  }
}
```

### API Response Structure
```python
# Success response
{
    'success': True,
    'message': 'Success message',
    'data': {},
    'logs': []
}

# Error response
{
    'success': False,
    'message': 'Error message',
    'error': 'Error details'
}
```

---

## 🎨 Frontend Patterns

### Making API Calls
```javascript
async function callBackend(route, data) {
    try {
        const response = await fetch(route, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        if (result.success) {
            notification.success(result.message);
            return result;
        } else {
            notification.error(result.message);
            return null;
        }
    } catch (error) {
        notification.error('Error: ' + error.message);
        return null;
    }
}
```

### Using Notifications
```javascript
// Success notification
notification.success('Operation completed successfully');

// Error notification
notification.error('Operation failed');

// Warning notification
notification.warning('Please check your input');

// Info notification
notification.info('Loading data...');
```

### LocalStorage Operations
```javascript
// Save to LocalStorage
storage.set('aiModel', 'openai');

// Get from LocalStorage
const aiModel = storage.get('aiModel', 'openai'); // default: 'openai'

// Remove from LocalStorage
storage.remove('aiModel');

// Clear all
storage.clear();
```

---

## 🧪 Testing Patterns

### Generated Test Structure
```python
import pytest
import requests
import allure

@allure.suite("TestComponent01TestFile01")
class TestComponent01TestFile01:
    
    @allure.title("Test description")
    def test_01_method_name(self):
        """Test method docstring"""
        base_url = "https://petstore.swagger.io/v2"
        
        # Step 1: Make API call
        response = requests.post(
            url=f"{base_url}/pet",
            json={"name": "doggie"}
        )
        
        # Assertions
        assert response.status_code == 200
        assert response.json()['name'] == 'doggie'
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific component
pytest rest_test/TestComponent_01/

# Run specific file
pytest rest_test/TestComponent_01/TestFile_01.py

# Run specific method
pytest rest_test/TestComponent_01/TestFile_01.py::TestComponent01TestFile01::test_01_method

# Run with Allure
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 🔍 Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Flask Logs
```bash
# Flask runs in debug mode by default
# Check console output for detailed logs
```

### Check Browser Console
```javascript
// Add console.log statements
console.log('Debug info:', data);

// Check Network tab for API calls
// Check Console tab for JavaScript errors
```

### Common Issues

**Issue:** Excel file not found
```python
# Check path
import os
excel_path = os.path.join(PROJECT_ROOT, 'Rest_API_Data', 'file.xlsx')
print(f"Checking: {excel_path}")
print(f"Exists: {os.path.exists(excel_path)}")
```

**Issue:** AI API key not working
```bash
# Check .env file
cat .env

# Verify environment variable
echo $OPENAI_API_KEY
```

**Issue:** Test file not generated
```python
# Check permissions
import os
rest_test_dir = os.path.join(PROJECT_ROOT, 'rest_test')
print(f"Directory exists: {os.path.exists(rest_test_dir)}")
print(f"Writable: {os.access(rest_test_dir, os.W_OK)}")
```

---

## 📝 Code Style Guidelines

### Python
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to all functions/classes
- Use logging instead of print statements
- Handle exceptions gracefully

### JavaScript
- Use ES6+ features
- Use async/await for asynchronous operations
- Use const/let instead of var
- Add JSDoc comments for functions
- Use meaningful variable names

### File Naming
- Python: `snake_case.py`
- JavaScript: `camelCase.js`
- Test files: `test_*.py`
- Component folders: `TestComponent_XX`

---

## 🚀 Deployment Checklist

- [ ] Update `.env` with production API keys
- [ ] Set `DEBUG = False` in Flask
- [ ] Configure WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure file permissions
- [ ] Set up logging
- [ ] Configure backup for Excel data
- [ ] Set up monitoring
- [ ] Test all routes
- [ ] Test AI integrations
- [ ] Test file operations

---

## 📚 Additional Resources

### Documentation
- `README.md` - Project overview
- `TECHNICAL_DOCUMENTATION.md` - Technical details
- `TEST_GENERATION_FLOW.md` - Test generation workflow
- `PROJECT_FEATURES_SUMMARY.md` - Complete features list
- `ARCHITECTURE_VISUAL.md` - Visual architecture diagrams

### Module Documentation
- Each module has its own README file
- Check `generator_aiUtil/`, `generator_altUtl/`, `ext_util/` for specific docs

### External Resources
- Flask: https://flask.palletsprojects.com/
- pytest: https://docs.pytest.org/
- Allure: https://docs.qameta.io/allure/
- OpenAPI: https://swagger.io/specification/

---

## 🆘 Getting Help

1. Check existing documentation
2. Review code comments
3. Check GitHub issues
4. Contact: [@Manju-crz](https://github.com/Manju-crz)

---

**Last Updated:** August 25, 2026  
**Author:** Manju-crz  
**Repository:** https://github.com/Manju-crz/SynaptixPhase2
