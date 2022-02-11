# Онлайн кинотеатр
Демо проект для **Яндекс.Практикум**.

## Запуск проекта

### Конфигурация
Создать файлы с переменными окружения из следующих примеров:
```shell
cp deploy/admin_panel/example.env deploy/admin_panel/.env
cp deploy/db/example.env deploy/db/.env
cp deploy/ps_to_es/example.env deploy/ps_to_es/.env
```

### Установка
Выполнить следующие команды из корневой директории проекта:
```shell
docker-compose -f docker-compose.yml down -v
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec admin_panel python manage.py collectstatic --no-input --clear
docker-compose -f docker-compose.yml exec admin_panel python manage.py migrate --fake movies 0001
docker-compose -f docker-compose.yml exec admin_panel python manage.py makemigrations
docker-compose -f docker-compose.yml exec admin_panel python manage.py migrate
docker-compose -f docker-compose.yml exec admin_panel python manage.py createsuperuser --noinput
docker-compose -f docker-compose.yml exec admin_panel python manage.py loaddata /home/app/fixtures.json.gz
```

## Что потыкать?
### Django:
Простенький рест на джанге с первого спринта:
 - http://localhost/django_api/v1/movies/01ab9e34-4ceb-4337-bb69-68a1b0de46b2
 
Админка джанги (логин: `admin`, пароль: `password`)
 - http://localhost/admin

### Kibana:
 - http://localhost/kibana
 
### FastAPI:
 - http://localhost/api/openapi
 

## Django - панель администратора
### Доступ к административной панели
Суперпользователь создается на основе конфигов из `deploy/web/.env`
```ini
...
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=password
DJANGO_SUPERUSER_EMAIL=mail@example.com
...
```

### Проверка корректной установки
```shell
curl -X GET --location "http://localhost/django_api/v1/movies/01ab9e34-4ceb-4337-bb69-68a1b0de46b2"
```
Ответ:
```json
{
  "id": "01ab9e34-4ceb-4337-bb69-68a1b0de46b2",
  "title": "Axl Rose: The Prettiest Star",
  "description": "A biography of Axl Rose.",
  ...
}
```
