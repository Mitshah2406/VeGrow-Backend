# Generated by Django 4.0.10 on 2023-03-24 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_rename_bitamount_productbidding_bidamount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productbidding',
            old_name='invetoryId',
            new_name='inventoryId',
        ),
    ]