import asyncio
import json
import websockets
import django
import os
import logging
from django.core.mail import send_mail
from alerts.models import Alert
from asgiref.sync import sync_to_async

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_alerts.settings')
django.setup()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_price():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                async for message in websocket:
                    data = json.loads(message)
                    price = float(data['p'])
                    logger.info(f"Received price update: {price}")

                    # Fetch alerts
                    alerts = await sync_to_async(list)(Alert.objects.filter(status='created', cryptocurrency='BTC'))
                    for alert in alerts:
                        if (alert.target_price <= price and price >= alert.target_price) or \
                                (alert.target_price >= price and price <= alert.target_price):
                            user_email = await sync_to_async(lambda: alert.user.email)()
                            logger.info(f"Triggering alert for {user_email} at price {alert.target_price}")

                            # Send email
                            await sync_to_async(send_mail)(
                                'Price Alert Triggered',
                                f'The price for BTC has reached {alert.target_price}',
                                'keshiba1238@gmail.com',
                                [user_email],
                                fail_silently=False,
                            )

                            # Update alert status
                            alert.status = 'triggered'
                            await sync_to_async(alert.save)()
                            logger.info(f"Email sent to {user_email} and alert status updated.")
        except websockets.ConnectionClosed as e:
            logger.warning(f"WebSocket connection closed: {e}")
            await asyncio.sleep(1)  # Reconnect after a short delay
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            await asyncio.sleep(1)  # Handle other exceptions and reconnect


def start_price_listener():
    asyncio.run(get_price())


if __name__ == "__main__":
    start_price_listener()
