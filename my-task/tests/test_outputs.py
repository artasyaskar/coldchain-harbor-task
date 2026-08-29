import os
import sys
import json
import csv
import re
import math

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = "/workspace/output"
if not os.path.exists(OUT_DIR):
    OUT_DIR = os.path.join(BASE_DIR, "output")
    if not os.path.exists(OUT_DIR):
        OUT_DIR = os.path.join(os.getcwd(), "output")

ALLOWED_STRATEGIES = ["BEV_DEPOT", "BIO_CNG", "DIESEL_HYB_TRU", "H2_FCEV"]

# -------------------------------------------------------------
# 1. Structural & File Presence Tests
# -------------------------------------------------------------
def test_output_files_exist():
    """Verify all 3 required deliverable files exist in output/."""
    req_files = [
        "executive_recommendation.md",
        "lifecycle_cost_analysis.csv",
        "operational_risk_matrix.json"
    ]
    for rf in req_files:
        fpath = os.path.join(OUT_DIR, rf)
        assert os.path.exists(fpath), f"Missing required output file: {rf}"
        assert os.path.getsize(fpath) > 20, f"Output file is empty or trivial: {rf}"

def test_csv_schema_and_row_count():
    """Verify lifecycle_cost_analysis.csv has exact required columns and 4 strategy rows."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
        
    expected_headers = [
        "strategy_id", "net_vehicle_capex_musd", "fuel_and_energy_musd", "depot_infra_capex_musd",
        "utility_demand_and_substation_musd", "maintenance_and_overhauls_musd",
        "sla_and_pharma_penalties_musd", "regulatory_tolls_musd", "total_tcol_musd",
        "tcol_per_pallet_mile_usd", "final_rank"
    ]
    assert headers == expected_headers, f"CSV headers mismatch. Got: {headers}, Expected: {expected_headers}"
    assert len(rows) == 4, f"Expected exactly 4 strategy rows, got {len(rows)}"
    
    found_strats = [r["strategy_id"].strip() for r in rows]
    assert set(found_strats) == set(ALLOWED_STRATEGIES), f"Invalid strategy tokens in CSV: {found_strats}"

def test_json_schema_validity():
    """Verify operational_risk_matrix.json adheres to schema and contains required keys."""
    json_path = os.path.join(OUT_DIR, "operational_risk_matrix.json")
    assert os.path.exists(json_path), "operational_risk_matrix.json missing"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert "fleet_size_total" in data and data["fleet_size_total"] == 90
    assert "planning_horizon_years" in data and data["planning_horizon_years"] == 5
    assert "recommended_strategy" in data
    assert "hub_feasibility" in data
    assert "candidate_tcol_summary" in data
    
    for hub in ["HUB_NORTH", "HUB_CENTRAL", "HUB_SOUTH"]:
        assert hub in data["hub_feasibility"], f"Missing hub {hub} in hub_feasibility"
        h_info = data["hub_feasibility"][hub]
        assert "strategy_feasible" in h_info
        assert "grid_substation_upgrade_required" in h_info
        assert "annual_clean_air_tolls_usd" in h_info
        assert "annual_sla_breach_count" in h_info

def test_md_required_headings():
    """Verify executive_recommendation.md contains all 6 required section headers."""
    md_path = os.path.join(OUT_DIR, "executive_recommendation.md")
    assert os.path.exists(md_path), "executive_recommendation.md missing"
    
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    req_headings = [
        r"# Executive Summary & Strategic Recommendation",
        r"## Selected Powertrain Architecture",
        r"## 5-Year Lifecycle Financial Summary",
        r"## Operational Feasibility & Cold-Chain Integrity Analysis",
        r"## Rejection Justifications for Alternative Options",
        r"## Hub-Specific Implementation & Risk Mitigation Plan"
    ]
    for rh in req_headings:
        assert re.search(re.escape(rh), content, re.IGNORECASE), f"Missing required heading in MD: {rh}"

# -------------------------------------------------------------
# 2. Decision & Recommendation Tests (is_recommendation_criterion)
# -------------------------------------------------------------
def test_md_selected_powertrain_architecture():
    """Decision Test 1: executive_recommendation.md selects DIESEL_HYB_TRU."""
    md_path = os.path.join(OUT_DIR, "executive_recommendation.md")
    assert os.path.exists(md_path), "executive_recommendation.md missing"
    
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "DIESEL_HYB_TRU" in content, "Winning token DIESEL_HYB_TRU not found in executive_recommendation.md"
    match = re.search(r"## Selected Powertrain Architecture\s+(.*?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
    assert match, "Section '## Selected Powertrain Architecture' empty or missing"
    sec_text = match.group(1)
    assert "DIESEL_HYB_TRU" in sec_text, f"Selected Powertrain Architecture section must name DIESEL_HYB_TRU, got: {sec_text}"

def test_csv_rank_1_is_diesel_hybrid():
    """Decision Test 2: lifecycle_cost_analysis.csv assigns final_rank 1 to DIESEL_HYB_TRU."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    rank1_rows = [r for r in rows if str(r.get("final_rank", "")).strip() == "1"]
    assert len(rank1_rows) == 1, f"Expected exactly one Rank 1 row, found {len(rank1_rows)}"
    assert rank1_rows[0]["strategy_id"].strip() == "DIESEL_HYB_TRU", f"Rank 1 strategy is {rank1_rows[0]['strategy_id']}, expected DIESEL_HYB_TRU"

