import requests
from django.shortcuts import render

from latihan.constants import Credentials
from latihan.forms import DocumentForm
from latihan.models import Document


# Create your views here.
def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            client_id = Credentials.client_id
            client_secret = Credentials.client_secret

            oauth_token = requests.post(
                'http://172.22.0.2/oauth/token',
                data={
                    'username': username,
                    'password': password,
                    'grant_type': 'password',
                    'client_id': client_id,
                    'client_secret': client_secret,
                }
            )

            if oauth_token.status_code == 200:
                file = Document(file=request.FILES['file'])
                file.save()

                # Redirect to the document list after POST
                return render(
                            request,
                            'file_zipping.html',
                            {'flag': True}
                        )
            else:
                return render(
                            request,
                            'file_zipping.html',
                            {'flag': False}
                        )
    else:
        form = DocumentForm()  # A empty, unbound form

    # Render list page with the documents and the form
    return render(
        request,
        'file_zipping.html',
        {'form': form, 'flag': False, 'hidden': 'hidden'}
    )


def zip_progress(request):
    return
