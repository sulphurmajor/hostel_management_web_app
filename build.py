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
    reset_password_once = os.environ.get("DJANGO_RESET_ADMIN_PASSWORD_ONCE")
    if reset_password_once and reset_password_once != "1":
        raise RuntimeError("DJANGO_RESET_ADMIN_PASSWORD_ONCE must be set to '1' or omitted.")
    if bool(username) != bool(password):
        raise RuntimeError(
            "Set both DJANGO_BOOTSTRAP_ADMIN_USERNAME and "
            "DJANGO_BOOTSTRAP_ADMIN_PASSWORD, or neither."
        )
    if not username:
        if reset_password_once:
            raise RuntimeError(
                "A one-time administrator password reset requires both bootstrap variables."
            )
        return
    if len(password) < 16 and not reset_password_once:
        raise RuntimeError("The bootstrap administrator password must be at least 16 characters.")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostelman.settings")
    import django

    django.setup()

    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    user = user_model.objects.filter(username=username).first()
    if reset_password_once:
        if user is None:
            raise RuntimeError(
                "Cannot reset the administrator password because the configured user does not exist."
            )
        user.set_password(password)
        user.save(update_fields=["password"])
        print(f"Reset password for administrator {username!r}.")
    elif user is None:
        user_model.objects.create_superuser(
            username=username,
            email=os.environ.get("DJANGO_BOOTSTRAP_ADMIN_EMAIL", ""),
            password=password,
        )


if __name__ == "__main__":
    main()
