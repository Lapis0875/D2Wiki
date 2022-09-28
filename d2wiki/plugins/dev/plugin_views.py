from enum import Enum
from typing import Iterable

from discord import ui, Interaction, SelectOption

from d2wiki.bot import D2WikiBot


class PluginManageMode(Enum):
    """
    Plugin Manage Mode Enum.
    """
    LOAD = "load"
    UNLOAD = "unload"
    RELOAD = "reload"


class PluginSelect(ui.Select):
    """
    Plugin Selector.
    """
    def __init__(self, plugins: dict[str, str], mode: PluginManageMode, bot: D2WikiBot):
        super(PluginSelect, self).__init__(
            placeholder="플러그인을 선택하세요.",
            min_values=1,
            max_values=len(plugins),
            options=[SelectOption(label=k, value=k) for k in plugins.keys()]
        )
        self.plugins: dict[str, str] = plugins      # {name: path, name: path, ...}
        self.mode: PluginManageMode = mode
        self.bot = bot

    def load_ext(self, targets: Iterable[tuple[str, str]]):
        for t in targets:
            self.bot.load_extension(t[1])       # load using path

    def unload_ext(self, targets: Iterable[tuple[str, str]]):
        for t in targets:
            self.bot.unload_extension(t[0])     # unload using name

    def reload_ext(self, targets: Iterable[tuple[str, str]]):
        for t in targets:
            self.bot.reload_extension(t[1])     # reload using path

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        targets: list[tuple[str, str]] = [(k, self.plugins[k]) for k in self.values]
        match self.mode:
            case PluginManageMode.LOAD:
                self.load_ext(targets)
                await interaction.followup.send(
                    "다음의 플러그인을 불러왔습니다.\n" + "\n".join(map(lambda target: f"- `{target[1]}`", targets)),
                    ephemeral=True
                )
            case PluginManageMode.UNLOAD:
                self.unload_ext(targets)
                await interaction.followup.send(
                    "다음의 플러그인을 제거했습니다.\n" + "\n".join(map(lambda name: f"- `{name}`", targets)),
                    ephemeral=True
                )
            case PluginManageMode.RELOAD:
                self.reload_ext(targets)
                await interaction.followup.send(
                    "다음의 플러그인을 다시 불러왔습니다.\n" + "\n".join(map(lambda name: f"- `{name}`", targets)),
                    ephemeral=True
                )
        self.view.stop()


def plugin_view(plugin_list: dict[str, str], mode: PluginManageMode, bot: D2WikiBot) -> ui.View:
    """
    Plugin View generator.
    :param plugin_list: list[str] of plugin paths.
    :param mode: Either one of LOAD/UNLOAD/RELOAD.
    :param bot: D2WikiBot instance.
    :return: ui.View object.
    """
    return ui.View(PluginSelect(plugin_list, mode, bot), disable_on_timeout=True)
