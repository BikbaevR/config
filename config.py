import os
import json

from config_element import ConfigElement

class Config:
    def __init__(self, directory: str, config_name: str):
        self.__main_directory = os.path.dirname(directory)
        self.__config_name = config_name + '.cfg'
        self.__config_file_full_path = os.path.join(self.__main_directory, self.__config_name)

        self.__config_elements: list[ConfigElement] = []
        self.__new_config_data: list[ConfigElement] = []


    def register_config_element(self, name: str, data_type: str, value: any = None, description: str = None, dependency: str = None):
        if not self.__check_name(name, 1):
            raise ValueError(f'Конфигурационный элемент с именем [{name}] уже зарегистрирован')

        self.__config_elements.append(ConfigElement(name, data_type, value, description, dependency))

    def get(self, name: str):
        for element in self.__new_config_data:
            if element.get_name().strip() == name.strip():
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
                for line in file:
                    line = line.strip()
                    if len(line) == 0:
                        continue

                    if line.startswith('#'):
                        continue

                    if '=' not in line:
                        raise ValueError(f'В конфигурационном файле {self.__config_name} не верная строка [{line}]')

                    element_name, element_value = line.split('=')

                    for element in self.__config_elements:
                        if element.get_name() == element_name.strip():
                            self.__check_dependency(element.get_dependency(), element_value.strip(), element_name.strip())


                            self.__new_config_data.append(ConfigElement(element_name, element.get_data_type(), element_value.strip(), element.get_description()))

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
        elements = []
        for config_element in self.__config_elements:
            elements.append(f'# {config_element.get_description()} - [{config_element.get_data_type()}] \n')
            elements.append(f'{config_element.get_name()} = {config_element.get_value()}\n\n')

        return ''.join(elements)

    def __config_file_is_exist(self):
        return os.path.isfile(self.__config_file_full_path)

    def __check_dependency(self, dependency_element_name: str, value: str, element_name: str):
        if dependency_element_name is not None:
            if len(dependency_element_name.strip()) != 0:
                for element in self.__new_config_data:
                    if element.get_name().strip() == dependency_element_name.strip():
                        if element.get_data_type() == 'bool':
                            if element.get_value() is True:
                                if len(value.strip()) == 0 or value.strip().lower() == 'none':
                                    raise ValueError(f'Элемент [{element_name}] не может быть пустым')
                                else:
                                    return True
                            else:
                                return True
                        else:
                            raise ValueError(f'Элемент от которого идет зависимость [{dependency_element_name.strip()}] должен иметь тип [bool]')
                raise ValueError(f'Не удалось найти элемент [{dependency_element_name.strip()}]')

