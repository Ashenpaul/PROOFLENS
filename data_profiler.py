import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

class DataProfiler:
    """
    Profiles messy multi-table data for:
    - Duplicate rows and primary key collisions
    - Unit / Currency inconsistencies (e.g., USD vs EUR without explicit context)
    - Ambiguous date notations (e.g., DD/MM/YYYY vs MM/DD/YYYY)
    - Cross-table contradictions (e.g., regional aggregated revenue vs itemized tx sums)
    - Missing values and dirty strings
    """

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.datasets: Dict[str, pd.DataFrame] = {}
        self.raw_files: List[Path] = []
        self._load_datasets()

    def _load_datasets(self):
        if not self.data_dir.exists():
            return

        for file_path in self.data_dir.glob("*"):
            if file_path.suffix.lower() == ".csv":
                try:
                    df = pd.read_csv(file_path)
                    self.datasets[file_path.name] = df
                    self.raw_files.append(file_path)
                except Exception as e:
                    print(f"Warning: Failed to load {file_path}: {e}")
            elif file_path.suffix.lower() == ".json":
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, list):
                        df = pd.DataFrame(data)
                        self.datasets[file_path.name] = df
                        self.raw_files.append(file_path)
                except Exception as e:
                    print(f"Warning: Failed to load {file_path}: {e}")

    def profile_all(self) -> Dict[str, Any]:
        """Runs comprehensive profiling across all loaded datasets."""
        profile = {
            "tables": {},
            "cross_table_contradictions": [],
            "date_ambiguities": [],
            "currency_inconsistencies": [],
            "duplicate_warnings": [],
            "missing_data_warnings": []
        }

        for table_name, df in self.datasets.items():
            # Clean NaN to None for JSON serialization
            clean_sample_df = df.head(3).copy()
            clean_sample_df = clean_sample_df.where(pd.notnull(clean_sample_df), None)
            table_info = {
                "row_count": len(df),
                "columns": list(df.columns),
                "null_counts": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
                "duplicate_rows": int(df.duplicated().sum()),
                "sample": clean_sample_df.to_dict(orient="records")
            }
            profile["tables"][table_name] = table_info

            # 1. Duplicate key check
            for id_col in ["tx_id", "transaction_id", "order_id", "id"]:
                if id_col in df.columns:
                    dupes = df[df.duplicated(subset=[id_col], keep=False)]
                    if not dupes.empty:
                        profile["duplicate_warnings"].append({
                            "table": table_name,
                            "column": id_col,
                            "duplicate_count": len(dupes),
                            "sample_keys": dupes[id_col].unique().tolist()[:5]
                        })

            # 2. Date ambiguity detection
            for col in df.columns:
                if "date" in col.lower() or "time" in col.lower():
                    ambiguous = self._detect_ambiguous_dates(df[col])
                    if ambiguous:
                        profile["date_ambiguities"].append({
                            "table": table_name,
                            "column": col,
                            "ambiguous_samples": ambiguous
                        })

            # 3. Currency / Unit detection
            for col in df.columns:
                if "currency" in col.lower():
                    unique_curr = df[col].dropna().unique().tolist()
                    if len(unique_curr) > 1:
                        profile["currency_inconsistencies"].append({
                            "table": table_name,
                            "column": col,
                            "currencies_found": unique_curr
                        })

        # 4. Cross-table contradiction detection
        profile["cross_table_contradictions"] = self._detect_cross_table_contradictions()

        return profile

    def _detect_ambiguous_dates(self, series: pd.Series) -> List[str]:
        """
        Identifies dates with slash notation like '06/07/2023' where both parts <= 12,
        making DD/MM/YYYY vs MM/DD/YYYY ambiguous.
        """
        ambiguous = []
        for val in series.dropna().astype(str):
            # Check pattern like XX/YY/ZZZZ or XX-YY-ZZZZ
            match = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})$", val.strip())
            if match:
                part1, part2 = int(match.group(1)), int(match.group(2))
                if part1 <= 12 and part2 <= 12 and part1 != part2:
                    ambiguous.append(val.strip())
        return list(set(ambiguous))

    def _detect_cross_table_contradictions(self) -> List[Dict[str, Any]]:
        """
        Checks for discrepancies between itemized sales and regional reported summaries.
        """
        contradictions = []
        if "sales_transactions.csv" in self.datasets and "regional_summaries.csv" in self.datasets:
            df_tx = self.datasets["sales_transactions.csv"].copy()
            df_reg = self.datasets["regional_summaries.csv"].copy()

            # Clean duplicates in tx for fair baseline
            if "tx_id" in df_tx.columns:
                df_tx = df_tx.drop_duplicates(subset=["tx_id"])

            if "region" in df_tx.columns and "region" in df_reg.columns and "reported_revenue_usd" in df_reg.columns:
                # Estimate itemized revenue in tx (approximate for detection)
                if "unit_price" in df_tx.columns and "quantity" in df_tx.columns:
                    df_tx["line_total"] = df_tx["unit_price"] * df_tx["quantity"]
                    tx_by_region = df_tx.groupby("region")["line_total"].sum().to_dict()

                    for _, row in df_reg.iterrows():
                        reg_name = row["region"]
                        reported_val = float(row["reported_revenue_usd"])
                        tx_val = tx_by_region.get(reg_name, 0.0)

                        # If relative difference > 50% and reported > 1000
                        if reported_val > 0 and tx_val > 0:
                            ratio = max(reported_val, tx_val) / min(reported_val, tx_val)
                            if ratio > 2.0:
                                contradictions.append({
                                    "conflict_type": "Regional Revenue Mismatch",
                                    "region": reg_name,
                                    "summary_table": "regional_summaries.csv",
                                    "summary_value": reported_val,
                                    "summary_notes": str(row.get("notes", "")),
                                    "line_items_table": "sales_transactions.csv",
                                    "line_items_sum": tx_val,
                                    "ratio_discrepancy": round(ratio, 2),
                                    "reason": (
                                        f"Conflicting sources: regional_summaries reports ${reported_val:,.2f} "
                                        f"for {reg_name}, whereas sales_transactions itemizes ${tx_val:,.2f} "
                                        f"({ratio:.1f}x mismatch)."
                                    )
                                })
        return contradictions
