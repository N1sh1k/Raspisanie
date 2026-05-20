import json
import shutil
from src.downloader import ScheduleDownloader
from src.parser import ScheduleParser

def main():
    url = "https://t706222.spo.obrazovanie33.ru/upload/site_files/22/8%20апреля.xls" 
    input_path = "data/schedule.xls"
    output_json = "data/result.json"

    # Скачивание
    print("=== ШАГ 1: Скачивание файла ===")
    downloader = ScheduleDownloader(url, input_path)
    if downloader.download():
        # Парсинг
        print("\n=== ШАГ 2: Парсинг данных ===")
        parser = ScheduleParser(input_path)
        data = parser.parse()

        # Сохранение
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Результат в {output_json}")

        # Синхронизация данных с веб-интерфейсом только если загрузилось
        shutil.copy(output_json, "web/result.json")
        print(f"Данные синхронизированы с веб-интерфейсом в web/result.json")
    else:
        print("Ошибка загрузки")


if __name__ == "__main__":
    main()