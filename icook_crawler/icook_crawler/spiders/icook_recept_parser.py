"""
Goal: Parse recipes in iCook
Name: Albert
"""

import re

from datetime import datetime
from bs4 import BeautifulSoup


# Constant

DATE_REGEX= "%Y/%m/%d"
MAIN = "main ingredients"
SAUCE = "sauce"

COMPILED_PATTERN = re.compile(r"(\d+\.?\d*|\.\d+|\d+/\d+)(.*)")
"""
\d+\.?\d* -> 1.5
\.\d+ ->  decimal without, 0.5 
\d+/\d+ -> fraction, 1/2
.* -> for any strings
"""


class Food:
    """
    This class is to record how many things that need to be stored
    """
    def __init__(self,
                 recept_id,
                 recipe_name, # str
                 author, # str
                 good, # int
                 recipe_url, # str
                 browsing_num, # int only in icook
                 people,  # int,
                 cooking_time, # int
                 recept_type, # str
                 ingredients, # list
                 quantity,  # int
                 unit, # str
                 recipe_upload_date, # datetime
                 crawl_datetime, # datetime
                 ):

        self.recept_id = recept_id # pk
        self.recipe_name = recipe_name # recipe name
        self.author = author  # recipe creator
        self.good = good  # recipe reputation
        self.recipe_url = recipe_url # recipe url
        self.browsing_num = browsing_num # browsing_num
        self.people = people  # the number of people
        self.cooking_time = cooking_time  # cooking time
        self.recept_type = recept_type
        self.ingredients = ingredients # cooking ingredients
        self.quantity = quantity
        self.unit = unit
        self.recipe_upload_date = recipe_upload_date  # recipe_upload_date
        self.crawl_datetime = crawl_datetime


    def __hash__(self):
        return hash(self.recipe_url) + hash(self.browsing_num) + hash(self.author) + hash(self.good)

    def __eq__(self, other):
        return (self.recipe_url == other.recipe_url
                and self.browsing_num == other.browsing_num
                and self.good == other.good)

    @staticmethod
    def separate_num_unit(string):
        """
        separate number and unit
        param string: Quantity with unit
        return: num: float, unit: string
        """
        match = re.fullmatch(COMPILED_PATTERN, string)
        if match:
            # extract the unit part
            unit_part = match.group(2).strip().replace(" ", "")
            try:
                # extract the num part
                num_part = float(match.group(1).strip().replace(" ", ""))
                return num_part, unit_part

            except ValueError: # for fraction scenario
                # extract the num part
                fractions = match.group(1).strip().split("/")
                numerator, denominator = map(int, fractions)
                num_part = numerator / denominator
                return num_part, unit_part
        else:
            return None, string


