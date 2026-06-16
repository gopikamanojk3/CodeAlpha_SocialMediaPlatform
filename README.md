# CodeAlpha - Social Media Platform (Task 2)

A mini social media application built with Django.

## Features
- User registration & login
- User profiles with bio and avatar
- Create, view, delete posts with image support
- Like/unlike posts
- Comment on posts
- Follow/unfollow users
- Personalized feed

## Tech Stack
- Backend: Python + Django
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Project Structure
```
social_media/
├── social_media_project/   # Django project config
├── users/                  # User auth & profiles
├── posts/                  # Posts, comments, likes
├── templates/              # HTML templates
├── static/                 # CSS/JS assets
└── manage.py
```
