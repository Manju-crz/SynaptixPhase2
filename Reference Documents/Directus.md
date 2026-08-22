# Directus Installation and Local Setup – Reference Document

## 1. Purpose

This document describes the complete procedure followed to install and configure **Directus locally on Windows**, using:

* Directus
* Node.js
* SQLite
* npm
* Windows Command Prompt
* Swagger UI Watcher for OpenAPI visualization

The final Directus application was successfully accessed at:

```text
http://localhost:8055
```

---

# 2. Environment Used

| Component          | Configuration                                            |
| ------------------ | -------------------------------------------------------- |
| Operating System   | Windows                                                  |
| Node.js            | Node.js 22.x                                             |
| npm                | npm 11.x                                                 |
| Directus           | 11.17.4                                                  |
| Database           | SQLite                                                   |
| Project Location   | `C:\DATA\VS_Code_Notes\directus-project\my-directus-app` |
| Directus URL       | `http://localhost:8055`                                  |
| Swagger UI Watcher | Globally installed through npm                           |

---

# 3. Recommended Project Directory

The Directus project was maintained under:

```text
C:\DATA\VS_Code_Notes\directus-project
```

The final Directus application directory was:

```text
C:\DATA\VS_Code_Notes\directus-project\my-directus-app
```

It is recommended to keep development projects outside:

```text
C:\Program Files
```

to avoid Windows permission-related issues.

---

# 4. Node.js Installation

## 4.1 Verify Node.js

Open Command Prompt and execute:

```cmd
node -v
```

Initially, Node.js version was:

```text
v24.14.0
```

The Directus installer reported that Node.js 22 was required.

Therefore, Node.js was changed to **Node.js 22**.

## 4.2 Verify the Correct Version

After installing Node.js 22, execute:

```cmd
node -v
```

Expected:

```text
v22.x.x
```

Also verify npm:

```cmd
npm -v
```

---

# 5. Create Directus Project Directory

Navigate to the development directory:

```cmd
cd C:\DATA\VS_Code_Notes\directus-project
```

---

# 6. Initial Directus Installation Attempt

The following command was initially attempted:

```cmd
npm create directus-project@latest
```

This resulted in:

```text
error: missing required argument 'directory'
```

The correct command requires the project directory name.

The following command was then used:

```cmd
npx create-directus-project@latest my-directus-app
```

---

# 7. Select Database

The Directus installer displayed:

```text
Choose your database client
```

SQLite was selected.

```text
SQLite
```

This was selected because SQLite is convenient for local development and testing.

---

# 8. SQLite Database File

The installer requested:

```text
Database File Path
```

The default path was retained:

```text
C:\DATA\VS_Code_Notes\directus-project\my-directus-app\data.db
```

The default path can simply be accepted by pressing:

```text
Enter
```

---

# 9. Initial Installer Issue

The Directus installer then reported:

```text
ERROR: "DB_CLIENT" Environment Variable is missing.
Error while initializing the project
```

The installer had partially created the project directory.

Therefore, the installation was completed manually.

---

# 10. Enter the Directus Application Directory

Execute:

```cmd
cd C:\DATA\VS_Code_Notes\directus-project\my-directus-app
```

Verify that the command prompt shows:

```text
C:\DATA\VS_Code_Notes\directus-project\my-directus-app>
```

All Directus-specific commands should be executed from this directory.

---

# 11. Install Directus and SQLite Packages

Execute:

```cmd
npm install directus sqlite3
```

The installation completed successfully.

npm displayed several warnings, including peer dependency warnings and vulnerability information.

These warnings did not prevent Directus from running locally.

---

# 12. Configure Environment Variables

Create a file named:

```text
.env
```

inside:

```text
C:\DATA\VS_Code_Notes\directus-project\my-directus-app
```

The local development configuration used was:

```env
DB_CLIENT=sqlite3
DB_FILENAME=./data.db

KEY=mysecretkey123
SECRET=myverysecretvalue123

ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

### Important

For a production installation, use strong randomly generated values for:

```text
KEY
SECRET
ADMIN_PASSWORD
```

The above values were used only for local development/testing.

---

# 13. Initialize Directus Database

From the Directus application directory:

```cmd
npx directus bootstrap
```

The bootstrap process initializes the Directus database and applies the required database migrations.

During the first attempt, a migration error occurred:

```text
SQLITE_ERROR: duplicate column name: project_owner
```

This happened because the SQLite database had already been partially initialized by the earlier failed installation attempt.

---

# 14. Clean Up the Partially Initialized Database

For a fresh local installation, the partially created SQLite database can be removed.

Inside:

```text
C:\DATA\VS_Code_Notes\directus-project\my-directus-app
```

remove:

```text
data.db
```

If an old `.env` configuration is incorrect, correct it before continuing.

Do not delete the entire project directory unless a completely fresh installation is required.

---

# 15. Run Bootstrap Again

After cleaning the partially initialized database, run:

```cmd
npx directus bootstrap
```

The bootstrap process should initialize the database and apply Directus migrations.

---

# 16. Start Directus

Once bootstrap is successful, start Directus:

```cmd
npx directus start
```

Directus starts on the default port:

```text
8055
```

---

# 17. Open Directus in Browser

Open:

```text
http://localhost:8055
```

The Directus login page should appear.

---

# 18. Directus Login Credentials

For the local setup, the configured credentials were:

```text
Email:
admin@example.com

