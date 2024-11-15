from django.utils import timezone
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ('admin', 'admin'),
        ('user', 'user'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=6, choices=ROLE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, blank=True)
    number = PhoneNumberField(unique=True, blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", 'password', 'role']

    objects = CustomManager()
    
    def __str__(self):
        return self.name

class Organization(models.Model):
    title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    commits = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old = Table.objects.get(pk=self.pk)
            if old.status != self.status:
                self.updated_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.name} - {self.organization.title}"
