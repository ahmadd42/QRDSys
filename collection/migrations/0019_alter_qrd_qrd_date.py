# Generated by Django 4.2.5 on 2023-12-17 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0018_alter_qrd_qrd_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrd',
            name='qrd_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 17, 15, 49, 50, 920988)),
        ),
    ]