Password:
admin123
```

These credentials should be changed for any non-test environment.

---

# 19. Directus Initial Onboarding

After the first login, Directus displayed a project-owner/license information page.

The following information was provided:

### Owner Email

Use the appropriate project owner's email.

For local testing, the configured administrator email can be used.

### Directus Usage

Select an appropriate option such as:

```text
Development
```

or the option that best describes the intended use.

### License Acceptance

Accept:

```text
I accept the terms of the Directus BSL 1.1 and Privacy Policy
```

The product-update subscription checkbox is optional.

Continue to the Directus dashboard.

---

# 20. Directus Dashboard

After onboarding, the Directus Content page initially displayed:

```text
No Collections
```

This is normal for a new Directus installation.

A Directus **Collection** represents a database table/entity and automatically becomes available through Directus APIs.

Examples:

```text
employees
customers
products
orders
```

---

# 21. Create the Employees Collection

Navigate to:

```text
Settings
    ↓
Data Model
```

Click:

```text
Create Collection
```

---

# 22. Collection Configuration

Create the collection using:

| Setting           | Value                    |
| ----------------- | ------------------------ |
| Collection Name   | `employees`              |
| Singleton         | Unchecked                |
| Primary Key Field | `id`                     |
| Primary Key Type  | Auto-incremented integer |

The collection should therefore represent:

```text
employees
```

with:

```text
id
```

as the primary key.

---

# 23. Optional System Fields

During collection creation, Directus displayed optional fields such as:

* Status
* Sort
* Created On
* Created By
* Updated On
* Updated By

For the test setup, useful audit fields were enabled:

```text
Created On
Updated On
```

The other fields are optional depending on the application's requirements.

---

# 24. Create Employee Fields

The following fields were created:

| Field        | Type    |
| ------------ | ------- |
| `first_name` | String  |
| `last_name`  | String  |
| `email`      | String  |
| `department` | String  |
| `salary`     | Integer |

For example, when creating `first_name`:

```text
Key:
first_name

Type:
String
```

Optional UI settings such as:

* Placeholder
* Icon Left
* Icon Right
* Default Value

do not need to be configured for a basic API-testing setup.

---

# 25. Save the Collection

After adding all fields, save the collection using the checkmark/save button.

The resulting data model is approximately:

```text
employees
│
├── id
├── date_created
├── date_updated
├── first_name
├── last_name
├── email
├── department
└── salary
```

---

# 26. Add Employee Data

Navigate to:

```text
Content
```

Open:

```text
employees
```

Create a new item.

Example:

```text
first_name: John
last_name: Smith
email: john@test.com
department: IT
salary: 75000
```

Additional employee records can be created for API testing.

---

# 27. Automatically Generated REST API

Once the `employees` collection exists, Directus automatically exposes REST APIs.

The main endpoint is:

```text
http://localhost:8055/items/employees
```

Example GET request:

```http
GET http://localhost:8055/items/employees
```

This returns employee records in JSON format.

---

# 28. CRUD APIs

Directus automatically generates CRUD operations.

### GET

```http
GET /items/employees
```

Retrieve employees.

### POST

```http
POST /items/employees
```

Create an employee.

### PATCH

```http
PATCH /items/employees/{id}
```

Update an employee.

### DELETE

```http
DELETE /items/employees/{id}
```

Delete an employee.

---

# 29. Native Directus OpenAPI Specification

Directus provides a dynamically generated OpenAPI specification.

Open:

```text
http://localhost:8055/server/specs/oas
```

The browser displays the raw OpenAPI JSON document.

The specification contains:

* API endpoints
* HTTP methods
* parameters
* request bodies
* response schemas
* authentication APIs
* collection APIs
* system APIs

---

# 30. Swagger UI

Directus provided the OpenAPI specification but the requirement was to view it through a graphical Swagger UI.

Therefore, Swagger UI Watcher was installed separately.

The OpenAPI architecture is:

```text
Directus
    │
    ▼
OpenAPI JSON
    │
    ▼
Swagger UI Watcher
    │
    ▼
