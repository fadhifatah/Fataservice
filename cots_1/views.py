import base64
import hashlib
import hmac

from django.core.signing import Signer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        header = request.META['HTTP_AUTHORIZATION']
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = models.User1.objects.get(username=str(username))
        except models.User1.DoesNotExist:
            return JsonResponse({'status': 201, 'message': 'Unauthorized'})

        secret_channel = user.secret
        body = '{"username":' + str(username) + ',"password":' + str(password) + '}'
        hashed = hmac.new(secret_channel.encode('utf-8'), body.encode('utf-8'), hashlib.md5).digest()
        signature = base64.b64encode(hashed)
        expected_header = 'Authorization: X-Service-Signature ' + str(signature)

        if header == expected_header:
            return JsonResponse({'status': 200, 'token': expected_header[35:]})
        else:
            return JsonResponse({'status': 201, 'message': 'Unauthorized'})
    return JsonResponse({'status': '500', 'message': 'Error'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        display_name = request.POST['displayName']

        signer = Signer('fataservice')
        secret_channel = signer.sign(str(username))

        try:
            models.User1.objects.get(username=str(username))
        except models.User1.DoesNotExist:
            models.User1.objects.create(username=str(username), password=str(password), display_name=str(display_name),
                                        secret=str(secret_channel))

            user_model = models.User1.objects.get(username=str(username))
            return JsonResponse({'status': 200, 'userId': user_model.id, 'displayName': str(display_name),
                                 'secret': str(secret_channel)})

        return JsonResponse({'status': 500, 'message': 'User already exist'})
    return JsonResponse({'status': '500', 'message': 'Error'})
