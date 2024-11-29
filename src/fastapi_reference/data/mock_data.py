import random
import string
from datetime import datetime, timedelta

import lorem
import polars as pl


def generate_random_name() -> str:
    """Generates a random product name.

    Returns:
        Product name.
    """
    adjectives = ["Amazing", "Cool", "Fancy", "Durable", "Eco", "Modern", "Premium", "Reliable"]
    nouns = ["Laptop", "Phone", "Chair", "Table", "Headset", "Backpack", "Shoes", "Watch"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    version = f"V{random.randint(1, 10)}.{random.randint(0, 9)}"
    return f"{adjective} {noun} {version}"


def generate_random_date(start_date: str = "2020-01-01", end_date: str = "2024-12-31") -> str:
    """Generates a random date between two dates.

    Args:
        start_date: Start date for selection purpose. Defaults to "2020-01-01".
        end_date: End date for selection purpose. Defaults to "2024-12-31".

    Returns:
        Date as string in format "YYYY-MM-DD".
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_date = start + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")


def generate_mock_data(n_samples: int) -> pl.DataFrame:
    """Generates mock data for testing purposes.

    Args:
        n_samples: Number of samples to generate.

    Returns:
        Polars DataFrame with mock data.
    """
    products = [
        {
            "product_id": str(i).zfill(5),
            "product_name": generate_random_name(),
            "product_description": lorem.sentence(),
            "product_category": f"Category {random.choice(string.ascii_uppercase[0:6])}",
            "price": round(random.uniform(5.0, 500.0), 2),
            "stock": random.randint(1, 100),
            "valid_from": generate_random_date("2015-01-01", "2020-01-01"),
            "valid_to": generate_random_date("2020-02-01", "2025-01-01"),
        }
        for i in range(1, n_samples + 1)
    ]
    return pl.DataFrame(products)
