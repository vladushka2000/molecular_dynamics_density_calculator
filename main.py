import sys

from dependency_injector.wiring import Provide, inject
import dotenv

from abstracts import factory
from common import bootstrap


@inject
def main(
    api_factory: factory.Factory = Provide[bootstrap.Bootstrap.api_factory],
) -> None:
    """
    Точка входа в программу
    :param api_factory: объект API
    """
    api = api_factory.create_instance()
    api.run()


if __name__ == "__main__":
    dotenv.load_dotenv()

    container = bootstrap.Bootstrap()
    container.config.api_type.from_env("API_TYPE")
    container.wire(modules=[sys.modules[__name__]])

    main()
