"""mathkit: a tiny utility toolkit used as an AgentDelta evaluation fixture."""

from mathkit.io import read_fixture
from mathkit.sequences import chunk, dedupe
from mathkit.stats import mean, variance
from mathkit.text import slugify, word_count

__all__ = ["mean", "variance", "chunk", "dedupe", "word_count", "slugify", "read_fixture"]
__version__ = "0.1.0"
