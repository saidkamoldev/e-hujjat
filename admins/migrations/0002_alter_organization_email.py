# Generated by Django 5.1.3 on 2024-11-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
