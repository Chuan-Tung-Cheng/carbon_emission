"""
Goal: Collect all links in searching the specific recept
Name: Albert
"""
import requests

import icook_recept_crawler as ic

def collect_next_page_links():
    """
    This function will collect all next page links in searching the specific recept
    """

    # set target url
    target = "https://icook.tw/search/%E7%87%89%E7%89%9B%E8%82%89/%E7%89%9B/"

    # request target url
    response = requests.get(target, headers=ic.HEADERS)

    try:
        response.raise_for_status() # should be 200
        print("Request succeeds!")
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
    all_next_pages = collect_next_page_links()
    collect_recept_links(all_next_pages)

if __name__ == '__main__':
    main()
