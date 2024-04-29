from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_test_user(sender, **kwargs):
    if not User.objects.filter(username='usuario').exists():
        User.objects.create_user(username='usuario', password='contraseña')
