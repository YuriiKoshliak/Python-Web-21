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
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Помилка при запиті до {url}: {e}")
        except json.JSONDecodeError as e:
            print(f"Помилка при перетворенні відповіді в JSON: {e}")

    async def get_currency_rate(self):
        currency_data = []
        async with aiohttp.ClientSession() as session:
            for day in range(self.days):
                date = datetime.now() - timedelta(days=day)
                formatted_date = date.strftime("%d.%m.%Y")
                url = f"{self.api_url}{formatted_date}"
                response = await self.fetch(session, url)
                if response:
                    try:
                        data = json.loads(response)
                        rates = {rate['currency']: {'sale': rate['saleRate'], 'purchase': rate['purchaseRate']}
                                 for rate in data['exchangeRate'] if rate['currency'] in ['EUR', 'USD']}
                        if rates:
                            currency_data.append({formatted_date: rates})
                    except KeyError as e:
                        print(f"Помилка при доступі до даних курсу валют: {e}")
        return currency_data

if __name__ == "__main__":
    days = int(sys.argv[1])
    currency_rate = CurrencyRate(days)
    result = asyncio.run(currency_rate.get_currency_rate())
    print(json.dumps(result, indent=2))