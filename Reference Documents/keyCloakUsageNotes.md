# Keycloak – Purpose, Consumers, SSO and Application Architecture

## 1. What is Keycloak?

**Keycloak** is an open-source **Identity and Access Management (IAM)** application.

Its primary responsibility is to manage:

* User identities
* Authentication (login)
* Authorization and access control
* Users and credentials
* Roles
* Groups
* Clients/applications
* Sessions
* Access tokens / JWTs
* Single Sign-On (SSO)

In simple words:

> **Keycloak acts as a central security and identity system for multiple applications.**

---

# 2. Who Consumes Keycloak?

The primary consumers of Keycloak are:

* Web applications
* Mobile applications
* REST APIs
* Backend services
* Microservices
* Other software applications

The end users, such as employees, customers or administrators, are the **users managed by Keycloak**, while the applications are the systems that **integrate with and consume Keycloak's authentication and authorization services**.

Example:

```text
                   Keycloak
              Identity & Security
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       HR One     Institute Note   EMS
       Portal       Application   Portal
```

---

# 3. What Does Keycloak Actually Do?

Keycloak primarily provides two important security functions:

## Authentication

Authentication answers:

> **"Who are you?"**

For example:

```text
Username: john.employee
Password: ********
```

Keycloak verifies the user's credentials.

If they are valid, Keycloak authenticates the user.

---

## Authorization

Authorization answers:

> **"What are you allowed to do?"**

For example:

```text
John
 │
 └── Role: Employee
```

John may be allowed to:

```text
View his own information
Access employee portal
Submit requests
```

But he may not be allowed to:

```text
Create employees
Delete users
Manage system configuration
```

Therefore:

```text
Authentication = Who are you?
Authorization  = What can you do?
```

---

# 4. Keycloak Is Not Normally the Business Database

Keycloak should not normally be considered the main database for the company's business information.

Instead, there are two separate layers:

```text
                 Company
                    │
        ┌───────────┴───────────┐
        │                       │
 Business Data             Security / Identity
        │                       │
        ▼                       ▼
Application Databases        Keycloak
```

### Keycloak manages:

```text
Users
Roles
Groups
Credentials
Clients
Sessions
Tokens
Authentication
Authorization
```

### Individual applications manage:

```text
Employee salary
Leave records
Invoices
Payments
Attendance
Payroll
Business transactions
Notes
Documents
Application-specific data
```

---

# 5. Example – Synaptix Technologies

Suppose Synaptix Technologies has several independent applications:

```text
Synaptix Technologies
        │
        ├── HR One
        ├── Institute Note
        ├── EMS
        ├── Finance Portal
        └── Employee Portal
```

Each application can have its own database and business functionality.

Keycloak can sit in the middle as the common identity and security layer:

```text
                    Keycloak
             Identity / Authentication
                    Authorization
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
    HR One         Institute Note         EMS
       │                 │                 │
       ▼                 ▼                 ▼
   HR Database       Notes DB           EMS Database
```

---

# 6. Single Sign-On (SSO)

One of the major benefits of Keycloak is **Single Sign-On (SSO)**.

SSO means that a user can authenticate once and then access multiple applications without repeatedly entering their username and password, provided those applications are configured to use the same Keycloak identity system.

Example:

```text
John
 │
 ▼
HR One
 │
 ▼
Keycloak
 │
 └── John authenticates
       │
       ▼
    HR One access
```

Later:

```text
John
 │
 ▼
EMS
 │
 ▼
Keycloak
 │
 └── Existing Keycloak session
       │
       ▼
    EMS access
```

John does not necessarily need to enter his credentials again.

---

# 7. How SSO Works Across Multiple Applications

Consider three applications:

```text
                    Keycloak
                       │
                 Single Sign-On
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       HR One      Institute Note    EMS
```

A typical flow is:

```text
1. User opens HR One
          ↓
2. HR One redirects user to Keycloak
          ↓
3. Keycloak authenticates the user
          ↓
4. Keycloak provides an authentication/access token
          ↓
5. HR One grants access
```

Later:

```text
1. User opens EMS
          ↓
2. EMS communicates with Keycloak
          ↓
3. Keycloak recognizes the existing authenticated session
          ↓
4. EMS grants access
```

This provides the SSO experience.

---

# 8. Role of Access Tokens

After successful authentication, Keycloak can issue an **access token**, commonly a JWT.

Conceptually:

```text
User
  │
  │ Login
  ▼
Keycloak
  │
  │ Authentication successful
  ▼
Access Token (JWT)
  │
  ▼
Application / API
```

The application can use the token when calling protected APIs.

Example:

```http
Authorization: Bearer <access_token>
```

The token can contain information such as:

```text
User identity
Roles
Scopes
Other claims
```

The receiving application/API can use this information when enforcing access control.

---

# 9. Users, Groups and Roles

Keycloak provides several mechanisms for organizing identities.

### Users

Represent individual people or service identities.

