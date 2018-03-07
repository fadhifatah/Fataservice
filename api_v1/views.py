from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_v1.models import User
from api_v1.constants import Constants
import requests


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong POST data'})

        oauth_token = requests.post(
            'http://172.22.0.2/oauth/token',
            data={
                'username': username,
                'password': password,
                'grant_type': 'password',
                'client_id': Constants.client_id,
                'client_secret': Constants.client_secret,
            }
        )

        if oauth_token.status_code == 200:
            access_token = oauth_token.json()['access_token']
            return JsonResponse({'status': 'ok', 'access_token': access_token})
        else:
            return JsonResponse({'status': 401, 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            auth_header = str(request.META['HTTP_AUTHORIZATION'])
            token = auth_header[7:]
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Header Error'})

        try:
            display_name = request.POST.get('displayName')
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong POST data'})

        oauth_resource = requests.get(
            'http://172.22.0.2/oauth/resource',
            headers={
                'Authorization': auth_header
            }
        )

        if oauth_resource.status_code == 200:
            return JsonResponse({'status': 'ok', 'access_token': token})
        return JsonResponse({'status': 401, 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


def get_users(request):
    if request.method == 'GET':

        users_dummy = User.objects.all()
        for dummy in users_dummy:
            username = dummy.username
            display_name = dummy.display_name

        return JsonResponse({'username': str(username), 'display_name': display_name})

    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


@csrf_exempt
def create_comment(request):
    return JsonResponse({})


def get_comment_by_id(request, comment_id):
    return JsonResponse({'comment_id': comment_id})


def get_comments(request):
    return JsonResponse({})


@csrf_exempt
def delete_comment(request):
    return JsonResponse({})


@csrf_exempt
def update_comment(request):
    return JsonResponse({})
