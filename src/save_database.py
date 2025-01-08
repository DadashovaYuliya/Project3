import json
from typing import Any

import psycopg2


def save_data_to_database(path, database_name: str, params: dict):
    """Сохранение данных о работодателях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for i in data:
            employer_data = i.get('employer')
            cur.execute(
                """
                INSERT INTO employer (name, employer_url)
                VALUES (%s, %s)
                RETURNING employer_id
                """,
                (employer_data['name'], employer_data['employer_url'])
            )

            employer_id = cur.fetchone()[0]
            vacancies_data = i['vacancies']

            for i in vacancies_data:
                cur.execute(
                     """
                    INSERT INTO vacancies (employer_id, title, salary, vacancies_url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (employer_id, i['title'], i['salary'],
                     i['url'])
                    )

    conn.commit()
    conn.close()