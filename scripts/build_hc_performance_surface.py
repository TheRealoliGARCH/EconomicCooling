#!/usr/bin/env python3
"""Generate a temperature x flow x grade coolant performance surface.

Reproducibility contract: deterministic inputs, explicit assumptions, no extrapolation.

Uses exact manufacturer observations at temperatures common to all five
Dynalene HC grades. No interpolation or extrapolation is performed.
Standard library only; output rows are model estimates, not measurements.
"""
from __future__ import annotations
import csv, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "coolant_observations.csv"
OUTPUT = ROOT / "reports" / "hc_performance_surface.csv"
GRADES = ("HC-10", "HC-20", "HC-30", "HC-40", "HC-50")
MASS_FLOWS_KG_S = (0.2, 0.3, 0.4)
DIAMETER_M = 0.020
LENGTH_M = 5.0
ROUGHNESS_M = 1.5e-6
PUMP_EFFICIENCY = 0.65
RE_MIN, RE_MAX = 3000.0, 5.0e6
PR_MIN, PR_MAX = 0.5, 2000.0


def churchill_darcy(Re: float, relative_roughness: float) -> float:
    A = (2.457 * math.log(
        1.0 / ((7.0 / Re) ** 0.9 + 0.27 * relative_roughness)
    )) ** 16
    B = (37530.0 / Re) ** 16
    return 8.0 * ((8.0 / Re) ** 12 + 1.0 / (A + B) ** 1.5) ** (1.0 / 12.0)


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as f:
        observations = list(csv.DictReader(f))
    properties = {}
    for grade in GRADES:
        properties[grade] = {}
        for row in observations:
            if row["product_id"] != f"DYNALENE-{grade}" or not row["cp_kJ_kgK"].strip():
                continue
            T = float(row["temperature_C"])
            if T in properties[grade]:
                raise ValueError(f"Duplicate complete property row: {grade} at {T} C")
            properties[grade][T] = {
                "cp": float(row["cp_kJ_kgK"]),
                "k": float(row["thermal_conductivity_W_mK"]),
                "rho": float(row["density_kg_m3"]),
                "mu": float(row["dynamic_viscosity_mPa_s"]) * 1e-3,
                "source": row["source_id"],
            }
    common_T = sorted(set.intersection(*(set(properties[g]) for g in GRADES)))
    if not common_T:
        raise ValueError("No common exact property temperatures across all grades")
    records = []
    area = math.pi * DIAMETER_M ** 2 / 4.0
    for T in common_T:
        for grade in GRADES:
            p = properties[grade][T]
            for mdot in MASS_FLOWS_KG_S:
                velocity = mdot / (p["rho"] * area)
                Re = p["rho"] * velocity * DIAMETER_M / p["mu"]
                Pr = p["mu"] * p["cp"] * 1000.0 / p["k"]
                fD = churchill_darcy(Re, ROUGHNESS_M / DIAMETER_M)
                dp = fD * LENGTH_M / DIAMETER_M * p["rho"] * velocity**2 / 2.0
                qv = mdot / p["rho"]
                hydraulic = dp * qv
                electric = hydraulic / PUMP_EFFICIENCY
                Nu, h = "", ""
                status = "outside_Gnielinski_envelope"
                if RE_MIN <= Re <= RE_MAX and PR_MIN <= Pr <= PR_MAX:
                    Nu = (
                        (fD / 8.0) * (Re - 1000.0) * Pr
                        / (1.0 + 12.7 * math.sqrt(fD / 8.0)
                           * (Pr ** (2.0 / 3.0) - 1.0))
                    )
                    h = Nu * p["k"] / DIAMETER_M
                    status = "Gnielinski_within_nominal_envelope"
                records.append({
                    "grade": grade, "temperature_C": T,
                    "mass_flow_kg_s": mdot, "pipe_diameter_m": DIAMETER_M,
                    "pipe_length_m": LENGTH_M, "roughness_m": ROUGHNESS_M,
                    "property_source_id": p["source"], "cp_kJ_kgK": p["cp"],
                    "k_W_mK": p["k"], "rho_kg_m3": p["rho"],
                    "mu_Pa_s": p["mu"], "velocity_m_s": velocity,
                    "Reynolds": Re, "Prandtl": Pr,
                    "Darcy_friction_factor": fD, "pressure_drop_Pa": dp,
                    "hydraulic_power_W": hydraulic,
                    "pump_electric_power_W": electric,
                    "heat_capacity_rate_W_K": mdot * p["cp"] * 1000.0,
                    "Nusselt": Nu, "internal_h_W_m2K": h,
                    "correlation_status": status, "evidence_type": "model_estimated",
                })
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Common exact temperatures: {common_T}")
    print(f"Wrote {len(records)} model rows to {OUTPUT.relative_to(ROOT)}")
    print("No property interpolation/extrapolation; correlation validity is flagged per row.")


if __name__ == "__main__":
    main()
