# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import File
from .forms import FileForm


def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = File(file=request.FILES['file'])
            file.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('file'))
    else:
        form = FileForm()  # A empty, unbound form

    # Load documents for the list page
    documents = File.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'file_upload.html',
        {'documents': documents, 'form': form}
    )
