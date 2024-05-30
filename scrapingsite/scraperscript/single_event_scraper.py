from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, JSONDecodeError
import logging
from django.conf import settings
from time import sleep
import asyncio

from .request_logmaker import make_request
from .models import HeaderSpoofResponse, HockeyTeams, OscarFilms
from .heading_map import heading_mapper

LOG_FILENAME = settings.LOG_FILENAME
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# enhancing the modularity
base_url = "https://www.scrapethissite.com/"

def advanced_header_spoofing():

    page_url = "pages/advanced/"

    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    params = {"gotcha":"headers"}

    try:
        response = requests.get(base_url + page_url, headers=headers, params=params)
        # print(response.text)
        soup = BeautifulSoup(
            response.text,
            "html5lib"
        )

        main_text = soup.find(
            "div",
            attrs= {"class" : "col-md-4 col-md-offset-4"}
        )

        got_it = main_text.text.strip() == "Headers properly spoofed, request appears to be coming from a browser :)"

        HeaderSpoofResponse.objects.create(
            response = got_it
        )
        
        return got_it

    except HTTPError:
        logging.error("Failed to make request")
        raise Exception("Failed to make request")
    
    except Exception as e:
        logging.error(f"An error occurred : {e}")
        raise Exception("some error occured")

def hockey_single_scraper(page_url, title_mapping):
    curr_pageurl = base_url + page_url
    # print(curr_pageurl)
    # using "make_request" it to log the errors but not fail completely
    page_to_scrape = make_request(
        curr_pageurl
    )

    try:

        soup = BeautifulSoup(
            page_to_scrape.text,  # type: ignore
            "html5lib"
        )

        rows = soup.find(
            "table"
        ).find_all(  # type: ignore
            "tr"
        )

        # remove the first element which is the current page
        headings = [
            i.text.strip() for i in rows.pop(0).find_all("th")
        ]

    except Exception as e:
        logging.error(f"Failed to parse table for {curr_pageurl}: {e}")
        return

    headings = heading_mapper(headings, title_mapping)

    chunk = [
        [i.text.strip() for i in row.find_all("td")]
        for row in rows]
    # print(headings, chunk[0])
    bulk = [
        {
            head: item for head, item in zip(
                headings,
                row
            )
        } for row in chunk]

    HockeyTeams.objects.bulk_create(
        HockeyTeams(
            **team
        ) for team in bulk
    )
    
    sleep(2.5)
    # await asyncio.sleep(2.5)


def single_oscar_page_scraper(page_url, year):
    curr_pageurl = base_url + page_url

    params = {
        "ajax": "true",
        "year": year,
    }

    # using "make_request" it to log the errors but not fail completely
    page_to_scrape = make_request(
        curr_pageurl,
        params=params
    )

    try:
        scraped_data = page_to_scrape.json()

        # since the data is json format with key-value pair similar to ORM, this isn't required currently
        # but just in case

        # scraped_data = [
        #     {
        #         title_mapping[i]:j for i,j in entry.items() if i in title_mapping
        #     } for entry in scraped_data
        # ]

        # print("bado badi")

        OscarFilms.objects.bulk_create(
            OscarFilms(
                **entry
            ) for entry in scraped_data
        )

        # break
        sleep(3)
        # await asyncio.sleep(3)

    except JSONDecodeError:
        logging.error(
            f"Failed to parse JSON response for {page_url} : params {params}")