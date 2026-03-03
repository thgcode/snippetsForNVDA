import addonHandler
import api
import globalPluginHandler
import keyboardHandler
import textInfos
import ui
from scriptHandler import getLastScriptRepeatCount
import config
import json
import os
import re

# Fix for the Russian keyboard layout -- We can't use
# keyboardInputGesture.fromName() because it triggers a LookupError
CTRLV = keyboardHandler.KeyboardInputGesture(
{(17, False), (16, False)},
86,
		0,
False
)

# Fix compatibility with the new role constants introduced in NVDA 2022.1."""
try:
    from controlTypes import Role
    ROLE_EDITABLETEXT = Role.EDITABLETEXT
    ROLE_DOCUMENT = Role.DOCUMENT
except ImportError:
    from controlTypes import ROLE_EDITABLETEXT, ROLE_DOCUMENT

# Save the NVDA translation function so that we can use it if we need it
nvdaTranslation = _

# Then, init our translation system
# At this point, the _ (underscore) function will be rebound with the translations of our addon
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    memory = {}
    lastPressedKey = 0
    
    # Virtual View states
    current_slot_key = None
    cursors = {} # { keyCode: int }

    def script_saveToMemory(self, gesture):
        focus = api.getFocusObject()
        textInfo = None
        if focus.treeInterceptor is not None and not focus.treeInterceptor.passThrough:
            textInfo = focus.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
        elif focus.windowClassName in ["AkelEditW"] or focus.role in [ROLE_EDITABLETEXT, ROLE_DOCUMENT]:
            textInfo = focus.makeTextInfo(textInfos.POSITION_SELECTION)
        if textInfo is not None:
            text = textInfo.text
            if len(text) > 0:
                keyCode = str(gesture.vkCode) # Get which number the user pressed.
                # The number will be in the range 48 to 57 inclusive, and we will use it to hash the data in the dictionary.
                self.memory[keyCode] = text
                # Translators: This message is displayed when text is saved on a memory slot.
                ui.message(_("Saved"))
            else:
                ui.message(nvdaTranslation("No selection"))

    # Translators: the documentation of the save to memory slot command, displayed on the input help mode.
    script_saveToMemory.__doc__ = _("""When pressed, this key saves the selected text to this memory slot.""")

    def script_speakAndCopyMemory(self, gesture):
        keyCode = str(gesture.vkCode)
        try:
            data = self.memory[keyCode]
            self.current_slot_key = keyCode
            if keyCode not in self.cursors:
                self.cursors[keyCode] = 0

            if getLastScriptRepeatCount() == 0:
                ui.message(data)
                self.lastPressedKey = keyCode
            elif getLastScriptRepeatCount() == 1 and self.isLastPressedKey(keyCode):
                api.copyToClip(data)
                # Translators: The message displayed when the user pasted this memory slot to an edit field.
                ui.message(_("Pasted {data}").format(data=data))
                self.lastPressedKey = 0
                # Paste the selected text
                CTRLV.send()
            else:
                self.lastPressedKey = 0
                ui.message(data)
        except KeyError:
            # Translators: The message when the user checks a memory slot but there is no data in it
            ui.message(_("No data at this position"))
            self.lastPressedKey = 0
            self.current_slot_key = None

    # Translators: the documentation of the speak and copy memory slot command, displayed on the input help mode.
    script_speakAndCopyMemory.__doc__ = _("""Pressing this key combination once , the content of this memory slot will be spoken.
Pressing it twice quickly, the content of this memory slot will be pasted to the running application.""")

    def script_saveSnippets(self, gesture):
        with open(os.path.join(config.getUserDefaultConfigPath(),"snippets.data"), "w") as file:
            json.dump(self.memory, file)
        ui.message(_("Snippets saved"))

    script_saveSnippets.__doc__ = _("""Save the snippets to be used later""")

    def script_loadSnippets(self, gesture):
        with open(os.path.join(config.getUserDefaultConfigPath(),"snippets.data"), "r") as file:
            self.memory = json.load(file)
        ui.message(_("Snnipets loaded successfully"))

    script_loadSnippets.__doc__ = _("""Loads previously saved snippets""")

    def _get_char_name(self, char):
        if char == " ":
            return _("space")
        elif char == "\n":
            return _("new line")
        elif char == "\t":
            return _("tab")
        return char

    def script_nextChar(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
        
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        if cursor < len(data) - 1:
            cursor += 1
            self.cursors[self.current_slot_key] = cursor
            char = data[cursor]
            ui.message(self._get_char_name(char))
        else:
            ui.message(_("Bottom"))

    script_nextChar.__doc__ = _("""Moves to the next character in the current memory slot.""")

    def script_prevChar(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
            
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        if cursor > 0:
            cursor -= 1
            self.cursors[self.current_slot_key] = cursor
            char = data[cursor]
            ui.message(self._get_char_name(char))
        else:
            ui.message(_("Top"))

    script_prevChar.__doc__ = _("""Moves to the previous character in the current memory slot.""")

    def _get_words(self, text):
        return [(m.start(0), m.end(0), m.group(0)) for m in re.finditer(r'\w+|[^\w\s]+', text)]
        
    def script_nextWord(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
            
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        words = self._get_words(data)
        
        for start, end, word in words:
            if start > cursor:
                self.cursors[self.current_slot_key] = start
                ui.message(word)
                return
                
        ui.message(_("Bottom"))

    script_nextWord.__doc__ = _("""Moves to the next word in the current memory slot.""")

    def script_prevWord(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
            
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        words = self._get_words(data)
        
        for i in range(len(words) - 1, -1, -1):
            start, end, word = words[i]
            if end <= cursor or start < cursor:
                self.cursors[self.current_slot_key] = start
                ui.message(word)
                return
                
        ui.message(_("Top"))

    script_prevWord.__doc__ = _("""Moves to the previous word in the current memory slot.""")

    def _get_lines(self, text):
        lines = []
        start = 0
        for line in text.splitlines(False): # keep line string, do not keep \n 
            end = start + len(line)
            lines.append((start, end, line))
            start = end + 1 # +1 for \n
        return lines

    def script_nextLine(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
            
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        lines = self._get_lines(data)
        
        for start, end, line in lines:
            if start > cursor:
                self.cursors[self.current_slot_key] = start
                ui.message(line if line.strip() else _("blank"))
                return
                
        ui.message(_("Bottom"))

    script_nextLine.__doc__ = _("""Moves to the next line in the current memory slot.""")

    def script_prevLine(self, gesture):
        if not self.current_slot_key:
            ui.message(_("No memory slot selected"))
            return
            
        data = self.memory.get(self.current_slot_key, "")
        if not data:
            return
            
        cursor = self.cursors.get(self.current_slot_key, 0)
        lines = self._get_lines(data)
        
        for i in range(len(lines) - 1, -1, -1):
            start, end, line = lines[i]
            if start < cursor:
                self.cursors[self.current_slot_key] = start
                ui.message(line if line.strip() else _("blank"))
                return
                
        ui.message(_("Top"))

    script_prevLine.__doc__ = _("""Moves to the previous line in the current memory slot.""")

    def isLastPressedKey(self, keyCode):
        return self.lastPressedKey == keyCode

    __gestures = {}
    __gestures["kb:NVDA+ALT+S"] = "saveSnippets"
    __gestures["kb:NVDA+ALT+L"] = "loadSnippets"
    __gestures["kb:ALT+SHIFT+rightArrow"] = "nextChar"
    __gestures["kb:ALT+SHIFT+leftArrow"] = "prevChar"
    __gestures["kb:CONTROL+ALT+SHIFT+rightArrow"] = "nextWord"
    __gestures["kb:CONTROL+ALT+SHIFT+leftArrow"] = "prevWord"
    __gestures["kb:ALT+SHIFT+downArrow"] = "nextLine"
    __gestures["kb:ALT+SHIFT+upArrow"] = "prevLine"

    # Maps all 10 numeric keyboard keys to the apropriate gesture.
    # It was done this way to avoid code repetition and to facilitate adding more commands in the future.
    for keyboardKey in range(10):
        __gestures[f"kb:NVDA+CONTROL+{keyboardKey}"] = "saveToMemory"
        __gestures[f"kb:NVDA+CONTROL+SHIFT+{keyboardKey}"] = "speakAndCopyMemory"

    # Maps minus and equals for 2 additional slots
    for key in ("-", "="):
        __gestures[f"kb:NVDA+CONTROL+{key}"] = "saveToMemory"
        __gestures[f"kb:NVDA+CONTROL+SHIFT+{key}"] = "speakAndCopyMemory"

    # Maps numpad keys for 10 additional slots
    for keyboardKey in range(10):
        __gestures[f"kb:NVDA+CONTROL+numpad{keyboardKey}"] = "saveToMemory"
        __gestures[f"kb:NVDA+CONTROL+SHIFT+numpad{keyboardKey}"] = "speakAndCopyMemory"

    # Maps backspace, numpad minus and numpad plus for 3 additional slots
    for key in ("backspace", "numpadMinus", "numpadPlus"):
        __gestures[f"kb:NVDA+CONTROL+{key}"] = "saveToMemory"
        __gestures[f"kb:NVDA+CONTROL+SHIFT+{key}"] = "speakAndCopyMemory"
