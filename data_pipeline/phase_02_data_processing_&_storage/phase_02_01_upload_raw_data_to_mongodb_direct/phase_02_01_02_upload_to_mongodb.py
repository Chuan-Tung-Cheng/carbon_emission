import os, sys, signal

import phase_02_01_01_download_data_from_kafka as kafka
import utils.mongodb_connection as mondb

DATABASE_1 = os.getenv("DATABASE_2")
COLLECTION_1 = os.getenv("COLLECTION_2")

GROUP_ID = os.getenv("GROUP_ID_OFFICIAL_3")
TOPIC_NAME = os.getenv("TOPIC_NAME_2")

running = True

def handle_shutdown(signum, frame):
    global running
    print(f"receive the signal number {signum}, now is going to cease this program...\n")
    print(f"closing consumer's connection ...\n")
    consumer.close()
    print(f"closing MongoDB's connection ...\n")
    mondb.close_connection(client)
    print(f"Done!\n")
    running = False


if __name__ == "__main__":
    """Here will receive the list of data from kafka and insert into mongodb"""
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    client = mondb.connect_to_local_mongodb()
    # connect_to_online_mongodb()
    db = client[DATABASE_1] # connect to targeted database
    collection = db[COLLECTION_1] # connect to targeted collection

    consumer = kafka.create_consumer(
        group_id=GROUP_ID,
        topic_name=TOPIC_NAME,
    )

    data_stream = kafka.consumer_raw_data_to_mongodb(consumer)

    try:
        print("start to retrieve data from kafka and load into mongodb")
        for data in data_stream:
            if not running :
                break
            try:
                collection.insert_many(data, ordered=False)
                sys.stderr.write(f"{len(data)} documents inserted into mongodb")
            except Exception as e:
                sys.stderr.write(f"{e}")
    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
