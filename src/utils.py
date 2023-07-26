import requests
import psycopg2


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
        string = string.replace(symbol, '')

    return string


def filter_salary(salary):
    if salary is not None:
        if salary['from'] is not None and salary['to'] is not None:
            return round((salary['from'] + salary['to']) / 2)
        elif salary['from'] is not None:
            return salary['from']
        elif salary['to'] is not None:
            return salary['to']
    return None


def create_db(database_name, params):
    connection = psycopg2.connect(database='postgres', **params)
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(f'DROP DATABASE {database_name}')
        cursor.execute(f'CREATE DATABASE {database_name}')

    connection.close()


def create_tables(database_name, params):
    connection = psycopg2.connect(database=database_name, **params)

    with connection.cursor() as cursor:
        cursor.execute('CREATE TABLE companies('
                       'company_id serial PRIMARY KEY,'
                       'company_name varchar(50) NOT NULL,'
                       'description text,'
                       'link varchar(200) NOT NULL,'
                       'url_vacancies varchar(200) NOT NULL)')

        cursor.execute('CREATE TABLE vacancies('
                       'vacancy_id serial PRIMARY KEY,'
                       'company_id int REFERENCES companies (company_id) NOT NULL,'
                       'title_vacancy varchar(150) NOT NULL,'
                       'salary int,'
                       'link varchar(200) NOT NULL,'
                       'description text,'
                       'experience varchar(70))')

    connection.commit()
    connection.close()


def fill_db(employers: list[dict], database_name, params):
    connection = psycopg2.connect(database=database_name, **params)

    with connection.cursor() as cursor:
        for employer in employers:
            cursor.execute('INSERT INTO companies (company_name, description, link, url_vacancies)'
                           'VALUES (%s, %s, %s, %s)'
                           'returning company_id',
                           (employer["company"].get("name"),
                            filter_strings(employer["company"].get("description")),
                            employer["company"].get("alternate_url"),
                            employer["company"].get("vacancies_url")))

            company_id = cursor.fetchone()[0]

            for vacancy in employer["vacancies"]:
                salary = filter_salary(vacancy["salary"])
                cursor.execute('INSERT INTO vacancies'
                               '(company_id, title_vacancy, salary, link, description, experience)'
                               'VALUES (%s, %s, %s, %s, %s, %s)',
                               (company_id, vacancy["name"], salary,
                                vacancy["alternate_url"], vacancy["snippet"].get("responsibility"),
                                vacancy["experience"].get("name")))

    connection.commit()
    connection.close()
