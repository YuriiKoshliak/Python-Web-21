import aiohttp
import asyncio
from datetime import datetime, timedelta
import json
import sys

class CurrencyRate:
    def __init__(self, days):
        self.days = min(days, 10)
        self.api_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get_currency_rate(self):
        currency_data = []
        async with aiohttp.ClientSession() as session:
            for day in range(self.days):
                date = datetime.now() - timedelta(days=day)
                formatted_date = date.strftime("%d.%m.%Y")
                url = self.api_url + date.strftime("%d.%m.%Y")
                response = await self.fetch(session, url)
                data = json.loads(response)
                eur = usd = None
                for exchange_rate in data['exchangeRate']:
                    if exchange_rate['currency'] == 'EUR':
                        eur = {'sale': exchange_rate['saleRate'], 'purchase': exchange_rate['purchaseRate']}
                    elif exchange_rate['currency'] == 'USD':
                        usd = {'sale': exchange_rate['saleRate'], 'purchase': exchange_rate['purchaseRate']}
                if eur and usd:
                    currency_data.append({formatted_date: {'EUR': eur, 'USD': usd}})
        return currency_data

if __name__ == "__main__":
    days = int(sys.argv[1])
    currency_rate = CurrencyRate(days)
    result = asyncio.run(currency_rate.get_currency_rate())
    print(json.dumps(result, indent=2))
