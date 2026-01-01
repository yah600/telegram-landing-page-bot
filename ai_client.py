"""
AI Client with Groq - optimized for rate limits.
"""

import os
import logging
import time

logger = logging.getLogger(__name__)


class AIClient:
    """Groq AI client with rate limit handling."""

    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.groq_client = None
        self.last_call = 0

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
        max_tokens: int = 4000,
        temperature: float = 0.7,
        prefer_deepseek: bool = False
    ) -> str:
        """Generate with rate limit handling."""

        # Throttle requests
        elapsed = time.time() - self.last_call
        if elapsed < 3:
            time.sleep(3 - elapsed)

        # Truncate very long prompts
        if len(prompt) > 20000:
            prompt = prompt[:20000] + "\n\n[Content truncated for length]"

        models = [
            ("llama-3.3-70b-versatile", 4000),
            ("gemma2-9b-it", 4000),
        ]

        errors = []
        for model, tokens in models:
            try:
                logger.info(f"Trying {model}")
                self.last_call = time.time()
                result = await self._generate(prompt, tokens, temperature, model)
                if result:
                    return result
            except Exception as e:
                err = str(e)[:80]
                errors.append(f"{model}: {err}")
                logger.warning(f"{model} failed: {err}")
                if "429" in str(e):
                    time.sleep(10)
                continue

        raise Exception(f"All failed: {errors}")

    async def generate_code(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.3) -> str:
        return await self.generate(prompt, max_tokens, temperature)

    async def _generate(self, prompt: str, max_tokens: int, temp: float, model: str) -> str:
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
