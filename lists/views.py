from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    the_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=the_list)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' % the_list.id)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': the_list, 'error': error})


def new_list(request):
    the_list = List.objects.create()
    item = Item(text=request.POST['item_text'], list=the_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        the_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/%d/' % the_list.id)
