#Учебный проект Продктовый Помощник

#Описание
Проект foodgram - сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

#Технологии
Python 3.10
Django 4.0.6
Django REST 3.12.4

#Запуск с помощью Doker
#Описание команд для запуска приложения в контейнерах:

Установить Doker:
Вся информация по установке Doker на сайте https://docs.docker.com/

Через консоль перейти в каталог приложения infra:
cd infra/

Обратите внимание на файл .env с секретными данными:
SECRET_KEY = <серетный ключ Джанго>
DB_NAME = <имя базы данных>
POSTGRES_USER = <имя пользователя базы данных>
POSTGRES_PASSWORD = <пароль от базы данных>
DB_PORT = <номер порта>

Собрать и запустить все сервисы командой:
docker-compose up -d

Подготовить и запустить миграции:
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

Собрать статику:
docker-compose exec backend python manage.py collectstatic --no-input

Создать администратора:
docker-compose exec backend python manage.py createsuperuser

Готово!
Сайт запущен по адресу localhost в адресной строке браузера

Ознакомиться с пользовательскими командами апи можно по ссылке localhost\redoc\

Загрузить тестовые данные можно предварительно скопируя их в контейнер:
docker-compose exec backend python manage.py loaddata fixtures.json

Остановить сервисы можно командой:
docker-compose stop

Автор проекта:
Алферов Антон email: anton.alferov@icloud.com
