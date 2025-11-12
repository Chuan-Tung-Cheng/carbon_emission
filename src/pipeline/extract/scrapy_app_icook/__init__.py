import logging
import subprocess, sys

from datetime import datetime
from pathlib import Path

class IcookDailySpider:
    def __init__(self, keyword="latest"):
        # start from the latest part
        self.keyword = keyword
        # project root dir: project_footprint_calculation
        self.project_root = Path(__file__).resolve().parents[4] # find the root directory
        # program-running dir
        self.scapy_project_dir = self.project_root / "src"/ "pipeline" / "extract" / "scrapy_app_icook"
        # file-saved dir
        self.data_dir = self.project_root / "data"/ "daily"
        # create data dir
        self.output_dir = self.data_dir / f"Created_on_{datetime.today().date()}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # output file path
        self.output_file_path = self.output_dir / f"icook_recipe_{datetime.today().date()}.csv"

        # === Logging ===
        log_dir = self.project_root / "logs" / "scrapy"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"icook_{datetime.today().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # 同時輸出到 console（方便在 Airflow log 看）
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized IcookDailySpider with keyword={self.keyword}")


    def run(self):
        command = [
            "scrapy", "crawl", "icook_daily",
            "-a", f"keyword={self.keyword}",
            "-O", str(self.output_file_path)
        ]

        self.logger.info(f"[INFO] Start processing...")
        self.logger.info(f"[INFO] Output: {self.output_file_path}")

        try:
            result = subprocess.run(
                args=command,
                cwd=self.scapy_project_dir,
                check=True,
                text=True,
                stderr = sys.stderr,
            )

            if result.stdout:
                self.logger.info("[SCRAPY STDOUT]")
                self.logger.info(result.stdout)

            if result.stderr:
                self.logger.warning("[SCRAPY STDERR]")
                self.logger.warning(result.stderr)

            self.logger.info(f"[SUCCESS] Scrapy completed successfully.")

        except subprocess.CalledProcessError as e:
            self.logger.info(f"[ERROR] Failed!")
            self.logger.info(e.stderr)

        finally:
            self.logger.info("Scrapy task finished.")
