# ClientTrack

ClientTrack is a backend-focused Django mini CRM application designed to help users manage clients, interactions, sales opportunities, follow-up activities, team members, and business reports in one place.

The project focuses on secure backend architecture, authentication, authorization, ownership control, strict user-specific data isolation, automated testing, and production deployment.

## Live Application

**Production:** https://clienttrack.tanersahindev.com

ClientTrack is deployed on a production VPS using Ubuntu Linux, PostgreSQL, Gunicorn, Nginx, SSL/TLS, HTTPS, and HSTS.

---

## Key Highlights

- Django-based CRM application
- Secure authentication and authorization
- Strict user-specific data isolation
- Client management
- Interaction tracking
- Sales pipeline management
- Smart follow-up reminders
- Team management
- Reports and dashboard
- Ownership-protected CRUD operations
- 61 automated tests passing
- Modular Django application structure
- PostgreSQL production database
- Gunicorn application server
- Nginx reverse proxy
- HTTPS production deployment
- HSTS enabled
- systemd service management

---

## Features

### Authentication

- User registration
- User login
- POST-based logout
- Custom Django user model
- Login-protected application features
- Authenticated user-specific data access
- Automated authentication tests

### Client Management

- Create, view, update, and delete clients
- User-specific client ownership
- Ownership-protected detail pages
- Secure update and delete operations
- Client data isolation between users

Each client belongs to the authenticated user. Client querysets are restricted using ownership filtering so one user cannot access another user's client records.

### Interaction Management

- Create, view, update, and delete interactions
- Associate interactions with clients
- Track different interaction types
- Store follow-up dates
- User-specific interaction filtering
- Ownership protection for interaction records

Interactions allow users to keep track of communication and follow-up activities related to their clients.

### Sales Pipeline

- Create and manage sales opportunities
- Track deal stages
- Store opportunity values
- Monitor open, won, and lost deals
- User-specific sales records
- Ownership-protected CRUD operations

The sales module provides a simple CRM pipeline for tracking opportunities throughout the sales process.

### Smart Follow-up Reminders

- Track upcoming follow-ups
- Detect overdue follow-ups
- Track completed follow-ups
- Mark follow-ups as completed
- POST-based state-changing operations
- User-specific reminder filtering
- Security and ownership tests

The reminder system uses interaction follow-up dates to help users identify activities that require attention.

### Team Management

- Create, view, update, and delete team members
- Store team member name and email
- Assign team roles
- Activate or deactivate team members
- User-specific team ownership
- Ownership-protected detail, update, and delete operations

Supported roles include:

- Manager
- Sales
- Support
- Other

Each team member belongs to the authenticated owner and cannot be accessed by another user.

### Reports and Dashboard

ClientTrack includes user-specific business reports and dashboard statistics.

Reports include:

- Total client count
- Total interaction count
- Total deal count
- Pipeline value
- Open deals
- Won deals
- Lost deals
- Deal stage summary
- Recent interactions
- Upcoming follow-ups

All report calculations are restricted to the authenticated user's own records.

---

## Secure Data Isolation

ClientTrack is designed around strict user-specific data isolation.

The core security rule is:

> An authenticated user can access only records that belong to that user.

Ownership filtering is enforced on the backend using Django ORM querysets.

Example:

```python
Client.objects.filter(user=request.user)
```

Detail, update, and delete operations enforce ownership checks:

```python
get_object_or_404(
    Model,
    pk=pk,
    user=request.user,
)
```

Team member ownership follows the same principle using the `owner` field.

This prevents users from accessing another user's records by manually changing object IDs in URLs.

The isolation model applies to:

- Clients
- Interactions
- Sales opportunities
- Follow-up reminders
- Team members
- Reports and dashboard data

Unauthorized record access returns a 404 response rather than exposing another user's private data.

---

## Authentication, Authorization and Ownership

ClientTrack separates three important backend security concepts:

### Authentication

Determines who the user is.

### Authorization

Determines what the authenticated user is allowed to access.

### Ownership

Determines which records belong to the authenticated user.

These concepts are enforced throughout the application's backend rather than relying on frontend restrictions.

---

## Tech Stack

### Backend

- Python 3.12.10
- Django 5.2.17
- Django ORM
- Django Templates

### Database

- SQLite for local development
- PostgreSQL for production

### Frontend

- HTML5
- CSS3
- Bootstrap 5

### Testing

- Django TestCase
- Django Test Client
- Automated security and regression testing

### Production Infrastructure

- VPS
- Ubuntu Linux
- PostgreSQL
- Gunicorn
- Nginx
- systemd
- Domain and DNS configuration
- SSL/TLS
- HTTPS
- HSTS

### Development and Version Control

- Git
- GitHub
- Visual Studio Code

