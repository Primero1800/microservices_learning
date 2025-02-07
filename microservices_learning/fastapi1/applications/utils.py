import inspect
import re
from typing import Set, Any

from pydantic import BaseConfig
from pydantic.v1.fields import ModelField, Undefined


def get_path_param_names(path: str) -> Set[str]:
    return set(re.findall("{(.*?)}", path))


def get_param_field(param: inspect.Parameter, param_name: str) -> ModelField:
    default_value: Any = Undefined
    if not param.default == param.empty:
        default_value = param.default
        required = True
    if default_value is not Undefined:
        required = False
    annotation: Any = Any
    if not param.annotation == param.empty:
        annotation = param.annotation
    field = ModelField(
        name=param_name,
        type_=annotation,
        default=default_value,
        class_validators=None,
        required=required,
        model_config=BaseConfig,
    )
    return field
