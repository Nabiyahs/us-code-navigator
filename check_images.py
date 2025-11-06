#!/usr/bin/env python3
"""
Script to verify image references in index.html match actual JPG files
"""

import os
import glob
import re

# Get all JPG files in the repository
actual_files = set()
for pattern in ['*.jpg', '*.JPG']:
    for f in glob.glob(pattern):
        # Store just the basename without extension
        name_without_ext = os.path.splitext(f)[0]
        actual_files.add(name_without_ext)

print("=== Actual JPG Files in Repository ===")
for f in sorted(actual_files):
    print(f"  {f}")
print(f"Total: {len(actual_files)} files\n")

# Define the CodeAttachment data from index.html
attachments = [
    {"id": "D001", "filename": "IBC_3_307.1.1_T1"},
    {"id": "D002", "filename": "IBC_3_307.1.1_T2"},
    {"id": "D003", "filename": "IBC_4_403_F"},
    {"id": "D004", "filename": "IBC_4_[BE]403.5.1_F"},
    {"id": "D005", "filename": "IBC_4_[F]414.2_F"},
    {"id": "D006", "filename": "IBC_4_[F]414.2.2_T1"},
    {"id": "D007", "filename": "IBC_4_[F]414.2.2_F"},
    {"id": "D008", "filename": "IBC_4_[F]414.5.1_T"},
    {"id": "D009", "filename": "IBC_4_[F]415.6.5_T"},
    {"id": "D010", "filename": "IBC_4_[F]415.11.1.1_T"},
    {"id": "D011", "filename": "IBC_5_503.1.2_F1"},
    {"id": "D012", "filename": "IBC_5_503.1.2_F2"},
    {"id": "D013", "filename": "IBC_5_504.3_T"},
    {"id": "D014", "filename": "IBC_5_504.4_T"},
    {"id": "D015", "filename": "IBC_5_506.2_T"},
    {"id": "D016", "filename": "IBC_5_506.3.2_F"},
    {"id": "D017", "filename": "IBC_5_506.3.3_T"},
    {"id": "D018", "filename": "IBC_5_508.4_T"},
    {"id": "D019", "filename": "IBC_5_509.1_T"},
    {"id": "D020", "filename": "IBC_5_510.2_F"},
    {"id": "D021", "filename": "NFPA 13_3_3.3.89_F"},
    {"id": "D022", "filename": "NFPA 13_16_16.12_F"},
    {"id": "D023", "filename": "NFPA 13_17_17.4_F"},
]

print("=== CodeAttachment References in index.html ===")
for att in attachments:
    print(f"  {att['id']}: {att['filename']}")
print(f"Total: {len(attachments)} references\n")

# Function to generate possible filename variants based on the openImageModal function logic
def get_filename_variants(base_filename):
    """Generate filename variants based on the JavaScript logic in openImageModal"""
    variants = []

    # Original filename
    variants.append(base_filename)

    # Variant 1: Replace first dot after ']number' with underscore (e.g., [BE]403.5.1 -> [BE]403_5.1)
    variant1 = re.sub(r'(\]\d+)\.', r'\1_', base_filename)
    if variant1 != base_filename:
        variants.append(variant1)

    # Variant 2: Replace all dots with underscores
    variant2 = base_filename.replace('.', '_')
    if variant2 != base_filename and variant2 != variant1:
        variants.append(variant2)

    return variants

# Check each attachment reference
print("=== Matching Analysis ===")
missing_attachments = []
matched_attachments = []
unmatched_files = set(actual_files)

for att in attachments:
    filename = att['filename']
    variants = get_filename_variants(filename)

    matched = False
    matched_file = None
    for variant in variants:
        if variant in actual_files:
            matched = True
            matched_file = variant
            if variant in unmatched_files:
                unmatched_files.remove(variant)
            break

    if matched:
        print(f"✓ {att['id']}: {filename}")
        print(f"  → Matched: {matched_file}")
        matched_attachments.append(att)
    else:
        print(f"✗ {att['id']}: {filename}")
        print(f"  → Tried variants: {variants}")
        print(f"  → NOT FOUND")
        missing_attachments.append(att)

print("\n=== Files Not Referenced in index.html ===")
if unmatched_files:
    for f in sorted(unmatched_files):
        print(f"  {f}")
else:
    print("  (None)")

print("\n=== SUMMARY ===")
print(f"Total attachments in index.html: {len(attachments)}")
print(f"Matched attachments: {len(matched_attachments)}")
print(f"Missing files: {len(missing_attachments)}")
print(f"Total actual JPG files: {len(actual_files)}")
print(f"Unreferenced JPG files: {len(unmatched_files)}")

if missing_attachments:
    print("\n⚠️  ISSUES FOUND:")
    print(f"   {len(missing_attachments)} attachment(s) reference missing JPG files")
    for att in missing_attachments:
        print(f"   - {att['id']}: {att['filename']}")

if unmatched_files:
    print(f"\n⚠️  {len(unmatched_files)} JPG file(s) are not referenced in index.html:")
    for f in sorted(unmatched_files):
        print(f"   - {f}")

if not missing_attachments and not unmatched_files:
    print("\n✓ All checks passed! All attachments match actual files.")
