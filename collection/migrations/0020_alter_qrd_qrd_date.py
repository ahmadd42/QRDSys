# Generated by Django 4.2.5 on 2023-12-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0019_alter_qrd_qrd_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrd',
            name='qrd_date',
            field=models.DateTimeField(),
        ),
    ]