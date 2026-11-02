from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView

from common.mixins import CheckIsOwnerMixin
from photos.forms import PhotoAddForm, PhotoEditForm
from photos.models import Photo


@login_required
def photo_add_view(request: HttpRequest) -> HttpResponse:
    form = PhotoAddForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
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


class PhotoEditView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    model = Photo
    form_class = PhotoEditForm
    template_name = 'photos/photo-edit-page.html'

    def get_success_url(self) -> str:
        return reverse(
            'photos:details',
            kwargs={"pk": self.object.pk},
        )


class PhotoDeleteView(LoginRequiredMixin, CheckIsOwnerMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('common:home')
