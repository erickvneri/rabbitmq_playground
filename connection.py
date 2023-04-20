import pika


def connection(host: str = "localhost"):
    conn = None
    opts = pika.ConnectionParameters(host)
    conn = pika.BlockingConnection(opts)
    return conn
