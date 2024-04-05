# Generated by Django 4.2 on 2024-04-05 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPacific', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id reserva')),
                ('nombre_cli', models.CharField(max_length=30, verbose_name='Nombre cliente')),
                ('apellidos_cli', models.CharField(max_length=30, verbose_name='Apellidos cliente')),
                ('rut_cli', models.CharField(max_length=25, verbose_name='Rut cliente')),
                ('correo_cli', models.CharField(max_length=40, verbose_name='Correo cliente')),
                ('celular_cli', models.CharField(max_length=40, verbose_name='Celular cliente')),
                ('metodo_pago', models.CharField(max_length=20, verbose_name='Metodo Pago cliente')),
                ('pago_reserva', models.CharField(max_length=20, verbose_name='Pago Reserva')),
                ('total_restante', models.CharField(max_length=20, verbose_name='Total Restante')),
                ('estado_pago', models.CharField(max_length=20, verbose_name='Estado Pago')),
            ],
        ),
        migrations.AddField(
            model_name='registrousuario',
            name='rol',
            field=models.CharField(default='Cliente', max_length=20, verbose_name='Rol del usuario'),
        ),
    ]