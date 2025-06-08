# 💸 Personal Budget Tracker

A simple web application to help users manage their personal finances by tracking income and expenses. Built with **Django**, **Tailwind CSS**, and **Chart.js**, it supports user authentication, categorization, and interactive financial summaries.

---

## 🚀 Features

### 🔐 User Authentication
- Sign up, log in, and log out
- Each user manages their own private financial data
- Powered by Django's built-in authentication system

### 💰 Income & Expense Management
- Add, edit, or delete financial entries
- Entry fields: Title, Amount, Date, Type (income/expense), Notes
- Full CRUD functionality for user-specific entries

### 🗂 Expense Categorization
- Categorize expenses (e.g., Food, Travel, Bills, etc.)
- Uses a dropdown from Django model or static choices

### 📊 Dashboard & Visualizations
- View monthly summaries of income vs. expenses
- Pie chart showing expense distribution by category
- Bar graph comparing monthly income and expenses
- Remaining balance display (Income - Expenses)
- Dashboard includes quick links for adding/viewing entries

---

## 🛠 Tech Stack

- **Backend**: Django 5.1.6
- **Frontend Styling**: Tailwind CSS
- **Charts/Visualization**: Chart.js
- **Authentication**: Django's built-in user system
- **Database**: SQLite (for development)

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/budget-tracker.git
   cd budget-tracker

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # or `env\Scripts\activate` on Windows

3. **Install dependencies**
    ```bash
   pip install -r requirements.txt

4. **Configure Tailwind (if using django-tailwind)**
   ```bash
   python manage.py tailwind install
   python manage.py tailwind build

5. **Run migrations**
   ```bash
   python manage.py migrate

6. **Start the development server**
    ```bash
   python manage.py runserver

7. **Access the app**
   Go to http://127.0.0.1:8000/ in your browser.

---

## 👥 Contributors
- Janna Maureen A. Bantugan
- Angelinne C. Trocio
- Chraine Paul S. Tuazon

## Deployment on Railway

### Prerequisites
- A Railway account (https://railway.app/)
- A GitHub account with your code repository

### Environment Variables
The following environment variables need to be set in Railway:

```
SECRET_KEY=your-secure-secret-key
DEBUG=False
OPENAI_API_KEY=your-openai-key
```

Railway will automatically set the following PostgreSQL variables:
```
POSTGRES_DATABASE
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
```

### Deployment Steps
1. Go to https://railway.app/
2. Sign in with your GitHub account
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your PeraHub repository
6. Add a PostgreSQL database from the Railway dashboard
7. Set up the required environment variables
8. Railway will automatically deploy your application

### Local Development Setup
1. Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
POSTGRES_DATABASE=your_db_name
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
OPENAI_API_KEY=your-openai-key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

