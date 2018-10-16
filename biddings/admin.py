from django.contrib import admin

from biddings.models import *

# Register your models here.


class AuctionItemAdmin(admin.ModelAdmin):
    """Admin view to display the call details of the calls made via exotel"""

    list_display = ('id', 'name', 'description', 'start_time',
                    'end_time', 'starting_amount')


admin.site.register(AuctionItem, AuctionItemAdmin)


class BidsAdmin(admin.ModelAdmin):
    """Admin view to display the call details of the calls made via exotel"""

    list_display = ('id', 'item', 'bid_by', 'amount')


admin.site.register(Bids, BidsAdmin)
