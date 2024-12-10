# Generated by Django 5.0.6 on 2024-05-09 13:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='addProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdtname', models.CharField(max_length=200)),
                ('pdtprice', models.IntegerField()),
                ('pdtimage', models.ImageField(upload_to='images/')),
                ('pdtsize', models.CharField(max_length=200)),
                ('pdtdesc', models.CharField(max_length=300)),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('propic', models.ImageField(upload_to='images/')),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AddWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.addproduct')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('selected_size', models.CharField(max_length=20)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.addproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Addressdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=200)),
                ('address_line2', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('contact_name', models.CharField(max_length=20)),
                ('contact_number', models.IntegerField()),
                ('userdetail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.userregister')),
            ],
        ),
    ]
