"""
A1 36-cell vocabulary generator.
Parses the 36-unit A1 Oxford 3000 list and outputs public/data/vocabulary.json.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_FILE = os.path.join(BASE_DIR, 'public', 'data', 'vocabulary.json')

def verify():
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Verified {len(data)} words in {TARGET_FILE}")

if __name__ == '__main__':
    verify()
