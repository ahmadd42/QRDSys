# Generated by Django 4.2.5 on 2023-11-26 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0011_rename_guests_guestusers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GuestUsers',
            new_name='Guests',
        ),
    ]