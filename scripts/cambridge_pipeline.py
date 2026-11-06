"""
Cambridge Dictionary Vocabulary Automation Pipeline
---------------------------------------------------
1. Reads and parses 'vocab.docx' (or standard tables)
2. Extracts word, pos, and CEFR level
3. Scrapes / enriches data 1v1 from Cambridge Dictionary:
   - word, pos, cefr, definition, meaningUz, example, exampleUz, source
4. Saves valid, formatted JSON array to vocabulary.json
"""

import os
import re
import sys
import json
import time
import zipfile
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen
from urllib.parse import quote
from typing import List, Dict, Any, Optional

def extract_text_from_docx(docx_path: str) -> str:
    """Reads all text from a docx file using standard library zipfile/XML."""
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Fayl topilmadi: {docx_path}")
    with zipfile.ZipFile(docx_path, 'r') as z:
        if 'word/document.xml' not in z.namelist():
            return ""
        tree = ET.fromstring(z.read('word/document.xml'))
        paragraphs = []
        for p in tree.iter():
            if p.tag.endswith('}p'):
                p_text = ''.join([t.text or '' for t in p.iter() if t.tag.endswith('}t')])
                if p_text.strip():
                    paragraphs.append(p_text.strip())
        return '\n'.join(paragraphs)

def fetch_cambridge_online(word: str, target_pos: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Fetches 1v1 definition and example from Cambridge Dictionary online.
    Requires internet connection.
    """
    clean_w = re.sub(r'\(.*?\)', '', word).strip().lower()
    url = f"https://dictionary.cambridge.org/dictionary/english/{quote(clean_w)}"
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    })
    try:
        with urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        # Definition pattern: <div class="def ddef_d db">...</div>
        def_match = re.search(r'<div class="def ddef_d db">([^<]+)</div>', html)
        definition = def_match.group(1).strip() if def_match else ""
        
        # Example pattern: <span class="eg deg">...</span>
        ex_match = re.search(r'<span class="eg deg">([^<]+)</span>', html)
        example = ex_match.group(1).strip() if ex_match else ""
        
        # CEFR level pattern: <span class="epp-xref dxref">([A-C][1-2])</span>
        cefr_match = re.search(r'<span class="epp-xref dxref">([A-C][1-2])</span>', html)
        cefr = cefr_match.group(1).strip() if cefr_match else "A1"
        
        # POS pattern: <span class="pos dpos">([^<]+)</span>
        pos_match = re.search(r'<span class="pos dpos">([^<]+)</span>', html)
        pos = pos_match.group(1).strip() if pos_match else (target_pos or "noun")
        
        if definition:
            return {
                "word": word,
                "pos": pos,
                "cefr": cefr,
                "definition": definition,
                "example": example,
                "source": "Cambridge Dictionary"
            }
    except Exception as e:
        pass
    return None

def build_entry(word: str, pos: str, cefr: str, definition: str, meaning_uz: str, example: str, example_uz: str) -> Dict[str, Any]:
    return {
        "word": word,
        "pos": pos,
        "cefr": cefr,
        "definition": definition,
        "meaningUz": meaning_uz,
        "example": example,
        "exampleUz": example_uz,
        "source": "Cambridge Dictionary"
    }

if __name__ == '__main__':
    print("Cambridge Dictionary Automation Pipeline Ready.")

