# Commercial Cold-Chain Fleet Powertrain & Refrigeration Transition Strategy

## 1. Professional Role & Decision Context

You are the Lead Fleet Logistics Data Analyst and Asset Strategy Advisor to the Senior Vice President of Supply Chain Logistics & Fleet Assets at Vanguard ColdChain Logistics (VCCL).

VCCL operates a specialized multi-regional refrigerated fleet transporting high-value pharmaceuticals, including biologics, vaccines, and active pharmaceutical ingredients under Good Distribution Practice (GDP) protocols, as well as perishable food products.

The company operates across three major operational hubs:

1. **Hub-North (Allentown, PA)**: Dense urban delivery routes, regional cold-chain distribution, and municipal Low-Emission Zone (LEZ) regulations.
2. **Hub-Central (Greensboro, NC)**: High-volume regional distribution network with 250–350 mile corridors and standard commercial electric utility service.
3. **Hub-South (Jacksonville, FL)**: Subtropical climate, extreme summer ambient heat, long linehaul corridors, and strict pharmaceutical GDP temperature-integrity requirements.

VCCL's existing 90-unit Class 8 refrigerated tractor fleet and 120 matching multi-temperature refrigerated trailers have reached the end of their operational lifecycle.

Your task is to evaluate four competing powertrain and refrigeration technology architectures over a **5-year planning horizon (60 months)** and select exactly **ONE unified strategy** to deploy across all 90 tractor replacements, with 30 units assigned per hub, and all 120 matching trailer replacements.

---

## 2. Candidate Strategy Tokens

Your evaluation must strictly analyze the following four standardized candidate options:

* `BEV_DEPOT`: Class 8 Heavy-Duty Battery Electric Vehicle (BEV) Tractors with Integrated All-Electric Transport Refrigeration Units (e-TRUs) and On-Site Depot DC Fast Charging.
* `BIO_CNG`: Renewable Natural Gas (RNG / Bio-Methane) Tractors with Mechanical-Drive Transport Refrigeration Units and On-Site Modular CNG Fast-Fill Fueling.
* `DIESEL_HYB_TRU`: Next-Generation Ultra-Low-Emission Clean Diesel Tractors (EPA 2027 / Euro VI-E compliant) paired with Solar-Assisted Electric Hybrid TRUs (Rooftop Solar-PV + 480V Depot Shore-Power Standby).
* `H2_FCEV`: Class 8 Hydrogen Fuel Cell Electric Vehicle (FCEV) Tractors with Cryo-Electric TRUs and Contracted On-Site Tube-Trailer Dispensing.

---

## 3. Available Data Sources

The following operational, technical, financial, and regulatory datasets are provided in the `environment/` directory:

1. `fleet_route_telematics_2025.csv`: Full-year sampled operational route dispatches across all three hubs, recording route class, distance, stop count, door-opening durations, transit hours, cargo classification (`PHARMA_GDP` vs `PERISHABLE_FOOD`), pallet payload, and dispatch completion status.
2. `refrigeration_thermal_logs.json`: Telemetry recordings of ambient temperature, target box temperatures, steady-state thermal loads, infiltration heat flux, and compressor power draw across all 12 calendar months and facilities.
3. `hub_utility_and_facility_tariffs.xlsx`: Electric utility rate schedules across three sheets: Time-of-Use (TOU) energy rates, 15-minute coincident peak demand charge tariffs with 85% rolling ratchet rules and facility transformer capacity limits, and utility substation upgrade capital cost schedules.
4. `powertrain_procurement_contracts.pdf`: Master RFP procurement agreements detailing vehicle purchase pricing (MSRP), government incentive/voucher structures, guaranteed Year-5 residual buyback rates, scheduled preventive maintenance (PM) rates, component overhaul schedules, and delivery delay/temperature-excursion SLA penalty terms.
5. `fuel_and_energy_index_pricing.csv`: Historical and projected delivered fuel commodity prices, regional pipeline transportation surcharges, and vehicle tractive fuel economy benchmarks.
6. `depot_infrastructure_quotes.json`: Capital expenditure (CapEx) and annual maintenance/lease quotes for private hub fueling and charging infrastructure across all four powertrain architectures.
7. `municipal_clean_air_regulations.csv`: Municipal clean-air zone entry toll rates, vehicle technology exemptions, and annual regulated urban delivery frequencies.

---

## 4. Required Deliverables & Output Contract

You must execute the complete analysis and generate **exactly three structured deliverable files** within the `output/` directory.

### Deliverable 1: `output/executive_recommendation.md`

Create a formal executive briefing and strategic justification for the Senior Vice President of Supply Chain Logistics.

The document must be valid Markdown and contain the following **exact section headings**:

