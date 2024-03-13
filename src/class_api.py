from abc import ABC, abstractmethod
import requests


class AbstractApi(ABC):
    @abstractmethod
    def filter_vacancies_by_name(self, arg1):
        pass

    @abstractmethod
    def get_vacancies(self, arg):
        pass


class ApiVacanciesHh(AbstractApi):
    """Класс для получения списка вакансий на HeadHunter по запросу"""

    def __init__(self):
        self.hh_vacancies = []

    def get_vacancies(self, job_name: str) -> None:
        """Получаем запрос из сервера"""

        range_pages = 0

        response = requests.get(
            f"https://api.hh.ru/vacancies?per_page=100&page={range_pages}&text={job_name.lower()}&search_field=name")

        if response.status_code == 200:
            self.filter_vacancies_by_name(response.json())

        pages = response.json()["pages"]
        if pages > 19:
            range_pages = 20
        else:
            range_pages = pages

        for number in range(1, range_pages):
            url = f"https://api.hh.ru/vacancies?per_page=100&page={number}&text={job_name.lower()}&search_field=name"
            result = requests.get(url)
            if result.status_code == 200:
                self.filter_vacancies_by_name(result.json())

    def filter_vacancies_by_name(self, vacancies: dict) -> None:
        """Фильтруем вакансии по валюте и добавляем в список вакансий"""

        for vacancy in vacancies["items"]:
            if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR" or not vacancy["salary"]:
                self.hh_vacancies.append({"id": vacancy["id"],
                                          "name": vacancy["name"],
                                          "url": vacancy["alternate_url"],
                                          "salary": vacancy["salary"],
                                          "requirement": vacancy["snippet"]["requirement"]})
