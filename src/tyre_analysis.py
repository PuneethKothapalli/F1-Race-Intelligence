import fastf1
import matplotlib.pyplot as plt

# Load the 2024 Monaco GP Race
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

# Get lap data
laps = session.laps

# Select driver
driver = laps.pick_driver("VER").copy()

# Keep accurate laps with valid lap times and tyre information
driver = driver[
    (driver["IsAccurate"] == True) &
    (driver["LapTime"].notna()) &
    (driver["TyreLife"].notna()) &
    (driver["Compound"].notna())
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

# Display tyre information
print("\n===== TYRE DATA =====")
print(
    driver[
        [
            "LapNumber",
            "Stint",
            "Compound",
            "TyreLife",
            "LapTimeSeconds"
        ]
    ].to_string(index=False)
)

# Plot tyre degradation
plt.figure(figsize=(12, 6))

for compound in driver["Compound"].unique():

    tyre_data = driver[
        driver["Compound"] == compound
    ]

    plt.plot(
        tyre_data["TyreLife"],
        tyre_data["LapTimeSeconds"],
        marker="o",
        markersize=4,
        label=compound
    )

plt.xlabel("Tyre Age (laps)")
plt.ylabel("Lap Time (seconds)")
plt.title("2024 Monaco GP - VER Tyre Performance")
plt.legend(title="Tyre Compound")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()