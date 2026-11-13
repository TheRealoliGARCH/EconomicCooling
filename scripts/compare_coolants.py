#!/usr/bin/env python3
"""Create a no-extrapolation property comparison at a chosen temperature.

Uses only the Python standard library. Linear interpolation is a transparent
screening operation, not a constitutive property model or a substitute for
measured values at the target temperature.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "data" / "coolant_observations.csv"
PRODUCTS = ROOT / "data" / "products.csv"
OUTPUT = ROOT / "reports" / "comparison_at_20C.csv"
TARGET_C = 20.0
PROPERTIES = (
    "cp_kJ_kgK",
    "thermal_conductivity_W_mK",
    "density_kg_m3",
    "dynamic_viscosity_mPa_s",
)


def interpolate(rows: list[dict[str, str]], field: str, target: float) -> tuple[float | None, str]:
    valid = []
    for row in rows:
        raw_t, raw_y = row.get("temperature_C", "").strip(), row.get(field, "").strip()
        if raw_t and raw_y:
            valid.append((float(raw_t), float(raw_y)))
    valid.sort()
    for temperature, value in valid:
        if temperature == target:
            return value, "reported_at_target"
    lower = [(t, y) for t, y in valid if t < target]
    upper = [(t, y) for t, y in valid if t > target]
    if not lower or not upper:
        return None, "not_available_without_extrapolation"
    t0, y0 = lower[-1]
    t1, y1 = upper[0]
    value = y0 + (target - t0) * (y1 - y0) / (t1 - t0)
    return value, f"linear_interpolation_{t0:g}_to_{t1:g}_C"


def main() -> int:
    with PRODUCTS.open(newline="", encoding="utf-8") as handle:
        products = list(csv.DictReader(handle))
    with OBSERVATIONS.open(newline="", encoding="utf-8") as handle:
        observations = list(csv.DictReader(handle))

    output_rows = []
    for product in products:
        product_id = product["product_id"]
        rows = [r for r in observations if r["product_id"] == product_id]
        if not rows:
            continue
        result = {
            "target_temperature_C": f"{TARGET_C:g}",
            "product_id": product_id,
            "manufacturer": product["manufacturer"],
            "product_name": product["product_name"],
            "fluid_chemistry": product["fluid_chemistry"],
            "concentration_value": product.get("concentration_value", ""),
            "concentration_unit": product.get("concentration_unit", ""),
            "concentration_basis": product.get("concentration_basis", ""),
        }
        methods = []
        for field in PROPERTIES:
            value, method = interpolate(rows, field, TARGET_C)
            result[field] = "" if value is None else f"{value:.8g}"
            methods.append(f"{field}:{method}")
        result["calculation_methods"] = "; ".join(methods)
        result["evidence_class"] = "manufacturer-reported or linearly interpolated; inspect source-level provenance"
        output_rows.append(result)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if not output_rows:
        print("No products have property observations.")
        return 0
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Wrote {len(output_rows)} product rows to {OUTPUT.relative_to(ROOT)}")
    print("No extrapolation was performed; missing target values remain blank.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
