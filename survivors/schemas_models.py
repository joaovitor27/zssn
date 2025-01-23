from typing import List

from ninja import ModelSchema

from survivors.models import Survivor, Inventory, Item, ItemInventory, Report


class ReportSchema(ModelSchema):
    class Meta:
        model = Report
        fields = '__all__'


class ItemSchema(ModelSchema):
    class Meta:
        model = Item
        fields = 'id', 'name', 'points'


class ItemInventorySchema(ModelSchema):
    item: ItemSchema

    class Meta:
        model = ItemInventory
        fields = '__all__'


class InventorySchema(ModelSchema):
    items: List[ItemInventorySchema]
    survivor_id: int

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'survivor']


class SurvivorSchema(ModelSchema):
    inventory: InventorySchema
    reports: List[ReportSchema]

    class Meta:
        model = Survivor
        fields = '__all__'

    @staticmethod
    def resolve_reports(obj: Survivor) -> List[ReportSchema]:
        """
        Método que resolve o relacionamento ManyToMany com o modelo Report.
        Retorna uma lista de schemas de relatórios associados ao sobrevivente.
        """
        reports = obj.reported.all()  # ou obj.reporter.all(), dependendo do relacionamento desejado
        return [ReportSchema.from_orm(report) for report in reports]

    @staticmethod
    def resolve_inventory(obj: Survivor) -> InventorySchema | None:
        """
        Método que resolve o relacionamento OneToOne com o modelo Inventory.
        Retorna o schema do inventário associado ao sobrevivente.
        """
        if obj.inventory:
            return InventorySchema.from_orm(obj.inventory)
        return None


class SurvivorCreateSchema(ModelSchema):
    class Meta:
        model = Survivor
        fields = '__all__'
        exclude = ['id', 'reports', 'infected', 'created_at', 'updated_at']


class SurvivorUpdateSchema(ModelSchema):
    latitude: float
    longitude: float

    class Meta:
        model = Survivor
        fields = ['latitude', 'longitude']
