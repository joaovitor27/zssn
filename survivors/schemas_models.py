from typing import List, Optional

from ninja import ModelSchema

from survivors.models import Survivor, Inventory, Item


class ItemInventorySchema(ModelSchema):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['created_at', 'updated_at']


class InventorySurvivorUpdateSchema(ModelSchema):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['id', 'created_at', 'item', 'updated_at']


class InventorySurvivorSchema(ModelSchema):
    item: ItemInventorySchema

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['survivor']


class SurvivorSchema(ModelSchema):
    items: List[InventorySurvivorSchema]

    class Meta:
        model = Survivor
        fields = '__all__'


class InventorySurvivorCreateSchema(ModelSchema):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['id', 'survivor', 'created_at', 'updated_at']


class SurvivorCreateSchema(ModelSchema):
    items: Optional[List[InventorySurvivorCreateSchema]]

    class Meta:
        model = Survivor
        fields = '__all__'
        exclude = ['id', 'reports', 'infected', 'created_at', 'updated_at']


class SurvivorUpdateSchema(ModelSchema):
    class Meta:
        model = Survivor
        fields = ['latitude', 'longitude']


class InventorySchema(ModelSchema):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['survivor']