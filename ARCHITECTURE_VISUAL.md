# SynaptixPhase2 - Visual Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WEB BROWSER (Client)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      User Interface (HTML/CSS/JS)                    │   │
│  │  ┌──────────┬──────────┬──────────┬──────────┬──────────┬─────────┐ │   │
│  │  │  Config  │ Features │ Executor │Generator │ Swagger  │ OpenAPI │ │   │
│  │  │   Tab    │   Tab    │   Tab    │   Tab    │   Tab    │   Tab   │ │   │
│  │  └──────────┴──────────┴──────────┴──────────┴──────────┴─────────┘ │   │
│  │                                                                       │   │
│  │  JavaScript Modules (ES6+)                                           │   │
│  │  ├── pages/                                                          │   │
│  │  │   ├── configurationPage.js                                       │   │
│  │  │   ├── executorPage.js                                            │   │
│  │  │   ├── generatorPage.js                                           │   │
│  │  │   ├── swaggerScraperPage.js                                      │   │
│  │  │   └── openapiParserPage.js                                       │   │
│  │  ├── components/                                                     │   │
│  │  │   └── notification.js                                            │   │
│  │  └── utils/                                                          │   │
│  │      ├── storage.js                                                  │   │
│  │      └── validators.js                                               │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                    │                                          │
│                                    │ HTTP/AJAX Requests                       │
│                                    ▼                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLASK WEB SERVER (Backend)                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         app.py (21 Routes)                             │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │ Core Routes                                                       │ │  │
│  │  │  • GET  /                    - Main UI page                      │ │  │
│  │  │  • GET  /get-excel-files     - List Excel files                 │ │  │
│  │  ├──────────────────────────────────────────────────────────────────┤ │  │
│  │  │ Swagger/OpenAPI Routes                                           │ │  │
│  │  │  • POST /run-test            - Swagger UI scraper               │ │  │
│  │  │  • POST /run-json-parser     - OpenAPI JSON parser              │ │  │
│  │  ├──────────────────────────────────────────────────────────────────┤ │  │
│  │  │ Executor Routes                                                  │ │  │
│  │  │  • POST /run-executor        - Execute API calls                │ │  │
│  │  ├──────────────────────────────────────────────────────────────────┤ │  │
│  │  │ Generator Routes                                                 │ │  │
│  │  │  • POST /run-generator       - Generate test code               │ │  │
│  │  │  • POST /execute-generated-test - Execute single test           │ │  │
│  │  │  • POST /execute-class-tests - Execute class tests              │ │  │
│  │  │  • GET  /check-test-status/<id> - Check test status             │ │  │
│  │  │  • POST /show-allure-report  - Generate Allure report           │ │  │
│  │  ├──────────────────────────────────────────────────────────────────┤ │  │
│  │  │ Test Management Routes                                           │ │  │
│  │  │  • GET  /load-existing-tests - Load test structure              │ │  │
│  │  │  • POST /update-prompt       - Update method prompt             │ │  │
│  │  │  • POST /rename-method       - Rename test method               │ │  │
│  │  │  • POST /delete-method       - Delete test method               │ │  │
│  │  │  • POST /rename-file         - Rename test file                 │ │  │
│  │  │  • POST /delete-file         - Delete test file                 │ │  │
│  │  │  • POST /rename-class        - Rename test class                │ │  │
│  │  │  • POST /rename-component    - Rename component                 │ │  │
│  │  │  • POST /delete-component    - Delete component                 │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                          │
│                                    │ Calls                                    │
│                                    ▼                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          BUSINESS LOGIC LAYER                                │
│                                                                               │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │   executor_util/    │  │  generator_util/    │  │ generator_aiUtil/  │  │
│  │  ┌───────────────┐  │  │  ┌───────────────┐  │  │ ┌────────────────┐ │  │
│  │  │ ApiExecutor   │  │  │  │CodeGenerator  │  │  │ │AICodeModifier  │ │  │
│  │  │               │  │  │  │               │  │  │ │                │ │  │
│  │  │ • execute_api │  │  │  │ • generate_   │  │  │ │ • modify_code  │ │  │
│  │  │   _call()     │  │  │  │   test_file() │  │  │ │   _with_ai()   │ │  │
│  │  │               │  │  │  │               │  │  │ │ • replace_     │ │  │
│  │  │ • build_      │  │  │  │ • validate_   │  │  │ │   method()     │ │  │
│  │  │   request()   │  │  │  │   code()      │  │  │ │                │ │  │
│  │  └───────────────┘  │  │  └───────────────┘  │  │ └────────────────┘ │  │
│  └─────────────────────┘  └─────────────────────┘  └────────────────────┘  │
│                                                                               │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │ generator_altUtl/   │  │     nlp/            │  │    loader/         │  │
│  │  ┌───────────────┐  │  │  ┌───────────────┐  │  │ ┌────────────────┐ │  │
│  │  │MethodRename   │  │  │  │SemanticSearch │  │  │ │TestLoader      │ │  │
│  │  │MethodRemove   │  │  │  │Engine         │  │  │ │                │ │  │
│  │  │ ClassRename   │  │  │  │               │  │  │ │ • load_tests() │ │  │
│  │  │ FileRename    │  │  │  │ • search()    │  │  │ │                │ │  │
│  │  │ FileDelete    │  │  │  │ • get_best_   │  │  │ │PromptManager   │ │  │
│  │  │ ComponentDel  │  │  │  │   match()     │  │  │ │                │ │  │
│  │  └───────────────┘  │  │  └───────────────┘  │  │ │ • save_prompt()│ │  │
│  └─────────────────────┘  └─────────────────────┘  │ │ • load_prompt()│ │  │
│                                                     │ └────────────────┘ │  │
│  ┌─────────────────────┐  ┌─────────────────────┐  └────────────────────┘  │
│  │   swagger/          │  │  openapi_json/      │                           │
│  │  ┌───────────────┐  │  │  ┌───────────────┐  │                           │
│  │  │SwaggerScraper │  │  │  │OpenAPIParser  │  │                           │
│  │  │               │  │  │  │               │  │                           │
│  │  │ • scrape_ui() │  │  │  │ • parse_spec()│  │                           │
│  │  │ • extract_    │  │  │  │ • extract_    │  │                           │
│  │  │   endpoints() │  │  │  │   operations()│  │                           │
│  │  └───────────────┘  │  │  └───────────────┘  │                           │
│  └─────────────────────┘  └─────────────────────┘                           │
│                                                                               │
│  ┌─────────────────────┐  ┌─────────────────────┐                           │
│  │    ext_util/        │  │   rest_util/        │                           │
│  │  ┌───────────────┐  │  │  ┌───────────────┐  │                           │
│  │  │ParameterExtr  │  │  │  │RestClient     │  │                           │
│  │  │               │  │  │  │               │  │                           │
│  │  │ • extract_    │  │  │  │ • get()       │  │                           │
│  │  │   parameters()│  │  │  │ • post()      │  │                           │
│  │  │               │  │  │  │ • put()       │  │                           │
│  │  │ExcelUtil      │  │  │  │ • delete()    │  │                           │
│  │  │               │  │  │  └───────────────┘  │                           │
│  │  │ • read_excel()│  │  └─────────────────────┘                           │
│  │  │ • write_excel│  │                                                      │
│  │  └───────────────┘  │                                                      │
│  └─────────────────────┘                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES LAYER                             │
│                                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   OpenAI API    │  │  DeepSeek API   │  │    Groq API     │             │
│  │                 │  │                 │  │                 │             │
│  │  • GPT-4        │  │  • DeepSeek-V2  │  │  • Mixtral      │             │
│  │  • GPT-3.5      │  │                 │  │  • Llama        │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              Sentence Transformers (HuggingFace)                     │    │
│  │                  • all-mpnet-base-v2                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA STORAGE LAYER                                │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      Rest_API_Data/ (Excel Files)                    │    │
│  │  • OpenAPI_Data_2026_08_25_02_24.xlsx                               │    │
│  │  • Swagger_Data_2026_08_20_15_30.xlsx                               │    │
│  │  • ...                                                               │    │
│  │                                                                       │    │
│  │  Columns:                                                            │    │
│  │    - Sl_No, Component, Operation_Method, Operation_Path             │    │
│  │    - Operation_Summary, header_parameters, query_parameters         │    │
│  │    - path_parameters, form_data_parameters                          │    │
│  │    - example_value_json, response_model_json                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    rest_test/ (Generated Tests)                      │    │
│  │  TestComponent_01/                                                   │    │
│  │    ├── TestFile_01.py                                               │    │
│  │    ├── TestFile_02.py                                               │    │
│  │    └── .prompts/                                                    │    │
│  │        └── TestFile_01.json  (Prompt sidecar)                       │    │
│  │  TestComponent_02/                                                   │    │
│  │    └── ...                                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   allure-results/ (Test Results)                     │    │
│  │  • JSON result files                                                │    │
│  │  • Attachments                                                      │    │
│  │  • History                                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   allure-report/ (HTML Reports)                      │    │
│  │  • index.html                                                       │    │
│  │  • Static assets                                                    │    │
│  │  • Test history                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │              Browser LocalStorage (Client-Side)                      │    │
│  │  • AI model selection                                               │    │
│  │  • Base URL preferences                                             │    │
│  │  • UI state                                                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### 1. Test Code Generation Flow

