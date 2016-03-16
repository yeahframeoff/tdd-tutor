from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from .forms import ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['text'], list=the_list)
            item.full_clean()
            item.save()
            return redirect(the_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': the_list, 'error': error})


def new_list(request):
    the_list = List.objects.create()
    item = Item(text=request.POST['text'], list=the_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        the_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(the_list)
