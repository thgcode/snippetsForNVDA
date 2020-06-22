import api
import controlTypes
import globalPluginHandler
import keyboardHandler
import textInfos
import ui
from scriptHandler import getLastScriptRepeatCount

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    memory = {}
    lastPressedKey = 0

    def script_saveToMemory(self, gesture):
        """When pressed, this key saves the selected text to this position on the NVDA memory."""
        focus = api.getFocusObject()
        textInfo = None
        if focus.windowClassName in ["AkelEditW"] or focus.role in [controlTypes.ROLE_EDITABLETEXT]:
            textInfo = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        elif focus.treeInterceptor is not None:
            textInfo = focus.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
        if textInfo is not None:
            text = textInfo.text
            if len(text) > 0:
                keyCode = gesture.vkCode # Get which number the user pressed.
                # The number will be in the range 48 to 57 inclusive, and we will use it to hash the data in the dictionary.
                self.memory[keyCode] = text
                ui.message("Saved")
            else:
                ui.message("No selection")

    def script_speakAndCopyMemory(self, gesture):
        """When pressed, this key speaks and copies the text saved at this position of the NVDA memory to the clipboard."""
        keyCode = gesture.vkCode
        try:
            data = self.memory[keyCode]
            if getLastScriptRepeatCount() == 0:
                ui.message(data)
                self.lastPressedKey = keyCode
            elif getLastScriptRepeatCount() == 1 and self.isLastPressedKey(keyCode):
                api.copyToClip(data)
                ui.message(f"Copied {data}")
                self.lastPressedKey = 0
                # Paste the selected text
                keyboardHandler.KeyboardInputGesture.fromName("CONTROL+V").send()
            else:
                self.lastPressedKey = 0
                ui.message(data)
        except KeyError:
            ui.message("No data at this position")
            self.lastPressedKey = 0

    def isLastPressedKey(self, keyCode):
        return self.lastPressedKey == keyCode

    __gestures = {}

    # Maps all 10 numeric keyboard keys to the apropriate gesture.
    # It was done this way to avoid code repetition and to facilitate adding more commands in the future.
    for keyboardKey in range(10):
            __gestures[f"kb:NVDA+CONTROL+{keyboardKey}"] = "saveToMemory"
            __gestures[f"kb:NVDA+CONTROL+SHIFT+{keyboardKey}"] = "speakAndCopyMemory"
