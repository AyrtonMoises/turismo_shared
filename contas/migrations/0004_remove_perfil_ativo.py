# Generated by Django 3.2.7 on 2021-09-29 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_alter_perfil_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='ativo',
        ),
    ]
