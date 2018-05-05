from django.http import HttpResponse
from PIL import Image
from thumb.constants import Constants


# Create your views here.
def image(request):
    img = open(Constants.dir + '/data/img/image.jpg', 'rb').read()
    return HttpResponse(img, content_type='image/jpeg')


def thumb(request):
    img = Image.open(Constants.dir + '/data/img/image.jpg')
    img.thumbnail((240, 240))
    img.save(Constants.dir + '/data/img/image.thumbnail.jpg')

    tmb = open(Constants.dir + '/data/img/image.thumbnail.jpg', 'rb').read()
    return HttpResponse(tmb, content_type='image/jpeg')