```
┌──────────────┐
│ User Input   │
│ (Generator)  │
└──────┬───────┘
       │
       │ Natural Language Query:
       │ "Create pet → Extract pet_id; Update pet → Use pet_id"
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Flask Route: /run-generator                              │
│  1. Parse query (split by semicolon)                    │
│  2. Extract main actions (before →)                     │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ SemanticSearchEngine (nlp/)                              │
│  1. Load sentence transformer model                     │
│  2. Generate embeddings for Excel rows                  │
│  3. Search for each query                               │
│  4. Return best matching Sl_No for each                 │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Sl_Nos: [2, 3, 8]
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ CodeGenerator (generator_util/)                          │
│  1. Read Excel data for each Sl_No                      │
│  2. Extract parameters (ParameterExtractor)             │
│  3. Generate pytest test method                         │
│  4. Create/update file in rest_test/                    │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Generated: test_01_create_a_new_pet_in_pest_store()
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ TestMethodReader (generator_aiUtil/)                     │
│  1. Parse file with AST                                 │
│  2. Extract generated method code                       │
│  3. Return method details                               │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Original code extracted
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Check for Instructions                                   │
│  Query contains → or -> ?                               │
└──────┬────────────────────────────────┬──────────────────┘
       │ NO                             │ YES
       │                                │
       │                                ▼
       │                 ┌──────────────────────────────────┐
       │                 │ ParameterExtractor (ext_util/)   │
       │                 │  Extract Excel data for each API │
       │                 └──────┬───────────────────────────┘
       │                        │
       │                        ▼
       │                 ┌──────────────────────────────────┐
       │                 │ AICodeModifier (generator_aiUtil)│
       │                 │  1. Parse instructions           │
       │                 │  2. Build AI prompt              │
       │                 │  3. Call AI API (OpenAI/etc)     │
       │                 │  4. Get enhanced code            │
       │                 │  5. Replace original method      │
       │                 └──────┬───────────────────────────┘
       │                        │
       │                        │ AI-enhanced code
       │                        │
       ▼                        ▼
┌──────────────────────────────────────────────────────────┐
│ CodeValidator (generator_util/)                          │
│  1. Compile Python code                                 │
│  2. Check for syntax errors                             │
│  3. Return validation results                           │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ PromptManager (loader/)                                  │
│  Save original prompt to sidecar JSON                   │
│  rest_test/{component}/.prompts/{file}.json             │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Return to UI                                             │
│  • Success/failure status                               │
│  • Generated code (both versions)                       │
│  • File path                                            │
│  • Validation results                                   │
│  • Logs                                                 │
└──────────────────────────────────────────────────────────┘
```

