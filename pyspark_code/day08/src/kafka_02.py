from kafka import KafkaConsumer

if __name__ == '__main__':
    # 1- 创建消费者：默认从最新的地方开始消费
    consumer = KafkaConsumer(
        "test01",
        bootstrap_servers=['192.168.88.161:9092','192.168.88.162:9092']
    )

    # 2- 开始消费数据
    for msg in consumer:
        topic = msg.topic
        partition = msg.partition
        offset = msg.offset
        key = msg.key
        value = msg.value

        print(f"topic={topic}，partition={partition}，offset={offset}，key={key}，value={value.decode('UTF-8')}")