import json
import time

import pika
import requests

# Message Consumer 22018
access_token = ""

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
    exchange='orchestration',
    durable=True,
    exchange_type='fanout'
)

queue = channel.queue_declare(
    durable=True,
    exclusive=True
)

queue_name = queue.method.queue
channel.queue_bind(
    exchange='orchestration',
    queue=queue_name
)


def authentication(username, password, client_id, client_secret):
    # OAuth
    oauth_token = requests.post(
        'http://172.22.0.2/oauth/token',
        data={
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )

    if oauth_token.status_code == 200:
        global access_token
        access_token = oauth_token.json()['access_token']
    else:
        return "Access Denied! Username or Password is invalid."
    pass


def do_compress(file):
    file_name = file['name']
    file_type = file['type']
    file_size = file['size']
    file_base64 = file['base64']

    compression = requests.post(
        'http://host22018.proxy.infralabs.cs.ui.ac.id/uas/latihan/compression/',
        headers={
            'Authorization': 'Bearer ' + access_token
        },
        data={
            'file': {
                'name': file_name,
                'type': file_type,
                'size': file_size,
                'base64': file_base64
            }
        }
    )

    if compression.status_code == 200:
        pass
    else:
        return "Timeout!"


def generate_link(file):
    pass


def start_orchestration(body):
    try:
        body_unicode = body.decode('utf-8')
        json_body = json.loads(body_unicode)
    except:
        return "JSON Error"

    # OAuth 2.0
    username = json_body['oauth']['username']
    password = json_body['oauth']['password']
    client_id = json_body['oauth']['client_id']
    client_secret = json_body['oauth']['client_secret']

    authentication(username, password, client_id, client_secret)

    # File Compression
    file = json_body['file']
    do_compress(file)

    # Generate Link
    generate_link(file)

    pass


def callback(ch, method, properties, body):
    # Start orchestration as SERVER #2
    start_orchestration(body)
    time.sleep(5)


channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)
channel.start_consuming()
