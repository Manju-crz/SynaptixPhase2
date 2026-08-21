# Keycloak 26.7.1 – Installation, Swagger UI & API Testing Reference Notes

## 1. Purpose

Keycloak is an open-source Identity and Access Management (IAM) platform.

In this project, Keycloak is being used as a realistic application for:

* REST API testing
* Authentication and authorization testing
* User management API testing
* Role and permission testing
* Client management API testing
* OAuth 2.0 / OpenID Connect testing
* JWT testing
* OpenAPI / Swagger UI integration
* ReadyAPI integration
* API automation
* Positive and negative API test scenarios

---

# 2. Installed Keycloak Version

The installed version is:

```text
Keycloak 26.7.1
```

Installation type:

```text
Server ZIP Distribution
```

Operating system:

```text
Windows 11
```

Java detected by Keycloak:

```text
JVM: 17.0.18
Microsoft OpenJDK 64-Bit Server VM
```

---

# 3. Keycloak Installation Directory

Keycloak was extracted to:

```text
C:\CustomConfigs\keycloak-26.7.1
```

Therefore:

```text
Keycloak Home:
C:\CustomConfigs\keycloak-26.7.1
```

Important directories:

```text
C:\CustomConfigs\keycloak-26.7.1
│
├── bin
├── conf
├── data
├── lib
├── providers
└── themes
```

The main Windows launcher is:

```text
C:\CustomConfigs\keycloak-26.7.1\bin\kc.bat
```

---

# 4. Verify Keycloak Installation

Open Command Prompt.

Navigate to the Keycloak directory:

```cmd
cd C:\CustomConfigs\keycloak-26.7.1
```

Check the Keycloak version:

```cmd
bin\kc.bat --version
```

Expected output:

```text
Keycloak 26.7.1
JVM: 17.0.18 (Microsoft OpenJDK 64-Bit Server VM 17.0.18+8-LTS)
OS: Windows 11 10.0 amd64
```

This confirms that:

* Keycloak is installed.
* `kc.bat` is accessible.
* Java is detected.
* Windows is detected correctly.

---

# 5. Start Keycloak

For local development and testing, use development mode:

```cmd
bin\kc.bat start-dev
```

Keycloak will start using development-friendly configuration.

The Command Prompt running this command must remain open while Keycloak is running.

---

# 6. Verify Keycloak Is Running

The default HTTP port is:

```text
8080
```

Open:

```text
http://localhost:8080
```

Administration Console:

```text
http://localhost:8080/admin/
```

If the browser reports:

```text
ERR_CONNECTION_REFUSED
```

check whether port 8080 is listening.

Open another Command Prompt:

```cmd
netstat -ano | findstr :8080
```

A running Keycloak server should normally show something similar to:

```text
TCP    0.0.0.0:8080    0.0.0.0:0    LISTENING    <PID>
```

---

# 7. Initial Administrator

Keycloak does not come with a universal:

```text
admin / admin
```

username/password combination.

An initial administrator must be bootstrapped.

If necessary, stop Keycloak:

```text
Ctrl + C
```

Then run:

```cmd
bin\kc.bat bootstrap-admin user
```

Follow the prompts to create the initial administrator.

Then restart Keycloak:

```cmd
bin\kc.bat start-dev
```

Open:

```text
http://localhost:8080/admin/
```

and log in with the administrator credentials.

---

# 8. Keycloak Main Components

The main Keycloak concepts are:

```text
Keycloak
│
├── Realms
├── Users
├── Groups
├── Clients
├── Roles
├── Client Scopes
├── Identity Providers
├── Authentication
└── Authorization
```

For API testing, the most important components are:

```text
Realm
   ↓
Users
   ↓
Roles
   ↓
Clients
   ↓
Authentication
   ↓
Access Token / JWT
   ↓
REST API
```

---

# 9. Master Realm

A default Keycloak installation contains:

```text
master
```

The `master` realm is primarily intended for administration of Keycloak itself.

For application/API testing, create a separate realm.

Recommended example:

```text
fourth-sem-project
```

Result:

```text
Keycloak
│
├── master
│
└── fourth-sem-project
```

Use the application realm for test users, roles, clients and API testing.

---

# 10. Create Test Users

Inside the application realm:

```text
fourth-sem-project
```

go to:

```text
Users
    ↓
Create user
```

Example:

```text
Username: testuser
First Name: Test
Last Name: User
```

Configure the password under:

```text
Credentials
```

For a test user, `Temporary` can be set to:

```text
Off
```

when you don't want Keycloak to force a password change during the first login.

---

# 11. Create Roles

Roles represent permissions or responsibilities.

Example realm roles:

```text
admin
tester
developer
user
```

