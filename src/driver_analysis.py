import fastf1
import pandas as pd

# Load session
session = fastf1.get_session(2024, "Monaco", "R")
session.load()

laps = session.laps


def prepare_driver(driver_code):
    driver_laps = laps.pick_driver(driver_code).copy()

    # Keep accurate laps with valid lap times
    driver_laps = driver_laps[
        (driver_laps["IsAccurate"] == True) &
        (driver_laps["LapTime"].notna())
    ].copy()

    # Convert lap time to seconds
    driver_laps["LapTimeSeconds"] = (
    driver_laps["LapTime"].dt.total_seconds()
    )

    # Remove unrealistic lap times
    driver_laps = driver_laps[
        (driver_laps["LapTimeSeconds"] > 60) &
        (driver_laps["LapTimeSeconds"] < 120)
    ]

    return driver_laps


# Prepare drivers
lec = prepare_driver("LEC")
ver = prepare_driver("VER")


# Calculate statistics
results = {
    "Driver": ["LEC", "VER"],
    "Valid Laps": [
        len(lec),
        len(ver)
    ],
    "Fastest Lap (s)": [
        lec["LapTimeSeconds"].min(),
        ver["LapTimeSeconds"].min()
    ],
    "Average Lap (s)": [
        lec["LapTimeSeconds"].mean(),
        ver["LapTimeSeconds"].mean()
    ],
    "Median Lap (s)": [
        lec["LapTimeSeconds"].median(),
        ver["LapTimeSeconds"].median()
    ]
}


df = pd.DataFrame(results)

print("\n===== DRIVER PERFORMANCE =====")
print(df.to_string(index=False))


# Compare average pace
pace_difference = (
    lec["LapTimeSeconds"].mean()
    - ver["LapTimeSeconds"].mean()
)

print("\n===== PACE DIFFERENCE =====")

if pace_difference > 0:
    print(
        f"VER was {pace_difference:.3f} seconds faster "
        f"than LEC on average."
    )
elif pace_difference < 0:
    print(
        f"LEC was {abs(pace_difference):.3f} seconds faster "
        f"than VER on average."
    )
else:
    print("Both drivers had the same average lap time.")