import logging

import hydra
import polars as pl
import pydantic
from hydra.utils import to_absolute_path as abspath
from omegaconf import DictConfig


class Dataset(pydantic.BaseModel):

    city: str
    category: str
    footage: int
    doorms: int
    garages: int
    price: int


@hydra.main(config_path="../config/", config_name="main")
def get_data(config: DictConfig) -> pl.DataFrame:

    """
    Load the data into the working environment for later processing
    """

    raw_path = abspath(config.raw.path)
    logging.info(f"Using raw data: {raw_path}")

    df = pl.read_parquet(
        raw_path,
        columns=[
            "categoty",
            "city",
            "address",
            "footage",
            "doorms",
            "garages",
            "price",
        ],
    )

    logging.warning("df created with sucesses")

    return df


@hydra.main(config_path="../config", config_name="process")
def process_data(config: DictConfig) -> pl.DataFrame:

    """
    Pre-processing and processing the data for model development:
    - Extract the data from the source
    - Load the data into the envirement
    - Clean the data
    - Prepare the data
    """

    df = get_data(config)

    df = (
        df.drop("address")
        .drop_nulls()
        .with_columns(
            (pl.col("category") == config.outliers_thershold.type[0])
            | (pl.col("category") == config.outliers_thershold.type[1])
            | (pl.col("category") == config.outliers_thershold.type[2])
            | (pl.col("category") == config.outliers_thershold.type[3])
            | (pl.col("category") == config.outliers_thershold.type[4])
        )
        .with_columns(
            [
                (pl.col(config.use_features[1]).cast(pl.Categorical)),
                (pl.col(config.use_features[0]).cast(pl.Categorical)),
                (pl.col(config.use_features[2]).cast(pl.Int16)),
                (pl.col(config.use_features[3]).cast(pl.Int8)),
                (pl.col(config.use_features[4]).cast(pl.Int8)),
                (pl.col(config.use_features[5]).cast(pl.Int32)),
            ]
        )
        .filter(
            (pl.col(config.use_features[5]) <= config.outliers_thershold.price)
            & (pl.col(config.use_features[2]) <= config.outliers_thershold.footage)
            & (pl.col(config.use_features[3]) <= config.outliers_thershold.doorms)
            & (pl.col(config.use_features[4]) <= config.outliers_thershold.garages)
        )
    )

    logging.info(f"Features: {config.use_features}")

    return df


if __name__ == "__main__":
    process_data()
