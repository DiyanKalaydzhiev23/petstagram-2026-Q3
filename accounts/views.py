from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count, Sum
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import AppUserCreateForm, ProfileEditForm
from accounts.models import Profile
from common.mixins import CheckIsOwnerMixin

UserModel = get_user_model()


class RegisterAppUserView(CreateView):
    model = UserModel
    form_class = AppUserCreateForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('accounts:login')


class LoginAppUserView(LoginView):
    template_name = 'accounts/login-page.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_likes'] = self.object.user.photo_set.annotate(
            num_likes=Count('like'),
        ).aggregate(total_likes=Sum('num_likes')).get('total_likes', 0)
        context['total_pets'] = self.object.user.pet_set.count()
        context['total_photos'] = self.object.user.photo_set.count()

        return context

class ProfileUpdateView(LoginRequiredMixin, CheckIsOwnerMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_success_url(self) -> str:
        return reverse(
            'accounts:details',
            kwargs={
                'pk': self.object.pk,
            }
        )


def profile_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    user = UserModel.objects.get(pk=pk)

    if request.user.is_authenticated and request.user.pk == user.pk:
        if request.method == "POST":
            user.delete()
            return reverse('common:home')
    else:
        return HttpResponseForbidden()


    return render(request, 'accounts/profile-delete-page.html')
