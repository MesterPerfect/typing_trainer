import os
import sys
import re
import struct
from pathlib import Path

def parse_po(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    pattern = re.compile(
        r'msgid\s+((?:\"(?:[^\"\\]|\\.)*\"\s*)+)\s*msgstr\s+((?:\"(?:[^\"\\]|\\.)*\"\s*)+)',
        re.MULTILINE
    )

    def clean_str(s):
        lines = re.findall(r'\"((?:[^\"\\]|\\.)*)\"', s)
        joined = ''.join(lines)
        # Unescape standard escape sequences safely
        return (joined
                .replace(r'\n', '\n')
                .replace(r'\t', '\t')
                .replace(r'\"', '"')
                .replace(r'\\', '\\'))

    for match in pattern.finditer(content):
        raw_id, raw_str = match.groups()
        msg_id = clean_str(raw_id)
        msg_str = clean_str(raw_str)
        # We must include the empty key "" as it contains metadata (Content-Type: charset=UTF-8)
        entries[msg_id] = msg_str

    return entries

def generate_mo(entries, mo_path):
    keys = sorted(entries.keys())
    offsets = []
    ids = b''
    strs = b''

    for k in keys:
        v = entries[k]
        k_bytes = k.encode('utf-8') + b'\x00'
        v_bytes = v.encode('utf-8') + b'\x00'
        offsets.append((len(ids), len(k_bytes) - 1, len(strs), len(v_bytes) - 1))
        ids += k_bytes
        strs += v_bytes

    keystart = 7 * 4 + len(keys) * 8 * 2
    valuestart = keystart + len(ids)

    koffsets = []
    voffsets = []
    for (o1, l1, o2, l2) in offsets:
        koffsets.append((l1, o1 + keystart))
        voffsets.append((l2, o2 + valuestart))

    output = struct.pack('Iiiiiii',
        0x950412de, # Magic
        0,          # Version
        len(keys),  # Number of strings
        7 * 4,      # Offset of table with originals
        7 * 4 + len(keys) * 8, # Offset of table with translation
        0, 0        # Size and offset of hash table
    )

    for l, o in koffsets:
        output += struct.pack('ii', l, o)
    for l, o in voffsets:
        output += struct.pack('ii', l, o)

    output += ids
    output += strs

    mo_path = Path(mo_path)
    mo_path.parent.mkdir(parents=True, exist_ok=True)
    with open(mo_path, 'wb') as f:
        f.write(output)
    print(f"MO compiled successfully with {len(keys)} entries -> {mo_path}")

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parent.parent
    po_file = base_dir / 'locales/ar/LC_MESSAGES/messages.po'
    mo_file = base_dir / 'locales/ar/LC_MESSAGES/messages.mo'
    entries = parse_po(po_file)
    generate_mo(entries, mo_file)
