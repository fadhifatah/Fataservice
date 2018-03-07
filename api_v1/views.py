from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from api_v1.models import User, Comment
from api_v1.constants import Constants
import requests
import json


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
                'Authorization': 'Bearer ' + token
            }
        )

        if oauth_resource.status_code == 200:
            username = oauth_resource.json()['user_id']

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 401, 'description': 'User already exist'})
            else:
                User.objects.create(username=username, display_name=display_name)
                return JsonResponse({'status': 'ok', 'access_token': token})
        else:
            return JsonResponse({'status': 401, 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


def get_users(request):
    if request.method == 'GET':
        try:
            auth_header = str(request.META['HTTP_AUTHORIZATION'])
            token = auth_header[7:]
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Header Error'})

        oauth_resource = requests.get(
            'http://172.22.0.2/oauth/resource',
            headers={
                'Authorization': 'Bearer ' + token
            }
        )

        if oauth_resource.status_code == 200:
            try:
                page = request.GET.get('page')
                limit = request.GET.get('limit')
            except ValueError:
                return JsonResponse({'status': 401, 'description': 'Wrong parameters'})

            list_of_users = User.objects.all()
            paginator = Paginator(list_of_users, limit)

            try:
                users = paginator.page(page)
            except EmptyPage:
                return JsonResponse({'status': 401, 'description': 'Page empty'})
            except PageNotAnInteger:
                return JsonResponse({'status': 401, 'description': 'Invalid page format'})
            except InvalidPage:
                return JsonResponse({'status': 401, 'description': 'Invalid page number'})

            data = []
            for user in users:
                user_data = {'userId': user.id, 'displayName': user.display_name}
                data.append(user_data)

            return JsonResponse({'status': 'ok', 'page': int(page), 'limit': int(limit),
                                 'total': int(list_of_users.count()), 'data': data})
        else:
            return JsonResponse({'status': 'ok', 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        try:
            auth_header = str(request.META['HTTP_AUTHORIZATION'])
            token = auth_header[7:]
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Header Error'})

        try:
            comment = request.POST.get('comment')
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong POST data'})

        oauth_resource = requests.get(
            'http://172.22.0.2/oauth/resource',
            headers={
                'Authorization': 'Bearer ' + token
            }
        )

        if oauth_resource.status_code == 200:
            username = oauth_resource.json()['user_id']

            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)

                comment = Comment.objects.create(created_by=user, comment=comment)
                data = {
                    'id': comment.id,
                    'comment': comment.comment,
                    'createdBy': user.display_name,
                    'createdAt': comment.created_at,
                    'updatedAt': comment.updated_at
                }
                return JsonResponse({'status': 'ok', 'data': data})
            else:
                return JsonResponse({'status': 401, 'description': 'Please register first!'})
        else:
            return JsonResponse({'status': 401, 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


def get_comment_by_id(request, comment_id):
    if request.method == 'GET':
        if Comment.objects.filter(id=comment_id).exists():
            comment = Comment.objects.get(id=comment_id)
            data = {
                'id': comment.id,
                'comment': comment.comment,
                'createdBy': comment.created_by.display_name,
                'createdAt': comment.created_at,
                'updatedAt': comment.updated_at
            }
            return JsonResponse({'status': 'ok', 'data': data})
        else:
            return JsonResponse({'status': 401, 'description': 'Comment by id=' + str(comment_id) + ' not found'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


def get_comments(request):
    return JsonResponse({})


@csrf_exempt
def delete_comment(request):
    if request.method == 'DELETE':
        try:
            auth_header = str(request.META['HTTP_AUTHORIZATION'])
            token = auth_header[7:]
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Header Error'})

        try:
            comment_id = json.load(request.body.decode('uf-8'))['id']
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong POST data'})

        oauth_resource = requests.get(
            'http://172.22.0.2/oauth/resource',
            headers={
                'Authorization': 'Bearer ' + token
            }
        )

        if oauth_resource.status_code == 200:
            username = oauth_resource.json()['user_id']

            if Comment.objects.filter(id=comment_id).exists():
                comment = Comment.objects.get(id=comment_id)
                user = User.objects.get(username=username)

                if user.username == comment.created_by.username:
                    Comment.objects.filter(id=comment_id).delete()
                    return JsonResponse({'status': 'ok'})
                else:
                    return JsonResponse({'status': 401, 'description': 'Can\'t remove this comment. Not yours!'})
            else:
                return JsonResponse({'status': 401, 'description': 'Comment by id=' + str(comment_id) + ' not found'})
        else:
            return JsonResponse({'status': 401, 'description': 'Failed'})
    return JsonResponse({'status': 401, 'description': 'Wrong Method'})


@csrf_exempt
def update_comment(request):
    if request.method == 'PUT':
        return
    return JsonResponse({})
