from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator
from .models import Players, Events, Details, Blog
from members.models import Profile
import datetime

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def contact(request):
    return render(request, 'contact.html')

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
        
        print(playername.id)

        positions = ""

        if playername.pitcher == True:
            positions = positions + "P/"
        if playername.catcher == True:
            positions = positions + "C/"
        if playername.firstbase == True:
            positions = positions + "1B/"
        if playername.secondbase == True:
            positions = positions + "2B/"
        if playername.thirdbase == True:
            positions = positions + "3B/"
        if playername.shortstop == True:
            positions = positions + "SS/"
        if playername.outfield == True:
            positions = positions + "OF"


        positions = positions.rstrip("/")
        
        
        
        
        
        
        context = {
            'playername': playername, 'playerevents': playerevents, 'playerimg': playerimg, 'playerpositions': positions,
        }
        
    else:
        playername = playerinfo[0]
        playerimg = playername.player.image
        print(playername.player.id)


        positions = ""

        if playername.player.pitcher == True:
            positions = positions + "P/"
        if playername.player.catcher == True:
            positions = positions + "C/"
        if playername.player.firstbase == True:
            positions = positions + "1B/"
        if playername.player.secondbase == True:
            positions = positions + "2B/"
        if playername.player.thirdbase == True:
            positions = positions + "3B/"
        if playername.player.shortstop == True:
            positions = positions + "SS/"
        if playername.player.outfield == True:
            positions = positions + "OF"

        positions = positions.rstrip("/")
        

        
        template = loader.get_template('playerdetail.html')
        context = {
            'playerinfo': playerinfo,'playername': playername, 'playerimg': playerimg, 'playerpositions': positions, 
        }
        
    return HttpResponse(template.render(context, request))

def eventdetail(request,id):
    eventinfo = Events.objects.get(pk=id)
    
    template = loader.get_template('eventdetail.html')
    context = {
        'eventinfo': eventinfo,
    }
    return HttpResponse(template.render(context, request))

def eventresults(request,id):
    print(id)
    eventinfo = Events.objects.get(pk=id)
    eventdetails = Details.objects.filter(event__pk=id).order_by('player__lastName')
    
    template = loader.get_template('eventresults.html')
    context = {
        'eventinfo': eventinfo, 'eventdetails': eventdetails,
    }
    return HttpResponse(template.render(context, request))

def players(request):
    allplayers = Players.objects.all().order_by('lastName').values()
    

    context = {
        'allplayers': allplayers,
                }



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