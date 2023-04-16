from typing import Optional, Type, Any, Sequence, List, Union, Dict, Set

from fastapi import params
from fastapi.datastructures import DefaultPlaceholder, Default
from fastapi.encoders import SetIntStr, DictIntStrAny
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute

from fastapi_utils.types import ErrRespModel


def view(
    response_model: Optional[Type[Any]] = Dict,
    status_code: Optional[int] = None,
    tags: Optional[List[str]] = None,
    dependencies: Optional[Sequence[params.Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    methods: Optional[Union[Set[str], List[str]]] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse),
    name: Optional[str] = None,
    route_class_override: Optional[Type[APIRoute]] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
):
    def _route(func) -> dict:
        _responses = responses or {}
        _responses = {**_responses, **{422: {'model': ErrRespModel}}}

        return {
            'endpoint': func,
            'response_model': response_model,
            'status_code': status_code,
            'tags': tags,
            'dependencies': dependencies,
            'summary': summary,
            'description': description,
            'response_description': response_description,
            'responses': _responses,
            'deprecated': deprecated,
            'methods': methods,
            'operation_id': operation_id,
            'response_model_include': response_model_include,
            'response_model_exclude': response_model_exclude,
            'response_model_by_alias': response_model_by_alias,
            'response_model_exclude_unset': response_model_exclude_unset,
            'response_model_exclude_defaults': response_model_exclude_defaults,
            'response_model_exclude_none': response_model_exclude_none,
            'include_in_schema': include_in_schema,
            'response_class': response_class,
            'name': name,
            'route_class_override': route_class_override,
            'callbacks': callbacks,
            'openapi_extra': openapi_extra,
        }

    return _route