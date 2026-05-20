import pandas as pd
import json

class ScheduleParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.schedule_data = {}
        self.target_groups = [
            "ТМ-11", "ИС-11", "ТИК-11", "ПДК-11", "ТМ-21", "ИС-21",
            "ЮДК-21", "ЭДК-21", "ТИК-21", "ТМ-31", "ТМ-32", "ТЭ-31",
            "ИС-31", "ЮД-31", "ТИК-31", "ЮДК-32", "ТМ-41", "ТЭ-41",
            "ГД-41", "ИСК-41", "ЮДК-41"
        ]

    def parse(self):
        print(f"Парсинг файла: {self.file_path} ---")
        df = pd.read_excel(self.file_path, engine='xlrd', header=None)
        
        current_day = None
        groups_in_row = []
        days_list = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

        for _, row in df.iterrows():
            val = str(row[0]).strip()

            if val in days_list:
                current_day = val
                if current_day not in self.schedule_data:
                    self.schedule_data[current_day] = {}
                continue

            if val == "Пара":
                # Считывание пар
                groups_in_row = [str(g).strip() for g in row[1:]]
                for g in groups_in_row:
                    if g in self.target_groups and g not in self.schedule_data[current_day]:
                        self.schedule_data[current_day][g] = {}
                continue

            if val.isdigit() and current_day:
                slot_num = str(val) # номер пары
                for i, group_name in enumerate(groups_in_row):
                    if group_name in self.target_groups:
                        lesson_info = str(row[i + 1]).strip()
                        if lesson_info and lesson_info.lower() != 'nan' and len(lesson_info) > 4:
                            self.schedule_data[current_day][group_name][slot_num] = lesson_info

        print(f"Найдено групп с уроками: {len(self.schedule_data.get('Понедельник', {}))}")
        return self.schedule_data