from django.contrib import admin

from photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['location', 'date_of_publication', 'tagged_pets_list']

    @staticmethod
    def tagged_pets_list(obj) -> str:
        return ', '.join(p.name for p in obj.tagged_pets.all())
