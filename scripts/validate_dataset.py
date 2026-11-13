#!/usr/bin/env python3
"""Validate coolant product, observation, and source-register CSV files.

This is a structural and plausibility check, not verification of source accuracy.
Uses only the Python standard library.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "coolant_observations.csv"
PRODUCTS = ROOT / "data" / "products.csv"
SOURCES = ROOT / "data" / "source_register.csv"

REQUIRED_OBSERVATIONS = {
    "observation_id", "product_id", "manufacturer", "product_name",
    "chemical_family", "temperature_C", "pressure_kPa", "cp_kJ_kgK",
    "thermal_conductivity_W_mK", "density_kg_m3",
    "dynamic_viscosity_mPa_s", "kinematic_viscosity_mm2_s",
    "evidence_type", "source_id",
}
REQUIRED_PRODUCTS = {
    "product_id", "manufacturer", "product_name", "fluid_chemistry",
    "phase_regime", "application", "source_id", "evidence_status",
}
ALLOWED_EVIDENCE = {
    "independent_measurement", "manufacturer_guaranteed",
    "manufacturer_typical", "manufacturer_calculated",
    "secondary_compilation", "interpolated", "model_estimated",
    "simulation_output",
}
POSITIVE_FIELDS = (
    "cp_kJ_kgK", "thermal_conductivity_W_mK", "density_kg_m3",
    "dynamic_viscosity_mPa_s", "kinematic_viscosity_mm2_s",
)
NUMERIC_FIELDS = POSITIVE_FIELDS + (
    "temperature_C", "pressure_kPa", "vapor_pressure_kPa",
    "concentration_value",
)


def read_csv(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return rows, set(reader.fieldnames or [])


def main() -> int:
    errors: list[str] = []
    observations, obs_columns = read_csv(OBS)
    products, product_columns = read_csv(PRODUCTS)
    sources, source_columns = read_csv(SOURCES)

    missing = REQUIRED_OBSERVATIONS - obs_columns
    if missing:
        errors.append(f"Observation file missing columns: {sorted(missing)}")
    missing = REQUIRED_PRODUCTS - product_columns
    if missing:
        errors.append(f"Product file missing columns: {sorted(missing)}")
    if not {"source_id", "url", "evidence_role"} <= source_columns:
        errors.append("Source register missing required provenance columns.")

    source_ids = {row.get("source_id", "") for row in sources}
    product_ids = {row.get("product_id", "").strip() for row in products}
    if len(product_ids) != len(products) or "" in product_ids:
        errors.append("Product catalogue contains an empty or duplicate product_id.")

    for line, row in enumerate(products, start=2):
        if row.get("source_id", "") not in source_ids:
            errors.append(f"Product row {line}: unknown source_id {row.get('source_id')}")
        if row.get("phase_regime", "") not in {"single_phase", "two_phase", "mixed_or_unknown"}:
            errors.append(f"Product row {line}: invalid phase_regime")
        for field in ("product_page_url", "tds_url"):
            value = row.get(field, "").strip()
            if value and not value.startswith(("https://", "http://")):
                errors.append(f"Product row {line}: {field} must be an http(s) URL")

    seen_ids: set[str] = set()
    for line, row in enumerate(observations, start=2):
        oid = row.get("observation_id", "").strip()
        if not oid:
            errors.append(f"Observation row {line}: empty observation_id")
        elif oid in seen_ids:
            errors.append(f"Observation row {line}: duplicate observation_id {oid}")
        seen_ids.add(oid)

        if row.get("source_id", "") not in source_ids:
            errors.append(f"Observation row {line}: unknown source_id {row.get('source_id')}")
        if row.get("product_id", "") not in product_ids:
            errors.append(f"Observation row {line}: unknown product_id {row.get('product_id')}")

        evidence = row.get("evidence_type", "")
        if evidence not in ALLOWED_EVIDENCE:
            errors.append(f"Observation row {line}: invalid evidence_type {evidence!r}")

        for field in NUMERIC_FIELDS:
            raw = row.get(field, "").strip()
            if raw:
                try:
                    value = float(raw)
                    if not math.isfinite(value):
                        raise ValueError("not finite")
                except ValueError:
                    errors.append(f"Observation row {line}: {field} is not a finite number: {raw!r}")

        for field in POSITIVE_FIELDS:
            raw = row.get(field, "").strip()
            if raw:
                try:
                    if float(raw) <= 0:
                        errors.append(f"Observation row {line}: {field} must be positive")
                except ValueError:
                    pass

        basis = row.get("concentration_basis", "").strip()
        if row.get("concentration_value", "").strip() and basis not in {
            "mass", "volume", "mole", "not_applicable"
        }:
            errors.append(f"Observation row {line}: concentration basis missing or unrecognised")

        if not row.get("notes", "").strip():
            errors.append(f"Observation row {line}: add provenance or qualification notes")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"VALIDATION PASSED: {len(products)} products; "
        f"{len(observations)} observations; {len(sources)} sources."
    )
    print("Reminder: structural validation does not independently verify source values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
