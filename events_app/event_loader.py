from events_app.models import User, AboutUser, UserGoals, Events, EventParticipation
from django.db.models import Count, F
from django.utils.timezone import datetime
from django.db.models import Q



def get_by_category(category, limit=3, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).filter(category=category).order_by('-count')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')[0:limit]
    return with_participations(lst, usr)


def get_most_popular(limit=3, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).order_by('-count')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')[0:limit]
    return with_participations(lst, usr)

def get_most_recent(limit=3, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).order_by('-created_at')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')[0:limit]
    return with_participations(lst, usr)


def get_upcoming(limit=3, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).filter(event_date__gte=datetime.today()).order_by('event_date')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')[0:limit]
    return with_participations(lst, usr)

def get_by_slug(slug, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)),creator_name=F('creator__username')).filter(slug=slug).order_by('-created_at')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')
    return with_participations(lst, usr)

def search(slug, usr=None):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).filter(Q(name__icontains=slug.replace("-"," ")) | Q(slug__icontains=slug)).order_by('-created_at')
    lst = events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')
    return with_participations(lst, usr)

def with_participations(lst, usr):
    if usr==None or not usr.is_authenticated:
        return lst
    print(usr)
    newLst = []
    for val in lst:
        event = Events.objects.get(slug=val[5])
        participating = EventParticipation.objects.filter(user=usr,event=event)
        if len(participating) > 0:
            participating = 1 if participating[0].participating else 0
        else:
            participating = -1
        newLst.append((val[0],val[1],val[2],val[3],val[4], val[5], participating),)
    return tuple(newLst)

def get_events_for(user):
    events = Events.objects.annotate(count=Count('eventparticipation', filter=Q(eventparticipation__participating=True)), creator_name=F('creator__username')).filter(creator=user).order_by('-created_at')
    return events.values_list('name', 'category', 'count', 'image', 'creator_name', 'slug')