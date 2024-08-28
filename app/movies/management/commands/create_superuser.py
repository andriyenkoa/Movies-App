import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Create a superuser based on environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        if username and email and password:
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
        else:
            self.stdout.write(self.style.WARNING('Environment variables for superuser creation not set.'))
