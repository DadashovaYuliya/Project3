from src.config import config
from src.database import create_database
from src.hh_api import HeadHunterAPI
from src.save_database import save_data_to_database
from src.save_json import add_vacancy


def main():
    params = config()

    platforms = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = platforms.get_vacancies()
    create_database('vacancies', params)

    # Сохранение информации о вакансиях в файл
    json_saver = add_vacancy("data/vacancies.json", hh_vacancies)

    save_data_to_database("data/vacancies.json", 'vacancies', params)


if __name__ == '__main__':
    main()