#!/usr/bin/env python3
"""Prepare fixed-2020 GHSL urban-centre boundaries from reviewed stable IDs.

The GHSL MTUC polygon layer inspected for this project exposes ID_MTUC, Year,
and ID_UC_G0; it does not expose city-name or country-name fields. The mapping
therefore uses exact stable urban-centre ID plus exact epoch, with city/country
labels retained as project metadata. No fuzzy matching is performed.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd

TARGET_CRS = "EPSG:4326"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, default=Path("data/city_boundary_selection.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/processed/cities_2020.geojson"))
    args = parser.parse_args()

    mapping = pd.read_csv(args.selection, dtype=str).fillna("")
    required = {
        "city_id", "city_name", "country", "ghsl_layer", "ghsl_id_field",
        "ghsl_id_value", "ghsl_epoch_field", "ghsl_epoch_value",
    }
    missing = required.difference(mapping.columns)
    if missing:
        raise ValueError(f"Selection CSV is missing columns: {sorted(missing)}")

    outputs = []
    for row in mapping.to_dict("records"):
        unset = [k for k in required if not row.get(k, "").strip()]
        if unset:
            raise ValueError(
                f"{row.get('city_name', row.get('city_id'))}: complete mapping fields {unset}"
            )

        source = Path(row["ghsl_layer"])
        if not source.exists():
            raise FileNotFoundError(f"GHSL layer path does not exist: {source}")

        gdf = gpd.read_file(source)
        for field in (row["ghsl_id_field"], row["ghsl_epoch_field"]):
            if field not in gdf.columns:
                raise KeyError(f"{source}: field {field!r} not found; available: {list(gdf.columns)}")

        try:
            target_id = int(row["ghsl_id_value"])
            target_epoch = int(row["ghsl_epoch_value"])
        except ValueError as exc:
            raise ValueError(f"Invalid numeric GHSL ID or epoch for {row['city_name']}") from exc

        id_values = pd.to_numeric(gdf[row["ghsl_id_field"]], errors="coerce")
        epoch_values = pd.to_numeric(gdf[row["ghsl_epoch_field"]], errors="coerce")
        selected = gdf[(id_values == target_id) & (epoch_values == target_epoch)].copy()

        if selected.empty:
            raise ValueError(
                f"No exact GHSL match for {row['city_name']}: "
                f"{row['ghsl_id_field']}={target_id}, "
                f"{row['ghsl_epoch_field']}={target_epoch}"
            )
        if len(selected) != 1:
            raise ValueError(
                f"Expected exactly one polygon for {row['city_name']}, found {len(selected)}. "
                "Review the GHSL ID/epoch mapping; do not silently dissolve features."
            )

        # Calculate area in the source projected CRS (World Mollweide, metres)
        # before transforming to geographic coordinates.
        selected["ghsl_area_km2"] = selected.geometry.area / 1_000_000
        if not selected.geometry.is_valid.all():
            raise ValueError(f"Invalid selected geometry for {row['city_name']}; repair/review explicitly.")
        if "ID_MTUC" in selected.columns:
            selected["ghsl_mtuc_id"] = selected["ID_MTUC"].astype(str)
        else:
            selected["ghsl_mtuc_id"] = ""

        selected = selected.to_crs(TARGET_CRS)
        selected["city_id"] = row["city_id"]
        selected["city_name"] = row["city_name"]
        selected["country"] = row["country"]
        selected["ghsl_id"] = selected[row["ghsl_id_field"]].astype(str)
        selected["ghsl_epoch"] = target_epoch
        selected["geometry_source"] = "GHSL_WUP_MTUC_GLOBE_R2025A_V1_1"
        selected["selection_rule"] = "exact stable urban-centre ID + epoch; reviewed mapping"
        selected["selection_notes"] = row.get("selection_notes", "")
        outputs.append(selected[[
            "city_id", "city_name", "country", "ghsl_id",
            "ghsl_epoch", "ghsl_mtuc_id", "ghsl_area_km2",
            "geometry_source", "selection_rule", "selection_notes", "geometry"
        ]])

        print(f"{row['city_name']}: selected {len(selected)} GHSL feature; ID={target_id}, epoch={target_epoch}")
        print(f"  Area: {selected['ghsl_area_km2'].iloc[0]:.2f} km2")

    result = gpd.GeoDataFrame(pd.concat(outputs, ignore_index=True), crs=TARGET_CRS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_file(args.output, driver="GeoJSON")
    print(f"Wrote {len(result)} feature(s) to {args.output}")
    print("Selection IDs are provisional until the output geometries are visually and substantively reviewed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