def parse_icook_recipe(scrapy_response):
    """
    This function PARSES the icook recipe page from a Scrapy response.
    It is now a GENERATOR (yields data).

    param: scrapy_response (This is Scrapy's response object, NOT a URL string)
    """
    ### define all values ###
    recept_id = None
    recipe_name = str
    author = str
    recipe_url = scrapy_response.url
    upload_date = datetime
    browsing = None
    good = None
    ppl = None # means people
    time_item = None
    recept_type = None
    quantity = 0
    unit = None
    crawl_datetime = datetime.now()

    # Parse HTML
    soup = BeautifulSoup(scrapy_response.text, "lxml")

    #### find ID ####
    recept_id = recipe_url.split("/")[-1]
    #### find ID end ####

    #### find author ####
    author = soup.find("a", attrs={"class": "author-name-link"})
    if author: # if author exist
        author = author.text.strip()
    #### find author end ####

    #### find recipe name ####
    recipe_name = soup.find("h1", attrs={"id": "recipe-name"})
    if recipe_name:
        recipe_name = recipe_name.text.strip()
    #### find recipe name end ####

    #### find upload date & browsing  ####
    upload_browsing = soup.find("div", attrs={"class": "recipe-detail-metas"})
    if upload_browsing:
        # find upload date
        # strip the right, left, inner blank
        upload_date = upload_browsing.find("time").text.strip().replace(" ", "")[:-2]
        # regex datetime
        upload_date = datetime.date(datetime.strptime(upload_date, DATE_REGEX))
        # find browsing
        browsing = upload_browsing.find("div").text.strip().replace(" ", "")[:-2]
        if "萬" in browsing:
            browsing = browsing[:-1]
            browsing = int(browsing.replace(".", "")) * int((10000/10)) # unit is 10000 but remove the point
        elif len(browsing) > 3:
            browsing = int(browsing.replace(",", ""))
        else:
            browsing = int(browsing)
    #### find upload  date& browsing end ####

    #### find good reputation ####
    """need to consider good reputation will increase or decrease"""
    good = soup.find("span", attrs={"class": "stat-content bold"}).text.strip()
    if good:
        if "萬" in good:
            good = good[:-1]
            good = int(good.replace(".", "")) * int((10000 / 10))  # unit is 10000 but remove the point
        elif len(good) > 3:
            good = int(good.replace(",", ""))
        else:
            good = int(good)
    #### find good reputation end ####

    #### find people ####
    ppl = soup.find("div", attrs={"class": "servings"})
    if ppl:
        ppl = int(ppl.find("span", attrs={"class": "num"}).text.strip())
    #### find people end ####

    #### find cooking time ####
    time = soup.find("div", attrs={"class": "time-info info-block"})
    if time:
        time_item = int(time.find("span", attrs={"class": "num"}).text.strip())
    #### find cooking time end ####

    ### find main ingredients ####
    r_ings = soup.find_all("div", attrs={"class": "group group-0"})
    if r_ings:
        for r_ing in r_ings:
            ings = r_ing.find_all("li", attrs={"class": "ingredient"}) # list
            for ing in ings:
                ing_name = ing.find("a", attrs={"class": "ingredient-search"}).text.strip()
                ing_num = ing.find("div", attrs={"class": "ingredient-unit"}).text.strip()
                # separate the num and unit
                ing_num, ing_unit = Food.separate_num_unit(ing_num)
                # collect all info into an object, Food
                food_data = Food(
                                recept_id=recept_id,
                                recipe_name=recipe_name,
                                author=author,
                                good=good,
                                recipe_url=recipe_url,
                                browsing_num=browsing,
                                people=ppl,
                                cooking_time=time_item,
                                recept_type=MAIN,
                                ingredients=ing_name,
                                quantity=ing_num,
                                unit=ing_unit,
                                recipe_upload_date=upload_date,
                                crawl_datetime=crawl_datetime,
                                )
                yield food_data
    #### find main ingredients end ####

    #### find sauce ingredients ####
    r_sauces = soup.find_all("div", attrs={"class": "group group-1"})
    if r_sauces:
        for r_sauce in r_sauces:
            sauces = r_sauce.find_all("li", attrs={"class": "ingredient"})
            for sauce in sauces:
                sauce_name = sauce.find("a", attrs={"class": "ingredient-search"}).text.strip()
                sauce_num = sauce.find("div", attrs={"class": "ingredient-unit"}).text.strip()
                # separate the num and unit
                sauce_num, sauce_unit = Food.separate_num_unit(sauce_num)
                # collect all info into an object, Food
                food_data = Food(
                    recept_id=recept_id,
                    recipe_name=recipe_name,
                    author=author,
                    good=good,
                    recipe_url=recipe_url,
                    browsing_num=browsing,
                    people=ppl,
                    cooking_time=time_item,
                    recept_type=SAUCE,
                    ingredients=sauce_name,
                    quantity=sauce_num,
                    unit=sauce_unit,
                    recipe_upload_date=upload_date,
                    crawl_datetime=crawl_datetime,
                )
            yield food_data
    #### find sauce ingredients end ####
