## Example application: live plotting & logging

This is a **test project for my [`dummysensors`](https://github.com/SculptTechProject/dummysensors) package**, showing how to run it in a standalone repo to simulate engine data, plot it live, and save it for later analysis.

### How to run (YAML config — recommended)

`dummysensors` auto-discovers a config file named `config.sensors.yaml` in the current directory.

1. Clone:

   ```bash
   git clone https://github.com/SculptTechProject/ds-test
   cd ds-test
   ```
2. Create venv and install deps:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3.1. Run generator (autodetection picks up `config.sensors.yaml`):

   ```bash
   dummy-sensors run
   ```

3.2. Run generator via yaml config by providing file:

   ```bash
   dummy-sensors run --config config.sensors.yaml
   ```

   Outputs:

   * `out/temp.jsonl` (temperature, JSONL)
   * `out/vibration.csv` (vibration, CSV)

#### Example `config.sensors.yaml`

```yaml
rate: 2
count: 20
partition_by: type

outputs:
  - type: jsonl
    for: temp
    path: out/temp.jsonl
  - type: csv
    for: vibration
    path: out/vibration.csv

devices:
  - id: engine-A
    sensors:
      - kind: temp
        count: 1
      - kind: vibration
        count: 1
```

---

### How to run (live plot via `main.py`)

1. After installing requirements:

   ```bash
   python main.py
   ```
2. You will see a **live matplotlib plot** (temperature + vibration) and a log file:

   * `out.jsonl` (JSON Lines with snapshots of temp+vibration)

#### Live plot + JSONL logging (excerpt from `main.py`)

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
        record_temp = {"ts": t, "device_id": "engine-A", "sensor_id": "temp-0", "type": "temperature", "value": temp.read()}
        record_vib  = {"ts": t, "device_id": "engine-A", "sensor_id": "vib-0",  "type": "vibration",  "value": vib.read(t)}
        f.write(json.dumps(record_temp) + "\n")
        f.write(json.dumps(record_vib) + "\n")
```

---

### Analysis with Pandas

```python
import pandas as pd
import matplotlib.pyplot as plt

# From YAML run
temp = pd.read_json("out/temp.jsonl", lines=True)
vib  = pd.read_csv("out/vibration.csv")
print("Avg temp:", temp["value"].mean())
print("Avg vibration:", vib["value"].mean())

fig, axes = plt.subplots(2, 1, figsize=(8, 6))
axes[0].plot(temp["ts_ms"]/1000.0, temp["value"], color="red"); axes[0].set_ylabel("Temp (°C)")
axes[1].plot(vib["ts_ms"]/1000.0, vib["value"], color="blue"); axes[1].set_ylabel("Vibration"); axes[1].set_xlabel("Time (s)")
plt.tight_layout(); plt.show()
```

### What will you see?

<img width="790" height="657" alt="image" src="https://github.com/user-attachments/assets/132a7800-9c51-4ae5-93f9-7327382fd806" /> 

>Live plot

<img width="785" height="559" alt="image" src="https://github.com/user-attachments/assets/4f22a680-b81f-49e6-ab01-3d7424335ceb" />

```bash
=== Head of dataframe ===
ts device_id sensor_id         type      value
0  0.0  engine-A    temp-0  temperature  84.620850
1  0.0  engine-A     vib-0    vibration   0.179118
2  0.5  engine-A    temp-0  temperature  76.254692
3  0.5  engine-A     vib-0    vibration   0.166054
4  1.0  engine-A    temp-0  temperature  76.256331

Average values by type:
type
temperature    76.844964
vibration      -0.017095
Name: value, dtype: float64

```
> Analysis with Pandas

---

This demo shows both modes: **YAML config** for reproducible runs and **interactive `main.py`** for quick exploration.
