# Swagger UI – Installation, Launch and OpenAPI Usage Reference Notes

## 1. What is Swagger UI?

**Swagger UI** is a web-based interface used to visualize and interact with APIs described using the **OpenAPI Specification**.

It allows us to:

* View available API endpoints.
* Understand HTTP methods such as `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.
* View request parameters and request bodies.
* View expected API responses.
* Execute APIs using **Try it out**.
* Load an OpenAPI JSON/YAML specification.

> Swagger UI does not create or implement APIs. It reads an existing OpenAPI specification and provides a user-friendly interface for viewing and testing those APIs.

---

# 2. Swagger UI Installation

After downloading/extracting Swagger UI, the important directory for basic usage is:

```text
swagger-ui/
└── dist/
    ├── index.html
    ├── swagger-ui.css
    ├── swagger-ui-bundle.js
    └── ...
```

For this setup, we use the `dist` directory.

Example:

```text
C:\swagger-ui\dist
```

---

# 3. How to Launch Swagger UI

Swagger UI should preferably be launched through a local HTTP server instead of opening `index.html` directly using `file://`.

## Step 1 – Open Command Prompt / PowerShell

Navigate to the Swagger UI `dist` folder:

```bash
cd C:\swagger-ui\dist
```

Replace the path with the actual location of Swagger UI on your system.

## Step 2 – Start the Python HTTP Server

Run:

```bash
python -m http.server 8080
```

You should see something similar to:

```text
Serving HTTP on 0.0.0.0 port 8080
```

Keep this terminal window open while using Swagger UI.

## Step 3 – Open Swagger UI

Open a browser and navigate to:

```text
http://localhost:8080
```

Swagger UI should now be displayed.

## Step 4 – Stop Swagger UI

When finished, return to the Command Prompt and press:

```text
Ctrl + C
```

This stops the local HTTP server.

---

# 4. How Swagger UI Loads an OpenAPI JSON

Swagger UI needs an **OpenAPI specification**.

The specification can be:

* A local JSON file.
* A local YAML file.
* A remote JSON URL.
* A remote YAML URL.

For example:

```text
OpenAPI JSON
     |
     v
Swagger UI
     |
     v
API Documentation
     |
     v
Try it out
     |
     v
Actual API Server
```

---

# 5. Loading a Local OpenAPI JSON File

Suppose you have:

```text
C:\swagger-ui\dist\openapi.json
```

Your folder structure would be:

```text
C:\swagger-ui\
└── dist\
    ├── index.html
    ├── swagger-ui-bundle.js
    ├── swagger-ui.css
    └── openapi.json
```

Because the `dist` directory is being served at:

```text
http://localhost:8080
```

the OpenAPI JSON becomes available at:

```text
http://localhost:8080/openapi.json
```

---

# 6. Configure Swagger UI to Load the Local JSON

Open:

```text
C:\swagger-ui\dist\index.html
```

Find the Swagger UI configuration section.

It may contain something similar to:

```javascript
url: "https://petstore.swagger.io/v2/swagger.json",
```

Change it to:

```javascript
url: "openapi.json",
```

Save the file.

Now start Swagger UI:

```bash
cd C:\swagger-ui\dist
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Swagger UI will load:

```text
http://localhost:8080/openapi.json
```

and display the APIs defined in that file.

---

# 7. Loading an OpenAPI JSON from a Remote URL

Instead of storing the JSON locally, Swagger UI can directly load an OpenAPI specification from a URL.

For example:

```javascript
url: "https://example.com/openapi.json",
```

The general flow is:

```text
Remote OpenAPI JSON URL
          |
          v
     Swagger UI
          |
          v
    API Documentation
```

---

# 8. Using Keycloak OpenAPI JSON

For the Keycloak installation, we identified the following OpenAPI specification URL:

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

The URL contains:

```text
latest
```

rather than a specific Keycloak version.

This is acceptable when the intention is to use the **latest API documentation provided by Keycloak**.

---

# 9. Configure Swagger UI for Keycloak

Open:

```text
C:\swagger-ui\dist\index.html
```

Configure the OpenAPI URL as:

```javascript
url: "https://www.keycloak.org/docs-api/latest/rest-api/openapi.json",
```

Save the file.

Then start Swagger UI:

```bash
cd C:\swagger-ui\dist
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Swagger UI will retrieve the Keycloak OpenAPI specification and display the available Keycloak REST APIs.

---

# 10. Testing an API Using Swagger UI

Once the OpenAPI specification is loaded, Swagger UI displays the available endpoints.

Example:

```text
GET     /users
POST    /users
GET     /users/{id}
PUT     /users/{id}
DELETE  /users/{id}
```

To test an endpoint:

### Step 1

Select the required API endpoint.

### Step 2

Click:

```text
Try it out
```

### Step 3

Enter the required parameters/request body.

### Step 4

Click:

```text
Execute
```

