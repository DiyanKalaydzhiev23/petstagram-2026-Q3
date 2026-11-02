from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Exists, OuterRef
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, resolve_url
from django.views.generic import ListView
from pyperclip import copy

from common.forms import SearchForm, CommentForm
from common.models import Like
from photos.models import Photo


class HomeView(ListView):
    context_object_name = "all_photos"
    paginate_by = 1
    template_name = "common/home-page.html"

    def get_queryset(self) -> QuerySet:
        qs = Photo.objects.prefetch_related('tagged_pets', 'like_set').order_by('-date_of_publication')
        pet_name = self.request.GET.get('pet_name')

        if pet_name:
            qs = qs.filter(tagged_pets__name__icontains=pet_name)

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_liked_by_user=Exists(
                    Like.objects.filter(
                        to_photo_id=OuterRef('pk'),
                        user=self.request.user,
                    )
                )
            )
        else:
            qs = qs.annotate(
                is_liked_by_user=Exists(Like.objects.none()),
            )

        return qs


@login_required
def like_functionality_view(request: HttpRequest, photo_id: int) -> HttpResponse:
    like_object = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()

    if like_object:
        like_object.delete()
    else:
        Like.objects.create(
            to_photo_id=photo_id,
            user=request.user,
        )

    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')

@login_required
def add_comment_view(request: HttpRequest, photo_id: int) -> HttpResponse:
    if request.method == "POST":
        photo = Photo.objects.get(pk=photo_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.user = request.user
            comment.save()

        return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')

def share_functionality(request: HttpRequest, photo_id: int) -> HttpResponse:
    copy(request.META.get('HTTP_REFERER')[:-1] + resolve_url('photos:details', photo_id))
    return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')