import subprocess, sys

from datetime import datetime
from pathlib import Path

# project root dir: project_footprint_calculation
PROJECT_ROOT = Path(__file__).resolve().parents[4] # find the root directory
# program-running dir
SCRAPY_PROJECT_DIR = PROJECT_ROOT / "src"/ "pipeline" / "extract" / "scrapy_app_icook"
# file-saved dir
DATA_DIR = PROJECT_ROOT / "data" / "daily"

KEYWORD = "latest"

def run_scrapy():
    print(f"Processing...")
    # create data dir
    output_dir = DATA_DIR / f"Created_on_{datetime.today().date()}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # output file path
    output_file_path = output_dir / f"icook_recipe_{datetime.today().date()}.csv"

    # execute scrapy
    command = [
        "scrapy", "crawl", "icook_daily",
        "-a", f"keyword={KEYWORD}",
        "-O", str(output_file_path)
    ]

    print(f"[INFO] Start processing...")
    print(f"[INFO] Output: {output_file_path}")

    try:
        subprocess.run(
            args=command,
            cwd=SCRAPY_PROJECT_DIR,
            check=True,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        print(f"[SUCCESS] Completed!")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed!")
        print(e.stderr)


def main():
    """
    Update the latest recipe from icook daily.
    This program will automatically be activated to retrieve the yesterday data
    """
    run_scrapy()


if __name__ == "__main__":
    main()