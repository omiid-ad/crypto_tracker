from django.db import models
from django.utils import timezone


class Coin(models.Model):
    english_name = models.CharField(max_length=255, blank=True, null=True)
    persian_name = models.CharField(max_length=255, blank=True, null=True)
    symbol = models.CharField(max_length=20, unique=True, blank=False, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    last_price_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.symbol} - {self.persian_name or 'No Persian Name'}"


class CoinPriceHistory(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.coin.symbol} - {self.price} @ {self.timestamp}"
