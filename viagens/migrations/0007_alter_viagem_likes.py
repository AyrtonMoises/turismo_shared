# Generated by Django 3.2.7 on 2021-10-12 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viagens', '0006_rename_datahora_comentario_data_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viagem',
            name='likes',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
