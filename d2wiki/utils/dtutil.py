"""
Aware Datetime Utility
"""

import datetime

import pytz

__all__ = ("UTC", "KST", "utcnow", "kstnow", "from_utc_isoformat", "get_discord_timestamp", "notion2dt", "dt2notion")

UTC = pytz.UTC
KST = pytz.timezone("Asia/Seoul")


def utcnow() -> datetime.datetime:
    """
    Get current datetime in UTC.
    :return: aware datetime object in timezone UTC.
    """
    return UTC.localize(datetime.datetime.utcnow())

def kstnow() -> datetime.datetime:
    """
    Get current datetime in KST.
    :return: aware datetime object in timezone KST.
    """
    return utcnow().astimezone(KST)

def from_utc_isoformat(dt_str: str) -> datetime.datetime:
    """
    Convert UTC ISO formatted string to aware datetime object with pytz.UTC timezone.
    :param dt_str: UTC ISO formatted string to convert.
    :return: datetime object converted from UTC ISO formatted string.
    """
    dt = datetime.datetime.fromisoformat(dt_str)
    return dt.replace(tzinfo=UTC)

def get_discord_timestamp(dt: datetime.datetime, style: str = None):
    """
    return
    Convert datetime object into discord's timestamp expression.
    :param dt: datetime object to convert.
    :param style: timestamp style. default is None.
    :return: string value of timestamp expression.
    """
    if dt is None:
        return "UNDEFINED"
    if dt.tzinfo is None:
        dt = UTC.localize(dt)
    elif dt.isoformat().split("+")[1] == "00:00":  # UTC / 이거 왜만들었더라
        dt = dt.replace(tzinfo=UTC)

    return f"(KST) <t:{int(dt.timestamp())}" + (f":{style}>" if style else ">")


def notion2dt(dt_str: str) -> datetime.datetime:
    """
    Parse Notion's datetime string into datetime object.
    :param dt_str: Notion's datetime string.
    :return: datetime object.
    """
    return UTC.localize(datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ"))


def dt2notion(dt: datetime.datetime) -> str:
    """
    Parse python's aware datetime objecti nto Notion's datetime string.
    :param dt: datetime object.
    :return: Notion's datetime string.
    """
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
