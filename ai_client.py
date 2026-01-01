"""
AI Client with Groq - using currently available models.
"""

import os
import logging

logger = logging.getLogger(__name__)


class AIClient:
    """Groq AI client with model fallbacks."""

    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.groq_client = None

        if self.groq_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_key)
                logger.info("Groq initialized")
            except Exception as e:
                logger.warning(f"Groq init failed: {e}")

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        prefer_deepseek: bool = False
    ) -> str:
        """Generate text with model fallback."""

        # Current available Groq models (Dec 2024)
        models = [
            ("llama-3.3-70b-versatile", 32000),
            ("llama-3.1-8b-instant", 8000),
            ("gemma2-9b-it", 8000),
        ]

        errors = []
        for model, max_ctx in models:
            try:
                logger.info(f"Trying {model}")
                result = await self._generate(prompt, min(max_tokens, max_ctx), temperature, model)
                if result and len(result) > 50:
                    logger.info(f"Success with {model}")
                    return result
            except Exception as e:
                err = str(e)[:100]
                errors.append(f"{model}: {err}")
                logger.warning(f"{model} failed: {err}")
                continue

        raise Exception(f"All models failed: {errors}")

    async def generate_code(
        self,
        prompt: str,
        max_tokens: int = 16000,
        temperature: float = 0.3
    ) -> str:
        """Generate code."""
        return await self.generate(prompt, max_tokens, temperature)

    async def _generate(self, prompt: str, max_tokens: int, temp: float, model: str) -> str:
        """Generate with specific model."""
        if not self.groq_client:
            raise Exception("Groq not configured")

        r = self.groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temp
        )
        return r.choices[0].message.content

    def get_status(self) -> dict:
        return {"groq": self.groq_client is not None}
