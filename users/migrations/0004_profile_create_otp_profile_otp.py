# Generated by Django 5.0.6 on 2024-08-26 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_uname_profile_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='create_otp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
