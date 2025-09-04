import time
import json
import matplotlib.pyplot as plt
from dummysensors import TemperatureSensor, VibrationSensor
import pandas as pd

# create sensors
temp = TemperatureSensor(min_val=70, max_val=90, noise=0.5)
vib = VibrationSensor(base_hz=20, amp=2.0, noise=0.2)

# storage
temps = []
vibs = []
times = []

plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

for i in range(50):  # 50 samples
    t = i * 0.2
    times.append(t)
    temps.append(temp.read())
    vibs.append(vib.read(t))

    # live plot
    ax1.clear()
    ax2.clear()
    ax1.plot(times, temps, color="red")
    ax1.set_ylabel("Temperature (°C)")
    ax2.plot(times, vibs, color="blue")
    ax2.set_ylabel("Vibration signal")
    ax2.set_xlabel("Time (s)")

    plt.pause(0.1)
    time.sleep(0.2)

plt.ioff()
plt.show()


with open("out.jsonl", "w", encoding="utf-8") as f:
    for i in range(20):
        t = round(i * 0.5, 2)
        record_temp = {
            "ts": t,
            "device_id": "engine-A",
            "sensor_id": "temp-0",
            "type": "temperature",
            "value": temp.read(),
        }
        record_vib = {
            "ts": t,
            "device_id": "engine-A",
            "sensor_id": "vib-0",
            "type": "vibration",
            "value": vib.read(t),
        }
        # write as JSON lines
        f.write(json.dumps(record_temp) + "\n")
        f.write(json.dumps(record_vib) + "\n")
        print("wrote sample", i)
        time.sleep(0.2)

# read JSONL into pandas dataframe
df = pd.read_json("out.jsonl", lines=True)

print("\n=== Head of dataframe ===")
print(df.head())

# analysis
print("\nAverage values by type:")
print(df.groupby("type")["value"].mean())

# simple plot
df.pivot(index="ts", columns="type", values="value").plot(subplots=True, figsize=(8,5))
plt.show()

print("Done")