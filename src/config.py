from dataclasses import dataclass

@dataclass
class Default:
    model: str
    process: str


@dataclass
class Paths:
    raw: str
    processed: str
    final: str
    model: str


@dataclass
class Files:
    raw: str
    processed: str
    final: str
    pipeline: str


@dataclass
class Features:
    used_feature: list[str]
    indep_variables: list[str]
    dep_variables: str


@dataclass
class Thershold:
    category: list[str]
    footage: int
    doorms: int
    garages: int
    price: int


@dataclass
class Models:
    name: str


@dataclass
class Params:
    boosting_type: str
    learning_rate: float
    max_depth: int


@dataclass
class Mlflow:
    experiment: str
    tracking_uri: str


@dataclass
class AppConfig:
    defaults: Default
    paths: Paths
    files: Files
    features: Features
    thresholds: Thershold
    models: Models
    params: Params
