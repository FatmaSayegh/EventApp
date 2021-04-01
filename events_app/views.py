from django.shortcuts import render
from django.http import HttpResponse 
from events_app.forms import UserForm, AboutForm, GoalForm, EventCreationForm
from events_app.models import User, AboutUser, UserGoals, Events
import events_app.event_loader as eLoader
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# generate some constants
APP_NAME = 'Events'
MOST_POP_EVENTS_COUNT = 3


# session constants
SESSION_TIMEOUT = 15 # 15 minutes

SESSION_LOGIN_TIME = 'login_time'
# Create your views here.

"""
This will use the base.html template, along with th index.html files
to generte the view
"""
def index(request):
    context = {'app_name': APP_NAME, 'event_types':{('Most Popular Events', eLoader.get_most_popular(usr=request.user)), 
               ('Recent Events',eLoader.get_most_recent(usr=request.user)),('Upcoming Events',eLoader.get_upcoming(usr=request.user))},
               'logged_in': is_logged_in(request)}
    return render(request, "event_templates/index.html", context)
    
def about(request):
    context = {'app_name': APP_NAME, 'logged_in': is_logged_in(request)}
    return render(request, "event_templates/about.html", context)

def events(request):
    x = range(3)
    context = {'app_name': APP_NAME, 'event_types':{('Most Popular Events', eLoader.get_most_popular(usr=request.user)), 
               ('Recent Events',eLoader.get_most_recent(usr=request.user)),('Upcoming Events',eLoader.get_upcoming(usr=request.user))},
               'logged_in': is_logged_in(request)}
    return render(request, "event_templates/events.html", context)
    
def disabled(request):
    if is_logged_in(request):
        return redirect(reverse('events_app:profile'))
    return render(request, "event_templates/disabled.html", {'logged_in': is_logged_in(request)})


def user_login(request):
    if is_logged_in(request):
        return redirect(reverse('events_app:profile'))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # validate then show profile
        user = authenticate(username=username, password=password)
        
        if (not user == None) and user.is_active:
            login(request, user)
            update_session(request)
            return redirect(reverse('events_app:profile'))
        else:
            return redirect(reverse('events_app:disabled'))
    context = {'app_name': APP_NAME, 'pop_events':eLoader.get_most_popular(), 'logged_in': is_logged_in(request)}

    return render(request, "event_templates/login.html", context)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('events_app:index'))
    
def profile(request):
    # not use @login_required because of session timeout
    if not is_logged_in(request):
        return redirect(reverse('events_app:login'))
    # get all the users with this email
    user = request.user
    user_about = AboutUser.objects.filter(user=user)[0]
    user_goals = UserGoals.objects.filter(user=user)[0]
    
    user_context_general = {'Username': user.username, 'Email': user.email, 'Date Of Birth':user_about.dob, 'Gender':AboutUser.gender_from_id(user_about.gender)}
    
    events = eLoader.get_events_for(user)
    event_context = {('Your Events',events)}
    
               
    user_context_goals = {"Goal 1": user_goals.goal_1,"Goal 2": user_goals.goal_2, "Goal 3": user_goals.goal_3}
    
    
    context = {'General': user_context_general, 'Goals': user_context_goals, 'Biography':user_goals.bio, 'logged_in': is_logged_in(request), 'event_types':event_context, "event_count":len(events)}
    
    print("CONTEXT IS", context)
    
    return render(request, "event_templates/profile.html", context)


def register(request):
    # not use @login_required because of session timeout
    if is_logged_in(request):
        return redirect(reverse('events_app:profile'))
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        about_form = AboutForm(request.POST)
        goal_form = GoalForm(request.POST)
        if user_form.is_valid() and about_form.is_valid() and goal_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            print("User saved!")
            about_form.user = user
            about_form.save()
            print("About Failed to save")
            goal_form.user = user
            goal_form.save()
            return render(request, "event_templates/registered.html")
        else:
            print(user_form.errors, about_form.errors, goal_form.errors)
    else:
        user_form = UserForm()
        about_form = AboutForm()
        goal_form = GoalForm()
    
    context = {'app_name': APP_NAME, 'user_form':user_form, 'about_form': about_form, 'goal_form': goal_form, 'logged_in': is_logged_in(request)}
    return render(request, "event_templates/register.html", context)


def add_event(request):
    if not is_logged_in(request):
        return redirect(reverse('events_app:login'))
    if request.method == 'POST':
        add_form = EventCreationForm(request.POST, request.FILES)
        
        if add_form.is_valid():
            event = add_form.save(commit=False)
            event.creator = request.user
            event.save()
            context = {'slug': event.slug}
            print(context)
            return render(request, "event_templates/added.html", context)
        else:
            print(add_form.errors)
    else:
        add_form = EventCreationForm()
        
    context = {'app_name': APP_NAME, 'form':add_form, 'logged_in': is_logged_in(request)}
    return render(request, "event_templates/add_event.html", context)
    
    
def view_event(request, event_slug):
    update_session(request)
    context = {}
    try:
        # add to context
        events = eLoader.get_by_slug(event_slug, request.user)
        
        if len(events) > 0:
            context['exists'] = True
            context['event_types'] = [("View Event", events)]
        else:
            context['exists'] = False
    except Events.DoesNotExist:
        # nothing
        context['exists'] = False
        
    print(context)
    return render(request, "event_templates/view_event.html", context)

def search_event(request, search_slug):
    update_session(request)
    context = {}
    try:
        # add to context
        events = eLoader.search(search_slug, request.user)
        
        if len(events) > 0:
            context['exists'] = True
            context['event_types'] = [("Search results for " + search_slug.replace("-", " "), events)]
        else:
            context['exists'] = False
    except Events.DoesNotExist:
        # nothing
        context['exists'] = False
        
    print(context)
    return render(request, "event_templates/view_event.html", context)
    
def is_logged_in(request):
    update_session(request)
    if request.user and request.user.is_authenticated:
        if get_session_elapsed(request) > SESSION_TIMEOUT:
            logout(request)
            return False
        return True
    return False


def update_session(request):
    if request.user and request.user.is_authenticated:
        request.session[SESSION_LOGIN_TIME] = str(datetime.now())
    elif SESSION_LOGIN_TIME in request.session:
        request.session.pop(SESSION_LOGIN_TIME)
    
    
        
    
    
def get_session_elapsed(request):
    if not SESSION_LOGIN_TIME in request.session:
        return -1
    start_time_str = request.session[SESSION_LOGIN_TIME]
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S.%f")
    
    return int((datetime.now()-start_time).seconds/60)
