from typing import Optional

from ninja import FilterSchema


class SurvivorFilter(FilterSchema):
    name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    infected: Optional[bool] = None
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    updated_after: Optional[str] = None
    updated_before: Optional[str] = None



