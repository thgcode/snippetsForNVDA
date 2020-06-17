import api
import globalPluginHandler
import ui

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    memory = {}

    def script_saveToMemory(self, gesture):
        """When pressed, this key saves the text copied to the clipboard to this position on the NVDA memory."""
        try:
            clipboardContent = api.getClipData()
        except OSError:
            ui.message("Clipboard is empty")
            return
        keyCode = gesture.vkCode # Get which number the user pressed.
        # The number will be in the range 48 to 57 inclusive, and we will use it to hash the data in the dictionary.
        if isinstance(clipboardContent, str):
            self.memory[keyCode] = clipboardContent
            ui.message("Saved")

    def script_speakAndCopyMemory(self, gesture):
        """When pressed, this key speaks and copies the text saved at this position of the NVDA memory to the clipboard."""
        keyCode = gesture.vkCode
        try:
            data = self.memory[keyCode]
            api.copyToClip(data)
            ui.message(f"Copied {data}")
        except KeyError:
            ui.message("No data at this position")

    __gestures = {}

    # Maps all 10 numeric keyboard keys to the apropriate gesture.
    # It was done this way to avoid code repetition and to facilitate adding more commands in the future.
    for keyboardKey in range(11):
            __gestures[f"kb:NVDA+CONTROL+{keyboardKey}"] = "saveToMemory"
            __gestures[f"kb:NVDA+CONTROL+SHIFT+{keyboardKey}"] = "speakAndCopyMemory"
