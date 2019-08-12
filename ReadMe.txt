запуск проекта
python manage.py runserver

создание базы
create DATABASE datalab;
FLUSH PRIVILEGES;
SET GLOBAL validate_password_policy = 0;
CREATE USER 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
GRANT ALL PRIVILEGES ON datalab.* TO 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
FLUSH PRIVILEGES;

миграция
python manage.py makemigrations datalab
python manage.py migrate

вторая миграция содержит начальное заполнение списка алгоритмов

удалить миграцию
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?
создать и удалить пользователя. Перезапустить проект. Попробовать доставить пакет а потом удалить. Ошибка уйдет.

