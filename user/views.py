from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('<h1>List of users</h1>')
