import os
import subprocess
import sys
from pathlib import (
    Path,
)
from typing import (
    Final,
)

SCRIPTS_ROOT: Final[Path] = Path(__file__).parent  # current directory
PYTHON_PATH: Final[Path] = Path(os.getenv("PYTHONPATH", "/app"))

RELATIVE_ROOT: Final[Path] = SCRIPTS_ROOT.relative_to(PYTHON_PATH)
EXCLUDED_NAMES: Final[set[str]] = {"all", "__init__"}
TIMEOUT: Final[float] = 5  # seconds


def run_health_check(script_name: str) -> bool:
    """
    Run the health check script in another process.

    Parameters
    ----------
    script_name : str
        script name

    Returns
    -------
    bool
        status code
    """
    try:
        result = subprocess.run(
            args=[
                sys.executable,
                "-m",
                str(RELATIVE_ROOT / script_name).replace("/", "."),
            ],
            stdout=sys.stdout,
            stderr=sys.stderr,
            timeout=TIMEOUT,
            env=os.environ,
        )
    except subprocess.TimeoutExpired:
        print(f"⚠️ {script_name.upper()}: Timeout ({TIMEOUT} seconds)")
    except Exception as e:
        print(f"⚠️ {script_name.upper()}: Launch error - {e!s}")
    else:
        return result.returncode == 0

    return False


def check_connections() -> tuple[bool, str]:
    """
    Run all health checks.

    Returns
    -------
    tuple[bool, str]
        status, message
    """
    health_checks = [
        script for script in SCRIPTS_ROOT.glob("*.py") if script.stem not in EXCLUDED_NAMES
    ]
    num_health_checks = len(health_checks)

    if num_health_checks == 0:
        return False, "⚠️ There are no health check scripts"

    print(f"📋 {num_health_checks} health check script(s) found:\n")

    results: list[bool] = []
    messages = ["Summary:"]

    for i, script_path in enumerate(health_checks, start=1):
        print(f"{i}/{num_health_checks}:", end=" ")

        script_name = script_path.stem
        ok = run_health_check(script_name)
        results.append(ok)
        messages.append(
            f"{i}. {script_name.title():<10} - {'✅ Running' if ok else '❌ Failed'}",
        )

        print("\n--------------------------------")

    print("\nAll health checks have been completed\n")
    return all(results), "\n".join(messages)


if __name__ == "__main__":
    print("🏥 Health check...")

    try:
        ok, msg = check_connections()
    except Exception as e:
        ok, msg = False, f"❌ Health check failed:\n{e!s}"

    print(msg)
    sys.exit(not ok)
