from django.contrib.auth.models import AbstractUser, UserManager

from django.utils import timezone

from django.contrib.auth.models import Group

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create users with staff authentications when domain fixes"""
        email = self.normalize_email(email)
        is_staff = (lambda x: True if x.split('@')[1] == 'mirrormedia.mg' else False)(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True, last_login=timezone.now(),
                          date_joined=timezone.now(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        group = Group.objects.get(name='board-working-group') 
        user.groups.add(group)
        return user
                                 
# Create your models here.
class User(AbstractUser):
    """Custom User with Custom UserManager"""
    objects = CustomUserManager()
    # class Meta:
    #     db_table='auth_user'

