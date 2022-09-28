from typing import cast

from discord import application_command, ApplicationContext, option, SlashCommand, Option

from d2wiki.bot import D2WikiBot
from d2wiki.notion.wrapper import D2NotionWrapper, D2NotionRoute
from d2wiki.plugins.plugin_base import PluginBase, extension_helper
from d2wiki.types import CoroutineFunction

PerkCategory2Route = {
    "총열/조준경 (1퍽)": D2NotionRoute.Perks.PerkRow1,
    "탄창 (2퍽)": D2NotionRoute.Perks.PerkRow2,
    "특성 (3~4퍽)": D2NotionRoute.Perks.PerkRow34
}


def query_cmd(name: str, query_handler: CoroutineFunction, ko_name: str, description: str, options: list[Option]) -> SlashCommand:
    cmd_name: str = f"query_{name}"

    @application_command(name=cmd_name, name_localizations={"ko": f"{ko_name}-검색"}, description=description)
    async def cmd(ctx: ApplicationContext, *, query: str):
        query = (await query_handler(query))
        try:
            res = query[0]
            await ctx.respond(embed=res.embed)
        except IndexError:
            await ctx.respond(content="검색 결과가 없습니다.🤔")

    cmd.__name__ = cmd_name
    cmd.__qualname__ = f"{D2NotionPlugin.__name__}.{cmd_name}"
    return cast(SlashCommand, cmd)


class D2NotionPlugin(PluginBase):
    def __init__(self, bot: D2WikiBot):
        super(D2NotionPlugin, self).__init__(bot)
        self.notion: D2NotionWrapper = D2NotionWrapper(self.bot.config["notion"])

    @application_command(name="query_perks", name_localizations={"ko": "특성"}, description="무기 특성을 검색합니다.")
    @option(name="category", description="검색할 특성의 종류", required=True, choices=list(PerkCategory2Route.keys()))
    @option(name="query", description="검색할 특성의 이름.", required=True, type=str)
    async def query_perks(self, ctx: ApplicationContext, category: str, query: str):
        await ctx.defer()
        query = (await self.notion.query_perks(PerkCategory2Route[category], query))
        try:
            res = query[0]
            await ctx.respond(embed=res.embed)
        except IndexError:
            await ctx.respond(content="검색 결과가 없습니다.🤔")

    @application_command(name="query_exotic_armors", name_localizations={"ko": "경이방어구"}, description="경이 방어구를 검색합니다.")
    @option(name="query", description="검색할 경이 방어구의 이름.", required=True, type=str)
    async def query_exotic_armors(self, ctx: ApplicationContext, query: str):
        await ctx.defer()
        query = (await self.notion.query_exotic_armor(query))
        try:
            res = query[0]
            await ctx.respond(embed=res.embed)
        except IndexError:
            await ctx.respond(content="검색 결과가 없습니다.🤔")

    @application_command(name="query_exotic_weapons", name_localizations={"ko": "경이무기"}, description="경이 무기를 검색합니다.")
    @option(name="query", description="검색할 경이 무기의 이름.", required=True, type=str)
    async def query_exotic_weapons(self, ctx: ApplicationContext, query: str):
        await ctx.defer()
        query = (await self.notion.query_exotic_weapon(query))
        try:
            res = query[0]
            await ctx.respond(embed=res.embed)
        except IndexError:
            await ctx.respond(content="검색 결과가 없습니다.🤔")

    @application_command(name="query_wells", name_localizations={"ko": "원소샘"}, description="원소 샘 개조부품을 검색합니다.")
    @option(name="query", description="검색할 원소 샘 개조부품의 이름.", required=True, type=str)
    async def query_wells(self, ctx: ApplicationContext, query: str):
        await ctx.defer()
        query = (await self.notion.query_elemental_well(query))
        try:
            res = query[0]
            await ctx.respond(embed=res.embed)
        except IndexError:
            await ctx.respond(content="검색 결과가 없습니다.🤔")


setup, teardown = extension_helper(D2NotionPlugin)

