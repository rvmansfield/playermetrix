from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .models import Players, Events, Details

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def confirm(request):
    return render(request, 'confirm.html')

def about(request):
    return render(request, 'about.html')

def playerdetail(request,slug):
    playerinfo = Details.objects.filter(player__slug=slug)
    playername = playerinfo[0]
    template = loader.get_template('playerdetail.html')
    context = {
        'playerinfo': playerinfo,'playername': playername,
    }
    return HttpResponse(template.render(context, request))

def eventdetail(request,id):
    eventinfo = Events.objects.get(pk=id)
    
    template = loader.get_template('eventdetail.html')
    context = {
        'eventinfo': eventinfo,
    }
    return HttpResponse(template.render(context, request))

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

def events(request):
    allevents = Events.objects.all().order_by('date').values()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(allevents, 10) #pagination rows

    context = {
        'allevents': allevents,
                }

    try:
        allevents = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        allevents = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        allevents = paginator.page(paginator.num_pages)

    return render(request, 'events.html', {'allevents': allevents})





def tester(request):
    testinfo = Details.objects.get(id=1)
    template = loader.get_template('tester.html')
    context = {
        'testinfo': testinfo,
    }
    return HttpResponse(template.render(context, request))