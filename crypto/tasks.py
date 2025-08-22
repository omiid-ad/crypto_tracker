import logging
import requests

from celery import shared_task
from django.utils import timezone

from crypto.models import Coin

logger = logging.getLogger(__name__)


@shared_task
def update_or_create_coins():
    source_endpoint = 'https://apiv2.nobitex.ir/v3/orderbook/all'
    try:
        response = requests.get(source_endpoint)
        response.raise_for_status()
        data = response.json()
        for key, value in data.items():
            if key != "status":  # skip the status key
                coin, _ = Coin.objects.get_or_create(
                    symbol=key
                )
                coin.price = float(value['lastTradePrice'] if value['lastTradePrice'] else 0)
                coin.last_price_update = timezone.now()
                coin.save(update_fields=['last_price_update', 'price'])

    except requests.exceptions.RequestException as e:
        logger.error(f'Error connecting to Nobitex API: {str(e)}')
