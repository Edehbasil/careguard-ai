# CareGuard

A backend API for healthcare compliance and data governance, built with FastAPI, SQLAlchemy, and SQLite.

CareGuard was developed to demonstrate the intersection of software engineering and legal compliance in a healthcare context — specifically around UK GDPR, the Data Protection Act 2018, and NHS information governance standards.

---

## Why CareGuard?

Healthcare organisations handle some of the most sensitive personal data in existence. The legal framework governing that data — UK GDPR, DPA 2018, the Caldicott Principles, and the NHS Data Security and Protection Toolkit — places strict obligations on how data is requested, stored, shared, and protected.

CareGuard is built around those obligations. It is not a generic CRUD application — it is a domain-specific compliance tool designed with real healthcare workflows in mind.

---

## Features

### Authentication & Authorisation
- Secure user registration and login
- JWT-based authentication with token expiry
- Role-based access control (admin vs standard user)
- Protected routes requiring valid authentication

### Subject Access Request (SAR) Tracker
- Submit SARs referencing UK GDPR Article 15 (right of access)
- Automatic 30-day response deadline enforcement (as required by UK GDPR)
- Real-time days remaining calculation
- Status workflow: pending → in_progress → completed → closed
- Automatic resolution timestamp on completion
- Admin-only status updates; users can only view their own SARs

### Audit Log
- Automatic logging of all significant actions (SAR submissions, status updates)
- Records user, action type, affected resource, and timestamp
- Admin endpoint to view full system audit trail
- User endpoint to view personal activity log
- Supports accountability principle under UK GDPR Article 5(2)

### Data Breach Notification Tracker
- Report data breaches with severity classification
- Automatic 72-hour ICO notification deadline (UK GDPR Article 33)
- Real-time hours remaining countdown
- ICO notification and resolution status tracking
- Admin-only breach listing; reporters can view their own breaches
- All actions automatically logged to audit trail

### Health Check-Ins
- Employee health check submission with temperature validation
- Retrieval of individual and all check-in records

---

## Tech Stack

- **FastAPI** — modern, high-performance Python web framework
- **SQLAlchemy** — ORM for database modelling and queries
- **Alembic** — database migration management
- **SQLite** — lightweight relational database
- **JWT (python-jose)** — stateless authentication
- **Passlib / bcrypt** — secure password hashing
- **Pydantic v2** — data validation and serialisation

---

## Legal & Compliance Context

| Feature | Legal Basis |
|---|---|
| SAR 30-day deadline | UK GDPR Article 12(3) |
| Right of access | UK GDPR Article 15 |
| Password hashing | DPA 2018 security obligations |
| Role-based access | Data minimisation principle (UK GDPR Article 5) |
| Audit timestamps | Accountability principle (UK GDPR Article 5(2)) |

---

## Project Structure
careguard-ai/
├── app/
│   ├── main.py
│   ├── routers/          # API route handlers
│   ├── models/           # SQLAlchemy database models
│   ├── schemas/          # Pydantic request/response schemas
│   ├── db/               # Database setup, session, migrations
│   └── utils/            # Security utilities (hashing, JWT)
├── alembic/              # Database migration files
└── requirements.txt


---

## Running Locally

```bash
# Clone the repository
git clone https://github.com/Edehbasil/careguard-ai.git
cd careguard-ai

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

---

## Background

This project was built by a developer with an MSc in Computing and an undergraduate background in Law, with additional training in Health and Social Care. CareGuard reflects a deliberate effort to apply technical skills to a domain where software engineering, legal compliance, and patient safety intersect.