# agent_runner.py

import os
import json
import anthropic
from prompts import PROMPTS
from dotenv import load_dotenv
from utils import pretty_print_json, extract_json_block, save_raw_draft

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

def unescape_json_strings(obj):
    """Recursively decode all strings in a JSON-like structure."""
    if isinstance(obj, dict):
        return {k: unescape_json_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [unescape_json_strings(i) for i in obj]
    elif isinstance(obj, str):
        return obj.encode("utf-8").decode("unicode_escape")
    else:
        return obj

def ask_agent(agent_name, user_input, temperature=0.7):
    system_prompt = PROMPTS[agent_name]

    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_input}]
    )

    raw = response.content[0].text.strip()
    json_text = extract_json_block(raw)

    try:
        parsed = json.loads(json_text)
        parsed = unescape_json_strings(parsed)

        # Auto-save long writer content for inspection
        if agent_name == "writer" and "content" in parsed:
            save_raw_draft(parsed["content"], filename="latest_draft.md")

        return parsed

    except json.JSONDecodeError:
        print(f"\n⚠️ Failed to parse JSON from {agent_name}:\n")
        pretty_print_json(raw)

        if agent_name == "writer":
            save_raw_draft(raw)
            return {"content": raw}

        return {
            "decision": "revise",
            "reason": "Claude returned unstructured output.",
            "comments": raw
        }
