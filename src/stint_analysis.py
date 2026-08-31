import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the 2024 Monaco GP Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get lap data
laps = session.laps

# Select VER
driver = laps.pick_driver("VER").copy()

# Keep useful records
driver = driver[
    (driver["IsAccurate"] == True) &
    (driver["LapTime"].notna()) &
    (driver["TyreLife"].notna()) &
    (driver["Compound"].notna()) &
    (driver["Stint"].notna())
].copy()

# Convert lap time to seconds
driver["LapTimeSeconds"] = (
    driver["LapTime"].dt.total_seconds()
)

# Remove unrealistic lap times
driver = driver[
    (driver["LapTimeSeconds"] > 60) &
    (driver["LapTimeSeconds"] < 120)
].copy()

print("\n===== STINT ANALYSIS =====")

# Analyze each stint
for stint_number, stint_data in driver.groupby("Stint"):

    # Need at least 3 laps for a meaningful trend
    if len(stint_data) < 3:
        continue

    # Linear trend:
    # x = tyre age
    # y = lap time
    slope, intercept = np.polyfit(
        stint_data["TyreLife"],
        stint_data["LapTimeSeconds"],
        1
    )

    print(f"\nStint {int(stint_number)}")
    print(f"Tyre compound: {stint_data['Compound'].iloc[0]}")
    print(f"Number of laps: {len(stint_data)}")
    print(f"Tyre age: {stint_data['TyreLife'].min()} "
          f"to {stint_data['TyreLife'].max()} laps")
    print(f"Observed lap-time trend: {slope:.3f} sec/lap")

    if slope > 0:
        print("Lap time generally increased as the tyre aged.")
    elif slope < 0:
        print("Lap time generally decreased as the tyre aged.")
    else:
        print("Lap time remained approximately stable.")


# Plot each stint separately
plt.figure(figsize=(12, 6))

for stint_number, stint_data in driver.groupby("Stint"):

    if len(stint_data) < 3:
        continue

    compound = stint_data["Compound"].iloc[0]

    plt.plot(
        stint_data["TyreLife"],
        stint_data["LapTimeSeconds"],
        marker="o",
        markersize=4,
        label=f"Stint {int(stint_number)} - {compound}"
    )

plt.xlabel("Tyre Age (laps)")
plt.ylabel("Lap Time (seconds)")
plt.title("2024 Monaco GP - VER Stint Performance")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()