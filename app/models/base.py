from collections.abc import Iterable

import pydantic


class BaseModel(pydantic.BaseModel):

    @classmethod
    def from_iterable(cls, values: Iterable):
        fields = cls.model_fields
        return cls(**dict(zip(fields, values)))
