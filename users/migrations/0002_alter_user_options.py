# Generated by Django 5.0.7 on 2024-09-09 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_view_users', "Can view users' list"), ('can_ban_user', 'Can ban user')]},
        ),
    ]
