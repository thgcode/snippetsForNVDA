# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries
from site_scons.site_tools.NVDATool.utils import _


# Add-on information variables
addon_info = {
        # for previously unpublished addons, please follow the community guidelines at:
        # https://bitbucket.org/nvdaaddonteam/todo/raw/master/guidelines.txt
        # add-on Name, internal for nvda
        "addon_name" : "snippetsForNVDA",
        # Add-on summary, usually the user visible name of the addon.
        # Translators: Summary for this add-on to be shown on installation and add-on information.
        "addon_summary" : _("Text snippet handling features for NVDA"),
        # Add-on description
        # Translators: Long description to be shown for this add-on on add-on information from add-ons manager
        "addon_description" : _("""This addon provides text snippet handling features to NVDA, including snippet memory slots and more.
To use the snippet memory slots function:
Select some text.
Press NVDA+CONTROL+numeric keys to copy the selected text to a memory slot.
Press NVDA+CONTROL+SHIFT+numeric keys once  to hear the content of this memory slot.
Press NVDA+CONTROL+SHIFT+numeric keys twice quickly to paste the content of this memory slot to the running application.
Press NVDA+ALT+S to save the snippets to disk.
Press NVDA+ALT+L to load the previously saved snippets from disk."""),
        # Translators: what's new text for this add-on version shown in add-on store.
        "addon_changelog": _("""NVDA 2026.1 compatibility."""),
        # version
        "addon_version" : "1.0.11",
        # Author(s)
        # Translators: The people that have created snippetsForNVDA, shown on the manage addons dialog
        "addon_author" : _("snippetsForNVDA contributors"),
        # URL for the add-on documentation support
        "addon_url" : "https://github.com/thgcode/snippetsForNVDA",
        # Documentation file name
        "addon_docFileName" : "readme.html",
        # Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
        "addon_minimumNVDAVersion" : "2019.3.0",
        # Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
        "addon_lastTestedNVDAVersion" : "2026.1",
        # Add-on update channel (default is None, denoting stable releases, and for development releases, use "dev"; do not change unless you know what you are doing)
        "addon_updateChannel" : None,
}
pythonSources: list[str] = ["addon/globalPlugins/snippetsForNVDA/*.py"]
i18nSources: list[str] = pythonSources + ["buildVars.py"]

# Paths are relative to the addon directory when building the bundle.
excludedFiles: list[str] = [
    "doc/*/contributing*.*",
    "doc/*/*.tpl.md",
]

baseLanguage: str = "en"
markdownExtensions: list[str] = []

brailleTables: BrailleTables = {}
symbolDictionaries: SymbolDictionaries = {}
