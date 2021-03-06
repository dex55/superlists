from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/' + str(list_.id) + '/')


def add_to_list(request, list_id):
    existing_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=existing_list)
    return redirect('/lists/' + str(existing_list.id) + '/')
