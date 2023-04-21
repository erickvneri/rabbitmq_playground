### Set up

- Initialize virtual enviroment

        python -m pip install virtualenv
        python -m virtualenv .env
        . .env/bin/activate
        python -m pip install -r pika

- Initialize RabbitMQ locally

        docker run -it \
        --rm --name rabbitmq \
        -p 5672:5672 \
        -p 15672:15672 \
        rabbitmq:3.11-management

- Initialize server

        python server.py

- Initialize client in other terminals _(as many as needed)_

        . env/bin/activate
        python client.py
