from __future__ import annotations
import attr

from d2wiki.bot import D2WikiBot
from d2wiki.types import JSON_VALUES, JSON


@attr.s
class Contributor:
    """
    Contributor Model.
    """
    id: int = attr.ib(repr=True, eq=True, hash=True)
    name: str = attr.ib(repr=True, eq=True, hash=True)
    avatar_url: str = attr.ib(repr=True, eq=True, hash=True)
    email: str | None = attr.ib(default=None, repr=False, eq=False, hash=False)
    comment: str | None = attr.ib(default=None, repr=False, eq=False, hash=False)

    @classmethod
    def from_json(cls, **json_values: JSON_VALUES) -> Contributor:
        return cls(
            id=json_values["id"],
            name=json_values["name"],
            avatar_url=json_values["avatar_url"],
            email=json_values.get("email"),
            comment=json_values.get("comment")
        )

    @classmethod
    async def get(cls, id: int, name: str, comment: str | None, bot: D2WikiBot) -> Contributor:
        u = bot.get_user(id) or await bot.fetch_user(id)
        return cls.from_json(id=id, name=name, avatar_url=u.avatar.url, comment=comment, email=None)    # email not now.

    def to_json(self) -> JSON:
        return {
            "id": self.id,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "email": self.email,
            "comment": self.comment
        }

    @property
    def mention(self) -> str:
        return f"<@!{self.id}>"
