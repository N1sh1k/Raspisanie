import pandas as pd

class ScheduleParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        df = pd.read_excel(self.file_path, engine='xlrd', header=None)
        result = []
        
        days_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        current_day = "Неизвестно"
        
        # Поиск групп
        group_row_idx = 7 
        groups = df.iloc[group_row_idx, :].tolist()
        
        for row_idx in range(group_row_idx + 1, len(df)):
            # Проверка
            first_col_val = str(df.iloc[row_idx, 0]).strip()
            if first_col_val in days_list:
                current_day = first_col_val
                continue

            # Номер пары
            slot_raw = str(df.iloc[row_idx, 1]).strip()
            slot = slot_raw if slot_raw.isdigit() else "1"

            for col_idx, group_name in enumerate(groups):
                group_name = str(group_name).strip()
                if "-" not in group_name or len(group_name) < 3:
                    continue

                lesson_data = str(df.iloc[row_idx, col_idx]).strip()
                if lesson_data and lesson_data.lower() != 'nan' and len(lesson_data) > 3:
                    result.append({
                        "day": current_day,
                        "group": group_name,
                        "lesson": lesson_data.replace('\n', ' '),
                        "slot": slot
                    })
        return result