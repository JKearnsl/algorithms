from abc import ABC

from src.themes.base import BaseTheme


class BaseModel(ABC):
    theme: tuple[type[BaseTheme], str, str]

    _mObservers = []

    def add_observer(self, observer):
        self._mObservers.append(observer)

    def remove_observer(self, observer):
        self._mObservers.remove(observer)

    def notify_observers(self):
        for observer in self._mObservers:
            observer.model_changed()