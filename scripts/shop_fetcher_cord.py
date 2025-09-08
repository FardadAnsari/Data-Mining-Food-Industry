import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import random
import asyncio
import concurrent.futures

from modules.justeat_api import JustEatAPI




class ShopFetcherCoordinate:
    def __init__(
        self,
        coordinates_file="cord_G.txt",
        output_dir="data",
        batch_size=1000,
        max_workers=50,
    ):
        self.coordinates_file = coordinates_file
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.max_workers = max_workers

        self.api = JustEatAPI()
        os.makedirs(self.output_dir, exist_ok=True)





    def load_coordinates(self, coordinates_file):
        if not os.path.exists(coordinates_file):
            raise FileNotFoundError(f"Coordinates file not found: {coordinates_file}")
        with open(coordinates_file, "r") as f:
            lines = f.read().splitlines()
        return [line.strip() for line in lines if line.strip()]







    def _fetch_and_save(self, latitude, longitude):
        try:
            data = self.api.get_restaurants_by_coordinates(latitude, longitude)
        except Exception as e:
            print(f"❌ Request error for coordinates {latitude}, {longitude}: {e}")
            return

        if data:
            for shop in data:
                shop_id = shop.get("id")
                filename = os.path.join(self.output_dir, f"{shop_id}.json")
                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"✅ Saved shop data for coordinates {latitude}, {longitude}")
                except Exception as e:
                    print(f"❌ Error saving shop data for coordinates {latitude}, {longitude}: {e}")

        else:
            print(f"❌ Empty or invalid for coordinates {latitude}, {longitude}")






    async def run(self):
        loop = asyncio.get_running_loop()
        coordinates = self.load_coordinates(self.coordinates_file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = []
            for coord in coordinates:
                lat, lon = map(str.strip, coord.split(","))
                task = loop.run_in_executor(executor, self._fetch_and_save, lat, lon)
                tasks.append(task)

                if len(tasks) >= self.batch_size:
                    await asyncio.gather(*tasks)
                    tasks = []

            if tasks:
                await asyncio.gather(*tasks)








# ---- Run directly or import elsewhere ----
if __name__ == "__main__":
    fetcher = ShopFetcherCoordinate(
        coordinates_file="config/cord_G.txt",
        output_dir="data",
        batch_size=1000,
        max_workers=50,
    )
    asyncio.run(fetcher.run())
