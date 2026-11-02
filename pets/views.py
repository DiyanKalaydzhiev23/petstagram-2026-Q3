from django.db.models import Prefetch
from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from pets.models import Pet
from photos.models import Photo


class PetAddView(CreateView):
    model = Pet
    form_class = PetCreateForm
    template_name = 'pets/pet-add-page.html'
    success_url = reverse_lazy('accounts:details', kwargs={"pk": 1})

    def get_success_url(self) -> str:
        return reverse(
            'accounts:details',
            kwargs={'pk': self.request.user.pk},
        )

    def form_valid(self, form) -> HttpResponseRedirect:
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


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


class PetDetailView(DetailView):
    queryset = Pet.objects.prefetch_related(
        Prefetch(
            'photo_set',
            queryset=Photo.objects.prefetch_related('tagged_pets', 'like_set')
        )
    )
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-details-page.html"