Swagger UI sends the HTTP request to the API server.

The response will show information such as:

```text
Request URL
Response Code
Response Headers
Response Body
```

Example:

```text
Response Code: 200
```

---

# 11. Testing a POST API

For example:

```text
POST /users
```

Swagger UI may provide a request-body editor.

Example:

```json
{
  "name": "John",
  "email": "john@example.com"
}
```

Click:

```text
Try it out
```

Then:

```text
Execute
```

Swagger UI sends the JSON request to the API server and displays the response.

---

# 12. Authentication

Many APIs require authentication.

Swagger UI may provide an:

```text
Authorize
```

button.

Depending on the API, authentication can use:

* Basic Authentication
* Bearer Token
* OAuth 2.0
* API Key
* OpenID Connect

For example:

```text
Authorization: Bearer <access-token>
```

For Keycloak APIs, authentication is particularly important because many administrative REST APIs require a valid Keycloak access token.

---

# 13. Important Swagger/OpenAPI Terminology

| Term                  | Meaning                                                              |
| --------------------- | -------------------------------------------------------------------- |
| **OpenAPI**           | Standard specification used to describe APIs                         |
| **OpenAPI JSON/YAML** | Actual API definition file                                           |
| **Swagger UI**        | Web interface for viewing/interacting with the OpenAPI specification |
| **Endpoint**          | Specific API URL, e.g. `/users`                                      |
| **HTTP Method**       | GET, POST, PUT, PATCH, DELETE, etc.                                  |
| **Request**           | Information sent to the API                                          |
| **Response**          | Information returned by the API                                      |
| **Schema**            | Structure/format of request or response data                         |
| **Swagger Editor**    | Tool for creating/editing OpenAPI specifications                     |

---

# 14. Swagger UI vs Postman

Swagger UI and Postman can both be used for API testing, but their primary purposes differ.

| Feature                | Swagger UI | Postman   |
| ---------------------- | ---------- | --------- |
| API documentation      | Excellent  | Limited   |
| OpenAPI integration    | Excellent  | Excellent |
| Quick API exploration  | Excellent  | Excellent |
| Try API from browser   | Yes        | Yes       |
| Test scripting         | Limited    | Strong    |
| Collections            | Limited    | Strong    |
| Environment management | Basic      | Strong    |
| Automated API testing  | Limited    | Strong    |

A practical workflow is:

```text
OpenAPI Specification
        |
        +------------------+
        |                  |
        v                  v
   Swagger UI           Postman
        |                  |
        v                  v
Understand &          Detailed API
explore APIs          testing/automation
```

---

# 15. Practical Workflow for API Testing

For API testing and automation, the following workflow is useful:

```text
1. Identify the application
             ↓
2. Find its OpenAPI JSON/YAML
             ↓
3. Load the specification into Swagger UI
             ↓
4. Explore available endpoints
             ↓
5. Understand parameters and request bodies
             ↓
6. Perform exploratory testing using "Try it out"
             ↓
7. Validate API responses
             ↓
8. Create detailed tests in Postman / ReadyAPI
             ↓
9. Automate the API test scenarios
             ↓
10. Execute through CI/CD
```

---

# 16. Quick Reference – Commands

### Navigate to Swagger UI

```bash
cd C:\swagger-ui\dist
```

### Start Swagger UI

```bash
python -m http.server 8080
```

### Open Swagger UI

```text
http://localhost:8080
```

### Stop Swagger UI

```text
Ctrl + C
```

---

# 17. Quick Reference – Local OpenAPI JSON

If the file is:

```text
C:\swagger-ui\dist\openapi.json
```

Configure `index.html`:

```javascript
url: "openapi.json",
```

Then:

```bash
cd C:\swagger-ui\dist
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

Swagger UI loads:

```text
http://localhost:8080/openapi.json
```

---

# 18. Quick Reference – Keycloak OpenAPI JSON

Keycloak OpenAPI specification:

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

Configure `index.html`:

```javascript
url: "https://www.keycloak.org/docs-api/latest/rest-api/openapi.json",
```

Then:

```bash
cd C:\swagger-ui\dist
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

---

# 19. Most Important Things to Remember

```text
Swagger UI
    ↓
Reads OpenAPI JSON/YAML
    ↓
Generates API documentation
    ↓
"Try it out"
    ↓
Sends request to actual API
    ↓
Displays API response
```

### The three commands/URLs to remember

**Launch command:**

```bash
python -m http.server 8080
```

**Swagger UI:**

```text
http://localhost:8080
```

**Keycloak OpenAPI specification:**

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

> **Key concept:** Swagger UI is the **interface**, OpenAPI JSON is the **API description**, and the actual application (such as Keycloak) is the **API provider**.



PS C:\DATA\VS_Code_Notes\SwaggerUI> swagger-ui-watcher .\keycloak.json
Listening on http://127.0.0.1:8000


