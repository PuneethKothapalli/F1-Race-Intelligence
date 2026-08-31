import fastf1

# Load the 2024 Monaco GP Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get lap data
laps = session.laps

print("\n===== DATASET INFORMATION =====")
print("Number of rows:", len(laps))
print("Number of columns:", len(laps.columns))

print("\n===== COLUMNS =====")
print(laps.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(laps.head())

print("\n===== DRIVERS =====")
print(laps["Driver"].unique())