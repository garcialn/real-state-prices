import pickle

import bentoml
import hydra
from hydra.core.config_store import ConfigStore
from lightgbm import LGBMRegressor
from loguru import logger
from sklearn.pipeline import Pipeline

from config import AppConfig

# cs = ConfigStore.instance()
# cs.store(name="app_config", node=AppConfig)

# @hydra.main(version_base=None, config_path="../config", config_name="main")
# def get_pipe(cfg: AppConfig) -> Pipeline:

#     '''
#         Get the sklearn Pipeline Object
#     '''

#     pipe_file = f'{cfg.paths.model}{cfg.files.pipeline}'
#     with open(pipe_file, 'rb') as f:
#         model = pickle.load(f)

#     logger.warning(f'Pipeline Object imported successfully from: {pipe_file}')
#     return model

# model = get_pipe()

model = bentoml.sklearn.load_model("lightgbm_reg:latest")
