from collections.abc import Iterable

import pydantic
from pydantic import field_validator


class BaseModel(pydantic.BaseModel):

    @classmethod
    def from_iterable(cls, values: Iterable):
        if values:
            fields = cls.model_fields
            return cls(**dict(zip(fields, values)))

    @field_validator(
        'created_at', 'updated_at',
        check_fields=False,
        mode='before'
    )
    def format_timestamps(cls, v):
        return str(v) if v else None
