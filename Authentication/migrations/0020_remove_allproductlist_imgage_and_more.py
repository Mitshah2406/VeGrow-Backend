# Generated by Django 4.0.10 on 2023-03-25 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0019_allproductlist_productcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allproductlist',
            name='imgage',
        ),
        migrations.AddField(
            model_name='allproductlist',
            name='productImage',
            field=models.TextField(null=True),
        ),
    ]
