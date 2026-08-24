# SynaptixPhase2 - Complete Features Summary

**AI-Based REST API Test Automation Framework**  
**Last Updated:** August 25, 2026  
**Version:** 4.0+

---

## 📋 Executive Summary

SynaptixPhase2 is a comprehensive AI-powered REST API test automation framework that transforms natural language descriptions into executable pytest code. The project features a modern web-based UI built with Flask, modular JavaScript architecture, and integration with multiple AI providers (OpenAI, DeepSeek, Groq).

---

## 🏗️ Architecture Overview

### Technology Stack
- **Backend:** Flask (Python 3.10+)
- **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3
- **AI Integration:** OpenAI, DeepSeek, Groq APIs
- **NLP:** Sentence Transformers (all-mpnet-base-v2)
- **Testing:** pytest, Allure reporting
- **Data Storage:** Excel (openpyxl), LocalStorage (browser)
- **Browser Automation:** Selenium (for Swagger scraping)

### Project Structure
```
SynaptixPhase2/
├── custom_ui/              # Flask web application
│   ├── app.py              # Main Flask app (21 routes)
│   ├── templates/          # Jinja2 HTML templates
│   │   ├── index.html      # Main layout
│   │   └── tabs/           # Tab-specific templates
│   └── static/             # Frontend assets
│       ├── js/
│       │   ├── pages/      # Page controllers (5 modules)
│       │   ├── components/ # Reusable UI components
│       │   └── utils/      # Utility functions
│       └── css/            # Stylesheets
│
├── executor_util/          # API execution engine
├── generator_util/         # Test code generation
├── generator_aiUtil/       # AI code modification
├── generator_altUtl/       # File/method/class management utilities
├── nlp/                    # Semantic search engine
├── loader/                 # Test loader & prompt manager
├── openapi_json/           # OpenAPI JSON parser
├── swagger/                # Swagger UI scraper
├── rest_util/              # REST API client
├── ext_util/               # Excel & parameter utilities
├── Rest_API_Data/          # Excel data files (gitignored)
└── rest_test/              # Generated test outputs (gitignored)
```

---

## ✨ Core Features

### 1. **Code Generator Tab** ⚡
**Purpose:** Generate pytest test code from natural language prompts

#### Key Capabilities:
- **Natural Language Input:** Describe test cases in plain English
- **Multi-Step Test Generation:** Support for complex multi-API workflows
- **AI-Powered Enhancement:** Automatic code enhancement with data extraction
- **Semantic Search:** Intelligent API endpoint matching using NLP
- **Method Management:** Replace/append AI-enhanced methods
- **Test Execution:** One-click test execution with real-time logs
- **Allure Reporting:** Generate beautiful HTML test reports

#### AI Model Support:
- OpenAI (GPT-4, GPT-3.5)
- DeepSeek
- Groq

#### Query Syntax:
```
Create a new pet → Retrieve the pet_id from the response;
Update pet information → Use the pet_id from previous response;
Delete a pet → Use the pet_id from previous response
```

#### Workflow:
1. Select Excel file with API data
2. Choose base URL (PETSTORE, JSONPLACEHOLDER, or custom)
3. Enter folder/file name for test output
4. Enter natural language query with instructions
5. Select AI model
6. Click "Generate Test Code"
7. View generated code (both standard and AI-enhanced)
8. Execute test with one click
9. Generate Allure report

#### Recent Enhancements:
- **Replace vs Append:** AI-enhanced methods now replace original methods (not append)
- **UI Display:** Shows both versions for comparison, but file contains only AI version
- **Prompt Sidecar:** Stores original prompts for each test method
- **Load Existing Tests:** Browse and manage existing test files
- **Validation:** Automatic Python syntax validation

---

### 2. **API Executor Tab** 🚀
**Purpose:** Execute API calls using natural language queries

#### Key Capabilities:
- **Natural Language Queries:** Execute APIs without writing code
- **Semantic Search:** Find the right API endpoint automatically
- **Multi-Query Execution:** Execute multiple APIs in sequence (semicolon-separated)
- **Real-Time Results:** View API responses instantly
- **Comprehensive Logging:** Detailed execution logs
- **Response Display:** Formatted JSON responses

