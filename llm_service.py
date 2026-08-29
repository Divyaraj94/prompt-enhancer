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
        # Using gemini-2.5-flash as it has a larger free-tier quota (1500/day) than lite
        self._model = genai.GenerativeModel('gemini-2.5-flash')
        # Generation config: low temperature for accuracy, limited tokens for speed
        self._gen_config = genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1024,
        )

    def _get_model_for_mode(self, mode: str):
        if mode == 'grammar':
            sys_instruct = "You are a professional editor. Fix grammar, spelling, and punctuation only. Reply with ONLY the improved text. Do not add conversational filler or explanations."
        elif mode == 'prompt':
            sys_instruct = "You are an expert prompt engineer. Rewrite the user's input as a detailed, clear AI prompt. Improve structure and vocabulary. Reply with ONLY the improved prompt."
        else:
            sys_instruct = "You are a professional editor. Fix grammar, improve clarity, and make the writing more professional and concise. Reply with ONLY the improved text."

        return genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=sys_instruct
        )

    def enhance_text(self, original_text: str, mode: str = 'mix') -> str:
        """Processes the text based on the selected mode."""
        if not original_text.strip():
            return original_text 

        model = self._get_model_for_mode(mode)

        try:
            response = model.generate_content(original_text, generation_config=self._gen_config)
            return response.text.strip()
        except genai.types.BlockedPromptException as e:
            raise RuntimeError(f"LLM API blocked the prompt/response due to safety concerns: {e}")
        except google.api_core.exceptions.GoogleAPIError as e:
            raise RuntimeError(f"Google Generative AI API error occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during text enhancement: {e}")