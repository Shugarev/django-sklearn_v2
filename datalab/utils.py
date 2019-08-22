import pandas as pd
import os
from datalab.models import Algorithm
from datalab.models import DataSet
from datalab.models import Profile
from sklearn_django.settings import BASE_DIR
from evaluation.constants import Params

def get_data_to_create_profile_config(request):
    teach_id = request.POST.get('teach')
    teach = DataSet.objects.get(pk=teach_id)

    algorithm_id = request.POST.get('algorithm')
    algorithm = Algorithm.objects.get(pk=algorithm_id)

    profile_name = request.POST.get('profile_name')
    return teach, algorithm, profile_name


def get_data_to_create_profile(request):
    teach_id = request.POST.get('teach')
    teach = DataSet.objects.get(pk=teach_id)

    algorithm_id = request.POST.get('algorithm')
    algorithm = Algorithm.objects.get(pk=algorithm_id)

    profile_name = 'profiles/' + request.POST.get('profile_name')
    feature_importance = 'fi/fi-' + request.POST.get('profile_name') + '.csv'
    return teach, algorithm, profile_name, feature_importance

def get_data_to_create_experiment(request):
    profile_id = request.POST.get('profile_id')
    profile = Profile.objects.get(pk=profile_id)

    test_id = int(request.POST.get('test'))
    test = DataSet.objects.get(pk=test_id)

    experiment_name = 'exp/Test1-' + request.POST.get('experiment_name') + '.csv'
    analyzer_name = 'exp/Analyzer-' + request.POST.get('experiment_name') + '.csv'
    return profile, test, experiment_name, analyzer_name

def get_file_columns(teach):
    file_path = "{}/media/{}".format(BASE_DIR, teach.file.name)
    df = pd.read_csv(file_path, dtype=str, nrows=1)
    columns = {col: 1 for col in list(df)}
    return columns


def get_used_columns_to_profile(request, teach):
    file_path = "{}/media/{}".format(BASE_DIR, teach.file.name)
    df = pd.read_csv(file_path, dtype=str, nrows=1)
    used_columns = {col: 1 if request.POST.get(col) and request.POST.get(col) == '1' else 0 for col in list(df)}
    return used_columns


def get_full_path(name):
    return "{}/media/{}".format(BASE_DIR, name)


def get_description(profile,test):
    return 'model: ' +  profile.profile_name + '\ntest_name: ' + test.file.name

def remove_compare_results():
    if os.path.exists(Params.COMPARE_RESULT_PATH):
        os.remove(Params.COMPARE_RESULT_PATH)
