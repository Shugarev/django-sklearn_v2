from django.db import migrations
from datalab.models import Algorithm


def populate_algorithms(*args):
    default_algorithm_params = {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'random_state': 123}
    algorithm_params_range = {'learning_rate': [0.2, 0.5, 0.7, 1, 1.5], 'max_depth': [2, 3, 5, 7],
                              'n_estimators': [60, 80, 100, 120, 140], 'random_state': [123]}
    algorithm = Algorithm(algorithm_name='xgboost', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'learning_rate': 1.0, 'n_estimators': 50, 'random_state': 123}
    algorithm_params_range = {'learning_rate': [0.2, 0.5, 0.7, 1, 1.5], 'n_estimators': [60, 80, 100, 120, 140],
                              'random_state': [123]}
    algorithm = Algorithm(algorithm_name='adaboost', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100, 'random_state': 123}
    algorithm_params_range = {'learning_rate': [0.2, 0.5, 0.7, 1, 1.5], 'max_depth': 2,
                              'n_estimators': [60, 80, 100, 120, 140], 'random_state': [123]}
    algorithm = Algorithm(algorithm_name='gradientboost', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {}
    algorithm_params_range = {}
    algorithm = Algorithm(algorithm_name='gausnb', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'random_state': 123}
    algorithm_params_range = {'max_iter': 100, 'penalty': 'l2'}
    algorithm = Algorithm(algorithm_name='logregression', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'max_iter': 1000, 'loss': 'modified_huber', 'penalty': 'l2'}
    algorithm_params_range = {'penalty': ['none', 'l2', 'l1', 'elasticnet'], 'max_iter': [800, 1000, 1200, 1500]}
    algorithm = Algorithm(algorithm_name='linear_sgd', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'learning_rate': 0.1, 'max_depth': -1, 'n_estimators': 100, 'num_leaves': 31,
                                'objective': 'binary','random_state': 123}
    algorithm_params_range = {'learning_rate': [0.02, 0.05, 0.1, 0.2, 0.5], 'max_depth': [2, 3, 5, 7],
                              'n_estimators': [60, 80, 100, 120, 140], 'random_state': [123]}
    algorithm = Algorithm(algorithm_name='lightgbm', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()

    default_algorithm_params = {'weights': 'distance', 'n_neighbors': 20}
    algorithm_params_range = {'weights': ['uniform', 'distance'], 'n_neighbors': [3, 5, 7, 9, 20, 25]}
    algorithm = Algorithm(algorithm_name='kneighbors', default_algorithm_params=default_algorithm_params,
                          algorithm_params_range=algorithm_params_range)
    algorithm.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datalab', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_algorithms),
    ]
