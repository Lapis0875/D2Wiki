from typing import Final

from discord import application_command, ApplicationContext, SlashCommandGroup, CheckFailure, Embed, Color
from discord.ext.commands import check

from d2wiki.bot import D2WikiBot
from d2wiki.plugins.dev.contributors import Contributor
from d2wiki.plugins.dev.plugin_views import PluginManageMode, plugin_view
from d2wiki.plugins.plugin_base import PluginBase


def check_dev():
    return check(lambda ctx: ctx.author is not None and ctx.author.id == ctx.bot.owner_id)


GIT_REPO: Final[str] = "https://github.com/Lapis0875/D2Wiki"
NOTION_URL: Final[str] = "https://www.notion.so/destinyko/64517a4f88034d6a8d7c869230b741aa"


class DevPlugin(PluginBase):
    """
    Developer Features
    """
    # Plugin command group.
    grp_plugin = SlashCommandGroup(name="plugin", description="봇의 플러그인을 관리합니다.")

    def __init__(self, bot: D2WikiBot):
        super().__init__(bot)
        self.plugins: dict[str, str] = {name: f"d2wiki.plugins.{path}" for path, name in bot.config["plugins"].items()}
        self.contributors: list[Contributor] = []

    async def resolve_contributors(self):
        """
        Resolve contributors.
        """
        self.contributors.extend([(await Contributor.get(**c, bot=self.bot)) for c in self.bot.config["contributors"]])

    @application_command(name="info", description="봇의 정보를 표기합니다.")
    async def cmd_info(self, ctx: ApplicationContext):
        if len(self.contributors) == 0:
            await self.resolve_contributors()
        info = Embed(
            title="데스티니 가디언즈 위키 봇",
            description=f"[데스티니 가디언즈 노션]({NOTION_URL}) 에 기록된 정보를 디스코드에서 편리하게 검색할 수 있도록 구현한 봇입니다.",
            color=Color.green(),
            url=GIT_REPO
        ).add_field(
            name="깃허브 저장소 (기여 환영합니다!)",
            value=f"[{GIT_REPO}]({GIT_REPO})",
            inline=True
        ).add_field(
            name="노션 페이지",
            value=f"[{NOTION_URL}]({NOTION_URL})",
            inline=True
        ).add_field(
            name="도와주신 분들",
            value="\n".join(map(lambda c: f"- {c.mention}: {c.comment}", self.contributors)),
            inline=False
        ).set_thumbnail(
            url=self.bot.user.avatar.url
        )
        return await ctx.respond(embed=info)

    @application_command(name="link", description="노션 페이지와 깃허브 저장소의 링크를 보여줍니다.")
    async def cmd_link(self, ctx: ApplicationContext):
        return await ctx.respond(content=f"노션 페이지 : {NOTION_URL}\n봇 오픈소스 : {GIT_REPO}")

    @application_command(name="stop", description="봇을 종료합니다.")
    @check_dev()
    async def cmd_stop(self, ctx: ApplicationContext):
        await ctx.respond("봇을 종료합니다.")
        await self.bot.close()

    @cmd_stop.error
    async def on_stop_error(self, ctx: ApplicationContext, e):
        if isinstance(e, CheckFailure):
            return await ctx.respond("당신에게는 봇을 종료할 권한이 없습니다.", ephemeral=True)
        else:
            return await ctx.respond("이유는 모르겠지만 오류가 발생했어요! <@!280855156608860160>")

    @grp_plugin.command(name="load", description="플러그인을 불러옵니다.")
    @check_dev()
    async def cmd_load_plugin(self, ctx: ApplicationContext):
        await ctx.respond(view=plugin_view(self.plugins, PluginManageMode.LOAD, self.bot))

    @cmd_load_plugin.error
    async def on_load_error(self, ctx: ApplicationContext, e):
        if isinstance(e, CheckFailure):
            return await ctx.respond("당신에게는 플러그인의 관리 권한이 없습니다.", ephemeral=True)
        else:
            return await ctx.respond("이유는 모르겠지만 오류가 발생했어요! <@!280855156608860160>")

    @grp_plugin.command(name="unload", description="플러그인을 불러옵니다.")
    @check_dev()
    async def cmd_unload_plugin(self, ctx: ApplicationContext):
        await ctx.respond(view=plugin_view(self.plugins, PluginManageMode.UNLOAD, self.bot))

    @cmd_unload_plugin.error
    async def on_unload_error(self, ctx: ApplicationContext, e):
        if isinstance(e, CheckFailure):
            return await ctx.respond("당신에게는 플러그인의 관리 권한이 없습니다.", ephemeral=True)
        else:
            return await ctx.respond("이유는 모르겠지만 오류가 발생했어요! <@!280855156608860160>")

    @grp_plugin.command(name="reload", description="플러그인을 불러옵니다.")
    @check_dev()
    async def cmd_reload_plugin(self, ctx: ApplicationContext):
        await ctx.respond(view=plugin_view(self.plugins, PluginManageMode.RELOAD, self.bot))

    @cmd_reload_plugin.error
    async def on_reload_error(self, ctx: ApplicationContext, e):
        if isinstance(e, CheckFailure):
            return await ctx.respond("당신에게는 플러그인의 관리 권한이 없습니다.", ephemeral=True)
        else:
            return await ctx.respond("이유는 모르겠지만 오류가 발생했어요! <@!280855156608860160>")
