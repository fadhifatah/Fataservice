from django.http import HttpResponse
from PIL import Image


# Create your views here.
def image(request):
    img = open('data/img/image.jpg', 'rb').read()
    return HttpResponse(img, content_type='image/jpeg')


def thumbnail(request):
    tmb = Image.open()
    return HttpResponse(tmb, content_type='image/jpeg')
