from uuid import UUID

from notion_client import AsyncClient

from d2wiki.notion.models.rich_text import flatten_richtext
from d2wiki.notion.models.weapon_perk import D2Perk
from d2wiki.types import JSON


class D2NotionWrapper:
    """
    D2 Notion API Wrapper using notion_client.
    This class only wraps json response to python model.
    """
    def __init__(self, config: JSON):
        self.client: AsyncClient = AsyncClient(auth=config["token"])

    async def query_perks(self, perk_name: str) -> list[D2Perk]:
        resp = await self.client.databases.query(**{
            "database_id": str(UUID("c45bc65fcdeb43738c31870481541f7d")),
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
            img_url=page["icon"]["file"]["url"]
        ) for page in resp["results"]]

