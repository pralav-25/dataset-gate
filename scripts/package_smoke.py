"""Install a wheel into a fresh environment and exercise the core with no API dependencies."""

import argparse
import json
import os
import subprocess
import tempfile
import venv
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    wheel = args.wheel.resolve()
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        venv.EnvBuilder(with_pip=True).create(root / "venv")
        python = root / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-deps", str(wheel)], check=True)
        result = subprocess.run(
            [str(python), "-m", "dataset_gate", "doctor"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        diagnostics = json.loads(result.stdout)
        assert not diagnostics["api_available"]
        data = root / "data.csv"
        data.write_text("id\na\nb")
        contract = root / "contract.json"
        contract.write_text(
            json.dumps(
                {
                    "version": 1,
                    "name": "Wheel smoke",
                    "rules": [{"id": "unique", "check": "unique", "column": "id"}],
                }
            )
        )
        result = subprocess.run(
            [str(python), "-m", "dataset_gate", "validate", str(data), "--contract", str(contract)],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        assert json.loads(result.stdout)["status"] == "passed"
        print("Clean wheel installation: core CLI works without FastAPI")
