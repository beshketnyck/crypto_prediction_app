import aiohttp
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import os
import requests_cache

requests_cache.install_cache('crypto_cache', expire_after=300)

class DataAnalyser:
    def __init__(self, base_api_url):
        self.base_api_url = base_api_url
        self.timeout = aiohttp.ClientTimeout(total=60*60*24, sock_connect=30, sock_read=30)

    async def fetch_data(self, session, start_date, end_date, coin_id):
        url = f'{self.base_api_url}/coins/{coin_id}/market_chart/range'
        params = {
            'vs_currency': 'usd',
            'from': int(start_date.timestamp()),
            'to': int(end_date.timestamp())
        }
        try:
            print(f"Fetching data from {url} with params {params}")
            async with session.get(url, params=params, timeout=self.timeout) as response:
                print(f"Response status: {response.status}")
                data = await response.json()

                if 'prices' not in data:
                    raise ValueError("Invalid response from API: 'prices' key not found")

                prices = data['prices']
                market_caps = data.get('market_caps', [])
                volumes = data.get('total_volumes', [])

                df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'], unit='ms')
                df_prices.set_index('timestamp', inplace=True)

                if market_caps:
                    df_market_caps = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
                    df_market_caps['timestamp'] = pd.to_datetime(df_market_caps['timestamp'], unit='ms')
                    df_market_caps.set_index('timestamp', inplace=True)
                    df_prices['market_cap'] = df_market_caps['market_cap']

                if volumes:
                    df_volumes = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
                    df_volumes['timestamp'] = pd.to_datetime(df_volumes['timestamp'], unit='ms')
                    df_volumes.set_index('timestamp', inplace=True)
                    df_prices['volume'] = df_volumes['volume']

                daily_data = df_prices.resample('D').apply(lambda x: x.at_time('12:00') if '12:00' in x.index.time else x.iloc[0])
                daily_data.index = daily_data.index.date

                daily_data = daily_data[(daily_data.index >= start_date.date()) & (daily_data.index <= end_date.date())]

                return daily_data
        except asyncio.TimeoutError:
            print("Request timed out")
            return None
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    async def get_data(self, start_date, end_date, coin_id):
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            data = await self.fetch_data(session, start_date, end_date, coin_id)
        return data

    def save_to_csv(self, data, filename):
        dir_path = './app/main/data'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filepath = os.path.join(dir_path, filename)
        data.to_csv(filepath, index=True)

    async def fetch_twitter_followers(self, coin_id):
        url = f'{self.base_api_url}/coins/{coin_id}'
        try:
            print(f"Fetching Twitter followers from {url}")
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    print(f"Response status: {response.status}")
                    data = await response.json()
                    if 'community_data' in data:
                        return data['community_data'].get('twitter_followers', 'N/A')
                    return 'N/A'
        except asyncio.TimeoutError:
            print("Request timed out")
            return 'N/A'
        except aiohttp.ClientError as e:
            print(f"Client error: {e}")
            return 'N/A'
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 'N/A'
