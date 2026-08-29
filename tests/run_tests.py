import os
import sys
import json
import traceback

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TESTS_DIR = os.path.join(BASE_DIR, "tests")
sys.path.insert(0, TESTS_DIR)

import test_outputs

# Load weights
weights_file = os.path.join(TESTS_DIR, "test_weights.json")
with open(weights_file, "r", encoding="utf-8") as f:
    weights_data = json.load(f)

weights_map = {item["test_name"]: item["weight"] for item in weights_data}
decision_map = {item["test_name"]: item.get("decision", False) for item in weights_data}

# Run tests
test_funcs = [
    test_outputs.test_output_files_exist,
    test_outputs.test_csv_schema_and_row_count,
    test_outputs.test_json_schema_validity,
    test_outputs.test_md_required_headings,
    test_outputs.test_md_selected_powertrain_architecture,
    test_outputs.test_csv_rank_1_is_diesel_hybrid,
    test_outputs.test_json_recommended_strategy,
    test_outputs.test_tcol_numeric_reconciliation,
    test_outputs.test_pallet_mile_metric_validity,
    test_outputs.test_bev_grid_substation_finding,
    test_outputs.test_sla_pharma_delay_penalty_finding,
    test_outputs.test_penalty_unauthorized_strategy_tokens,
    test_outputs.test_penalty_substation_upgrade_omitted_for_bev,
]

earned_weights = 0
positive_weights_sum = sum(w for w in weights_map.values() if w > 0)
ctrf_tests = []

print("Running Automated Verifier Suite...")

for func in test_funcs:
    tname = func.__name__
    w = weights_map.get(tname, 1)
    status = "passed"
    err_msg = ""
    
    try:
        func()
        # For positive tests: passing earns +w
        # For penalty tests (w < 0): passing means defect is present -> charges penalty (w is negative, so subtracts)
        if w > 0:
            earned_weights += w
            print(f"  [PASS] {tname:<45} (+{w} pts)")
        else:
            # Penalty passed => defect present!
            earned_weights += w
            print(f"  [PENALTY FIRED] {tname:<45} ({w} pts)")
    except Exception as e:
        err_msg = str(e)
        if w > 0:
            status = "failed"
            print(f"  [FAIL] {tname:<45} (0/{w} pts) -> {err_msg}")
        else:
            # Penalty failed (assert failed) => defect is ABSENT (good)!
            status = "passed"
            print(f"  [CLEAN] {tname:<45} (0 penalty pts)")
            
    ctrf_tests.append({
        "name": tname,
        "status": status,
        "raw_status": status,
        "message": err_msg,
        "weight": w,
        "decision": decision_map.get(tname, False)
    })

reward = max(0.0, min(1.0, earned_weights / positive_weights_sum))
print(f"\nFinal Reward: {reward:.4f} ({earned_weights}/{positive_weights_sum} points)")

# Create logs directory
log_dir = os.path.join(BASE_DIR, "logs", "verifier")
if not os.path.exists(log_dir):
    log_dir = r"/logs/verifier"
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        log_dir = os.path.join(BASE_DIR, "logs", "verifier")
        os.makedirs(log_dir, exist_ok=True)
else:
    os.makedirs(log_dir, exist_ok=True)

# Write reward.json
reward_path = os.path.join(log_dir, "reward.json")
with open(reward_path, "w", encoding="utf-8") as f:
    json.dump({"reward": reward}, f, indent=2)

# Write ctrf.json
ctrf_report = {
    "report": {
        "summary": {
            "tests": len(ctrf_tests),
            "passed": sum(1 for t in ctrf_tests if t["status"] == "passed"),
            "failed": sum(1 for t in ctrf_tests if t["status"] == "failed"),
            "reward": reward
        },
        "tests": ctrf_tests
    }
}
ctrf_path = os.path.join(log_dir, "ctrf.json")
with open(ctrf_path, "w", encoding="utf-8") as f:
    json.dump(ctrf_report, f, indent=2)

print(f"Verifier results written to {reward_path} and {ctrf_path}")
