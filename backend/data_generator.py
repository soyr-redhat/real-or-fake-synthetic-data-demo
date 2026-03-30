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

Include 2-3 human characteristics from this list:
- Specific product details (model names, prices like $19.99, device models)
- Personal context ("I bought this bc...", family members, use cases)
- Casual grammar ("tho", "bc", lowercase i, "wayyy")
- Vivid metaphors or creative comparisons
- Mixed emotions (praise + complaint)
- Conversational asides ("honestly", "just saying")
- Specific numbers (3 months, $17.99, 16-megapixel)

IMPORTANT: Write EXACTLY 2-3 sentences maximum. Be concise."""

    def _product_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for product description"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a basic product description for a consumer electronics item. Use simple, formal language. 2-3 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a product description similar to this style: '{real_sample}'. Make it engaging and realistic. 2-4 sentences."
        else:  # HARD
            return f"""Write a technical product description matching this style: '{real_sample}'.

Include 2-3 characteristics from this list:
- Specific technical specs (480Mbps, 5V/3A, exact measurements)
- Compatibility lists (Windows 11/10/8.1/8/7, Mac OS 10.15)
- Testing details (passed 10,000 bending tests, certified)
- Title Case headers with colons (Fast Charging:, Universal Compatibility:)
- Marketing em-dashes (—) between features
- Brand names and technical terminology

IMPORTANT: Write EXACTLY 2-3 sentences maximum in e-commerce style."""

    def _profile_prompt(self, difficulty: DifficultyLevel, real_sample: str) -> str:
        """Generate prompt for user profile"""
        if difficulty == DifficultyLevel.EASY:
            return "Write a brief user profile bio for a social media platform. Keep it generic and simple. 1-2 sentences."
        elif difficulty == DifficultyLevel.MEDIUM:
            return f"Write a user profile bio similar to this one: '{real_sample}'. Make it sound natural and authentic. 1-3 sentences."
        else:  # HARD
            return f"""Write an authentic social media bio matching this style: '{real_sample}'.

Include 2-3 characteristics from this list:
- Lowercase casual style ("bc", "lol", "rn", "ur", "prob")
- Parenthetical asides ("send help", "it explains everything")
- Pronouns (he/him, she/they, they/them)
- Pop culture references (shows, musicians, trends)
- Self-deprecating humor
- Specific numbers (47th time, 37 plants)
- Internet slang (TBR, cottagecore, chronically online)
- Career/identity with personal quirks

IMPORTANT: Write EXACTLY 2-3 short sentences maximum."""

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
- Python idioms (using 'or {{}}' for defaults, '.strip().lower()' for normalization)

Write 10-20 lines that look like they came from a real GitHub repository."""

    async def _call_llm(self, prompt: str, difficulty: DifficultyLevel) -> str:
        """Call the LLM API to generate text"""

        # Adjust temperature based on difficulty
        temperature_map = {
            DifficultyLevel.EASY: 0.3,    # Lower temp = more predictable
            DifficultyLevel.MEDIUM: 0.7,  # Medium temp = balanced
            DifficultyLevel.HARD: 0.9,    # Higher temp = more creative/human-like
        }

        # Adjust max_tokens based on difficulty
        max_tokens_map = {
            DifficultyLevel.EASY: 100,
            DifficultyLevel.MEDIUM: 150,
            DifficultyLevel.HARD: 200,  # Enough for 2-3 detailed sentences
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
        """Fallback generation if LLM fails - return more realistic alternatives"""
        import random

        if category == DataCategory.CUSTOMER_REVIEW:
            fallbacks = [
                "got this for my tablet and works perfectly. been using it for about 2 weeks now, no complaints so far. the only thing is i wish it came with a longer cable but thats not a dealbreaker",
                "Ordered this bc it was on sale for $24.99 and honestly pretty happy with the purchase. Setup took like 10 mins but after that its been solid. Would def buy again",
                "Works great in my phone, no issues. Fast shipping too which was nice. Only complaint is the packaging was kinda excessive but whatever, the product itself is good"
            ]
            return random.choice(fallbacks)
        elif category == DataCategory.PRODUCT_DESCRIPTION:
            fallbacks = [
                "Universal Compatibility — Works with all USB enabled devices including smartphones, tablets, laptops and more. Fast Charging Support — Supports up to 3A fast charging for rapid power delivery. Durable Design — Premium braided cable with reinforced connectors tested for 10,000+ bends. Extended Length — 1.5 meter cable provides convenient reach without tangling.",
                "High Speed Data Transfer: Transfer files at up to 480Mbps for quick syncing. Premium Materials: Aircraft-grade aluminum connectors with nylon braided jacket for maximum durability. Multi-Device Support: Compatible with Android, iOS, Windows, and Mac devices. Warranty: 18 month manufacturer warranty included.",
                "Fast Wireless Connectivity — Dual-band support for 2.4GHz and 5GHz networks with speeds up to 300Mbps. Compact Design — Ultra-portable nano adapter fits in your laptop without blocking adjacent ports. Wide Compatibility — Supports Windows 10/8.1/8/7, Mac OS X 10.9 and later."
            ]
            return random.choice(fallbacks)
        elif category == DataCategory.USER_PROFILE:
            fallbacks = [
                "software dev who writes bugs for a living lol. coffee addict. probably debugging something rn. he/him",
                "part time student, full time overthinker. trying to learn guitar (its not going well). playlist curator. they/them",
                "former teacher turned freelance writer bc capitalism. plant parent to 12 succulents. chronically online. she/her"
            ]
            return random.choice(fallbacks)
        else:  # CODE_SNIPPET
            fallbacks = [
                """def validate_email(email):
    \"\"\"Check if email address is valid.\"\"\"
    if not email or '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    return len(parts[0]) > 0 and len(parts[1]) > 0""",
                """def format_price(amount, currency='USD'):
    \"\"\"Format price with currency symbol.\"\"\"
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:.2f}" """,
                """def filter_active_users(users):
    \"\"\"Return only active users from list.\"\"\"
    active = []
    for user in users:
        if user.get('active', False):
            active.append(user)
    return active"""
            ]
            return random.choice(fallbacks)
