#!/usr/bin/env python3
"""
Run dummysensors using a YAML config.
- If a config is present (config.sensors.yaml | dummysensors.yaml | config.yaml), it will be used.
- If none is found, a minimal default config.sensors.yaml is created and then used.
Outputs:
  - out/temp.jsonl (temperature)
  - out/vibration.csv (vibration)
"""
from __future__ import annotations
import os
from pathlib import Path

try:
    from dummysensors.config import find_config_path, run_from_config
except Exception as e:  # pragma: no cover
    raise SystemExit("dummysensors is not installed. Run: pip install dummysensors[yaml]") from e

DEFAULT_CFG_NAME = "config.sensors.yaml"
DEFAULT_CFG = """
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
""".lstrip()


def ensure_config(cwd: Path) -> str:
    # Try to auto-discover existing config
    found = find_config_path(str(cwd))
    if found:
        print(f"[ds-test] Using existing config: {found}")
        return found
    # Otherwise write a default config.sensors.yaml
    cfg_path = cwd / DEFAULT_CFG_NAME
    cfg_path.write_text(DEFAULT_CFG, encoding="utf-8")
    print(f"[ds-test] Wrote default {cfg_path.name} in {cwd}")
    return str(cfg_path)


def main() -> None:
    cwd = Path.cwd()
    cfg = ensure_config(cwd)
    # Run generator according to YAML
    run_from_config(cfg)
    # Quick pointers for the user
    print("\n[ds-test] Done. Peek at outputs:")
    print("  - out/temp.jsonl (JSON Lines)")
    print("  - out/vibration.csv (CSV)")


if __name__ == "__main__":
    main()
