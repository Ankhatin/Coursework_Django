# Generated by Django 5.0.7 on 2024-09-09 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_client_owner_message_owner_newsletter_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['id'], 'permissions': [('can_disable_newsletter', 'Can disable newsletter')], 'verbose_name': 'клиент', 'verbose_name_plural': 'клиенты'},
        ),
    ]
