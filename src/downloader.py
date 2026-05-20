import requests
import os

class ScheduleDownloader:
    """Загрузка файла по URL-ссылке"""

    def __init__(self, url, destination_path):
        """
        :param url: ссылка на файл
        :param destination_path: куда сохранить (data/schedule.xls)
        """
        self.url = url
        self.destination_path = destination_path

    def download(self):
        """HTTP-запрос и сохранение на диск"""
        print(f"Попытка скачивания: {self.url}...")
        try:
            # Установка заголовков
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            
            # Проверяем, что запрос успешный (код 200)
            response.raise_for_status()
            
            # Создаем папку, если её нет
            os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
            
            with open(self.destination_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Файл скачан и сохранен в {self.destination_path}")
            return True
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
            return False