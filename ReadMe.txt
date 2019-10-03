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
пункты 0, 3, 4 ,5 реализованы в  build-push-docker_image.sh

6) проверить наличие файла wait-for-it.sh в папке с docker-compose.yml
7) проверить наличие и содержание файлов web.env
В данном проекте в настройках окружения хранятся переменная ALLOWED_HOSTS, которая в setting.py map-ся в список разрешенных hosts.
8) Из корня проекта выполнить
docker-compose up

 - проект будет доступен по ссылке http://localhost:8000/datalab/

Запустить проект на другом хосте.
1) Проверить наличие docker и docker compose( docker version, docker-compose  version. При необходимости установить оба пакета)
2) Создать новую директорию
3) записать два файла docker-compose.yml и  wait-for-it.sh, web.env
4) залогиниться docker login
5) Выполнить команду из директории
docker-compose up
6) Вaжно !
    - в settings.py должны быть прописаны settings.py ALLOWED_HOSTS(или ALLOWED_HOSTS берутся из переменных окружения)
    - раздела volumes
     volumes:
      - ./media:/code/media
     Папка ./media(путь от файла docker-compose.yml) на хосте мэпится в папку /code/media в контейнере. Это значит, при запуске docker-copose up
     папка содержимое папки /code/media удаляется. И это папка ссылается на папку ./media на хосте. В дальнейшем контейнер работает с папкой хоста.
     После остановки контейнера вся информация остается на хосте и восстанавливается при restart. Файлы, созданные в контейнере имеют
     пользователя root.
    - раздел links в docker-compose.yml deprecated, вместо него depends_on
    - раздел build в в docker-compose.yml можно оставить только если работаешь локально или в папке откуда идет запуск находятся файлы проекта.
    - На сервере проект работает http://192.168.0.105:8000/datalab/dataset/

7) Внесение изменения в application. Если мы не хотим терять базу, но необходимо перебилдить web конетейнер.
Тогда нужно остановить и удалить конейнер и образ (web).
Выполнить команду docker-compose up --no-deps web
где image shugarev1974/django-sklearn_v2 стянется из репозитория, произойдет build, и создастя и запустится контейнер web.
  web:
    image: shugarev1974/django-sklearn_v2

docker-compose.yml содержит два контейнера.
Для того, чтобы в web контейнере выполнились миграции вначале должен полностью прогрузиться
контейнер db(db - загружает mysql в контейнер). Порядок загузки указан в разделе depends on.


Список команд:
docker images - список образов. ( docker history image_name - посмотреть историю запуска образов, пример docker history mysql:5.7)
docker ps  - список работающих контейнеров.
docker exec -it 72ca2488b353 bash - зайти внутрь работающего контейнера
docker ps -a список всех конейнеров.
docker rmi img_hash удалить образ.
docker rm container_hash удалить контейнер.
docker rm $( docker ps -a -q -f status=exited) -удалить все остановленные контейнеры.

docker-copose up - создание и запуск всех контейнеров находящися в файле docker-compost.yml
docker-compose run db -d  - создание и запуск контейнера db (из файла docker-compost.yml), демон.
docker-compose run web -d - создание и запуск контейнера web (из файла docker-compost.yml), демон.
docker-compose down - остановливает и удаляет контейнеры запущенные текущим docker-compose

docker run image_id - создать контейнер из image

docker login залогиниться в репозитории(https://hub.docker.com login: shugarev1974,)
docker push shugarev1974/evaluation-service1414  запушить image в репозиторий https://hub.docker.com
docker pull  shugarev1974/evaluation-service1414 cтянуть из репозитория
docker logs container_id -f - запуск вывода лога контейнера в терминал

Для для удаления ненужных файлов из контекста создания образа можно воспользоваться файлом .dockerignore
Допускаютсясимволы шаблонов * и  ?

зайти в mysql по порту, в котором работает контейнер.
mysql -udatalab -pDatalab1414 -h127.0.0.1 -P3308
show databases;
datalab'@'172.26.0.1'

Для работы с приложениями запущенными на localhost-е по другим портам необходимо в settings.py раскомментировать
 строку 'api.middleware.MyMiddleware' и создать файл api/middleware.py  в котором изменяется header response.
 Или взаимодействовать через локальный proxy server (cors-anywhere)

Для очистки данных на сервере.
- зайти внутрь работающего контейнера mysql:5.7( см. список команд сверху)
- выполнить команды по удалению и созданию базы:
mysql --host=127.0.0.1 -P 3306 -u datalab -pDatalab1414 -e "DROP DATABASE datalab;"
mysql --host=127.0.0.1 -P 3306 -u datalab -pDatalab1414 -e "CREATE DATABASE datalab;"
(не понятно нужны ли host и port?)
- зайти внутрь работающего контейнера shugarev1974/django-sklearn_v2  ( см. список команд сверху)
- внутри контейнера выполнить bash скрипт ./clear-temporary.sh
