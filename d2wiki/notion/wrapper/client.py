from __future__ import annotations
from typing import ClassVar, cast, Protocol
from uuid import UUID

from notion_client import AsyncClient
from notion_client.helpers import get_id

from d2wiki.types import JSON
from d2wiki.notion.models import D2ElementalWell, D2ExoticWeapon, D2ExoticArmor, flat_rich_text, D2Perk, NotionPage, \
    NotionDatabase, NotionUser, NotionBlock


class HasChildren(Protocol):
    """
    Protocols for Notion Models which have children.
    """
    id: str     # id of this object.
    nc: D2NotionWrapper     # Notion Client
    children: list[NotionBlock]     # list to store children.

    async def retrieve_children(self) -> HasChildren:   ...     # async method to retrieve children.


class D2NotionRoute:
    class Perks:
        PerkRow1: ClassVar[str] = str(UUID("72365f8fb13a491ca2ebf39c8628d7d8"))
        Barrel = Scope = Sight = PerkRow1  # alias
        PerkRow2: ClassVar[str] = str(UUID("f3168fe6663b49af810c0de65647ef5f"))
        Ammo = Magazine = PerkRow2  # alias
        PerkRow34: ClassVar[str] = str(UUID("28b23d0af78a4fceb29ccb631ccb5613"))
        Trait = PerkRow34  # alias

    class CombatStyleMods:
        WarmindCell: ClassVar[str] = str(UUID("e62bdff005924a5c882389af3db59574"))
        ChargedWithLight: ClassVar[str] = str(UUID("734f6ce4666c44c5b20b6ba0bc736642"))
        ElementalWells: ClassVar[str] = str(UUID("5fe7ebc7654e4a6284a0c8c99c98d5cd"))

    class Exotics:
        Weapons: ClassVar[str] = str(UUID("d638955238f34f6ebbb3dd82fd260028"))
        Armors: ClassVar[str] = str(UUID("3e6ed1607fc24a2080bc2a089e301e97"))


