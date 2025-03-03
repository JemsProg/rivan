from django.contrib import admin
from .models import TrainingQuotationRequest

@admin.register(TrainingQuotationRequest)
class TrainingQuotationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "course", "submitted_at")
    search_fields = ("full_name", "email", "course")
    list_filter = ("course", "training_location", "submitted_at")
