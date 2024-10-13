from typing import List

from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination

from survivors.models import Survivor
from survivors.schemas_filters import SurvivorFilter
from survivors.schemas_models import SurvivorSchema

router = Router()


@router.get("/", response=List[SurvivorSchema])
@paginate(PageNumberPagination, page_size=10)
def list_survivors(request, filters: SurvivorFilter = Query(...)):
    survivors = Survivor.objects.all()
    survivors = filters.filter(survivors)
    return survivors
