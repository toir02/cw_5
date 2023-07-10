import requests


class HeadHunterAPI:
    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self):
        vacancies = []
        url = 'https://api.hh.ru/vacancies/'
        for page in range(10):
            params = {
                'per_page': 100,
                'page': page,
                'text': self.keyword,
                'archive': False
            }
            vacancies.append(requests.get(url, params=params).json())
        return vacancies
