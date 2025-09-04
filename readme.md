## Example application: live plotting & logging

This demo shows how to run `dummysensors` in a standalone project to simulate engine data, plot it live, and save it to a JSONL file for later analysis.

### How to run

1. Clone this repo (or copy `main.py` to your project):
   ```bash
   git clone https://github.com/SculptTechProject/ds-test
   cd ds-test
   ```
2. Create a virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Run the demo:
   ```bash
   python main.py
   ```

This will:

* Show a **live matplotlib plot** of temperature and vibration
* Write JSONL logs to `out.jsonl`
* Print progress to the console

---

### Live plot + JSONL logging

```python
import time, json
import matplotlib.pyplot as plt
from dummysensors import TemperatureSensor, VibrationSensor

# create sensors
temp = TemperatureSensor(min_val=70, max_val=90, noise=0.5)
vib  = VibrationSensor(base_hz=20, amp=2.0, noise=0.2)

# live plotting
temps, vibs, times = [], [], []
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

for i in range(50):
    t = i * 0.2
    times.append(t)
    temps.append(temp.read())
    vibs.append(vib.read(t))
    ax1.clear(); ax2.clear()
    ax1.plot(times, temps, color="red"); ax1.set_ylabel("Temperature (°C)")
    ax2.plot(times, vibs, color="blue"); ax2.set_ylabel("Vibration signal"); ax2.set_xlabel("Time (s)")
    plt.pause(0.1); time.sleep(0.2)

plt.ioff(); plt.show()

# JSONL logging
with open("out.jsonl", "w", encoding="utf-8") as f:
    for i in range(20):
        t = round(i * 0.5, 2)
        record_temp = {
            "ts": t, "device_id": "engine-A", "sensor_id": "temp-0",
            "type": "temperature", "value": temp.read()
        }
        record_vib = {
            "ts": t, "device_id": "engine-A", "sensor_id": "vib-0",
            "type": "vibration", "value": vib.read(t)
        }
        f.write(json.dumps(record_temp) + "\n")
        f.write(json.dumps(record_vib) + "\n")
```

### Analysis with Pandas

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_json("out.jsonl", lines=True)
print(df.groupby("type")["value"].mean())

df.pivot(index="ts", columns="type", values="value").plot(subplots=True)
plt.show()
```

This demo produces both a live plot while generating data, and later an offline analysis from the JSONL log.

