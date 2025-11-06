from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """
    Кастомный storage для медиа файлов в DigitalOcean Spaces
    """
    location = ''  # Убираем префикс, так как upload_to уже содержит путь
    file_overwrite = False
