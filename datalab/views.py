# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from datalab.models import UploadDataSet
from datalab.models import DataSet
from datalab.models import Algorithm
from datalab.models import Profile
from datalab.models import Experiment


def dataset(request):
    if request.method == "POST":
        if request.POST.get('form_name') == 'upload_form':
            img = UploadDataSet(request.POST, request.FILES)
            if img.is_valid():
                img.save()
    datasets = DataSet.objects.all().order_by('-upload_date')
    context = {'datasets': datasets, 'dataset': 'active'}
    return render(request, 'datalab/dataset.html', context)


def profile(request):
    pass


def profile_config(request):
    pass


def experiment(request):
    pass


def delete_dataset(request, pk):
    if request.method == "POST":
        img = DataSet.objects.get(pk=pk)
        try:
            img.delete()
        except IOError as e:
            messages.error(request, str(e))
    return HttpResponseRedirect(reverse("dataset"))


def delete_profile(request, pk):
    pass


def delete_experiment(request, pk):
    pass


def research(request):
    pass
