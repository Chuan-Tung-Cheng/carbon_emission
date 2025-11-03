import csv
import pymongo as mon
import os
import glob
from dotenv import load_dotenv

"""Upload "csv files" into mongodb"""

"""0. upload env variables"""
load_dotenv() # MUST

USERNAME=os.getenv("MONGO_USERNAME")
PASSWORD=os.getenv("MONGO_PASSWORD")
HOST=os.getenv("MONGO_HOST")
PORT=os.getenv("MONGO_PORT")
AUTH_DB=os.getenv("MONGO_AUTH_DB")

BATCH_SIZE = 30 # upload in a batch of 30


def connect_to_mongodb():
    """1. connect to MongoDB"""
    connection_string = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource={AUTH_DB}"
    try:
        connection = mon.MongoClient(connection_string) # connecting
        print(connection.server_info())
        print("Authentication successful")
        return connection

    except Exception as e:
        print(f"Authentication failed: {e}")
        return e

def find_csv_file_path(root_dir):
    """2. find csv path"""
    csv_files = f"/Users/cct/Downloads/{root_dir}/"
    return csv_files

def upload_to_mongodb(connection, file_path):
    """3. upload data to mongodb"""

    # connect to database
    db = connection["mydatabase"]
    # connect to selected table
    collection = db["test"]

    batch_to_insert = []
    file_amount = 0
    total_amount = 0

    for csv_file_path in glob.glob(os.path.join(file_path, "*.csv")):
        file_amount += 1
        with open(csv_file_path, mode="r", encoding="utf-8") as f:
            # DictReader
            reader = csv.DictReader(f)
            for row in reader:
                batch_to_insert.append(row)

                # limit the amount of one-time uploading
                if len(batch_to_insert) >= BATCH_SIZE:
                    collection.insert_many(batch_to_insert)
                    total_amount += len(batch_to_insert)
                    batch_to_insert.clear()

    if batch_to_insert:
        collection.insert_many(batch_to_insert)
        total_amount += len(batch_to_insert)

    print(f"""
    {file_amount} files have been uploaded
    {total_amount} data has been uploaded
    """)

def close_connection(db_connection):
    """4. close mongodb"""
    print("All data has been uploaded and mongodb is closed")
    db_connection.close()


if __name__ == "__main__":
    """1. connect to MongoDB"""
    # get connected object, called connection
    client = connect_to_mongodb()
    """2. find csv path"""
    # input files' root directory
    pr_root_dir = input("root dir: ")
    csv_path = find_csv_file_path(pr_root_dir)
    """3. upload data to mongodb"""
    upload_to_mongodb(client, csv_path)
    """4. close mongodb"""
    close_connection(client)
