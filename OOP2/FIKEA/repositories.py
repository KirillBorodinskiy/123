from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence, Dict, Callable, Union

TEntity = TypeVar('TEntity')  # Variabilní typ (generika)
TKey = TypeVar('TKey')


# Vytváříme generickou abstraktní třídu - jedná se o "template typu",
# kterému přiřadíme specifické typy, podle kterého se bude výsledný typ chovat.
class Repository(ABC, Generic[TKey, TEntity]):
    key_selector: Callable[[TEntity], TKey]

    @abstractmethod  # Abstraktní metoda - ve všech třídách co z této abstraktní třídy
    # dědí ji musíme implementovat
    def get_by_id(self, key: TKey) -> TEntity:
        pass

    @abstractmethod
    def get_by_id_or_default(self, key: TKey) -> Union[TEntity, None]:
        pass

    @abstractmethod
    def add_entity(self, entity: TEntity, key: TKey = None) -> None:
        pass

    @abstractmethod
    def get_all(self, selector: Callable[[TEntity], bool]) -> Sequence[TEntity]:
        pass


class DictionaryRepository(Repository, Generic[TKey, TEntity]):
    def __init__(self, default: Union[TEntity, None], key_selector: Callable[[TEntity], TKey]):
        self.repository: Dict[TKey, TEntity] = {}
        self.default = default
        self.key_selector = key_selector

    def get_by_id(self, key: TKey) -> TEntity:
        if key not in self.repository:
            raise KeyError
        return self.repository[key]

    def get_by_id_or_default(self, key: TKey) -> Union[TEntity, None]:
        if key not in self.repository:
            return self.default
        return self.repository[key]

    def add_entity(self, entity: TEntity, key: TKey = None) -> None:
        if key is None:
            key = self.key_selector(entity)
        if key is None:
            raise KeyError
        if key in self.repository:
            raise KeyError
        self.repository[key] = entity

    def get_all(self, selector: Callable[[TEntity], bool]) -> Sequence[TEntity]:
        return [x for x in self.repository.values() if selector(x)]
