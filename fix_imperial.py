"""Verify Imperial website: check for duplicates, missing functions, and HTML integrity."""
import re

BASE = r"c:\Users\HP\.gemini\antigravity\playground\spatial-cosmos\imperial"

# 1. Check HTML for duplicates
with open(f"{BASE}\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Count occurrences of each product
products = re.findall(r'alt="([^"]+)"', html)
from collections import Counter
counts = Counter(products)
dupes = {k: v for k, v in counts.items() if v > 1}
print(f"=== Product Duplicates ===")
if dupes:
    print(f"FOUND {len(dupes)} duplicated products:")
    for name, count in sorted(dupes.items()):
        print(f"  {name}: {count}x")
else:
    print("PASS: No duplicate products found!")

# 2. Check JS functions
with open(f"{BASE}\\script.js", "r", encoding="utf-8") as f:
    js = f.read()

# Find all function calls in HTML onclick handlers
onclick_funcs = set(re.findall(r'onclick="(\w+)\(', html))
# Find all function definitions in JS
js_funcs = set(re.findall(r'function\s+(\w+)\s*\(', js))

print(f"\n=== JS Function Coverage ===")
print(f"Functions called in HTML: {len(onclick_funcs)}")
print(f"Functions defined in JS: {len(js_funcs)}")

missing = onclick_funcs - js_funcs
if missing:
    print(f"MISSING functions ({len(missing)}):")
    for f in sorted(missing):
        print(f"  ❌ {f}")
else:
    print("PASS: All functions called in HTML are defined in JS!")

# 3. Check HTML structure 
open_divs = html.count('<div')
close_divs = html.count('</div')
print(f"\n=== HTML Structure ===")
print(f"Opening <div>: {open_divs}")
print(f"Closing </div>: {close_divs}")
print(f"Balance: {'PASS' if open_divs == close_divs else f'MISMATCH (diff: {open_divs - close_divs})'}")

open_sections = html.count('<section')
close_sections = html.count('</section')
print(f"Opening <section>: {open_sections}")
print(f"Closing </section>: {close_sections}")
print(f"Balance: {'PASS' if open_sections == close_sections else f'MISMATCH (diff: {open_sections - close_sections})'}")

# 4. Check total lines
lines = html.split('\n')
print(f"\n=== File Stats ===")
print(f"HTML: {len(lines)} lines")
js_lines = js.split('\n')
print(f"JS: {len(js_lines)} lines")

# 5. Essential elements
essential = ['bookingModal', 'cartOverlay', 'cartSidebar', 'pcGrid', 'catEmpty', 'catTitle', 'catDesc']
print(f"\n=== Essential Elements ===")
for elem in essential:
    found = elem in html
    print(f"  {'✓' if found else '❌'} {elem}: {'found' if found else 'MISSING!'}")

print("\n=== Category Counts ===")
cats = re.findall(r'data-cat="(\w+)"', html)
cat_counts = Counter(cats)
for cat, count in sorted(cat_counts.items()):
    print(f"  {cat}: {count} products")
print(f"  Total: {len(cats)} products")
