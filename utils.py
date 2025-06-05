# utils.py

import json
import re

def pretty_print_json(raw_text):
    """Attempt to print pretty JSON if possible."""
    try:
        parsed = json.loads(raw_text)
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print("\n⚠️ Unparsable JSON, showing raw text:\n")
        print(raw_text)

def extract_json_block(raw):
    """Extract JSON object from messy Claude response."""
    match = re.search(r'(\{.*\})', raw, re.DOTALL)
    return match.group(1) if match else raw

def save_raw_draft(content, filename="fallback_draft.md"):
    """Save raw content to a .md file when Claude doesn't return valid JSON."""
    with open(filename, "w") as f:
        f.write(content.strip())
