import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events.settings')
from django.utils.timezone import datetime
import django
django.setup()


import random as random

from events_app.models import User, AboutUser, UserGoals, Events, EventParticipation

from django.db.models import Count, F


def populate():
    user_names = ['Jad', 'Ahmad', 'Fatma', 'Ali', 'Mariam', 'Karma', 'Aya']
    users = []
    for name in user_names:
        user = add_user(name, name+"@email.com", str("123"+name+"456"))
        set_goals_and_bio(user, "My First goal " + name, name + " My Second goal", name + " my third goal", name + " my biooo")
        set_about(user, '1998-05-23', 'F', 'S', 'S')
        users.append(user)
    
    events = [('Football', 'S', 'SCOT',"2021-07-23"), ('Basketball', 'S', 'LOND', "2021-05-7"), ('Boat Ride', 'F', 'LOND','2021-06-30'), ('Party', 'F', 'WALE', '2021-08-20')]
    
    for data in events:
        # not to create duplicate events, since they have random users
        if len(Events.objects.filter(name=data[0])) > 0:
            continue
        event = add_event(data[0], data[1], 'event_images/football.jpeg', data[2], random.choice(users), data[3])
        for i in range(int(random.random()*4)):
            add_participation(event, random.choice(users)).save()
        

def add_user(name, email, password):
    user, created = User.objects.get_or_create(username=name, first_name=name, last_name="family", email=email)
    if created:
        user.set_password(password)
        user.save()
    return user

def set_goals_and_bio(user, goal1, goal2, goal3, bio):
    goals = UserGoals.objects.get_or_create(user=user, goal_1=goal1,goal_2=goal2,goal_3=goal3, bio=bio)[0]
    
    goals.save()
    return goals

def set_about(user, dob, gender, status, occupation):
    about =AboutUser.objects.get_or_create(user=user,dob=dob,gender=gender,status=status,occupation=occupation)[0]
    about.save()
    return about
    
def add_event(name, category, image, location, creator, date):
    event = Events.objects.get_or_create(name=name, category=category,image=image,location=location,creator=creator, event_date=date)[0]
    event.save()
    return event

def add_participation(event, user):
    part = EventParticipation.objects.get_or_create(event=event, user=user, participating=True)[0]
    return part


if __name__ == '__main__':
    print('Starting events population script...')
    populate()
    print("done!")
    

    
    