import json


class Vacancy:
    """
    Класс, представляющий информацию о вакансии на платформе HeadHunter
    """
    hh_list_of_objects = []  # список объектов из HeadHunter

    def __init__(self, name, salary, reqs, responsibilities, area, employer, url):
        """
        Создает объект с информацией о вакансии

        :param name: название вакансии
        :param salary: зарплата
        :param reqs: требования
        :param responsibilities: обязанности
        :param area: город вакансии
        :param employer: работодатель
        :param url: ссылка на вакансию
        """
        self.name = name
        self.salary = salary
        self.reqs = reqs
        self.responsibilities = responsibilities
        self.area = area
        self.employer = employer
        self.url = url

    @classmethod
    def hh_create_list_of_objects(cls, file):
        """
        Создает список объектов Vacancy из файла с данными

        :param file: файл с данными
        """
        with open(file, encoding='utf-8') as vacancies:
            python_type_vacancies = json.load(vacancies)
            for vacancy in python_type_vacancies:
                if vacancy['salary'] is not None:
                    name = vacancy['name']
                    salary = vacancy['salary']
                    reqs = vacancy['snippet']['requirement']
                    responsibilities = vacancy['snippet']['responsibility']
                    area = vacancy['area']['name']
                    employer = vacancy['employer']['name']
                    url = f'https://hh.ru/vacancy/{vacancy["id"]}'
                    cls.hh_list_of_objects.append(cls(name, salary, reqs, responsibilities, area, employer, url))

    def __str__(self):
        salary_str = f'От {self.salary["from"]} до {self.salary["to"]} {self.salary["currency"]}' if self.salary else 'Не указано'
        reqs_str = self.reqs if self.reqs else 'Не указаны'

        return f' |Вакансия: {self.name}\nЗарплата: {salary_str}\nТребования: {reqs_str}\n' \
               f'Город: {self.area}\nРаботодатель: {self.employer}\nСсылка: {self.url}\n'