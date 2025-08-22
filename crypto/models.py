from django.db import models


class Coin(models.Model):
    symbol = models.CharField(max_length=20, unique=True, blank=False, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    last_price_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.symbol
