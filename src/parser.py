import pandas as pd

class ScheduleParser:
    """Обработка сетки расписания"""
    def __init__(self, file_path):
        """Инициализация парсера :param file_path: путь к скачанному файлу"""
        self.file_path = file_path

    def get_clean_data(self):
        """Чтение файла и удаление пустых строк"""
        df = pd.read_excel(self.file_path, engine='xlrd', header=None)
        return df

    def parse(self):
        """Разбор сетки файла"""
        df = self.get_clean_data()
        schedule = []

        for col_idx in range(2, df.shape[1]):
            group_name = str(df.iloc[7, col_idx]).strip()
            
            if len(group_name) < 2 or "nan" in group_name.lower():
                continue

            for row_idx in range(9, len(df)):  # Пары начинаются ниже
                lesson = str(df.iloc[row_idx, col_idx]).strip()
                
                if lesson and "nan" not in lesson.lower():
                    # Сбор данных
                    schedule.append({
                        "group": group_name,
                        "lesson": lesson,
                        "row": row_idx,
                        "col": col_idx
                    })
        
        return schedule