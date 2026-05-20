import os
import pytest
from src.parser import ScheduleParser
from src.downloader import ScheduleDownloader

def test_downloader_init():
    """Проверка правильной инициализации загрузчика"""
    url = "https://t706222.spo.obrazovanie33.ru/upload/site_files/22/8%20апреля.xls"
    path = "data/test.xls"
    downloader = ScheduleDownloader(url, path)
    
    assert downloader.url == url
    assert downloader.destination_path == path

def test_parser_init():
    """Проверка правильной инициализации парсера"""
    path = "data/schedule.xls"
    parser = ScheduleParser(path)
    
    assert parser.file_path == path

def test_parsing_result_type():
    """Проверка логики структуры"""
    path = "data/schedule.xls"
    if os.path.exists(path):
        parser = ScheduleParser(path)
        data = parser.parse()
        assert isinstance(data, list)
    else:
        # Если файла нет - тест пропускается 
        pytest.skip("Файл расписания не найден для теста")

def test_folder_structure():
    """Проверка наличия необходимых папок проекта"""
    assert os.path.exists("src/")
    assert os.path.exists("data/")