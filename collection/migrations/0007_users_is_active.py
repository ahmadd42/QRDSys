# Generated by Django 4.2.5 on 2023-11-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_alter_users_email_alter_users_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_active',
            field=models.CharField(default='No', max_length=3),
        ),
    ]