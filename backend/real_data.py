"""
Real Data Library - Curated authentic data samples
"""
import random
from models import DataCategory, DifficultyLevel

class RealDataLibrary:
    """Library of real data samples for comparison"""

    def __init__(self):
        self.data = {
            DataCategory.CUSTOMER_REVIEW: {
                DifficultyLevel.EASY: [
                    "great product would buy again",
                    "not worth the money tbh, broke after 2 weeks :(",
                    "Pretty good I guess. Does what it says",
                    "LOVE THIS!! best purchase ever!!!",
                    "meh its ok nothing special"
                ],
                DifficultyLevel.MEDIUM: [
                    "So I was skeptical at first but after using it for a month I'm actually impressed. Battery life could be better tho.",
                    "Works well enough for the price point. Setup was a bit confusing but customer service helped me out. 4/5",
                    "idk why ppl are complaining, mine works perfectly fine lol been using daily for 3 months",
                    "Would give 5 stars but shipping took forever and box was damaged. Product itself is solid though",
                    "Not bad! My only complaint is its a little bulky for what I needed but otherwise no issues"
                ],
                DifficultyLevel.HARD: [
                    "Ok so first off let me say I NEVER write reviews but this deserved one. Got it as a gift for my wife and she literally uses it every single day. Only weird thing is it makes this clicking noise sometimes? Not a dealbreaker but kinda annoying. Overall tho def recommend if ur on the fence about it",
                    "Honestly expected more for the price but its fine I guess. The color is slightly different than the photos (more of a navy than royal blue) and it feels cheaper than I thought itd be. Still works tho so whatever. Shipping was fast at least",
                    "UPDATE: changing my review from 3 to 5 stars!! I initially had issues getting it to connect to my wifi but turns out I was just doing it wrong lmao. Once I figured it out (shoutout to the youtube tutorials) it's been amazing. Super intuitive and my kids love it too",
                    "been using this for my small business for about 6 months now and honestly cant imagine going back to the old setup. Yes its pricey but the time it saves me is worth every penny. My only gripe is the mobile app is kinda buggy on Android but the desktop version is perfect",
                    "so i bought this bc everyone on tiktok was raving about it and i was like ok lemme see what the hype is about... and yeah its actually pretty good?? like not life-changing but definitely worth it. also it came with a cute little carrying case which was a nice surprise lol"
                ]
            },
            DataCategory.PRODUCT_DESCRIPTION: {
                DifficultyLevel.EASY: [
                    "Wireless Bluetooth Speaker with LED lights. Portable and rechargeable. Great sound quality.",
                    "Stainless steel water bottle. Keeps drinks cold for 24 hours. BPA free and leak proof.",
                    "Ergonomic office chair with lumbar support. Adjustable height and armrests. Black mesh design."
                ],
                DifficultyLevel.MEDIUM: [
                    "Meet your new favorite coffee maker. This sleek, programmable brewer delivers barista-quality coffee at the touch of a button. Features a built-in grinder, thermal carafe, and customizable brew strength. Start your mornings right.",
                    "Transform your living space with our ultra-soft microfiber throw blanket. Available in 12 rich colors, this versatile blanket is perfect for cozy nights on the couch or adding a pop of color to your bedroom. Machine washable for easy care.",
                    "Elevate your cooking game with this professional-grade chef's knife. Hand-forged from high-carbon German steel, it features a razor-sharp edge that holds its precision through years of use. The ergonomic pakkawood handle ensures comfort and control."
                ],
                DifficultyLevel.HARD: [
                    "Introducing the NightVision Pro 4K Security Camera - your 24/7 guardian. Cutting-edge AI detection distinguishes between people, pets, and vehicles, eliminating false alerts. Crystal-clear 4K resolution captures every detail, while advanced night vision illuminates up to 30 feet in complete darkness. Weatherproof construction stands up to any climate, and two-way audio lets you communicate from anywhere. Works seamlessly with Alexa and Google Home. Protect what matters most with professional-grade security made simple.",
                    "Discover the freedom of wireless. These next-gen earbuds deliver studio-quality sound with adaptive noise cancellation that adjusts to your environment. Transparency mode keeps you connected when you need to be, while spatial audio creates an immersive listening experience. With 8 hours of playtime per charge (32 hours with the case), quick-charge functionality, and IPX7 water resistance, they're built for your lifestyle. Three sizes of silicone tips ensure the perfect fit. Your music, your way.",
                    "Experience comfort redefined with our premium memory foam mattress. Engineered with three layers of CertiPUR-US certified foam, it contours to your body while providing optimal spinal alignment. The cooling gel-infused top layer regulates temperature throughout the night, while the high-density support core ensures durability for years to come. Hypoallergenic and dust-mite resistant cover is removable and machine washable. Available in all standard sizes. 100-night trial with free returns. Sleep better, live better."
                ]
            },
            DataCategory.USER_PROFILE: {
                DifficultyLevel.EASY: [
                    "Software engineer. Love coding and gaming.",
                    "Fitness enthusiast. Always at the gym!",
                    "Travel blogger exploring the world one country at a time."
                ],
                DifficultyLevel.MEDIUM: [
                    "Part-time barista, full-time plant parent. Trying to keep 37 houseplants alive while perfecting my latte art.",
                    "High school history teacher by day, amateur astronomer by night. Mars enthusiast. Dad jokes are my specialty.",
                    "Freelance graphic designer. Cat mom to 3 chaos agents. Always looking for my next creative project (and coffee)."
                ],
                DifficultyLevel.HARD: [
                    "reformed finance bro turned pottery instructor bc life's too short to stare at spreadsheets. currently attempting sourdough (send help). he/him. prob listening to bon iver rn",
                    "PhD student researching marine biology but mostly just stressed about my thesis lol. shark conservation advocate. certified scuba diver. if I'm not in the lab I'm probably at the beach or rewatching The Office for the 47th time",
                    "ex-corporate lawyer who said nope and opened a bookstore/cafe in my hometown. living my cottagecore fantasy. chronically online. will absolutely judge ur TBR. she/they. pisces sun, virgo moon (it explains everything)"
                ]
            },
            DataCategory.CODE_SNIPPET: {
                DifficultyLevel.EASY: [
                    """def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)
print(result)""",

                    """numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(total)""",

                    """def greet(name):
    return f"Hello, {name}!"

message = greet("World")
print(message)"""
                ],
                DifficultyLevel.MEDIUM: [
                    """def calculate_discount(price, discount_percent):
    # Calculate final price after discount
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return round(final_price, 2)

# Example usage
original = 99.99
discounted = calculate_discount(original, 15)
print(f"Final price: ${discounted}")""",

                    """def find_duplicates(items):
    seen = set()
    duplicates = []
    for item in items:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)
    return duplicates""",

                    """import json

def load_config(filepath):
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Config file not found: {filepath}")
        return {}"""
                ],
                DifficultyLevel.HARD: [
                    """def process_user_data(raw_data, filters=None):
    \"\"\"Process and validate user data with optional filters.\"\"\"
    filters = filters or {}

    processed = []
    for user in raw_data:
        # Skip inactive users
        if not user.get('active', True):
            continue

        # Apply age filter if specified
        if 'min_age' in filters:
            if user.get('age', 0) < filters['min_age']:
                continue

        # Normalize email
        email = user.get('email', '').lower().strip()
        if '@' not in email:
            continue  # Invalid email

        processed.append({
            'id': user['id'],
            'name': user['name'],
            'email': email,
            'created_at': user.get('created_at', 'unknown')
        })

    return processed""",

                    """class CacheManager:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}

    def get(self, key):
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Evict least frequently used
            lfu_key = min(self.access_count, key=self.access_count.get)
            del self.cache[lfu_key]
            del self.access_count[lfu_key]

        self.cache[key] = value
        self.access_count[key] = 0""",

                    """async def fetch_with_retry(url, max_retries=3):
    \"\"\"Fetch URL with exponential backoff retry logic.\"\"\"
    import asyncio
    import aiohttp

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            await asyncio.sleep(wait_time)"""
                ]
            }
        }

    def get_sample(self, category: DataCategory, difficulty: DifficultyLevel) -> str:
        """Get a random real data sample for the given category and difficulty"""
        samples = self.data.get(category, {}).get(difficulty, [])
        if not samples:
            # Fallback to easier difficulty if not found
            samples = self.data.get(category, {}).get(DifficultyLevel.MEDIUM, [])
        if not samples:
            return "Sample data not available"

        return random.choice(samples)
