# Продуктовый сайт Foodgram

### Описание проекта:
Cайт Foodgram даёт возможность публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а также скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Тестовый проект доступен по адресу :
https://barabulka.sytes.net/
Админка:
login: admin / password: a

### Как запустить проект:
Клонируйте репозиторий, перейдите в директорию с проектом:

В корневой директории создайте файл .env и заполните следующими данными для базы данных (например):
```
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432

```

Запустите контейнер в корневой директории директории :

```
docker compose up 
```

Выполните по очереди команды (во втором git bash окне , в корневой директории):

```
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic

(Создание Админки)
docker container ls (получите и скопируйте ID контейнера foodgram-project-react-backend)
winpty docker exec -ti <номер контейнера> bash
python manage.py createsuperuser

(Следующие команды по желанию  , для заполнения базу данных заранее подготовленными данными)
docker compose exec backend python manage.py load_ing (подгрузка ингредиентов)
docker compose exec backend python manage.py load_tags (подгрузка тэгов)
docker compose exec backend python manage.py load_recipes (подгрузка 10 тестовых рецептов)
```

После запуска , сайт будет доступен по адресу:

```
http://localhost/
```
После запуска проекта документация доступна по адресу:

```
http://localhost/api/docs/
```

