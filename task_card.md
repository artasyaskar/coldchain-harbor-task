# Task Card: Commercial Cold-Chain Fleet Powertrain & Refrigeration Transition Strategy

## 1. Task Overview
- **Domain**: Supply Chain Logistics, Fleet Decarbonization, Commercial Energy Economics, & Cold-Chain Operations
- **Role**: Lead Fleet Logistics Data Analyst & Asset Strategy Advisor
- **Organization**: Vanguard ColdChain Logistics (VCCL)
- **Decision to be Made**: Choose exactly one 5-year fleet powertrain & refrigeration technology architecture (i.e., `BEV_DEPOT`, `BIO_CNG`, `DIESEL_HYB_TRU`, or `H2_FCEV`) for a 90-unit Class 8 tractor replacement and 120-trailer program across 3 operational hubs (Hub-North / Allentown, Hub-Central / Greensboro, Hub-South / Jacksonville).
- **Deliverables**:
  1. `output/executive_recommendation.md`: Formal briefing document with 6 required section headers and clear decision justification.
  2. `output/lifecycle_cost_analysis.csv`: Complete 5-year discounted lifecycle cost analysis across all 4 candidate strategies.
  3. `output/operational_risk_matrix.json`: Structured hub-level feasibility, grid impact, regulatory tolls, and SLA metrics.

---

## 2. Complexity Justification & Design Challenges

### Reasoning Challenge 1: The Ambient Thermal Refrigeration & Range Collapse Crux (The Primary Crux)
- **Planted Evidence**: `refrigeration_thermal_logs.json` records high summer ambient temperatures (up to 95°F–104°F / 35°C–40°C in Hub-South) and high steady-state compressor power draw (8.5–11.5 kW continuous). `fleet_route_telematics_2025.csv` logs 3,530 annual completed dispatches across local, regional, and linehaul distances with multi-stop door openings.
- **Correct Action**: Reconcile thermal cooling power with route transit duration and tractive energy draw (1.85 kWh/mile). Recognize that auxiliary refrigeration collapses BEV usable range by 34%–42% on summer regional and linehaul routes, causing battery deficits on 71.6% of dispatches. Model the mandatory 45-minute en-route DC fast charging dwell times at peak commercial rates ($0.45/kWh) and calculate delivery SLA delay penalties ($1,200/event) and pharma GDP spoilage deductibles ($15,000/event), accumulating $17.49M in operational penalties over 5 years.
- **Careless Action**: Uses nominal EPA highway tractive efficiency (1.85 kWh/mile) and ignores auxiliary refrigeration power draw, assuming all BEV routes complete on depot charge without en-route delays or penalties.

### Reasoning Challenge 2: Coincident 15-Minute Peak Demand Ratchets & Grid Interconnection Barrier
- **Planted Evidence**: `hub_utility_and_facility_tariffs.xlsx` specifies a 15-minute peak demand charge tariff ($21.00–$26.80/kW/month), an 85% rolling 12-month ratchet clause, and a 2.50 MW firm transformer capacity limit. `depot_infrastructure_quotes.json` details 15 dual-port 150 kW DC Fast Chargers per hub.
- **Correct Action**: Model the simultaneous overnight charging profile of 30 BEVs per hub; identify that coincident peak load reaches 2.85 MW, exceeding the 2.50 MW facility transformer capacity. Calculate the mandatory $2.95M utility substation upgrade capex across all three hubs and apply the 85% rolling ratchet rule across monthly billed demand, adding $10.76M in utility demand and infrastructure costs for `BEV_DEPOT`.
- **Careless Action**: Multiplies total kWh energy by off-peak volumetric rates ($0.09/kWh) and completely ignores 15-minute demand charges, rolling ratchet clauses, and grid capacity thresholds.

### Reasoning Challenge 3: Lifecycle Engine Maintenance Escalation & Tank NDT Traps in Bio-CNG
- **Planted Evidence**: `powertrain_procurement_contracts.pdf` establishes scheduled PM rates for spark-ignited natural gas engines ($0.178/mile vs $0.112/mile for diesel) and mandates Month-36 DOT ultrasonic non-destructive testing (NDT) and hydro-structural cylinder recertifications ($2,800/tractor). `fuel_and_energy_index_pricing.csv` adds regional pipeline transportation surcharges in Hub-North ($0.35/DGE).
- **Correct Action**: Compute cumulative 5-year maintenance escalation, pipeline delivery surcharges, and discounted Year-3 DOT cylinder inspection costs, revealing that `BIO_CNG`'s total lifecycle cost ($25.66M) exceeds `DIESEL_HYB_TRU` ($22.47M) by $3.19M (+14.2%).
- **Careless Action**: Assumes uniform preventive maintenance across internal combustion engines and overlooks DOT composite tank recertification schedules.

---

## 3. Ground-Truth Recommendation & Figures

Across 124.83M 5-year delivered pallet-miles discounted at 6.0% per annum:

1. **`DIESEL_HYB_TRU` (Rank 1 - WINNER)**: **$22.47M Total TCOL** ($0.180/pallet-mile).
   - Net Vehicle Capex: $19.15M
   - Fuel & Energy: $2.25M (Solar-PV offsets 36.0% of daytime road TRU power; depot shore power eliminates idling)
   - Depot Infrastructure: $0.55M
   - Utility Demand & Substations: $0.00M
   - Maintenance & Overhauls: $0.46M
   - SLA Delay & Pharma Penalties: $0.00M (100% route feasibility)
   - Municipal Clean Air Tolls: $0.07M ($35.00/entry in Allentown LEZ)
2. **`BIO_CNG` (Rank 2)**: **$25.66M Total TCOL** ($0.205/pallet-mile) — +$3.19M / +14.2% cost premium.
3. **`H2_FCEV` (Rank 3)**: **$49.57M Total TCOL** ($0.397/pallet-mile) — Exorbitant fuel costs ($11.80/kg H2) and $780k/yr tube-trailer lease fees.
4. **`BEV_DEPOT` (Rank 4)**: **$63.01M Total TCOL** ($0.505/pallet-mile) — Burdened by $17.49M SLA/GDP penalties and $10.76M utility substation/demand ratchet costs.

---

## 4. Taxonomy Tags
`logistics`, `cold-chain`, `fleet-management`, `energy-transition`, `tco-analysis`, `utility-tariffs`, `demand-charges`, `refrigeration-physics`, `multi-source-reconciliation`

---

## 5. Expected Difficulty & Sweep Model Failure Modes
- **Strong Model Target (Mean Reward <= 0.60)**: Strong models often evaluate nominal fuel efficiency and state zero-emission vouchers, selecting `BEV_DEPOT` or `BIO_CNG`. They overlook the non-linear coupling between high-temperature ambient cooling loads, battery depletion, mid-route DCFC delays, and 15-minute utility demand ratchets.
- **Weak Model Target (Mean Reward <= 0.35)**: Weak models fail on multi-format data reconciliation, hub aliasing, mixed temperature/power units, and complex financial discounting.
