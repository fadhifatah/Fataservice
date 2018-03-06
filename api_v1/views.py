from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        User.objects.create(username='1406571842', display_name='Fatah Fadhlurrohman')
        return JsonResponse({'username': username, 'password': password})
    return JsonResponse({'status': 'Gagal'})


@csrf_exempt
def register(request):
    return JsonResponse({})


def get_users(request):
    if request.method == 'GET':
        users_dummy = User.objects.all()
        for dummy in users_dummy:
            username = dummy.username
            display_name = dummy.display_name

        return JsonResponse({'username': username, 'display_name': display_name})
    else:
        return JsonResponse()


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
