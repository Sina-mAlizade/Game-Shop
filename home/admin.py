from django.contrib import admin
from .models import *


admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "is_trending",
        "is_most_played",
    )

    search_fields = (
        "title",
        "category",
    )

    list_filter = (
        "category",
        "is_trending",
    )


