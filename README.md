# **User Authentication and Wallet API Documentation**

## **Overview**
This project provides a user authentication and wallet management API built with Django Rest Framework (DRF). It includes user registration, login, profile management, and wallet functionalities.

---

## **Table of Contents**
- [Overview](#overview)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [User Registration](#user-registration)
- [User Login](#user-login)
- [User Profile](#user-profile)
- [Wallet Management](#wallet-management)
- [Permissions](#permissions)
- [Contributing](#contributing)
- [Contact](#contact)

---

## **Installation**

### **Prerequisites**
- Python 3.11.6
- Django 5.1.3
- Django Rest Framework
- Git

### **Admin Credentials**

- Phone: 01706711482
- Password: 1234

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/username/project-name.git
   cd project-name


2. Create and activate a virtual environment:
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Apply migrations:
    python manage.py migrate

5. Run the development server:
    python manage.py runserver


API Endpoints
1. User Registration
    Endpoint:
        POST /api/auth/register/

    Request Body:
        {
            "phone": "0123456789",
            "password": "YourPassword123",
            "password2": "YourPassword123"
        }

2. User Login
    Endpoint:
        POST /api/auth/login/

    Request Body:

        {
            "phone": "0123456789",
            "password": "YourPassword123"
        }

3. User Profile
    Endpoint:
    GET /api/profile/

    Request Parameters:
    id - User ID

    Authorization (Bearer Token):
    Token <token>

    Example Request:
    GET /api/profile/?id=1

4. User Profile Update
    Endpoint:
    PATCH /api/profile/

    Request Parameters:
    id - User ID

    Authorization (Bearer Token):
    Token <token>

    Example Request:
    GET /api/profile/?id=1


5. Wallet Management
    1. Check Wallet Balance
        Endpoint:
        GET /api/wallet/?id=1

        Request Parameters:
        id - User ID

        Authorization (Bearer Token):
        Token <token>

    2. Add Funds
        Endpoint:
        POST /api/wallet/?id=1

        Request Parameters:
        id - User ID

        Authorization (Bearer Token):
        Token <token>

        Request Body:
        {
        "amount": 500
        }

    3. Spend Funds
        Endpoint:
        PATCH /api/wallet/?id=1

        Request Parameters:
        id - User ID

        Authorization (Bearer Token):
        Token <token>

        Request Body:
        {
        "amount": 300
        }

6. Permissions
Profile and Wallet: Only authenticated users can access or modify their own profile and wallet.

7. Contact
For any issues or questions, please contact:

Email: swesadiqul@gmail.com
Mobile: +8801613525410