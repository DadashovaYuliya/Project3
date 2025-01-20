import psycopg2


class DBManager:
    """Класс взаимодействия с базой данных"""

    def __init__(self, database_name: str, params: dict):
        """Конструктор класса"""

        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute(
            """
            SELECT name, COUNT(vacancies.employer_id)
            FROM employer
            INNER JOIN vacancies USING (employer_id)
            GROUP BY name
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute(
            """
            SELECT vacancies_id, name, title, salary, vacancies_url
            FROM vacancies
            INNER JOIN employer USING (employer_id)
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute(
            """
            SELECT AVG(salary)
            FROM vacancies
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute(
            """
            SELECT vacancies_id, name, title, salary, vacancies_url
            FROM vacancies
            INNER JOIN employer USING (employer_id)
            WHERE salary >= (SELECT AVG(salary) FROM vacancies)
            ORDER BY salary DESC
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = """
            SELECT vacancies_id, name, title, salary, vacancies_url
            FROM vacancies
            INNER JOIN employer USING (employer_id)
            WHERE salary >= (SELECT AVG(salary) FROM vacancies)
            """

        filtered_vacancies = []

        if keyword:
            query += "AND (title LIKE %s OR name LIKE %s)"
            filtered_vacancies.extend([f"%{keyword}%"] * 2)

        query += "ORDER BY salary DESC"

        self.cur.execute(query, filtered_vacancies)
        return self.cur.fetchall()
