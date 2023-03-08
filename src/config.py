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


@dataclass
class FIles:
    raw: str
    processed: str
    final: str


@dataclass
class Features:
    used_feature: str
    indep_variables: str
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
class AppConfig:
    defaults: Default
    paths: Paths
    files: FIles
    features: Features
    thresholds: Thershold
    models: Models
    params: Params