Interactive Swagger UI
```

---

# 31. Install Swagger UI Watcher

Swagger UI Watcher was installed globally so that it can be reused with other projects.

Open PowerShell or Command Prompt and execute:

```cmd
npm install -g swagger-ui-watcher
```

Verify:

```cmd
swagger-ui-watcher --help
```

If the help information appears, the installation is successful.

---

# 32. Important Swagger UI Watcher Limitation

The following command does **not** work:

```cmd
swagger-ui-watcher http://localhost:8055/server/specs/oas
```

because Swagger UI Watcher expects a local OpenAPI/Swagger file rather than the Directus URL directly.

It therefore tries to interpret the URL as a local file path.

---

# 33. Save Directus OpenAPI JSON

Open:

```text
http://localhost:8055/server/specs/oas
```

Save the JSON response as:

```text
openapi.json
```

For example:

```text
C:\DATA\VS_Code_Notes\SwaggerUI\openapi.json
```

---

# 34. Start Swagger UI Watcher

Navigate to the Swagger UI directory:

```cmd
cd C:\DATA\VS_Code_Notes\SwaggerUI
```

Run:

```cmd
swagger-ui-watcher openapi.json
```

Swagger UI Watcher starts a local Swagger interface.

The default port is:

```text
8000
```

Open:

```text
http://127.0.0.1:8000
```

The interactive Swagger UI will display the Directus OpenAPI endpoints.

---

# 35. Final Local Architecture

The completed local environment is:

```text
Windows
│
├── Node.js 22
│
├── Directus
│   │
│   ├── SQLite
│   │   └── data.db
│   │
│   └── REST APIs
│
├── OpenAPI Specification
│   └── http://localhost:8055/server/specs/oas
│
└── Swagger UI Watcher
    └── http://127.0.0.1:8000
```

---

# 36. Important URLs

| Purpose              | URL                                      |
| -------------------- | ---------------------------------------- |
| Directus Application | `http://localhost:8055`                  |
| Directus Admin       | `http://localhost:8055/admin`            |
| Employees API        | `http://localhost:8055/items/employees`  |
| OpenAPI JSON         | `http://localhost:8055/server/specs/oas` |
| Swagger UI           | `http://127.0.0.1:8000`                  |

---

# 37. Important Commands

### Start Directus

```cmd
cd C:\DATA\VS_Code_Notes\directus-project\my-directus-app
npx directus start
```

### Bootstrap Directus

```cmd
cd C:\DATA\VS_Code_Notes\directus-project\my-directus-app
npx directus bootstrap
```

### Check Node.js

```cmd
node -v
```

### Check npm

```cmd
npm -v
```

### Start Swagger UI

```cmd
cd C:\DATA\VS_Code_Notes\SwaggerUI
swagger-ui-watcher openapi.json
```

---

# 38. Troubleshooting Issues Encountered

## Issue 1 — Missing Directory

Command:

```cmd
npm create directus-project@latest
```

Error:

```text
missing required argument 'directory'
```

### Solution

Use:

```cmd
npx create-directus-project@latest my-directus-app
```

---

## Issue 2 — Unsupported Node.js Version

Node.js was initially:

```text
v24.14.0
```

The installer reported:

```text
Directus requires Node.js 22.
```

### Solution

Install/use Node.js 22 and verify:

```cmd
node -v
```

---

## Issue 3 — DB_CLIENT Environment Variable Missing

The Directus project creator reported:

```text
"DB_CLIENT" Environment Variable is missing.
```

### Solution

Complete the installation manually by installing Directus:

```cmd
npm install directus sqlite3
```

and configuring `.env`:

```env
DB_CLIENT=sqlite3
DB_FILENAME=./data.db
```

---

## Issue 4 — Duplicate SQLite Column

Bootstrap reported:

```text
SQLITE_ERROR: duplicate column name: project_owner
```

### Cause

The earlier failed installation had already partially initialized the SQLite database.

### Solution

For a fresh local installation, remove the partially initialized:

```text
data.db
```

and bootstrap again.

---

## Issue 5 — npm ECOMPROMISED / Lock Compromised

npm reported:

```text
npm error code ECOMPROMISED
npm error Lock compromised
```

### General Cleanup

If this occurs again:

```cmd
npm cache clean --force
```

Then remove the local:

```text
node_modules
package-lock.json
```

and reinstall:

```cmd
npm install directus sqlite3
```

---

## Issue 6 — Swagger UI Watcher Treating URL as File

Command:

```cmd
swagger-ui-watcher http://localhost:8055/server/specs/oas
```

failed because the watcher expects a local OpenAPI file.

### Solution

Save the OpenAPI JSON locally:

```text
openapi.json
```

Then run:

```cmd
swagger-ui-watcher openapi.json
```

---

# 39. Current Successful Setup

At the end of the installation process:

### Directus

```text
Running
```

### Directus Admin

```text
http://localhost:8055/admin
```

### Database

```text
SQLite
```

### Collection

```text
employees
```

### OpenAPI

```text
http://localhost:8055/server/specs/oas
```

### Swagger UI

```text
http://127.0.0.1:8000
```

The environment is therefore ready for:

* REST API testing
* Swagger/OpenAPI exploration
* Postman testing
* API automation
* API schema analysis
* AI-based API discovery
* AI-driven API test generation
* CRUD API experimentation
