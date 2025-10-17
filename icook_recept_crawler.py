"""
Goal: Crawling the recipe
Name: Albert
"""
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import random

# Constant
BASE_URL_ICOOK = "https://icook.tw"

SEARCH_ICOOK = "/search/"

HEADERS = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

DATE_REGEX= "%Y/%m/%d"


class Food:
    """
    This class is to record how many things that need to be stored
    """
    def __init__(self,
                 recipe_name, # str
                 author, # str
                 recipe_url, # str
                 recipe_upload_date, # datetime
                 browsing_num, # int
                 good, # int
                 people, # int,
                 cooking_time, # int
                 main_ingredients, # list
                 sauce, # list
                 crawl_datetime, # datetime
                 ):

        self.recipe_name = recipe_name # recipe name
        self.author = author  # recipe creator
        self.recipe_url = recipe_url # recipe url
        self.recipe_upload_date = recipe_upload_date # recipe_upload_date
        self.browsing_num = browsing_num # browsing_num
        self.good = good # recipe reputation
        self.people = people # the number of people
        self.cooking_time = cooking_time # cooking time
        self.main_ingredients = main_ingredients # cooking ingredients
        self.sauce = sauce # cooking sauce
        self.crawl_datetime = crawl_datetime



    def __hash__(self):
        return hash(self.recipe_url) + hash(self.browsing_num) + hash(self.author) + hash(self.good)

    def __eq__(self, other):
        return (self.recipe_url == other.recipe_url
                and self.browsing_num == other.browsing_num
                and self.good == other.good)


def crawl_icook_recept():
    """
    This function is to crawl the icook recipe page
    """

    recipe_name = str
    author = str
    recipe_url = "https://icook.tw/recipes/482266"
    upload_date = datetime
    browsing = None
    good = None
    ppl = None # means people
    time_item = None
    ing_list = [] # collect the all of main ings
    sauce_list = [] # collect the all of source ings
    crawl_datetime = datetime.now()

    response = requests.get(recipe_url, headers=HEADERS) # HTML
    # print(response) # show 200 or not
    try:
        response.raise_for_status() # make sure to receive 200

        soup = BeautifulSoup(response.text, "lxml") # HTML
        # # print(soup)
        #### find author ####
        r_author = soup.find_all("a", attrs={"class": "author-name-link"})
        if r_author: # if author exist
            for author in r_author:
                author = author.text.strip()
                print(f"author: {author}", type(author))
        #### find author end ####

        #### find recipe name ####
        r_recipe_name = soup.find_all("h1", attrs={"id": "recipe-name"})
        if r_recipe_name:
            for recipe_name in r_recipe_name:
                recipe_name = recipe_name.text.strip()
                print(f"recipe: {recipe_name}", type(recipe_name))
        else:
            recipe_name = None
        #### find recipe name end ####

        #### find upload date & browsing  ####
        r_upload_browsing = soup.find_all("div", attrs={"class": "recipe-detail-metas"})
        # print(r_upload)
        if r_upload_browsing:
            for upload_browsing in r_upload_browsing:
                # find upload date
                # strip the right, left, inner blank
                upload_date = upload_browsing.find("time").text.strip().replace(" ", "")[:-2]
                # regex datetime
                upload_date = datetime.date(datetime.strptime(upload_date, DATE_REGEX))
                print(f"upload date: {upload_date}", type(upload_date))
                # find browsing
                browsing = int(upload_browsing.find("div").text.strip().replace(" ", "")[:-2])
                print(f"browsing num: {browsing}", type(browsing))
        #### find upload  date& browsing end ####

        #### find good reputation ####
        """need to consider good reputation will increase or decrease"""
        r_good = soup.find_all("span", attrs={"class": "stat-content bold"})
        if r_good:
            for good in r_good:
                good = int(good.text.strip())
                print(f"reputation: {good}", type(good))
        #### find good reputation end ####

        #### find people ####
        r_ppl = soup.find_all("div", attrs={"class": "servings"})
        if r_ppl:
            for ppl in r_ppl:
                ppl = int(ppl.find("span", attrs={"class": "num"}).text.strip())
                print(f"serving : {ppl}", type(ppl))
        #### find people end ####

        #### find cooking time ####
        r_time = soup.find_all("div", attrs={"class": "time-info info-block"})
        if r_time:
            for time_item in r_time:
                time_item = int(time_item.find("span", attrs={"class": "num"}).text.strip())
                print(f"time : {time_item}", type(time_item))
        #### find cooking time end ####

        #### find main ingredients ####
        r_ings = soup.find_all("div", attrs={"class": "group group-0"})
        # print(r_ings)
        if r_ings:
            for r_ing in r_ings:
                ings = r_ing.find_all("li", attrs={"class": "ingredient"})
                for ing in ings:
                    ing_name = ing.find("a", attrs={"class": "ingredient-search"}).text.strip()
                    ing_num = ing.find("div", attrs={"class": "ingredient-unit"}).text.strip()
                    print(f"main ingredient: {ing_name}", type(ing_name))
                    print(f"main ingredient num: {ing_num}", type(ing_num))
                    ing_list.append([ing_name, ing_num])
        #### find main ingredients end ####

        #### find sauce ingredients ####
        r_sauces = soup.find_all("div", attrs={"class": "group group-1"})
        # print(r_sauces)
        if r_sauces:
            for r_sauce in r_sauces:
                sauces = r_sauce.find_all("li", attrs={"class": "ingredient"})
                for sauce in sauces:
                    sauce_name = sauce.find("a", attrs={"class": "ingredient-search"}).text.strip()
                    sauce_num = sauce.find("div", attrs={"class": "ingredient-unit"}).text.strip()
                    print(f"sauce ingredient: {sauce_name}", type(sauce_name))
                    print(f"sauce ingredient num: {sauce_num}", type(sauce_num))
                    sauce_list = [sauce_name, sauce_num]
        #### find sauce ingredients end ####

        #### for converting the above info into pandas ####

        recept_data = Food(
            recipe_name=recipe_name,
            author=author,
            recipe_url=recipe_url,
            recipe_upload_date=upload_date,
            browsing_num=browsing,
            good=good,
            people=ppl,
            cooking_time=time_item,
            main_ingredients=ing_list,
            sauce=sauce_list,
            crawl_datetime=crawl_datetime,
        )

        columns = [
            "recipe_name",
            "author",
            "recipe_url",
            "recipe_upload_date",
            "browsing_num",
            "good",
            "people",
            "cooking_time",
            "main_ingredients",
            "sauce",
            "crawl_datetime",
        ]

        data = [
            [
                recept_data.recipe_name,
                recept_data.author,
                recept_data.recipe_url,
                recept_data.recipe_upload_date,
                recept_data.browsing_num,
                recept_data.good,
                recept_data.people,
                recept_data.cooking_time,
                recept_data.main_ingredients,
                recept_data.sauce,
                recept_data.crawl_datetime,

            ]
        ]

        recept_df = pd.DataFrame(data, columns=columns)
        print("=" * 60)
        print(recept_df)

        #### for converting the above info into pandas end ####

        sleeptime = random.randint(2,5)
        time.sleep(sleeptime)  # no need for one-time request

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")


def main():
    crawl_icook_recept()


if __name__ == '__main__':
    main()
