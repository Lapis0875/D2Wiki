from typing import Type

from discord import Cog

from d2wiki.bot import D2WikiBot
from d2wiki.utils.log import get_logger


class PluginBase(Cog):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__cog_name__ = cls.__name__.replace("Plugin", "").lower()  # patch cog name with ~Plugin naming.

    def __init__(self, bot: D2WikiBot):
        self.bot: D2WikiBot = bot
        self.logger = get_logger(
            f"d2wiki.{self.qualified_name}",
            stream=True,
            fmt="[{asctime}] [{levelname}] "f"plugins.{self.qualified_name}"": {message}",
            file=True
        )
        self.logger.info("Plugin loaded.")

    def cog_unload(self) -> None:
        self.logger.info("Plugin unloaded.")


def extension_helper(plugin_cls: Type[PluginBase]):
    def setup(bot: D2WikiBot):
        bot.add_cog(plugin_cls(bot))

    def teardown(bot: D2WikiBot):
        bot.remove_cog(plugin_cls.__cog_name__)

    return setup, teardown
