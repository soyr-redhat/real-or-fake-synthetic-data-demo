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
                    "Great product, would buy again!",
                    "Not worth the money.",
                    "Works great in a Samsung Galaxy S3.",
                    "Fast, very fast",
                    "Good quality, would recommend",
                    "It does the job.",
                    "Best breakfast buffet!!!",
                    "Will be back again!",
                    "Food arrived quickly!",
                    "Highly recommended.",
                    "Loved it...friendly servers, great food, wonderful and imaginative menu.",
                    "The fries were great too.",
                    "Omelets to die for!",
                    "Everything was fresh and delicious!",
                    "A great touch."
                ],
                DifficultyLevel.MEDIUM: [
                    "Purchased this for my device, it worked as advertised. You can never have too much phone memory, since I download a lot of stuff this was a no brainer for me.",
                    "Works in a HTC Rezound. Was running short of space on a 64GB Sandisk so I ordered this when it came out, fast and no issues.",
                    "It works, but file writes are a bit slower than expected on a USB3 reader. Also, both reads and writes are FASTER with the card inside the standard-size SD adapter.",
                    "I have it in my phone and it never skips a beat. File transfers are speedy and have not had any corruption issues or memory fade issues as I would expect from the Sandisk brand.",
                    "got this because i had a 2 GB one that filled up. i kept getting the insufficient disk space on my phone. my kids take my phone and do selfies. mostly my daughter. Now I have plenty of space.",
                    "Stopped by during the late May bank holiday off Rick Steve recommendation and loved it.",
                    "The potatoes were like rubber and you could tell they had been made up ahead of time being kept under a warmer.",
                    "The cashier had no care what so ever on what I had to say it still ended up being wayyy overpriced.",
                    "Waitress was a little slow in service.",
                    "The selection on the menu was great and so were the prices."
                ],
                DifficultyLevel.HARD: [
                    "It's hard to believe how affordable digital has become. 32 GB in a device one quarter the size of postage stamp would have been science fiction less than a generation ago. I picked this up for portable music when I didn't want to schlep (or risk) a phone or iPod. Works great with all SD card readers. Select with confidence.",
                    "I bought this to use with my go pro hero 3 black edition. It requires a class 10 MicroSDXC card. So far I've had no issues with it. Fast read/write, came with adapter, small packaging, but that's all it needed! Comes with a nice hard plastic case to keep both dry and together if needed.",
                    "Ordered this for a Galaxy S3. Lasted a few months and then broke. Is not accessible on several different PC's. Says 'limited lifetime' warranty - BS. You have ONE MONTH for Eco Zone. Not only did I lose pictures but now I am out $$ because of a crappy return policy. UPDATE: Amazon Customer service made good and refunded my purchase price. I still will not be buying any more Sandisk memory cards however...",
                    "I got this because I just couldn't pass up the deal, $17.99. It has been incredibly fast in my HTC Sensation 4g. Pictures are taken and saved instantaneously. Only had it a few days, but have been very happy. Shipping was fast and the packaging was easy to open which is always great in my book. Only issue I had was I had to format it on my computer first before my phone was able to recognize it.",
                    "I bought two of these one for my Samsung tablet and one for my samsung galaxy note. Great hardware that is truly speedy, responsive and meets my needs! I purchased this after my wife and I bought our Samsung Galaxy S4 to store all the music, pictures and videos. The S4 camera is capable of capturing 16-megapixels photos so the 16GB microSD that I had will not suffice.",
                    "My side Greek salad with the Greek dressing was so tasty, and the pita and hummus was very refreshing.",
                    "He came running after us when he realized my husband had left his sunglasses on the table.",
                    "Coming here is like experiencing an underwhelming relationship where both parties can't wait for the other person to ask to break up.",
                    "It's like a really sexy party in your mouth, where you're outrageously flirting with the hottest person at the party.",
                    "walked in and the place smelled like an old grease trap and only 2 others there eating."
                ]
            },
            DataCategory.PRODUCT_DESCRIPTION: {
                DifficultyLevel.EASY: [
                    "1m long Type-C USB Cable. Sturdy and Durable. With USB cable you can transfer data with speeds of upto 480 Mbps. Upto 3A output. 6 months warranty.",
                    "1M Long Cable. Usb 2.0 (Type A) Toughened Joints. Strong And Sturdy.",
                    "USB Type-C to Type-C cable with universal compatibility. 1m Length & Reversible design. High Speed Data/Charging with USB 2.0.",
                    "Micro usb cable is 1 meter in length, optimized for easy use for your comfort at home or office."
                ],
                DifficultyLevel.MEDIUM: [
                    "Compatible with all Type C enabled devices, be it an android smartphone (Mi, Samsung, Oppo, Vivo, Realme, OnePlus, etc), tablet, laptop (Macbook, Chromebook, etc). Supports Quick Charging (2.0/3.0). Unbreakable – Made of special braided outer with rugged interior bindings, it is ultra-durable cable that won't be affected by daily rough usage.",
                    "The boAt Deuce USB 300 2 in 1 cable is compatible with smartphones, tablets, PC peripherals, Bluetooth speakers, power banks and all other devices with Type-C as well as Micro USB port. It ensures 3A fast charging and data transmissions with rapid sync at 480 mbps. The premium Nylon braided skin makes it sturdy and invincible against external damage.",
                    "Flexible, lightweight HDMI cable for connecting media devices to playback display such as HDTVs, projectors, and more. Compatible with Blu-Ray players, computers, Apple TV, Roku, cable, PS4, Xbox One, and other HDMI-compatible devices. Solid copper conductors and full metal jacket shielding for durability and high-performance connectivity.",
                    "USB WiFi Adapter — Speedy wireless transmission at up to 150Mbps ideal for video streaming or internet calls. Mini Design — Sleek miniature design so small that once plugged in, can be left in a Laptop's USB port. Advanced Security — Supports 64/128 WEP, WPA, PA2/WPA-PSK/WPA2-PSK(TKIP/AES)."
                ],
                DifficultyLevel.HARD: [
                    "Universal Compatibility – It is compatible with all Micro USB enabled devices, be it an android smartphone, tablet, PC peripheral or any other micro USB compatible device. Unbreakable – Made of special braided outer with rugged interior bindings, it is ultra-durable cable that won't be affected by daily rough usage. Ideal Length – It has ideal length of 1.5 meters which is neither too short like your typical 1meter cable or too long like a 2meters cable. Supports maximum 3A fast charging and 480 Mbps data transfer speed.",
                    "High Speed WiFi — Up to 600Mbps speeds with 200Mbps on 2.4GHz and 433 Mbps on 5GHz, upgrades your devices to higher AC WiFi speeds. Dual Band Wireless — 2.4GHz and 5GHz band for flexible connectivity, upgrades your devices to work with the latest dual-band WiFi router for faster speed and extended range. Nano design — Small, unobtrusive design allows you to plug it in and forget it is even there. Operating System — Supports Windows 11/10/8.1/8/7/XP, Mac OS 10.15 and earlier.",
                    "Fast Charging & Data Sync: Solero MB301 micro USB cable supports fast charge up to 5V/3A for devices and data syncing speed up to 480Mbps. Universal Compatibility: This USB charging cable connects micro USB port devices with standard USB port devices like laptops, hard drives, power banks, wall and car chargers, etc. Rough & Tough USB Cable: Charging cable with a double-braided exterior, premium aramid fiber core and metal plugs. It has passed 10,000 bending tests and can easily withstand daily use. Extended Length: 1.5-meter long micro USB data and charging cable use nylon material to protect the wire and avoid knots.",
                    "3A/QC 3.0 FAST CHARGING and DATA SYNC: This USB C cable supports QC 3.0 Fast Charging and Data Syncing, max current 3.0A and transfer speed up to 480Mbps. Built-in 56K pull-up resistor and strong metal connections provides reliable conductivity and stability. Nylon Braided Tangle-free Design: Premium Nylon Braided Type C Cable/Lead adds additional durability and tangle free with a tested lifespan of 10000+ bending test. SAFE & RELIABLE: High-purity copper wire features anti-oxidation and anti-rust, which will keep long-lasting fast charging performance."
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
print(message)""",

                    """def proxy_type(self):
    \"\"\"
    Returns proxy type as `ProxyType`.
    \"\"\"
    return self.proxyType""",

                    """def __rdivmod__(self, *args, **kwargs):
    \"\"\" Return divmod(value, self). \"\"\"
    pass""",

                    """def Name(self):
    \"\"\"Return the name corresponding to an object.\"\"\"
    return that"""
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
        return {}""",

                    """@staticmethod
def _to_list(x: Optional[Any]) -> List[Any]:
    \"\"\"Convert object to a list if it is not a list, `None` converted to empty list.\"\"\"
    if x is None:
        x = []
    return x""",

                    """def get_kinetic_matrix(self):
    \"\"\"Kinetic matrix.\"\"\"
    return self._kinetic_matrix

def set_preferred_dgps_timeout(self, timeout):
    '''set the preferred DGPS timeout for receiver'''
    self.preferred_dgps_timeout = timeout
    if timeout is not None:
        return True""",

                    """constraints = []

def add_constraint(constraint):
    constraints.append(constraint)
    return len(constraints)"""
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
            await asyncio.sleep(wait_time)""",

                    """@staticmethod
def get_backtrack_config(curr_config, updated_config):
    diff = DatabaseOptions.get_options_diff(curr_config, updated_config)
    bt_config = {}
    for option in diff:
        if option in curr_config:
            bt_config[option] = curr_config[option]
    return bt_config""",

                    """def test_validate_without_timesheet(self):
    # employee creates a leave request
    number_of_days = (self.leave_end_datetime - self.leave_start_datetime).days
    holiday = self.Requests.with_user(self.user_employee).create({
        'name': 'Leave Request',
        'holiday_status_id': self.leave_type.id,
        'date_from': self.leave_start_datetime,
        'date_to': self.leave_end_datetime,
        'number_of_days': number_of_days,
    })
    return holiday""",

                    """def get(self):
    \"\"\"Return the result of calling the function or reraise any exceptions
    that were raised.
    \"\"\"
    if self._exception is not None:
        raise self._exception
    return self._result"""
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