#### Example Query:
```
Create a new pet with name "Fluffy"
```

#### Workflow:
1. Select Excel file with API data
2. Choose base URL
3. Enter natural language query
4. Click "Execute Query"
5. View API response and logs

---

### 3. **Swagger UI Scraper Tab** 🌐
**Purpose:** Extract API documentation from Swagger UI pages

#### Key Capabilities:
- **Automated Scraping:** Extract API endpoints from Swagger UI
- **Browser Automation:** Uses Selenium for dynamic content
- **Excel Export:** Save extracted data to Excel format
- **Customizable Filename:** Set custom prefix for output files
- **Multiple Swagger Versions:** Support for Swagger 2.0 and 3.0

#### Workflow:
1. Enter Swagger UI URL
2. Set filename prefix (optional)
3. Click "Run Scraper"
4. Excel file generated in Rest_API_Data/

---

### 4. **OpenAPI JSON Parser Tab** 📄
**Purpose:** Parse OpenAPI/Swagger JSON specifications

#### Key Capabilities:
- **URL Parsing:** Fetch and parse OpenAPI spec from URL
- **File Upload:** Upload and parse local JSON files
- **Schema Extraction:** Extract all API endpoints and schemas
- **Excel Export:** Save parsed data to Excel format
- **Tag Organization:** Group APIs by tags/components
- **Parameter Extraction:** Extract headers, query params, path params, body params

#### Supported Formats:
- OpenAPI 3.0
- Swagger 2.0

#### Workflow:
1. Choose input method (URL or File Upload)
2. Enter OpenAPI spec URL or upload JSON file
3. Set filename prefix (optional)
4. Click "Parse JSON"
5. Excel file generated in Rest_API_Data/

---

### 5. **Configuration Tab** ⚙️
**Purpose:** Manage application settings

#### Key Capabilities:
- **AI Model Selection:** Choose default AI provider
- **Persistent Settings:** Settings saved to LocalStorage
- **System Information:** View project paths and configuration
- **Real-Time Updates:** Settings apply immediately

---

### 6. **Features Dashboard Tab** ✨
**Purpose:** Overview of all framework capabilities

#### Displays:
- Feature status
- Quick navigation links
- System information
- Documentation links

---

## 🔧 Advanced Utilities (generator_altUtl)

### File Management
1. **File Rename Utility** (`file_rename_util.py`)
   - Rename test files within components
   - Recursive folder search
   - Extension handling
   - Validation checks

2. **File Delete Utility** (`file_delete_util.py`)
   - Delete individual test files
   - Delete entire components (folders)
   - Cascade deletion of all files in component
   - Safety checks

### Method Management
3. **Method Rename Utility** (`method_rename_util.py`)
   - Rename test methods in files
   - Append suffixes to method names
   - Regex-based replacement
   - Validation checks

4. **Method Remove Utility** (`method_remove_util.py`)
   - Remove test methods from files
   - AST-based method detection
   - Decorator handling
   - Clean removal (no orphaned code)

### Class Management
5. **Class Rename Utility** (`class_rename_util.py`)
   - Rename test classes
   - Sync with Allure suite annotations
   - Validation checks
   - Fallback to first class if name mismatch

6. **Allure Suite Update Utility** (`allure_suite_update_util.py`)
   - Keep @allure.suite in sync with class name
   - Automatic annotation updates

---

## 🤖 AI Integration Features

### AI Code Modifier (`generator_aiUtil/ai_code_modifier_util.py`)

#### Key Functions:
1. **`modify_generated_code_with_ai()`**
   - Enhances generated code with AI
   - Supports OpenAI, DeepSeek, Groq
   - Parses query instructions
   - Extracts data from responses
   - Chains API calls with variables

2. **`replace_method_with_ai_version()`**
   - Replaces original method with AI version
   - AST-based method location
   - Preserves decorators
   - Proper indentation handling

3. **Instruction Parsing:**
   - Detects `→` or `->` in queries
   - Extracts main action and instructions
   - Builds AI prompts with context

