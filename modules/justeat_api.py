import json

import requests



class JustEatAPI:
    """
    A Python wrapper for retrieving restaurant data from the Just Eat API based on location.
    """
    def __init__(self):
        self.HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
        }


    def get_restaurants_by_coordinates(self, latitude, longitude):
        """
        Retrieve a list of restaurants based on latitude and longitude.
        """
        url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched?latitude={latitude}&longitude={longitude}"

        try:
            response = requests.get(url, headers=self.HEADERS)
            data = response.json()
            return data.get("restaurants", [])

        except Exception as error:
            print(f"❌ Failed to get restaurants from JustEat: {error}")
            return []







if __name__ == "__main__":
    justeat = JustEatAPI()

    lat, lng = 55.8621354408273, -4.27839211407259
    restaurants = justeat.get_restaurants_by_coordinates(lat, lng)

    if restaurants:
        print(f"✅ Found {len(restaurants)} restaurants in the area.")
        with open(f"restaurants_{lat}_{lng}.json", 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=4)
            print("  - Data saved to file.")
    else:
        print("❌ No restaurants found in the area.")

    justeat.rm.report()
