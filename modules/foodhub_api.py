import json
import requests


class foodhub_api:
    def __init__(self):
        self.HEADERS = {
            "franchise": "foodhub.co.uk",
            "user-agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 "
                "Mobile/15E148 Safari/537.36"
            ),
        }
        self.URL = "https://foodhub.co.uk/api/consumer/store?app_name=FRANCHISE"


    def get_restaurant_by_id(self, shop_id, user_agent=None, proxy=None):
        headers = self.HEADERS.copy()
        headers["user-agent"] = user_agent or headers["user-agent"]
        headers["store"] = str(shop_id)

        try:
            response = requests.get(self.URL, headers=headers, proxies=proxy)
            json_data = response.json()

            if json_data.get("error", {}):
                print(f"⚠️shop_id({shop_id}): {json_data.get('error').get('message', '')}")
                return {}

            return json_data

        except Exception as e:
            print(f"❌ Failed to fetch restaurant by ID {shop_id}: {e}")
            return {}





if __name__ == "__main__":
    api = foodhub_api()
    shop_id = 865153  # Example shop ID
    restaurant_data = api.get_restaurant_by_id(shop_id)
    print(restaurant_data)