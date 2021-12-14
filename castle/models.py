from django.db import models
from django.utils.translation import gettext_lazy as _
from config.settings import AUTH_USER_MODEL


class Border(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=63)
    is_available = models.BooleanField(db_column='IsAvailable', default=False)

    class Meta:
        db_table = 'Border'


class UserBorders(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='UserID')
    border_id = models.ForeignKey(Border, models.CASCADE, db_column='BorderID')
    is_active = models.BooleanField(db_column='IsActive', default=True)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)

    class Meta:
        db_table = 'UserBorders'

# class Archer(models.Model):
#     id = models.BigAutoField(db_column='ID', primary_key=True)
#     name = models.CharField(db_column='Name', max_length=63)
#     is_active = models.BooleanField(db_column='IsActive', default=True)
#     date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
#     date_updated = models.DateField(db_column='DateUpdated', auto_now=True)
#     archer_class_id = models.ForeignKey(ArcherClass, models.CASCADE, db_column='ArcherClassID')
#
#     class Meta:
#         db_table = 'Archer'
#
#
# class ArcherSkins(models.Model):
#     id = models.BigAutoField(db_column='ID', primary_key=True)
#     skin_name = models.CharField(db_column='SkinName', max_length=63)
#     archer_id = models.ForeignKey(Archer, models.CASCADE, db_column='ArcherID')
#     date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
#     date_updated = models.DateField(db_column='DateUpdated', auto_now=True)
#
#     class Meta:
#         db_table = 'ArcherSkins'
#
#
# class BoughtArcherSkins(models.Model):
#     id = models.BigAutoField(db_column='ID', primary_key=True)
#     user_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='UserID')
#     archer_skins_id = models.ForeignKey(ArcherSkins, models.CASCADE, db_column='ArcherSkinsID')
#     date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
#
#     class Meta:
#         db_table = 'BoughtArcherSkins'
#
#
