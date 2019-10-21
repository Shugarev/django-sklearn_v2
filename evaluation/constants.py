from sklearn_django.settings import BASE_DIR

class Params:
    BAD_STATUSES = ('true', 1, '1')
    ALGORITHMS = ['adaboost', 'gausnb', 'decisiontree', 'gradientboost', 'logregression', 'linear_sgd','xgboost'
        ,'lightgbm', 'kneighbors']
    COMPARE_RESULT_URL = '/media/exp/compare-results.csv'
    COMPARE_RESULT_PATH = '{}/media/exp/{}' . format(BASE_DIR, 'compare-results.csv')
