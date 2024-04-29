# Generated by Django 5.0.2 on 2024-04-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_is_author_customuser_is_moderator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_author',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_moderator',
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='834033', max_length=6),
        ),
    ]