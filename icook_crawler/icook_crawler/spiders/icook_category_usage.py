import scrapy

from .icook_recept_parser import parse_icook_recipe
from urllib.parse import  quote

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError


class IcookCategorySpider(scrapy.Spider):
    name = "icook_category_usage"
    allowed_domains = ["icook.tw"]

    # 1. 新增 __init__ 方法，接收 keyword 參數
    def __init__(self, keyword=None, *args, **kwargs):
        super(IcookCategorySpider, self).__init__(*args, **kwargs)  # Scrapy 標準初始化

        if keyword is None:
            raise ValueError("必須提供 'keyword' 參數 (例如 -a keyword=...)")

        self.search_keyword = keyword


    def start_requests(self):
        """
        replace start_url, make users available to mine data in category page
        """
        # users can enter keyword by -a keyword="number", the number can refer to the category page: https://icook.tw/categories
        # search_keyword = getattr(self, "keyword", None)
        # convert the keyword into the code that can be used for url
        encoded_keyword = quote(self.search_keyword)
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
            yield response.follow(
                link,
                callback=self.parse_recipe_detail,
                errback=self.handle_recipe_error,
                meta={
                    "max_retry_times": 3
                },
            )

        # next page
        next_page_link = response.xpath('//a[@rel="next nofollow"]/@href').get()
        if next_page_link is not None:
            # 找到下一頁，要求 Scrapy 抓取它，並用「同一個 parse」函式處理
            yield response.follow(
                next_page_link,
                callback=self.parse,
                errback=self.handle_recipe_error,
                meta = {
                "max_retry_times": 1
                },
            )

    def handle_recipe_error(self, failure):
        """
        This is a function will function only when errors happen
        """
        failed_request = failure.request

        # 檢查 failure 是哪種類型
        if failure.check(HttpError):
            # HTTP 錯誤 (4xx, 5xx)
            response = failure.value.response
            self.logger.error(
                f"HTTP Error {response.status} on URL: {response.url}"
            )

        elif failure.check(DNSLookupError):
            # DNS 錯誤
            self.logger.error(
                f"DNS Lookup Error on URL: {failed_request.url}"
            )

        elif failure.check(TimeoutError, TCPTimedOutError):
            # 超時錯誤
            self.logger.error(
                f"Timeout Error on URL: {failed_request.url}"
            )

        else:
            # 其他所有類型的錯誤 (例如連線被拒)
            self.logger.error(
                f"Unhandled Error {failure.value} on URL: {failed_request.url}"
            )

        # 【重點】
        # 我們只記錄 (log) 錯誤，但函式正常結束 (pass)
        # Scrapy 會認為這個錯誤「已被處理」，於是爬蟲會繼續爬取下一個任務。
        pass

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




