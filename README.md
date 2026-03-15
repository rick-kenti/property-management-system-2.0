# PropertyHub — Property Management System

A full-stack property management web application built with **Flask** (backend API)
and **React** (frontend SPA). Manage properties, tenants, and rent payments
with a clean, responsive dashboard.

---

## Tech Stack

| Layer     | Technology                                       |
|-----------|--------------------------------------------------|
| Backend   | Python, Flask, Flask-SQLAlchemy, Flask-Migrate   |
| Auth      | Flask-JWT-Extended, Flask-Bcrypt                 |
| Database  | SQLite (dev) / PostgreSQL (prod)                 |
| Frontend  | React 18, React Router v6, Vite                  |
| Forms     | Formik + Yup validation                          |
| Styling   | Custom CSS (dark theme)                          |

---

## Models & Relationships

- User ──< Property       (One-to-Many: User has many Properties)
- Property ──< RentPayment (One-to-Many: Property has many Payments)
- Tenant ──< RentPayment   (One-to-Many: Tenant has many Payments)
- Property >──< Tenant     (Many-to-Many via RentPayment association table)


### RentPayment Association Table (user-submittable attributes)
- `amount_paid` (Float)
- `payment_date` (Date)
- `due_date` (Date)
- `status` (paid / pending / overdue / partial)
- `payment_method` (cash / mpesa / bank_transfer / cheque)
- `notes` (Text)

---

## Features

- **User Authentication** — JWT-based secure login and registration
- **Property Management** — Full CRUD (Create, Read, Update, Delete)
- **Tenant Management** — Full CRUD with phone and email validation
- **Rent Tracking** — Record and monitor payments with status tracking
- **Reports Dashboard** — Live stats: revenue, paid/pending/overdue counts
- **Formik Forms** — All inputs validated with Yup schemas
- **Protected Routes** — All pages require authentication
- **Responsive Design** — Mobile-friendly layout

---

## Project Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- pip and npm

---

### Backend Setup

```bash
# 1. Navigate to the server directory
cd server

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database
flask db init
flask db migrate -m "initial migration"
flask db upgrade

# 5. Seed the database with sample data
python seed.py

# 6. Start the Flask server
python app.py

The Flask API will run at: http://localhost:5555Default seed credentials:
Email: admin@propertyhub.com
Password: Admin@1234

---

### Frontend Setup

---
# 1. Navigate to the client directory
cd client

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev

### Folder structure

property-management/
├── server/
│   ├── app.py          # Flask routes and API
│   ├── models.py       # SQLAlchemy models
│   ├── config.py       # App configuration
│   ├── seed.py         # Database seeder
│   └── requirements.txt
└── client/
    ├── src/
    │   ├── context/    # Auth context (JWT state)
    │   ├── components/ # Navbar, StatCard, ProtectedRoute
    │   ├── pages/      # Login, Dashboard, Properties, Tenants, RentPayments
    │   ├── App.jsx     # Routes configuration
    │   └── index.css   # Global styles
    ├── public/
    └── package.json
