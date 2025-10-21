import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 1. 匯入您的 Spider
from icook_crawler.spiders.icook_category_usage import IcookCategorySpider


def main():
    # 2. 定義您所有想爬的關鍵字
    SEARCH_KEYWORDS_LIST = [
        "349", # 中式點心
        "54", # 家常食材
        "58", # 異國料理
        "19", # 飲料冰品
        "405", # 寶寶兒童
        "437", # 快速省錢
        "460", # 果醬醬料
        "59", # 烹調器具
        "352", # 功效
        "31", # 季節節慶
        "606", # 寵物料理
    ]

    # 3. 取得專案設定
    settings = get_project_settings()


    # 4. 建立 CrawlerProcess
    process = CrawlerProcess(settings)

    # 5. 【關鍵】迴圈排程所有任務
    for keyword in SEARCH_KEYWORDS_LIST:
        print(f"排程任務: {keyword}")

        # 迴圈呼叫 process.crawl()
        # Scrapy 會為每個關鍵字建立一個「獨立的」Spider 實例
        process.crawl(IcookCategorySpider, keyword=keyword)

        # 注意：我們在這裡「不要」設定 FEEDS
        # 因為這會導致所有爬蟲都寫入同一個檔案

    # 6. 【重要】在迴圈「結束後」，才呼叫 start() 一次
    #    Scrapy 引擎會啟動，並「同時」執行您剛剛排程的 4 個爬蟲
    process.start()

    print("所有爬取任務已完成！")


if __name__ == "__main__":
    main()