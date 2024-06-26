import dataclasses

from abstracts import api_user_input


@dataclasses.dataclass
class APIUserInput(api_user_input.APIUserInput):
    """
    Класс, описывающий поля API, заполняемые пользователем
    """

    pass
