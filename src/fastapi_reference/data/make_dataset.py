import logging


def make_dataset(raw_filepath: str) -> None:
    """Runs data loading scripts that saves new raw data in (../raw).

    Args:
            raw_filepath: directory of output files
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
