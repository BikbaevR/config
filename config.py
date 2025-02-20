import os
import json

from config_element import ConfigElement

class Config:
    def __init__(self, directory: str, config_name: str):
        self.__main_directory = os.path.dirname(directory)
        self.__config_name = config_name + '.json'
        self.__config_file_full_path = os.path.join(self.__main_directory, self.__config_name)

        self.__config_elements: list[ConfigElement] = []
        self.__new_config_data: list[ConfigElement] = []

        self.__config_file_structure = {
            'config': {
                'config_name': self.__config_name,
                'config_elements': []
            }
        }

    def register_config_element(self, name: str, data_type: str, value: any = None, description: str = None):
        if not self.__check_name(name, 1):
            raise ValueError(f'Конфигурационный элемент с именем [{name}] уже зарегистрирован')

        self.__config_elements.append(ConfigElement(name, data_type, value, description))

    def get(self, name: str):
        for element in self.__new_config_data:
            if element.get_name() == name:
                return element.get_value()
        raise ValueError(f'Элемент с именем [{name}] не найден')

    def create_config_file(self):
        if not self.__config_file_is_exist():
            with open(self.__config_file_full_path, mode='w', encoding='utf-8') as config_file:
                config_file.write(self.__generate_config_file())

    def read_config_file(self):
        if not self.__config_file_is_exist():
            raise Exception(f'Не удалось найти конфигурационный файл [{self.__config_name}] по пути [{self.__config_file_full_path}]')

        try:
            with open(self.__config_file_full_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                config_elements = data["config"]["config_elements"]

                for element in config_elements:
                    self.__register_new_config_element(element["name"], element["data_type"], element["value"], element["description"])
        except Exception as e:
            raise Exception(f'Не удалось считать конфигурационный файл [{self.__config_name}] - {e}')

    def __register_new_config_element(self, name: str, data_type: str, value: any = None, description: str = None):
        if not self.__check_name(name, 0):
            raise ValueError(f'Конфигурационный элемент с именем [{name}] уже зарегистрирован')

        self.__new_config_data.append(ConfigElement(name, data_type, value, description))

    def __check_name(self, name: str, mode: int):
        for element in self.__config_elements if mode == 1 else self.__new_config_data:
            if element.get_name() == name:
                return False
        return True

    def __generate_config_file(self):
        self.__config_file_structure['config']['config_elements'] = [
            {
                'name': element.get_name(),
                'data_type': element.get_data_type(),
                'value': element.get_value(),
                'description': element.get_description()
            }
            for element in self.__config_elements
        ]
        return json.dumps(self.__config_file_structure, indent=4, ensure_ascii=False)

    def __config_file_is_exist(self):
        return os.path.isfile(self.__config_file_full_path)
