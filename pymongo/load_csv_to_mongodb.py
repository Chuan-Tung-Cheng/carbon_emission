import csv, glob, os, sys
import utils.mongodb_connection as mongo

"""Upload "csv files" into mongodb"""


BATCH_SIZE = 30 # upload in a batch of 30


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


if __name__ == "__main__":
    """1. connect to MongoDB"""
    # get connected object, called connection
    client = mongo.connect_to_local_mongodb()
    """2. find csv path"""
    # input files' root directory
    file_dir = sys.argv[1]
    """3. upload data to mongodb"""
    upload_to_mongodb(client, file_dir)
    """4. close mongodb"""
    mongo.close_connection(client)
