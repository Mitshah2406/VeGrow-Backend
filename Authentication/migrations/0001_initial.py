# Generated by Django 4.0.10 on 2023-03-22 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllProductList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=254, unique=True)),
                ('imgage', models.ImageField(null=True, upload_to='farmers/allProductList')),
                ('productMarketPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='userAuth',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(max_length=254, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farmers',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fName', models.CharField(max_length=254)),
                ('lName', models.CharField(max_length=254)),
                ('location', models.JSONField(default=dict, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region='IN')),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fName', models.CharField(max_length=254)),
                ('lName', models.CharField(max_length=254)),
                ('location', models.JSONField(default=dict, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region='IN')),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('inventoryId', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=254)),
                ('productDescription', models.TextField(null=True)),
                ('productListedDate', models.DateField(auto_now_add=True)),
                ('productExpiryDate', models.DateField(null=True)),
                ('productImages', models.TextField(blank=True, default='', null=True)),
                ('productUnit', models.CharField(max_length=254, null=True)),
                ('productQuantity', models.CharField(max_length=254, null=True)),
                ('initialBidPrice', models.DecimalField(decimal_places=2, max_digits=15)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Authentication.allproductlist')),
                ('farmerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.farmers')),
            ],
        ),
    ]