---

## Automated Testing

ClientTrack includes an automated test suite built with Django's testing framework.

Current test status:

**61 tests passed successfully.**

The test suite verifies important application behavior including:

- Authentication
- Registration
- Login
- POST logout
- CRUD operations
- Login protection
- Authorization
- Ownership protection
- User isolation
- Client security
- Interaction security
- Sales security
- Follow-up reminder security
- Team member security
- Reports
- Secure data isolation page

### Run the Tests

```bash
python manage.py test
```

Expected result:

```text
Ran 61 tests

OK
```

Automated testing is especially important in ClientTrack because security rules must continue working as new application features are added.

---

## Project Structure

ClientTrack follows a modular Django application architecture.

```text
clienttrack/
│
├── accounts/          # Authentication and custom user
├── clients/           # Client management
├── interactions/      # Client interactions and follow-ups
├── sales/             # Sales opportunities and pipeline
├── reports/           # Dashboard and business reports
├── core/              # Homepage and core application views
│
├── config/            # Django project configuration
├── templates/         # Global templates
├── static/            # CSS and static assets
├── screenshots/       # Project screenshots
│
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

Each Django application is responsible for a specific part of the CRM system. This keeps the project modular, maintainable, and easier to test.

---

## Installation and Local Setup

Follow the steps below to run ClientTrack locally.

### 1. Clone the Repository

```bash
git clone https://github.com/taner-sahin/ClientTrack.git
cd ClientTrack
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

On Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on the provided `.env.example` file.

Sensitive configuration such as the Django secret key and production database credentials must not be committed to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will then be available through Django's local development server.

---

## Environment Variables

ClientTrack uses environment variables to separate sensitive configuration from source code.

The repository includes:

```text
.env.example
```

Create a local `.env` file based on this example and provide the required configuration values.

Production configuration includes environment-specific values such as:

- Django secret key
- Debug configuration
- Allowed hosts
- Database connection configuration

The real `.env` file remains private and is excluded from version control.

---

## Screenshots

The screenshots below demonstrate the main features and workflows of ClientTrack.

### Home Page

![ClientTrack Home Page](screenshots/home.png)

### Dashboard and Reports

User-specific CRM statistics including clients, interactions, sales opportunities, pipeline value, and deal status summaries.

![ClientTrack Dashboard and Reports](screenshots/dashboard.png)

### Client Management

Create and manage client records with user-specific ownership protection.

![ClientTrack Client Management](screenshots/clients.png)

### Interaction Tracking

Track client interactions, communication activities, and follow-up information.

![ClientTrack Interaction Tracking](screenshots/interactions.png)

### Sales Pipeline

Manage sales opportunities, pipeline stages, deal values, and estimated closing dates.

![ClientTrack Sales Pipeline](screenshots/sales.png)

### Smart Follow-up Reminders

Monitor upcoming, overdue, and completed follow-up activities.

![ClientTrack Smart Follow-up Reminders](screenshots/reminders.png)

### Team Management

Manage team members, roles, contact information, and active status.

![ClientTrack Team Management](screenshots/team.png)

### Secure Data Isolation

ClientTrack applies backend ownership controls so authenticated users can access only their own records.

![ClientTrack Secure Data Isolation](screenshots/security.png)

---

## Security Design

Security and user isolation are core architectural requirements of ClientTrack rather than optional frontend features.

Important security principles include:

- Authentication-protected application pages
- Backend ownership filtering
- User-specific querysets
- Ownership checks for detail operations
- Ownership checks for update operations
- Ownership checks for delete operations
- POST for state-changing operations
- CSRF protection
- Secure session cookies in production
- Secure CSRF cookies in production
- HTTPS redirection
- Trusted CSRF origins
- User-specific dashboard statistics
- User-specific reports
- Automated security tests
- HSTS

The frontend is never trusted to enforce ownership.

Security rules are applied directly in Django views and querysets.

---

## Production Deployment

ClientTrack is deployed to a production VPS and is publicly accessible over HTTPS.

### Live Application

**Production URL:** https://clienttrack.tanersahindev.com

### Production Architecture

```text
User / Browser
      │
      ▼
Internet
      │
      ▼
Domain / DNS
      │
      ▼
HTTPS / SSL/TLS
      │
      ▼
Nginx
      │
      ▼
Gunicorn
      │
      ▼
Django
      │
      ▼
PostgreSQL
```

### VPS and Ubuntu Linux

The application runs on a VPS using Ubuntu Linux.

The VPS provides the always-running production environment where the Django application, web server, application server, and production database operate.

### PostgreSQL

PostgreSQL is used as the production database.

SQLite remains available for local development, while production data is stored in PostgreSQL.

