# Generated by Django 4.0.10 on 2023-03-08 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='student_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
