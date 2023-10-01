from src.api_classes import HHApi
from src.json_operations import JSon
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
    input_keyword = input('Введите ключевое слово для поиска вакансии на сайте HeadHunter: ')
    input_page_number = int(
        input('С какой страницы получать информацию? Для получения самых свежих данных укажите 0: '))
    input_top_number = int(input('Сколько вакансий с самой высокой оплатой труда показать? (Только для RU-региона): '))
    input_area = input('Для какого города получить список вакансий? ')

    try:
        # получение информации с сайта
        hh_vacancies = HHApi(input_page_number, input_keyword).get_info_from_site()
    except Exception as e:
        print("Возникла ошибка при получении данных с сайта: ", e)
        return

    JSon('vacancies_from_hh.json', hh_vacancies).write_info()
    Vacancy.hh_create_list_of_objects('vacancies_from_hh.json')

    # запрос от пользователя для выбора зарубежных вакансий
    input_region = input('Показать доступные вакансии за рубежом и вакансии с возможностью переезда? (Да/Нет): ')
    if input_region.lower() == 'да':
        hh_foreign_vacancies = [vacancy for vacancy in Vacancy.hh_list_of_objects if
                                vacancy.salary['currency'] != 'RUR']

        print('\nДоступны следующие вакансии за рубежом и вакансии с возможностью переезда:')
        for job in hh_foreign_vacancies:
            print(f'{job}\n')

    hh_list = [vacancy for vacancy in Vacancy.hh_list_of_objects if
               vacancy.salary['to'] is not None and vacancy.salary['currency'] == 'RUR']
    hh_list.sort(key=lambda x: x.salary['to'], reverse=True)

    print('Список вакансий с наибольшим уровнем оплаты труда:\n')
    for vacancy in hh_list[:input_top_number]:
        print(vacancy)

    hh_sorted_area = [work for work in Vacancy.hh_list_of_objects if work.area == input_area]

    if not hh_sorted_area:
        print('Вакансий по заданному городу не найдено')
        print("1. Промотр текущих вакансий")
        print("2. Просмотр архивных вакансий")

        choice = input("Сделайте выбор: ")

        if choice == '1':
            vacancies = HHApi.get_vacancies()
            print('\n'.join(map(str, vacancies)))
        elif choice == '2':
            vacancies = JSon('vacancies_from_hh.json', hh_vacancies).get_archived_vacancies()
            print('\n'.join(map(str, vacancies)))
        else:
            print("Неверный выбор")
    else:
        print('Список вакансий по заданному городу: ')
        for work_in_city in hh_sorted_area:
            print(work_in_city)
