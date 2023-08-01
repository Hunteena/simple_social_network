import typing
from collections.abc import Iterable

import pydantic
from pydantic import field_validator


class BaseModel(pydantic.BaseModel):

    @classmethod
    def from_iterable(cls, row: Iterable):
        """
        Create an instance of a class from the iterable with fields values in proper order.
        For nested models the iterable should be flattened.
        Example:
            class User(BaseModel):
                id: int
                name: str

            class Post(BaseModel):
                id: int
                author: User
                text: str

        Post.from_iterable([<post id>, <user id>, <user name>, <text>])
        """
        if not row:
            return None

        row_iter = iter(row)
        mapping = {}

        for field, field_info in cls.model_fields.items():
            field_type = field_info.annotation
            if typing.get_origin(field_type) is typing.Union:
                field_type = typing.get_args(field_type)[0]
            if issubclass(field_type, BaseModel):
                field_values = [
                    next(row_iter)
                    for _ in range(len(field_type.model_fields))
                ]
                mapping[field] = field_type.from_iterable(field_values)
            else:
                mapping[field] = next(row_iter)
        return cls(**mapping)

    @field_validator(
        'created_at', 'updated_at',
        check_fields=False,
        mode='before'
    )
    def format_timestamps(cls, v):
        return str(v) if v else None
