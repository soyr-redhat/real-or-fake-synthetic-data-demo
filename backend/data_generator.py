"""
Synthetic Data Generator using LLM
"""
import os
import httpx
from models import DataCategory, DifficultyLevel

class DataGenerator:
    """Generates synthetic data using LLM API"""

    def __init__(self):
        self.api_url = os.getenv("LLM_API_URL", "https://litellm-litemaas.apps.prod.rhoai.rh-aiservices-bu.com/v1")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("MODEL_NAME", "Mistral-Small-24B-W8A8")
        self.last_prompt = ""  # Store last prompt for educational reveal

    async def generate_synthetic(
        self,
        category: DataCategory,
        difficulty: DifficultyLevel,
        real_sample: str
    ) -> str:
        """Generate synthetic data matching the category and difficulty"""

        # Build prompt based on category
        prompts = {
            DataCategory.CUSTOMER_REVIEW: self._review_prompt,
            DataCategory.PRODUCT_DESCRIPTION: self._product_prompt,
            DataCategory.USER_PROFILE: self._profile_prompt,
            DataCategory.CODE_SNIPPET: self._code_prompt,
        }

        prompt_fn = prompts.get(category, self._review_prompt)
        prompt = prompt_fn(difficulty, real_sample)
        self.last_prompt = prompt

        # Generate using LLM
        try:
            synthetic = await self._call_llm(prompt, difficulty)
            return synthetic
        except Exception as e:
            print(f"Error generating synthetic data: {e}")
            # Fallback to simple transformation of real sample
            return self._fallback_generation(category, real_sample)

    def _review_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for customer review"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a generic customer review for a product. Make it obviously AI-generated with perfect grammar and corporate language. 2-3 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a customer review similar to this one in style and tone: '{real_sample}'. Make it realistic but don't copy it. Include natural language quirks. 2-4 sentences."
        else:  # HARD
            return f"Write a customer review that sounds extremely authentic and human-written. Study this example: '{real_sample}'. Match the informal tone, include typos or casual grammar if present, and make it indistinguishable from real reviews. 2-4 sentences."

    def _product_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for product description"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a basic product description for a consumer electronics item. Use simple, formal language. 2-3 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a product description similar to this style: '{real_sample}'. Make it engaging and realistic. 2-4 sentences."
        else:  # HARD
            return f"Write a highly authentic product description matching this style: '{real_sample}'. Include specific details, marketing language, and make it indistinguishable from real product copy. 3-4 sentences."

    def _profile_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for user profile"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a brief user profile bio for a social media platform. Keep it generic and simple. 1-2 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a user profile bio similar to this one: '{real_sample}'. Make it sound natural and authentic. 1-3 sentences."
        else:  # HARD
            return f"Write a highly realistic user profile bio matching this style: '{real_sample}'. Include personality quirks, specific interests, and make it indistinguishable from a real person's bio. 2-3 sentences."

    def _code_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for code snippet"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a simple Python function with basic logic. Use generic variable names and perfect formatting."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a Python function similar to this style: '{real_sample}'. Make it realistic with some comments. 5-10 lines."
        else:  # HARD
            return f"Write Python code matching this style: '{real_sample}'. Include realistic variable names, potential edge cases, and make it look like production code. 8-15 lines."

    async def _call_llm(self, prompt: str, difficulty: DifficultyLevel) -> str:
        """Call the LLM API to generate text"""

        # Adjust temperature based on difficulty
        temperature_map = {
            DifficultyLevel.EASY: 0.3,    # Lower temp = more predictable
            DifficultyLevel.MEDIUM: 0.7,  # Medium temp = balanced
            DifficultyLevel.HARD: 0.9,    # Higher temp = more creative/human-like
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature_map.get(difficulty, 0.7),
                    "max_tokens": 200
                }
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()

    def _fallback_generation(self, category: DataCategory, real_sample: str) -> str:
        """Fallback generation if LLM fails"""
        if category == DataCategory.CUSTOMER_REVIEW:
            return "This product exceeded my expectations. The quality is outstanding and delivery was fast. Highly recommend to anyone looking for a reliable option. Five stars!"
        elif category == DataCategory.PRODUCT_DESCRIPTION:
            return "Premium quality wireless headphones featuring advanced noise cancellation technology. Enjoy crystal-clear audio with up to 30 hours of battery life. Perfect for work, travel, or leisure."
        elif category == DataCategory.USER_PROFILE:
            return "Tech enthusiast and coffee lover. Passionate about AI, open source, and building cool stuff. Always learning something new!"
        else:  # CODE_SNIPPET
            return """def calculate_average(numbers):
    # Calculate the average of a list of numbers
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)"""
