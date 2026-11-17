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
development. For Vercel, configure `DATABASE_URL` with a managed PostgreSQL
connection string. The production build runs database migrations. To create
the initial administrator, set `DJANGO_BOOTSTRAP_ADMIN_USERNAME` and
`DJANGO_BOOTSTRAP_ADMIN_PASSWORD` in the Vercel Production environment; the
password must be at least 16 characters. The build creates this account only
if it does not already exist. Remove both variables after the first successful
deployment, and do not reuse default or shared credentials.

For a one-time password reset of an existing administrator, set
`DJANGO_RESET_ADMIN_PASSWORD_ONCE=1` together with the administrator username
and password variables in Production, then redeploy. This allows a shorter
password for that reset only. Remove all three variables immediately after a
successful deployment; otherwise future builds can reset the password again
or fail the bootstrap password-length check.
Because shared passwords expose administrator access, use this only for an
explicitly approved grading window and change it immediately afterward.
