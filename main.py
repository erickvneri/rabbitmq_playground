import pika
import time
import logging
import json
from uuid import uuid1
from datetime import datetime

## first run docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


class Message:
    """
    Example:

        Message(
            data=dict(
                mc_id=uuid1(),
                boutique_id=uuid1(),
                action="add",
                target="sales_associate",
                data=[
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                    dict(uuid=str(uuid1()), first_name="John", last_name="Doe"),
                ],
            )
        )
    """

    def __init__(self, **kwargs) -> "Message":
        self.created_at = str(datetime.now())
        self.reference_id = str(uuid1())

        # Dinamically set message custom attributes
        [setattr(self, k, v) for k, v in kwargs.items()]

    @property
    def encode(self):
        stringify = json.dumps(self.__dict__)
        return stringify.encode()
