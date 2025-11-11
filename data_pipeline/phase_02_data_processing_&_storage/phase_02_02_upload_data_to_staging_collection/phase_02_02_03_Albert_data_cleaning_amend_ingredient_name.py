import os
import utils.mongodb_connection as mondb

DATABASE_1 = os.getenv("DATABASE_1")
COLLECTION_1 = os.getenv("COLLECTION_1_STAGE")

if __name__ == "__main__":
    #### connect to MongoDB
    client = mondb.connect_to_local_mongodb() # connect to MongoDB server
    db = client[DATABASE_1] # connect to targeted database
    collection = db[COLLECTION_1] # connect to targeted collection
    #### connect to MongoDB

    # loop:
        # get_target_data()
        # clean_data()
        # save_cleaned_data()









    # close
    mondb.close_connection(client)
