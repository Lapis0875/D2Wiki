from discord import application_command, ApplicationContext, Colour, Embed

from d2wiki.bot import D2WikiBot
from d2wiki.notion import D2NotionWrapper
from d2wiki.plugins.plugin_base import PluginBase, extension_helper


class D2NotionPlugin(PluginBase):
    def __init__(self, bot: D2WikiBot):
        super(D2NotionPlugin, self).__init__(bot)
        self.notion: D2NotionWrapper = D2NotionWrapper(self.bot.config["notion"])

    @application_command(name="테스트", description="테스트 명령어", guild_ids=[881164190784565319])
    async def test(self, ctx: ApplicationContext):
        napal_tan = (await self.notion.query_perks("나팔 탄창"))[0]
        await ctx.respond(
            embed=Embed(
                title=napal_tan.name,
                description=napal_tan.description,
                colour=Colour.green()
            ).set_thumbnail(url=napal_tan.img_url)
        )


setup, teardown = extension_helper(D2NotionPlugin)
