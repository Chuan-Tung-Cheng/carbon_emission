import os
import sys
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
from pathlib import Path

# from icook_crawler.spiders.icook_category_usage import IcookCategorySpider

PROJECT_ROOT = Path(__file__).resolve().parent
# OUTPUT_DIR = PROJECT_ROOT / 'output_csvs'

# keyword
# SEARCH_KEYWORDS_LIST = [
#         "54", # 家常食材
#         "58", # 異國料理
#         "19", # 飲料冰品
#         "405", # 寶寶兒童
#         "437", # 快速省錢
#         "460", # 果醬醬料
#         "59", # 烹調器具
#         "352", # 功效
#         "31", # 季節節慶
######## general ingredients ########
#         "592", # 家常美味
#         "593", # 烘焙專區
#         "608", # 當季食材
#         "395", # 瓜果
#         "393", # 根莖
#         "394", # 葉菜
#         "660", # 豆類蔬菜
#         "390", # 菌藻、菇類
#         "2", # 五穀雜糧
#         "6", # 水果
#         "301", # 蛋
#         "302", # 豆製品
#         "3", # 海鮮
#         "40", # 豬肉
#         "38", # 雞肉
#         "39", # 牛肉
#         "41", # 羊肉
#         "43", # 鴨肉

def main(search_from_outside):

    # 3. 取得專案設定
    # 此作法為效能考量，只需進入硬碟讀取一次，其餘用複製的
    # base_settings = get_project_settings()

    # OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    os.chdir(PROJECT_ROOT)

    # 迴圈排程所有任務
    for keyword in search_from_outside:
        print(f"排程任務: {keyword}")

        command = (
            f"scrapy crawl icook_category_usage "
            f"-a keyword={keyword} "
            f"-O output_csvs/icook_{keyword}.csv"
        )

        print(f"執行{command}中")

        os.system(command)

        print(f"排程任務完成: {keyword}")

        # process_settings = base_settings.copy()

        # output_filepath = OUTPUT_DIR / f"icook_{keyword}.csv"

        # process_settings.set('FEEDS', {
        #     str(output_filepath): {
        #         'format': 'csv',
        #         'encoding': 'utf8',
        #         'overwrite': True,
        #     }
        # })

        # Scrapy 會為每個關鍵字建立一個「獨立的」Spider 實例
        # 5. 建立 CrawlerProcess
        # process = CrawlerProcess(process_settings)

        # 迴圈呼叫 process.crawl()
        # process.crawl(IcookCategorySpider, keyword=keyword)

        # 6. 【重要】在迴圈「結束後」，才呼叫 start() 一次
        #    Scrapy 引擎會啟動，並「同時」執行您剛剛排程的 4 個爬蟲
        # process.start()

    print("所有爬取任務已完成！")


if __name__ == "__main__":
    search = sys.argv[1].split(" ")
    main(search)