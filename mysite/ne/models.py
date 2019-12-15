from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class MyUserManager(BaseUserManager):
    def create_user(self, email, age, gender, name, password):

        if not email:
            raise ValueError('Users must have an email address')

        if not age or not gender or not name:
            raise ValueError('Please enter all fields')

        user = self.model(
            email=self.normalize_email(email),
            age=age,
            gender=gender,
            name=name

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, age, gender, name, password):

        user = self.create_user(email, age=age, password=password, gender=gender, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    age = models.IntegerField()
    gender = models.CharField(max_length=2)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'gender', 'name']

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
