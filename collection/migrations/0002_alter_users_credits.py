# Generated by Django 4.2.5 on 2023-11-06 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='credits',
            field=models.IntegerField(null=True),
        ),
    ]
