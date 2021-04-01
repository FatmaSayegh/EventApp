from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


# The first model is called Users and contains the General info about the user
# id, Name, email, password

"""
class EventUsers(models.Model):
    NAME_SIZE = 200
    MAIL_SIZE = 200
    PASSWORD_SIZE = 50
"""
        


# The second model is called AboutUser and contains all the about info
class AboutUser(models.Model):
    GENDER_IDS = [('M', 'Male'), ('F', "Female"), ('O', "Other")]
    STATUS_IDS = [('S', 'Single'), ('IR', "In a Relationship"), ('M', "Married"),('W', "Widowed")]
    OCCUPATION_IDS = [('S', 'Student'), ('NAN', "Invalid"), ('W', "Worker"),('E', "Entrepreneur")]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #about
    dob = models.DateField()
    gender = models.CharField(max_length=1,choices=GENDER_IDS)
    status = models.CharField(max_length=2, choices=STATUS_IDS)
    occupation = models.CharField(max_length=3,choices=OCCUPATION_IDS) 
    
    def gender_from_id(identifier):
        for gender in AboutUser.GENDER_IDS:
            if gender[0] == identifier:
                return gender[1]
        return None
    
AboutUser.gender_from_id = staticmethod(AboutUser.gender_from_id)
  


# The third model is UserGoals and contains all the goals
class UserGoals(models.Model):
    GOAL_SIZE=200
    BIO_LENGTH = 600;
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # goals
    goal_1 = models.CharField(max_length=200)
    goal_2 = models.CharField(max_length=200)
    goal_3 = models.CharField(max_length=200)
    
    # biography
    bio = models.CharField(max_length=600)
    
    
    
"""
- Each event has a name, id, image, location
"""
class Events(models.Model):
    CATEGORIES = [('S', 'SPORTS'), ('F', "FUN"), ('O', "Other")]
    LOCATIONS = [('SCOT', 'Scotland'), ('ENGL', "ENGLAND"), ('WALE', "WALES"), ('IREL', 'IRELAND')]
    NAME_SIZE = 200
    LOCATION_LENGTH = 4
    
    event_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=3,choices=CATEGORIES, default=CATEGORIES[0]) 
    name = models.CharField(max_length=NAME_SIZE)
    image = models.FileField(upload_to = 'event_images')
    location = models.CharField(max_length=LOCATION_LENGTH, choices=LOCATIONS)
    creator = models.ForeignKey(User, on_delete=models.CASCADE) 
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        obj = Events.objects.latest('event_id')
        id = 0
        if not obj == None:
            id = obj.event_id+1
        self.slug = slugify(self.name + str(id))
        super(Events, self).save(*args, **kwargs)
    
"""
- User - Event
"""

class EventParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=False) 
    event = models.ForeignKey(Events, on_delete=models.CASCADE, primary_key=False) 
    participating = models.BooleanField()