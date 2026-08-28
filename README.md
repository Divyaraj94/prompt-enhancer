# AI Prompt Coach 🚀

A lightweight desktop tool that enhances your writing in real-time using Google Gemini AI. Select text anywhere, press a hotkey, and get instant grammar fixes or prompt enhancements.

## Features

- **Grammar Fix (F7)** — Corrects spelling, grammar, and punctuation while keeping your original tone
- **Prompt Enhance (F8)** — Rewrites your text into a detailed, professional AI prompt
- **Mix Mode (F9)** — Fixes grammar + improves clarity and professionalism
- **Customizable Hotkeys** — Change keys anytime via `settings.json`
- **Works Everywhere** — Select text in any app (Notepad, browser, email, etc.)

## Setup

1. Install dependencies:
   ```bash
   pip install keyboard pyperclip pyautogui google-generativeai
   ```

2. Add your Google Gemini API key in `main.py`

3. Run the app:
   ```bash
   python main.py
   ```
   Or double-click `Start_AI_Coach.bat`

## How to Use

1. Select any text in any application
2. Press your hotkey:
   - **F7** → Grammar only
   - **F8** → Prompt enhancement
   - **F9** → Both (grammar + enhance)
3. Your text is instantly replaced with the improved version!

## Customize Hotkeys

Edit `settings.json`:
```json
{
    "hotkeys": {
        "grammar": "f7",
        "prompt": "f8",
        "mix": "f9"
    }
}
```

Restart the app after changing.

## Tech Stack

- Python
- Google Gemini AI (gemini-2.5-flash-lite)
- keyboard, pyautogui, pyperclip
