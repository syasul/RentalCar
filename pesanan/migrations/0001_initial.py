# Generated by Django 5.0.1 on 2024-06-04 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('grand_total', models.BigIntegerField()),
                ('status', models.CharField(choices=[('Belum Terkonfirmasi', 'Belum Terkonfirmasi'), ('Terkonfirmasi', 'Terkonfirmasi'), ('Dikirim', 'Dikirim')], max_length=20)),
                ('payment_receipt_image_path', models.ImageField(upload_to='images/')),
                ('photo_kk', models.ImageField(upload_to='images/')),
                ('photo_ktp', models.ImageField(upload_to='images/')),
                ('telephone', models.IntegerField()),
                ('address', models.TextField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fine', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('photo_payment_fine', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('status', models.CharField(choices=[('Dikembalikan', 'Dikembalikan'), ('Diterima', 'Diterima')], default='Dikembalikan', max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
