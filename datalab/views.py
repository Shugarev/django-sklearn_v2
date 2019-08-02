# Create your views here.
import json

import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datalab.models import Algorithm
from datalab.models import DataSet
from datalab.models import Profile
from datalab.models import UploadDataSet
from datalab.utils import get_objects_to_create_profile
from datalab.utils import get_objects_to_create_profile_config
from datalab.utils import get_profile_path
from datalab.utils import get_teach_path
from datalab.utils import get_feature_path
from datalab.utils import get_used_columns_to_profile
from evaluation.model_creator import modelCreator
from sklearn_django.settings import BASE_DIR


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
            teach, algorithm, profile_name, feature_importance = get_objects_to_create_profile(request)
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
            modelCreator.run(get_teach_path(teach.file.name), algorithm.algorithm_name
                                      , profile.profile_params, get_profile_path(profile_name)
                                      , profile.get_used_factor_list(), get_feature_path(feature_importance))

    datasets = DataSet.objects.all().order_by('-upload_date')
    profiles = Profile.objects.all().order_by('-created_date')
    algorithms = Algorithm.objects.all().order_by('algorithm_name')

    context = {'datasets': datasets, 'profiles': profiles
        , 'algorithms': algorithms, 'profile': 'active'}
    return render(request, 'datalab/profile.html', context)


def profile_config(request):
    if request.method == "POST":
        if request.POST.get('form_name') == 'profile_config':
            teach, algorithm, profile_name = get_objects_to_create_profile_config(request)
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
    if request.method == "POST":
        profile = Profile.objects.get(pk=pk)
        try:
            profile.delete()
        except IOError as e:
            messages.error(request, str(e))
    return HttpResponseRedirect(reverse("profile"))


def delete_experiment(request, pk):
    pass


def research(request):
    pass
