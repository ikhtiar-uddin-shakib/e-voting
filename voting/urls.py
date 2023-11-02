from django.urls import path
from . import views

urlpatterns = [
    path('ballot/fetch/', views.fetch_ballot, name='fetch_ballot'),
    # path('myprofile/', views.userProfile, name='userProfile'),
    path('ballot/vote', views.show_ballot, name='show_ballot'),
    path('ballot/vote/preview', views.preview_vote, name='preview_vote'),
    path('ballot/vote/submit', views.submit_ballot, name='submit_ballot'),
]
