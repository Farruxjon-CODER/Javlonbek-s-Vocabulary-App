"""
Canonical Column-Major Vocabulary Generator for Oxford 3000
Reads the Excel sheet '36 Katak + POS' column-by-column (from Column 1 to Column 36, top to bottom),
attaches rich metadata (CEFR, definitions, Uzbek meanings, examples, senses) using stable keys,
assigns sequential orderIndex (1 to 3304), and writes the canonical public/data/vocabulary.json.
"""

import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PUBLIC_DATA_DIR = os.path.join(BASE_DIR, 'public', 'data')

EXCEL_FILE = os.path.join(DATA_DIR, 'Oxford_3000_36_katak_WORD_POS_bitta_katak.xlsx')
if not os.path.exists(EXCEL_FILE):
    # Fallback to Downloads if not yet in data
    EXCEL_FILE = r'C:\Users\Farruxjon\Downloads\Oxford_3000_36_katak_WORD_POS_bitta_katak.xlsx'

OUTPUT_JSON = os.path.join(PUBLIC_DATA_DIR, 'vocabulary.json')
OUTPUT_ENRICHED = os.path.join(PUBLIC_DATA_DIR, 'vocabulary.enriched.json')
BASE_ID_JSON = os.path.join(PUBLIC_DATA_DIR, 'vocabulary.before-enrichment.json')
ENRICHED_JSON = os.path.join(PUBLIC_DATA_DIR, 'vocabulary.enriched.json')

print(f"📖 Reading Excel file: {EXCEL_FILE}")

def num2col(num):
    col = ''
    while num > 0:
        num, rem = divmod(num - 1, 26)
        col = chr(65 + rem) + col
    return col

def load_excel_sheet(excel_path, sheet_name):
    with zipfile.ZipFile(excel_path) as z:
        wb_tree = ET.fromstring(z.read('xl/workbook.xml'))
        rels_tree = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        rel_map = {rel.attrib['Id']: rel.attrib['Target'] for rel in rels_tree}
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        sheet_path = None
        for sheet in wb_tree.findall('.//ns:sheet', ns):
            if sheet.attrib['name'] == sheet_name:
                rId = sheet.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                sheet_path = rel_map[rId].lstrip('/')
                break
        if not sheet_path:
            raise ValueError(f"Sheet '{sheet_name}' not found in {excel_path}")
        if not sheet_path.startswith('xl/'):
            sheet_path = 'xl/' + sheet_path

        ws_tree = ET.fromstring(z.read(sheet_path))
        table = {}
        for r in ws_tree.findall('.//ns:row', ns):
            r_num = int(r.attrib.get('r'))
            for c in r.findall('ns:c', ns):
                col_ref = c.attrib.get('r')
                col_letter = ''.join([ch for ch in col_ref if ch.isalpha()])
                is_el = c.find('ns:is', ns)
                v_el = c.find('ns:v', ns)
                val = ''
                if is_el is not None:
                    val = ''.join([t.text for t in is_el.iter() if t.text])
                elif v_el is not None:
                    val = v_el.text or ''
                table[(col_letter, r_num)] = val.strip()
        return table

# 1. Load stable base IDs
stable_id_map = {} # (normalizedWord, normalizedPOS) -> original ID
if os.path.exists(BASE_ID_JSON):
    with open(BASE_ID_JSON, 'r', encoding='utf-8') as f:
        base_items = json.load(f)
        for item in base_items:
            w = item['word'].strip().lower()
            p = item.get('pos', '').strip().lower()
            stable_id_map[f"{w}|{p}"] = item['id']
            # Also map single POS parts if merged
            for part in p.split(','):
                part = part.strip()
                if part and f"{w}|{part}" not in stable_id_map:
                    stable_id_map[f"{w}|{part}"] = item['id']

# 2. Load enriched definitions & Uzbek translations
enriched_data = []
if os.path.exists(ENRICHED_JSON):
    with open(ENRICHED_JSON, 'r', encoding='utf-8') as f:
        enriched_data = json.load(f)

print(f"Loaded enriched vocabulary entries: {len(enriched_data)}")

# Map existing metadata by stable key (normalizedWord + '|' + normalizedPOS)
# also by normalizedWord
metadata_by_key = {}
metadata_by_word = {}

for item in enriched_data:
    w = item['word'].strip().lower()
    p = item.get('pos', '').strip().lower()
    key = f"{w}|{p}"
    metadata_by_key[key] = item
    metadata_by_word.setdefault(w, []).append(item)
    # Also index by single POS parts
    for part in p.split(','):
        part = part.strip()
        if part and f"{w}|{part}" not in metadata_by_key:
            metadata_by_key[f"{w}|{part}"] = item

# 3. Load Original tartib for authoritative CEFR levels
table_orig = load_excel_sheet(EXCEL_FILE, 'Original tartib')
orig_cefr_map = {} # (word.lower(), pos.lower()) -> list of CEFRs
for r in range(2, max(k[1] for k in table_orig.keys()) + 1):
    w = table_orig.get(('B', r), '').strip().lower()
    cefr = table_orig.get(('C', r), '').strip()
    pos = table_orig.get(('D', r), '').strip().lower()
    if w:
        orig_cefr_map.setdefault((w, pos), []).append(cefr)

# Special entry for 'about' which is A1
orig_cefr_map.setdefault(('about', 'prep., adv.'), ['A1'])

# 3. Read Excel Sheet '36 Katak + POS' Column-by-Column, Top-to-Bottom
table_36 = load_excel_sheet(EXCEL_FILE, '36 Katak + POS')
max_row = max(k[1] for k in table_36.keys())

