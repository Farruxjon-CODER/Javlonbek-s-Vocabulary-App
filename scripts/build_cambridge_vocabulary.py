"""
Cambridge Dictionary Vocabulary Builder & Enricher
Reads words from vocab.docx (or raw text), retrieves 1v1 Cambridge Dictionary definitions,
examples, CEFR levels, literary Uzbek translations, and saves to vocabulary.json.
"""

import os
import re
import sys
import json
import zipfile
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, 'public', 'data', 'vocabulary.json')

# 1. DOCX Reader
def read_docx(path: str) -> str:
    if not os.path.exists(path):
        return ""
    try:
        with zipfile.ZipFile(path, 'r') as z:
            if 'word/document.xml' not in z.namelist():
                return ""
            tree = ET.fromstring(z.read('word/document.xml'))
            texts = []
            for node in tree.iter():
                if node.tag.endswith('}p'):
                    p_text = ''.join([t.text or '' for t in node.iter() if node.tag.endswith('}t') or t.tag.endswith('}t')])
                    if p_text.strip():
                        texts.append(p_text.strip())
            return '\n'.join(texts)
    except Exception as e:
        print(f"Error reading docx: {e}")
        return ""

# Known POS patterns
POS_PATTERNS = [
    r'number/det\.,\s*pron\.',
    r'det\./pron\./adv\.',
    r'det\./adj\.,\s*pron\.',
    r'det\./pron\.,\s*adv\.',
    r'adj\.,\s*det\./pron\.',
    r'n\.,\s*det\./pron\.',
    r'adj\.,\s*pron\.,\s*adv\.',
    r'adj\.,\s*adv\.,\s*n\.',
    r'adj\.,\s*n\.,\s*prep\.,\s*adv\.',
    r'adv\.,\s*pron\.,\s*conj\.',
    r'pron\.,\s*conj\.',
    r'pron\./det\.',
    r'det\.,\s*pron\.,\s*conj\.',
    r'det\.,\s*pron\.',
    r'det\./pron\.',
    r'adj\./pron\.',
    r'adj\./adv\.',
    r'exclam\.,\s*adj\./adv\.',
    r'exclam\.,\s*v\.,\s*adj\.',
    r'exclam\.,\s*det\.',
    r'exclam\.,\s*n\.',
    r'exclam\./n\.',
    r'adj\.,\s*exclam\.',
    r'prep\.,\s*infinitive\s+marker',
    r'infinitive\s+marker',
    r'indefinite\s+article',
    r'definite\s+article',
    r'modal\s+v\.',
    r'auxiliary\s+v\.',
    r'v\.,\s*auxiliary\s+v\.',
    r'v\.,\s*n\.',
    r'n\.,\s*v\.',
    r'adj\.,\s*v\.',
    r'n\.,\s*adj\.',
    r'adj\.,\s*n\.',
    r'adv\.,\s*prep\.',
    r'prep\.,\s*adv\.',
    r'adv\.,\s*n\.',
    r'n\.,\s*adv\.',
    r'adj\.,\s*adv\.',
    r'adv\.,\s*adj\.',
    r'n\.,\s*adj\.,\s*adv\.',
    r'adj\.,\s*n\.,\s*prep\.',
    r'prep\.,\s*adj\.,\s*adv\.',
    r'conj\./prep\.',
    r'adv\.,\s*conj\.',
    r'adv\./prep\.',
    r'det\./number,\s*adv\.',
    r'det\./number',
    r'pron\.,\s*det\.,\s*adv\.',
    r'det\.,\s*pron\.,\s*adv\.',
    r'adv\.,\s*adj\.,\s*exclam\.',
    r'pron\.,\s*det\.',
    r'number',
    r'n\.',
    r'v\.',
    r'adj\.',
    r'adv\.',
    r'prep\.',
    r'conj\.',
    r'det\.',
    r'pron\.',
    r'exclam\.'
]

POS_NORMALIZATION = {
    'n.': 'noun',
    'v.': 'verb',
    'adj.': 'adjective',
    'adv.': 'adverb',
    'prep.': 'preposition',
    'conj.': 'conjunction',
    'det.': 'determiner',
    'pron.': 'pronoun',
    'exclam.': 'exclamation',
    'number': 'number',
    'modal v.': 'modal verb',
    'auxiliary v.': 'auxiliary verb',
    'indefinite article': 'indefinite article',
    'definite article': 'definite article',
    'infinitive marker': 'infinitive marker',
}

def normalize_pos(raw_pos: str) -> str:
    raw = raw_pos.strip()
    return POS_NORMALIZATION.get(raw, raw)

print("Helper functions compiled.")

