# Django Supply Chain Management

Это веб-приложение, созданное с использованием Django и Django REST Framework, представляет собой систему управления
цепочкой поставок. Приложение позволяет управлять иерархической структурой сущностей (заводы, розничные сети,
индивидуальные предприниматели), а также управлять продуктами и контактами этих сущностей.

## Начало работы

Эти инструкции помогут вам получить копию проекта и запустить его на локальной машине для разработки и тестирования.

### Предварительные требования

Для запуска этого проекта вам понадобятся:

- Python 3.8+
- Django 3+
- Django REST Framework 3.10+
- PostgreSQL 10+

### Установка

Шаги для запуска проекта на локальной машине:

1. Клонируйте репозиторий:
   git clone https://github.com/maximshurygin/test_task_ck

2. Перейдите в директорию проекта:
   cd test_task_ck

3. Установите необходимые зависимости:
   pip install -r requirements.txt

4. Создайте и заполните файл .env по примеру как в .env.sample

5. Выполните миграции:
   python manage.py migrate

6. Запустите сервер разработки:
   python manage.py runserver

## Запуск тестов

Для запуска тестов выполните команду:

python manage.py test

## Использованные технологии

- [Django](https://www.djangoproject.com/) - основной веб-фреймворк
- [Django REST Framework](https://www.django-rest-framework.org/) - фреймворк для создания API
- [PostgreSQL](https://www.postgresql.org/) - система управления базами данных

## Авторы

* **Шурыгин Максим**  [https://github.com/maximshurygin/](https://github.com/maximshurygin/)


