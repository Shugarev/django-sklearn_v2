import pandas as pd

from datalab.models import Algorithm
from datalab.models import DataSet
from sklearn_django.settings import BASE_DIR


def get_objects_to_create_profile_config(request):
    teach_id = request.POST.get('teach')
    teach = DataSet.objects.get(pk=teach_id)

    algorithm_id = request.POST.get('algorithm')
    algorithm = Algorithm.objects.get(pk=algorithm_id)

    profile_name = request.POST.get('profile_name')
    return teach, algorithm, profile_name


def get_objects_to_create_profile(request):
    teach_id = request.POST.get('teach')
    teach = DataSet.objects.get(pk=teach_id)

    algorithm_id = request.POST.get('algorithm')
    algorithm = Algorithm.objects.get(pk=algorithm_id)

    profile_name = 'profiles/' + request.POST.get('profile_name')
    feature_importance = 'fi/fi-' + request.POST.get('profile_name') + '.csv'
    return teach, algorithm, profile_name, feature_importance


def get_file_columns(teach):
    file_path = "{}/media/{}".format(BASE_DIR, teach.file.name)
    df = pd.read_csv(file_path, dtype=str, nrows=1)
    columns = {col: 1 for col in list(df)}
    return columns


def get_used_columns_to_profile(request, teach):
    file_path = "{}/media/{}".format(BASE_DIR, teach.file.name)
    df = pd.read_csv(file_path, dtype=str, nrows=1)
    used_columns = {col: 1 if request.POST.get(col) and request.POST.get(col) == '1' else 0 for col in list(df)}
    print((used_columns))
    return used_columns


def get_teach_path(teach_file_name):
    return "{}/media/{}".format(BASE_DIR, teach_file_name)

def get_feature_path(feature_name):
    return "{}/media/{}".format(BASE_DIR, feature_name)

def get_profile_path(profile_name):
    return "{}/media/{}".format(BASE_DIR, profile_name)
