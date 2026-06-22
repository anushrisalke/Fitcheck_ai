import requests
from bs4 import BeautifulSoup


def get_product_data(url):

    try:

        response = requests.get(
    url,
    timeout=15,

    headers={

        "User-Agent":

        "Mozilla/5.0"
    }
)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.string

        return {
            "product_name": title,
            "price": "Not Found",
            "rating": "Not Found"
        }

    except Exception as e:

     print("SCRAPER ERROR:", e)

    return {
        "product_name": "Error",
        "price": "Error",
        "rating": "Error"
    }