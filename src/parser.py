import pandas as pd
import json

class ScheduleParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.target_groups = [
            "ТМ-11", "ИС-11", "ТИК-11", "ПДК-11", "ТМ-21", "ИС-21",
            "ЮДК-21", "ЭДК-21", "ТИК-21", "ТМ-31", "ТМ-32", "ТЭ-31",
            "ИС-31", "ЮД-31", "ТИК-31", "ЮДК-32", "ТМ-41", "ТЭ-41",
            "ГД-41", "ИСК-41", "ЮДК-41"
        ]

    def parse(self):
        print(f"--- Старт парсинга: {self.file_path} ---")
        df = pd.read_excel(self.file_path, engine='xlrd', header=None)
        schedule_result = {}

        # Поиск строк с группами
        header_row_idx = None
        for r in range(10):
            row_str = [str(x).strip() for x in df.iloc[r].tolist()]
            if any(g in row_str for g in self.target_groups):
                header_row_idx = r
                break
        
        if header_row_idx is None:
            print("Строка с названиями групп не найдена")
            return {}

        # Создание колонок
        groups_map = {}
        for c in range(len(df.columns)):
            val = str(df.iloc[header_row_idx, c]).strip()
            if val in self.target_groups:
                groups_map[c] = val

        # Заголовки
        current_day = "Неизвестно"
        
        for r_idx in range(header_row_idx + 1, len(df)):
            row = df.iloc[r_idx]
            
            # Дни недели
            day_cell = str(row[0]).strip()
            if day_cell and day_cell.lower() != 'nan' and len(day_cell) > 5:
                current_day = day_cell
                print(f"День: {current_day}")

            # Номер пары
            pair_raw = str(row[1]).strip()
            if not pair_raw or pair_raw.lower() == 'nan':
                continue
            
            slot = pair_raw[0] if pair_raw[0].isdigit() else "1"

            if current_day not in schedule_result:
                schedule_result[current_day] = {}

            # Сборка данных
            for col_idx, g_name in groups_map.items():
                lesson = str(row[col_idx]).strip()
                # Номер кабинета справа от предмета
                room = str(row[col_idx + 1]).strip() if col_idx + 1 < len(df.columns) else ""
                
                if lesson and lesson.lower() != 'nan' and len(lesson) > 3:
                    if g_name not in schedule_result[current_day]:
                        schedule_result[current_day][g_name] = {}
                    
                    room_txt = f"\nКаб: {room.split('.')[0]}" if room and room.lower() != 'nan' else ""
                    schedule_result[current_day][g_name][slot] = f"{lesson}{room_txt}"

        print(f"Сгруппировано данных для дней: {len(schedule_result)}")
        return schedule_result











        