#### AI Prompt Structure:
```
ORIGINAL CODE: [generated test method]
EXCEL DATA: [API specs for each step]
INSTRUCTIONS:
  Step 1: Create pet
    → Extract pet_id
  Step 2: Update pet
    → Use pet_id
REQUIREMENTS:
  - Extract pet_id from response
  - Store in variable
  - Use in next request
```

---

## 📊 Data Flow & Workflows

### Test Generation Flow

```
User Input (Natural Language Query)
    ↓
Semantic Search (NLP) → Find matching APIs (Sl_No)
    ↓
Code Generator → Generate pytest test method
    ↓
Test Method Reader → Extract generated code
    ↓
[Instructions detected?]
    ↓ YES
Parameter Extractor → Get Excel data for each API
    ↓
AI Code Modifier → Enhance code with AI
    ↓
Replace Original Method → Only AI version in file
    ↓
Code Validator → Check syntax errors
    ↓
Return to UI → Display both versions (original + AI)
```

### API Execution Flow

```
User Query (Natural Language)
    ↓
Semantic Search → Find matching API (Sl_No)
    ↓
Parameter Extractor → Get API details from Excel
    ↓
REST Client → Execute API call
    ↓
Response Handler → Format and display results
    ↓
Return to UI → Show response + logs
```

---

## 🗄️ Data Storage

### Excel Data Structure
**Location:** `Rest_API_Data/*.xlsx`

**Columns:**
- `Sl_No` - Serial number (unique identifier)
- `Component` - API component/tag
- `Component_SmallDescription` - Brief description
- `Operation_Method` - HTTP method (GET, POST, PUT, DELETE)
- `Operation_Path` - API endpoint path
- `Operation_Summary` - Primary summary
- `Operation_SecondarySummary` - Additional details
- `header_parameters` - JSON string of headers
- `query_parameters` - JSON string of query params
- `path_parameters` - JSON string of path params
- `form_data_parameters` - JSON string of form data
- `example_value_json` - JSON example for request body
- `response_model_json` - JSON schema for response

### Prompt Sidecar Storage
**Location:** `rest_test/{component}/.prompts/{file}.json`

**Structure:**
```json
{
  "methods": {
    "test_01_create_pet": "Create a new pet → Extract pet_id",
    "test_02_update_pet": "Update pet → Use pet_id"
  }
}
```

### LocalStorage (Browser)
- AI model selection
- Base URL preferences
- UI state

---

## 🔌 Flask API Routes (21 Routes)

### Core Routes
1. `GET /` - Main UI page
2. `GET /get-excel-files` - List available Excel files

### Swagger/OpenAPI Routes
3. `POST /run-test` - Run Swagger UI scraper
4. `POST /run-json-parser` - Parse OpenAPI JSON

### Executor Routes
5. `POST /run-executor` - Execute API calls

### Generator Routes
6. `POST /run-generator` - Generate test code
7. `POST /execute-generated-test` - Execute single test method
8. `POST /execute-class-tests` - Execute all tests in a class
9. `GET /check-test-status/<test_id>` - Check test execution status
10. `POST /clear-execution-results` - Clear execution results
11. `POST /show-allure-report` - Generate Allure report
12. `GET /allure-report/<path:filename>` - Serve Allure report files

### Test Management Routes
13. `GET /load-existing-tests` - Load existing test structure
14. `POST /update-prompt` - Update test method prompt

### File Management Routes
15. `POST /rename-file` - Rename test file
16. `POST /delete-file` - Delete test file

### Method Management Routes
17. `POST /rename-method` - Rename test method
18. `POST /delete-method` - Delete test method

### Class Management Routes
19. `POST /rename-class` - Rename test class

### Component Management Routes
20. `POST /rename-component` - Rename component folder
21. `POST /delete-component` - Delete component folder

---

## 🎯 Recent Enhancements & Modifications

### 1. AI Method Replacement (August 2026)
**What Changed:**
- AI-enhanced methods now **replace** original methods (not append)
- File contains only AI version
- UI displays both for comparison

**Benefits:**
- Cleaner test files
- No duplicate methods
- Automatic enhancement
- Better UX

### 2. Test Loader Integration
**What Added:**
- Load existing test structure in UI
- Browse components, files, classes, methods
- View original prompts for each method
- Manage existing tests

