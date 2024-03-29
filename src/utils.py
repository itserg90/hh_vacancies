from src.class_api import ApiVacanciesHh
from src.class_json import JSONSaver
from src.class_vacancy import Vacancy
from src.my_exceptions import ExceptionSalary

import re


def filter_vacancies(vacancies: list, words: list) -> list:
    """Фильтр по ключевым словам в описании"""

    if not words:
        return vacancies
    current_vacancies = []
    for vacancy in vacancies:
        if any(word.lower() in vacancy.requirements.lower() for word in words):
            current_vacancies.append(vacancy)
    return current_vacancies


def get_vacancies_by_salary(vacancies: list, salary: str) -> list:
    """Фильтр по желаемой зарплате"""

    if not salary:
        return vacancies
    current_vacancies = []
    current_salary = re.split(r"\D", salary)
    user_salary_from = int(current_salary[0])
    user_salary_to = int(current_salary[-1])

    if user_salary_from >= user_salary_to:
        raise ExceptionSalary("Первое число должно быть меньше второго")

    for vacancy in vacancies:
        if not vacancy.salary == {"from": 0, "to": 0}:
            salary_from = vacancy.salary["from"]
            salary_to = vacancy.salary["to"]
            if (salary_from and salary_to) and (
                    salary_from <= user_salary_from <= salary_to or salary_from <= user_salary_to <= salary_to):
                current_vacancies.append(vacancy)
            elif (salary_from and not salary_to) and user_salary_from <= salary_from <= user_salary_to:
                current_vacancies.append(vacancy)
            elif (not salary_from and salary_to) and user_salary_from <= salary_to <= user_salary_to:
                current_vacancies.append(vacancy)

    return current_vacancies


def sort_vacancies(vacancies: list) -> list:
    """Сортировка вакансий по зарплате"""

    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Для получения желаемого количества вакансий"""

    return vacancies[:top_n]


def print_vacancies(vacancies: list) -> None:
    """Удлобный вывод вакансий для пользователя"""

    for number, vacancy in enumerate(vacancies):
        print(f"\n{number + 1}. {vacancy.name}")
        print(f"Ссылка: {vacancy.link}")
        if vacancy.salary == {"from": 0, "to": 0}:
            print("Зарплата не указана")
        elif not vacancy.salary["to"]:
            print(f"Зарплата от {vacancy.salary['from']} руб.")
        elif not vacancy.salary["from"]:
            print(f"Зарплата до {vacancy.salary['to']} руб.")
        else:
            print(f"Зарплата от {vacancy.salary['from']} руб. до {vacancy.salary['to']} руб.")
        print(f"Описание: {vacancy.requirements}")


def user_interaction() -> None:
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
        except ExceptionSalary:
            print('Первое число должно быть меньше второго(например: 100000 - 150000)')
            salary_range = input('Введите диапазон зарплат(в формате: "число" - "число"): ')

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)

    while True:
        user_answer = input("Хотите сохранить эти вакансии в файл?(введите: да/нет)")
        if user_answer in ("да", "lf"):
            j1 = JSONSaver()

            for vacancy in top_vacancies:
                j1.add_vacancy(vacancy)

            print("Вакансии сохранены")
            break
        elif user_answer in ("нет", "ytn"):
            print("Вакансии не сохранены")
            break