### 2. API Execution Flow

```
┌──────────────┐
│ User Input   │
│ (Executor)   │
└──────┬───────┘
       │
       │ Natural Language Query:
       │ "Get pet by ID 123"
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Flask Route: /run-executor                               │
│  1. Validate inputs                                     │
│  2. Parse query (split by semicolon for multiple)      │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ SemanticSearchEngine (nlp/)                              │
│  1. Search for matching API                             │
│  2. Return best matching Sl_No                          │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Sl_No: 5
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ ParameterExtractor (ext_util/)                           │
│  1. Read Excel row for Sl_No                            │
│  2. Extract operation details                           │
│  3. Extract all parameters                              │
│  4. Get request/response examples                       │
└──────┬───────────────────────────────────────────────────┘
       │
       │ API Details: GET /pet/{petId}
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ ApiExecutor (executor_util/)                             │
│  1. Build request (headers, params, body)               │
│  2. Make HTTP call (RestClient)                         │
│  3. Parse response                                      │
│  4. Format results                                      │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ RestClient (rest_util/)                                  │
│  Execute HTTP request                                   │
│  • GET, POST, PUT, DELETE                               │
│  • Handle authentication                                │
│  • Return response                                      │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Response: {"id": 123, "name": "Fluffy", ...}
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Return to UI                                             │
│  • Success/failure status                               │
│  • API response (formatted JSON)                        │
│  • Status code                                          │
│  • Execution logs                                       │
└──────────────────────────────────────────────────────────┘
```

### 3. OpenAPI Parsing Flow

```
┌──────────────┐
│ User Input   │
│ (OpenAPI)    │
└──────┬───────┘
       │
       │ OpenAPI Spec URL or File Upload
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Flask Route: /run-json-parser                            │
│  1. Validate input (URL or file content)                │
│  2. Determine input type                                │
└──────┬───────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ OpenAPIParser (openapi_json/)                            │
│  1. Fetch/load OpenAPI spec                             │
│  2. Parse JSON structure                                │
│  3. Extract base URL                                    │
│  4. Extract tags/components                             │
│  5. Extract all operations                              │
│  6. Parse parameters (header, query, path, body)        │
│  7. Extract request/response schemas                    │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Parsed Data: 20 operations
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ ExcelUtil (ext_util/)                                    │
│  1. Create Excel workbook                               │
│  2. Write headers                                       │
│  3. Write data rows                                     │
│  4. Format cells                                        │
│  5. Save to Rest_API_Data/                              │
└──────┬───────────────────────────────────────────────────┘
       │
       │ File: OpenAPI_Data_2026_08_25_02_24.xlsx
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│ Return to UI                                             │
│  • Success/failure status                               │
│  • File path                                            │
│  • Number of operations extracted                       │
│  • Logs                                                 │
└──────────────────────────────────────────────────────────┘
```

