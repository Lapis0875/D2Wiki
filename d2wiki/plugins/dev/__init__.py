from d2wiki.plugins.plugin_base import extension_helper
from .dev import DevPlugin

setup, teardown = extension_helper(DevPlugin)
