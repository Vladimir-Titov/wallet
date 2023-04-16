from typing import List, Type, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

scope = {}


def get_annotation(model):
    parent_models: List[Type] = [
        parent_model for parent_model in getattr(model, '__bases__')
        if (
            issubclass(parent_model, BaseModel)
            and hasattr(parent_model, '__annotations__')
        )
    ]

    annotations = {}

    for parent_model in reversed(parent_models):
        annotations.update(get_annotation(parent_model))

    annotations.update(model.__annotations__)

    return {k: v for k, v in annotations.items()}


def get_attributes(model):
    parent_models = [parent for parent in getattr(model, '__bases__') if (issubclass(parent, BaseModel))]
    attrs = {}

    for parent_model in reversed(parent_models):
        attrs.update(get_attributes(parent_model))

    attrs.update({k: v for k, v in model.__dict__.items() if not k.startswith('__')})
    return {k: v for k, v in attrs.items()}


def partial(cls: T) -> T:
    name = f'{cls.__name__}.partial'
    if name not in scope:
        attributes = {
            '__module__': cls.__module__,
            '__annotations__': {k: Optional[v] for k, v in get_annotation(cls).items()},
        }
        scope[name] = type(name, (cls,), attributes)
    return scope[name]


def only(*fields, model: T = None) -> T:
    def dec(cls: T) -> Type[T]:
        name = f'{cls.__name__}.only{fields}'
        if name not in scope:
            attributes = {k: v for k, v in get_attributes(cls).items() if k in fields}
            attributes.update({
                '__module__': cls.__module__,
                '__annotations__': {k: v for k, v in get_annotation(cls).items() if k in fields},
            })
            scope[name] = type(name, (BaseModel,), attributes)
        return scope[name]

    return dec(model) if model else dec


def exclude(*fields, model: T = None) -> T:
    def dec(cls: T) -> Type[T]:
        name = f'{cls.__name__}.exclude{fields}'
        if name not in scope:
            attributes = {k: v for k, v in get_attributes(cls).items() if k not in fields}
            attributes.update({
                '__module__': cls.__module__,
                '__annotations__': {k: v for k, v in get_annotation(cls).items() if k not in fields},
            })
            scope[name] = type(name, (BaseModel,), attributes)
        return scope[name]

    return dec(model) if model else dec
