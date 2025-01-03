import pika

QUEUE_NAME = 'scrape'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)

# 获取数据
def callback(ch, method, properties, body):
    print(f"Get {body}")
channel.basic_consume(queue=QUEUE_NAME,
                      on_message_callback=callback, 
                      auto_ack=True)
channel.start_consuming()