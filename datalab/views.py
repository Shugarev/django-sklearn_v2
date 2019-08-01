# Create your views here.

from django.shortcuts import render

def dataset(request):
    return render(request, 'datalab/file.html')


def profile(request):
    pass


def profile_config(request):
    pass


def experiment(request):
    pass


def delete_dataset(request, pk):
    pass


def delete_profile(request, pk):
    pass


def delete_experiment(request, pk):
    pass


def research(request):
    pass
