# Generated by Django 4.2.5 on 2023-12-10 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0016_alter_qrd_qrd_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrd',
            name='short_title',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
