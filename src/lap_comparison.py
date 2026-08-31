import fastf1
import matplotlib.pyplot as plt

# Load the 2024 Monaco GP Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get lap data
laps = session.laps

# Select drivers
driver1 = laps.pick_driver("LEC").copy()
driver2 = laps.pick_driver("VER").copy()

# Keep only accurate laps with a valid lap time
driver1 = driver1[
    (driver1["IsAccurate"] == True) &
    (driver1["LapTime"].notna())
]

driver2 = driver2[
    (driver2["IsAccurate"] == True) &
    (driver2["LapTime"].notna())
]

# Convert lap time to seconds
driver1["LapTimeSeconds"] = driver1["LapTime"].dt.total_seconds()
driver2["LapTimeSeconds"] = driver2["LapTime"].dt.total_seconds()

# Remove unrealistic lap times
driver1 = driver1[
    (driver1["LapTimeSeconds"] > 60) &
    (driver1["LapTimeSeconds"] < 120)
]

driver2 = driver2[
    (driver2["LapTimeSeconds"] > 60) &
    (driver2["LapTimeSeconds"] < 120)
]

# Create plot
plt.figure(figsize=(12, 6))

plt.plot(
    driver1["LapNumber"],
    driver1["LapTimeSeconds"],
    label="LEC",
    marker="o",
    markersize=3
)

plt.plot(
    driver2["LapNumber"],
    driver2["LapTimeSeconds"],
    label="VER",
    marker="o",
    markersize=3
)

plt.xlabel("Lap Number")
plt.ylabel("Lap Time (seconds)")
plt.title("2024 Monaco GP - Lap Time Comparison")

plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()