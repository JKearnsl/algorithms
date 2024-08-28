import psutil

from src.config import InIConfig
from src.models import BaseModel


class MainModel(BaseModel):

    def __init__(self, config: InIConfig, theme: tuple[type[any], str, str]):
        self.config = config
        self.theme = theme

        # список наблюдателей
        self._mObservers = []

    def get_ram_usage(self) -> int:
        return int(psutil.Process().memory_info().rss / (1024 * 1024))
