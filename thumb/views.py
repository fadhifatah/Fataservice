from django.http import HttpResponse


# Create your views here.
def image(request):
    img = open('data/img/image.jpg').read()
    return HttpResponse(img, content_type='image/jpeg')


def thumbnail(request):
    return HttpResponse()
