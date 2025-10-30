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

"""1. connect to MongoDB"""
connection_string = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource={AUTH_DB}"
try:
    client = mon.MongoClient(connection_string) # connecting
    client.server_info()
    print(client.server_info())
    print("Authentication successful")

except Exception as e:
    print("Authentication failed")
    raise e

db = client["mydatabase"] # connect to database
collection = db["test"]

"""2. find csv path"""
batch_to_insert = []
file_amount = 0
total_amount = 0
csv_files = f"/Users/cct/Downloads/young/"

"""3. ready to upload csv files"""
for csv_file_path in glob.glob(os.path.join(csv_files, "*.csv")):
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

"""4. upload data to mongodb"""
if batch_to_insert:
    collection.insert_many(batch_to_insert)
    total_amount += len(batch_to_insert)


"""5. close mongodb"""
print(f"""
{file_amount} files have been uploaded
{total_amount} data has been uploaded
""")
client.close()
print("All data has been uploaded and mongodb is closed")
