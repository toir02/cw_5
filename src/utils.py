import requests
import psycopg2
from config import HOST, DB_NAME, USER, PASSWORD


def get_employers(companies):
    """
    В качестве аргумента принимает список с id компаниями
    Возвращает список словарей формата
    {company:
    vacancies: }
    """
    employers = []
    for company in companies:
        url = f'https://api.hh.ru/employers/{company}'
        company_response = requests.get(url).json()
        vacancy_response = requests.get(company_response['vacancies_url']).json()
        employers.append({
            'company': company_response,
            'vacancies': vacancy_response['items']
        })

    return employers


def filter_strings(string: str) -> str:
    """
    Принимает в качестве аргумента строку
    Возвращает измененную строку без символов, прописанных в списке symbols
    """

    symbols = ['\n', '<strong>', '\r', '</strong>', '</p>', '<p>', '</li>', '<li>',
               '<b>', '</b>', '<ul>', '<li>', '</li>', '<br />', '</ul>']

    for symbol in symbols:
        string = string.replace(symbol, ' ')

    return string


def create_db():
    try:
        connection = psycopg2.connect(host=HOST,
                                      database=DB_NAME,
                                      user=USER,
                                      password=PASSWORD)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f'DROP DATABASE {DB_NAME}')
                cursor.execute(f'CREATE DATABASE {DB_NAME}')

    except (Exception, psycopg2.DatabaseError) as error:
        return f'[INFO] {error}'

    finally:
        connection.close()


def create_tables():
    try:
        connection = psycopg2.connect(host=HOST,
                                      database=DB_NAME,
                                      user=USER,
                                      password=PASSWORD)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('CREATE TABLE employees('
                               'company_id serial PRIMARY KEY,'
                               'company_name varchar(50) NOT NULL,'
                               'description text,'
                               'link varchar(200) NOT NULL,'
                               'url_vacancies varchar(200) NOT NULL)')

                cursor.execute('CREATE TABLE vacancies('
                               'vacancy_id serial PRIMARY KEY,'
                               'company_id int PRIMARY KEY REFERENCES employeers (company_id) NOT NULL,'
                               'title_vacancy varchar(150) NOT NULL,'
                               'salary int,'
                               'link varchar(200) NOT NULL,'
                               'description text,'
                               'experience varchar(70))')

    except (Exception, psycopg2.DatabaseError) as error:
        return f'[INFO] {error}'

    finally:
        connection.close()


def fill_db(employers: list[dict]):
    try:
        connection = psycopg2.connect(host=HOST,
                                      database=DB_NAME,
                                      user=USER,
                                      password=PASSWORD)
        with connection:
            for employer in employers:
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO employees (company_name, description, link, url_vacancies)'
                                   'VALUES (%s, %s, %s, %s, %s)'
                                   (employer["company"].get("name"),
                                    filter_strings(employer["company"].get("description")),
                                    employer["company"].get("alternate_url"),
                                    employer["company"].get("vacancies_url")))

    except (Exception, psycopg2.DatabaseError) as error:
        return f'[INFO] {error}'

    finally:
        connection.close()