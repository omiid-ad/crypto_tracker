from rest_framework import serializers

from crypto.models import Coin, CoinPriceHistory


class CoinPriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPriceHistory
        fields = ['price', 'timestamp']


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'
