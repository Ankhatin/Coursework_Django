# Generated by Django 5.0.7 on 2024-09-08 17:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attempt',
            options={'verbose_name': 'попытка рассылки', 'verbose_name_plural': 'попытки рассылки'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['id'], 'verbose_name': 'клиент', 'verbose_name_plural': 'клиенты'},
        ),
        migrations.AlterModelOptions(
            name='newsletter',
            options={'ordering': ['date_start'], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
        migrations.AddField(
            model_name='attempt',
            name='newsletter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='mailing.newsletter', verbose_name='рассылка'),
        ),
        migrations.AddField(
            model_name='message',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name='медиа'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='is_successful',
            field=models.BooleanField(default=False, verbose_name='статус попытки'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='clients',
            field=models.ManyToManyField(related_name='newsletters', to='mailing.client', verbose_name='клиенты'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='date_start',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='дата и время отправки'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='заголовок'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newsletters', to='mailing.message', verbose_name='сообщение'),
        ),
    ]
