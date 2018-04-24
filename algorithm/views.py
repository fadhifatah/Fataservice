import time
from collections import OrderedDict

import requests
from django.http import JsonResponse
from django.shortcuts import render

from algorithm.forms import InputForm


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


def index(request):
    if request.method == 'POST':
        # something
        value_a = request.POST['A']
        value_b = request.POST['B']
        value_c = request.POST['C']
        value_d = request.POST['D']

        # proceed orchestrator
        orchestrator = requests.get(
            'http://host21018.proxy.infralabs.cs.ui.ac.id/algorithms/green?'
            'a=' + str(value_a) +
            '&b=' + str(value_b) +
            '&c=' + str(value_c) +
            '&d=' + str(value_d),
        )

        result = 'Timeout :('
        if orchestrator.status_code == 200:
            result = orchestrator.json()['result']

        return render(request, 'cots_2.html', {'result': result})
    else:
        form = InputForm()
        return render(request, 'cots_2.html', {'form': form})


def green(request):
    if request.method == 'GET':
        # do something
        value_a = request.GET.get('a')
        value_b = request.GET.get('b')
        value_c = request.GET.get('c')
        value_d = request.GET.get('d')

        while True:
            # r1 requests
            r1_req = requests.get(
                'http://host22018.proxy.infralabs.cs.ui.ac.id/algorithms/r1?'
                'a=' + str(value_a) +
                '&b=' + str(value_b) +
                '&c=' + str(value_c) +
                '&d=' + str(value_d)
            )

            if r1_req.status_code == 200:
                r1_res = r1_req.json()['result']
                break

        # time.sleep(0.5)

        while True:
            # r2 requests
            r2_req = requests.get(
                'http://host23018.proxy.infralabs.cs.ui.ac.id/algorithms/r2?'
                'a=' + str(value_a) +
                '&b=' + str(value_b) +
                '&c=' + str(value_c) +
                '&d=' + str(value_d)
            )

            if r2_req.status_code == 200:
                r2_res = r2_req.json()['result']
                break

            # time.sleep(0)

        while True:
            # r3 requests
            r3_req = requests.get(
                'http://host24018.proxy.infralabs.cs.ui.ac.id/algorithms/r3?'
                'a=' + str(value_a) +
                '&b=' + str(value_b) +
                '&c=' + str(value_c) +
                '&d=' + str(value_d)
            )

            if r3_req.status_code == 200:
                r3_res = r3_req.json()['result']
                break

        #     time.sleep(1.5)

        result = r1_res + r2_res - r3_res
        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'),
                                         ('result', result)]))


def r1(request):
    global e_res, f_res, g_res
    if request.method == 'GET':
        # [((A + B) * C) / D]
        # [(E * C) / D]
        # [F / D]
        # G

        value_a = request.GET.get('a')
        value_b = request.GET.get('b')
        value_c = request.GET.get('c')
        value_d = request.GET.get('d')

        # get E
        e_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php?'
            'a=' + str(value_a) +
            '&b=' + str(value_b)
        )
        if e_req.status_code == 200:
            e_res = e_req.json()['hasil']

        # get F
        f_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/kali.php',
            headers={
                'Argumen-A': str(e_res),
                'Argumen-B': str(value_c)
            }
        )
        if f_req.status_code == 200:
            f_res = f_req.text

        # get G
        g_req = requests.head(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/bagi.php',
            headers={
                'Argumen-A': str(f_res),
                'Argumen-B': str(value_d)
            }
        )
        if g_req.status_code == 200:
            g_res = int(round(g_req.headers['Hasil']))

        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'),
                                         ('result', g_res)]))


def r2(request):
    global e_res, f_res, g_res, h_res
    if request.method == 'GET':
        # [((A + B + C) * D) / C]
        # [((E + C) * D) / C]
        # [(F * D) / C]
        # [G / C]
        # H

        value_a = request.GET.get('a')
        value_b = request.GET.get('b')
        value_c = request.GET.get('c')
        value_d = request.GET.get('d')

        # get E
        e_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php?'
            'a=' + str(value_a) +
            '&b=' + str(value_b)
        )
        if e_req.status_code == 200:
            e_res = e_req.json()['hasil']

        # get F
        f_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php?'
            'a=' + str(e_res) +
            '&b=' + str(value_c)
        )
        if f_req.status_code == 200:
            f_res = f_req.json()['hasil']

        # get G
        g_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/kali.php',
            headers={
                'Argumen-A': str(f_res),
                'Argumen-B': str(value_d)
            }
        )
        if g_req.status_code == 200:
            g_res = g_req.text

        # get H
        h_req = requests.head(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/bagi.php',
            headers={
                'Argumen-A': str(g_res),
                'Argumen-B': str(value_c)
            }
        )
        if h_req.status_code == 200:
            h_res = int(round(h_req.headers['Hasil']))

        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'),
                                         ('result', h_res)]))


def r3(request):
    global f_res, e_res, g_res
    if request.method == 'GET':
        # [((C * B) * D) / A]
        # [(E * D) / A]
        # [F / A]

        value_a = request.GET.get('a')
        value_b = request.GET.get('b')
        value_c = request.GET.get('c')
        value_d = request.GET.get('d')

        # get E
        e_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/kali.php',
            headers={
                'Argumen-A': str(value_c),
                'Argumen-B': str(value_b)
            }
        )
        if e_req.status_code == 200:
            e_res = e_req.text

        # get F
        f_req = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/kali.php',
            headers={
                'Argumen-A': str(e_res),
                'Argumen-B': str(value_d)
            }
        )
        if f_req.status_code == 200:
            f_res = f_req.text

        # get H
        g_req = requests.head(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/bagi.php',
            headers={
                'Argumen-A': str(f_res),
                'Argumen-B': str(value_a)
            }
        )
        if g_req.status_code == 200:
            g_res = int(round(g_req.headers['Hasil']))

        return JsonResponse(OrderedDict([('status', 200), ('description', 'OK'),
                                         ('result', g_res)]))
