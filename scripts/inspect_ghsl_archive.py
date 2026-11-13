#!/usr/bin/env python3
"""Download (optionally), extract, and inventory the GHSL MTUC vector archive.

This script does not select city polygons automatically. It records layer names,
fields, CRS, feature counts, and a small attribute sample so that city matching
can be reviewed before any geometry is designated as a study boundary.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

import geopandas as gpd
import pandas as pd
import pyogrio

URL = (
    "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/"
    "GHS_WUP_MTUC_GLOBE_R2025A/V1-1/"
    "GHS_WUP_MTUC_GLOBE_R2025A_V1_1_vector.zip"
)


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "EconomicCooling-research/1.0"})
    with urlopen(request, timeout=90) as response, destination.open("wb") as out:
        total = int(response.headers.get("Content-Length", "0"))
        received = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            received += len(chunk)
            if total:
                print(f"\\rDownloaded {received / total:.1%}", end="", flush=True)
    print(f"\\nSaved archive: {destination} ({destination.stat().st_size:,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("data/raw/ghsl/mtuc_v1_1.zip"))
    parser.add_argument("--download", action="store_true", help="Download official V1_1 archive first")
    parser.add_argument("--extract-dir", type=Path, default=Path("data/raw/ghsl/extracted"))
    parser.add_argument("--inventory", type=Path, default=Path("reports/ghsl_layer_inventory.json"))
    args = parser.parse_args()

    if args.download or not args.archive.exists():
        print(f"Downloading official GHSL archive from {URL}")
        download(URL, args.archive)

    args.extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.archive) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Archive integrity check failed at: {bad}")
        archive.extractall(args.extract_dir)

    vector_files = [
        p for p in args.extract_dir.rglob("*")
        if p.suffix.lower() in {".shp", ".gpkg", ".geojson", ".fgb"}
    ]
    if not vector_files:
        raise FileNotFoundError(f"No supported vector datasets found under {args.extract_dir}")

    inventory = []
    for path in vector_files:
        try:
            layers = pyogrio.list_layers(path)
            for layer_row in layers:
                layer_name = str(layer_row[0]) if len(layer_row) else None
                info = pyogrio.read_info(path, layer=layer_name)
                sample = gpd.read_file(path, layer=layer_name, rows=8)
                record = {
                    "path": str(path),
                    "layer": layer_name,
                    "feature_count": int(info.get("features", -1)),
                    "geometry_type": str(info.get("geometry_type")),
                    "crs": str(info.get("crs")),
                    "fields": list(info.get("fields", [])),
                    "sample_attributes": sample.drop(columns="geometry", errors="ignore").to_dict("records"),
                }
                inventory.append(record)
                print(f"\\n{path} | layer={layer_name} | features={record['feature_count']}")
                print(f"CRS: {record['crs']}")
                print(f"Fields: {', '.join(record['fields'])}")
                print(pd.DataFrame(record["sample_attributes"]).to_string(index=False))
        except Exception as exc:
            print(f"WARNING: Could not inspect {path}: {exc}", file=sys.stderr)

    args.inventory.parent.mkdir(parents=True, exist_ok=True)
    args.inventory.write_text(json.dumps(inventory, indent=2, default=str), encoding="utf-8")
    print(f"\\nInventory written to {args.inventory}")
    print("Next: inspect city/country/name/year fields and complete data/city_boundary_selection.csv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