---

## Component Interaction Matrix

| Component | Interacts With | Purpose |
|-----------|----------------|---------|
| **Flask App** | All modules | Route requests to appropriate handlers |
| **SemanticSearchEngine** | Excel files, Sentence Transformers | Find matching APIs for queries |
| **CodeGenerator** | ParameterExtractor, Excel files | Generate pytest test methods |
| **AICodeModifier** | OpenAI/DeepSeek/Groq APIs | Enhance generated code |
| **ParameterExtractor** | Excel files | Extract API details |
| **TestMethodReader** | Generated test files | Read test method code |
| **ApiExecutor** | RestClient, ParameterExtractor | Execute API calls |
| **RestClient** | External APIs | Make HTTP requests |
| **OpenAPIParser** | OpenAPI specs | Parse API specifications |
| **SwaggerScraper** | Selenium, Swagger UI | Scrape API documentation |
| **TestLoader** | Generated test files, PromptManager | Load existing tests |
| **PromptManager** | Sidecar JSON files | Manage test prompts |
| **File/Method/Class Utils** | Generated test files | Manage test artifacts |

---

## Technology Stack Details

### Backend
- **Flask 2.0+** - Web framework
- **Python 3.10+** - Programming language
- **pytest** - Testing framework
- **Allure** - Test reporting
- **openpyxl** - Excel file handling
- **requests** - HTTP client
- **Selenium** - Browser automation

### Frontend
- **Vanilla JavaScript (ES6+)** - No framework dependencies
- **HTML5** - Markup
- **CSS3** - Styling
- **LocalStorage API** - Client-side storage

### AI/ML
- **OpenAI API** - GPT-4, GPT-3.5
- **DeepSeek API** - DeepSeek-V2
- **Groq API** - Mixtral, Llama
- **Sentence Transformers** - all-mpnet-base-v2
- **HuggingFace** - Model hosting

### Data Processing
- **pandas** - Data manipulation (optional)
- **numpy** - Numerical operations
- **openpyxl** - Excel I/O
- **json** - JSON parsing

### Code Analysis
- **ast** - Python AST parsing
- **re** - Regular expressions
- **inspect** - Code introspection

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Production Server                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Reverse Proxy (Nginx)                │  │
│  │         http://your-domain.com                    │  │
│  └────────────────────┬──────────────────────────────┘  │
│                       │                                  │
│                       ▼                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │           WSGI Server (Gunicorn)                  │  │
│  │         Workers: 4, Threads: 2                    │  │
│  └────────────────────┬──────────────────────────────┘  │
│                       │                                  │
│                       ▼                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │          Flask Application (app.py)               │  │
│  │         Port: 5000 (internal)                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              File System                          │  │
│  │  • Rest_API_Data/  (Excel files)                 │  │
│  │  • rest_test/      (Generated tests)             │  │
│  │  • allure-results/ (Test results)                │  │
│  │  • allure-report/  (HTML reports)                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

External Services (Cloud):
  • OpenAI API
  • DeepSeek API
  • Groq API
  • HuggingFace (Model downloads)
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
│                                                          │
│  1. Environment Variables                               │
│     • OPENAI_API_KEY                                    │
│     • DEEPSEEK_API_KEY                                  │
│     • GROQ_API_KEY                                      │
│     • Stored in .env file (gitignored)                  │
│                                                          │
│  2. Input Validation                                    │
│     • validators.js (client-side)                       │
│     • Flask request validation (server-side)            │
│                                                          │
│  3. File System Isolation                               │
│     • Generated tests in rest_test/ only                │
│     • Excel data in Rest_API_Data/ only                 │
│     • No arbitrary file access                          │
│                                                          │
│  4. Code Validation                                     │
│     • Python syntax checking before execution           │
│     • AST parsing for safe code analysis                │
│                                                          │
│  5. API Rate Limiting                                   │
│     • Handled by AI provider APIs                       │
│     • Client-side request throttling                    │
└─────────────────────────────────────────────────────────┘
```

---

**Generated:** August 25, 2026  
**Author:** Manju-crz  
**Repository:** https://github.com/Manju-crz/SynaptixPhase2