### 3. File/Method/Class Management
**What Added:**
- Rename test files, methods, classes
- Delete test files, methods, components
- Validation checks
- Prompt sidecar sync

### 4. Allure Suite Sync
**What Added:**
- Auto-update @allure.suite annotation
- Keep in sync with class name
- Proper test organization

### 5. Multi-AI Provider Support
**What Added:**
- OpenAI integration
- DeepSeek integration
- Groq integration
- Configurable in UI

### 6. Code Validation
**What Added:**
- Automatic Python syntax validation
- Compilation checks
- Error reporting

---

## 📝 Usage Examples

### Example 1: Generate Multi-Step Test
**Query:**
```
Create a new pet → Retrieve the pet_id from the response;
Update pet information → Use the pet_id from previous response;
Delete a pet → Use the pet_id from previous response
```

**Generated Code (AI-Enhanced):**
```python
@allure.suite("TestComponent01TestFile01")
class TestComponent01TestFile01:
    
    @allure.title("Create a new pet in pest store")
    def test_01_create_a_new_pet_in_pest_store_ai(self):
        # Step 1: Create a new pet
        response1 = requests.post(
            url=f"{base_url}/pet",
            json={"name": "doggie", "status": "available"}
        )
        assert response1.status_code == 200
        pet_id = response1.json()['id']  # Extract pet_id
        
        # Step 2: Update pet information
        response2 = requests.put(
            url=f"{base_url}/pet",
            json={"id": pet_id, "name": "updated_doggie"}
        )
        assert response2.status_code == 200
        
        # Step 3: Delete a pet
        response3 = requests.delete(
            url=f"{base_url}/pet/{pet_id}"
        )
        assert response3.status_code == 200
```

### Example 2: Execute API Call
**Query:**
```
Get pet by ID 123
```

**Result:**
```json
{
  "id": 123,
  "name": "Fluffy",
  "status": "available"
}
```

---

## 🔍 Key Components Deep Dive

### 1. Semantic Search Engine (`nlp/semantic_search_util.py`)
- **Model:** all-mpnet-base-v2 (sentence transformers)
- **Purpose:** Find matching APIs for natural language queries
- **Search Columns:** Component, Operation_Summary, Operation_Path, etc.
- **Algorithm:** Cosine similarity on embeddings
- **Performance:** Generates embeddings once, reuses for all queries

### 2. Code Generator (`generator_util/code_generator_util.py`)
- **Purpose:** Generate pytest test methods from Excel data
- **Features:**
  - Parameter extraction (headers, query, path, body)
  - Schema to example conversion
  - Multi-step test generation
  - Allure annotations
  - Proper indentation

### 3. Parameter Extractor (`ext_util/parameter_extractor_util.py`)
- **Purpose:** Extract API details from Excel
- **Extracts:**
  - Operation details (method, path, summary)
  - All parameter types (header, query, path, form)
  - Request/response examples
  - JSON schemas

### 4. Test Method Reader (`generator_aiUtil/test_method_reader_util.py`)
- **Purpose:** Read generated test methods using AST
- **Features:**
  - Parse Python files
  - Extract method code
  - Count steps
  - Preserve formatting

### 5. Prompt Manager (`loader/prompt_manager.py`)
- **Purpose:** Manage test method prompts
- **Features:**
  - Save prompts to sidecar JSON
  - Load prompts for UI display
  - Migrate legacy sidecars
  - Rename method prompts

---

## 🚀 Deployment & Operations

### Running the Application
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export OPENAI_API_KEY=your_key
export DEEPSEEK_API_KEY=your_key
export GROQ_API_KEY=your_key

# 3. Run Flask app
python custom_ui/app.py

# 4. Open browser
http://localhost:5000
```

### Running Tests
```bash
# Run all tests
pytest

# Run with Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

---

## 📚 Documentation Files

### Main Documentation
- `README.md` - Project overview and quick start
- `TECHNICAL_DOCUMENTATION.md` - Technical details
- `TEST_GENERATION_FLOW.md` - Test generation workflow
- `MODIFICATION_SUMMARY.md` - Recent modifications

