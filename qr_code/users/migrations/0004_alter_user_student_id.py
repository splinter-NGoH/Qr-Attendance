# Generated by Django 4.0.10 on 2023-03-11 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_city_user_country_user_gender_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
