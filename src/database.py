import psycopg2


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employer (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employer(employer_id),
                title VARCHAR NOT NULL,
                salary INTEGER,
                vacancies_url TEXT
            )
        """)

    conn.commit()
    conn.close()