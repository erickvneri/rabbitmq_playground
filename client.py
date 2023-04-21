from datetime import datetime
from uuid import uuid1

# locals
from connection import connection
from message import Message

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
    message = Message(
        created_at=datetime.now(),
        reference_id=uuid1(),
        data={
            "action": "add",
            "target": "entity",
            "entity": "table_a",
            "reporter": uuid1(),
            "data": [
                {"id": uuid1(), "name": "sample_entity_0"},
                {"id": uuid1(), "name": "sample_entity_1"},
                {"id": uuid1(), "name": "sample_entity_2"},
                {"id": uuid1(), "name": "sample_entity_3"},
                {"id": uuid1(), "name": "sample_entity_4"},
                {"id": uuid1(), "name": "sample_entity_5"},
            ],
        },
    )

    print(f"publishing message at {TOPIC['private']}...")
    channel.basic_publish(
        exchange=TOPIC["private"], routing_key="", body=message.encode()
    )

    init_server(channel)


if __name__ == "__main__":
    main()
