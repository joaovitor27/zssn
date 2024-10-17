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


@router.get("inventories", response=List[InventorySurvivorSchema])
@paginate(PageNumberPagination, page_size=10)
def list_inventories(request, filters: InventoryFilter = Query(...)):
    inventories = Inventory.objects.all()
    inventories = filters.filter(inventories)
    return inventories


@router.get("inventories/{id}", response=InventorySurvivorSchema)
def get_inventory(request, id: int):
    return get_object_or_404(Inventory, id=id)


@router.put("inventories/{item_id}", response=InventorySurvivorSchema)
def create_inventory(request, item_id: int, data: InventorySurvivorUpdateSchema):
    survivor = get_object_or_404(Survivor, id=data.survivor_id)
    if survivor.infected:
        raise Exception("Survivor is infected")

    item = get_object_or_404(Item, id=item_id)

    if survivor.inventory_set.filter(item=data.item).exists():
        survivor.inventory_set.filter(item=data.item).update(quantity=data.quantity)
        return survivor.inventory_set.get(item=data.item)

    return survivor.inventory_set.create(item=item, quantity=data.quantity)


@router.delete("inventories/{item_id}")
def delete_inventory(request, id: int, item_id: int):
    survivor = get_object_or_404(Survivor, id=id)
    inventory = get_object_or_404(survivor.inventory_set, item_id=item_id)
    inventory.delete()
    return {"message": "Inventory deleted successfully"}
