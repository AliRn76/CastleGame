from django.db import models
from config.settings import AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _


class UnitClass(models.Model):
    class UnitClasses(models.TextChoices):
        TANK = 'tank', _('Tank')
        AGILITY = 'agility', _('Agility')
        RANGE = 'range', _('Range')
        WITCH = 'witch', _('Witch')

    id = models.BigAutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', choices=UnitClasses.choices, max_length=63)
    base_armor = models.IntegerField(db_column='BaseArmor', default=0)
    base_hp = models.IntegerField(db_column='BaseHP', default=0)
    base_damage = models.IntegerField(db_column='BaseDamage', default=0)
    base_speed = models.IntegerField(db_column='BaseSpeed', default=0)

    class Meta:
        db_table = 'UnitClass'


class Unit(models.Model):
    class MovementType(models.TextChoices):
        GROUND = 0, _('Ground')
        AIR = 1, _('Air')

    class AttackType(models.TextChoices):
        MELEE = 'melee', _('Melee')
        RANGE = 'range', _('Range')

    class TargetType(models.TextChoices):
        GROUND = 'ground', _('Ground')
        AIR = 'air', _('Air')
        BOTh = 'both', _('Both')

    id = models.BigAutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=63)
    armor = models.IntegerField(db_column='Armor', default=0)
    hp = models.IntegerField(db_column='HP', default=0)
    damage = models.IntegerField(db_column='Damage', default=0)
    speed = models.IntegerField(db_column='Speed', default=0)
    movement_type = models.CharField(db_column='MovementType', max_length=15, choices=MovementType.choices)
    attack_type = models.CharField(db_column='AttackType', max_length=15, choices=AttackType.choices)
    target_type = models.CharField(db_column='TargetType', max_length=15, choices=TargetType.choices)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
    date_updated = models.DateField(db_column='DateUpdated', auto_now=True)
    unit_class_id = models.ForeignKey(UnitClass, models.CASCADE, db_column='UnitClassID')

    class Meta:
        db_table = 'Unit'


class UnitSkins(models.Model):
    class CostType(models.TextChoices):
        GOLD = 'gold', _('Gold')
        GEM = 'gem', _('Gem')

    id = models.BigAutoField(db_column='ID', primary_key=True)
    skin_name = models.CharField(db_column='SkinName', max_length=63)
    cost = models.PositiveIntegerField(db_column='Cost', default=0)
    cost_type = models.CharField(db_column='CostType', max_length=63, choices=CostType.choices, default=CostType.GOLD)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)
    date_updated = models.DateField(db_column='DateUpdated', auto_now=True)

    class Meta:
        db_table = 'UnitSkins'


class BoughtUnitSkin(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, db_column='UserID')
    unit_skin_id = models.ForeignKey(UnitSkins, models.CASCADE, db_column='UnitSkinID')

    class Meta:
        db_table = 'BoughtUnitSkin'


class UserUnits(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    level = models.PositiveBigIntegerField(db_column='Level', default=0)
    bought_unit_skin_id = models.ForeignKey(BoughtUnitSkin, models.SET_NULL, blank=True, null=True)
    date_created = models.DateField(db_column='DateCreated', auto_now_add=True)

    class Meta:
        db_table = 'UserUnits'
