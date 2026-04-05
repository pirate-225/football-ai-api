import os

print("Updating matches...")
os.system("python -m api.update_api_data")

print("Updating odds...")
os.system("python -m api.update_odds_data")

print("Updating standings...")
os.system("python -m api.update_standings_data")

print("Building form...")
os.system("python build_form.py")

print("Building elo...")
os.system("python build_elo.py")

print("Building master dataset...")
os.system("python build_master_dataset.py")

print("Building features...")
os.system("python feature_engineering.py")

print("Training models...")
os.system("python train_models.py")

print("Update finished successfully")