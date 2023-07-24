import psycopg2


class DBManager:
    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        try:
            connection = psycopg2.connect(database=self.database_name, **self.params)

        except (Exception, psycopg2.DatabaseError) as error:
            return f'[INFO] {error}'

        pass
