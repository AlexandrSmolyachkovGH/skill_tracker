# Generated by Django 5.2.1 on 2025-05-29 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
