import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import CommandError, ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create the first Render admin when a password is supplied privately."""

    help = "Create the initial admin account from DJANGO_ADMIN_PASSWORD, if supplied."

    def handle(self, *args, **options):
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")
        if not password:
            self.stdout.write("DJANGO_ADMIN_PASSWORD not set; initial admin setup skipped.")
            return

        User = get_user_model()
        username = "admin"
        existing = User.objects.filter(username=username).first()
        if existing:
            if existing.is_superuser:
                self.stdout.write("Initial admin already exists; leaving its password unchanged.")
                return
            raise CommandError("Username 'admin' already exists but is not a superuser.")

        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")
        try:
            validate_password(password, user=User(username=username, email=email))
        except ValidationError as exc:
            message = "; ".join(exc.messages)
            raise CommandError(f"DJANGO_ADMIN_PASSWORD does not meet Django's password rules: {message}") from exc

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS("Created the initial admin account."))
