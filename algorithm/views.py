from django.http import JsonResponse
from collections import OrderedDict

# Create your views here.


def plus(request):
    if request.method == 'GET':
        number1 = request.GET.get('x1')
        number2 = request.GET.get('x2')

        if number1 is None or number2 is None:
            return JsonResponse(OrderedDict([('status', 401), ('description', 'Bad Request, Wrong Parameters or '
                                                                              'Missing Parameters')]))

        try:
            number1 = int(number1)
            number2 = int(number2)
        except ValueError:
            return JsonResponse(OrderedDict([('status', 402), ('description', 'Bad Request, Parameters not Integer or '
                                                                              'can\'t be Empty')]))

        result = number1 + number2
        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'), ('result', result)]))
    return JsonResponse(OrderedDict([('status', 400), ('description', 'Bad Request, Wrong Method')]))


def times(request):
    if request.method == 'GET':
        number1 = request.GET.get('x1')
        number2 = request.GET.get('x2')

        if number1 is None or number2 is None:
            return JsonResponse(OrderedDict([('status', 401), ('description', 'Bad Request, Wrong Parameters or '
                                                                              'Missing Parameters')]))

        try:
            number1 = int(number1)
            number2 = int(number2)
        except ValueError:
            return JsonResponse(OrderedDict([('status', 402), ('description', 'Bad Request, Parameters not Integer or '
                                                                              'can\'t be Empty')]))

        result = number1 * number2
        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'), ('result', result)]))
    return JsonResponse(OrderedDict([('status', 400), ('description', 'Bad Request, Wrong Method')]))
