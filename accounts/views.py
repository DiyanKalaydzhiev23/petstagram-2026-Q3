from http.client import HTTPResponse

from django.http import HttpRequest
from django.shortcuts import render


def register_view(request: HttpRequest) -> HTTPResponse:
    return render(request, 'accounts/register-page.html')


def login_view(request: HttpRequest) -> HTTPResponse:
    return render(request, 'accounts/login-page.html')


def profile_details_view(request: HttpRequest, pk: int) -> HTTPResponse:
    return render(request, 'accounts/profile-details-page.html')


def profile_edit_view(request: HttpRequest, pk: int) -> HTTPResponse:
    return render(request, 'accounts/profile-edit-page.html')


def profile_delete_view(request: HttpRequest, pk: int) -> HTTPResponse:
    return render(request, 'accounts/profile-delete-page.html')
