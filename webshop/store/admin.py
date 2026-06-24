from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
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

class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)

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
admin.site.register(User, CustomUserAdmin)

