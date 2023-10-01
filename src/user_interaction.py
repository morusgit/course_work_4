from src.api_classes import HHApi, SuperJobApi
from src.json_operations import JsonFileHandler
from src.vacancy import Vacancy


def user_interaction():
    """
    Функция, реализущая взаимодействие с пользователем.
    Пользователь выбирает платформу, ключевое слово, страницу сайта
    Фунцкция сортирует полученные данные по зарплате, и пользователь указывает какое количество вакансий вывести
    Также происходит сортировка город, который также определяется пользователем
    Для платформы HeadHunter выводится информация по зарубежным вакансиям.
    """

    # запрос от пользователя для ввода платформы, ключевого слова, номера страницы для получения данных
    input_platform = input('Введите ключевое слово для поиска вакансии на сайте (HeadHunter/SuperJob): ')
    if input_platform not in ['hh', 'HH', 'headhunter', 'HeadHunter', 'sj', 'SJ', 'Super', 'SuperJob']:
        quit('С такой платформой работать пока не умею')
    else:
        input_keyword = input('Введите ключевое слово для поиска вакансии на сайте HeadHunter: ')
        input_page_number = int(
        input('С какой страницы получать информацию? Для получения самых свежих данных укажите 0: '))
        input_top_number = int(input('Сколько вакансий с самой высокой оплатой труда показать? (Только для RU-региона): '))
        input_area = input('Для какого города получить список вакансий? ')

    if input_platform in ['hh', 'HH', 'headhunter', 'HeadHunter']:
        hh_vacancies = HHApi(input_page_number, input_keyword).get_info_from_site()
        JsonFileHandler('vacancies_from_hh.json', hh_vacancies).write_info()
        Vacancy.hh_create_list_of_objects('vacancies_from_hh.json')
        input_region = input(
            'Отобразить доступные вакансии из зарубежных государств и вакансии с релокацией?(Да/Нет): ')

        if input_region == 'Да':
            hh_foreign_vacancies = [vacancy for vacancy in Vacancy.hh_list_of_objects if
                                    vacancy.salary['currency'] != 'RUR']
            print('\nДоступные вакансии зарубежом и вакансии с релокацией:')
            for job in hh_foreign_vacancies:
                print(f'{job}\n')

        hh_list = [vacancy for vacancy in Vacancy.hh_list_of_objects if vacancy.salary['to'] is not None and
                   vacancy.salary['currency'] == 'RUR']
        hh_list.sort(key=lambda x: x.salary['to'], reverse=True)
        print('Топ вакансий:\n')
        for vacancy in hh_list[:input_top_number]:
            print(vacancy)

        hh_sorted_area = [work for work in Vacancy.hh_list_of_objects if work.area == input_area]
        if len(hh_sorted_area) == 0:
            print('В этом городе вакансий нет')
        else:
            print('В указанном городе есть следующие вакансии: ')
            for work_in_city in hh_sorted_area:
                print(work_in_city)

    elif input_platform in ['sj', 'SJ', 'Super', 'SuperJob']:
        sj_vacancies = SuperJobApi(input_page_number, input_keyword).get_info_from_site()
        JsonFileHandler('vacancies_from_sj.json', sj_vacancies).write_info()
        Vacancy.sj_create_list_of_objects('vacancies_from_sj.json')

        sj_list = [vacancy for vacancy in Vacancy.sj_list_of_objects if vacancy.salary['to'] != 0
                   and vacancy.salary['currency'] == 'rub']
        sj_list.sort(key=lambda x: x.salary['to'], reverse=True)
        print('\nТоп вакансий:')
        for vacancy_ in sj_list[:input_top_number]:
            print(vacancy_)

        sj_sorted_area = [work for work in Vacancy.sj_list_of_objects if work.area == input_area]
        if len(sj_sorted_area) == 0:
            print('В указанном городе вакансий нет')
        else:
            print('В указанном городе есть следующие вакансии: ')
            for work_in_city_ in sj_sorted_area:
                print(work_in_city_)
