"""
LLM-based vocabulary enrichment (OpenAI gpt-4o-mini or Google Gemini)
Powered strictly by Cambridge Dictionary.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

SYSTEM_PROMPT = """You are the official Cambridge Dictionary API (https://dictionary.cambridge.org/dictionary/).
You enrich learner vocabulary entries strictly based on the Cambridge Advanced Learner's Dictionary and Cambridge English Corpus.
Use ONLY the provided word, POS, and CEFR level.

Output MUST be a single valid JSON object with exactly these keys:
{
  "word": "...",
  "pos": "...",
  "cefr": "...",
  "definition": "...",
  "meaningUz": "...",
  "examples": [
    {
      "en": "...",
      "uz": "..."
    }
  ],
  "source": "Cambridge Dictionary"
}

No markdown. No code fences. No extra commentary.

Strict Rules:
1. Definition: Must strictly mirror the exact official definition from Cambridge Dictionary for the specified POS and CEFR level. Do NOT use definitions from other dictionaries.
2. Examples: Must include ALL authentic example sentences provided by Cambridge Dictionary for this definition (multiple examples). Format each example as an object with "en" (Cambridge original) and "uz" (accurate Uzbek translation).
3. Translations:
   - meaningUz: Natural, accurate Uzbek translation (Latin script) of the Cambridge definition and lemma.
   - uz (in examples): Accurate, natural Uzbek translation of each Cambridge example sentence.
4. Source: The "source" field MUST always be exactly "Cambridge Dictionary".
5. Match the FIRST POS tag when multiple POS are listed, unless a parenthetical disambiguation is in the word."""

FEW_SHOT_USER_1 = json.dumps(
    {"word": "article", "pos": "noun", "cefr": "B1"},
    ensure_ascii=False,
)
FEW_SHOT_ASSISTANT_1 = json.dumps(
    {
        "word": "article",
        "pos": "noun",
        "cefr": "B1",
        "definition": "a piece of writing on a particular subject in a newspaper or magazine, or on the internet",
        "meaningUz": "gazeta, jurnal yoki internetda ma'lum bir mavzuda yozilgan matn (maqola)",
        "examples": [
            {
                "en": "There was an interesting article on vegetarianism in the paper yesterday.",
                "uz": "Kecha gazetada vegetarianlik haqida qiziqarli maqola bor edi."
            },
            {
                "en": "She has written several articles for national magazines.",
                "uz": "U milliy jurnallar uchun bir nechta maqolalar yozgan."
            }
        ],
        "source": "Cambridge Dictionary"
    },
    ensure_ascii=False,
)

REQUIRED_KEYS = (
    "word",
    "pos",
    "cefr",
    "definition",
    "meaningUz",
    "examples",
    "source",
)


def _strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_payload(data: Dict[str, Any], word: str, pos: str, cefr: str) -> Dict[str, Any]:
    for key in REQUIRED_KEYS:
        if key not in data:
            raise ValueError(f"Missing key: {key}")
    if not isinstance(data.get("examples"), list):
        raise ValueError("examples must be a list of {en, uz} objects")
    
    cleaned_examples: List[Dict[str, str]] = []
    for ex in data["examples"]:
        if isinstance(ex, dict) and "en" in ex:
            cleaned_examples.append({
                "en": str(ex.get("en", "")).strip(),
                "uz": str(ex.get("uz", "")).strip()
            })
    
    data["word"] = word
    data["pos"] = pos
    data["cefr"] = cefr
    data["definition"] = str(data["definition"]).strip()
    data["meaningUz"] = str(data["meaningUz"]).strip()
    data["examples"] = cleaned_examples
    data["source"] = "Cambridge Dictionary"
    return data


def enrich_entry_with_llm(
    word: str,
    pos: str,
    cefr: str,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    provider = provider or os.environ.get("LLM_PROVIDER", "openai").lower()
    user_payload = json.dumps({"word": word, "pos": pos, "cefr": cefr}, ensure_ascii=False)

    if provider == "gemini":
        return _enrich_with_gemini(user_payload, word, pos, cefr)
    return _enrich_with_openai(user_payload, word, pos, cefr)


def _enrich_with_openai(user_payload: str, word: str, pos: str, cefr: str) -> Dict[str, Any]:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": FEW_SHOT_USER_1},
            {"role": "assistant", "content": FEW_SHOT_ASSISTANT_1},
            {"role": "user", "content": user_payload},
        ],
    )
    raw = response.choices[0].message.content or ""
    parsed = json.loads(_strip_fences(raw))
    return _validate_payload(parsed, word, pos, cefr)


def _enrich_with_gemini(user_payload: str, word: str, pos: str, cefr: str) -> Dict[str, Any]:
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    client = genai.Client(api_key=api_key)

    prompt_text = (
        f"{SYSTEM_PROMPT}

"
        f"Example Input:
{FEW_SHOT_USER_1}
"
        f"Example Output:
{FEW_SHOT_ASSISTANT_1}

"
        f"Now enrich this input:
{user_payload}"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt_text,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )
    raw = response.text or ""
    parsed = json.loads(_strip_fences(raw))
    return _validate_payload(parsed, word, pos, cefr)
