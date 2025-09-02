import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import random
import asyncio
import concurrent.futures
from fake_useragent import UserAgent
from modules.foodhub_api import foodhub_api




class ShopFetcher:
    def __init__(
        self,
        start_id=0,
        end_id=1_000_001,
        use_proxy=False,
        proxy_file="proxies.txt",
        output_dir="results",
        batch_size=1000,
        max_workers=50,
    ):
        self.start_id = start_id
        self.end_id = end_id
        self.use_proxy = use_proxy
        self.proxy_file = proxy_file
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.max_workers = max_workers

        self.api = foodhub_api()
        self.user_agent = UserAgent()
        self.proxies = self._load_proxies() if self.use_proxy else []

        os.makedirs(self.output_dir, exist_ok=True)


    def _load_proxies(self):
        if not os.path.exists(self.proxy_file):
            raise FileNotFoundError(f"Proxy file not found: {self.proxy_file}")
        with open(self.proxy_file, "r") as f:
            lines = f.read().splitlines()
        return [self._format_proxy(line) for line in lines if line.strip()]

    @staticmethod
    def _format_proxy(proxy_str):
        parts = proxy_str.strip().split(":")
        if len(parts) == 4:
            ip, port, user, pwd = parts
            return f"http://{user}:{pwd}@{ip}:{port}"
        elif len(parts) == 2:
            ip, port = parts
            return f"http://{ip}:{port}"
        else:
            raise ValueError(f"Invalid proxy format: {proxy_str}")

    def _get_random_proxy(self):
        if not self.use_proxy or not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        return {"http": proxy, "https": proxy}




    def _fetch_and_save(self, shop_id):
        proxy = self._get_random_proxy()
        ua = self.user_agent.random

        try:
            data = self.api.get_restaurant_by_id(shop_id, user_agent=ua, proxy=proxy)
        except Exception as e:
            print(f"❌ Request error for shop_id {shop_id}: {e}")
            return

        if data:
            filename = os.path.join(self.output_dir, f"{shop_id}.json")
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"✅ Saved shop_id {shop_id}")
            except Exception as e:
                print(f"❌ Error saving shop_id {shop_id}: {e}")
        else:
            print(f"❌ Empty or invalid for shop_id {shop_id}")






    async def run(self):
        loop = asyncio.get_running_loop()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = []
            for shop_id in range(self.start_id, self.end_id):
                task = loop.run_in_executor(executor, self._fetch_and_save, shop_id)
                tasks.append(task)

                if len(tasks) >= self.batch_size:
                    await asyncio.gather(*tasks)
                    tasks = []

            if tasks:
                await asyncio.gather(*tasks)








# ---- Run directly or import elsewhere ----
if __name__ == "__main__":
    fetcher = ShopFetcher(
        start_id=880068,
        end_id=1_000_001,
        use_proxy=False,
        proxy_file="",
        output_dir="data",
        batch_size=1000,
        max_workers=50,
    )
    asyncio.run(fetcher.run())
