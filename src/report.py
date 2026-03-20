import csv
from datetime import datetime
from config import DATA_CSV_PATH

def generate_session_report():
    """Reads the plates.csv and prints a summary for the current day."""
    if not os.path.exists(DATA_CSV_PATH):
        print("No plate data found yet.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    plate_counts = {}
    total_detections = 0

    with open(DATA_CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row['Timestamp']
            plate = row['PlateText']
            
            if ts.startswith(today):
                plate_counts[plate] = plate_counts.get(plate, 0) + 1
                total_detections += 1

    print(f"\n--- [ANPR SESSION REPORT: {today}] ---")
    print(f"Total Unique Plates: {len(plate_counts)}")
    print(f"Total Valid Detections: {total_detections}")
    print("---------------------------------------")
    for plate, count in plate_counts.items():
        print(f" - {plate}: Detected {count} times")
    print("---------------------------------------\n")

import os
if __name__ == "__main__":
    generate_session_report()
