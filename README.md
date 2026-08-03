# Synaptix

**AI-Based REST API Test Automation Framework**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Transform natural language prompts into executable REST API test scripts with AI-powered code generation, execution, and reporting.

---

## 📋 Overview

**Synaptix** is an AI-driven REST API test automation framework that bridges the gap between natural language test descriptions and executable pytest code. It combines:

- 🤖 **AI-powered test generation** from natural language queries
- 🌐 **Swagger/OpenAPI parsing** for API discovery
- 🚀 **Natural language API execution** with semantic search
- 📊 **Allure reporting** integration
- 🎨 **Web-based UI** for end-to-end workflow management

The framework is designed for QA engineers, developers, and automation teams who want to rapidly generate, execute, and report API tests without writing boilerplate code.

---

## ✨ Features

### Core Capabilities
- ✅ **Natural Language to Test Code** — Describe test cases in plain English; get pytest code
- ✅ **OpenAPI/Swagger Integration** — Parse API specs from JSON or scrape Swagger UI
- ✅ **NLP Semantic Search** — Find the right API endpoints for your queries
- ✅ **AI Code Enhancement** — Modify generated code using OpenAI, DeepSeek, or Groq
- ✅ **Test Execution Engine** — Run generated tests with one click
- ✅ **Allure Reporting** — Generate beautiful HTML test reports
- ✅ **Modular Web UI** — Clean, tab-based interface for all operations

### User Interface Tabs
| Tab | Purpose |
|-----|---------|
| ⚙️ **Configuration** | Select AI model and view system info |
| ✨ **Features** | Overview of framework capabilities |
| 🚀 **Executor** | Execute API calls using natural language |
| ⚡ **Generator** | Generate, execute, and report pytest test code |
| 🌐 **Swagger UI Scraper** | Extract API data from Swagger UI pages |
| 📄 **OpenAPI JSON Parser** | Parse OpenAPI/Swagger JSON specifications |

---

## 🏗️ Architecture

```
SynaptixPhase2/
│
├── custom_ui/              # Flask web application
│   ├── app.py              # Main Flask app and routes
│   ├── features/           # Backend feature modules
│   ├── templates/          # Jinja2 HTML templates
│   │   ├── index.html      # Main layout
│   │   └── tabs/           # Tab-specific templates
│   └── static/             # CSS, JavaScript, assets
│       ├── js/             # Modular JavaScript
│       │   ├── pages/      # Page controllers
│       │   ├── components/ # Reusable UI components
│       │   └── utils/      # Utility functions
│       └── css/            # Stylesheets
│
├── executor_util/          # API execution utilities
├── generator_aiUtil/       # AI code modification utilities
├── generator_util/         # Test code generation utilities
├── nlp/                    # NLP semantic search
├── openapi_json/           # OpenAPI JSON parser
├── rest_util/              # REST API client
├── swagger/                # Swagger UI scraper
├── ext_util/               # Excel, filesystem, and parameter utilities
├── Reference Documents/    # Reference queries and notes
├── Rest_API_Data/          # Excel data files (ignored in git)
└── rest_test/              # Generated test outputs (ignored in git)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- API keys for desired AI providers (OpenAI, DeepSeek, Groq)

### 1. Clone the Repository

```bash
git clone https://github.com/Manju-crz/SynaptixPhase2.git
cd SynaptixPhase2
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Linux/macOS
venv\Scripts\activate       # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```env
OPENAI_API_KEY=your_openai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
GROQ_API_KEY=your_groq_key_here
```

### 5. Run the Application

```bash
python custom_ui/app.py
```

### 6. Open in Browser

Navigate to [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 🧪 Usage Workflow

### Generate Test Code

1. Go to the **⚡ Generator** tab
2. Select an **Excel file** with API test data
3. Choose a **Base URL** (PETSTORE, JSONPLACEHOLDER, or custom)
4. Enter a **Folder Name** (e.g., `pet_tests`)
5. Enter a **File Name** (e.g., `test_pet_operations`)
6. Enter a natural language test prompt:
   ```
   Create a new pet in pet store -> Retrieve the pet_id from the response
   Update pet information -> Use the pet_id from previous response
   Delete a pet -> Use the pet_id from previous response
   ```
7. Click **⚡ Generate Test Code**
8. Generated files will be saved in `rest_test/<folder_name>/<file_name>.py`

### Execute Tests

1. After generating code, click **▶️ Execute Test**
2. Monitor execution logs in the **🔍 Execution Logs** tab
3. Once complete, click **📊 Generate Report** for Allure report

### Execute API Calls

1. Go to the **🚀 Executor** tab
2. Select an Excel file and base URL
3. Enter a natural language query
4. Click **▶️ Execute Query**
5. View the API response in the results section

---

## 📁 Project Structure

### Web UI (`custom_ui/`)

| File/Folder | Purpose |
|-------------|---------|
| `app.py` | Flask application entry point |
| `templates/index.html` | Main page layout |
| `templates/tabs/` | Individual tab templates |
| `static/js/pages/` | Page controllers (Configuration, Executor, Generator, etc.) |
| `static/js/components/` | Reusable components (notifications) |
| `static/js/utils/` | Utility functions (storage, validators) |
| `static/style.css` | Main stylesheet |

### Backend Utilities

| Module | Purpose |
|--------|---------|
| `executor_util/` | Build and execute API commands |
| `generator_util/` | Generate and validate pytest test code |
| `generator_aiUtil/` | AI-based code modification and method reading |
| `nlp/` | Semantic search for API endpoint discovery |
| `rest_util/` | REST API client and configuration |
| `swagger/` | Swagger UI browser automation |
| `openapi_json/` | OpenAPI/Swagger JSON parser |
| `ext_util/` | Excel, filesystem, and parameter extraction utilities |

---

## 🛠️ Development

### Running Tests

```bash
pytest
```

### Generating Allure Report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Project Configuration

Key configuration is in `rest_util/config.py` and `custom_ui/config.py`:
- Base URLs: PETSTORE, JSONPLACEHOLDER
- Excel data location: `Rest_API_Data/`
- Generated test location: `rest_test/`

---

## 📚 Documentation

Comprehensive documentation is available in the `custom_ui/` directory:

- **MIGRATION_COMPLETE.md** — Migration completion summary
- **MIGRATION_INDEX.md** — Documentation navigator
- **INCREMENTAL_MIGRATION_GUIDE.md** — Migration strategy and patterns
- **ARCHITECTURE_DIAGRAM.md** — Visual architecture overview
- **QUICK_REFERENCE.md** — Quick reference card
- **README_MIGRATION.md** — Migration quick start

Additional project documentation:

- **TECHNICAL_DOCUMENTATION.md** — Technical details
- **QUICK_START_GUIDE.md** — Quick start instructions
- **RELEASE_NOTES_v3.0.md** — Release notes
- **DOCUMENTATION_INDEX.md** — Documentation index

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Manju-crz**

- GitHub: [@Manju-crz](https://github.com/Manju-crz)
- Repository: [https://github.com/Manju-crz/SynaptixPhase2](https://github.com/Manju-crz/SynaptixPhase2)

---

## 🙏 Acknowledgments

- OpenAI, DeepSeek, and Groq for AI model APIs
- Flask team for the lightweight web framework
- Allure for test reporting
- pytest community for the testing framework
