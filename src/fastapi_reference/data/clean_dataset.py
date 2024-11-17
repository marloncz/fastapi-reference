import logging


def clean_dataset(input_filepath: str, output_filepath: str) -> None:
    """Clean input data and write it back to output filepath.

    Runs data cleaning scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../interim).

    Args:
            input_filepath: directory of input files
            output_filepath: directory of output files
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
