import logging
import requests
from requests import exceptions

LOG_FILENAME = "scraping_logging.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

def make_request(url, *args, **kwargs):
    try:
        response = requests.get(url, **kwargs, timeout=3)
        # print(response.json())
        return response
    except TimeoutError:
        logging.error(f"Failed to make request to {url} : Timed Out")
    except exceptions.HTTPError as e:
        logging.error(f"Failed to make requests to {url} : {e.errno}")