def test_json_recommended_strategy():
    """Decision Test 3: operational_risk_matrix.json has recommended_strategy == 'DIESEL_HYB_TRU'."""
    json_path = os.path.join(OUT_DIR, "operational_risk_matrix.json")
    assert os.path.exists(json_path), "operational_risk_matrix.json missing"
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data.get("recommended_strategy") == "DIESEL_HYB_TRU", f"JSON recommended_strategy is {data.get('recommended_strategy')}, expected DIESEL_HYB_TRU"

# -------------------------------------------------------------
# 3. Quantitative Financial & Operational Tests
# -------------------------------------------------------------
def test_tcol_numeric_reconciliation():
    """Verify total_tcol_musd reconciles with component sums and matches ground-truth within 10%."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    expected_ranges = {
        "DIESEL_HYB_TRU": (20.0, 26.0),
        "BIO_CNG": (23.0, 29.0),
        "H2_FCEV": (44.0, 56.0),
        "BEV_DEPOT": (52.0, 75.0)
    }
    
    for r in rows:
        strat = r["strategy_id"].strip()
        tot = float(r["total_tcol_musd"])
        
        comp_sum = (float(r["net_vehicle_capex_musd"]) + 
                    float(r["fuel_and_energy_musd"]) + 
                    float(r["depot_infra_capex_musd"]) + 
                    float(r["utility_demand_and_substation_musd"]) + 
                    float(r["maintenance_and_overhauls_musd"]) + 
                    float(r["sla_and_pharma_penalties_musd"]) + 
                    float(r["regulatory_tolls_musd"]))
        assert abs(tot - comp_sum) < 0.15, f"Component sum mismatch for {strat}: total={tot}, sum={comp_sum}"
        
        low, high = expected_ranges[strat]
        assert low <= tot <= high, f"Reported TCOL for {strat} ({tot}M) outside valid range [{low}M, {high}M]"

def test_pallet_mile_metric_validity():
    """Verify tcol_per_pallet_mile_usd is mathematically consistent with total_tcol_musd."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    for r in rows:
        strat = r["strategy_id"].strip()
        tot_m = float(r["total_tcol_musd"])
        pm_cost = float(r["tcol_per_pallet_mile_usd"])
        
        implied_pm = (tot_m * 1e6) / pm_cost
        assert 1.0e8 <= implied_pm <= 1.5e8, f"Implied 5-year pallet-miles for {strat} ({implied_pm:,.0f}) outside realistic 100M-150M range"

def test_bev_grid_substation_finding():
    """Verify operational analysis identifies non-zero utility/substation costs for BEV."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = {r["strategy_id"].strip(): r for r in reader}
        
    bev_util = float(rows["BEV_DEPOT"]["utility_demand_and_substation_musd"])
    assert bev_util >= 5.0, f"BEV utility demand and substation cost must be >= $5.0M, got {bev_util}M"

def test_sla_pharma_delay_penalty_finding():
    """Verify operational analysis identifies significant SLA/pharma penalties for BEV (> $5.0M)."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    assert os.path.exists(csv_path), "lifecycle_cost_analysis.csv missing"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = {r["strategy_id"].strip(): r for r in reader}
        
    bev_sla = float(rows["BEV_DEPOT"]["sla_and_pharma_penalties_musd"])
    assert bev_sla >= 5.0, f"BEV SLA/Pharma penalties must be >= $5.0M due to en-route charging dwell delays, got {bev_sla}M"

# -------------------------------------------------------------
# 4. Penalty Tests (Negative Weights for Independent Defects)
# -------------------------------------------------------------
def test_penalty_unauthorized_strategy_tokens():
    """Penalty test: Passes (charges penalty) only if candidate tokens other than standard 4 are used in an existing file."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    if not os.path.exists(csv_path):
        assert False, "File missing; no penalty charged"
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        strats = [r.get("strategy_id", "").strip() for r in reader]
    invalid = [s for s in strats if s not in ALLOWED_STRATEGIES]
    assert len(invalid) > 0, "No unauthorized tokens found (clean attempt)"

def test_penalty_substation_upgrade_omitted_for_bev():
    """Penalty test: Passes (charges penalty) if BEV utility/substation cost is reported as 0.0 in an existing file."""
    csv_path = os.path.join(OUT_DIR, "lifecycle_cost_analysis.csv")
    if not os.path.exists(csv_path):
        assert False, "File missing; no penalty charged"
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = {r.get("strategy_id", "").strip(): r for r in reader}
    bev_row = rows.get("BEV_DEPOT")
    if not bev_row:
        assert False, "BEV row missing; no penalty charged"
    bev_util = float(bev_row.get("utility_demand_and_substation_musd", 0.0))
    assert bev_util == 0.0, "BEV utility cost correctly identified as non-zero"

