# Generated by Django 4.2.5 on 2023-11-06 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('area_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=200)),
                ('zip_codes', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('cat_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cat_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceLists',
            fields=[
                ('list_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('base_price', models.IntegerField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.areas')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('type_of_user', models.CharField(choices=[('subsc', 'subscriber'), ('seeker', 'service seeker')], max_length=15)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=80, null=True)),
                ('phone', models.BigIntegerField(null=True)),
                ('notify_mode', models.CharField(choices=[('mail', 'email'), ('msg', 'sms')], max_length=6, null=True)),
                ('password', models.CharField(max_length=20)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('sub_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('tier', models.CharField(choices=[('std', 'standard'), ('gold', 'gold'), ('ptn', 'platinum')], max_length=9)),
                ('service_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.servicelists')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.users')),
            ],
        ),
        migrations.CreateModel(
            name='QRD',
            fields=[
                ('qrd_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('budget', models.IntegerField()),
                ('timeline', models.IntegerField()),
                ('description', models.TextField()),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.areas')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.categories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.users')),
            ],
        ),
    ]
