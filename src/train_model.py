import pickle
from posixpath import abspath

import hydra
import polars as pl
from hydra.core.config_store import ConfigStore
from lightgbm import LGBMRegressor
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import AppConfig

cs = ConfigStore.instance()
cs.store(name="app_config", node=AppConfig)


@hydra.main(version_base=None, config_path="../config", config_name="main")
def train(cfg: AppConfig) -> None:

    """
    Get the processed data from path and
    define X (Independent Variable) and y (Dependent Variable)
    """

    logger.info("Training process started")

    input_path = abspath(cfg.paths.processed)
    input_data = cfg.files.processed

    df = pl.read_parquet(f"{input_path}{input_data}")

    logger.warning(f"Imported data from: {input_path}")

    ## defining X and y to use on models

    target = pl.DataFrame(df["price"])
    y = target.clone().to_pandas()
    features = df.drop(columns=["price"])
    X = features.clone().to_pandas()

    final_path = abspath(cfg.paths.final)
    X_path = cfg.files.final.X
    y_path = cfg.files.final.y

    pl.DataFrame(X).write_parquet(f"{final_path}{X_path}")
    pl.DataFrame(y).write_parquet(f"{final_path}{y_path}")

    ## using OneHotEncoder

    logger.warning(f"Files saved on: {final_path}")

    ohe = OneHotEncoder(handle_unknown="ignore")
    X_cat = X.select_dtypes(include=["category"]).columns

    ss = StandardScaler()
    X_num = X.select_dtypes(include=["int16"]).columns

    transformer = ColumnTransformer(
        transformers=[("cat_cols", ohe, X_cat), ("num_cols", ss, X_num)]
    )

    transformer.fit(X)

    logger.warning("Feature transformation done!")

    # Create model the prediction model

    params = cfg.model.params

    lgbm_regressor = LGBMRegressor(**params)

    logger.info("Regressor Model created with success")

    pipe = Pipeline(steps=[("processing", transformer), ("regressor", lgbm_regressor)])

    logger.info("Pipeline created with success")

    pipe.fit(X, y)
    logger.warning("Model trained")

    ## Save model
    model_path = cfg.paths.model
    with open(model_path, "wb") as f:
        pickle.dump(pipe, f)

    logger.warning(f"Model saved at {model_path}")


if __name__ == "__main__":
    train()