Possible testing model:

```text
admin
 ├── Create User
 ├── Update User
 ├── Delete User
 └── Manage Clients

tester
 ├── Read Users
 ├── Read Clients
 └── Execute API Tests

user
 └── Access permitted user functionality
```

Roles are particularly useful for testing:

```text
200 OK
401 Unauthorized
403 Forbidden
```

---

# 12. Create a Client

A Keycloak Client represents an application or service that communicates with Keycloak.

Example:

```text
Client ID:
api-test-client
```

Protocol:

```text
OpenID Connect
```

Possible clients for API testing:

```text
web-app
api
postman-client
readyapi-client
swagger-client
```

---

# 13. Authentication Flow

The general authentication flow is:

```text
Application / Client
        │
        │ Authentication request
        ▼
     Keycloak
        │
        │ Authenticate user
        ▼
       User
        │
        │ Successful authentication
        ▼
   Access Token
        │
        ▼
Protected REST API
```

The access token is commonly a JWT.

The token is supplied to an API using:

```http
Authorization: Bearer <access_token>
```

---

# 14. Keycloak Admin REST API

Keycloak provides an Admin REST API for programmatically managing Keycloak resources.

The API includes operations related to:

```text
Realms
Users
Groups
Clients
Roles
Client Scopes
Identity Providers
Authentication
Components
Sessions
Keys
Events
Authorization
Organizations
```

This makes Keycloak suitable for building a realistic API automation framework.

---

# 15. Official Keycloak REST API Documentation

Official REST API documentation:

```text
https://www.keycloak.org/docs-api/latest/rest-api/index.html
```

Official OpenAPI JSON:

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

The OpenAPI JSON can be consumed by:

```text
Swagger UI
Swagger Editor
Postman
ReadyAPI
Other OpenAPI-compatible tools
```

---

# 16. Understanding the "latest" OpenAPI URL

The official URL is:

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

The word:

```text
latest
```

refers to the latest documentation/API-definition stream.

It does not mean:

```text
Keycloak version = latest
```

If the OpenAPI document contains:

```json
"version": "1.0"
```

that should not be interpreted as:

```text
Keycloak 1.0
```

The locally installed Keycloak version remains:

```text
26.7.1
```

For learning and initial API testing, the official OpenAPI definition is appropriate.

For a production-grade automation framework, API compatibility should always be checked against the Keycloak version actually deployed.

---

# 17. Download the Keycloak OpenAPI JSON

Open the following URL:

```text
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json
```

Save the file locally as:

```text
keycloak-openapi.json
```

Example location:

```text
C:\CustomConfigs\keycloak-openapi.json
```

The directory can therefore look like:

```text
C:\CustomConfigs
│
├── keycloak-26.7.1
│
└── keycloak-openapi.json
```

---

# 18. Swagger UI

Swagger UI is a web interface that reads an OpenAPI definition and displays the APIs in an interactive format.

It allows you to see:

* API endpoints
* HTTP methods
* Parameters
* Request bodies
* Response codes
* Schemas
* Authentication requirements
* Try It Out functionality

Architecture:

```text
Keycloak
   │
   │ OpenAPI definition
   ▼
keycloak-openapi.json
   │
   ▼
Swagger UI
   │
   ▼
Interactive API documentation
```

---

# 19. Option 1 – Swagger Editor

For a quick test, use the online Swagger Editor:

```text
https://editor.swagger.io/
```

You can import or paste the Keycloak OpenAPI JSON into Swagger Editor.

The API definition will then be displayed interactively.

This is useful for quickly examining the API specification.

However, for this project, running Swagger UI locally is preferable.

---

# 20. Option 2 – Run Swagger UI Using Docker

If Docker Desktop is installed, Swagger UI can be run locally.

Open Command Prompt and execute:

```cmd
docker run -p 8081:8080 swaggerapi/swagger-ui
```

Swagger UI will then be available at:

```text
http://localhost:8081
```

Important:

```text
Keycloak:
http://localhost:8080

Swagger UI:
http://localhost:8081
```

These are two different applications.

---

# 21. Run Swagger UI and Automatically Load Keycloak OpenAPI JSON

Suppose the OpenAPI file is stored here:

```text
C:\CustomConfigs\keycloak-openapi.json
```

Run:

```cmd
docker run -p 8081:8080 ^
  -e SWAGGER_JSON=/foo/keycloak-openapi.json ^
  -v C:\CustomConfigs:/foo ^
  swaggerapi/swagger-ui
```

Explanation:

```text
-p 8081:8080
```

Maps the Docker Swagger UI port to:

```text
localhost:8081
```

This:

