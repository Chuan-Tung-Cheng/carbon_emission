import phase_02_01_01_download_data_from_kafka as kafka
import utils.mongodb_connection as mondb





if __name__ == "__main__":
    client = mondb.connect_to_local_mongodb()
    # connect_to_online_mongodb()

    mondb.close_connection(client)