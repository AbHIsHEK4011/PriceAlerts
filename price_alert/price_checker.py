import asyncio
import json
import websockets
import django
import os
import logging
from django.core.mail import send_mail
from alerts.models import Alert

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_alert.settings')
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
                    alerts = Alert.objects.filter(status='created', cryptocurrency='BTC')
                    for alert in alerts:
                        if (alert.target_price <= price and price >= alert.target_price) or \
                           (alert.target_price >= price and price <= alert.target_price):
                            logger.info(f"Triggering alert for {alert.user.email} at price {alert.target_price}")
                            send_mail(
                                'Price Alert Triggered',
                                f'The price for BTC has reached {alert.target_price}',
                                'keshiba1238@gmail.com',
                                [alert.user.email],
                                fail_silently=False,
                            )
                            alert.status = 'triggered'
                            alert.save()
                            logger.info(f"Email sent to {alert.user.email} and alert status updated.")
        except websockets.ConnectionClosed as e:
            logger.warning(f"WebSocket connection closed: {e}")
            await asyncio.sleep(1)  # Reconnect after a short delay
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await asyncio.sleep(1)  # Handle other exceptions and reconnect

def start_price_listener():
    asyncio.get_event_loop().run_until_complete(get_price())

if __name__ == "__main__":
    start_price_listener()
