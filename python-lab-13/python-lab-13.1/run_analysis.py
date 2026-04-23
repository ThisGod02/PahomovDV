import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_command(command, *, allow_failure: bool = False, env=None) -> int:
    print(f"$ {' '.join(command)}")
    base_env = os.environ.copy()
    base_env.setdefault("PYTHONUTF8", "1")
    base_env.setdefault("PYTHONIOENCODING", "utf-8")
    if env:
        base_env.update(env)
    result = subprocess.run(command, cwd=ROOT, env=base_env)
    if result.returncode != 0 and not allow_failure:
        raise SystemExit(result.returncode)
    return result.returncode


def main() -> None:
    section("Lab 13.1: SAST with Bandit")

    run_command([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])

    section("Bandit: vulnerable_app.py")
    run_command([sys.executable, "-m", "bandit", "vulnerable_app.py", "-f", "txt"], allow_failure=True)
    run_command([sys.executable, "-m", "bandit", "vulnerable_app.py", "-f", "html", "-o", "bandit_before.html"], allow_failure=True)
    run_command([sys.executable, "-m", "bandit", "vulnerable_app.py", "-f", "json", "-o", "bandit_before.json"], allow_failure=True)

    section("Bandit: secure_app.py")
    run_command([sys.executable, "-m", "bandit", "secure_app.py", "-f", "txt"], allow_failure=True)
    run_command([sys.executable, "-m", "bandit", "secure_app.py", "-f", "html", "-o", "bandit_after.html"], allow_failure=True)
    run_command([sys.executable, "-m", "bandit", "secure_app.py", "-f", "json", "-o", "bandit_after.json"], allow_failure=True)

    section("Pytest")
    env = {"API_KEY": os.environ.get("API_KEY", "test-key-for-tests")}
    run_command([sys.executable, "-m", "pytest", "test_apps.py", "-v"], env=env)

    print()
    print("Artifacts generated:")
    print("- bandit_before.html / bandit_before.json")
    print("- bandit_after.html / bandit_after.json")


if __name__ == "__main__":
    main()
