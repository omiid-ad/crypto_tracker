import logging
import requests

from celery import shared_task
from django.utils import timezone

from crypto.models import Coin

logger = logging.getLogger(__name__)


@shared_task
def update_or_create_coins():
    source_endpoint = 'https://apiv2.nobitex.ir/v3/orderbook/all'
    logger.info("Starting coin update task...")
    logger.debug(f"Fetching data from endpoint: {source_endpoint}")

    try:
        response = requests.get(source_endpoint, timeout=10)
        response.raise_for_status()
        logger.info("Successfully fetched data from Nobitex API.")

        data = response.json()
        logger.debug(f"API response keys: {list(data.keys())}")

        coins_processed = 0
        for key, value in data.items():
            if key == "status":
                logger.debug("Skipping status key in API response.")
                continue

            try:
                last_price = float(value.get('lastTradePrice', 0) or 0)
                coin, created = Coin.objects.get_or_create(symbol=key)

                if created:
                    logger.info(f"Created new coin record: {key}")
                else:
                    logger.debug(f"Updating existing coin record: {key}")

                coin.price = last_price
                coin.last_price_update = timezone.now()
                coin.save(update_fields=['last_price_update', 'price'])

                logger.info(f"Updated {key} with price {last_price}")
                coins_processed += 1
            except Exception as coin_error:
                logger.error(f"Error updating coin {key}: {coin_error}", exc_info=True)

        logger.info(f"Coin update task completed. Total coins processed: {coins_processed}")

    except requests.exceptions.Timeout:
        logger.error("Timeout occurred while connecting to Nobitex API.", exc_info=True)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Nobitex API: {str(e)}", exc_info=True)
    except Exception as general_error:
        logger.critical(f"Unexpected error in update_or_create_coins: {general_error}", exc_info=True)
