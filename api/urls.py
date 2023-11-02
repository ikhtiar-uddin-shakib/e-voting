from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('position', ElectionViewSet)
router.register('position', PositionViewSet)
router.register('voter', VoterViewSet)
router.register('vote', VoteViewSet)
router.register('candidate', CandidateViewSet)
# router.register(r'position', views.PositionList,basename="position")
# router.register(r'voter', views.VoterList,basename="voter")
# router.register(r'candidate', views.CandidateList,basename="candidate")
# router.register(r'vote', views.VoteList,basename="vote")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('position/', PositionViewSet.as_view()),
    # path('position/<int:pk>/', PositionDeleteUpdate.as_view()),
    # path('position/', PositionList.as_view()),
    # path('position/<int:pk>/', PositionDeleteUpdate.as_view()),
    # path('voter/', VoterList.as_view()),
    # path('voter/<int:pk>/', VoterDeleteUpdate.as_view()),
    # path('candidate/', CandidateList.as_view()),
    # path('candidate/<int:pk>/', CandidateDeleteUpdate.as_view()),
    # path('vote/', VoteList.as_view()),
    # path('vote/<int:pk>/', VoteDeleteUpdate.as_view()),
]