### Module Documentation
- `custom_ui/UI_FEATURES.md` - UI features overview
- `generator_aiUtil/README_AICodeModifier.md` - AI code modifier
- `generator_aiUtil/README_TestMethodReader.md` - Test method reader
- `generator_altUtl/CLI_USAGE_GUIDE.md` - CLI usage
- `ext_util/README_ParameterExtractor.md` - Parameter extractor

### Reference Documents
- `Reference Documents/To-Do.txt` - Pending features
- `Reference Documents/SwaggerUi.md` - Swagger UI notes
- `Reference Documents/Keycloak.md` - Keycloak integration notes

---

## 🎯 Pending Features (From To-Do.txt)

1. **Method-Level Execution** - Execute individual test methods from UI
2. **Class-Level Execution** - Execute all methods in a class
3. **Component-Level Execution** - Execute all tests in a component
4. **Auto-Healing** - Automatic code fixing after test failures
5. **Bulk Execution** - Execute multiple tests in parallel
6. **Clear Past Reports** - Clear old Allure reports before generating new ones
7. **Directus Integration** - Explore Directus APIs for bulk execution

---

## 🏆 Key Strengths

1. **Natural Language Interface** - No coding required for test generation
2. **AI-Powered Enhancement** - Automatic data extraction and chaining
3. **Multi-Provider Support** - OpenAI, DeepSeek, Groq
4. **Modular Architecture** - Clean separation of concerns
5. **Comprehensive UI** - All features accessible from web interface
6. **Semantic Search** - Intelligent API matching
7. **Allure Integration** - Beautiful test reports
8. **File Management** - Complete CRUD operations on tests
9. **Prompt Tracking** - Original prompts stored for reference
10. **Validation** - Automatic syntax checking

---

## 🔧 Configuration

### Base URLs
- **PETSTORE:** `https://petstore.swagger.io/v2`
- **JSONPLACEHOLDER:** `https://jsonplaceholder.typicode.com`
- **Custom:** User-defined

### Paths
- **Excel Data:** `Rest_API_Data/`
- **Generated Tests:** `rest_test/`
- **Allure Results:** `allure-results/`
- **Allure Report:** `allure-report/`

---

## 📊 Statistics

- **Total Routes:** 21 Flask routes
- **Frontend Pages:** 5 JavaScript modules
- **Utility Modules:** 15+ Python modules
- **AI Providers:** 3 (OpenAI, DeepSeek, Groq)
- **Supported Formats:** OpenAPI 3.0, Swagger 2.0
- **Test Frameworks:** pytest, Allure

---

## 🎓 Learning Resources

### For Users
1. Start with `README.md` for quick start
2. Read `custom_ui/UI_FEATURES.md` for UI overview
3. Check `TEST_GENERATION_FLOW.md` for workflow understanding

### For Developers
1. Review `TECHNICAL_DOCUMENTATION.md` for architecture
2. Explore module-specific README files
3. Check `MODIFICATION_SUMMARY.md` for recent changes

---

## 🤝 Contributing

The project follows a modular architecture with clear separation:
- **Frontend:** JavaScript modules in `custom_ui/static/js/`
- **Backend:** Flask routes in `custom_ui/app.py`
- **Utilities:** Separate modules for each feature
- **Documentation:** Comprehensive README files in each module

---

## 📅 Version History

- **v4.0+** (August 2026) - AI method replacement, test loader, file management
- **v3.0** (July 2026) - Multi-AI provider support, semantic search
- **v2.0** (June 2026) - Web UI, code generator, executor
- **v1.0** (May 2026) - Initial release with basic features

---

## 🎯 Conclusion

SynaptixPhase2 is a mature, feature-rich REST API test automation framework that successfully bridges the gap between natural language test descriptions and executable code. With its AI-powered enhancements, comprehensive UI, and modular architecture, it provides a complete solution for API testing automation.

The framework is actively maintained with regular enhancements and has a clear roadmap for future features including auto-healing, bulk execution, and advanced test management capabilities.

---

**Generated:** August 25, 2026  
**Author:** Manju-crz  
**Repository:** https://github.com/Manju-crz/SynaptixPhase2
