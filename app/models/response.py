from __future__ import annotations

import uuid
from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

ResponseContent = TypeVar("ResponseContent")


class Response(GenericModel, Generic[ResponseContent]):
    success: bool = Field(..., alias="result")
    error_description: str | None = Field(None, alias="errorDesc")
    request_id: str = Field(
        alias="requestId", default_factory=lambda: str(uuid.uuid4())
    )
    data: ResponseContent

    @classmethod
    def error_response(
        cls,
        error_description: str | None = None,
        data: ResponseContent | None = None,
    ) -> Response[ResponseContent]:
        return cls(
            result=False,
            errorDesc=error_description,
            requestId=str(uuid.uuid4()),
            data=data,
        )

    @classmethod
    def success_response(
        cls, data: ResponseContent | None = None
    ) -> Response[ResponseContent]:
        return cls(
            result=True,
            data=data,
            errorDesc=None,
            requestId=str(uuid.uuid4()),
        )
