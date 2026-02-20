# Cinema Rate (Django + PostgreSQL)

A movie and actor voting website built with Django, HTML, CSS, and JavaScript.

## Features
- English-only user-facing text.
- Registration with email + unique username + password.
- Login via unique username/password OR email/password.
- Home page highlights **Best Movie** and **Best Actor** at the top.
- Ranking sections show rank 2 to 20 by default.
- "Show all movies" button to list all ranked movies.
- Country filters for both movies and actors (10 countries seeded by migration).
- Header includes current Gregorian date and user profile area on the left.

## Tech stack
- Django
- PostgreSQL (default database)
- HTML/CSS/JavaScript

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy env file:
   ```bash
   cp .env.example .env
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

## Git-related notes
- `.env` is ignored by git.
- `requirements.txt` is tracked and lists package dependencies.
- See `.gitignore` for all excluded files and folders.