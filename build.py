import os
import subprocess
import sys


def main():
    if os.environ.get("VERCEL_ENV") != "production":
        return
    if not os.environ.get("DATABASE_URL"):
        raise RuntimeError("Set DATABASE_URL for the Vercel Production environment.")

    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        check=True,
    )

    username = os.environ.get("DJANGO_BOOTSTRAP_ADMIN_USERNAME")
    password = os.environ.get("DJANGO_BOOTSTRAP_ADMIN_PASSWORD")
    if bool(username) != bool(password):
        raise RuntimeError(
            "Set both DJANGO_BOOTSTRAP_ADMIN_USERNAME and "
            "DJANGO_BOOTSTRAP_ADMIN_PASSWORD, or neither."
        )
    if not username:
        return
    if len(password) < 16:
        raise RuntimeError("The bootstrap administrator password must be at least 16 characters.")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostelman.settings")
    import django

    django.setup()

    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    if not user_model.objects.filter(username=username).exists():
        user_model.objects.create_superuser(
            username=username,
            email=os.environ.get("DJANGO_BOOTSTRAP_ADMIN_EMAIL", ""),
            password=password,
        )


if __name__ == "__main__":
    main()
