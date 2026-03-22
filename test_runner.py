import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pytest
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"

print(f"[test_runner] ENV_PATH = {ENV_PATH}")
print(f"[test_runner] .env exists? {ENV_PATH.exists()}")

if ENV_PATH.exists():
    load_dotenv(ENV_PATH, override=False)
    print(f"[test_runner] Loaded .env from: {ENV_PATH}")
else:
    print(f"[test_runner] WARNING: .env not found at: {ENV_PATH}")

print(f"[test_runner] API_KEY available? {bool(os.getenv('API_KEY'))}")
print(f"[test_runner] API_SECRET available? {bool(os.getenv('API_SECRET'))}")
print(f"[test_runner] ACCOUNT_ID available? {bool(os.getenv('ACCOUNT_ID'))}")
print(f"[test_runner] BASE_URL = {os.getenv('BASE_URL', 'not-set')}")


SUITE_ROOTS = {
    "testSuite": "src/test/aquanow/tests",
}


def get_env_value(key: str, default: str = "not-set") -> str:
    if not ENV_PATH.exists():
        print(f"[Allure env] .env file not found at {ENV_PATH}")
        return default

    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip()
    except Exception as e:
        print(f"[Allure env] Error reading .env: {e}")
        return default

    return default


def write_allure_environment(allure_results_dir: str) -> None:
    os.makedirs(allure_results_dir, exist_ok=True)

    base_url = get_env_value("BASE_URL", "not-set")
    account_id = get_env_value("ACCOUNT_ID", "not-set")
    get_quote_path = get_env_value("GET_QUOTE_PATH", "not-set")
    create_quote_path = get_env_value("CREATE_QUOTE_PATH", "not-set")
    execute_quote_path = get_env_value("EXECUTE_QUOTE_PATH", "not-set")
    expire_quote_path = get_env_value("EXPIRE_QUOTE_PATH", "not-set")
    deliver_quantity = get_env_value("DELIVER_QUANTITY", "not-set")

    print("[Allure env] Values to write:")
    print(f"  BASE_URL           = {base_url}")
    print(f"  ACCOUNT_ID         = {account_id}")
    print(f"  GET_QUOTE_PATH     = {get_quote_path}")
    print(f"  CREATE_QUOTE_PATH  = {create_quote_path}")
    print(f"  EXECUTE_QUOTE_PATH = {execute_quote_path}")
    print(f"  EXPIRE_QUOTE_PATH  = {expire_quote_path}")
    print(f"  DELIVER_QUANTITY   = {deliver_quantity}")

    env_file = os.path.join(allure_results_dir, "environment.properties")
    print(f"[Allure env] Writing environment.properties to: {env_file}")

    with open(env_file, "w", encoding="utf-8") as f:
        f.write(f"base_url={base_url}\n")
        f.write(f"account_id={account_id}\n")
        f.write(f"get_quote_path={get_quote_path}\n")
        f.write(f"create_quote_path={create_quote_path}\n")
        f.write(f"execute_quote_path={execute_quote_path}\n")
        f.write(f"expire_quote_path={expire_quote_path}\n")
        f.write(f"deliver_quantity={deliver_quantity}\n")


def copy_history_from_previous_report(allure_report_root: str, allure_results_dir: str) -> None:
    if not os.path.exists(allure_report_root):
        print("[Allure trend] No previous report root found")
        return

    subdirs = [
        d for d in os.listdir(allure_report_root)
        if os.path.isdir(os.path.join(allure_report_root, d))
    ]
    if not subdirs:
        print("[Allure trend] No previous report directories found")
        return

    subdirs.sort()
    latest_dir = os.path.join(allure_report_root, subdirs[-1])
    prev_history = os.path.join(latest_dir, "history")
    dest_history = os.path.join(allure_results_dir, "history")

    if os.path.exists(prev_history):
        if os.path.exists(dest_history):
            shutil.rmtree(dest_history)
        shutil.copytree(prev_history, dest_history)
        print(f"[Allure trend] Copied history from {prev_history} to {dest_history}")
    else:
        print("[Allure trend] No history folder found in latest report")


def run_tests(
    suite: str = "smoke",
    files: Optional[List[str]] = None,
    *,
    open_report: bool = False,
    auto_close_seconds: int = 180,
) -> int:
    if suite not in SUITE_ROOTS:
        raise ValueError(f"Unknown suite '{suite}'. Available: {list(SUITE_ROOTS.keys())}")

    suite_root = SUITE_ROOTS[suite]
    suite_root_path = PROJECT_ROOT / suite_root

    if files is None:
        test_targets = [str(suite_root_path)]
    else:
        test_targets = []
        for f in files:
            f_rel = f.lstrip(os.sep)
            test_targets.append(str(suite_root_path / f_rel))

    now = datetime.now()
    date_folder = now.strftime("%Y-%m-%d")
    time_folder = now.strftime("%H-%M-%S")
    timestamp = f"{date_folder}_{time_folder}"

    allure_results_dir_root = os.path.join("allure-results", suite)
    allure_results_dir = os.path.join(allure_results_dir_root, timestamp)

    allure_report_root = os.path.join("reports", "allure", suite)
    allure_report_dir = os.path.join(allure_report_root, timestamp)

    html_reports_root = os.path.join("reports", "html")
    html_report_filename = f"{suite}_{date_folder}_{time_folder}.html"
    html_report_path = os.path.join(html_reports_root, html_report_filename)

    os.makedirs(allure_results_dir, exist_ok=True)
    os.makedirs(allure_report_dir, exist_ok=True)
    os.makedirs(html_reports_root, exist_ok=True)

    copy_history_from_previous_report(allure_report_root, allure_results_dir)
    write_allure_environment(allure_results_dir)

    pytest_args = [
        *test_targets,
        "-s",
        "-vv",
        "--tb=long",
        "--alluredir",
        allure_results_dir,
        "--html",
        html_report_path,
        "--self-contained-html",
    ]

    print(f"\n=== Running suite: {suite} ===")
    print(f"Test targets: {test_targets}")
    print(f"Allure results: {allure_results_dir}")
    print(f"Allure report : {allure_report_dir}")
    print(f"HTML report   : {html_report_path}\n")

    exit_code = pytest.main(pytest_args)

    print(f"Pytest finished with exit code: {exit_code}\n")

    try:
        subprocess.run(
            ["allure", "generate", allure_results_dir, "-o", allure_report_dir, "--clean"],
            check=True,
        )

        index_path = os.path.abspath(os.path.join(allure_report_dir, "index.html"))
        print("\n==============================")
        print("    ALLURE REPORT READY")
        print("==============================")
        print(f"{index_path}\n")

        print("==============================")
        print(" SINGLE-FILE HTML REPORT READY")
        print("==============================")
        print(f"{os.path.abspath(html_report_path)}\n")

        if open_report:
            print(f"Opening Allure report for {auto_close_seconds} seconds...\n")
            proc = subprocess.Popen(["allure", "open", allure_report_dir])

            import time
            time.sleep(auto_close_seconds)

            proc.terminate()
            print("Allure server stopped automatically.\n")

    except FileNotFoundError:
        print("\nERROR: 'allure' command not found. Install Allure CLI and add it to PATH.\n")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR generating Allure report: {e}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_tests())