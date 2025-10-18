from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock
from django.http import HttpResponse

def stock_index(request):
	stocks = Stock.objects.all().order_by('-created_at')
	return render(request, "stock/stock_index.html", {"stocks": stocks})

def stock_detail(request, pk):
	stock = get_object_or_404(Stock, pk=pk)
	return render(request, "stock/stock_detail.html", {"stock": stock})

def stock_add(request):
	if request.method == "POST":
		code = request.POST.get("code")
		name = request.POST.get("name")
		price = request.POST.get("price")
		Stock.objects.create(code=code, name=name, price=price)
		return redirect("/stock/")
	return render(request, "stock/stock_add.html")

def stock_edit(request, pk):
	stock = get_object_or_404(Stock, pk=pk)
	if request.method == "POST":
		stock.code = request.POST.get("code")
		stock.name = request.POST.get("name")
		stock.price = request.POST.get("price")
		stock.save()
		return redirect(f"/stock/{pk}/")
	return render(request, "stock/stock_edit.html", {"stock": stock})

def stock_delete(request, pk):
	stock = get_object_or_404(Stock, pk=pk)
	if request.method == "POST":
		stock.delete()
		return redirect("/stock/")
	return render(request, "stock/stock_delete.html", {"stock": stock})
