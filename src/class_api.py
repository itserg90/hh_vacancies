from abc import ABC, abstractmethod
import requests


class AbstractApi(ABC):
    @abstractmethod
    def filter_vacancies_by_name(self, arg1, arg2):
        pass

    @abstractmethod
    def get_vacancies(self, arg):
        pass


class ApiVacanciesHh(AbstractApi):
    """Класс для получения списка вакансий на HeadHunter по запросу"""

    def __init__(self):
        self.hh_vacancies = []

    def get_vacancies(self, job_name: str):
        for number in range(20):
            url = f"https://api.hh.ru/vacancies?per_page=100&page={number}"
            result = requests.get(url)
            if result.status_code == 200:
                self.filter_vacancies_by_name(job_name, result.json())

    def filter_vacancies_by_name(self, job_name: str, vacancies: dict):
        for vacancy in vacancies["items"]:
            if job_name.lower() in vacancy["name"].lower():
                if vacancy["salary"] and vacancy["salary"]["currency"] == "RUR" or not vacancy["salary"]:
                    self.hh_vacancies.append({"name": vacancy["name"],
                                              "url": vacancy["alternate_url"],
                                              "salary": vacancy["salary"],
                                              "requirement": vacancy["snippet"]["requirement"]})
