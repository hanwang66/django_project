from django.shortcuts import render, redirect, get_object_or_404
from .models import EnglishStudyRecord
from .forms import EnglishStudyRecordForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


@login_required
def submit_record(request):
    if request.method == 'POST':
        form = EnglishStudyRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('english:overview')
    else:
        form = EnglishStudyRecordForm()
    return render(request, 'english/submit_record.html', {'form': form})


@login_required
def edit_record(request, pk):
    record = get_object_or_404(EnglishStudyRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EnglishStudyRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('english:overview')
    else:
        form = EnglishStudyRecordForm(instance=record)
    return render(request, 'english/edit_record.html', {'form': form})


@login_required
def delete_record(request, pk):
    record = get_object_or_404(EnglishStudyRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('english:overview')
    return render(request, 'english/delete_record.html', {'record': record})


@login_required
def record_detail(request, pk):
    record = get_object_or_404(EnglishStudyRecord, pk=pk, user=request.user)
    return render(request, 'english/record_detail.html', {'record': record})


@login_required
def overview(request):
    records = EnglishStudyRecord.objects.filter(user=request.user).order_by('-date')
    total_duration = records.aggregate(Sum('duration'))['duration__sum'] or 0
    return render(request, 'english/overview.html', {
        'records': records,
        'total_duration': total_duration
    })
