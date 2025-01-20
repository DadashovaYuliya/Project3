from src.config import config
from src.database import create_database
from src.DBManager import DBManager
from src.hh_api import HeadHunterAPI
from src.save_database import save_data_to_database
from src.save_json import add_vacancy


def main():
    params = config()

    platforms = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = platforms.get_vacancies()
    create_database("vacancies", params)

    # Сохранение информации о вакансиях в файл
    json_saver = add_vacancy("data/vacancies.json", hh_vacancies)

    # Сохранение информации о вакансиях в базу данных
    save_data_to_database("data/vacancies.json", "vacancies", params)

    # Взаимодействие с пользователем
    db_manager = DBManager("vacancies", params)

    user_input = input(
        "Давайте найдем для Вас подходящую вакансию. Вывести количество вакансий в выбранных компаниях?"
    )
    if user_input == "да":
        vacancies_count = db_manager.get_companies_and_vacancies_count()
        print(vacancies_count)

    user_input = input("Вывести все вакансии в выбранных компаниях?")
    if user_input == "да":
        vacancies_count = db_manager.get_all_vacancies()
        print(vacancies_count)

    user_input = input("Вывести среднюю заработную плату по вакансиям в выбранных компаниях?")
    if user_input == "да":
        vacancies_count = db_manager.get_avg_salary()
        print(vacancies_count)

    user_input = input("Вывести только вакансии с заработной платой выше средней?")
    if user_input == "да":
        vacancies_count = db_manager.get_vacancies_with_higher_salary()
        print(vacancies_count)

    user_input = input("Введите слово для поиска в вакансиях: ")
    vacancies_count = db_manager.get_vacancies_with_keyword(user_input)
    print(vacancies_count)


if __name__ == "__main__":
    main()
