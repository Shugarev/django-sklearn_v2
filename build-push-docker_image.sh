#!/bin/bash

# заменить 'HOST': 'localhost'  на 'HOST': 'db'
sed -i "s/'HOST': 'localhost'/'HOST': 'db'/g" ./sklearn_django/settings.py


# удаление прдедидущего образа проекта
docker rmi  shugarev1974/django-sklearn_v2

# создание нового образа из проекта
docker build -t shugarev1974/django-sklearn_v2 .

# залогиниться в dockerhub репозитории
docker login

# запушить изменения в репозиторий
docker push shugarev1974/django-sklearn_v2

# Обратная замена 'HOST': 'db' на 'HOST': 'localhost'
sed -i "s/'HOST': 'db'/'HOST': 'localhost'/g" ./sklearn_django/settings.py