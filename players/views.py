from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .models import Players, Events, Details, Blog
import datetime

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def confirm(request):
    return render(request, 'confirm.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def playerdetail(request,slug):
    playerinfo = Details.objects.filter(player__slug=slug)


    if playerinfo.count() < 1:
        template = loader.get_template('playerdetail.html')
        playername = Players.objects.get(slug=slug)
        playerimg = playername.image
        playerevents = 0
        context = {
            'playername': playername, 'playerevents': playerevents, 'playerimg': playerimg,
        }
        
    else:
        playername = playerinfo[0]
        playerimg = playername.player.image
        template = loader.get_template('playerdetail.html')
        context = {
            'playerinfo': playerinfo,'playername': playername, 'playerimg': playerimg,
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

    paginator = Paginator(allplayers, 15) #pagination rows

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
    allevents = Events.objects.all().order_by('-date').values()
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


def blog(request):
    allPosts = Blog.objects.all().order_by('-date').values()
   
    
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(allPosts, 10) #pagination rows

    context = {
        'allPosts': allPosts,
                }

    try:
        allPosts = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        allPosts = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        allPosts = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {'allPosts': allPosts})

def blogpost(request,slug):
    blogpost = Blog.objects.get(slug=slug)
    
    template = loader.get_template('blogpost.html')
    context = {
        'blogpost': blogpost,
    }
    return HttpResponse(template.render(context, request))


def tester(request):
    allevents = Events.objects.all().order_by('-date').values()
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

    return render(request, 'tester.html', {'allevents': allevents})