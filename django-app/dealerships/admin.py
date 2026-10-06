from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    fields = ('name', 'type', 'year', 'dealer_id')
    show_change_link = True

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_summary', 'models_count', 'created_at')
    search_fields = ('name', 'description')
    inlines = [CarModelInline]

    def description_summary(self, obj):
        return obj.description[:60] + "..." if len(obj.description) > 60 else obj.description
    description_summary.short_description = "Descripción"

    def models_count(self, obj):
        return obj.models.count()
    models_count.short_description = "Total Modelos"


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make', 'type', 'year', 'dealer_id')
    list_filter = ('make', 'type', 'year')
    search_fields = ('name', 'make__name')
    list_editable = ('type', 'year')
