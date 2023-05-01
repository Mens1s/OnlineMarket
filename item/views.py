from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import NewItemForm, EditItemForm
# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_item = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_item': related_item
    })
@login_required()
def new(request):
    if( request.method == 'POST'):
        form = NewItemForm(request.POST, request.FILES or None)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render (request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required()
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if( request.method == 'POST'):
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render (request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })

@login_required()
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')