#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Excel (all sheets) -> JSON exporter

Goals
- Export EVERY sheet and EVERY column by default (no allow-list filtering).
- Preserve line breaks (\n) inside cells.
- Strip only leading/trailing spaces/tabs from strings.
- Convert empty strings -> null, NaN -> null.
- Drop only completely empty rows (all cells empty).
- Optional: add derived fields for CodeContent:
  - IndexTags: split Index by ';'
  - SubindexPaths: split SubIndex by ';' then '_' into hierarchical arrays
- Safe JSON serialization for numpy / datetime types.

Usage:
  python excel_to_json_all.py --input path/to/file.xlsx --outdir json_out
  python excel_to_json_all.py --input file.xlsx --outdir json_out --no-indent
  python excel_to_json_all.py --input file.xlsx --outdir json_out --only-sheets CodeContent CodeChapter
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd


# -----------------------------
# JSON helpers
# -----------------------------
def json_default(o: Any):
    """Make common non-JSON-native types serializable."""
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if math.isnan(float(o)) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (Decimal,)):
        return float(o)
    # pandas Timestamp etc.
    if hasattr(o, "isoformat"):
        try:
            return o.isoformat()
        except Exception:
            pass
    return str(o)


def sanitize_filename(name: str) -> str:
    """Safe file name from sheet name."""
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", str(name)).strip()
    return (safe[:150] or "sheet").strip("_") or "sheet"


# -----------------------------
# Derived fields for CodeContent
# -----------------------------
def parse_index_tags(value: Any) -> List[str]:
    """Index: 'A;B;C' -> ['A','B','C']"""
    if not isinstance(value, str):
        return []
    parts = [p.strip() for p in value.split(";")]
    return [p for p in parts if p]


def parse_subindex_paths(value: Any) -> List[List[str]]:
    """
    SubIndex: 'A_B;C_D_E' -> [['A','B'], ['C','D','E']]
    """
    if not isinstance(value, str):
        return []
    paths: List[List[str]] = []
    for token in value.split(";"):
        token = token.strip()
        if not token:
            continue
        segments = [seg.strip() for seg in token.split("_") if seg.strip()]
        if segments:
            paths.append(segments)
    return paths


# -----------------------------
# Cleaning / normalization
# -----------------------------
def normalize_columns(cols: Iterable[Any]) -> List[str]:
    """
    - Convert to strings
    - Strip whitespace
    - Replace empty/Unnamed columns with generated names
    - Deduplicate duplicates by suffixing _2, _3, ...
    """
    raw = []
    for c in cols:
        s = "" if c is None else str(c)
        s = s.strip()
        if not s or s.lower().startswith("unnamed:"):
            s = "Column"
        raw.append(s)

    # Deduplicate
    seen: Dict[str, int] = {}
    out: List[str] = []
    for s in raw:
        if s not in seen:
            seen[s] = 1
            out.append(s)
        else:
            seen[s] += 1
            out.append(f"{s}_{seen[s]}")
    return out


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Keep all columns (no filtering)
    - Strip only spaces/tabs at ends of strings
    - Empty string -> NaN -> None
    - Drop only completely empty rows
    """
    # Normalize headers
    df = df.copy()
    df.columns = normalize_columns(df.columns)

    # Strip strings, preserve newlines
    for col in df.columns:
        if df[col].dtype == "object" or pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].map(lambda x: x.strip(" \t") if isinstance(x, str) else x)

    # Treat empty strings as missing
    df = df.replace("", np.nan)

    # Drop only fully empty rows
    df = df.dropna(how="all")

    # NaN -> None (JSON null)
    df = df.where(pd.notna(df), None)
    return df


# -----------------------------
# Main export
# -----------------------------
@dataclass
class ExportOptions:
    indent: Optional[int] = 2
    only_sheets: Optional[List[str]] = None
    add_codecontent_derivatives: bool = True


def excel_to_json_tables(xlsx_path: Path, outdir: Path, options: ExportOptions) -> None:
    if not xlsx_path.exists():
        raise FileNotFoundError(f"엑셀 파일 없음: {xlsx_path}")

    outdir.mkdir(parents=True, exist_ok=True)

    # Load all sheets
    sheets = pd.read_excel(
        xlsx_path,
        sheet_name=None,      # all sheets
        engine="openpyxl",
        dtype=object,
        header=0,
    )

    sheet_names = list(sheets.keys())

    if options.only_sheets:
        wanted = set(options.only_sheets)
        sheet_names = [s for s in sheet_names if s in wanted]

    if not sheet_names:
        raise ValueError("내보낼 시트가 없습니다. --only-sheets 옵션을 확인하세요.")

    for sheet_name in sheet_names:
        df = sheets[sheet_name]
        df = clean_dataframe(df)

        # Optional: derived fields for CodeContent
        if options.add_codecontent_derivatives and sheet_name == "CodeContent":
            # Only add if source columns exist; never crash if missing
            if "Index" in df.columns:
                df["IndexTags"] = df["Index"].map(parse_index_tags)
            if "SubIndex" in df.columns:
                df["SubindexPaths"] = df["SubIndex"].map(parse_subindex_paths)

        records = df.to_dict(orient="records")

        json_filename = sanitize_filename(sheet_name) + ".json"
        out_path = outdir / json_filename

        with out_path.open("w", encoding="utf-8") as f:
            json.dump(
                records,
                f,
                ensure_ascii=False,
                indent=options.indent,
                default=json_default,
            )

        print(f"[OK] {sheet_name} → {out_path} (rows: {len(records)}, cols: {len(df.columns)})")


def main():
    parser = argparse.ArgumentParser(description="Excel (all sheets/all columns) → JSON 변환")
    parser.add_argument("--input", required=True, help="입력 엑셀 파일 경로(.xlsx)")
    parser.add_argument("--outdir", default="json_out", help="출력 폴더")
    parser.add_argument("--no-indent", action="store_true", help="JSON pretty indent 끄기")
    parser.add_argument(
        "--only-sheets",
        nargs="*",
        default=None,
        help="특정 시트만 내보내기 (예: --only-sheets CodeContent CodeChapter)",
    )
    parser.add_argument(
        "--no-codecontent-derivatives",
        action="store_true",
        help="CodeContent의 IndexTags/SubindexPaths 파생 컬럼 생성을 끄기",
    )
    args = parser.parse_args()

    options = ExportOptions(
        indent=None if args.no_indent else 2,
        only_sheets=args.only_sheets,
        add_codecontent_derivatives=not args.no_codecontent_derivatives,
    )

    excel_to_json_tables(
        xlsx_path=Path(args.input),
        outdir=Path(args.outdir),
        options=options,
    )


if __name__ == "__main__":
    main()
