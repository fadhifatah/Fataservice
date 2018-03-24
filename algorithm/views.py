from django.http import JsonResponse
from collections import OrderedDict

# Create your views here.


def plus(request):
    if request.method == 'GET':
        try:
            number1 = request.GET.get('x1')
            number2 = request.GET.get('x2')
        except ValueError:
            return JsonResponse(OrderedDict(status=400, description='Bad Request, Wrong Parameters'))

        try:
            number1 = int(number1)
            number2 = int(number2)
        except ValueError:
            return JsonResponse(OrderedDict(status=400, description='Bad Request, Parameters not Integer'))

        result = number1 + number2
        return JsonResponse(OrderedDict(status=200, description='OK', result=result))
    return JsonResponse(OrderedDict(status=400, description='Bad Request, Wrong Method'))


def times(request):
    if request.method == 'GET':
        try:
            number1 = request.GET.get('x1')
            number2 = request.GET.get('x2')
        except ValueError:
            return JsonResponse(OrderedDict(status=400, description='Bad Request, Wrong Parameters'))

        try:
            number1 = int(number1)
            number2 = int(number2)
        except ValueError:
            return JsonResponse(OrderedDict(status=400, description='Bad Request, Parameters not Integer'))

        result = number1 * number2
        return JsonResponse(OrderedDict(status=200, description='OK', result=result))
    return JsonResponse(OrderedDict(status=400, description='Bad Request, Wrong Method'))
