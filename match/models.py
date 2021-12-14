from django.db import models

from archer.models import Archer, ArcherSkins
from config.settings import AUTH_USER_MODEL
from unit.models import Unit, UnitSkins
from django.utils.translation import gettext_lazy as _


class Match(models.Model):
    class Winner(models.TextChoices):
        PLAYER1 = 'player1_id', _('player1')
        PLAYER2 = 'player2_id', _('player2')

    id          = models.BigAutoField(db_column='ID', primary_key=True)
    winner      = models.CharField(db_column='Winner', max_length=15, choices=Winner.choices, blank=True, null=True)
    duration    = models.IntegerField(db_column='Duration', blank=True, null=True)
    max_viewers_count = models.IntegerField(db_column='MaxViewersCount', blank=True, null=True)
    date        = models.DateTimeField(db_column='Date', auto_now_add=True)
    player1_id  = models.ForeignKey(AUTH_USER_MODEL, models.SET_NULL, db_column='Player1ID', related_name='player1', blank=True, null=True)
    player2_id  = models.ForeignKey(AUTH_USER_MODEL, models.SET_NULL, db_column='Player2ID', related_name='player2', blank=True, null=True)

    class Meta:
        db_table = 'Match'


class Deck(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    unit1_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit1ID', related_name='unit1', blank=True, null=True)
    unit2_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit2ID', related_name='unit2', blank=True, null=True)
    unit3_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit3ID', related_name='unit3', blank=True, null=True)
    unit4_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit4ID', related_name='unit4', blank=True, null=True)
    unit5_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit5ID', related_name='unit5', blank=True, null=True)
    unit6_id = models.ForeignKey(Unit, models.SET_NULL, db_column='Unit6ID', related_name='unit6', blank=True, null=True)
    unit1_level = models.PositiveBigIntegerField(db_column='Unit1Level')
    unit2_level = models.PositiveBigIntegerField(db_column='Unit2Level')
    unit3_level = models.PositiveBigIntegerField(db_column='Unit3Level')
    unit4_level = models.PositiveBigIntegerField(db_column='Unit4Level')
    unit5_level = models.PositiveBigIntegerField(db_column='Unit5Level')
    unit6_level = models.PositiveBigIntegerField(db_column='Unit6Level')
    unit1_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit1SkinID', related_name='unit1_skin', blank=True, null=True)
    unit2_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit2SkinID', related_name='unit2_skin', blank=True, null=True)
    unit3_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit3SkinID', related_name='unit3_skin', blank=True, null=True)
    unit4_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit4SkinID', related_name='unit4_skin', blank=True, null=True)
    unit5_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit5SkinID', related_name='unit5_skin', blank=True, null=True)
    unit6_skin_id = models.ForeignKey(UnitSkins, models.SET_NULL, db_column='Unit6SkinID', related_name='unit6_skin', blank=True, null=True)
    archer_id = models.ForeignKey(Archer, models.SET_NULL, db_column='ArcherID', blank=True, null=True)
    archer_skin_id = models.ForeignKey(ArcherSkins, models.SET_NULL, db_column='ArcherSkinsID', blank=True, null=True)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='UserID')

    class Meta:
        db_table = 'Deck'



