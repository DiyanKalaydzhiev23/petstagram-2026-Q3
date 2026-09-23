from http.client import HTTPResponse
from django.http import HttpRequest
from django.shortcuts import render


def home_page_view(request: HttpRequest) -> HTTPResponse:
    return render(request, 'common/home-page.html')
