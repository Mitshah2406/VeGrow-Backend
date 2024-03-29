# Generated by Django 4.0.10 on 2023-03-23 18:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinventory',
            name='productQuantityLeftInInventory',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='status',
            field=models.CharField(default='listed', max_length=254),
        ),
        migrations.CreateModel(
            name='PurchaseTransactions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('totalPurchasePrice', models.DecimalField(decimal_places=2, max_digits=15)),
                ('purchaseQuantity', models.CharField(max_length=254)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Authentication.vendor')),
                ('inventoryId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Authentication.productinventory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBidding',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('bidQuantity', models.CharField(max_length=254)),
                ('bitAmount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('bidStatus', models.CharField(default='placed', max_length=254)),
                ('invetoryId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Authentication.productinventory')),
                ('vendorId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Authentication.vendor')),
            ],
        ),
    ]
