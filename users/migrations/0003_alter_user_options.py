# Generated by Django 5.0.7 on 2024-09-10 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'permissions': [('can_view_users', "Can view users' list"), ('can_ban_user', 'Can ban user')]},
        ),
    ]
