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
            return f"""Write an authentic customer review matching this style: '{real_sample}'.

CRITICAL - Include these human characteristics:
- Specific product details (model names, prices like $19.99, specific phone/device models)
- Personal context and anecdotes (family members, use cases, "I bought this because...")
- Minor typos or casual grammar ("tho", "bc", lowercase i, extra letters like "wayyy")
- Updates or contradictions ("UPDATE:", changing opinion)
- Vivid metaphors or creative comparisons
- Mixed emotions (praise + complaint)
- Conversational asides ("in my book", "just saying", "honestly")
- Specific numbers (used for 3 months, $17.99, 16-megapixel camera)

Write 3-5 sentences that sound like a real person sharing their genuine experience."""

    def _product_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for product description"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a basic product description for a consumer electronics item. Use simple, formal language. 2-3 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a product description similar to this style: '{real_sample}'. Make it engaging and realistic. 2-4 sentences."
        else:  # HARD
            return f"""Write a technical product description matching this style: '{real_sample}'.

CRITICAL - Include these characteristics:
- Very specific technical specs (480Mbps, 5V/3A, 56K resistor, exact measurements)
- Compatibility lists with version numbers (Windows 11/10/8.1/8/7, Mac OS 10.15)
- Certification/testing details (passed 10,000 bending tests, UL certified)
- Marketing formatting with em-dashes (—) and colons
- Title Case section headers followed by colons (Fast Charging & Data Sync:, Universal Compatibility:)
- Brand names and model numbers
- Multiple feature callouts in bullet-point style prose
- Technical terminology (pull-up resistor, aramid fiber, dual-band wireless)

Write 3-4 sentences formatted like real Amazon/e-commerce copy."""

    def _profile_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for user profile"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a brief user profile bio for a social media platform. Keep it generic and simple. 1-2 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a user profile bio similar to this one: '{real_sample}'. Make it sound natural and authentic. 1-3 sentences."
        else:  # HARD
            return f"""Write an authentic social media bio matching this style: '{real_sample}'.

CRITICAL - Include these characteristics:
- Mostly lowercase casual style ("bc", "lol", "rn", "ur", "prob")
- Parenthetical asides with humor ("send help", "it explains everything", "obviously")
- Pronouns explicitly listed (he/him, she/they, they/them)
- Pop culture references (specific shows, musicians, trends)
- Self-deprecating or ironic humor
- Very specific numbers (47th time, 37 plants, 3 cats)
- Internet slang and abbreviations (TBR, cottagecore, chronically online)
- Mix of career/identity statements with personal quirks
- Astrology references if relevant (pisces sun, virgo moon)

Write 2-3 sentences that sound like a real person's Twitter/Instagram bio."""

    def _code_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for code snippet"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a simple Python function with a COMPLETE implementation including the function body. The function should do something basic like list operations, string manipulation, or simple calculations. Use generic variable names and perfect formatting. Include the full working code, not just a signature. 5-10 lines."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a Python function similar to this style: '{real_sample}'. Include the COMPLETE implementation with actual logic in the function body. Make it realistic with some comments and docstrings. Must have working code, not just signatures. 8-15 lines."
        else:  # HARD
            return f"""Write production-quality Python code matching this style: '{real_sample}'.

CRITICAL - Include these characteristics:
- FULL working implementation with complete logic (no 'pass' or '...' placeholders)
- Edge case handling (check for None, empty lists, invalid input)
- Inline comments explaining complex logic (# Skip inactive users, # Invalid email)
- Realistic variable names from actual codebases (processed, raw_data, filters)
- Dictionary/object construction and manipulation
- Type hints if the example has them (Optional[str], List[dict])
- Triple-quoted docstrings with proper formatting
- Common patterns: .get() with defaults, list comprehensions, early returns
- Error handling or validation checks
- Python idioms (using 'or {}' for defaults, '.strip().lower()' for normalization)

Write 10-20 lines that look like they came from a real GitHub repository."""

    async def _call_llm(self, prompt: str, difficulty: DifficultyLevel) -> str:
        """Call the LLM API to generate text"""

        # Adjust temperature based on difficulty
        temperature_map = {
            DifficultyLevel.EASY: 0.3,    # Lower temp = more predictable
            DifficultyLevel.MEDIUM: 0.7,  # Medium temp = balanced
            DifficultyLevel.HARD: 0.9,    # Higher temp = more creative/human-like
        }

        # Adjust max_tokens based on difficulty (HARD needs more for detailed output)
        max_tokens_map = {
            DifficultyLevel.EASY: 150,
            DifficultyLevel.MEDIUM: 250,
            DifficultyLevel.HARD: 400,  # More tokens for detailed human-like content
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
                    "max_tokens": max_tokens_map.get(difficulty, 250)
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
            return """def process_items(items, threshold=10):
    \"\"\"Process items and filter based on threshold.\"\"\"
    result = []
    for item in items:
        if item > threshold:
            result.append(item * 2)
        else:
            result.append(item)
    return result"""