ordered_vocabulary = []
order_index = 1
# Track which IDs have been assigned so far
assigned_ids = set()
next_new_id = max(stable_id_map.values()) + 1 if stable_id_map else 1

# Special curated dictionary for known words not in old json
SPECIAL_ENTRIES = {
    'about|prep., adv.': {
        'word': 'about',
        'pos': 'prep., adv.',
        'cefr': 'A1',
        'definition': 'on the subject of; or approximately in number or amount',
        'meaningUz': "haqida; to'g'risida; taxminan",
        'example': 'He told me all about his new job.',
        'exampleUz': "U menga yangi ishi haqida hamma narsani aytib berdi."
    }
}

for col_idx in range(1, 37):
    # Column 1 -> A (Word) & B (POS)
    # Column 2 -> C (Word) & D (POS)
    # Column i -> 2*i - 1 & 2*i
    w_col = num2col(2 * col_idx - 1)
    p_col = num2col(2 * col_idx)
    col_header = table_36.get((w_col, 1), f"{col_idx}-so'z")
    
    col_items_count = 0
    for r in range(2, max_row + 1):
        raw_word = table_36.get((w_col, r), '').strip()
        raw_pos = table_36.get((p_col, r), '').strip()
        
        # Skip empty cells
        if not raw_word:
            continue
        
        col_items_count += 1
        norm_w = raw_word.lower()
        norm_p = raw_pos.lower()
        key = f"{norm_w}|{norm_p}"
        
        # Determine expected CEFR level based on row position:
        # Rows 2..26: A1
        # Rows 27..51: A2
        # Rows 52..75: B1
        # Rows 76..93: B2
        if r <= 26:
            block_cefr = 'A1'
        elif r <= 51:
            block_cefr = 'A2'
        elif r <= 75:
            block_cefr = 'B1'
        else:
            block_cefr = 'B2'
            
        # Determine CEFR:
        # Check if orig_cefr_map has this CEFR for this word+pos
        candidate_cefrs = orig_cefr_map.get((norm_w, norm_p), [])
        if block_cefr in candidate_cefrs:
            final_cefr = block_cefr
        elif candidate_cefrs:
            final_cefr = candidate_cefrs[0]
        else:
            final_cefr = block_cefr
            
        # Match metadata:
        meta = None
        if key in SPECIAL_ENTRIES:
            meta = SPECIAL_ENTRIES[key]
        elif key in metadata_by_key:
            meta = metadata_by_key[key]
        elif norm_w in metadata_by_word:
            # Fallback to word match if POS string differs slightly (e.g. 'it' vs 'IT')
            candidates = metadata_by_word[norm_w]
            # If multiple, prefer matching CEFR
            matching_cefr = [c for c in candidates if c.get('cefr') == final_cefr]
            meta = matching_cefr[0] if matching_cefr else candidates[0]
            
        # Determine stable ID:
        item_id = None
        if key in stable_id_map and stable_id_map[key] not in assigned_ids:
            item_id = stable_id_map[key]
            assigned_ids.add(item_id)
        elif key in stable_id_map:
            # Word appears multiple times (e.g. chair A1 and chair B2)
            item_id = next_new_id
            next_new_id += 1
            assigned_ids.add(item_id)
        elif meta and 'id' in meta and meta['id'] not in assigned_ids:
            item_id = meta['id']
            assigned_ids.add(item_id)
        else:
            item_id = next_new_id
            next_new_id += 1
            assigned_ids.add(item_id)

        # Build vocabulary entry
        entry = {
            'id': item_id,
            'orderIndex': order_index,
            'word': raw_word,
            'pos': raw_pos,
            'cefr': final_cefr,
            'definition': meta.get('definition', '') if meta else '',
            'meaningUz': meta.get('meaningUz', '') if meta else '',
            'example': meta.get('example', '') if meta else '',
            'exampleUz': meta.get('exampleUz', '') if meta else '',
            'column': col_idx,
            'row': r
        }
        
        if meta and meta.get('senses'):
            entry['senses'] = meta['senses']
            
        ordered_vocabulary.append(entry)
        order_index += 1

print(f"\n✅ Extracted {len(ordered_vocabulary)} items across 36 columns.")

# Ensure public/data directory exists
os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)

# Write output files
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(ordered_vocabulary, f, ensure_ascii=False, indent=2)

with open(OUTPUT_ENRICHED, 'w', encoding='utf-8') as f:
    json.dump(ordered_vocabulary, f, ensure_ascii=False, indent=2)

print(f"📁 Written canonical data to: {OUTPUT_JSON}")
print(f"📁 Written canonical data to: {OUTPUT_ENRICHED}")

# Print first 30 items for verification
print("\n==================================================")
print("FIRST 30 GENERATED VOCABULARY ITEMS")
print("==================================================")
for i, item in enumerate(ordered_vocabulary[:30], 1):
    print(f"{i:2d}. {item['word']} ({item['pos']}) [CEFR: {item['cefr']}, Col: {item['column']}, Row: {item['row']}, ID: {item['id']}, orderIndex: {item['orderIndex']}]")
    print(f"    Uzbek: {item.get('meaningUz')}")
    print(f"    Def:   {item.get('definition')[:60]}...")

print("\n==================================================")
print("ITEMS 91 TO 95 (TRANSITION FROM COL 1 TO COL 2)")
print("==================================================")
for i, item in enumerate(ordered_vocabulary[90:95], 91):
    print(f"{i:2d}. {item['word']} ({item['pos']}) [CEFR: {item['cefr']}, Col: {item['column']}, Row: {item['row']}, orderIndex: {item['orderIndex']}]")
