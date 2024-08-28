import os
from dataclasses import dataclass
import configparser

from src.version import __version__


@dataclass
class Contact:
    NAME: str | None
    URL: str | None
    EMAIL: str | None


@dataclass
class Base:
    APP_NAME: str
    DEBUG: bool
    THEME_TITLE: str
    CONTACT: Contact


@dataclass
class Config:
    VERSION: str
    BASE: Base


def str_to_bool(value: str) -> bool:
    return value.lower() in ("yes", "true", "t", "1")


class InIConfig:
    VAR: Config
    raw: configparser.ConfigParser

    def __init__(self, path: str | os.PathLike, encoding="utf-8"):
        config = configparser.ConfigParser()
        config.read(filenames=path, encoding=encoding)

        self.VAR = Config(
            VERSION=__version__,
            BASE=Base(
                APP_NAME=config["BASE"]["APP_NAME"],
                DEBUG=str_to_bool(config["BASE"]["DEBUG"]),
                THEME_TITLE=config["BASE"]["THEME_TITLE"],
                CONTACT=Contact(
                    NAME=config["CONTACT"]["NAME"],
                    URL=config["CONTACT"]["URL"],
                    EMAIL=config["CONTACT"]["EMAIL"]
                ),
            )
        )
        self.path = path
        self.raw = config

    def reload(self):
        self.__init__(self.path)

    def save(self):
        with open(self.path, "w") as f:
            self.raw.write(f)
