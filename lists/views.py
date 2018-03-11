from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    minimal_page = '<html><head><title>To-Do lists</title></head></html>'
    return HttpResponse(minimal_page)
