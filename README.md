# Prodigy Progress Tracker API

This project provides a REST API for tracking user progress in a 5-minute daily activity program.

## 🚀 Steps to Run the Project

### 1. Clone the Repository

```sh
git clone git@github.com:shivapittala19/activityTracker.git
cd activityTracker
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add:

```ini
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
```

### 5. Apply Migrations

```sh
python manage.py migrate
```

### 6. Create a Superuser (for Admin Panel)

```sh
python manage.py createsuperuser
```

### 7. Run the Development Server

```sh
python manage.py runserver
```

Now, visit `http://127.0.0.1:8000/swagger/` to explore the API documentation.

---

## 📌 API Endpoints

### 1. **User Progress** (Get activities for a given date range)

- **Endpoint:** `GET /api/user_progress/`
- **Params:** `start_date`, `end_date`
- **Response:**

```json
[
  {
    "id": 103,
    "date": "2025-02-20",
    "activity": {
      "id": 2,
      "name": "Running",
      "frequency": "1 x/ Day",
      "duration": 30
    },
    "is_completed": false
  },
]
```

### 2. **Mark Activity as Complete**

- **Endpoint:** `POST /api/mark_complete/{id}/`
- **Response:**

```json

Response body
{
  "message": "Activity updated",
  "is_completed": true
}
```

---

## 🛠 Technologies Used

- **Django** & **Django REST Framework** (API backend)
- **PostgreSQL** (Database)
- **drf-yasg** (Swagger API documentation)

### 📝 Notes

- Use `admin/` for managing programs and activities via the Django admin panel.

---

🚀
