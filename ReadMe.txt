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

0) В settings.py в настройках соединения с базой установить 'Host':'db'( указать ссылку на  название контейнера)
1) В корне проекта создать Dockerfile
2) В корне проекта создать docker-compose.yml
3) Создать image из проекта (выполнить команду из корня проекта)
docker build -t shugarev1974/django-sklearn_v2 .
4) залогиниться в репозитории https://hub.docker.com, login: shugarev1974
docker login
5) запушить в репозиторий
docker push shugarev1974/django-sklearn_v2
6) проверить наличие файла wait-for-it.sh в папке с docker-compose.yml
7) Из корня проекта выполнить
docker-compose up

 - проект будет доступен по ссылке http://localhost:8000/datalab/

Запустить проект на другом хосте.
1) Проверить наличие docker и docker compose( docker version, docker-compose  version. При необходимости установить оба пакета)
2) Создать новую директорию
3) записать два файла docker-compose.yml и  wait-for-it.sh
4) залогиниться docker login
5) Выполнить команду из директории
docker-compose up
6) Вaжно !
    - в settings.py должны быть прописаны settings.py ALLOWED_HOSTS.
    - в docker-compose.yml не должно быть раздела volumes
    ( если этот раздел есть, то предполагается что на всех машинах, на которые будет установливаться контейнер
    структура папок одинаковая. volumes можно оставить только на этапе разработки, тогда очень удобно при изменении
    локально происходят изменения в контейнере.)
    volumes:
      - .:/code
    - раздел links в docker-compose.yml deprecated, вместо него depends_on
    - раздел buil в в docker-compose.yml можно оставить только если работаешь локально или в папке откуда идет запуск находятся файлы проекта.
    - На сервере проект работает http://192.168.0.105:8000/datalab/dataset/
    - на проде тушить контейнер


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



 # Для работы с приложениями запущенными на localhost-е по другим портам необходимо в settings.py раскомментировать
 строку 'api.middleware.MyMiddleware' и создать файл api/middleware.py  в котором изменяется header response.
 Или взаимодействовать через локальный proxy server (cors-anywhere)