🛒 StoreFront - E-Commerce Web Application

Overview

StoreFront is a full-stack e-commerce web application built using Flask and SQLAlchemy. The project was developed to simulate the core functionality of a modern online shopping platform while following modular backend development practices.

The application provides user authentication, product management, shopping cart functionality, order management, administrative controls, and REST API endpoints. The project is structured using Flask Blueprints to maintain separation of concerns and improve scalability.

---

Key Features

User Features

- User Registration and Login
- Secure Password Reset Workflow
- Product Browsing and Search
- Product Detail Pages
- Shopping Cart Management
- Order Placement
- Contact and Feedback System

Administrative Features

- Dedicated Admin Dashboard
- Product CRUD Operations
- Order Monitoring and Management
- Customer Message Management
- Restricted Access for Administrative Actions

Backend Features

- Flask Blueprint Architecture
- SQLAlchemy ORM Integration
- Database Migrations using Flask-Migrate
- REST API Endpoints
- Session-Based Authentication
- Form Validation with Flask-WTF

---

Project Architecture

StoreFront
│
├── app
│   ├── admin
│   ├── auth
│   ├── api
│   ├── orders
│   ├── static
│   ├── templates
│   ├── models.py
│   ├── forms.py
│   ├── cart.py
│   └── __init__.py
│
├── migrations
├── config.py
├── run.py
└── requirements.txt

The project follows a modular architecture where each module is responsible for a specific business domain, improving maintainability and future scalability.

---

Technology Stack

Backend

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Migrate

Database

- SQLite
- Oracle SQL / PL-SQL (Academic & Practice Experience)

Frontend

- HTML5
- CSS3
- Jinja2 Templates

Development Tools

- Git
- GitHub
- VS Code

---

REST API

The application includes REST API endpoints that expose application resources and support integration with external clients.

Example capabilities include:

- Product Retrieval
- Product Details
- Order Information
- Administrative Operations

---

Security Considerations

- User Authentication System
- Role-Based Administrative Access
- Form Validation
- Protected Administrative Routes
- Password Reset Functionality

---

Future Improvements

- JWT Authentication
- OAuth2 / Google Login
- PostgreSQL Migration
- Docker Containerization
- Redis Caching
- CI/CD Pipeline
- Nginx Deployment
- AI-Powered Product Recommendations
- RAG-Based Product Assistant

---

Learning Outcomes

Through this project I gained practical experience in:

- Backend Web Development with Flask
- Database Design and ORM Usage
- Authentication and Authorization
- REST API Development
- Application Architecture
- CRUD Operations
- Database Migrations
- Git and Version Control

---

Installation

Clone the repository:

git clone <repository-url>
cd StoreFront

Create a virtual environment:

python -m venv venv

Activate the environment:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python run.py

Open your browser and visit:

http://127.0.0.1:5000

---

Author

Ahmed Raza

Aspiring Backend Developer focused on Python, Flask, SQL, Database Systems, and Backend Application Development.

Always learning, building, and improving.
