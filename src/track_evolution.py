import fastf1
import pandas as pd
import matplotlib.pyplot as plt

# Load the 2024 Monaco GP Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get lap data
laps = session.laps.copy()

# Keep accurate laps with valid lap times
laps = laps[
    (laps["IsAccurate"] == True) &
    (laps["LapTime"].notna())
].copy()

# Convert lap time to seconds
laps["LapTimeSeconds"] = (
    laps["LapTime"].dt.total_seconds()
)

# Remove unrealistic lap times
laps = laps[
    (laps["LapTimeSeconds"] > 60) &
    (laps["LapTimeSeconds"] < 120)
].copy()

# Calculate average lap time for each lap number
track_evolution = (
    laps.groupby("LapNumber")["LapTimeSeconds"]
    .mean()
    .reset_index()
)

print("\n===== TRACK EVOLUTION =====")
print(track_evolution.head(10))

# Plot
plt.figure(figsize=(12, 6))

plt.plot(
    track_evolution["LapNumber"],
    track_evolution["LapTimeSeconds"],
    marker="o",
    markersize=4
)

plt.xlabel("Lap Number")
plt.ylabel("Average Lap Time (seconds)")
plt.title("2024 Monaco GP - Track Evolution")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()