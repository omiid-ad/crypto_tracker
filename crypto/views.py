from datetime import timedelta

from django.db.models import Prefetch
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from crypto.models import Coin, CoinPriceHistory
from crypto.paginations import CoinPagination
from crypto.serializers import CoinSerializer, CoinPriceHistorySerializer


class CoinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coin.objects.prefetch_related(
        Prefetch(
            'price_history',
            queryset=CoinPriceHistory.objects.order_by('-timestamp')
        )
    )
    serializer_class = CoinSerializer
    pagination_class = CoinPagination

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        try:
            if lookup_value.isdigit():
                return self.queryset.get(pk=int(lookup_value))
            return self.queryset.get(symbol__iexact=lookup_value)
        except Coin.DoesNotExist:
            raise NotFound(detail="Coin not found")

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        coin = self.get_object()
        three_days_ago = now() - timedelta(days=3)
        history_qs = [h for h in coin.price_history.all() if h.timestamp >= three_days_ago]

        if not history_qs:
            raise NotFound("No history found for this coin in the last 3 days.")

        serializer = CoinPriceHistorySerializer(history_qs, many=True)
        return Response(serializer.data)
