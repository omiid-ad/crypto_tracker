import os
import json
import logging
import requests

from celery import shared_task
from django.utils import timezone

from crypto.models import Coin, CoinPriceHistory

logger = logging.getLogger(__name__)

CRYPTO_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "crypto.json")
try:
    with open(CRYPTO_FILE_PATH, "r", encoding="utf-8") as f:
        CRYPTO_MAPPING = {item["symbol"]: item for item in json.load(f)}
    logger.info("Crypto mapping loaded successfully.")
except FileNotFoundError:
    CRYPTO_MAPPING = {}
    logger.warning(f"crypto.json not found at {CRYPTO_FILE_PATH}. Persian names will not be set.")


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

                mapping = CRYPTO_MAPPING.get(key)
                if mapping:
                    coin.english_name = mapping.get("english_name")
                    coin.persian_name = mapping.get("persian_name")

                if created:
                    logger.info(f"Created new coin record: {key}")
                else:
                    logger.debug(f"Updating existing coin record: {key}")

                coin.price = last_price
                coin.last_price_update = timezone.now()
                coin.save(update_fields=['last_price_update', 'price', 'english_name', 'persian_name'])

                CoinPriceHistory.objects.create(
                    coin=coin,
                    price=last_price
                )
                logger.debug(f"History saved for {key} at price {last_price}")

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
