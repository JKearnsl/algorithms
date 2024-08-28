from src.config import InIConfig
from src.models import BaseModel
from src.models.sort import MenuItem


class TestModel(BaseModel):
    id: MenuItem = MenuItem.TEST
    title: str = 'Тестирование'

    def __init__(self, config: InIConfig, theme):

        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def sort(self) -> None:
        pass
