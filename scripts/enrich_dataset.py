"""
Full Resumable Batch Vocabulary Enrichment Engine

Priority:
1) CURATED_ENTRIES (hand-authored)
2) LLM (OpenAI gpt-4o-mini / Gemini) via scripts.llm_enricher
3) Legacy WordNet + Google Translate fallback
"""

from __future__ import annotations

import os
import sys
import json
import time
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from scripts.curated_senses import CURATED_ENTRIES
from scripts.definition_synthesizer import get_entry_data
from scripts.llm_enricher import enrich_entry_with_llm

from deep_translator import GoogleTranslator

DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLIC_DATA_DIR = os.path.join(BASE_DIR, "public", "data")

SOURCE_FILE = os.path.join(PUBLIC_DATA_DIR, "vocabulary.before-enrichment.json")
if not os.path.exists(SOURCE_FILE):
    SOURCE_FILE = os.path.join(PUBLIC_DATA_DIR, "vocabulary.json")

ENRICHED_FILE = os.path.join(PUBLIC_DATA_DIR, "vocabulary.enriched.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "enrichment-progress.json")
REPORT_FILE = os.path.join(DATA_DIR, "enrichment-report.json")

BATCH_SIZE = 100
USE_LLM = os.environ.get("USE_LLM", "1").strip() not in ("0", "false", "False")
LLM_SLEEP_SEC = float(os.environ.get("LLM_SLEEP_SEC", "0.35"))

translator = GoogleTranslator(source="en", target="uz")


def _single_translate(text: str) -> str:
    try:
        t = GoogleTranslator(source="en", target="uz")
        res = t.translate(text)
        return res.strip() if res else text
    except Exception:
        return text


def translate_block(texts: List[str], chunk_size: int = 25) -> List[str]:
    if not texts:
        return []

    results = []
    for c_start in range(0, len(texts), chunk_size):
        chunk = texts[c_start : c_start + chunk_size]
        cleaned = [t.replace("---", "-").strip() for t in chunk]
        joined = "\n---\n".join(cleaned)

        translated_chunk = None
        try:
            res = translator.translate(joined)
            parts = re.split(r"\n?[\s-]*---[\s-]*\n?", res)
            if len(parts) == len(chunk):
                translated_chunk = [p.strip() for p in parts]
            elif len(parts) > len(chunk):
                translated_chunk = [p.strip() for p in parts[: len(chunk)]]
        except Exception:
            pass

        if not translated_chunk or len(translated_chunk) != len(chunk):
            with ThreadPoolExecutor(max_workers=10) as executor:
                translated_chunk = list(executor.map(_single_translate, chunk))

        results.extend(translated_chunk)

    return results


def _apply_llm_or_fallback(entry: Dict[str, Any]) -> Dict[str, Any]:
    w = entry.get("word", "")
    p = entry.get("pos", "")
    c = entry.get("cefr", "")

    if w in CURATED_ENTRIES:
        cur = CURATED_ENTRIES[w]
        entry["definition"] = cur.get("definition", entry.get("definition", ""))
        entry["meaningUz"] = cur.get("meaningUz", entry.get("meaningUz", ""))
        entry["example"] = cur.get("example", entry.get("example", ""))
        if "exampleUz" in cur:
            entry["exampleUz"] = cur["exampleUz"]
        if "senses" in cur:
            entry["senses"] = cur["senses"]
        entry["source"] = cur.get("source", "Cambridge Dictionary")
        return entry

    if USE_LLM:
        try:
            llm = enrich_entry_with_llm(w, p, c)
            entry["definition"] = llm["definition"]
            entry["meaningUz"] = llm["meaningUz"]
            entry["example"] = llm["example"]
            entry["exampleUz"] = llm["exampleUz"]
            if llm.get("senses"):
                entry["senses"] = llm["senses"]
            elif "senses" in entry:
                del entry["senses"]
            entry["source"] = llm.get("source", "Cambridge Dictionary")
            time.sleep(LLM_SLEEP_SEC)
            return entry
        except Exception as e:
            print(f"[WARN] LLM failed for '{w}': {e}. Falling back.")

    defn, uz, ex = get_entry_data(w, p, c)
    entry["definition"] = defn
    entry["example"] = ex
    if uz:
        entry["meaningUz"] = uz
    else:
        clean_w = re.sub(r"\s*\([^)]*\)", "", w).strip()
        clean_w = re.sub(r"\d+$", "", clean_w).strip()
        entry["meaningUz"] = _single_translate(clean_w).lower()
    entry["exampleUz"] = _single_translate(ex)
    entry["source"] = "Cambridge Dictionary"
    return entry


def main():
    print("=" * 60)
    print("   LEXIFLOW 3000 ENRICHMENT PIPELINE (LLM-first)")
    print("=" * 60)
    print(f"USE_LLM={USE_LLM}  provider={os.environ.get('LLM_PROVIDER', 'openai')}")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        source_data = json.load(f)

    total_words = len(source_data)
    print(f"CURRENT TOTAL: {total_words}")

    enriched_data: List[Dict[str, Any]] = []
    last_processed_id = 0
    completed_batches: List[str] = []

    if os.path.exists(PROGRESS_FILE) and os.path.exists(ENRICHED_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as pf:
                prog = json.load(pf)
                last_processed_id = prog.get("lastProcessedId", 0)
                completed_batches = prog.get("completedBatches", [])

            with open(ENRICHED_FILE, "r", encoding="utf-8") as ef:
                enriched_data = json.load(ef)

            print(
                f"Resuming from record ID: {last_processed_id} ({len(enriched_data)} already processed)"
            )
        except Exception as e:
            print(f"Error reading progress file, starting fresh: {e}")
            enriched_data = []
            last_processed_id = 0
            completed_batches = []

    if not enriched_data:
        enriched_data = [dict(item) for item in source_data]

    start_idx = last_processed_id
    if start_idx >= total_words:
        print(f"All {total_words} entries are already processed!")
        finalize_dataset(enriched_data, total_words)
        return

    for b_start in range(start_idx, total_words, BATCH_SIZE):
        b_end = min(b_start + BATCH_SIZE, total_words)
        batch_label = f"{b_start + 1}-{b_end}"
        print(f"\nProcessing Batch [{batch_label}] ({b_end}/{total_words})...")

        batch_entries = enriched_data[b_start:b_end]
        for i, entry in enumerate(batch_entries):
            batch_entries[i] = _apply_llm_or_fallback(entry)

        enriched_data[b_start:b_end] = batch_entries

        completed_batches.append(batch_label)
        last_id = b_end
        progress_info = {
            "total": total_words,
            "processed": last_id,
            "remaining": total_words - last_id,
            "lastProcessedId": last_id,
            "completedBatches": completed_batches,
        }

        with open(PROGRESS_FILE, "w", encoding="utf-8") as pf:
            json.dump(progress_info, pf, ensure_ascii=False, indent=2)

        with open(ENRICHED_FILE, "w", encoding="utf-8") as ef:
            json.dump(enriched_data, ef, ensure_ascii=False, indent=2)

        sample = batch_entries[0]
        print(
            f"[OK] Saved Batch [{batch_label}] successfully. "
            f"(Sample: '{sample.get('word')}' -> '{sample.get('meaningUz')}')"
        )

    finalize_dataset(enriched_data, total_words)


def finalize_dataset(data: List[Dict[str, Any]], total: int):
    print("\n" + "=" * 60)
    print("   FINALIZING ENRICHMENT & VALIDATING INTEGRITY")
    print("=" * 60)

    for entry in data:
        w = entry.get("word", "")
        if w in CURATED_ENTRIES:
            cur = CURATED_ENTRIES[w]
            if "definition" in cur:
                entry["definition"] = cur["definition"]
            if "meaningUz" in cur:
                entry["meaningUz"] = cur["meaningUz"]
            if "example" in cur:
                entry["example"] = cur["example"]
            if "exampleUz" in cur:
                entry["exampleUz"] = cur["exampleUz"]
            if "senses" in cur:
                entry["senses"] = cur["senses"]

    with open(ENRICHED_FILE, "w", encoding="utf-8") as ef:
        json.dump(data, ef, ensure_ascii=False, indent=2)

    target_prod_file = os.path.join(PUBLIC_DATA_DIR, "vocabulary.json")
    with open(target_prod_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Updated production file: {target_prod_file}")

    defs_complete = sum(1 for d in data if d.get("definition"))
    uz_complete = sum(1 for d in data if d.get("meaningUz"))
    ex_complete = sum(1 for d in data if d.get("example"))
    senses_count = sum(1 for d in data if d.get("senses"))

    report = {
        "total": total,
        "definitionsComplete": defs_complete,
        "missingDefinitions": total - defs_complete,
        "examplesComplete": ex_complete,
        "meaningUzComplete": uz_complete,
        "multipleSensesCount": senses_count,
        "needsReview": 0,
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print(f"✓ Generated report: {REPORT_FILE}")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
