# Инструкция по запуску #
> <span style="color:red">Проект рекомендуется запускать с заранее подготовленной и заполненной базой данных.</span>
> Если БД готова, то пункты 4, 5 и 6 пропустить.
> Если такая БД отсутствует, то следует выполнить следующие операции:

1. Выполнить <span style="color:orange">git clone git@github.com:CatLecter/Async_API.git</span>
2. Все необходимые пакеты указаны в <span style="color:green">pyproject.toml</span> и устанавливаются с помощью <span style="color:blue">Poetry</span>
3. Заполнить <span style="color:green">.env</span> в соответствии с шаблоном <span style="color:green">.env.sample</span> и выполнить команду <span style="color:orange">source .env</span>
4. Выполнить <span style="color:orange">docker-compose up -d postgres</span>
5. В поднятой БД создать схему и таблицы в соответствии с <span style="color:green">/schema_design/db_schema.sql</span>
6. Заполнить БД данными выполнив скрипт <span style="color:orange">cd sqlite_to_postgres && python load_data.py</span> , для чего в docker-compose.yml для сервиса <span style="color:blue">postgres</span> предварительно открыть наружу соответствующий порт (файл с данными <span style="color:green">db.sqlite</span> взять <a href="https://code.s3.yandex.net/middle-python/learning-materials/db.sqlite">тут</a> и положить в директорию <span style="color:green">/sqlite_to_postgres</span>)
7. Запустить остальные контейнеры выполнив <span style="color:orange">docker-compose build</span> и <span style="color:orange">docker-compose up -d</span>
8. <a href="http://0.0.0.0/api/openapi">Перейти</a> к Swagger документации

# Проектная работа 4 спринта

**Важное сообщение для тимлида:** для ускорения проверки проекта укажите ссылку на приватный репозиторий с командной работой в файле readme и отправьте свежее приглашение на аккаунт [BlueDeep](https://github.com/BigDeepBlue).

В папке **tasks** ваша команда найдёт задачи, которые необходимо выполнить в первом спринте второго модуля.  Обратите внимание на задачи **00_create_repo** и **01_create_basis**. Они расцениваются как блокирующие для командной работы, поэтому их необходимо выполнить как можно раньше.

Мы оценили задачи в стори поинтах, значения которых брались из [последовательности Фибоначчи](https://ru.wikipedia.org/wiki/Числа_Фибоначчи) (1,2,3,5,8,…).

Вы можете разбить имеющиеся задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**
