from abc import ABC, ABCMeta, abstractmethod


class _SingletonMeta(ABCMeta):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# data access handler / integration later adapter class
class DalHandler(ABC, metaclass=_SingletonMeta):
    @abstractmethod
    def add_product_deployment(
        self,
        portfolio_id: str,
        product_stack_id: str,
        product_name: str,
        product_version: str,
        account_id: str,
        consumer_name: str,
        region: str,
    ) -> None: ...  # pragma: no cover) -> None: ...  # pragma: no cover
