# SwiftServe

A scalable **Restaurant Management & Food Delivery Backend** built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. SwiftServe provides a production-style backend architecture with secure authentication, restaurant management, inventory tracking, order processing, and payment management.

---

##  Features

###  Authentication & Authorization
- JWT-based Authentication
- Secure User Registration & Login
- Role-Based Access Control (Customer & Restaurant Owner)

###  Restaurant Management
- Create and Manage Restaurants
- Restaurant Profile Management
- Restaurant Availability

###  Category Management
- Create Menu Categories
- Update & Delete Categories
- Restaurant-wise Category Management

###  Menu Management
- Add Menu Items
- Update Menu Items
- Manage Pricing
- Availability Status

###  Inventory Management
- Add Inventory Items
- Track Stock Quantity
- Minimum Stock Alerts
- Ingredient Management

###  Recipe Management
- Link Ingredients to Menu Items
- Automatic Ingredient Consumption Logic
- Recipe Quantity Management

###  Order Management
- Place Orders
- Multiple Order Items
- Order Status Tracking
- Customer Order History
- Restaurant Order Dashboard

###  Payment Module
- Payment Creation
- Payment Status Updates
- Payment History
- Transaction Management

---

##  Tech Stack

### Backend
- FastAPI
- Python 3.x

### Database
- PostgreSQL
- SQLAlchemy ORM

### Authentication
- JWT Tokens
- OAuth2 Password Bearer

### Validation
- Pydantic

### API Testing
- Swagger UI
- OpenAPI

### Tools
- Git
- GitHub

---

#  Project Structure

```
SwiftServe
│
├── app
│   ├── models
│   ├── schemas
│   ├── repositories
│   ├── services
│   ├── routers
│   ├── dependencies
│   ├── utils
│   └── main.py
│
├── docs
├── diagrams
├── requirements.txt
├── README.md
└── .gitignore
```

---

#  Architecture

SwiftServe follows a layered architecture:

```
Client
   │
   ▼
Router
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
PostgreSQL Database
```

This architecture keeps business logic separate from database operations, making the application scalable and maintainable.

---

#  Database Modules

- Users
- Restaurants
- Categories
- Menu Items
- Inventory Items
- Recipes
- Orders
- Order Items
- Payments

---

#  API Modules

| Module | Status |
|---------|--------|
| Authentication | ✅ |
| Restaurants | ✅ |
| Categories | ✅ |
| Menu | ✅ |
| Inventory | ✅ |
| Recipes | ✅ |
| Orders | ✅ |
| Payments | ✅ |
| Delivery | 🚧 |
| Notifications | 🚧 |
| Dynamic Pricing | 🚧 |

---

# ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/SwiftServe.git
```

Move into the project directory:

```bash
cd SwiftServe
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables by creating a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Run the application:

```bash
uvicorn app.main:app --reload
```

---

#  API Documentation

After running the server:

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

#  Future Enhancements

-  Delivery Management
-  Real-Time Notifications
-  Smart Dynamic Pricing Engine
-  AI-Based Demand Prediction
-  Restaurant Analytics Dashboard
-  Docker Deployment
-  CI/CD Pipeline

---

#  Learning Outcomes

This project demonstrates:

- Backend API Development
- RESTful API Design
- Layered Architecture
- JWT Authentication
- Database Design
- SQLAlchemy ORM
- Business Logic Implementation
- Inventory & Order Workflow
- Payment Processing
- Clean Project Structure

---

#  Author

**Ritagya Singh**

Backend Developer | Python | FastAPI | PostgreSQL | REST APIs

GitHub: https://github.com/ritagya-singh

LinkedIn: https://www.linkedin.com/in/ritagya-singh-8513a624a/

---

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on GitHub.

## Live API

Live Backend: https://swiftserve-74nx.onrender.com

Swagger API Docs: https://swiftserve-74nx.onrender.com/docs