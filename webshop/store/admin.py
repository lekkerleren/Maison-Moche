from django.contrib import admin

from django.contrib import admin
from .models import (
    Category,
    Product,
    Variant,
    VariantImage,
    VariantShipping,
    Collection,
    TableAttribute,
    LightingAttribute,
    SeatingAttribute,
    DecorativeAttribute,
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(VariantImage)
admin.site.register(VariantShipping)
admin.site.register(Collection)
admin.site.register(TableAttribute)
admin.site.register(LightingAttribute)
admin.site.register(SeatingAttribute)
admin.site.register(DecorativeAttribute)

