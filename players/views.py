from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .models import Players

def players(request):
    allplayers = Players.objects.all().order_by('lastName').values()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(allplayers, 10) #pagination rows

    context = {
        'allplayers': allplayers,
                }

    try:
        allplayers = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        allplayers = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        allplayers = paginator.page(paginator.num_pages)

    return render(request, 'players.html', {'allplayers': allplayers})

def tester(request):
    allplayers = Players.objects.all()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(allplayers, 10)

    context = {
        'allplayers': allplayers,
                }

    try:
        allplayers = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        allplayers = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        allplayers = paginator.page(paginator.num_pages)

    return render(request, 'players.html', {'allplayers': allplayers})