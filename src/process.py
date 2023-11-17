import hydra
import polars as pl
from hydra.core.config_store import ConfigStore
from loguru import logger

from config import AppConfig

cs = ConfigStore.instance()
cs.store(name="app_config", node=AppConfig)


@hydra.main(version_base=None, config_path="../config", config_name="main")
def process_data(cfg: AppConfig) -> pl.DataFrame:

    """
    Load the data into the working environment for later processing

    Pre-processing and processing the data for model development:
    - Extract the data from the source
    - Load the data into the envirement
    - Clean the data
    - Prepare the data
    """
    
    ## geting the data from the file
    raw_path = f"{cfg.paths.raw}{cfg.files.raw}"
    logger.info(f"Data to be loaded: {raw_path}")

    df = pl.read_parquet(
        raw_path,
        columns=[
            "type",
            "city",
            "address",
            "footage",
            "doorms",
            "garages",
            "price",
        ],
    )

    logger.warning(
        f"Dataframe created with success using the following features: {df.columns}"
    )

    ## pre-processing data
    logger.info("Start data processing")

    df = (
        df.drop("address")
        .drop_nulls()
        .with_columns(
            [
                ((pl.col(cfg.process.features.used_features[0])).cast(pl.Categorical)),
                ((pl.col(cfg.process.features.used_features[1])).cast(pl.Categorical)),
                ((pl.col(cfg.process.features.used_features[2])).cast(pl.Int16)),
                ((pl.col(cfg.process.features.used_features[3])).cast(pl.Int16)),
                ((pl.col(cfg.process.features.used_features[4])).cast(pl.Int16)),
                ((pl.col(cfg.process.features.used_features[5])).cast(pl.Int32)),
            ]
        )
        .filter(
            (
                (pl.col(cfg.process.features.indep_variables[1]))
                == cfg.process.thershold.type[0]
            )
            | (
                (pl.col(cfg.process.features.indep_variables[1]))
                == cfg.process.thershold.type[1]
            )
            | (
                (pl.col(cfg.process.features.indep_variables[1]))
                == cfg.process.thershold.type[2]
            )
            | (
                (pl.col(cfg.process.features.indep_variables[1]))
                == cfg.process.thershold.type[3]
            )
            | (
                (pl.col(cfg.process.features.indep_variables[1]))
                == cfg.process.thershold.type[4]
            )
        )
        .filter(
            (
                pl.col(cfg.process.features.used_features[5])
                <= cfg.process.thershold.price
            )
            & (
                pl.col(cfg.process.features.used_features[2])
                <= cfg.process.thershold.footage
            )
            & (
                pl.col(cfg.process.features.used_features[3])
                <= cfg.process.thershold.doorms
            )
            & (
                pl.col(cfg.process.features.used_features[4])
                <= cfg.process.thershold.garages
            )
        )
    )

    logger.warning("First pre-processing done")

    proccessed_path = f"{cfg.paths.processed}{cfg.files.processed}"
    df.write_parquet(f"{proccessed_path}")
    logger.warning("Processed df saved with success")


if __name__ == "__main__":
    process_data()
