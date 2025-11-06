# 🚀 Инструкция по настройке DigitalOcean Spaces для медиа

## 1️⃣ Создайте Space в DigitalOcean

1. Зайдите в DigitalOcean → Spaces
2. Создайте новый Space (например, `su-college-media`)
3. Выберите регион (например, `nyc3`)
4. Сохраните название и регион

## 2️⃣ Получите API ключи

1. Перейдите в API → Spaces Keys
2. Создайте новый ключ (Generate New Key)
3. Сохраните:
   - **Access Key** (SPACES_KEY)
   - **Secret Key** (SPACES_SECRET)

## 3️⃣ Настройте CORS для Space

В настройках вашего Space добавьте CORS правило:

```json
[
  {
    "AllowedOrigins": ["*"],
    "AllowedMethods": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3000
  }
]
```

## 4️⃣ Установите переменные окружения на Heroku

```bash
heroku config:set USE_SPACES=True
heroku config:set SPACES_KEY=your-access-key
heroku config:set SPACES_SECRET=your-secret-key
heroku config:set SPACES_NAME=su-college-media
heroku config:set SPACES_REGION=nyc3
heroku config:set SPACES_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

## 5️⃣ Для локальной разработки

Создайте файл `.env` в папке backend:

```env
USE_SPACES=False
```

Или если хотите тестировать с Spaces локально:

```env
USE_SPACES=True
SPACES_KEY=your-access-key
SPACES_SECRET=your-secret-key
SPACES_NAME=su-college-media
SPACES_REGION=nyc3
SPACES_ENDPOINT=https://nyc3.digitaloceanspaces.com
```

## 6️⃣ Установите зависимости

```bash
pip install -r requirements.txt
```

## 📝 Как это работает

- **Локально (USE_SPACES=False)**: медиа сохраняются в папку `media/`
- **На Heroku (USE_SPACES=True)**: медиа загружаются в DigitalOcean Spaces
- **Статика**: всегда обслуживается через Whitenoise (нет смысла грузить в Spaces)

## 🔍 Проверка

После загрузки файла через Django Admin, URL должен быть примерно таким:
```
https://su-college-media.nyc3.digitaloceanspaces.com/media/teachers/photo.jpg
```

## ⚠️ Важно

- Spaces работает как AWS S3 (S3-compatible API)
- Не забудьте настроить CORS
- Файлы станут публично доступны (ACL = public-read)
