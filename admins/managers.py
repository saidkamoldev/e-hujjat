from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomManager(BaseUserManager):
    def create_user(self, name, email, password, role, **extra_fields):
        if not name:
            raise ValueError("Error")
        if not email:
            raise ValueError("Error")
        if not password:
            raise ValueError("Error")
        if not role:
            raise ValueError("Error")
        
        user = self.model(
            name=name,
            email=email,
            role=role,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password, role, **extra_fields):
        user = self.create_user(
            name, email, password, role
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
