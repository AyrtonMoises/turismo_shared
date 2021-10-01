# Generated by Django 3.2.7 on 2021-09-29 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_remove_perfil_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL),
        ),
    ]
