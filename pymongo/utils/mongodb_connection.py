import os
import pymongo as mon
from dotenv import load_dotenv

load_dotenv()
USERNAME=os.getenv("MONGO_USERNAME")
PASSWORD=os.getenv("MONGO_PASSWORD")
HOST=os.getenv("MONGO_HOST")
PORT=os.getenv("MONGO_PORT")
AUTH_DB=os.getenv("MONGO_AUTH_DB")


def connect_to_mongodb():
    """connect to MongoDB Server"""
    connection_string = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/?authSource={AUTH_DB}"
    try:
        connection = mon.MongoClient(connection_string) # connecting
        print(connection.server_info())
        print("connect successfully to MongoDB")
        return connection

    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def close_connection(db_connection):
    """ disconnect to MongoDB Server"""
    print("All data has been uploaded and MongoDB is disconnected")
    db_connection.close()