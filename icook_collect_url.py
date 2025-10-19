"""
Goal: Collect all links in searching the specific recept
Name: Albert
"""
import requests
from bs4 import BeautifulSoup

import icook_recept_crawler as ic

def collect_page_links():
    """
    This function will collect all next page links in searching the specific recept
    """
    url_links = set()

    # set target url
    target = "https://icook.tw/search/%E7%87%89%E7%89%9B%E8%82%89/%E7%89%9B/"

    # request target url
    response = requests.get(target, headers=ic.HEADERS)
    # print(response)

    try:
        response.raise_for_status() # first page to go to the page
        print("Request succeeds!")
        soup = BeautifulSoup(response.text, "lxml")

        while True:
            # find present
            url_present = soup.find("a", attrs={"class": "pagination-tab-link--number page--current"})["href"]
            whole_present = ic.BASE_URL_ICOOK + url_present
            url_links.add(whole_present)

            cond = soup.find("a", attrs={"class": "pagination-tab-link--number page--current"})["href"]
            if not :
                break


    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        # If response error is 403, requests website with headers




    # find hrefs for next page

    # extract all hrefs
    # save them into a list
    # return the list
    return []


def collect_recept_links(url):
    """
    This function will collect all links in searching the specific recept
    param url : list, saving all the next-pages links
    """
    pass


def main():
    collect_page_links()
    # collect_recept_links

if __name__ == '__main__':
    main()
