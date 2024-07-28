# alerts/management/commands/start_binance_websocket.py

from django.core.management.base import BaseCommand
import asyncio
from alerts.price_checker import start_price_listener

class Command(BaseCommand):
    help = 'Start Binance WebSocket client'

    def handle(self, *args, **options):
        asyncio.run(start_price_listener())
