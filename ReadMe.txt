запуск проекта
python manage.py runserver

миграция
python manage.py makemigrations datalab
python manage.py migrate


create DATABASE datalab;
FLUSH PRIVILEGES;
SET GLOBAL validate_password_policy = 0;
CREATE USER 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
GRANT ALL PRIVILEGES ON datalab.* TO 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
FLUSH PRIVILEGES;


удалить миграцию
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?
создать и удалить пользователя. Перезапустить проект. Попробовать доставить пакет а потом удалить. Ошибка уйдет.

# add algorithms and configs in database.
$ python manage.py shell

from datalab.models import Algorithm
default_algorithm_params={'learning_rate': 0.2, 'max_depth': 2, 'n_estimators': 60, 'random_state': 123}
algorithm_params_range={'learning_rate': [0.2, 0.5, 0.7, 1, 1.5], 'max_depth': [2, 3, 5, 7], 'n_estimators': [60, 80, 100, 120, 140], 'random_state': [123]}
algorithm = Algorithm(algorithm_name='xgboost', default_algorithm_params=default_algorithm_params,algorithm_params_range=algorithm_params_range)
algorithm.save()

default_algorithm_params={'learning_rate': 0.2, 'n_estimators': 60, 'random_state': 123}
algorithm_params_range={'learning_rate': [0.2, 0.5, 0.7, 1, 1.5], 'n_estimators': [60, 80, 100, 120, 140], 'random_state': [123]}
algorithm = Algorithm(algorithm_name='adaboost', default_algorithm_params=default_algorithm_params,algorithm_params_range=algorithm_params_range)
algorithm.save()

algorithm = Algorithm(algorithm_name='test', default_algorithm_params=default_algorithm_params)
algorithm.save()
