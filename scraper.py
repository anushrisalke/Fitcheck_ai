import requests
from bs4 import BeautifulSoup


def get_product_data(url):

    try:

        response = requests.get(
    url,
    timeout=15,

    headers={

        "User-Agent": "Mozilla/5.0"
    }
)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.string

        return {
            "website": url.split("/")[2],

            "product_name": title,

            "brand": "Not Found",

            "price": "Not Found",

             "rating": "Not Found",

            "image_url": "Not Found"
        }

    except Exception as e:

      print("SCRAPER ERROR:", e)

      return {
        "website": "Error",
         "product_name": "Error",
          "brand": "Error",
          "price": "Error",
          "rating": "Error",
          "image_url": "Error"
         }

def calculate_buy_score(data):

    score = 0

    if data["product_name"] != "Error":
        score += 40

    if data["price"] != "Not Found":
        score += 30

    if data["rating"] != "Not Found":
        score += 30

    return score

