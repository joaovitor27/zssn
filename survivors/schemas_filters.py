from datetime import date
from typing import Optional

from ninja import FilterSchema, Field


class SurvivorFilter(FilterSchema):
    age: Optional[int] = None
    name: Optional[str] = Field(None, q='name__icontains')
    sex: Optional[str] = Field(None, q='sex')
    infected: Optional[bool] = Field(None, q='infected')
    from_date: Optional[date] = Field(None, q='created_at__date__gte')
    to_date: Optional[date] = Field(None, q='created_at__date__lte')


class InventoryFilter(FilterSchema):
    item: Optional[str] = None
    points: Optional[int] = None
    survivors_name: Optional[str] = None
    survivors_id: Optional[int] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None