Example:

```text
john.employee
jane.employee
hr.manager
it.manager
```

### Groups

Used to organize users.

Example:

```text
HR
IT
Finance
Management
Employees
```

### Roles

Represent permissions/responsibilities.

Example:

```text
company-admin
manager
employee
auditor
```

Example structure:

```text
Synaptix Technologies
        │
        ├── Users
        │    ├── John
        │    ├── Jane
        │    └── David
        │
        ├── Groups
        │    ├── HR
        │    ├── IT
        │    └── Finance
        │
        └── Roles
             ├── Admin
             ├── Manager
             └── Employee
```

---

# 10. Applications as Keycloak Clients

Each application that integrates with Keycloak is generally represented as a **Client**.

For example:

```text
Keycloak
   │
   └── synaptix-technologies
          │
          ├── Client: hr-one
          ├── Client: institute-note
          ├── Client: ems
          └── Client: finance-portal
```

Each client represents an application/service that uses Keycloak for authentication and/or authorization.

---

# 11. Important Distinction – Keycloak vs Application

Keycloak does **not** replace the applications.

For example:

```text
                    Keycloak
              Security / Identity
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    HR One       Institute Note         EMS
       │               │                │
       ▼               ▼                ▼
   HR Data         Notes Data         EMS Data
```

### Keycloak decides/handles:

> Who is this user?

> Has this user authenticated?

> What roles/identity information does this user have?

> Can this application/API authenticate and authorize this request?

### The application handles:

> What business data does the user see?

> What business operation should be performed?

> How should the company's business rules be applied?

> How should application-specific data be stored?

---

# 12. Example – Employee Access

Suppose John is an employee:

```text
John
 │
 ├── Username: john.employee
 ├── Group: Employees
 └── Role: employee
```

John opens HR One:

```text
John
  ↓
HR One
  ↓
Keycloak
  ↓
Authentication
  ↓
Access Token
  ↓
HR One
```

HR One can then use John's identity/roles to determine what functionality John can access.

For example:

```text
John – Employee
 ├── View own HR information       → Allowed
 ├── Submit leave request          → Allowed
 ├── View employee portal          → Allowed
 └── Manage other employees       → Not allowed
```

The exact authorization rules can be implemented by the application and/or Keycloak's authorization capabilities depending on the architecture.

---

# 13. Example – Administrator Access

Consider a Synaptix administrator:

```text
admin.synaptix
       │
       └── Role: company-admin
```

The administrator may be given broader access:

```text
HR One
 ├── Manage employees
 └── View HR information

EMS
 ├── Manage users
 └── Manage configuration

Finance Portal
 └── Administrative functions
```

The applications can use the user's Keycloak identity and assigned roles when deciding what functionality to expose.

---

# 14. Overall Architecture

A typical enterprise architecture can look like:

```text
                         SYNAPTIX TECHNOLOGIES
                                  │
                                  ▼
                             KEYCLOAK
                    Identity & Access Management
                                  │
               ┌──────────────────┼──────────────────┐
               │                  │                  │
               ▼                  ▼                  ▼
            HR One          Institute Note          EMS
          Application         Application        Application
               │                  │                  │
               ▼                  ▼                  ▼
          HR Database          Notes DB           EMS DB
```

Keycloak provides the common security layer while each application maintains its own business functionality and data.

---

# 15. Simple Real-World Analogy

Think of Keycloak as the **security gate and identity card system of a company campus**.

```text
Employee
    │
    ▼
Security Gate
    │
    ▼
Keycloak
    │
    ├── Verify identity
    ├── Check access
    └── Issue/validate credentials
    │
    ├─────────────┬─────────────┐
    ▼             ▼             ▼
   HR            Finance        IT
```

The security gate knows:

> "Who is this person?"

and:

> "Which areas are they allowed to enter?"

But the security gate does not maintain the actual HR, Finance or IT business data.

---

# 16. Keycloak in One Sentence

> **Keycloak is a central Identity and Access Management platform that allows multiple applications and APIs to share user identities, authentication, authorization and Single Sign-On, while each application continues to manage its own business data.**

---

# 17. Synaptix Technologies – Final Concept

For the Synaptix Technologies setup, the intended architecture can be summarized as:

```text
                      SYNAPTIX TECHNOLOGIES
                              │
                              ▼
                     KEYCLOAK REALM
                  synaptix-technologies
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
           Users           Groups            Roles
              │               │                │
              └───────────────┼────────────────┘
                              │
                              ▼
                           Clients
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
           HR One       Institute Note         EMS
              │               │                │
              ▼               ▼                ▼
        HR Business      Notes Business    EMS Business
            Data             Data              Data
```

### Core principle

**Keycloak = Identity + Authentication + Authorization + SSO**

**Applications = Business functionality + Business data**

This separation allows Synaptix Technologies to have multiple independent portals/applications while maintaining a common identity and security infrastructure through Keycloak.
