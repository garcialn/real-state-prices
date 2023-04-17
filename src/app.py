from typing import Optional

import bentoml
import numpy as np
import pandas as pd
from bentoml.io import JSON, NumpyNdarray
from pydantic import BaseModel, validator


class TypeError(Exception):
    """Error raised when type not listed"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class CityError(Exception):
    """Error raised when city not listed"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class FootageError(Exception):
    """Error raised when footage is not between the threshold values"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class DoormsError(Exception):
    """Error raised when doorms is bigger than threshold value"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class GaragesError(Exception):
    """Error raised when doorms is bigger than threshold value"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


## loading the runner based on the saved model from bento
model_runner = bentoml.sklearn.get("lightgbm_reg:latest").to_runner()

## creating the service based on the runner
svc = bentoml.Service("price_regression", runners=[model_runner])

## using pydantic to verify the features dtypes


class Lightgbm(BaseModel):
    """lightgbm model class"""

    type: str = "Apartamento"
    city: str = "Sao_Paulo"
    footage: int = "80"
    doorms: int = "2"
    garages: int = "1"

    ## optional parameter
    request_id: Optional[int]

    @validator("type")
    @classmethod
    def type_validation(cls, value):
        available_types = ["Apartamento", "Casa", "Cobertura", "Duplex", "Studio"]
        if value not in available_types:
            raise TypeError(
                value=value,
                message="Type of property needs to one of the following:\
                    Apartamento, Casa, Cobertura, Duplex, Studio",
            )
        return value

    @validator("city")
    @classmethod
    def city_validation(cls, value):
        available_cities = [
            "Sao_Paulo",
            "Rio_de_Janeiro",
            "Porto_Alegre",
            "Belo_Horizonte",
        ]
        if value not in available_cities:
            raise CityError(
                value=value,
                message="City of property needs to one of the following:\
                    Sao_Paulo, Rio_de_Janeiro, Porto_Alegre, Belo_Horizonte",
            )
        return value

    @validator("footage")
    @classmethod
    def footage_validation(cls, value):
        if value < 30 | value > 1_000:
            raise FootageError(
                value=value, message="Footage must be between 30m² and 1,000m²"
            )
        return value

    @validator("doorms")
    @classmethod
    def doorms_validation(cls, value):
        if value > 6:
            raise DoormsError(value=value, message="Nº of bedrooms must be less than 6")
        return value

    @validator("garages")
    @classmethod
    def garages_validation(cls, value):
        if value > 6:
            raise GaragesError(
                value=value, message="Nº of garage spots must be less than 6"
            )
        return value


class Config:
    extra = "forbid"


input_spec = JSON(pydantic_model=Lightgbm)


@svc.api(input=input_spec, output=NumpyNdarray())
def price_reg(input_data: Lightgbm) -> np.array:

    """
    Perform the Scikit-Learn Pipeline with Lightgbm Regression Model

    Given the following variables:
        - Type
        - City
        - Footage
        - Doorms nº
        - Garages nº

    You'll get the expected value for it (BR$)
    """

    input_df = pd.DataFrame([input_data.dict(exclude={"request_id"})])
    result = np.round(model_runner.run(input_df), 0)
    return result
