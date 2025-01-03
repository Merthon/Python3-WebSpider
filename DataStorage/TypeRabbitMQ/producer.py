# RabbitMQ基本使用
import pika

# 创建连接
QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 创建队列
channel.queue_declare(queue=QUEUE_NAME)

# 发送消息
channel.basic_publish(exchange='',
                      routing_key=QUEUE_NAME,
                      body='Hello, World!')