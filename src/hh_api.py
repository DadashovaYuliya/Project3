import requests


class HeadHunterAPI:

    def __init__(self):
        """Конструктор класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__employer_id = [
            "1942330",
            "4219",
            "78638",
            "1942336",
            "10545773",
            "2343",
            "80",
            "5919632",
            "5735829",
            "9301808",
        ]
        self.__params = {"page": 0, "per_page": 100, "employer_id": self.__employer_id}
        self.__vacancies = []

    def get_vacancies(self):
        """Функция, получающая данные по API"""
        try:
            while self.__params.get("page") != 50:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    vacancies = response.json()["items"]
                    self.__vacancies.extend(vacancies)
                    self.__params["page"] += 1
                    return self.__vacancies
        except Exception as e:
            print(f"Ошибка получения данных {e}")
            return self.__vacancies


if __name__ == "__main__":
    platforms = HeadHunterAPI()

    # Получение вакансий с hh.ru в формате JSON
    hh_vacancies = platforms.get_vacancies()
    print(hh_vacancies)
