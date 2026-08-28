import os
import google.generativeai as genai
import google.api_core.exceptions
from typing import Optional

class LLMService:
    """Handles communication with the Google Generative AI API."""

    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "Google Generative AI API key not found. "
                "Please set the 'GOOGLE_API_KEY' environment variable "
                "or pass it directly to LLMService."
            )

        genai.configure(api_key=api_key)
        # gemini-2.5-flash-lite: optimized for speed, no thinking overhead
        self._model = genai.GenerativeModel('gemini-2.5-flash-lite')
        # Generation config: low temperature for accuracy, limited tokens for speed
        self._gen_config = genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1024,
        )

    def enhance_text(self, original_text: str, mode: str = 'mix') -> str:
        """Processes the text based on the selected mode."""
        if not original_text.strip():
            return original_text 

        if mode == 'grammar':
            instruction = "Fix grammar, spelling, and punctuation only. Keep the original tone and vocabulary."
        elif mode == 'prompt':
            instruction = "Rewrite this as a detailed, clear AI prompt. Improve structure and vocabulary."
        else:
            instruction = "Fix grammar, improve clarity, and make the writing more professional and concise."

        prompt = (
            f"{instruction}\n"
            "Reply with ONLY the improved text, nothing else.\n\n"
            f"{original_text}"
        )

        try:
            response = self._model.generate_content(prompt, generation_config=self._gen_config)
            return response.text.strip()
        except genai.types.BlockedPromptException as e:
            raise RuntimeError(f"LLM API blocked the prompt/response due to safety concerns: {e}")
        except google.api_core.exceptions.GoogleAPIError as e:
            raise RuntimeError(f"Google Generative AI API error occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during text enhancement: {e}")