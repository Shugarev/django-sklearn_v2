# Create your views here.
import json
import pandas as pd
import os

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datalab.models import Algorithm
from datalab.models import DataSet
from datalab.models import Profile
from datalab.models import UploadDataSet
from datalab.models import Experiment
from datalab.utils import get_data_to_create_profile
from datalab.utils import get_data_to_create_profile_config
from datalab.utils import get_full_path
from datalab.utils import get_used_columns_to_profile
from datalab.utils import get_description
from datalab.utils import get_data_to_create_experiment
from datalab.utils import remove_compare_results
from evaluation.model_creator import modelCreator
from evaluation.dataset_tester import datasetTester
from sklearn_django.settings import BASE_DIR
from evaluation.constants import Params


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
    if request.method == "POST":
        if request.POST.get('form_name') == 'create_profile':
            teach, algorithm, profile_name, feature_importance = get_data_to_create_profile(request)
            used_columns = get_used_columns_to_profile(request, teach)

            if request.POST.get('profile_params'):
                s = request.POST.get('profile_params')
                try:
                    profile_params = json.loads(s)
                except json.JSONDecodeError as e:
                    messages.error(request, 'incorrect json config' + str(e))
                    return HttpResponseRedirect(reverse("profile"))
            profile = Profile(teach=teach, algorithm=algorithm, profile_name=profile_name
                              , feature_importance=feature_importance, factors=used_columns,
                              profile_params=profile_params)
            profile.save()
            modelCreator.run(get_full_path(teach.file.name), algorithm.algorithm_name
                             , profile.profile_params, get_full_path(profile_name)
                             , profile.get_used_factor_list(), get_full_path(feature_importance))

    datasets = DataSet.objects.all().order_by('-upload_date')
    profiles = Profile.objects.all().order_by('-created_date')
    algorithms = Algorithm.objects.all().order_by('algorithm_name')

    context = {'datasets': datasets, 'profiles': profiles
        , 'algorithms': algorithms, 'profile': 'active'}
    return render(request, 'datalab/profile.html', context)


def profile_config(request):
    if request.method == "POST":
        if request.POST.get('form_name') == 'profile_config':
            teach, algorithm, profile_name = get_data_to_create_profile_config(request)
            file_path = "{}/media/{}".format(BASE_DIR, teach.file.name)
            df = pd.read_csv(file_path, dtype=str, nrows=1)
            columns = {col: 1 for col in list(df)}
            default_config = algorithm.default_algorithm_params
            default_config = json.dumps(default_config)
            context = {'algorithm': algorithm, 'teach': teach
                , 'profile_name': profile_name, 'columns': columns
                , 'default_config': default_config}
            return render(request, 'datalab/profile_config.html', context)
        return HttpResponseRedirect(reverse("profile"))

def delete_dataset(request, pk):
    if request.method == "POST":
        img = DataSet.objects.get(pk=pk)
        try:
            img.delete()
        except IOError as e:
            messages.error(request, str(e))
    return HttpResponseRedirect(reverse("dataset"))


def delete_profile(request, pk):
    if request.method == "POST":
        profile = Profile.objects.get(pk=pk)
        try:
            profile.delete()
        except IOError as e:
            messages.error(request, str(e))
    return HttpResponseRedirect(reverse("profile"))

def experiment(request):
    if request.method == "POST":
        if request.POST.get('form_name') == 'create_experiment':
            profile, test, experiment_name, analyzer_name = get_data_to_create_experiment(request)
            experiment = Experiment(test=test, profile=profile, experiment_name=experiment_name, analyzer_name=analyzer_name)
            experiment.save()

            task = 'Tester'
            description = get_description(profile,test)
            datasetTester.run(task, get_full_path(test.file.name), profile.algorithm.algorithm_name
            , get_full_path(profile.profile_name), get_full_path(experiment_name), get_full_path(analyzer_name),
                              profile.get_used_factor_list(),description )
        if request.POST.get('form_name') == 'remove_compare_results':
            remove_compare_results()



    datasets = DataSet.objects.all().order_by('-upload_date')
    profiles = Profile.objects.all().order_by('-created_date')
    experiments = Experiment.objects.all().order_by('-created_date')
    context = {'datasets': datasets, 'experiments': experiments
        , 'profiles': profiles, 'experiment': 'active', 'compare_path': Params.COMPARE_RESULT_URL}

    return render(request, 'datalab/experiment.html', context)


def delete_experiment(request, pk):
    if request.method == "POST":
        experiment = Experiment.objects.get(pk=pk)
        experiment.delete()
    return HttpResponseRedirect(reverse("experiment"))


def research(request):
    context = {}
    return render(request, 'datalab/research.html', context)