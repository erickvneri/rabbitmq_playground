import time
from connection import connection

TOPIC = dict(private="changelog.private", public="changelog.public")


def propagate_message(*msg):
    channel, _b, _c, message = msg
    print(f"received message to private: {message}")

    channel.exchange_declare(exchange=TOPIC["public"], exchange_type="fanout")

    print(f"propagating updates at public: {TOPIC['public']}...")
    time.sleep(1)
    channel.basic_publish(exchange=TOPIC["public"], routing_key="", body=message)


def main():
    server = connection()
    channel = server.channel()

    channel.exchange_declare(exchange=TOPIC["private"], exchange_type="fanout")
    queue = channel.queue_declare(queue="", exclusive=True)
    channel.queue_bind(exchange=TOPIC["private"], queue=queue.method.queue)

    # open channel
    channel.basic_consume(
        queue=queue.method.queue,
        on_message_callback=propagate_message,
        auto_ack=True,
    )

    print(f"listening on private topic: {TOPIC['private']}")
    channel.start_consuming()


if __name__ == "__main__":
    main()
