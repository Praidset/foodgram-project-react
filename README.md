# Продуктовый сайт Foodgram

### Описание проекта:
Cайт Foodgram даёт возможность публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а также скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Как запустить проект:
Клонируйте репозиторий, перейдите в директорию с проектом:

В директории infra/ создайте файл .env и заполните следующими данными (напрмер):
```
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432

```

Запустите контейнер в директории infra/:

```
docker-compose up 
```

Выполните по очереди команды (во втором git bash окне , в директории infra/):

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic
(Следующие команды по желанию  , для заполнения базу данных заранее подготовленными данными)
docker-compose exec backend python manage.py load_ing (подгрузка ингредиентов)
docker-compose exec backend python manage.py load_tags (подгрузка тэгов)
docker-compose exec backend python manage.py load_recipes (подгрузка 10 тестовых рецептов)
```

После запуска , сайт будет доступен по адресу:

```
http://localhost/
```
После запуска проекта документация доступна по адресу:

```
http://localhost/api/docs/
```

