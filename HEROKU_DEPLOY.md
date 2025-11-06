# 🚀 Инструкция по деплою на Heroku

## 1️⃣ Пушим код на Heroku

```bash
cd backend

# Подключаем Heroku remote (если еще не подключено)
heroku git:remote -a su-college-back-0fa585fe0710

# Пушим код
git push heroku main
```

## 2️⃣ Устанавливаем переменные окружения

```bash
# Django настройки
heroku config:set DJANGO_SECRET_KEY="your-secret-key-change-this"
heroku config:set DJANGO_DEBUG=False

# DigitalOcean Spaces
heroku config:set USE_SPACES=True
heroku config:set SPACES_KEY=DO801GKT8RCG29U793F8
heroku config:set SPACES_SECRET=Ykc9Pa08PUCkn8VHOIFDHWpaXxjgZWfuPRcJI82KUZQ
heroku config:set SPACES_NAME=su-college
heroku config:set SPACES_REGION=blr1
heroku config:set SPACES_ENDPOINT=https://blr1.digitaloceanspaces.com

# Проверяем
heroku config
```

## 3️⃣ Применяем миграции

```bash
heroku run python manage.py migrate
```

## 4️⃣ Создаем суперпользователя

```bash
heroku run python manage.py createsuperuser
```

## 5️⃣ Собираем статику

```bash
heroku run python manage.py collectstatic --noinput
```

## 6️⃣ Экспорт данных из SQLite

```bash
# Локально экспортируем данные в JSON
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --indent 2 > data_dump.json

# Или экспортируем только определенные приложения
python manage.py dumpdata teachers news_app council_app projects_app resources_app vacancies_app schedule_app --natural-foreign --natural-primary --indent 2 > data_dump.json
```

## 7️⃣ Импорт данных в Heroku PostgreSQL

```bash
# Загружаем файл на Heroku (используя heroku run)
# Сначала копируем файл в репозиторий (временно)
git add data_dump.json
git commit -m "Add data dump"
git push heroku main

# Загружаем данные
heroku run python manage.py loaddata data_dump.json

# Удаляем файл из репозитория после импорта
git rm data_dump.json
git commit -m "Remove data dump"
git push heroku main
```

## 8️⃣ Мигрируем медиа файлы в Spaces

```bash
# Запускаем скрипт миграции на Heroku
heroku run python migrate_media_to_spaces.py
```

## 9️⃣ Проверка

```bash
# Открываем сайт
heroku open

# Смотрим логи
heroku logs --tail

# Заходим в админку
heroku open /admin
```

## 🔍 Полезные команды

```bash
# Подключиться к Heroku bash
heroku run bash

# Подключиться к PostgreSQL
heroku pg:psql

# Сбросить БД (ОСТОРОЖНО!)
heroku pg:reset DATABASE_URL --confirm su-college-back-0fa585fe0710

# Создать бэкап БД
heroku pg:backups:capture

# Скачать бэкап
heroku pg:backups:download

# Рестарт приложения
heroku restart
```

## ⚠️ Важно

1. **Не забудьте сменить SECRET_KEY** на продакшене
2. **Файлы медиа** будут храниться в DigitalOcean Spaces, не на Heroku
3. **База данных** - PostgreSQL на Heroku (автоматически создается)
4. **Статика** раздается через Whitenoise
