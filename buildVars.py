# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

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
Press NVDA+CONTROL+SHIFT+numeric keys twice quickly to paste the content of this memory slot to the running application."""),
        # version
        "addon_version" : "1.0.9",
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
        "addon_lastTestedNVDAVersion" : "2024.1",
        # Add-on update channel (default is None, denoting stable releases, and for development releases, use "dev"; do not change unless you know what you are doing)
        "addon_updateChannel" : None,
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join("addon", "globalPlugins", "snippetsForNVDA", "*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = [os.path.join("addon", "doc", "*", "contributing*.*")]
