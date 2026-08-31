import fastf1

print("FastF1 version:", fastf1.__version__)

session = fastf1.get_session(2024, "Monaco", "R")
session.load()

print("Session loaded successfully!")
print("Number of laps:", len(session.laps))