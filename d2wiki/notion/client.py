from typing import ClassVar
from uuid import UUID

from notion_client import AsyncClient

from d2wiki.notion.models.rich_text import flatten_richtext
from d2wiki.notion.models.weapon_perk import D2Perk
from d2wiki.types import JSON


class D2NotionRoute:
    class Perks:
        PerkRow1: ClassVar[str] = str(UUID("54a18fc21a45422da9567223463f512f"))
        Barrel = Scope = Sight = PerkRow1  # alias
        PerkRow2: ClassVar[str] = str(UUID("c45bc65fcdeb43738c31870481541f7d"))
        Ammo = Magazine = PerkRow2  # alias
        PerkRow34: ClassVar[str] = str(UUID("2a3d2c092ffb4c27be1fd3b6748a6ff1"))
        Trait = PerkRow34  # alias

    Wells: ClassVar[str] = str(UUID("feb9ab0ed69b4eccb8c4a16b303fd11c"))


class D2NotionWrapper:
    """
    D2 Notion API Wrapper using notion_client.
    This class only wraps json response to python model.
    """
    def __init__(self, config: JSON):
        self.client: AsyncClient = AsyncClient(auth=config["token"])

    async def query_perks(self, route: str, perk_name: str) -> list[D2Perk]:
        resp = await self.client.databases.query(**{
            "database_id": route,
            "filter": {
                "property": "이름",
                "rich_text": {
                    "contains": perk_name
                }
            }
        })
        from pprint import pprint
        pprint(resp)

        return [D2Perk.from_json(
            name=flatten_richtext(page["properties"]["이름"]["title"]),
            description=flatten_richtext(page["properties"]["설명"]["rich_text"]),
            img_url=page["icon"]["file"]["url"] if page.get("icon") is not None else None
        ) for page in resp["results"]]

