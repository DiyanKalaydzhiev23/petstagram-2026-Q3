from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from common.forms import SearchForm, CommentForm
from common.models import Like
from photos.models import Photo


def home_page_view(request: HttpRequest) -> HttpResponse:
    all_photos = Photo.objects.prefetch_related('tagged_pets', 'like_set').order_by('-date_of_publication')
    form = SearchForm(request.GET or None)

    if form.is_valid():
        searched_name = form.cleaned_data['pet_name']
        all_photos = all_photos.filter(tagged_pets__name__icontains=searched_name)

    context = {
        "all_photos": all_photos,
    }

    return render(request, 'common/home-page.html', context)


def like_functionality_view(request: HttpRequest, photo_id: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_id).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_id,
        )

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')


def add_comment_view(request: HttpRequest, photo_id: int) -> HttpResponse:
    if request.method == "POST":
        photo = Photo.objects.get(pk=photo_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')

def share_functionality(request: HttpRequest, photo_id: int) -> HttpResponse:
    copy(request.META.get('HTTP_REFERER')[:-1] + resolve_url('photos:details', photo_id))
    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')