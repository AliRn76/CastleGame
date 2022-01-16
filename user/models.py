from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException

from config.settings import AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def get_or_raise(self, *args, **kwargs):
        queryset = super().get_queryset()
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            raise APIException(detail=f'{queryset.model} Does Not Exist', code=status.HTTP_404_NOT_FOUND)

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Username Can\'t be empty')
        if not password:
            raise ValueError('Admin Most Have a Password')

        user = self.model(username=username)
        user.password = make_password(password)
        user.date_registered = timezone.now()
        user.save()
        return user

    # def create_admin(self, email, password=None):
    #     admin = self.create_user(email, password=password)
    #     Permissions.objects.create(user_id=admin)
    #     admin.is_admin = True
    #     admin.is_registered = True
    #     admin.is_premium = True
    #     admin.has_traffic = True
    #     admin.save(using=self._db)
    #     return admin

    def create_superuser(self, username, password=None):
        super_user = self.create_user(username, password=password)
        super_user.is_super_user = True
        super_user.is_admin = True
        super_user.save(using=self._db)
        return super_user

    def admin(self):
        return self.filter(is_admin=True)

    def banned(self):
        return self.filter(is_banned=True)

    def not_banned(self):
        return self.filter(is_banned=False)

    def online(self):
        return self.filter(is_online=True)


class User(AbstractBaseUser):
    def icon_path(self, filename: str) -> str: return f'icons/user_{self.id}-{uuid4().hex}-{filename}'

    id          = models.BigAutoField(db_column='ID', primary_key=True)
    xp          = models.PositiveIntegerField(db_column='XP', default=0)
    gold        = models.PositiveIntegerField(db_column='Gold', default=0)
    gem         = models.PositiveIntegerField(db_column='Gem', default=0)
    score       = models.PositiveIntegerField(db_column='Score', default=0)
    # icon        = models.ImageField(db_column='Icon', upload_to=icon_path, blank=True, null=True)
    region      = models.CharField(db_column='Region', max_length=255)
    username    = models.CharField(db_column='Username', max_length=63, unique=True)
    password    = models.CharField(db_column='Password', max_length=127, blank=True, null=True)
    wins_count      = models.PositiveIntegerField(db_column='WinsCount', default=0)
    losses_count    = models.PositiveIntegerField(db_column='LossesCount', default=0)
    is_online       = models.BooleanField(db_column='IsOnline', default=False)  # We can store it on redis
    is_admin        = models.BooleanField(db_column='IsAdmin', default=False)
    is_banned       = models.BooleanField(db_column='IsBanned', default=False)
    is_super_user      = models.BooleanField(db_column='IsSuperUser', default=False)
    last_login          = models.DateTimeField(db_column='LastLogin', blank=True, null=True)
    date_joined         = models.DateTimeField(db_column='DateJoined', auto_now_add=True)
    chest_opened_count  = models.PositiveIntegerField(db_column='ChestOpenedCount', default=0)
    # archer_race_id      = models.ForeignKey(to='archer.ArcherRace', on_delete=models.SET_NULL, db_column='ArcherRaceID', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD  = 'username'

    class Meta:
        db_table = 'User'

    @property
    def is_staff(self):
        return self.is_super_user

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Friend(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user1_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='User1ID', related_name='user1')
    user2_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='User2ID', related_name='user2')
    is_accepted = models.BooleanField(db_column='IsAccepted', default=False)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)

    class Meta:
        db_table = 'Friend'
        unique_together = ['user1_id', 'user2_id']

    # If always set the lower ID in user1_id, we won't have conflict here (2 people can't be friend two times.)

