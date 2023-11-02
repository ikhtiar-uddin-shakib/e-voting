from django.urls import path
from . import views


urlpatterns = [
    # team profile user
    path('profile/',views.profile, name='profile'),
    path('about/',views.aboutus, name='about'),
    path('how_to_use/',views.how_to_use, name="how_to_use"),
    
    # my code authentication
    path('logout/', views.account_logout, name="logout"),
    path('change_pass/', views.change_pass, name="change_pass"),
    path('login/',views.account_login, name='login'),
    path('register/',views.account_register, name='register'),
    
    
    #email varification and forgot pass
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]