Database credentials and connection configuration are provided through environment variables rather than being hard-coded into the repository.

### Gunicorn

Gunicorn runs the Django WSGI application in production.

Instead of exposing Django's development server to the internet, Gunicorn provides the production application server layer.

Gunicorn communicates with Nginx through a Unix socket.

### systemd

Gunicorn is managed through a systemd service.

This allows ClientTrack to run independently of an SSH terminal session and provides service management commands for starting, stopping, restarting, and checking the application.

Example:

```bash
sudo systemctl status clienttrack
```

### Nginx

Nginx acts as the public-facing web server and reverse proxy.

Incoming web requests reach Nginx first. Nginx then forwards application requests to Gunicorn.

The request flow is:

```text
Browser
   ↓
Nginx
   ↓
Gunicorn
   ↓
Django
```

### Domain and DNS

The ClientTrack production application uses the following subdomain:

```text
clienttrack.tanersahindev.com
```

DNS connects the domain name to the production VPS.

This allows users to access the application using a human-readable domain instead of the server IP address.

### SSL/TLS and HTTPS

The production application is served over HTTPS.

SSL/TLS encrypts communication between the user's browser and the production server.

This protects sensitive information such as authentication sessions and form submissions while data travels across the network.

### HSTS

HTTP Strict Transport Security is enabled.

HSTS instructs compatible browsers to use HTTPS when communicating with the application for the configured HSTS duration.

The deployment currently uses a controlled HSTS configuration rather than enabling preload and all-subdomain enforcement.

### Django Production Security

Production Django security configuration includes:

- `DEBUG=False`
- Production `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `SECURE_PROXY_SSL_HEADER`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- HSTS configuration

These settings help ensure Django correctly operates behind the Nginx HTTPS reverse proxy.

### Production Request Flow

The complete production request flow can be summarized as:

```text
Browser
   ↓
DNS resolves clienttrack.tanersahindev.com
   ↓
HTTPS request reaches the VPS
   ↓
Nginx receives the request
   ↓
Nginx forwards the request to the Gunicorn Unix socket
   ↓
Gunicorn runs the Django WSGI application
   ↓
Django processes application logic
   ↓
Django ORM communicates with PostgreSQL
   ↓
Response travels back through Gunicorn and Nginx
   ↓
Browser receives the HTTPS response
```

This architecture separates the responsibilities of the web server, application server, Django application, and database.

---

## Production Verification

The production deployment has been verified through the running application and server-side checks.

Verification includes:

- Gunicorn systemd service running successfully
- Gunicorn workers running
- Gunicorn listening through the ClientTrack Unix socket
- Nginx serving the public application
- HTTPS responding successfully
- PostgreSQL used as the production database
- Django deployment security checks reviewed
- Secure session cookies enabled
- Secure CSRF cookies enabled
- HSTS enabled

The production application responds successfully over HTTPS.

---

## Future Improvements

Possible future improvements include:

- REST API development
- Django REST Framework integration
- API authentication
- Docker containerization
- Redis
- Celery background tasks
- Email notifications
- Additional CRM analytics
- CI/CD
- Additional deployment automation

---

## Project Status

Current ClientTrack status:

- Core backend development: Complete
- Authentication: Complete
- Client Management: Complete
- Interaction Management: Complete
- Sales Pipeline: Complete
- Reports and Dashboard: Complete
- Smart Follow-up Reminders: Complete
- Team Management: Complete
- Secure Data Isolation: Complete
- Automated Tests: 61 tests passing
- Security Audit: Complete
- Professional README: Complete
- Project Screenshots: Complete
- PostgreSQL Production Database: Complete
- Gunicorn: Complete
- systemd Service: Complete
- Nginx: Complete
- Domain/DNS: Complete
- SSL/TLS and HTTPS: Complete
- HSTS: Enabled
- Production Deployment: Complete

---

## What This Project Demonstrates

ClientTrack demonstrates practical Django backend development beyond basic CRUD functionality.

The project includes:

- Multi-user backend architecture
- Authentication and authorization
- Ownership-based access control
- User data isolation
- Django ORM usage
- Relational data management
- Secure CRUD operations
- Automated testing
- Security-focused backend design
- PostgreSQL production database configuration
- Linux VPS deployment
- Gunicorn application serving
- Nginx reverse proxy configuration
- Domain and DNS configuration
- SSL/TLS and HTTPS
- HSTS
- Production service management with systemd

The goal of the project is to demonstrate the complete path from Django backend development to a securely deployed production application.

---

## About

ClientTrack is a backend-focused Django mini CRM project built to demonstrate secure multi-user data handling, CRM workflows, automated testing, and production-oriented Django development.

The project was developed as a practical backend portfolio project with emphasis on understanding how Django applications work from database and security design through production deployment.