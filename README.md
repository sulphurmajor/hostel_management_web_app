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

## Vercel environment variables

Set these in the Vercel project's environment-variable settings:

- `DJANGO_SECRET_KEY`: a long, random secret value; keep it private.
- `DJANGO_ALLOWED_HOSTS`: comma-separated Vercel hostnames, without `https://`.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: full origins such as `https://your-site.vercel.app`.

Vercel automatically provides `VERCEL_URL` and
`VERCEL_PROJECT_PRODUCTION_URL`, which are also allowed by the Django settings.
Production mode disables debug output and enables secure cookies and HTTPS
redirects. Vercel collects the files from `static/` into `staticfiles/` during
the build and serves them from its CDN.

**Database note:** this project currently uses SQLite for learning and local
development. Vercel serverless deployments do not provide durable local
database storage, so records and logins created there may not persist. Use a
managed database if the deployed demonstration needs to retain data.
