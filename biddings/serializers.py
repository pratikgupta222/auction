from rest_framework import serializers

from biddings.models import *


class AuctionItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionItem
        fields = '__all__'


class BidsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bids
        fields = '__all__'