from rest_framework import serializers

from crypto.models import Coin, CoinPriceHistory


class CoinPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPriceHistory
        fields = ['price', 'timestamp']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['symbol', 'price', 'last_price_update', 'persian_name', 'english_name']
