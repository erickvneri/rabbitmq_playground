from connection import connection

TOPIC = dict(private="changelog.private", public="changelog.public")


def init_server(channel):
    channel.exchange_declare(exchange=TOPIC["public"], exchange_type="fanout")
    queue = channel.queue_declare(queue="", exclusive=True)
    channel.queue_bind(exchange=TOPIC["public"], queue=queue.method.queue)

    # open channel
    channel.basic_consume(
        queue=queue.method.queue,
        on_message_callback=lambda _a, _b_, _c, message: print(
            f"handled public message propagation: {message}"
        ),
        auto_ack=True,
    )

    print(f"listening on public topic: {TOPIC['public']}")
    channel.start_consuming()


def main():
    client = connection()
    channel = client.channel()

    channel.exchange_declare(exchange=TOPIC["private"], exchange_type="fanout")
    message = "Hello world!"

    print(f"publishing message at {TOPIC['private']}...")
    channel.basic_publish(exchange=TOPIC["private"], routing_key="", body=message)

    init_server(channel)


if __name__ == "__main__":
    main()
