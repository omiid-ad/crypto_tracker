from django.contrib import admin

from crypto.models import CoinPriceHistory, Coin

admin.site.register(CoinPriceHistory)
admin.site.register(Coin)
