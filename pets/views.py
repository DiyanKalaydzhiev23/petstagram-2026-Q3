from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def pet_add_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'pets/pet-add-page.html')


def pet_details_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    return render(request, 'pets/pet-details-page.html')


def pet_edit_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    return render(request, 'pets/pet-edit-page.html')


def pet_delete_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
    return render(request, 'pets/pet-delete-page.html')
