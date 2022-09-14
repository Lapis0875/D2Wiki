import attr

from d2wiki.types import JSON


@attr.s
class NotionRichText:
    raw: str = attr.ib(repr=True, eq=True, hash=True)

    @classmethod
    def from_json(cls, json: JSON):
        return cls(raw=json.get("plain_text") or json["text"]["content"])

    def __str__(self):
        return self.raw


def flatten_richtext(richtext: list[JSON]) -> str:
    return "".join([NotionRichText.from_json(r).raw for r in richtext])
