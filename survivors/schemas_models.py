from ninja import ModelSchema

from survivors.models import Survivor


class SurvivorSchema(ModelSchema):
    class Meta:
        model = Survivor
        fields = '__all__'
