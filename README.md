<p align="center">
  <h3 align="center">E‑Commerce API (Flask & PostgreSQL)</h3>
</p>

![Badges](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) 
![Badges](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Badges](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

### Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Overview](#api-overview)

### About the Project

This repository contains a backend‑focused e‑commerce API built with Flask and PostgreSQL.  
The goal of the project is to model a realistic online marketplace where users can register, manage stores and products, and place orders in a secure and scalable way.

The codebase is structured around clear layers:
- `create_app` handles application factory, configuration and extensions (Redis cache, rate limiting).
- `routes` exposes HTTP endpoints for authentication, products, orders and stores.
- `controllers` contains request/response orchestration and business rules.
- `db` contains data‑access logic for PostgreSQL.
- `schemas` defines request/response validation using JSON schemas.

This project was originally developed as a learning project and has been refreshed to match current best practices and to demonstrate backend engineering skills on a modern Python stack.

### Features

- **User Management & Authentication**: Registration, login and JWT‑based authentication.
- **Store & Product Management**: CRUD operations for stores and products, including active/inactive flags.
- **Order Workflow**: Create and manage orders between buyers and sellers.
- **Input Validation**: JSON schema validation for request payloads.
- **Caching & Rate Limiting**: Redis‑backed caching and Flask‑Limiter integration for basic protection against abuse.
- **Configurable Environment**: Uses environment variables (e.g. database URL, secret keys) via `python-dotenv`.

### Tech Stack

- **Language**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **Caching / Rate Limiting**: Redis, Flask‑Caching, Flask‑Limiter
- **Other**: JWT (PyJWT), JSON Schema, Docker‑ready configuration (via env vars)

### Getting Started

#### Prerequisites

- Python 3.10+ (recommended)
- PostgreSQL instance
- Redis instance (for caching and rate limiting)
- `virtualenv` or similar tool for managing Python environments

#### Installation

```bash
git clone https://github.com/bcalagoz/E-Commerce-Api-using-Flask.git
cd E-Commerce-Api-using-Flask
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root with at least:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
```

Run the application:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

### API Overview

The following high‑level endpoint groups are available (see the code for full details):

- **Auth**: `POST /auth/register`, `POST /auth/login`
- **Products**: `GET /products`, `POST /products`, `GET /products/<id>`, `PUT /products/<id>`, `DELETE /products/<id>`
- **Stores**: `GET /stores`, `POST /stores`, `GET /stores/<id>`, etc.
- **Orders**: `POST /orders`, `GET /orders`, `GET /orders/<id>`, etc.

All non‑public endpoints expect a valid JWT access token.
