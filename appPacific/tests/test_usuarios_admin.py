from django.test import TestCase
from django.contrib.auth.models import User
import pytest



@pytest.mark.django_db
class CRUDTests(TestCase):
    def setUp(self):
        User.objects.create(first_name='Usuario1', last_name='Usuario1', username='Usuario1',email='usuario1@usuario1', password='Usuario1',is_superuser=0, is_staff=0)
        User.objects.create(first_name='Usuario2', last_name='Usuario2', username='Usuario2',email='usuario2@usuario2', password='Usuario2',is_superuser=1, is_staff=0)

    def test_create_usuario(self):
        User.objects.create(first_name='Nuevousuario', last_name='Nuevousuario', username='Nuevousuario',email='nuevousuario@nuevousuario', password='Nuevousuario',is_superuser=1, is_staff=0)
        self.assertEqual(User.objects.count(), 3)

    def test_read_usuario(self):
        usuario_1 = User.objects.get(first_name='Usuario1')
        usuario_2 = User.objects.get(first_name='Usuario2')
        self.assertEqual(usuario_1.email, 'usuario1@usuario1')
        self.assertEqual(usuario_2.is_superuser, 1)

    def test_update_usuario(self):
        usuario = User.objects.get(first_name='Usuario1')
        usuario.email = 'nuevousuariousuario1@nuevousuario1'
        usuario.save()
        self.assertEqual(User.objects.get(first_name='Usuario1').email, 'nuevousuariousuario1@nuevousuario1')
        
    def test_delete_usuario(self):
        usuario = User.objects.get(first_name='Usuario1')
        usuario.delete()
        self.assertEqual(User.objects.count(), 1)