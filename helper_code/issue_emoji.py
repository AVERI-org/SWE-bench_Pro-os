"""
Append a random sequence of emojis to a problem statement.

Uses the instance ID as a seed so the same instance always gets the same
emoji sequence, ensuring reproducibility across runs.
"""

import hashlib
import random

# A diverse pool of emojis spanning several Unicode blocks.
EMOJI_POOL = [
    "😀", "😂", "🥲", "😎", "🤔", "🤯", "😱", "🥳", "😴", "🤖",
    "👀", "🔥", "✨", "💡", "🚀", "🎯", "🧩", "🪲", "🐛", "🐍",
    "🦀", "🐳", "🌈", "⚡", "💎", "🔧", "🛠️", "📦", "🧪", "🔬",
    "📊", "🗂️", "🏗️", "🎲", "♻️", "🌀", "🔑", "🏷️", "📌", "🧲",
]

MIN_EMOJIS = 5
MAX_EMOJIS = 15


def inject_emojis(problem_statement: str, instance_id: str) -> str:
    """Return *problem_statement* with a random emoji sequence appended."""
    seed = int(hashlib.sha256(instance_id.encode()).hexdigest(), 16)
    rng = random.Random(seed)
    count = rng.randint(MIN_EMOJIS, MAX_EMOJIS)
    emojis = " ".join(rng.choices(EMOJI_POOL, k=count))
    return f"{problem_statement}\n\n{emojis}"
