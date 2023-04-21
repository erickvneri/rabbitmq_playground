# MIT License
#
# Copyright (c) 2023 erickvneri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from json import dumps
from uuid import uuid1
from datetime import datetime

## first run docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management


class Message:
    """
    Example:

        message = Message(
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

        send_message(message.encode())
    """

    def __init__(self, **kwargs) -> "Message":
        self.created_at = str(datetime.now())
        self.reference_id = str(uuid1())

        # Dinamically set message custom attributes
        [setattr(self, k, v) for k, v in kwargs.items()]

    def encode(self):
        parsed = self.remap(self.__dict__)
        parsed = dumps(parsed)
        return parsed.encode()

    def remap(self, target):
        primitives = [bool, int, str, float]

        if type(target) in primitives:
            return target

        for k, v in target.items():
            if type(v) is dict:
                v = self.remap(v)
                target[k] = self.remap(v)
            elif type(v) is list:
                target[k] = [self.remap(item) for item in v]
            elif type(v) is object:
                target[k] = self.remap(v.__dict__)
            elif type(v) in primitives:
                target[k] = v
            else:
                target[k] = str(v)
        return target
