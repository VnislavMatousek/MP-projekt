from django.contrib import admin

from .models import CalculationResult, CalculationResultYear

# Register your models here.


@admin.register(CalculationResult)
class CalculationResultAdmin(admin.ModelAdmin):
    pass


@admin.register(CalculationResultYear)
class CalculationResultYearAdmin(admin.ModelAdmin):
    pass
