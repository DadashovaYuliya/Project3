import json
import os


def add_vacancy(file_name: str, vacancies: dict):
    """Функция для добавления вакансий в файл json"""
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(file_name, "r+", encoding="utf-8") as f:
        try:
            file_vacancies = json.load(f)
        except json.JSONDecodeError:
            file_vacancies = []

    for vacancy in vacancies:
        dict_employer = {
            "name": vacancy.get("employer").get("name"),
            "employer_url": vacancy.get("employer").get("url"),
        }

        if vacancy.get("salary"):
            valid_salary = vacancy.get("salary").get("from")
        else:
            valid_salary = 0

        dict_vacancy = {
            "title": vacancy.get("name"),
            "salary": valid_salary,
            "url": vacancy.get("url"),
        }

        employer_exists = False
        for i in file_vacancies:
            if i["employer"] == dict_employer:
                employer_exists = True
                # Добавляем вакансию к существующему работодателю

                i["vacancies"].append(dict_vacancy)
                break

        # Если работодателя нет, добавляем новый словарь
        if not employer_exists:
            file_vacancies.append({"employer": dict_employer, "vacancies": [dict_vacancy]})

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(file_vacancies, f, ensure_ascii=False, indent=4)
