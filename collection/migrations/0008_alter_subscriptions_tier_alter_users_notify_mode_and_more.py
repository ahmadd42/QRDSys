# Generated by Django 4.2.5 on 2023-11-25 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_users_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='tier',
            field=models.CharField(choices=[('standard', 'standard'), ('gold', 'gold'), ('platinum', 'platinum')], max_length=9),
        ),
        migrations.AlterField(
            model_name='users',
            name='notify_mode',
            field=models.CharField(choices=[('email', 'email'), ('sms', 'sms')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='type_of_user',
            field=models.CharField(choices=[('subscriber', 'subscriber'), ('service seeker', 'service seeker')], max_length=15),
        ),
    ]
