from abc import ABC, abstractmethod


class AbstractVacancy(ABC):
    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, hh_vacancies):
        pass


class Vacancy(AbstractVacancy):
    """Класс для создания объектов"""

    __slots__ = ("name", "link", "salary", "requirements")

    def __init__(self, name: str, link: str, salary: (dict, None), requirements: str):
        self.name = name
        self.link = link
        if salary:
            self.salary = salary
        else:
            self.salary = "Зарплата не указана"
        if requirements:
            self.requirements = requirements
        else:
            self.requirements = "Описание не указано"

    @classmethod
    def cast_to_object_list(cls, hh_vacancies):
        current_list = []
        for vacancy in hh_vacancies:
            current_list.append(cls(vacancy["name"],
                                    vacancy["url"],
                                    vacancy["salary"],
                                    vacancy["requirement"]))
        return current_list

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.link}, {self.salary}, {self.requirements})"
