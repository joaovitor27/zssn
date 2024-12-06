from typing import Any, List

from django.db.models import QuerySet
from ninja import Schema, Field
from ninja.conf import settings
from ninja.pagination import  AsyncPaginationBase


class CustomPagination(AsyncPaginationBase):
    def __init__(self, page_size: int = settings.PAGINATION_PER_PAGE, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.page_size = page_size
        self.max_page_size = 100

    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(10, ge=1, le=100)

    class Output(Schema):
        results: List[Any]
        count: int
        page_size: int

    items_attribute = "results"


    def paginate_queryset(
            self,
            queryset: QuerySet,
            pagination: Input,
            **params: Any,
    ) -> Any:
        if pagination.page_size:
            if pagination.page_size > self.max_page_size:
                self.page_size = self.max_page_size
            else:
                self.page_size = pagination.page_size
        offset = (pagination.page - 1) * self.page_size
        return {
            "results": queryset[offset : offset + self.page_size],
            "count": self._items_count(queryset),
            "page_size": self.page_size,
        }

    async def apaginate_queryset(
                self,
                queryset: QuerySet,
                pagination: Input,
                **params: Any,
    ) -> Any:
        offset = (pagination.page - 1) * self.page_size
        return {
            "results": queryset[offset : offset + self.page_size],
            "count": await self._aitems_count(queryset),
            "per_page": self.page_size,
        }