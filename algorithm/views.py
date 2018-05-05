from collections import OrderedDict

import requests
import xmltodict
from django.http import JsonResponse
from django.shortcuts import render

from algorithm.constants import Constants, Review
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


def nlp_restaurant(request):
    if request.method == 'GET':
        list_of_unique_rid = set()

        with open(Constants.dir + '/data/dataset_part_31.xml') as d1:
            data_set1 = xmltodict.parse(d1.read())

        data1 = data_set1['corpus']['review']
        for d1 in data1:
            rid1 = d1['@rid']
            list_of_unique_rid.add(rid1)

        with open(Constants.dir + '/data/dataset_part_32.xml') as d2:
            data_set2 = xmltodict.parse(d2.read())

        data2 = data_set2['corpus']['review']
        for d2 in data2:
            rid2 = d2['@rid']
            list_of_unique_rid.add(rid2)

        with open(Constants.dir + '/data/dataset_part_33.xml') as d3:
            data_set3 = xmltodict.parse(d3.read())

        data3 = data_set3['corpus']['review']
        for d3 in data3:
            rid3 = d3['@rid']
            list_of_unique_rid.add(rid3)

        return render(request, 'nlp_compare.html', {'size': list_of_unique_rid.__len__(),
                                                    'data': list_of_unique_rid,
                                                    'flag': 1})


def nlp_restaurant_rid(request, rid):
    global review1, review2, review3
    if request.method == 'GET':
        with open(Constants.dir + '/data/dataset_part_31.xml') as d1:
            data_set1 = xmltodict.parse(d1.read())

        data1 = data_set1['corpus']['review']
        for d1 in data1:
            if d1['@rid'] == str(rid):
                d1_aspects = {}

                aspects = d1['aspects']['aspect']
                if isinstance(aspects, list):
                    for aspect in aspects:
                        d1_aspects[aspect['@category']] = aspect['@polarity']

                    review1 = Review(d1['@rid'], d1['text'], d1_aspects, 'Agung')
                    break
                else:
                    review1 = Review(d1['@rid'], d1['text'], {aspects['@category']: aspects['@polarity']}, 'Agung')
                    break

            else:
                review1 = Review('-', '-', {}, '-')

        with open(Constants.dir + '/data/dataset_part_32.xml') as d2:
            data_set2 = xmltodict.parse(d2.read())

        data2 = data_set2['corpus']['review']
        for d2 in data2:
            if d2['@rid'] == str(rid):
                d2_aspects = {}

                aspects = d2['aspects']['aspect']
                if isinstance(aspects, list):
                    for aspect in aspects:
                        d2_aspects[aspect['@category']] = aspect['@polarity']

                    review2 = Review(d2['@rid'], d2['text'], d2_aspects, 'Faisal')
                    break
                else:
                    review2 = Review(d2['@rid'], d2['text'], {aspects['@category']: aspects['@polarity']}, 'Faisal')
                    break

            else:
                review2 = Review('-', '-', {}, '-')

        with open(Constants.dir + '/data/dataset_part_33.xml') as d3:
            data_set3 = xmltodict.parse(d3.read())

        data3 = data_set3['corpus']['review']
        for d3 in data3:
            if d3['@rid'] == str(rid):
                d3_aspects = {}

                aspects = d3['aspects']['aspect']
                if isinstance(aspects, list):
                    for aspect in aspects:
                        d3_aspects[aspect['@category']] = aspect['@polarity']

                    review3 = Review(d3['@rid'], d3['text'], d3_aspects, 'Fatah')
                    break
                else:
                    review3 = Review(d3['@rid'], d3['text'], {aspects['@category']: aspects['@polarity']}, 'Fatah')
                    break

            else:
                review3 = Review('-', '-', {}, '-')

        return render(request, 'nlp_compare.html', {'flag': 2, 'review1': review1, 'review2': review2,
                                                    'review3': review3})
