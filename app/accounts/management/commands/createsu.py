from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Создаёт суперпользователя из переменных окружения, если его ещё нет"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write("Переменные DJANGO_SUPERUSER_USERNAME и DJANGO_SUPERUSER_PASSWORD не заданы. Пропускаем создание суперпользователя.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{username}' уже существует."))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{username}' успешно создан."))