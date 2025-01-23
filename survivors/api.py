from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination

from survivors.models import Survivor, Report
from survivors.pagination import CustomPagination
from survivors.schemas_filters import SurvivorFilter
from survivors.schemas_models import SurvivorSchema, SurvivorCreateSchema, SurvivorUpdateSchema, ReportSchema

router = Router()


@router.get("survivors", response=List[SurvivorSchema])
@paginate(CustomPagination)
def list_survivors(request, filters: SurvivorFilter = Query(...)):
    return filters.filter(Survivor.objects.select_related('inventory').prefetch_related('reported', 'reporter'))


@router.get("survivors/{id}", response=SurvivorSchema)
def get_survivor(request, id: int):
    return get_object_or_404(Survivor, id=id)


@router.post("survivors", response=SurvivorSchema)
def create_survivor(request, data: SurvivorCreateSchema):
    teste = Survivor.objects.create(**data.dict())
    return teste


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


@router.get("survivors/{id}/reports", response=List[SurvivorSchema])
def get_survivor_reports(request, id: int):
    survivor = get_object_or_404(Survivor, id=id)
    return survivor.reports.all()


@router.get("survivors/{id}/inventory", response=SurvivorSchema)
def get_survivor_inventory(request, id: int):
    survivor = get_object_or_404(Survivor, id=id)
    return survivor.inventory
