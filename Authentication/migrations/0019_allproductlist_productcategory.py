# Generated by Django 4.0.10 on 2023-03-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0018_productbidding_vendorname'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproductlist',
            name='productCategory',
            field=models.CharField(max_length=254, null=True),
        ),
    ]