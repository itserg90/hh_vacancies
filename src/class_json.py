from abc import ABC, abstractmethod
import json
from pathlib import Path


class AbstractJSONSaver(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractJSONSaver):
    """Класс для создания файла и сохранения, добавления и удаления вакансий"""

    COUNT_SAVER = 0

    def __init__(self):
        JSONSaver.COUNT_SAVER += 1
        self.__file_path = Path("data", "vacancies_")
        self.__filename = f"{self.__file_path}{JSONSaver.COUNT_SAVER}.json"
        if not Path(self.__filename).is_file():
            with open(self.__filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def add_vacancy(self, vacancy):
        with open(self.__filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
            vacancies.append({"name": vacancy.name,
                              "url": vacancy.link,
                              "salary": vacancy.salary,
                              "requirements": vacancy.requirements})
            with open(self.__filename, "w", encoding="utf-8") as fi:
                json.dump(vacancies, fi)

    def delete_vacancy(self, vacancy):
        with open(self.__filename, "r", encoding="utf-8") as file:
            new_vacancies = []
            vacancies = json.load(file)
            for vac in vacancies:
                if not vacancy.name.lower() == vac["name"].lower():
                    new_vacancies.append(vac)
            with open(self.__filename, "w", encoding="utf-8") as file1:
                json.dump(new_vacancies, file1)
