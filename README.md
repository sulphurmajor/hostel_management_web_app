# Hostel Management web app

A Django-based hostel management application for managing students, hostels, wardens, rooms, payments, and visitor records.

## Group members

- 224-063061-29769 — Ssemwogerere Rahim
- 224-063061-29531 — Muwanguzi Brian
- 224-063061-28452 — Namuyomba Jamirah

## Local setup

Install dependencies and run the local development server:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The local SQLite database is intentionally excluded from Git. Create your own
administrator account in each environment; do not publish the database or use
a shared default password.

## Deploy to Render

The repository includes a Render Blueprint (`render.yaml`) that creates a
Django web service and a PostgreSQL database. In Render, choose **New**
> **Blueprint** and connect this repository. Render reads the build and start
commands, links `DATABASE_URL` to the database, and generates
`DJANGO_SECRET_KEY`.

The build installs dependencies and collects static files. On each service
start, database migrations run before Gunicorn starts. WhiteNoise serves the
collected static files. SQLite remains available for local development; the
Render deployment requires PostgreSQL because service filesystems are
ephemeral.

After the first successful deploy, set `DJANGO_ADMIN_PASSWORD` in the web
service's Render environment settings and deploy. The build creates the first
superuser as `admin` only when that variable is present. You can optionally set
`DJANGO_ADMIN_EMAIL`. Remove `DJANGO_ADMIN_PASSWORD` after the first successful
admin setup; future builds leave the existing password unchanged. Sign in at
`/login/` or `/admin/`. Once signed in, use **Change password** in the top bar
or visit `/password/change/`.

Keep deployment secrets private. `DEBUG` is disabled in production, and the
Render hostname is added to Django's allowed hosts and CSRF trusted origins.
