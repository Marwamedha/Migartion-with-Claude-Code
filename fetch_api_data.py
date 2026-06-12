"""
Fetch CSV data from APIs and save to timestamped directories with logging.
"""

import asyncio
import httpx
import logging
from pathlib import Path
from datetime import datetime


async def fetch_data_from_apis() -> None:
    """
    Fetch CSV data from GitHub URLs using async httpx and save with logging.
    """
    # API URLs to fetch
    urls = [
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
    ]

    # Create timestamp for directory naming
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Setup data directory
    data_dir = Path(".claude/skills/fetchAPI/data") / timestamp
    data_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging directory
    log_dir = Path(".claude/skills/fetchAPI/logs") / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging
    log_file = log_dir / "fetchAPI.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger(__name__)

    logger.info("Starting API data fetch process")
    logger.info(f"Data directory: {data_dir}")
    logger.info(f"Log directory: {log_dir}")

    # Fetch data from all URLs
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [fetch_and_save_csv(client, url, data_dir, logger) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Summary
    successful = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False or isinstance(r, Exception))
    logger.info(f"Fetch complete: {successful} successful, {failed} failed")


async def fetch_and_save_csv(
    client: httpx.AsyncClient, url: str, data_dir: Path, logger: logging.Logger
) -> bool:
    """
    Fetch a single CSV file and save it.

    Args:
        client: AsyncClient instance
        url: URL to fetch from
        data_dir: Directory to save the file
        logger: Logger instance

    Returns:
        True if successful, False otherwise
    """
    filename = url.split("/")[-1]
    file_path = data_dir / filename

    try:
        logger.info(f"Fetching {filename} from {url}")
        response = await client.get(url)
        response.raise_for_status()

        # Save the file
        file_path.write_text(response.text)
        logger.info(f"Successfully saved {filename} ({len(response.content)} bytes)")
        return True

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {filename}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error fetching {filename}: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(fetch_data_from_apis())
