from dependency_injector import containers, providers
from factories import api_factory


class Bootstrap(containers.DeclarativeContainer):
    """
    Контейнер с зависимостями
    """

    config = providers.Configuration()

    api_factory = providers.Factory(api_factory.APIFactory, api_type=config.api_type)
