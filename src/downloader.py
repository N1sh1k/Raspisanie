import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScheduleDownloader:
    """Загрузка актуального файла"""

    def __init__(self, base_page_url, destination_path):
        # Теперь передаем ссылку не на файл, а на СТРАНИЦУ с кнопкой
        self.base_page_url = base_page_url 
        self.destination_path = destination_path

    def _get_actual_url(self):
        """Парсинг страницы и поиск актуальной ссылки на .xls файл"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.base_page_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Поиск всех ссылок на странице
            for a in soup.find_all('a', href=True):
                href = a['href']
                # Если ссылка содержит '.xls' или просто .xls
                if '.xls' in href.lower():
                    # Превращаем относительную ссылку в полную
                    full_url = urljoin(self.base_page_url, href)
                    print(f"Найдена актуальная ссылка: {full_url}")
                    return full_url
            return None
        except Exception as e:
            print(f"Ошибка поиска ссылки: {e}")
            return None

    def download(self):
        """Поиск ссылки и загрузка файла"""
        actual_url = self._get_actual_url()
        if not actual_url:
            return False

        try:
            print(f"Попытка скачивания...")
            response = requests.get(actual_url, stream=True, timeout=30)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
            with open(self.destination_path, 'wb') as f:
                f.write(response.content)
            print(f"Файл успешно сохранен")
            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False