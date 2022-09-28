"""
Rich Text Helper
"""
from __future__ import annotations

from enum import Enum
from typing import cast, Iterable, Final

import attr

from .notion_link import NotionLink
from .notion_color import NotionColor
from d2wiki.types import JSON, JsonSerializable

__all__ = ("flat_rich_text", "wrap_diff", "RichText", "ansi_colorize")


@attr.s(slots=True)
class RichTextAnnotations(JsonSerializable):
    """
    Rich Text Annotations.
    """
    color: NotionColor = attr.ib(repr=True, eq=True, hash=True)
    bold: bool = attr.ib(default=False, repr=True, eq=True, hash=True)
    italic: bool = attr.ib(default=False, repr=True, eq=True, hash=True)
    strikethrough: bool = attr.ib(default=False, repr=True, eq=True, hash=True)
    underline: bool = attr.ib(default=False, repr=True, eq=True, hash=True)
    code: bold = attr.ib(default=False, repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, **json: str | bool) -> RichTextAnnotations:
        return cls(
            color=NotionColor(json["color"]),
            bold=json["bold"],
            italic=json["italic"],
            strikethrough=json["strikethrough"],
            underline=json["underline"],
            code=json["code"]
        )

    def to_json(self) -> JSON:
        return {
            "color": self.color.value,
            "bold": self.bold,
            "italic": self.italic,
            "strikethrough": self.strikethrough,
            "underline": self.underline,
            "code": self.code
        }

    def get_ansi_format(self) -> str:
        fmt = ""
        if self.bold:
            fmt += "1;"
        if self.italic:
            fmt += "3;"
        if self.underline:
            fmt += "4;"
        if fmt == "":
            fmt += "0;"
        return fmt


class RichTextType(Enum):
    """
    Rich Text Type
    """
    TEXT = "text"
    MENTION = "mention"
    EQUATION = "equation"


class RichTextData(JsonSerializable):
    """
    Base class for rich text data.
    """


@attr.s
class TextData(RichTextData):
    """
    Text object inside of Rich Text.
    """
    content: str = attr.ib(repr=True, eq=True, hash=True)
    link: NotionLink | None = attr.ib(default=None, repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, **json: str | dict[str, str]) -> TextData:
        return cls(content=json["content"], link=None if json.get("link") is None else NotionLink.from_json(**json["link"]))

    def to_json(self) -> JSON:
        obj = {"content": self.content}
        if self.link is not None:
            obj["link"] = self.link.to_json()
        return obj


def parse_rich_text_data(rich_text_type: RichTextType, json: JSON) -> RichTextData | None:
    """
    Parse Rich Text data.
    :param rich_text_type: Rich Text type.
    :param json: JSON object.
    :return: Rich Text data.
    """
    match rich_text_type:
        case RichTextType.TEXT:
            return TextData.from_json(**json)
        case RichTextType.MENTION:
            return None
        case RichTextType.EQUATION:
            return None
        case _:
            return None


ANSI_COLOR_MAPPING = {
    NotionColor.GRAY: "30",
    NotionColor.RED: "31",
    NotionColor.GREEN: "32",
    NotionColor.YELLOW: "33",
    NotionColor.BLUE: "34",
    NotionColor.PINK: "35",
    NotionColor.DEFAULT: "37",
    NotionColor.ORANGE_BACKGROUND: "41",
    NotionColor.BLUE_BACKGROUND: "45",
    NotionColor.GRAY_BACKGROUND: "44"
}
ANSI_DEFAULT: Final[str] = ANSI_COLOR_MAPPING[NotionColor.DEFAULT]
ANSI_RESET: Final[str] = "[0m"


@attr.s
class RichText:
    """
    Notion Rich Text Model.
    """
    plain_text: str = attr.ib(repr=True, eq=True, hash=True)
    annotations: RichTextAnnotations = attr.ib(repr=True, eq=True, hash=True)
    type: RichTextType = attr.ib(repr=True, eq=True, hash=True)
    data: RichTextData = attr.ib(default=None, repr=False, eq=False, hash=False)
    href: str | None = attr.ib(default=None, repr=True, eq=True, hash=False)

    @classmethod
    def from_json(cls, **json: str | JSON) -> RichText:
        rich_text_type = RichTextType(json["type"])
        data = parse_rich_text_data(rich_text_type, json[cast(str, rich_text_type.value)])
        assert data is not None, f"Rich Text data is None. If rich text type is either mention or equation, it is not supported yet. RichText.type = {rich_text_type.value}"
        obj = cls(
            plain_text=json["plain_text"],
            annotations=RichTextAnnotations.from_json(**json["annotations"]),
            type=rich_text_type,
            data=data,
            href=json.get("href")
        )
        setattr(obj, cast(str, rich_text_type.value), data)
        return obj

    def to_json(self) -> JSON:
        obj = {
            "plain_text": self.plain_text,
            "annotations": self.annotations.to_json(),
            self.type.value: self.data.to_json()
        }
        if self.href is not None:
            obj["href"] = self.href
        return obj

    def ansi(self) -> str:
        """
        Returns ANSI color format of this rich text.
        :return: ansi formatted text of this rich text.
        """
        ansi = f"[{self.annotations.get_ansi_format()}"
        c = ANSI_COLOR_MAPPING.get(self.annotations.color)
        # print(f"plain_text : {self.plain_text}, fmt : {ansi, c}")
        ansi += c or ANSI_DEFAULT
        # return ansi + "m" + self.plain_text + ANSI_RESET
        return ansi + "m" + self.plain_text


def parse_rich_text(rich_text: list[JSON]) -> list[RichText]:
    """
    Parse rich_text json array into list of RichText Object.
    :param rich_text: array of rich_text json.
    :return: list of RichText object.
    """
    return list(map(RichText.from_json, rich_text))


def flat_rich_text(rich_text: list[RichText]) -> str:
    """
    Flat Notion's RichText object.
    :param rich_text: RichText object.
    :return: plain str object of total rich text.
    """
    return "".join([r.plain_text or cast(TextData, r.data).content for r in rich_text])


def wrap_diff(text: str) -> str:
    """
    Wrap text with `diff` codeblock.
    :param text: Text to wrap.
    :return: Wrapped text.
    """
    return f"```diff\n{text}\n```"


def ansi_colorize(rich_texts: Iterable[RichText]) -> str:
    """
    Wrap plain text with `ansi` codeblock, thereby colorizing some parts.
    :param rich_texts: list of RichText objects.
    :return: Wrapped text.
    """
    ansi_texts = "".join(map(lambda rt: rt.ansi(), rich_texts))
    if len(ansi_texts) == 0:
        return ""
    text = f"```ansi\n{ansi_texts}\n```"
    return text
