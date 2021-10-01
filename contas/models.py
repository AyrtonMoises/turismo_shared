from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_resized import ResizedImageField


class UserManager(BaseUserManager):
    """Define model manager para model User sem o campo username."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Cria e salva o usuário passando email e senha"""
        if not email:
            raise ValueError('Email deve ser informado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Cria e salva um usuário regular com email e senha."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Cria e salva um usuário super com email e senha"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ser is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ser is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name=(_('email address')), max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Perfil(models.Model):
    biografia = models.TextField('Bio', blank=True)
    foto = ResizedImageField(size=[500, 300], quality=70, upload_to='usuarios/', blank=True, null=True)
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    twitter = models.URLField('Twitter', blank=True)
    blog = models.URLField('Blog pessoal', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
    """ Cria perfil após cadastro de usuário """
    if created:
        Perfil.objects.create(user=instance)