import requests
import json
from abc import ABC, abstractmethod

class ApiGetter(ABC):
    def __init__(self, change_page, vacancy_name):
        """
        :param change_page: страница сайта, получаем данные
        :param vacancy_name: ключевое слово, по которому получаем вакансии
        """
        self.change_page = change_page
        self.vacancy_name = vacancy_name

    @abstractmethod
    def get_info_from_site(self):
        """
        Метод для получения данных с сайта и сохранения их в python объект
        """
        pass


class HHApi(ApiGetter):
    """
    Класс для HeadHunter
    """

    @staticmethod
    def get_vacancies():
        return HHApi(0, "Python").get_info_from_site()

    def get_info_from_site(self):
        response = requests.get("https://api.hh.ru/vacancies?page={}&per_page=100&text={}".format(self.change_page,
                                                                                                  self.vacancy_name))
        python_type = json.loads(response.text)
        vacancies_info = python_type['items']
        if len(vacancies_info) == 0:
            raise Exception('Нет информации по такому запросу ')
        return vacancies_info

class SuperJobApi(ApiGetter):
    """
    Класс для SuperJob
    """
    def get_info_from_site(self):
        header = {'X-Api-App-Id':
                  'v3.r.137847641.00c3bdb49d07ee5b0bc86e33af91fc5e8bb46604.71136f73b8e0166b8f6cd857f20835d7079223da'}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/?page={}&keyword={}&count=100'.format
                                (self.change_page, self.vacancy_name),
                                headers=header)
        python_type = json.loads(response.text)
        vacancies_info = python_type['objects']
        if len(vacancies_info) == 0:
            raise Exception('Нет информации по такой профессии')
        return vacancies_info