# Generated by Django 4.2.5 on 2023-11-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_alter_users_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='cat_desc',
            field=models.TextField(default='abc'),
            preserve_default=False,
        ),
    ]
