from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager
#
class RoleManager(Manager):
    def get_role(self, rol):
        return self.get(id=rol)
    

class UserManager(BaseUserManager, Manager):
    def _create_user(self, email, password, rol, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email=email,
            rol=rol,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    
    def create_superuser(self, email, password,  **extra_fields):
        return self._create_user(email, password, None, True, True, **extra_fields)

    def create_user(self, email, password, rol, **extra_fields):
        return self._create_user(email, password, rol, False, False, **extra_fields)
    