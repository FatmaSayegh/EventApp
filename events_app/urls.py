from django.urls import path
from events_app import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'events_app'



urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('events', views.events, name='events'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('profile', views.profile, name='profile'),
    path('add_event', views.add_event, name='add_event'),
    path('disabled', views.disabled, name='disabled'),
    path('logout', views.user_logout, name='logout'),
    path('events/<slug:event_slug>/', views.view_event, name="show_event"),
    path('search/<slug:search_slug>/', views.search_event, name="search_event"),
    path('manage/<slug:manage_slug>/<int:action>', views.manage_event, name="manage_event")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)