from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField
from ordered_model.models import OrderedModel


class TraceConfig(Model):
    name = CharField(max_length=1024)
    is_active = BooleanField(default=True)

class TraceFilter(OrderedModel):
    config = ForeignKey(TraceConfig, on_delete=CASCADE)
    string = CharField(max_length=1024)
    order_with_respect_to = 'config'