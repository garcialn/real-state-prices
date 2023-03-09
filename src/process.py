import logging

import hydra
import pandas as pd
import polars as pl
from hydra.core.config_store import ConfigStore
from sklearn.preprocessing import OrdinalEncoder

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
    logging.info(f"Data to be loaded: {raw_path}")

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

    logging.warning(
        f"Dataframe created with success using the following features: {df.columns}"
    )

    ## pre-processing data

    logging.info("Start data processing")

    df = (
        df.drop("address")
        .drop_nulls()
        .with_columns(
            [
                ((pl.col(cfg.process.features.used_features[0])).cast(pl.Categorical)),
                ((pl.col(cfg.process.features.used_features[1])).cast(pl.Categorical)),
                ((pl.col(cfg.process.features.used_features[2])).cast(pl.Int16)),
                ((pl.col(cfg.process.features.used_features[3])).cast(pl.Int8)),
                ((pl.col(cfg.process.features.used_features[4])).cast(pl.Int8)),
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

    logging.warning("First pre-processing done")

    proccessed_path = f"{cfg.paths.processed}{cfg.files.processed}"
    df.write_parquet(f"{proccessed_path}")
    logging.warning(f"Processed {df} saved with success")

    logging.info("Final part of pre-processing")

    ## defining X and y to use on models

    y = df["price"].to_pandas()
    X1 = df.drop(columns=["price"]).to_pandas()

    ## using OrdinalEncoder

    ord_enc = OrdinalEncoder()
    X2 = ord_enc.fit_transform(X1[["city", "type"]])
    X2 = pd.DataFrame(X2, columns=["location", "category"])
    X3 = X1.join(X2).drop(["city", "type"], axis=1)
    X3 = (
        pl.DataFrame(X3)
        .select(["location", "category", "footage", "doorms", "garages"])
        .to_pandas()
    )

    ## transforming the dtypes

    df = pl.from_pandas(X3.join(y)).with_columns(
        [
            (pl.col("location").cast(pl.Int8)),
            (pl.col("category").cast(pl.Int8)),
            (pl.col("footage").cast(pl.Float32)),
            (pl.col("doorms").cast(pl.Int8)),
            (pl.col("garages").cast(pl.Int8)),
            (pl.col("price").cast(pl.Int32)),
        ]
    )

    y = pl.DataFrame(df["price"])
    X = df.drop(columns=["price"])

    X_path = f"{cfg.paths.final}{cfg.files.final.X}"
    y_path = f"{cfg.paths.final}{cfg.files.final.y}"

    X.write_parquet(f"{X_path}")
    y.write_parquet(f"{y_path}")

    logging.warning(
        f"X and y defined with success and saved. \
        Independent Variables: {X.columns} \
        Dependent Variable {y.columns}"
    )

    print(df, df.describe())

    logging.warning("All processing done with success!")
    return df


if __name__ == "__main__":
    process_data()
