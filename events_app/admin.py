from django.contrib import admin

from events_app.models import AboutUser, UserGoals, Events, EventParticipation
# Register your models here.
admin.site.register(AboutUser)
admin.site.register(UserGoals)
admin.site.register(Events)
admin.site.register(EventParticipation)