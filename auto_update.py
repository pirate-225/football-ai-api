import os

print("🔄 Updating data...")

os.system("python update_teams.py")
os.system("python process_teams.py")

with open("update_log.txt", "a") as f:
    f.write("Update effectué\n")

print("✅ Data updated")