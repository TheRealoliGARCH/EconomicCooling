#!/usr/bin/env python3
"""Screen Dynalene HC grades with a transparent single-phase pipe-flow model.

Standard-library only. Reads exact 20 C manufacturer observations from the
master CSV. Outputs scenario-level estimates; this is not an experimental
validation or a system-level coolant qualification.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBS = ROOT / "data" / "coolant_observations.csv"
OUT = ROOT / "reports" / "hc_grade_hydraulic_screening.csv"

# Illustrative smooth-pipe test article; change only with an explicit rationale.
DIAMETER_M = 0.010
LENGTH_M = 10.0
ROUGHNESS_M = 1.5e-6
PUMP_EFFICIENCY = 0.65
EQUAL_MASS_FLOW_KG_S = 0.400
EQUAL_VOLUME_FLOW_M3_S = 0.000350
EQUAL_ELECTRIC_POWER_W = 50.0
PROPERTY_TEMPERATURE_C = 20.0
GRADES = ("HC-10", "HC-20", "HC-30", "HC-40", "HC-50")


def read_properties() -> list[dict[str, float | str]]:
    with OBS.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    fluids = []
    for grade in GRADES:
        matches = [
            row for row in rows
            if row["product_id"] == f"DYNALENE-{grade}"
            and float(row["temperature_C"]) == PROPERTY_TEMPERATURE_C
            and all(row[key].strip() for key in (
                "cp_kJ_kgK", "thermal_conductivity_W_mK",
                "density_kg_m3", "dynamic_viscosity_mPa_s",
            ))
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Expected exactly one complete {grade} observation at "
                f"{PROPERTY_TEMPERATURE_C:g} C; found {len(matches)}"
            )
        row = matches[0]
        fluids.append({
            "grade": grade,
            "cp": float(row["cp_kJ_kgK"]),
            "k": float(row["thermal_conductivity_W_mK"]),
            "rho": float(row["density_kg_m3"]),
            "mu": float(row["dynamic_viscosity_mPa_s"]) * 1e-3,
            "source_id": row["source_id"],
        })
    return fluids


def churchill_friction_factor(reynolds: float, relative_roughness: float) -> float:
    """Churchill all-regime Darcy friction factor."""
    if reynolds <= 0:
        raise ValueError("Reynolds number must be positive")
    term_a = (
        2.457 * math.log(
            1.0 / ((7.0 / reynolds) ** 0.9 + 0.27 * relative_roughness)
        )
    ) ** 16
    term_b = (37530.0 / reynolds) ** 16
    return 8.0 * (
        (8.0 / reynolds) ** 12
        + 1.0 / (term_a + term_b) ** 1.5
    ) ** (1.0 / 12.0)


def evaluate(fluid: dict[str, float | str], mass_flow: float) -> dict[str, float | str]:
    area = math.pi * DIAMETER_M**2 / 4.0
    cp = float(fluid["cp"]) * 1000.0
    conductivity = float(fluid["k"])
    density = float(fluid["rho"])
    viscosity = float(fluid["mu"])
    velocity = mass_flow / (density * area)
    reynolds = density * velocity * DIAMETER_M / viscosity
    prandtl = viscosity * cp / conductivity
    friction = churchill_friction_factor(
        reynolds, ROUGHNESS_M / DIAMETER_M
    )
    pressure_drop = (
        friction * LENGTH_M / DIAMETER_M
        * density * velocity**2 / 2.0
    )
    volumetric_flow = mass_flow / density
    hydraulic_power = pressure_drop * volumetric_flow
    electric_power = hydraulic_power / PUMP_EFFICIENCY

    if not (3000.0 <= reynolds <= 5.0e6 and 0.5 <= prandtl <= 2000.0):
        raise ValueError(
            f"{fluid['grade']} falls outside selected Gnielinski envelope: "
            f"Re={reynolds:.1f}, Pr={prandtl:.3f}"
        )
    nusselt = (
        (friction / 8.0) * (reynolds - 1000.0) * prandtl
        / (
            1.0 + 12.7 * math.sqrt(friction / 8.0)
            * (prandtl ** (2.0 / 3.0) - 1.0)
        )
    )
    h = nusselt * conductivity / DIAMETER_M
    return {
        "mass_flow_kg_s": mass_flow,
        "volumetric_flow_m3_s": volumetric_flow,
        "velocity_m_s": velocity,
        "reynolds": reynolds,
        "prandtl": prandtl,
        "darcy_friction_factor": friction,
        "pressure_drop_Pa": pressure_drop,
        "hydraulic_power_W": hydraulic_power,
        "pump_electric_power_W": electric_power,
        "nusselt": nusselt,
        "internal_h_W_m2K": h,
        "heat_capacity_rate_W_K": mass_flow * cp,
    }


def pump_input_for_flow(
    fluid: dict[str, float | str], mass_flow: float
) -> float:
    """Hydraulic-to-electric power calculation independent of heat-transfer Nu."""
    area = math.pi * DIAMETER_M**2 / 4.0
    density = float(fluid["rho"])
    velocity = mass_flow / (density * area)
    reynolds = density * velocity * DIAMETER_M / float(fluid["mu"])
    friction = churchill_friction_factor(
        reynolds, ROUGHNESS_M / DIAMETER_M
    )
    pressure_drop = (
        friction * LENGTH_M / DIAMETER_M
        * density * velocity**2 / 2.0
    )
    hydraulic_power = pressure_drop * mass_flow / density
    return hydraulic_power / PUMP_EFFICIENCY


def solve_mass_flow_for_power(
    fluid: dict[str, float | str], target_electric_power: float
) -> float:
    # The lower root bracket is intentionally allowed to be laminar; only the
    # final selected operating point must satisfy the Gnielinski envelope.
    low, high = 1e-4, 2.0
    if pump_input_for_flow(fluid, low) > target_electric_power:
        raise ValueError("Target power below lower flow bracket")
    if pump_input_for_flow(fluid, high) < target_electric_power:
        raise ValueError("Target power above upper flow bracket")
    for _ in range(100):
        mid = (low + high) / 2.0
        power = pump_input_for_flow(fluid, mid)
        if power < target_electric_power:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main() -> int:
    fluids = read_properties()
    records = []
    for fluid in fluids:
        cases = (
            ("equal_mass_flow", EQUAL_MASS_FLOW_KG_S),
            ("equal_volumetric_flow", float(fluid["rho"]) * EQUAL_VOLUME_FLOW_M3_S),
            (
                "equal_pump_electric_power",
                solve_mass_flow_for_power(fluid, EQUAL_ELECTRIC_POWER_W),
            ),
        )
        for scenario, mass_flow in cases:
            result = evaluate(fluid, mass_flow)
            records.append({
                "grade": fluid["grade"],
                "property_temperature_C": PROPERTY_TEMPERATURE_C,
                "scenario": scenario,
                **result,
                "property_source_id": fluid["source_id"],
                "model": "Churchill_Darcy_friction_plus_Gnielinski_Nu",
                "evidence_type": "model_estimated",
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(
        f"Wrote {len(records)} model rows to {OUT.relative_to(ROOT)} "
        f"for {len(fluids)} exact grades and three operating constraints."
    )
    print("Model outputs are screening estimates, not measured performance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
