import json
from typing import Any, Optional, List

from discord import Bot, ApplicationCommand

from d2wiki.utils.log import get_logger


class D2WikiBot(Bot):
    """
    D2Wiki Bot Class.
    """

    async def register_command(self, command: ApplicationCommand, force: bool = True,
                               guild_ids: Optional[List[int]] = None) -> None:
        return await super(D2WikiBot, self).sync_commands([command], force=force, guild_ids=guild_ids)

    def __init__(self):
        super().__init__(owner_id=280855156608860160)
        with open("./config.json", mode="rt", encoding="utf-8") as f:
            self.config: dict[str, Any] = json.load(f)
        self.logger = get_logger("d2wiki", stream=True, file=True)

    def run(self):
        for plugin_path in self.config["plugins"].keys():       # path: plugin.name
            self.load_extension(f"d2wiki.plugins.{plugin_path}")
        super().run(self.config.pop("token"))

    async def on_ready(self):
        self.logger.info("D2Wiki Online 🟢")
        await self.application_info()   # fetch self info.

    async def on_disconnect(self):
        self.logger.info("D2Wiki Offline 🔴")
