from lib2to3.fixes.fix_input import context

from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from pets.forms import PetCreateForm, PetEditForm, PetDeleteForm, PetForm
from pets.models import Pet
from photos.models import Photo


class PetAddView(CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('accounts:details', kwargs={"pk": 1})


# def pet_add_view(request: HttpRequest) -> HttpResponse:
#     form = PetCreateForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#         return redirect('accounts:details', pk=1)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'pets/pet-add-page.html', context)


class PetEditView(UpdateView):
    model = Pet
    form_class = PetEditForm
    template_name = 'pets/pet-edit-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_success_url(self) -> str:
        return reverse(
            'pets:details',
            kwargs={
                "username": "username",
                "pet_slug": self.object.slug,
            }
        )


# def pet_edit_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = get_object_or_404(Pet, slug=pet_slug)
#     form = PetEditForm(request.POST or None, instance=pet)
#
#     if form.is_valid():
#         pet = form.save()
#         return redirect('pets:details', username="username", pet_slug=pet.slug)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'pets/pet-edit-page.html', context)


class PetDeleteView(DeleteView):
    model = Pet
    form_class = PetDeleteForm
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    success_url = reverse_lazy('accounts:details', kwargs={"pk": 1})

    def get_initial(self):
        return self.object.__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "data": self.object.__dict__
        })
        return kwargs


# def pet_delete_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = get_object_or_404(Pet, slug=pet_slug)
#     form = PetDeleteForm(request.POST or None, instance=pet)
#
#     if request.method == "POST":
#         pet.delete()
#         return redirect('accounts:details', pk=1)
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'pets/pet-delete-page.html', context)
#


class PetDetailView(DetailView):
    queryset = Pet.objects.prefetch_related(
        Prefetch(
            'photo_set',
            queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
        )
    )
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-details-page.html"


#
# def pet_details_view(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = Pet.objects.prefetch_related(
#         Prefetch(
#             'photo_set',
#             queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
#         )
#     ).get(slug=pet_slug)
#
#     context = {
#         "pet": pet,
#     }
#
#     return render(request, 'pets/pet-details-page.html', context)
