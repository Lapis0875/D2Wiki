"""
Aware Datetime Utility
"""

import datetime

import pytz

__all__ = ("UTC", "KST", "utcnow", "kstnow", "from_utc_isoformat", "get_discord_timestamp")

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
