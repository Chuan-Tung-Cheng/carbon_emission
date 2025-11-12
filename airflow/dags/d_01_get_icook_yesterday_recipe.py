from src.pipeline.extract.scrapy_app_icook import IcookDailySpider
#
# from airflow import DAG
# from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta



def run_icook_spider():
    spider = IcookDailySpider(keyword="latest")
    spider.run()

run_icook_spider()

# # Default arguments for the DAG
# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'email': ['chengreentea0813@gmail.com'],
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,  #
#     'retry_delay': timedelta(minutes=5),  #
# }
#
# # Define the DAG
# dag = DAG(
#     'd_01_get_icook_yesterday_recipe',  #
#     default_args=default_args,
#     description='Python operators',  #
#     schedule_interval="*/10 * * * *",  #
#     start_date=datetime(2025, 11, 13),
#     catchup=False,
#     tags=["scrapy", "icook"]
# )
#
# # Define the tasks
# task1_obj = PythonOperator(
#     task_id='run_icook_scrapy',
#     python_callable=run_icook_spider,
#     dag=dag,
# )
#
#
# # Task dependencies
# task1_obj

