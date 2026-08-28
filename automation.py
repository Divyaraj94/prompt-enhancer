import time
import keyboard
import pyperclip
import pyautogui


class AutomationError(Exception):
    """Custom exception for automation-related errors."""
    pass


class TextAutomation:
    """Grabs selected text via Ctrl+C and replaces it via Ctrl+V."""

    def get_selected_text(self) -> str:
        """Copies the currently selected text and returns it."""
        pyperclip.copy("")
        time.sleep(0.1)

        try:
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.25)
            return pyperclip.paste()
        except Exception as e:
            raise AutomationError(f"Failed to copy text: {e}") from e

    def replace_selected_text(self, new_text: str) -> None:
        """Replaces the currently selected text with new_text via Ctrl+V."""
        try:
            pyperclip.copy(new_text)
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.05)
        except Exception as e:
            raise AutomationError(f"Failed to replace text: {e}") from e