import unfold
from django.contrib import admin
from unfold.admin import ModelAdmin
from pets.models import Pet


@admin.register(Pet)
class PetAdmin(ModelAdmin):
    list_display = ['id', 'name', 'date_of_birth']
