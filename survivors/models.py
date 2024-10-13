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
    items = models.ManyToManyField('Item', verbose_name=_('Itens'), through='Inventory')
    reports = models.ManyToManyField('self', verbose_name=_('Denúncias'), through='Report', symmetrical=False)


    class Meta:
        verbose_name = _('Sobrevivente')
        verbose_name_plural = _('Sobreviventes')
        indexes = [
            models.Index(fields=['name', 'date_of_birth']),
        ]

    def __str__(self):
        return self.name


class Item(models.Model):
    NAME_CHOICES = (
        ('Água', _('Água')),
        ('Comida', _('Comida')),
        ('Medicação', _('Medicação')),
        ('Munição', _('Munição'))
    )

    name = models.CharField(verbose_name=_('Nome'), max_length=100, choices=NAME_CHOICES)
    points = models.PositiveIntegerField(verbose_name=_('Pontos'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Itens')
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Inventory(models.Model):
    survivor = models.ForeignKey(Survivor, verbose_name=_('Sobrevivente'), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=_('Item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantidade'))

    class Meta:
        verbose_name = _('Inventário')
        verbose_name_plural = _('Inventários')
        indexes = [
            models.Index(fields=['survivor', 'item']),
        ]

    def __str__(self):
        return f'{self.survivor.name} - {self.item.name}'


class Report(models.Model):
    reporter = models.ForeignKey(Survivor, verbose_name=_('Denunciante'), on_delete=models.CASCADE, related_name='reporter')
    reported = models.ForeignKey(Survivor, verbose_name=_('Denunciado'), on_delete=models.CASCADE, related_name='reported')
    description = models.TextField(verbose_name=_('Descrição'))

    class Meta:
        verbose_name = _('Denúncia')
        verbose_name_plural = _('Denúncias')
        indexes = [
            models.Index(fields=['reporter', 'reported']),
        ]

    def __str__(self):
        return f'{self.reporter.name} - {self.reported.name}'


class Trade(models.Model):
    requester = models.ForeignKey(Survivor, verbose_name=_('Solicitante'), on_delete=models.CASCADE, related_name='requester')
    requested = models.ForeignKey(Survivor, verbose_name=_('Solicitado'), on_delete=models.CASCADE, related_name='requested')
    items_requester = models.ManyToManyField(Item, verbose_name=_('Itens Solicitante'), through='TradeItem', related_name='items_requester')
    items_requested = models.ManyToManyField(Item, verbose_name=_('Itens Solicitado'), through='TradeItem', related_name='items_requested')
    status = models.BooleanField(verbose_name=_('Status'), default=False)


    class Meta:
        verbose_name = _('Troca')
        verbose_name_plural = _('Trocas')
        indexes = [
            models.Index(fields=['requester', 'requested']),
        ]

    def __str__(self):
        return f'{self.requester.name} - {self.requested.name}'


class TradeItem(models.Model):
    trade = models.ForeignKey(Trade, verbose_name=_('Troca'), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=_('Item'), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_('Quantidade'))

    class Meta:
        verbose_name = _('Item da Troca')
        verbose_name_plural = _('Itens da Troca')
        indexes = [
            models.Index(fields=['trade', 'item']),
        ]

    def __str__(self):
        return f'{self.trade.requester.name} - {self.trade.requested.name} - {self.item.name}'
