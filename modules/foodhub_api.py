import json
import requests
import logging

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

        logging.basicConfig(
            filename="restaurant_scraper.log",
            filemode="a",
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO  # یا DEBUG برای اطلاعات بیشتر
        )


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








    def get_restaurants_by_postcode(self, postcode, user_agent=None, proxy=None):
            url = (
                "https://foodhub.co.uk/api/franchise/v2/takeaway/list?"
                f"api_token=99b8ad5d2f9e80889efcd73bc31f7e7b&app_name=FRANCHISE&postcode={postcode}"
            )
            headers = self.HEADERS.copy()
            headers["user-agent"] = user_agent or headers["user-agent"]

            try:
                response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
                response.raise_for_status()
                json_data = response.json()
                restaurants = json_data.get("data", [])

                if restaurants:
                    shop_ids = [restaurant.get("id") for restaurant in restaurants]
                    msg = f"✅ Found {len(restaurants)} restaurants for postcode ({postcode}) IDs: {shop_ids}"
                    print(msg)
                    logging.info(msg)
                else:
                    msg = f"⚠️ No restaurants found for postcode ({postcode})"
                    print(msg)
                    logging.warning(msg)

                return restaurants

            except requests.exceptions.RequestException as e:
                msg = f"❌ HTTP error for postcode ({postcode}): {e}"
                print(msg)
                logging.error(msg)
            except ValueError as e:
                msg = f"❌ JSON decode error for postcode ({postcode}): {e}"
                print(msg)
                logging.error(msg)
            except Exception as e:
                msg = f"❌ Unexpected error for postcode ({postcode}): {e}"
                print(msg)
                logging.exception(msg)

            return []











if __name__ == "__main__":
    api = foodhub_api()
    shop_id = 865153  # Example shop ID
    restaurant_data = api.get_restaurant_by_id(shop_id)
    print(restaurant_data)