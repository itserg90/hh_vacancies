from src.class_api import ApiVacanciesHh
from src.class_json import JSONSaver
from src.class_vacancy import Vacancy

import re


def filter_vacancies(vacancies: list, words: list):
    """Фильтр по ключевым словам в описании"""
    if not words:
        return vacancies
    current_vacancies = []
    for vacancy in vacancies:
        if any(word.lower() in vacancy.requirements.lower() for word in words):
            current_vacancies.append(vacancy)
    return current_vacancies


def get_vacancies_by_salary(vacancies: list, salary: str):
    """Фильтр по желаемой зарплате"""
    if not salary:
        return vacancies
    current_vacancies = []
    current_salary = re.split(r"\D", salary)
    user_salary_from = int(current_salary[0])
    for vacancy in vacancies:
        if not vacancy.salary == "Зарплата не указана":
            salary_from = vacancy.salary["from"]
            salary_to = vacancy.salary["to"]
            if salary_from and user_salary_from <= salary_from:
                current_vacancies.append(vacancy)
            elif salary_to and user_salary_from <= salary_to:
                current_vacancies.append(vacancy)
    return current_vacancies


def sort_vacancies(vacancies: list):
    """Сортировка вакансий по зарплате"""
    return sorted(vacancies,
                  key=lambda x: x.salary["from"] if not x.salary == "Зарплата не указана" and x.salary["from"] else 0,
                  reverse=True)


def get_top_vacancies(vacancies: list, top_n: int):
    """Для получения желаемого количества вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: list):
    """Удлобный вывод вакансий для пользователя"""

    for number, vacancy in enumerate(vacancies):
        print(f"\n{number + 1}. {vacancy.name}")
        print(f"Ссылка: {vacancy.link}")
        if vacancy.salary == "Зарплата не указана":
            print("Зарплата не указана")
        elif not vacancy.salary["to"]:
            print(f"Зарплата от {vacancy.salary['from']} руб.")
        elif not vacancy.salary["from"]:
            print(f"Зарплата до {vacancy.salary['to']} руб.")
        else:
            print(f"Зарплата от {vacancy.salary['from']} руб. до {vacancy.salary['to']} руб.")
        print(f"Описание: {vacancy.requirements}")


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    search_query = input("Введите поисковый запрос: ")
    print("Выполняется поиск...")
    print("Пожалуйста, подождите.")
    api_1 = ApiVacanciesHh()
    api_1.get_vacancies(search_query)

    vacancies_list = Vacancy.cast_to_object_list(api_1.hh_vacancies)

    while True:
        try:
            top_n = input("Введите количество вакансий для вывода в топ N: ")
            if not top_n:
                top_n = len(vacancies_list)
            else:
                top_n = int(top_n)
            break
        except ValueError:
            print("Пожалуйста, введите количество вакансий в числовом формате")

    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input('Введите диапазон зарплат(в формате: "число" - "число"): ')
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    while True:
        try:
            ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
            break
        except ValueError:
            print('Введите диапазон в формате: "число" - "число"(например: 100000 - 150000)')
            salary_range = input('Введите диапазон зарплат(в формате: "число" - "число"): ')

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

    user_answer = input("Хотите сохранить эти вакансии в файл?(введите: да/нет)")

    while True:
        if user_answer in ("да", "lf"):
            j1 = JSONSaver()

            for vacancy in top_vacancies:
                j1.add_vacancy(vacancy)

            print("Вакансии сохранены")
            break
        elif user_answer in ("нет", "ytn"):
            print("Вакансии не сохранены")
            break
        else:
            user_answer = input("Введите, пожалуйста, да или нет")
