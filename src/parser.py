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
        for r in range(min(len(df), 25)): 
            row_values = [str(val) for val in df.iloc[r].tolist()]
            row_str = " ".join(row_values)
            if row_str.count("-") > 5: 
                group_row_idx = r
                break
        
        groups_header = [str(g).strip() for g in df.iloc[group_row_idx].tolist()]
        print(f"Заголовок групп найден на строке {group_row_idx + 1}")

        # Перебор строк
        for row_idx in range(group_row_idx + 1, len(df)):
            row_data = df.iloc[row_idx]
            
            # Проверка названий
            row_start_text = " ".join([str(val) for val in row_data.iloc[:5].tolist()])
            new_day = next((day for day in days_list if day in row_start_text), None)
            
            if new_day:
                current_day = new_day
                print(f"Раздел: {current_day}")
                continue

            pair_num_raw = str(row_data.iloc[1]).strip()
            slot = pair_num_raw if pair_num_raw.isdigit() and len(pair_num_raw) == 1 else "1"

            # Перебор столбцов
            for col_idx, group_name in enumerate(groups_header):
                if "-" not in group_name or "nan" in group_name.lower():
                    continue

                lesson_raw = df.iloc[row_idx, col_idx]
                lesson = str(lesson_raw).strip()
                
                if lesson and lesson.lower() != 'nan' and len(lesson) > 4:
                    result.append({
                        "day": current_day,
                        "group": group_name,
                        "lesson": lesson.replace('\n', ' '),
                        "slot": slot
                    })

        print(f"Собрано занятий: {len(result)}")
        return result