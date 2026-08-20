import pika, os, json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "factoring_user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "factoring_pass")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "pricing_queue")

def get_latest_pricing():
    """Recupera el último mensaje de la cola pricing_queue"""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    method_frame, header_frame, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    connection.close()

    if body:
        return json.loads(body)
    else:
        return {"error": "No hay mensajes en la cola"}
