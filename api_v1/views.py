from django.http import JsonResponse, HttpResponse
from .models import User


# Create your views here.
def login(request):
    users_dummy = User.objects.all()
    for dummy in users_dummy:
        username = dummy.username
        display_name = dummy.display_name

    return JsonResponse({'username': username, 'display_name': display_name})


def register(request):
    return JsonResponse({})


def get_users(request):
    if request.method == 'GET':
        page = request.GET['page']
        limit = request.GET['limit']
        return JsonResponse({'page': page, 'limit': limit})
    else:
        return JsonResponse()


def create_comment(request):
    return JsonResponse({})


def get_comment_by_id(request, comment_id):
    return JsonResponse({'comment_id': comment_id})


def get_comments(request):
    return JsonResponse({})


def delete_comment(request):
    return JsonResponse({})


def update_comment(request):
    return JsonResponse({})
