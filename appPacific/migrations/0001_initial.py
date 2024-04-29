import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosBancarios',
            fields=[
                ('id_banco', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id Banco')),
                ('beneficiario', models.CharField(max_length=50, verbose_name='Beneficiario')),
                ('cuenta', models.CharField(max_length=50, verbose_name='Cuenta')),
                ('nro_cuenta', models.CharField(max_length=50, verbose_name='Número cuenta bancaria')),
                ('correo_banco', models.CharField(max_length=50, verbose_name='Correo Banco')),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id_hab', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id habitación')),
                ('titulo_hab', models.CharField(max_length=50, verbose_name='Titulo habitación')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('titulo_en', models.CharField(max_length=50, verbose_name='Titulo habitación en inglés')),
                ('descripcion_en', models.CharField(max_length=200, verbose_name='Descripción en inglés')),
                ('capacidad_max', models.IntegerField(verbose_name='Capacidad Máxima habitación')),
                ('precio', models.CharField(max_length=50, verbose_name='Precio')),
                ('estado', models.CharField(default='Disponible', max_length=50, verbose_name='Estado')),
                ('imagen', models.TextField(blank=True, null=True, verbose_name='Datos de la imagen en base64')),
            ],
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id_metodo_pago', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id Metodo Pago')),
                ('tipo_metodo_pago', models.CharField(max_length=20, verbose_name='Metodo Pago')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroUsuario',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id usuario')),
                ('nombres', models.CharField(max_length=50, verbose_name='Nombres del usuario')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos del usuario')),
                ('correo', models.EmailField(max_length=50, verbose_name='Correo del usuario')),
                ('telefono', models.CharField(default='', max_length=25, verbose_name='Teléfono del usuario')),
                ('contrasena', models.CharField(default='', max_length=25, verbose_name='Contraseña del usuario')),
                ('rol', models.CharField(blank=True, default='Cliente', max_length=20, null=True, verbose_name='Rol del usuario')),
            ],
        ),
        migrations.CreateModel(
            name='TipoHabitacion',
            fields=[
                ('id_tipo_hab', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='ID tipo habitación')),
                ('tipo_hab', models.CharField(max_length=25, verbose_name='Tipo habitación')),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id_tipo_usuario', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('nombre_tipo_usuario', models.CharField(max_length=20, verbose_name='Nombre tipo usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id_reserva', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id reserva')),
                ('id_user', models.CharField(max_length=20, verbose_name='Id Usuario')),
                ('order_id', models.CharField(default='', max_length=100, verbose_name='Id Orden PayPal')),
                ('fecha_llegada', models.DateField(verbose_name='Fecha Llegada')),
                ('fecha_salida', models.DateField(verbose_name='Fecha Salida')),
                ('cant_adultos', models.IntegerField(verbose_name='Cantidad Adultos')),
                ('cant_ninos', models.IntegerField(null=True, verbose_name='Cantidad Niños')),
                ('habitacion', models.CharField(max_length=50, verbose_name='Titulo Habitación')),
                ('total', models.IntegerField(verbose_name='Total Reserva')),
                ('pago_inicial', models.IntegerField(verbose_name='Pago Inicial Reserva')),
                ('pago_pendiente', models.IntegerField(verbose_name='Pago Pendiente')),
                ('estado_pago', models.CharField(default='Pendiente', max_length=20, verbose_name='Estado Pago')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_hab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appPacific.habitacion', verbose_name='ID Tipo Habitación')),
                ('id_metodo_pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appPacific.metodopago', verbose_name='ID Método de Pago cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteReserva',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='ID reporte')),
                ('dia_ingreso', models.DateField(verbose_name='Dia Ingreso')),
                ('hora_ingreso', models.TimeField(blank=True, null=True)),
                ('dia_salida', models.DateField(verbose_name='Dia Salida')),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('id_reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appPacific.reserva', verbose_name='Reserva')),
            ],
        ),
        migrations.AddField(
            model_name='habitacion',
            name='id_tipo_hab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appPacific.tipohabitacion', verbose_name='ID tipo habitación'),
        ),
    ]