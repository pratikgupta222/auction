from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

from biddings.constants import *

from users.models import User


class AuctionItem(models.Model):
    name = models.CharField(_('Item Name'), max_length=100, unique=True)
    description = models.CharField(_('Item Description'), max_length=255)
    start_time = models.DateTimeField(_('Auction Starts At'), blank=True)
    end_time = models.DateTimeField(_('Auction Ends At'), blank=True)
    starting_amount = models.FloatField(_('Starting Amount'), default=0.0)
    winner = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT)
    image_url = models.TextField(validators=[URLValidator()])
    status = models.CharField(
        _('Auction Status'), max_length=40, default=AUCTION_UPCOMING)

    class Meta:
        verbose_name = _('auction item')
        verbose_name_plural = _('auction items')

    def __str__(self):
        return self.name


class Bids(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    bid_by = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.FloatField(_('Amount'), default=0.0)

    class Meta:
        verbose_name = _('bid')
        verbose_name_plural = _('bids')

    def __str__(self):
        return (self.item.name) + ' | ' + str(self.amount) + ' | ' + str(self.bid_by.email)
