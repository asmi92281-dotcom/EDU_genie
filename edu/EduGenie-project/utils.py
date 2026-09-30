import json
import re
from typing import Any


def clean_json_block(text: str) -> str:
    """Remove Markdown fences and surrounding prose when a model returns JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    match = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
    return match.group(1).strip() if match else text


def parse_json(text: str) -> Any:
    return json.loads(clean_json_block(text))
