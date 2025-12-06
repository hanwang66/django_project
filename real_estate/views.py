from collections import defaultdict
import logging

from .models import RealEstate

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import RealEstate
from django.db.models import Avg, Max, Min, Count, Sum
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages 

logger = logging.getLogger(__name__) 


def is_admin(user):
    return user.is_superuser


def realestate_trend_list(request):
	
	all_estates = RealEstate.objects.all()
	top_n = request.GET.get('top_n')
	try:
		top_n = int(top_n)
		if top_n < 1 or top_n > 20:
			top_n = 3
	except Exception:
		top_n = 3
	city_groups = defaultdict(list)
	for e in all_estates:
		city_groups[e.city].append(e)
	trend_list = []
	for city, estates_in_city in city_groups.items():
		city_trends = []
		community_groups = defaultdict(list)
		for e in estates_in_city:
			community_groups[e.community].append(e)
		for community, group in community_groups.items():
			if len(group) < 2:
				continue
			sorted_group = sorted(group, key=lambda x: x.date)
			first = sorted_group[0]
			last = sorted_group[-1]
			try:
				first_unit_price = round(first.price * 10000 / float(first.area), 2) if first.area and first.price else None
				last_unit_price = round(last.price * 10000 / float(last.area), 2) if last.area and last.price else None
			except Exception:
				first_unit_price = None
				last_unit_price = None
			if first_unit_price and last_unit_price and first_unit_price != 0:
				change = round((last_unit_price - first_unit_price) / first_unit_price * 100, 2)
				city_trends.append({
					'city': city,
					'community': community,
					'first_unit_price': first_unit_price,
					'last_unit_price': last_unit_price,
					'change': change,
					'first_detail': {
						'date': first.date,
						'price': first.price,
						'area': first.area
					},
					'last_detail': {
						'date': last.date,
						'price': last.price,
						'area': last.area
					}
				})
		city_trends = sorted(city_trends, key=lambda x: abs(x['change']), reverse=True)[:top_n]
		trend_list.append({'city': city, 'trends': city_trends})
	return render(request, "real_estate/trend_list.html", {"trend_list": trend_list, "top_n": top_n})


def realestate_trend_data(request):
	city = request.GET.get('city', '').strip()
	community = request.GET.get('community', '').strip()
	qs = RealEstate.objects.all()
	if city:
		qs = qs.filter(city=city)
	if community:
		qs = qs.filter(community=community)
	# 按时间排序
	qs = qs.order_by('date')
	dates = []
	unit_prices = []
	for e in qs:
		try:
			unit_price = round(e.price * 10000 / float(e.area), 2) if e.area and e.price else None
		except Exception:
			unit_price = None
		if e.date and unit_price:
			dates.append(e.date)
			unit_prices.append(unit_price)
	return JsonResponse({'dates': dates, 'unit_prices': unit_prices})


def realestate_index(request):
	logger.info("进入 realestate_index 视图")
	estates = RealEstate.objects.all()
	city = request.GET.get('city', '').strip()
	community = request.GET.get('community', '').strip()
	if city:
		estates = estates.filter(city__icontains=city)
	if community:
		estates = estates.filter(community__icontains=community)
	estates = estates.order_by('-id')

	# 分页参数
	try:
		page_size = int(request.GET.get('page_size', 20))
		if page_size not in [10, 20, 50]:
			page_size = 20
	except Exception:
		page_size = 20
	try:
		page = int(request.GET.get('page', 1))
		if page < 1:
			page = 1
	except Exception:
		page = 1
	total = estates.count()
	start = (page - 1) * page_size
	end = start + page_size
	estates_page = estates[start:end]
	# 计算单价
	for e in estates_page:
		try:
			e.unit_price = round(e.price * 10000 / float(e.area), 2) if e.area and e.price else None
		except Exception:
			e.unit_price = None
	total_pages = (total + page_size - 1) // page_size

	cities = RealEstate.objects.values_list('city', flat=True).distinct()
	# 城市-小区房价变化趋势分析
	from collections import defaultdict
	trend_list = []
	all_estates = RealEstate.objects.all()
	# 按城市分组
	city_groups = defaultdict(list)
	for e in all_estates:
		city_groups[e.city].append(e)
	for city, estates_in_city in city_groups.items():
		city_trends = []
		# 按小区分组
		community_groups = defaultdict(list)
		for e in estates_in_city:
			community_groups[e.community].append(e)
		for community, group in community_groups.items():
			if len(group) < 2:
				continue
			# 按时间排序
			sorted_group = sorted(group, key=lambda x: x.date)
			first = sorted_group[0]
			last = sorted_group[-1]
			try:
				first_unit_price = round(first.price * 10000 / float(first.area), 2) if first.area and first.price else None
				last_unit_price = round(last.price * 10000 / float(last.area), 2) if last.area and last.price else None
			except Exception:
				first_unit_price = None
				last_unit_price = None
			if first_unit_price and last_unit_price and first_unit_price != 0:
				change = round((last_unit_price - first_unit_price) / first_unit_price * 100, 2)
				city_trends.append({
					'city': city,
					'community': community,
					'first_unit_price': first_unit_price,
					'last_unit_price': last_unit_price,
					'change': change
				})
		# 每个城市取变化幅度前三
		city_trends = sorted(city_trends, key=lambda x: abs(x['change']), reverse=True)[:3]
		trend_list.extend(city_trends)

	return render(request, "real_estate/list_realestate.html", {
		"estates": estates_page,
		"page": page,
		"page_size": page_size,
		"total": total,
		"total_pages": total_pages,
		"cities": cities,
		"trend_list": trend_list,
	})

def realestate_detail(request, pk):
	logger.info("进入 realestate_detail 视图")
	estate = get_object_or_404(RealEstate, pk=pk)
	return render(request, "real_estate/detail_realestate.html", {"estate": estate})

def realestate_add(request):
    
	if request.method == "POST":
		logger.info("正在处理添加房产的 POST 请求")
		community = request.POST.get("community")
		city = request.POST.get("city")
		area = request.POST.get("area")
		floor = request.POST.get("floor")
		price = request.POST.get("price") or 0
		date = request.POST.get("date") or ''
		RealEstate.objects.create(community=community, city=city, area=area, floor=floor, price=price, date=date)
		return redirect("/real_estate/")
	return render(request, "real_estate/add_realestate.html")


def realestate_edit(request, pk):
	estate = get_object_or_404(RealEstate, pk=pk)
	if not request.user.is_superuser:  # 检查是否是 admin 用户
		messages.error(request, "非管理员用户无权添加数据。")  # 添加提示信息
		return redirect("/real_estate/")  # 重定向到列表页
	if request.method == "POST":
		estate.community = request.POST.get("community")
		estate.city = request.POST.get("city")
		estate.area = request.POST.get("area")
		estate.floor = request.POST.get("floor")
		estate.price = request.POST.get("price")
		estate.date = request.POST.get("date")
		estate.save()
		return redirect(f"/real_estate/{pk}/")
	return render(request, "real_estate/edit_realestate.html", {"estate": estate})

def realestate_delete(request, pk):
	estate = get_object_or_404(RealEstate, pk=pk)
	if request.method == "POST":
		estate.delete()
		return redirect("/real_estate/")
	return render(request, "real_estate/delete_realestate.html", {"estate": estate})
