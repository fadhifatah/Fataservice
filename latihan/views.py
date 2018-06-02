import base64
import pika
import json

import requests
from django.http import JsonResponse
from django.shortcuts import render

from latihan.constants import Credentials
from latihan.forms import DocumentForm


# Create your views here.
def index(request):
    # Handle file upload as SERVER #1 21018
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            client_id = Credentials.client_id
            client_secret = Credentials.client_secret

            file = request.FILES['file']
            file_name = file.name
            file_type = file.content_type
            file_size = file.size
            file_base64 = base64.b64encode(file.read())

            credentials = pika.PlainCredentials('1406571842', '1406571842')
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='152.118.148.103',
                port=5672,
                virtual_host='/1406571842',
                credentials=credentials,
                heartbeat=10
            ))
            channel = connection.channel()

            body = json.dump({
                'oauth': {
                    'username': username,
                    'password': password,
                    'client_id': client_id,
                    'client_secret': client_secret
                },
                'file': {
                    'name': file_name,
                    'type': file_type,
                    'size': file_size,
                    'base64': file_base64
                }
            })

            channel.exchange_declare(
                exchange='orchestration',
                exchange_type='fanout'
            )

            channel.basic_publish(
                exchange='orchestration',
                routing_key='', body=body
            )

            # Redirect to the document list after POST
            return render(
                request,
                'file_zipping.html',
                {'flag': True}
            )
    else:
        form = DocumentForm()  # A empty, unbound form

    # Render list page with the documents and the form
    return render(
        request,
        'file_zipping.html',
        {'form': form, 'flag': False, 'hidden': 'hidden'}
    )


def compression(request):
    # File Compression as SERVER #3 22018
    if request.method == "POST":
        try:
            auth_header = str(request.META['HTTP_AUTHORIZATION'])
            token = auth_header[7:]
        except:
            return JsonResponse({'message': 'Access Denied!'})

        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except:
            return JsonResponse({'message': 'JSON Error'})

        access_token = body['access_token']
        file_name = body['file']['name']
        file_type = body['file']['type']
        file_size = body['file']['size']
        file_base64 = body['file']['base64']

        credentials = pika.PlainCredentials('1406571842', '1406571842')
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='152.118.148.103',
            port=5672,
            virtual_host='/1406571842',
            credentials=credentials,
            heartbeat=10
        ))
        channel = connection.channel()

        body = json.dump({
            'access_token': access_token,
            'file': {
                'name': file_name,
                'type': file_type,
                'size': file_size,
                'base64': file_base64
            }
        })

        channel.exchange_declare(
            exchange='compression_start',
            exchange_type='fanout'
        )

        channel.basic_publish(
            exchange='compression_start',
            routing_key='', body=body
        )

        return JsonResponse({'message': 'OK Success!'})
