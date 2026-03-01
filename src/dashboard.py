import json
import tkinter as tk
import datetime

def ts_to_time(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S") if ts else "—"

root = tk.Tk()
root.title("Traffic + Emission Dashboard")
root.geometry("420x300")

title = tk.Label(root, text="Traffic + Emission Estimator", font=("Arial", 16, "bold"))
title.pack(pady=10)

counts_label = tk.Label(root, text="Counts loading...", font=("Arial", 11))
counts_label.pack(pady=5)

co2_label = tk.Label(root, text="CO2 loading...", font=("Arial", 11))
co2_label.pack(pady=5)

level_label = tk.Label(root, text="Emission Level loading...", font=("Arial", 11, "bold"))
level_label.pack(pady=5)

peak_label = tk.Label(root, text="Peak CO2: --", font=("Arial", 11))
peak_label.pack(pady=5)

signal_label = tk.Label(root, text="Recommended Green Signal Time: -- sec", font=("Arial", 11))
signal_label.pack(pady=5)

route_label = tk.Label(root, text="Recommended Route: --", font=("Arial", 11))
route_label.pack(pady=5)

disclaimer = tk.Label(
    root,
    text="Note: CO₂ levels shown are estimates, not sensor-based values.",
    font=("Arial", 9),
    fg="gray"
)
disclaimer.pack(side="bottom", pady=6)

#Live Updates

def update_dashboard():
    try:
        with open("counts.json") as f:
            counts_data = json.load(f)["counts"]

        with open("emission.json") as f:
            emission_data = json.load(f)

        counts_text = (
            f"Cars: {counts_data['car']}   "
            f"Bikes: {counts_data['motorbike']}   "
            f"Buses: {counts_data['bus']}   "
            f"Trucks: {counts_data['truck']}"
        )
        peak_co2 = emission_data.get("peak_co2", 0)
        peak_time = emission_data.get("peak_time", None)
        counts_label.config(text=counts_text)
        co2_label.config(text=f"Estimated CO2/min: {emission_data['co2_per_min']} g")
        level_label.config(text=f"Emission Level: {emission_data['level']}")
        peak_label.config(text=f"Peak CO2/min: {peak_co2} g at {ts_to_time(peak_time)}")
        signal_label.config(text=f"Recommended Green Signal Time: {emission_data.get('recommended_green_time', '--')} sec")
        route_label.config(text=f"Recommended Route: {emission_data.get('recommended_route', '--')}")
    except Exception as e:
        counts_label.config(text="Waiting for data...")
        co2_label.config(text="")
        level_label.config(text="")
        peak_label.config(text="Peak CO2: --")


    root.after(1000, update_dashboard)  # refresh every 1 sec

update_dashboard()
root.mainloop()