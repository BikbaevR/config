
from config import Config

try:

    config = Config(__file__, 'test-config')

    config.register_config_element(
        name='element1',
        data_type='bool',
        value=True,
        description='Описание первого элемента',
        dependency=None
    )

    config.register_config_element(
        name='element2',
        data_type='int',
        value='',
        description='Описание второго элемента',
        dependency='element1'
    )

    config.register_config_element(
        name='element3',
        data_type='bool',
        value='True',
        description='Описание третьего элемента',
        dependency=None
    )

    config.register_config_element(
        name='element4',
        data_type='str',
        value='Тест',
        description='Описание четвертого элемента',
        dependency='element3'
    )

    config.create_config_file()

    config.read_config_file()


    print(config.get('element1'))
    print(config.get('element2'))

    second_config = Config(__file__, 'second-config')


    second_config.register_config_element(
        name='element1',
        data_type='bool',
        value=False,
        description='Описание первого элемента',
        dependency=None
    )

    second_config.register_config_element(
        name='element2',
        data_type='int',
        value='1',
        description='Описание второго элемента',
        dependency='element1'
    )

    second_config.create_config_file()

    second_config.read_config_file()
except Exception as e:
    print(e)