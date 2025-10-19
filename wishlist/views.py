from django.shortcuts import render, get_object_or_404, redirect
from .models import Wishlist, WishlistItem

def wishlist_list(request):
    wishlists = Wishlist.objects.all().order_by('-created_at')
    return render(request, 'wishlist/list_wishlist.html', {'wishlists': wishlists})

def wishlist_detail(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)
    filter_status = request.GET.get('status', 'all')
    all_items = wishlist.items.all().order_by('-created_at')
    if filter_status == 'done':
        items = all_items.filter(is_done=True)
    elif filter_status == 'undone':
        items = all_items.filter(is_done=False)
    else:
        items = all_items
    total = all_items.count()
    done_count = all_items.filter(is_done=True).count()
    undone_count = all_items.filter(is_done=False).count()
    percent = int(done_count * 100 / total) if total > 0 else 0
    total_price = sum([item.price or 0 for item in all_items])
    undone_price = sum([item.price or 0 for item in all_items.filter(is_done=False)])
    return render(request, 'wishlist/detail_wishlist.html', {
        'wishlist': wishlist,
        'items': items,
        'total': total,
        'done_count': done_count,
        'undone_count': undone_count,
        'percent': percent,
        'filter_status': filter_status,
        'total_price': total_price,
        'undone_price': undone_price
    })

def wishlist_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        Wishlist.objects.create(name=name, description=description)
        return redirect('/wishlist/')
    return render(request, 'wishlist/add_wishlist.html')

def wishlistitem_add(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price') or None
        description = request.POST.get('description', '')
        WishlistItem.objects.create(wishlist=wishlist, name=name, price=price, description=description)
        return redirect(f'/wishlist/{wishlist_id}/')
    return render(request, 'wishlist/add_wishlistitem.html', {'wishlist': wishlist})

def wishlist_edit(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)
    if request.method == 'POST':
        wishlist.name = request.POST.get('name')
        wishlist.description = request.POST.get('description', '')
        wishlist.save()
        return redirect(f'/wishlist/{pk}/')
    return render(request, 'wishlist/edit_wishlist.html', {'wishlist': wishlist})

def wishlist_delete(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)
    if request.method == 'POST':
        wishlist.delete()
        return redirect('/wishlist/')
    return render(request, 'wishlist/confirm_delete.html', {
        'message': f'确定要删除愿望清单“{wishlist.name}”吗？此操作不可恢复！',
        'cancel_url': f'/wishlist/{pk}/'
    })

def wishlistitem_edit(request, wishlist_id, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist_id=wishlist_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price') or None
        item.description = request.POST.get('description', '')
        item.save()
        return redirect(f'/wishlist/{wishlist_id}/')
    return render(request, 'wishlist/edit_wishlistitem.html', {'item': item})

def wishlistitem_delete(request, wishlist_id, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist_id=wishlist_id)
    if request.method == 'POST':
        item.delete()
        return redirect(f'/wishlist/{wishlist_id}/')
    return render(request, 'wishlist/confirm_delete.html', {
        'message': f'确定要删除小项目“{item.name}”吗？此操作不可恢复！',
        'cancel_url': f'/wishlist/{wishlist_id}/'
    })

def wishlistitem_done(request, wishlist_id, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist_id=wishlist_id)
    item.is_done = True
    item.save()
    return redirect(f'/wishlist/{wishlist_id}/')

def wishlistitem_undone(request, wishlist_id, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, wishlist_id=wishlist_id)
    item.is_done = False
    item.save()
    return redirect(f'/wishlist/{wishlist_id}/')
