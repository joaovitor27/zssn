from django.db import models

from django.utils.translation import gettext_lazy as _


# Create your models here.
class Survivor(models.Model):
    SEX_CHOICES = (
        ('M', _('Masculino')),
        ('F', _('Feminino')),
        ('O', _('Outro'))
    )

    name = models.CharField(verbose_name=_('Nome'), max_length=100)
    date_of_birth = models.DateField(verbose_name=_('Data de Nascimento'))
    sex = models.CharField(verbose_name=_('Sexo'), max_length=1, choices=SEX_CHOICES)
    latitude = models.FloatField(verbose_name=_('Latitude'))
    longitude = models.FloatField(verbose_name=_('Longitude'))
    infected = models.BooleanField(verbose_name=_('Infectado'), default=False)
    reports = models.ManyToManyField('self', verbose_name=_('Denúncias'), through='Report', symmetrical=False)
    created_at = models.DateTimeField(verbose_name=_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'survivors'
        verbose_name = _('Sobrevivente')
        verbose_name_plural = _('Sobreviventes')
        indexes = [
            models.Index(fields=['name', 'date_of_birth']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['infected']),
            models.Index(fields=['created_at', 'updated_at']),
        ]

    def __str__(self):
        return self.name

    def get_age(self):
        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.infected = self.reports.count() >= 3
        super().save(*args, **kwargs)
        Inventory.objects.get_or_create(survivor=self)



class Item(models.Model):
    WATER = 'Água'
    FOOD = 'Comida'
    MEDICATION = 'Medicação'
    AMMO = 'Munição'

    NAME_CHOICES = (
        (WATER, _('Água')),
        (FOOD, _('Comida')),
        (MEDICATION, _('Medicação')),
        (AMMO, _('Munição')),
    )

    name = models.CharField(verbose_name=_('Nome'), max_length=100, choices=NAME_CHOICES)
    points = models.PositiveIntegerField(verbose_name=_('Pontos'))
    created_at = models.DateTimeField(verbose_name=_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'items'
        verbose_name = _('Item')
        verbose_name_plural = _('Itens')
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class ItemInventory(models.Model):
    item = models.ForeignKey(Item, verbose_name=_('Item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantidade'))
    created_at = models.DateTimeField(verbose_name=_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'items_inventories'
        verbose_name = _('Item no Inventário')
        verbose_name_plural = _('Itens no Inventário')
        indexes = [
            models.Index(fields=['item']),
            models.Index(fields=['quantity']),
            models.Index(fields=['created_at', 'updated_at']),
        ]

    def __str__(self):
        return f'{self.item.name}'


class Inventory(models.Model):
    survivor = models.OneToOneField(Survivor, verbose_name=_('Sobrevivente'), on_delete=models.CASCADE)
    items = models.ManyToManyField(ItemInventory, verbose_name=_('Items'), related_name='items')
    created_at = models.DateTimeField(verbose_name=_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'inventories'
        verbose_name = _('Inventário')
        verbose_name_plural = _('Inventários')
        indexes = [
            models.Index(fields=['survivor']),
            models.Index(fields=['created_at', 'updated_at']),
        ]

    def __str__(self):
        return f'Inventário de {self.survivor.name}'


class Report(models.Model):
    reporter = models.ForeignKey(Survivor, verbose_name=_('Denunciante'), on_delete=models.CASCADE,
                                 related_name='reporter')
    reported = models.ForeignKey(Survivor, verbose_name=_('Denunciado'), on_delete=models.CASCADE,
                                 related_name='reported')
    description = models.TextField(verbose_name=_('Descrição'))
    created_at = models.DateTimeField(verbose_name=_('Criado em'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Atualizado em'), auto_now=True)

    class Meta:
        db_table = 'reports'
        verbose_name = _('Denúncia')
        verbose_name_plural = _('Denúncias')
        indexes = [
            models.Index(fields=['reporter', 'reported']),
        ]

    def __str__(self):
        return f'{self.reporter.name} - {self.reported.name}'
