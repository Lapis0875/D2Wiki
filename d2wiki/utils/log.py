import logging
from logging import CRITICAL, DEBUG, ERROR, FATAL, INFO, NOTSET, WARN, WARNING
from os import mkdir, path
from sys import stdout

from .dtutil import utcnow

__all__ = (
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARN",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
    "get_logger",
)


def get_logger(
    name: str,
    stream: bool = True,
    stream_level: int = logging.INFO,
    fmt: str = "[{asctime}] [{levelname}] {name}: {message}",
    file: bool = False,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(stream_level)

    if p := logger.parent:
        if len(p.handlers) > 0:
            return logger

    fmt = logging.Formatter(
        style="{", fmt=fmt
    )

    if stream:
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setLevel(stream_level)
        stream_handler.setFormatter(fmt)
        logger.addHandler(stream_handler)

    if file:
        if not path.exists("./logs"):
            mkdir("./logs")
        file_handler = logging.FileHandler(
            f'logs/{utcnow().isoformat(timespec="seconds").replace(":", "-")}.txt',
            mode="wt",
            encoding="utf-8",
        )
        logger.setLevel(file_level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
