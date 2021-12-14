from django.db import models

from config.settings import AUTH_USER_MODEL
from user.models import User
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
