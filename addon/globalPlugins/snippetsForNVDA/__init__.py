import addonHandler
import api
import globalPluginHandler
import keyboardHandler
import mouseHandler
import textInfos
import ui
import winUser
from scriptHandler import getLastScriptRepeatCount

# Fix compatibility with the new role constants introduced in NVDA 2022.1."""
try:
    from controlTypes import Role
    ROLE_EDITABLETEXT = Role.EDITABLETEXT
    ROLE_TERMINAL = Role.TERMINAL
except ImportError:
    from controlTypes import ROLE_EDITABLETEXT, ROLE_TERMINAL

# Save the NVDA translation function so that we can use it if we need it
nvdaTranslation = _

# Then, init our translation system
# At this point, the _ (underscore) function will be rebound with the translations of our addon
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    memory = {}
    lastPressedKey = 0

    def script_saveToMemory(self, gesture):
        focus = api.getFocusObject()
        textInfo = None
        if focus.windowClassName in ["AkelEditW"] or focus.role in [ROLE_EDITABLETEXT]:
            textInfo = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        elif focus.treeInterceptor is not None:
            textInfo = focus.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
        if textInfo is not None:
            text = textInfo.text
            if len(text) > 0:
                keyCode = gesture.vkCode # Get which number the user pressed.
                # The number will be in the range 48 to 57 inclusive, and we will use it to hash the data in the dictionary.
                self.memory[keyCode] = text
                # Translators: This message is displayed when text is saved on a memory slot.
                ui.message(_("Saved"))
            else:
                ui.message(nvdaTranslation("No selection"))

    # Translators: the documentation of the save to memory slot command, displayed on the input help mode.
    script_saveToMemory.__doc__ = _("""When pressed, this key saves the selected text to this memory slot.""")

    def script_speakAndCopyMemory(self, gesture):
        keyCode = gesture.vkCode
        try:
            data = self.memory[keyCode]
            if getLastScriptRepeatCount() == 0:
                ui.message(data)
                self.lastPressedKey = keyCode
            elif getLastScriptRepeatCount() == 1 and self.isLastPressedKey(keyCode):
                api.copyToClip(data)
                # Translators: The message displayed when the user pasted this memory slot to an edit field.
                ui.message(_("Pasted {data}").format(data=data))
                self.lastPressedKey = 0
                # Paste the selected text
                self._paste()
            else:
                self.lastPressedKey = 0
                ui.message(data)
        except KeyError:
            # Translators: The message when the user checks a memory slot but there is no data in it
            ui.message(_("No data at this position"))
            self.lastPressedKey = 0

    # Translators: the documentation of the speak and copy memory slot command, displayed on the input help mode.
    script_speakAndCopyMemory.__doc__ = _("""Pressing this key combination once , the content of this memory slot will be spoken.
Pressing it twice quickly, the content of this memory slot will be pasted to the running application.""")

    def _paste(self):
        focus = api.getFocusObject()
        if focus.role == ROLE_TERMINAL and focus.appModule.appName == "cmd":
            # Does a right click to trigger a paste on the console
            mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTDOWN,0,0)
            mouseHandler.executeMouseEvent(winUser.MOUSEEVENTF_RIGHTUP,0,0)
        else:
            keyboardHandler.KeyboardInputGesture.fromName("CONTROL+V").send()

    def isLastPressedKey(self, keyCode):
        return self.lastPressedKey == keyCode

    __gestures = {}

    # Maps all 10 numeric keyboard keys to the apropriate gesture.
    # It was done this way to avoid code repetition and to facilitate adding more commands in the future.
    for keyboardKey in range(10):
            __gestures[f"kb:NVDA+CONTROL+{keyboardKey}"] = "saveToMemory"
            __gestures[f"kb:NVDA+CONTROL+SHIFT+{keyboardKey}"] = "speakAndCopyMemory"
