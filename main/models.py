from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import PhoneNumberUserManager
from django.utils import timezone


# Create your models here.

class User(AbstractBaseUser):
    name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(unique=True, max_length=13)
    email = models.EmailField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=25)

    object = PhoneNumberUserManager()
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.phone_number

    def get_short_name(self):
        return self.phone_number

    def __str__(self):
        return str(self.email) + '(' + str(self.phone_number) + ')'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


STATUS_CHOICE = (
    ('PENDING', 'PENDING'),
    ('BOUGHT', 'BOUGHT'),
    ('NOT AVAILABLE', 'NOT AVAILABLE'),
)


class AddItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30, null=False, blank=False)
    item_quantity = models.IntegerField(null=False, blank=False)
    item_status = models.CharField(choices=STATUS_CHOICE, max_length=20, null=False, blank=False, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    date_str = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.user.name + " " + "Added" + " " + self.item_name + ", and the quantity is " + " " + str(
            self.item_quantity) + " " + "on" + " " + str(self.date)


class Savedlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return self.user+" "+"Saved" + str(self.item)