class D2NotionWrapper:
    """
    D2 Notion API Wrapper using notion_client.
    This class only wraps json response to python model.
    """
    def __init__(self, config: JSON):
        self.client: AsyncClient = AsyncClient(auth=config["token"])

    @staticmethod
    def get_icon_from_response(page: JSON) -> str | None:
        return cast(dict[str, str], page["icon"]["file"])["url"] if page.get("icon") is not None else None

    get_id = staticmethod(get_id)       # wrap helper function 'get_id' into D2NotionWrapper

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

        try:
            return [D2Perk.from_json(
                nc=self,
                name=page["properties"]["이름"]["title"],
                description=page["properties"]["설명"]["rich_text"],
                page_url=page["url"],
                img_url=self.get_icon_from_response(page)
            ) for page in resp["results"]]
        except Exception as e:
            print("Error occurred while querying weapon perk!")
            pprint(e)
            return []

    async def query_elemental_well(self, query: str) -> list[D2ElementalWell]:
        resp = await self.client.databases.query(**{
            "database_id": D2NotionRoute.CombatStyleMods.ElementalWells,
            "filter": {
                "property": "이름",
                "rich_text": {
                    "contains": query
                }
            }
        })

        from pprint import pprint
        pprint(resp)

        try:
            return [D2ElementalWell.from_json(
                nc=self,
                name=flat_rich_text(page["properties"]["이름"]["title"]),
                element=page["properties"]["원소"]["select"]["name"],
                mod_type=page["properties"]["분류"]["select"]["name"],
                cost=page["properties"]["에너지"]["number"],
                description=flat_rich_text(page["properties"]["설명"]["rich_text"]),
                footer=flat_rich_text(page["properties"]["각주"]["rich_text"]),
                page_url=page["url"],
                img_url=self.get_icon_from_response(page)
            ) for page in resp["results"]]
        except Exception as e:
            print("Error occurred while querying elemental well!")
            pprint(e)
            return []

    async def query_exotic_weapon(self, query: str) -> list[D2ExoticWeapon]:
        resp = await self.client.databases.query(**{
            "database_id": D2NotionRoute.Exotics.Weapons,
            "filter": {
                "property": "이름",
                "rich_text": {
                    "contains": query
                }
            }
        })

        from pprint import pprint
        pprint(resp)

        try:
            return [D2ExoticWeapon.from_json(
                nc=self,
                name=flat_rich_text(page["properties"]["이름"]["title"]),
                exotic_perk=flat_rich_text(page["properties"]["경이 특성"]["rich_text"]),
                description=flat_rich_text(page["properties"]["설명"]["rich_text"]),
                img_url=self.get_icon_from_response(page)
            ) for page in resp["results"]]
        except Exception as e:
            print("Error occurred while querying exotic weapon!")
            pprint(e)
            return []

    async def query_exotic_armor(self, query: str) -> list[D2ExoticArmor]:
        resp = await self.client.databases.query(**{
            "database_id": D2NotionRoute.Exotics.Armors,
            "filter": {
                "property": "이름",
                "rich_text": {
                    "contains": query
                }
            }
        })

        from pprint import pprint
        pprint(resp)

        try:
            res = [D2ExoticArmor.from_json(
                nc=self,
                name=page["properties"]["이름"]["title"],
                guardian_class=page["properties"]["직업"]["select"]["name"],
                category=page["properties"]["부위"]["select"]["name"],
                exotic_perk_name=page["properties"]["경이 특성"]["rich_text"],
                page_url=page["url"],
                img_url=self.get_icon_from_response(page)
            ) for page in resp["results"]]
            for elem in res:
                await elem.resolve_description()
            return res
        except Exception as e:
            print("Error occurred while querying exotic armor!")
            import traceback
            pprint(e)
            traceback.print_tb(e.__traceback__)
            return []

    async def retrieve_database(self, database_id: str) -> NotionDatabase | None:
        """
        Retrieve Notion Page and wrap it as NotionPage model.
        :param database_id: database id (UUID as str)
        :return: list of NotionDatabase element queried.
        """
        resp = await self.client.databases.retrieve(page_id=database_id)

        from pprint import pprint
        # pprint(resp)

        try:
            return NotionDatabase.from_json(
                nc=self,
                id=resp["id"]
            )
        except Exception as e:
            print("Error occurred while retrieving notion page!")
            pprint(e)
            return None

    async def retrieve_page(self, page_id: str) -> NotionPage | None:
        """
        Retrieve Notion Page and wrap it as NotionPage model.
        :param page_id: page id (UUID as str)
        :return: list of NotionPage element queried.
        """
        resp = await self.client.pages.retrieve(page_id=page_id)

        # from pprint import pprint
        # pprint(resp)

        try:
            return NotionPage.from_json(
                nc=self,
                id=resp["id"],
                created_time=resp["created_time"],
                created_by=resp["created_by"],
                last_edited_time=resp["last_edited_time"],
                last_edited_by=resp["last_edited_by"],
                archived=resp["archived"],
                cover=resp["cover"],
                icon=resp["icon"],
                parent=resp["parent"],
                properties=resp["properties"],
                url=resp["url"]
            )
        except Exception as e:
            print("Error occurred while retrieving notion page!")
            pprint(e)
            return None

    async def retrieve_user(self, user_id: str) -> NotionUser | None:
        resp = await self.client.users.retrieve(user_id=user_id)

        from pprint import pprint
        pprint(resp)

        try:
            return NotionUser.from_json(
                nc=self,

            )
        except Exception as e:
            print("Error occurred while retrieving notion user!")
            pprint(e)
            return None

    async def retrieve_child_blocks(self, parent: HasChildren) -> None:
        """
        Retrieve full block's child blocks.
        Page is also block, so NotionPage can also use this method to retrieve block contents.
        Reference : https://developers.notion.com/docs/working-with-page-content
        :param parent: Notion Model object matched with HasChildren protocol. Content blocks will be appended inside this object.
        """
        block_id = parent.id
        finished: bool = False
        next_cursor: str = ""
        blocks: list[NotionBlock] = []

        from pprint import pprint
        while not finished:
            if next_cursor:
                resp = await self.client.blocks.children.list(block_id=block_id, page_size=100, start_cursor=next_cursor)
            else:
                resp = await self.client.blocks.children.list(block_id=block_id, page_size=100)
            # print("Retrieving child blocks...")
            # pprint(resp)
            for block_resp in resp["results"]:
                blocks.append(await NotionBlock.from_json(nc=parent.nc, _parent=parent, **block_resp).retrieve_children())

            if resp["has_more"]:
                next_cursor = resp["next_cursor"]
            else:
                finished = True

        parent.children = blocks
