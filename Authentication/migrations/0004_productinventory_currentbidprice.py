# Generated by Django 4.0.10 on 2023-03-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_productinventory_farmerlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinventory',
            name='currentBidPrice',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]
