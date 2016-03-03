from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': the_list})


def new_list(request):
    the_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=the_list)
    return redirect('/lists/%d/' % the_list.id)


def add_item(request, list_id):
    the_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=the_list)
    return redirect('/lists/%d/' % the_list.id)
