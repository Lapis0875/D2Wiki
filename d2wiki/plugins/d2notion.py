from typing import Literal

from discord import application_command, ApplicationContext, Colour, Embed, option

from d2wiki.bot import D2WikiBot
from d2wiki.notion import D2NotionWrapper
from d2wiki.notion.client import D2NotionRoute
from d2wiki.plugins.plugin_base import PluginBase, extension_helper

PerkCategory2Route = {
    "총열/스코프 (1퍽)": D2NotionRoute.Perks.PerkRow1,
    "탄창 (2퍽)": D2NotionRoute.Perks.PerkRow2,
    "특성 (3~4퍽)": D2NotionRoute.Perks.PerkRow34
}


class D2NotionPlugin(PluginBase):
    def __init__(self, bot: D2WikiBot):
        super(D2NotionPlugin, self).__init__(bot)
        self.notion: D2NotionWrapper = D2NotionWrapper(self.bot.config["notion"])

    @application_command(name="query_perks", name_localizations={"ko": "특성_검색"}, description="무기 특성을 검색합니다.", guild_ids=[881164190784565319, 354316444089188372])
    @option(name="category", description="검색할 특성의 종류", required=True, choices=["총열/스코프 (1퍽)", "탄창 (2퍽)", "특성 (3~4퍽)"])
    @option(name="perk", description="검색할 특성의 이름.", required=True, type=str)
    async def query_perks(self, ctx: ApplicationContext, category: str, perk: str):
        query = (await self.notion.query_perks(PerkCategory2Route[category], perk))[0]
        embed = Embed(
            title=query.name,
            description=query.description,
            colour=Colour.green()
        )
        if query.img_url is not None:
            embed.set_image(url=query.img_url)
        await ctx.respond(embed=embed)


setup, teardown = extension_helper(D2NotionPlugin)