```text
-e SWAGGER_JSON=/foo/keycloak-openapi.json
```

tells Swagger UI which OpenAPI file to load.

This:

```text
-v C:\CustomConfigs:/foo
```

mounts the Windows directory into the Docker container.

---

# 22. Open Swagger UI

After starting the Docker container, open:

```text
http://localhost:8081
```

Swagger UI should automatically display the Keycloak Admin REST API.

You should see API groups related to resources such as:

```text
Users
Clients
Roles
Realms
Groups
Authentication
Client Scopes
Identity Providers
```

---

# 23. Swagger UI and Keycloak Are Separate

The final local setup is:

```text
                 Windows
                    │
        ┌───────────┴────────────┐
        │                        │
        ▼                        ▼
Keycloak 26.7.1             Swagger UI
localhost:8080              localhost:8081
        │                        │
        │                        │
        │                 Reads OpenAPI
        │                 JSON definition
        │                        │
        └────────────┬───────────┘
                     │
                 REST APIs
```

Swagger UI does not replace Keycloak.

Swagger UI is simply the interface used to view and interact with the APIs.

---

# 24. Important: OpenAPI JSON Does Not Provide Authentication

Importing:

```text
keycloak-openapi.json
```

into Swagger UI only gives Swagger UI the API definitions.

It does not automatically authenticate against Keycloak.

For protected Admin REST APIs, an access token is normally required.

Example:

```http
Authorization: Bearer eyJhbGciOi...
```

Therefore:

```text
OpenAPI JSON
     ↓
Swagger UI
     ↓
API definition
     ↓
Configure authentication
     ↓
Obtain Keycloak access token
     ↓
Send Bearer token
     ↓
Execute protected API
```

---

# 25. Example User APIs

Typical user-management operations include:

```http
GET    /admin/realms/{realm}/users
POST   /admin/realms/{realm}/users
GET    /admin/realms/{realm}/users/{user-id}
PUT    /admin/realms/{realm}/users/{user-id}
DELETE /admin/realms/{realm}/users/{user-id}
```

Possible test flow:

```text
Create User
     ↓
Get User
     ↓
Update User
     ↓
Verify User
     ↓
Delete User
```

---

# 26. Example Client API Test Flow

```text
Create Client
      ↓
Configure Client
      ↓
Get Client
      ↓
Update Client
      ↓
Verify Client
      ↓
Delete Client
```

---

# 27. Example Role API Test Flow

```text
Create Role
      ↓
Assign Role to User
      ↓
Verify Role Assignment
      ↓
Remove Role
      ↓
Verify Role Removal
```

---

# 28. Authentication Test Scenarios

## Positive Scenario

```text
Valid credentials
       ↓
Authentication successful
       ↓
Access Token
       ↓
API request
       ↓
200 OK
```

## No Token

```text
No Authorization header
       ↓
Protected API
       ↓
401 Unauthorized
```

## Invalid Token

```text
Invalid Bearer Token
       ↓
Protected API
       ↓
401 Unauthorized
```

## Expired Token

```text
Expired Token
       ↓
Protected API
       ↓
401 Unauthorized
```

## Insufficient Permission

```text
Valid Token
+
Insufficient Role
       ↓
Protected API
       ↓
403 Forbidden
```

---

# 29. Recommended API Testing Architecture

The intended architecture for this project is:

```text
                    Keycloak 26.7.1
                          │
                          │
                 Authentication
                          │
                          ▼
                   Access Token
                       (JWT)
                          │
                          ▼
               ┌────────────────────┐
               │ Swagger UI /       │
               │ ReadyAPI           │
               └─────────┬──────────┘
                         │
                   Bearer Token
                         │
                         ▼
               Keycloak Admin REST API
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
           Users       Roles      Clients
```

---

# 30. Recommended Learning / Testing Sequence

Follow this sequence:

```text
1. Install Keycloak 26.7.1
        ↓
2. Start Keycloak
        ↓
3. Create administrator
        ↓
4. Create application Realm
        ↓
5. Create test Users
        ↓
6. Create Roles
        ↓
7. Create Client
        ↓
8. Understand OAuth 2.0 / OIDC
        ↓
9. Obtain Access Token
        ↓
10. Download Keycloak OpenAPI JSON
        ↓
11. Install/Run Swagger UI
        ↓
12. Load OpenAPI JSON into Swagger UI
        ↓
13. Configure Bearer/OAuth authentication
        ↓
14. Execute User APIs
        ↓
15. Execute Role APIs
        ↓
16. Execute Client APIs
        ↓
17. Create positive API tests
        ↓
18. Create negative API tests
        ↓
19. Automate the complete test suite
```

---

# 31. Useful Commands

## Navigate to Keycloak

