# запуск проекта
python manage.py runserver

# создание базы
create DATABASE datalab;
FLUSH PRIVILEGES;
SET GLOBAL validate_password_policy = 0;
CREATE USER 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
GRANT ALL PRIVILEGES ON datalab.* TO 'datalab'@'localhost' IDENTIFIED BY 'Datalab1414';
FLUSH PRIVILEGES;

# миграция
python manage.py makemigrations datalab
python manage.py migrate

# вторая миграция содержит начальное заполнение списка алгоритмов

# удалить миграцию
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
Did you install mysqlclient?
#создать и удалить пользователя. Перезапустить проект. Попробовать доставить пакет а потом удалить. Ошибка уйдет.

# Docker

Подготовительная работа
a) Установить Docker
б) pip freeze > requirements.txt создать список зависимостей
в) Установить docker-compose

1) В корне проекта создать Dockerfile
2) В корне проекта создать docker-compose.yml
3) В корне проекта выполнить команду  docker-compose up
4) В settings.py в настройках соединения с базой установить 'Host':'db'( указать ссылку на  название контейнера)
5) проект будет доступен по ссылке http://localhost:8000/datalab/

docker-compose.yml содержит два контейнера.
Для того, чтобы в web контейнере выполнились миграции вначале должен полностью прогрузиться
контейнер db(db - загружает mysql в контейнер)


Список команд:
docker images - список образов.
docker ps  - список работающих контейнеров.
docker exec -it 72ca2488b353 bash - зайти внутрь работающего контейнера
docker ps -a список всех конейнеров.
docker rmi img_hash удалить образ.
docker rm container_hash удалить контейнер.
docker rm $( docker ps -a -q -f status=exited) -удалить все остановленные контейнеры.

docker-copose up - создание и запуск всех контейнеров находящися в файле docker-compost.yml
docker-compose run db -d  - создание и запуск контейнера db (из файла docker-compost.yml), демон.
docker-compose run web -d - создание и запуск контейнера web (из файла docker-compost.yml), демон.
docker-compose down - остановить все контейнеры

Note: Port mapping is incompatible with network_mode: host

зайти в mysql по порту, в котором работает контейнер.
mysql -udatalab -pDatalab1414 -h127.0.0.1 -P3308
show databases;
datalab'@'172.26.0.1'

залогиниться в репозитории(https://hub.docker.com login: shugarev1974,)
docker login

запушить image в репозиторий https://hub.docker.com
docker push shugarev1974/evaluation-service1414

стянуть из репозитория
docker pull  shugarev1974/evaluation-service1414