* `# Executive Summary & Strategic Recommendation`
* `## Selected Powertrain Architecture`
  Must clearly state the selected candidate token: `BEV_DEPOT`, `BIO_CNG`, `DIESEL_HYB_TRU`, or `H2_FCEV`.
* `## 5-Year Lifecycle Financial Summary`
* `## Operational Feasibility & Cold-Chain Integrity Analysis`
* `## Rejection Justifications for Alternative Options`
  Must explicitly address and justify the rejection of the other three candidate architectures.
* `## Hub-Specific Implementation & Risk Mitigation Plan`

### Deliverable 2: `output/lifecycle_cost_analysis.csv`

Create a standardized CSV file summarizing the 5-year discounted lifecycle cost breakdown across all four candidate strategies.

**Required Columns (Exact Header Names):**

`strategy_id,net_vehicle_capex_musd,fuel_and_energy_musd,depot_infra_capex_musd,utility_demand_and_substation_musd,maintenance_and_overhauls_musd,sla_and_pharma_penalties_musd,regulatory_tolls_musd,total_tcol_musd,tcol_per_pallet_mile_usd,final_rank`

**Required Rows:**

Exactly 4 rows, one for each candidate strategy:

* `BEV_DEPOT`
* `BIO_CNG`
* `DIESEL_HYB_TRU`
* `H2_FCEV`

**Precision:**

* Cost columns in millions of USD (`_musd`) must be numeric values rounded to 2 decimal places.
* `tcol_per_pallet_mile_usd` must be rounded to 3 decimal places.
* `final_rank` must be an integer from 1 (lowest cost / best) to 4 (highest cost).

### Deliverable 3: `output/operational_risk_matrix.json`

Create a machine-readable JSON file detailing hub-level operational feasibility and risk metrics.

It must match the following JSON schema:

```json
{
  "fleet_size_total": 90,
  "planning_horizon_years": 5,
  "recommended_strategy": "",
  "hub_feasibility": {
    "HUB_NORTH": {
      "strategy_feasible": true,
      "grid_substation_upgrade_required": false,
      "annual_clean_air_tolls_usd": 15750.0,
      "annual_sla_breach_count": 0
    },
    "HUB_CENTRAL": {
      "strategy_feasible": true,
      "grid_substation_upgrade_required": false,
      "annual_clean_air_tolls_usd": 0.0,
      "annual_sla_breach_count": 0
    },
    "HUB_SOUTH": {
      "strategy_feasible": true,
      "grid_substation_upgrade_required": false,
      "annual_clean_air_tolls_usd": 0.0,
      "annual_sla_breach_count": 0
    }
  },
  "candidate_tcol_summary": {
    "BEV_DEPOT": 0.00,
    "BIO_CNG": 0.00,
    "DIESEL_HYB_TRU": 0.00,
    "H2_FCEV": 0.00
  }
}
```

The placeholder values in `recommended_strategy` and `candidate_tcol_summary` must be replaced with the values calculated from the provided datasets. Do not hard-code a winner or lifecycle cost without deriving it from the source data.

---

## 5. Explicit Analytical Constraints & Rules

### 1. Planning Horizon & Discounting
The evaluation covers 5 operational years (60 months). All recurring annual operating expenses, including fuel, energy, maintenance, utility demand charges, facility leases, regulatory tolls, and SLA penalties, as well as Year-5 residual buyback values, must be discounted using the corporate discount rate of **6.0% per annum** specified in the master contract.

### 2. Single Unified Strategy
VCCL requires a single standardized powertrain architecture across all 90 tractors and 120 trailers. Multi-powertrain hybrid splitting across hubs is not supported. The final recommendation must therefore select exactly one of: `BEV_DEPOT`, `BIO_CNG`, `DIESEL_HYB_TRU`, or `H2_FCEV`.

### 3. Data Integrity & Reconciliation
The operational data contains real-world enterprise reporting variations, such as legacy facility naming aliases, mixed temperature scales, mixed power units, and test dispatches. You must systematically reconcile these data streams before calculating the final lifecycle economics. Do not assume that raw record counts, aliases, units, or test dispatches can be used without validation.

### 4. Source Data Must Drive the Analysis
All financial, operational, energy, refrigeration, regulatory, and infrastructure results must be derived from the datasets provided in the `environment/` directory. Do not use precomputed winner tables, hidden ground-truth values, rubric files, or hard-coded final answers as analytical inputs. The model should independently load and reconcile the source data, perform the required calculations, and determine the final ranking.

### 5. All Deliverables Must Be Written to `output/`
Evaluation is performed strictly on the deliverable files written to the `output/` directory. Text printed to the console is not graded.

The final `output/` directory must contain exactly these three deliverables:
```text
output/executive_recommendation.md
output/lifecycle_cost_analysis.csv
output/operational_risk_matrix.json
```