```cmd
cd C:\CustomConfigs\keycloak-26.7.1
```

## Verify Keycloak version

```cmd
bin\kc.bat --version
```

## Start Keycloak

```cmd
bin\kc.bat start-dev
```

## Stop Keycloak

```text
Ctrl + C
```

## Check Keycloak port

```cmd
netstat -ano | findstr :8080
```

## Create bootstrap administrator if required

```cmd
bin\kc.bat bootstrap-admin user
```

## Run Swagger UI with Docker

```cmd
docker run -p 8081:8080 swaggerapi/swagger-ui
```

## Run Swagger UI and load local OpenAPI JSON

```cmd
docker run -p 8081:8080 ^
  -e SWAGGER_JSON=/foo/keycloak-openapi.json ^
  -v C:\CustomConfigs:/foo ^
  swaggerapi/swagger-ui
```

---

# 32. Important URLs

| Purpose                         | URL                                                              |
| ------------------------------- | ---------------------------------------------------------------- |
| Keycloak Server                 | `http://localhost:8080`                                          |
| Keycloak Admin Console          | `http://localhost:8080/admin/`                                   |
| Swagger UI                      | `http://localhost:8081`                                          |
| Swagger Editor                  | `https://editor.swagger.io/`                                     |
| Keycloak REST API Documentation | `https://www.keycloak.org/docs-api/latest/rest-api/index.html`   |
| Keycloak OpenAPI JSON           | `https://www.keycloak.org/docs-api/latest/rest-api/openapi.json` |

---

# 33. Current Environment Summary

```text
Application:
Keycloak

Version:
26.7.1

Installation Type:
Server ZIP Distribution

Operating System:
Windows 11

Java:
Microsoft OpenJDK 17.0.18

Keycloak Installation:
C:\CustomConfigs\keycloak-26.7.1

Keycloak Startup:
bin\kc.bat start-dev

Keycloak Version Check:
bin\kc.bat --version

Keycloak HTTP Port:
8080

Keycloak URL:
http://localhost:8080

Keycloak Admin Console:
http://localhost:8080/admin/

OpenAPI JSON:
https://www.keycloak.org/docs-api/latest/rest-api/openapi.json

Local OpenAPI File:
C:\CustomConfigs\keycloak-openapi.json

Swagger UI Port:
8081

Swagger UI URL:
http://localhost:8081
```

---

# 34. Key Takeaways

1. Keycloak 26.7.1 has been successfully installed.
2. Java 17.0.18 is being used by the installation.
3. Keycloak is installed at `C:\CustomConfigs\keycloak-26.7.1`.
4. `bin\kc.bat start-dev` starts the local Keycloak server.
5. Keycloak is available on port `8080`.
6. The Administration Console is available at `/admin/`.
7. The `master` realm should generally be kept for Keycloak administration.
8. A separate application realm should be created for API testing.
9. Users, Roles and Clients are important resources for API testing.
10. Keycloak provides an Admin REST API.
11. The official OpenAPI JSON can be used to generate/view the REST APIs.
12. The `latest` URL refers to the latest documentation stream; it does not mean Keycloak version 1.0.
13. Swagger UI can be run locally using Docker.
14. Swagger UI can be run on port `8081`.
15. The Keycloak OpenAPI JSON can be mounted into the Swagger UI Docker container.
16. Swagger UI displays the API definitions but does not automatically authenticate.
17. Protected Keycloak Admin APIs require an appropriate access token.
18. Bearer-token authentication should be configured before executing protected APIs.
19. User, Role and Client APIs provide a realistic API automation exercise.
20. Positive and negative authentication/authorization scenarios can be created using Keycloak.

---

# 35. Final Project Flow

The complete environment established for this project is:

```text
                     ┌───────────────────────┐
                     │    Keycloak 26.7.1    │
                     │    localhost:8080     │
                     └───────────┬───────────┘
                                 │
                         Users / Roles /
                       Clients / Realms
                                 │
                                 ▼
                         Authentication
                                 │
                                 ▼
                           JWT Token
                                 │
                                 ▼
┌───────────────────────┐   Bearer Token   ┌────────────────────────┐
│      Swagger UI       │ ───────────────► │ Keycloak Admin REST API│
│   localhost:8081      │                  │                        │
└───────────┬───────────┘                  └────────────────────────┘
            │
            │
            ▼
   keycloak-openapi.json
            │
            ▼
      API Definitions
            │
            ▼
     API Test Scenarios
            │
            ▼
     ReadyAPI / Automation
```

This establishes the complete foundation for using **Keycloak as an API-testing target application**, from installation through OpenAPI/Swagger visualization and eventually authenticated API automation.
