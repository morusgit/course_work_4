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