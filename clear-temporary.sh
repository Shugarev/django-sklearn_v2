#!/bin/bash

mysql --host=127.0.0.1 -P 3306 -u datalab -pDatalab1414 -e "DROP DATABASE datalab;"
mysql --host=127.0.0.1 -P 3306 -u datalab -pDatalab1414 -e "CREATE DATABASE datalab;"


# удалть кроме двух файлов пример.
#find . -path "*/migrations/*.py" -not  \( -name "__init__.py" -or -name "0002_algorithms_migration.py" \) -delete

mv ./datalab/migrations/0002_data_migration.py  ./datalab
# удалить миграцию
find . -path "*/migrations/*.py" -not  -name "__init__.py"  -delete
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/datasets/*.*" -not -name "__init__.py" -delete
find . -path "*/exp/*.*" -not -name "__init__.py" -delete
find . -path "*/fi/*.*" -not -name "__init__.py" -delete
find . -path "*/profiles/*" -not -name "__init__.py" -delete

python manage.py makemigrations
mv ./datalab/0002_data_migration.py ./datalab/migrations/
python manage.py migrate

