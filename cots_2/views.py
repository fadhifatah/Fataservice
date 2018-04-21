import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from .forms import InputForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        value_a = int(request.POST['A'])
        value_b = int(request.POST['B'])
        value_c = int(request.POST['C'])
        value_d = int(request.POST['D'])

        # proceed orchestrator
        orchestrator = requests.post(
            'http://172.22.0.98/cots_2/orchestration',
            data={
                'a': value_a,
                'b': value_b,
                'c': value_c,
                'd': value_d,
            }
        )

        if orchestrator.status_code == 200:
            result = orchestrator.json()['result']
        else:
            result = str("Reload!")

        return render(request, 'cots_2.html', {'result': result})
    else:
        form = InputForm()
        return render(request, 'cots_2.html', {'form': form})


def orchestration(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            value_a = body['a']
            value_b = body['b']
            value_c = body['c']
            value_d = body['d']
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong JSON format'})

        # proceed blue formula
        blue_r = requests.post(
            'http://172.22.0.129/cots_2/blue?a=' + value_a + '&b=' + value_b + '&c=' + value_b + '&d=' + value_b,
        )

        r1 = 0
        if blue_r.status_code == 200:
            r1 = blue_r.json()['result']

        # proceed red formula
        red_r = requests.get(
            'http://172.22.0.160/cots_2/red?a=' + value_a + '&b=' + value_b + '&c=' + value_b + '&d=' + value_b,
        )

        r2 = 0
        if red_r.status_code == 200:
            r2 = red_r.json()['result']

        # proceed purple formula
        purple_r = requests.post(
            'http://172.22.0.191/cots_2/purple',
            data={
                'a': value_a,
                'b': value_b,
                'c': value_c,
                'd': value_d,
            }
        )

        r3 = 0
        if purple_r.status_code == 200:
            r3 = purple_r.json()['result']

        result = r1 + r2 - r3
        return JsonResponse({'result': result})


def blue(request):
    if request.method == 'GET':
        try:
            value_a = request.GET['a']
            value_b = request.GET['b']
            value_c = request.GET['c']
            value_d = request.GET['d']
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong JSON format'})

        # do tambah
        tambah = requests.get(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/tambah.php?a=' + value_a + '&b=' + value_b
        )

        tambah_r = 0
        if tambah.status_code == 200:
            tambah_r = tambah.json()['hasil']

        # do bagi
        bagi = requests.head(
            'http://host20099.proxy.infralabs.cs.ui.ac.id/bagi.php',
            headers={
                'Argumen-A': tambah_r,
                'Argumen-B': value_c,
            }
        )

        bagi_r = 0
        if bagi.status_code == 200:
            bagi_r = bagi.headers['Hasil']

        # do round

        return


def red(request):
    if request.method == 'GET':
        try:
            value_a = request.GET['a']
            value_b = request.GET['b']
            value_c = request.GET['c']
            value_d = request.GET['d']
        except ValueError:
            return JsonResponse({'status': 401, 'description': 'Wrong JSON format'})

        # do tambah

        return


def purple(request):
    if request.method == 'POST':

        return
