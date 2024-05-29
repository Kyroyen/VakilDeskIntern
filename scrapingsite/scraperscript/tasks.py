from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, JSONDecodeError
import logging
from time import sleep
from celery import shared_task

from .request_logmaker import make_request
from .models import OscarFilms, HockeyTeams
from .heading_map import heading_mapper

LOG_FILENAME = "scraping_logging.log"
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

            curr_pageurl = base_url + page_url

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
                continue

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

            # hockey_team_bulk = [

            # ]
            # print(bulk[0])
            HockeyTeams.objects.bulk_create(
                HockeyTeams(
                    **team
                ) for team in bulk
            )

            sleep(5)

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

                sleep(5)
                break

            except JSONDecodeError:
                logging.error(
                    f"Failed to parse JSON response for {page_url} : params {params}")

    except HTTPError as e:
        logging.error(f"Error in making request : {e.errno}")

    except Exception as e:
        logging.error(f"An error occurred : {e}")


oscar_scraper.delay()
hockey_scraper.delay()
