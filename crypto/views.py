from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from crypto.models import Coin
from crypto.paginations import CoinPagination
from crypto.serializers import CoinSerializer


class CoinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coin.objects.all()
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
