from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination

from survivors.models import Survivor, Item, Inventory
from survivors.schemas_filters import SurvivorFilter, InventoryFilter
from survivors.schemas_models import SurvivorSchema, SurvivorCreateSchema, SurvivorUpdateSchema, \
    InventorySurvivorSchema, InventorySurvivorUpdateSchema

router = Router()


@router.get("survivors", response=List[SurvivorSchema])
@paginate(PageNumberPagination, page_size=10)
def list_survivors(request, filters: SurvivorFilter = Query(...)):
    survivors = Survivor.objects.all()
    survivors = filters.filter(survivors)
    return survivors


@router.get("survivors/{id}", response=SurvivorSchema)
def get_survivor(request, id: int):
    return get_object_or_404(Survivor, id=id)


@router.post("survivors", response=SurvivorSchema)
def create_survivor(request, data: SurvivorCreateSchema):
    return Survivor.objects.create(**data.dict())


@router.put("survivors/{id}", response=SurvivorSchema)
def update_survivor(request, id: int, data: SurvivorUpdateSchema):
    survivor = get_object_or_404(Survivor, id=id)
    if survivor.infected:
        raise Exception("Survivor is infected")

    for key, value in data.dict().items():
        setattr(survivor, key, value)
    survivor.save()
    return survivor


@router.delete("survivors/{id}")
def delete_survivor(request, id: int):
    survivor = get_object_or_404(Survivor, id=id)
    survivor.delete()
    return {"message": "Survivor deleted successfully"}
