from kafka import KafkaProducer

if __name__ == '__main__':
    # 1- 创建生产者
    producer = KafkaProducer(bootstrap_servers=['192.168.88.161:9092','192.168.88.162:9092'])

    # 2- 发送消息
    for i in range(10):
        # 要发送出去的消息内容
        msg = f"消息内容{i}"

        # 同步发送
        result = producer.send(topic="test01",value=msg.encode("UTF-8")).get()

        # 返回值内容输出
        topic = result.topic
        partition = result.partition
        offset = result.offset
        print(f"消息所在的Topic={topic}，partition={partition}，offset={offset}")