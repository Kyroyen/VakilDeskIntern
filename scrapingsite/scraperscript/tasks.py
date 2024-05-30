from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, JSONDecodeError
import logging
from celery import shared_task
from django.conf import settings

from .request_logmaker import make_request
from .models import OscarFilms, HockeyTeams, HeaderSpoofResponse
from .heading_map import heading_mapper
from .single_event_scraper import hockey_single_scraper, single_oscar_page_scraper

LOG_FILENAME = settings.LOG_FILENAME
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# enhancing the modularity
base_url = "https://www.scrapethissite.com/"

@shared_task
def hockey_scraper():

    title_mapping = {
        "Team Name": "team_name",
        "Year": "year",
        "Wins": "wins",
        "Losses": "losses",
        "OT Losses": "ot_losses",
        "Win %": "win_percent",
        "Goals For (GF)": "goals_for",
        "Goals Against (GA)": "goals_against",
        "+ / -": "plus_minus",
    }

    page_url = "pages/forms/"

    try:
        # nothing else would continue if main page fails, hence directly raising exceptions here
        page_url_to_scrape = requests.get(base_url + page_url)

        soup = BeautifulSoup(
            page_url_to_scrape.text,
            "html5lib"
        )

        # not hardcoding the url for pagination
        # getting all the paginated urls from the site
        paginated_urls = list(
            set(
                a["href"] for a in soup.find(
                    "ul",
                    attrs={"class": "pagination"}
                ).find_all(  # type: ignore
                    "a",
                    href=True
                )
            )
        )

        # iterating through every url from pagination
        for page_url in paginated_urls:

            hockey_single_scraper(page_url, title_mapping)

    except HTTPError as e:
        logging.error(f"Error in making request : {e.errno}")

    except Exception as e:
        logging.error(f"An error occurred : {e}")


@shared_task
def oscar_scraper():

    page_url = "/pages/ajax-javascript/"

    title_mapping = {
        "title": "title",
        "year": "year",
        "awards": "awards",
        "nominations": "nominations",
        "best_picture": "best_picture",
    }

    try:

        # nothing else would continue if main page fails, hence directly raising exceptions here
        page_url_to_scrape = requests.get(base_url + page_url)

        soup = BeautifulSoup(
            page_url_to_scrape.text,
            "html5lib"
        )

        # not hardcoding the url for pagination
        paginated_years = [
            int(i.text) for i in soup.findAll(
                "a",
                attrs={"class": "year-link"},
                # href=True,
            )
        ]

        # iterating through every urls from pagination
        for year in paginated_years:

            single_oscar_page_scraper(page_url, year)            

    except HTTPError as e:
        logging.error(f"Error in making request : {e.errno}")

    except Exception as e:
        logging.error(f"An error occurred : {e}")


oscar_scraper.delay()
hockey_scraper.delay()
