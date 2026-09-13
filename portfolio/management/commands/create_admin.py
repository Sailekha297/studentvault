from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or reset the StudentVault admin user"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "admin"
        email = "admin@studentvault.com"
        password = "Admin@12345"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            }
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Admin account ready: admin / Admin@12345"
            )
        )