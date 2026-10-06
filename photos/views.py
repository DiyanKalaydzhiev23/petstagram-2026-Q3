from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from photos.forms import PhotoAddForm, PhotoEditForm
from photos.models import Photo


def photo_add_view(request: HttpRequest) -> HttpResponse:
    form = PhotoAddForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('common:home')

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-add-page.html', context)


def photo_details_view(request: HttpRequest, pk: int) -> HttpResponse:
    photo = Photo.objects.prefetch_related(
        'tagged_pets', 'like_set', 'comment_set'
    ).get(pk=pk)

    context = {
        'photo': photo,
    }

    return render(request, 'photos/photo-details-page.html', context)


def photo_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)
    form = PhotoEditForm(request.POST or None, request.FILES or None, instance=photo)

    if form.is_valid():
        form.save()
        return redirect('photos:details', photo.pk)

    context = {
        'form': form,
    }

    return render(request, 'photos/photo-edit-page.html', context)


def photo_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('common:home')