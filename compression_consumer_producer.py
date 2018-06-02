import base64
import json
import os
import time
import types
import zipfile
from functools import partial

import pika

# Message Consumer 22018
access_token = ""
extention = "bzip2"
progress_byte = 0

credentials = pika.PlainCredentials('1406571842', '1406571842')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='152.118.148.103',
    port=5672,
    virtual_host='/1406571842',
    credentials=credentials,
    heartbeat=10
))
channel = connection.channel()

channel.exchange_declare(
    exchange='compression_start',
    durable=True,
    exchange_type='fanout'
)

queue = channel.queue_declare(
    durable=True,
    exclusive=True
)

queue_name = queue.method.queue
channel.queue_bind(
    exchange='compression_start',
    queue=queue_name
)


def progress(size, write, self, buff):
    global progress_byte
    progress_byte += 1024 * 8
    progress_bar = 100 * progress_byte / size

    body = json.dump({

    })
    pass


def start_compress(body):
    try:
        body_unicode = body.decode('utf-8')
        json_body = json.loads(body_unicode)
    except:
        return "JSON Error"

    access_token = json_body['access_token']
    file_name = json_body['file']['name']
    file_type = json_body['file']['type']
    file_size = json_body['file']['size']
    file_base64 = json_body['file']['base64']

    file = base64.b64decode(file_base64)
    the_file = file_name + "." + file_type
    with open(the_file, 'wb') as f:
        f.write(file)
        f.close()

    file_output = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + the_file + "." + extention

    global progress_bytes
    progress_bytes = 0
    with zipfile.ZipFile(file_output, 'w', compression=zipfile.ZIP_BZIP2) as bzip2:
        # Track the progress
        bzip2.fp.write = types.MethodType(
            partial(
                progress,
                os.path.getsize(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + the_file),
                bzip2.fp.write
            ),
            bzip2.fp
        )

        bzip2.write(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + the_file)
        pass


def callback(ch, method, properties, body):
    # Start compress the file
    start_compress(body)

    time.sleep(5)


channel2 = connection.channel()
channel2.exchange_declare(exchange='compression')

channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)
channel.start_consuming()
