# Generated by Django 5.1.3 on 2024-11-14 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0009_user_telegram_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='commits',
            field=models.TextField(blank=True, null=True),
        ),
    ]