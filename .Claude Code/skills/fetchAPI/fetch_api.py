import asyncio
from datetime import datetime
from pathlib import Path
import logging

import httpx

URLS = [
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Calendar.csv",
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Customers.csv",
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Products.csv",
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Sales_2015.csv",
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Sales_2017.csv",
    "https://raw.githubusercontent.com/Marwamedha/Azure-data-engineering/refs/heads/main/Data/AdventureWorks_Returns.csv",
]

SKILL_BASE = Path(__file__).resolve().parent
DATA_BASE = SKILL_BASE / ".claude" / "skills" / "fetchAPI" / "data"
LOG_BASE = SKILL_BASE / ".claude" / "skills" / "fetchAPI" / "logs"


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def setup_logger(log_file: Path) -> logging.Logger:
    logger = logging.getLogger("fetchAPI")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


async def fetch_url(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> tuple[str, bool, str]:
    try:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        logger.info("Fetched %s successfully", url)
        return url, True, response.text
    except Exception as exc:
        logger.error("Failed to fetch %s: %s", url, exc)
        return url, False, str(exc)


async def fetch_all(urls: list[str], logger: logging.Logger) -> list[tuple[str, bool, str]]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url, logger) for url in urls]
        return await asyncio.gather(*tasks)


def save_response(content: str, output_dir: Path, url: str, logger: logging.Logger) -> None:
    filename = Path(url).name
    output_file = output_dir / filename
    output_file.write_text(content, encoding="utf-8")
    logger.info("Saved %s to %s", filename, output_file)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


async def main() -> None:
    timestamp = get_timestamp()
    data_dir = ensure_dir(DATA_BASE / timestamp)
    log_dir = ensure_dir(LOG_BASE / timestamp)
    log_file = log_dir / "fetchAPI.log"

    logger = setup_logger(log_file)
    logger.info("Starting fetchAPI run")
    logger.info("Saving data to %s", data_dir)
    logger.info("Saving logs to %s", log_file)

    results = await fetch_all(URLS, logger)

    for url, success, payload in results:
        if success:
            save_response(payload, data_dir, url, logger)
        else:
            logger.warning("Skipping save for %s because fetch failed", url)

    logger.info("fetchAPI run completed")


if __name__ == "__main__":
    asyncio.run(main())
