# SkillHub

SkillHub is an online platform where students can book sessions with teachers, leave reviews, and manage learning activities efficiently.

## Features

1. **Teacher Profile Page**
   - Displays teacher information and allows students to book sessions.
   - Includes a booking form for selecting date, time, duration, and topic.

2. **Booking System**
   - Students can request sessions with teachers.
   - Teachers can accept or reject bookings directly from the notifications.

3. **Notifications**
   - Teachers and students are notified about booking statuses in real-time.

4. **Search Functionality**
   - Students can search for teachers by name or skill.

5. **Dashboard**
   - Teachers can view their total students, active courses, pending assignments, and upcoming classes.

## Technologies Used

- **Backend**: Django, Celery
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (or any preferred relational database)
- **Task Queue**: Redis (for Celery)
- **Email Notifications**: Django's Email backend

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MariamKhoKh/Skill-Hub.git
   cd SkillHub
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Start the Celery worker:
   ```bash
   celery -A skillhub worker --pool=solo
   ```

8. Start Redis server (ensure Redis is installed and running):
   ```bash
   redis-server
   ```

## Usage

1. Navigate to `http://127.0.0.1:8000` in your browser.
2. Log in as the superuser to access the admin panel or create teacher and student accounts.
3. Test the booking functionality by logging in as a student and booking a session with a teacher.

## Project Structure

- `skillhub/`: Main Django app.
- `templates/`: HTML templates.
- `static/js/`: JavaScript files (e.g., `notifications.js`).
- `components/`: Reusable HTML components (e.g., booking form, teacher info).
- `tasks.py`: Celery tasks for notifications and email sending.

## Endpoints

### 1. **Retrieve a Single Teacher Profile**

- **URL:** `/teaching/api/teachers/<id>/`
- **Method:** `GET`
- **Description:** Retrieves the details of a teacher profile by its ID.

### 2. **Search Teachers by Skill**

- **example URL request:** `/teaching/api/teachers/search/?skill=Python`
- **Method:** `GET`
- **Description:** Search for teachers who have a specific skill.


### 3. **Retrieve Teachers with High Ratings**

- **URL:** `/teaching/api/teachers/high-rated/`
- **Method:** `GET`
- **Description:** Retrieves a list of teachers filtered by a minimum rating.
- **Query Parameters:**
  - `min_rating` (optional): Minimum rating threshold (e.g., `4.5`).

## Caching
- To enhance performance, caching is implemented for the teacher's profile view using Django's cache_page decorator.
- duration - 15 mins

## Additional Notes

- Ensure Redis is installed and running for Celery tasks.
- Configure email settings in `settings.py` for email notifications.

## to-do

- caching
- apis
- filtering
- update db
- upload

---


