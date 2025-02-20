
class ConfigElement:
    allowed_data_types: list = ['int', 'str', 'float', 'bool', 'none']

    def __init__(self, name: str, data_type: str, value: str = None, description: str = None):
        self.__name = name
        self.__data_type = data_type
        self.__value = self.__parse_to_data_type(data_type, value)
        self.__description = description
        self.__validate_type(data_type, name)

    def __validate_type(self, data_type: str, name: str):
        if data_type not in self.allowed_data_types:
            raise ValueError(f'Не верный тип данных [{data_type}] для элемента: {name}')
        return True

    def __parse_to_data_type(self, data_type: str, value: str):
        if value is None:
            return None
        if len(str(value)) == 0:
            return None

        if self.__validate_type(data_type, value):
            try:
                if data_type == 'int':
                    return int(value)
                elif data_type == 'str':
                    return str(value)
                elif data_type == 'float':
                    return float(value)
                elif data_type == 'bool':
                    return bool(value)
                elif data_type == 'none':
                    return None
            except ValueError:
                raise ValueError(f'Не удалось сконвертировать [{value}] в тип [{data_type}]')

    def get_name(self) -> str:
        return self.__name

    def get_data_type(self) -> str:
        return self.__data_type

    def get_value(self) -> any:
        return self.__value

    def get_description(self) -> str:
        return self.__description

    def __str__(self):
        return f'Name: {self.__name} | Type: {self.__data_type} | Value: {self.__value} | Description: {self.__description}'
