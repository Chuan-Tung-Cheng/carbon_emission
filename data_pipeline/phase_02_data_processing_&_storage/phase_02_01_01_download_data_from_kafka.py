import json, os, sys

from confluent_kafka import Consumer, KafkaException, KafkaError
from dotenv import load_dotenv

load_dotenv()
GROUP_ID = os.getenv("GROUP_ID")
TOPIC_NAME = os.getenv("TOPIC_NAME")
BATCH_SIZE = 2000

# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data:
        return data.decode('utf-8')
    else:
        return None


# 當發生commit時被呼叫
def print_commit_result(err, partitions):
    if err:
        print('# Failed to commit offsets: %s: %s' % (err, partitions))
    else:
        for p in partitions:
            print(
                'Committed offsets: topic: {}, partition: {}. offset: {}'.format(
                    p.topic, p.partition, p.offset
                )
            )

def consumer_raw_data_to_mongodb():
    """
    retrieve data from kafka topic and insert into mongodb
    return: list of dict (data to insert)
    """
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': 'localhost:9092',  # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': GROUP_ID,  # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'earliest',  # 是否從這個ConsumerGroup尚未讀取的partition/offset開始讀
        'enable.auto.commit': False,  # 是否啟動自動commit
        'on_commit': print_commit_result,  # 設定接收commit訊息的callback函數
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Consumer的實例
    consumer = Consumer(props)
    # 步驟3. 指定想要訂閱訊息的topic名稱
    topic_name = TOPIC_NAME
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topic_name])

    # 步驟5. 持續的拉取Kafka有進來的訊息
    try:
        while True:
            # build a container to save consume data
            insert_buffer = []

            # 請求Kafka把新的訊息吐出來
            records = consumer.consume(num_messages=BATCH_SIZE, timeout=1.0)  # 批次讀取
            if not records:
                continue

            for record in records:
                # 檢查是否有錯誤
                if record is None:
                    continue
                if record.error():
                    # Error or event
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            '%% {} [{}] reached end at offset {}\n'.format(
                                record.topic(),
                                record.partition(),
                                record.offset()
                            )
                        )

                    else:
                        raise KafkaException(record.error())
                    continue

                # ** 在這裡進行商業邏輯與訊息處理 **
                # 取出相關的metadata
                topic = record.topic()
                partition = record.partition()
                offset = record.offset()
                # timestamp = record.timestamp()
                # 取出msgKey與msgValue
                # msgKey = try_decode_utf8(record.key())

                try:
                    msg_value = try_decode_utf8(record.value())
                    document = json.loads(msg_value)
                except Exception as e:
                    print(f"Error : {e}")
                    continue

                document["_id"] = f"{topic}-{partition}-{offset}"
                document["_kafka_meta"] = {
                    "topic": topic,
                    "partition": partition,
                    "offset": offset
                }

                insert_buffer.append(document)
                if len(insert_buffer) >= BATCH_SIZE:
                    tem_buffer = insert_buffer
                    consumer.commit(record)  # 非同步的commit
                    return tem_buffer

            return insert_buffer



    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(str(e))

    finally:
        # 步驟6.關掉Consumer實例的連線
        consumer.close()
