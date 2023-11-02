from django.urls import path
from . import views
from voting.views import userProfile


urlpatterns = [

    path('', userProfile, name='userProfile'),

    path('dashboard', views.dashboard, name="userDashboard"),
    # Elections
    path('electionList', views.superAdminViewElections, name="superAdminViewElections"),

    path('elections', views.viewElections, name="viewElections"),
    path('election/view', views.view_election_by_id, name="viewElection"),
    path('elections/update', views.updateElection, name="updateElection"),
    path('elections/delete', views.deleteElection, name='deleteElection'),

    # * Voters
    path('voters', views.voters, name="adminViewVoters"),
    path('voters/view', views.view_voter_by_id, name="viewVoter"),
    path('voters/delete', views.deleteVoter, name='deleteVoter'),
    path('voters/update', views.updateVoter, name="updateVoter"),

    # # * Position
    path('positions/', views.viewPositions, name='viewPositions'),
    path('position/view', views.view_position_by_id, name="viewPosition"),
    path('position/update', views.updatePosition, name="updatePosition"),
    path('position/delete', views.deletePosition, name='deletePosition'),

    # * Candidate
    path('candidates/', views.viewCandidates, name='viewCandidates'),
    path('candidate/update', views.updateCandidate, name="updateCandidate"),
    path('candidate/delete', views.deleteCandidate, name='deleteCandidate'),
    path('candidate/view', views.view_candidate_by_id, name='viewCandidate'),

    # # * Settings (Ballot Position)
    path("settings/ballot/position", views.ballot_position, name='ballot_position'),
    path("settings/ballot/position/update/<int:position_id>/<str:up_or_down>/",
         views.update_ballot_position, name='update_ballot_position'),

    # # * Votes
    path('votes/view', views.viewVotes, name='viewVotes'),
    path('votes/reset/', views.resetVote, name='resetVote'),
    path('votes/print/', views.PrintView.as_view(), name='printResult'),
    
    # Messages
    path('messages/', views.all_messages, name='messages'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]
