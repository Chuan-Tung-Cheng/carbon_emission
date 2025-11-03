import csv, os
import utils.mongodb_connection as mongo

"""Here we will retrieve data from the MongoDB server and save it as a csv file."""




if __name__ == "__main__":
    """1. connect to MongoDB"""
    # get connected object, called connection
    client = mongo.connect_to_local_mongodb()
    """2. get data from MongoDB"""
    """3. save the data to csv file"""
    """4. close mongodb"""
    mongo.close_connection(client)


