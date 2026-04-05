import os

print("Updating matches...")
os.system("python -m api.update_api_data")

print("Building team stats...")
os.system("python build_team_stats.py")

print("Building features...")
os.system("python feature_engineering.py")

print("Training models...")
os.system("python train_models.py")

print("Update finished successfully")