import scrapy

from .icook_recept_parser import parse_icook_recipe
from urllib.parse import  quote

class IcookSpider(scrapy.Spider):
    name = "icook"
    allowed_domains = ["icook.tw"]
    start_urls = ["https://icook.tw/search/%e7%82%92%e9%ab%98%e9%ba%97%e8%8f%9c%e4%b9%be/"]

    def start_requests(self):
        """
        replace start_url, make users available to mine data in category page
        """
        # users can enter keyword by -a keyword="number", the number can refer to the category page: https://icook.tw/categories
        search_keyword = getattr(self, "keyword", None)
        # convert the keyword into the code that can be used for url
        encoded_keyword = quote(search_keyword)
        # concat
        url = f"https://icook.tw/categories/{encoded_keyword}/"
        # generate the first url that a spider requests
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # find the all recipt links in target url
        recipe_links = response.xpath('//a[@class="browse-recipe-link"]/@href').getall()
        for link in recipe_links:
            # response.follow 會自動處理相對路徑 (例如 /recipes/480984)
            # 並要求 Scrapy 抓取這個連結，完成後呼叫 parse_recipe_detail 函式
            yield response.follow(link, callback=self.parse_recipe_detail)

        # next page
        next_page_link = response.xpath('//a[@rel="next nofollow"]/@href').get()
        if next_page_link is not None:
            # 找到下一頁，要求 Scrapy 抓取它，並用「同一個 parse」函式處理
            yield response.follow(next_page_link, callback=self.parse)

    def parse_recipe_detail(self, response):
        # 呼叫 BS4 解析器函式
        #
        # parse_icook_recipe 是一個「產生器 (Generator)」
        # 它會 yield (產出) 一個或多個 Food 物件
        items_generator = parse_icook_recipe(response)

        #  迭代產生器，並 yield 每一筆資料給 Scrapy
        for food_object in items_generator:
            # 您的 food_object 是 Food Class
            # 我們將它轉為 dict，Scrapy 的 CSV/JSON
            # 導出器就能完美處理
            yield food_object.__dict__




