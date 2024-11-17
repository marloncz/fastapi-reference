import logging


def build_features(input_filepath: str, output_filepath: str) -> None:
    """Build features for input data and save results.

    Runs feature building scripts to turn clean data from (../interim) into
    processed data ready to be fed into a model.

    Args:
        input_filepath: directory of input files
        output_filepath: directory of output files
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
