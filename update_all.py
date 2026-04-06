import os
import subprocess

print("Starting full update pipeline...")

# Create folders if they don't exist
os.makedirs("data_raw", exist_ok=True)
os.makedirs("data_processed", exist_ok=True)
os.makedirs("models", exist_ok=True)

def run_script(script):
    print(f"Running {script}...")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"Error while running {script}")
        exit(1)

# API data
run_script("api/update_api_data.py")

# Build features pipeline
run_script("build_form.py")
run_script("build_elo.py")
run_script("build_master_dataset.py")
run_script("build_team_stats.py")
run_script("feature_engineering.py")
run_script("train_models.py")

print("Update finished successfully")