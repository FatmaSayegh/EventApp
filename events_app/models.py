from django.db import models

# Create your models here.


# The first model is called Users and contains the General info about the user
# id, Name, email, password

class EventUsers(models.Model):
    NAME_SIZE = 200
    MAIL_SIZE = 200
    PASSWORD_SIZE = 50
    
    # general
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=NAME_SIZE)
    mail = models.EmailField(max_length=MAIL_SIZE)
    password = models.CharField(max_length=PASSWORD_SIZE)
        


# The second model is called AboutUser and contains all the about info
class AboutUser(models.Model):
    GENDER_IDS = [('M', 'Male'), ('F', "Female"), ('O', "Other")]
    STATUS_IDS = [('S', 'Single'), ('IR', "In a Relationship"), ('M', "Married"),('W', "Widowed")]
    OCCUPATION_IDS = [('S', 'Student'), ('NAN', "Invalid"), ('W', "Worker"),('E', "Entrepreneur")]
    
    user = models.OneToOneField(EventUsers, on_delete=models.CASCADE, primary_key=True)
    #about
    dob = models.DateField()
    gender = models.CharField(max_length=1,choices=GENDER_IDS)
    status = models.CharField(max_length=2, choices=STATUS_IDS)
    occupation = models.CharField(max_length=3,choices=OCCUPATION_IDS) 
    
    


# The third model is UserGoals and contains all the goals
class UserGoals(models.Model):
    GOAL_SIZE=200
    BIO_LENGTH = 600;
    user = models.OneToOneField(EventUsers, on_delete=models.CASCADE, primary_key=True)
    # goals
    goal_1 = models.CharField(max_length=200)
    goal_2 = models.CharField(max_length=200)
    goal_3 = models.CharField(max_length=200)
    
    # biography
    bio = models.CharField(max_length=600)