import sys
import json
import os
import keyboard

from llm_service import LLMService
from automation import TextAutomation

DEFAULT_SETTINGS = {
    "hotkeys": {
        "grammar": "f7",
        "prompt": "f8",
        "mix": "f9"
    }
}

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")

def load_settings():
    """Load hotkey settings from settings.json. Creates default file if missing."""
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
        print(f"Created default settings file: {SETTINGS_FILE}")

    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def main():
    print("Starting AI Prompt Coach...")

    # Load hotkey settings
    settings = load_settings()
    hotkeys = settings.get("hotkeys", DEFAULT_SETTINGS["hotkeys"])
    hk_grammar = hotkeys.get("grammar", "f7")
    hk_prompt = hotkeys.get("prompt", "f8")
    hk_mix = hotkeys.get("mix", "f9")

    # Initialize services
    try:
        llm = LLMService(os.getenv("GEMINI_API_KEY"))
        print("LLM connected.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    automation = TextAutomation()

    def process(mode, hotkey_name):
        print(f"\n[{hotkey_name}] Processing ({mode})...")
        try:
            text = automation.get_selected_text()
            if not text or not text.strip():
                print("No text selected. Skipping.")
                return

            print(f"Input: '{text[:80]}...'")
            result = llm.enhance_text(text, mode=mode)
            print(f"Output: '{result[:80]}...'")

            automation.replace_selected_text(result)
            print("Done!")

        except Exception as e:
            print(f"Error: {e}")

    # Register hotkeys
    keyboard.add_hotkey(hk_grammar, lambda: process('grammar', hk_grammar.upper()))
    keyboard.add_hotkey(hk_prompt, lambda: process('prompt', hk_prompt.upper()))
    keyboard.add_hotkey(hk_mix, lambda: process('mix', hk_mix.upper()))

    print(f"\n[{hk_grammar.upper()}] Grammar  |  [{hk_prompt.upper()}] Prompt  |  [{hk_mix.upper()}] Mix")
    print(f"Settings: {SETTINGS_FILE}")
    print("Press Ctrl+C in this terminal to exit.\n")

    try:
        # Wait forever. (Previously this waited for 'esc', but pressing Esc 
        # during normal computer use would accidentally kill the app)
        keyboard.wait()
    except KeyboardInterrupt:
        pass
    finally:
        keyboard.unhook_all()
        print("Exiting.")

if __name__ == "__main__":
    main()
